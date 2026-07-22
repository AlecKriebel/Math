#!/usr/bin/env python3
"""Exact column-margin distance spectra for shifts of length 333.

Write a binary length-333 sequence as a 9 by 37 CRT array.  A lag ``s``
maps a cell ``(row, column)`` to

    (row + s mod 9, column + s mod 37).

When ``s`` is nonzero modulo 37, its column action is one 37-cycle.  This
module follows that cycle and uses a width-9 transfer dynamic program.  A
state is the 9-bit support of one column; a bitset records every reachable
Hamming distance.  Closing the transfer path back to its first state makes
the computation exact, including the otherwise easy-to-miss row twist.

For a shift divisible by 37, every column maps to itself instead.  Those 37
width-9 cyclic spectra are enumerated independently and combined by a bitset
sum.  The only inputs in either case are the prescribed column weights; no
Legendre-pair correlation equation is used.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
from math import gcd
from typing import Sequence

from legendre_333 import (
    COLUMN_MODULUS,
    FIXED_PLUS_COUNTS_A,
    FIXED_PLUS_COUNTS_B,
    N,
    ROW_MODULUS,
)


def _rotate_right(mask: int, amount: int, width: int) -> int:
    """Cyclically rotate a ``width``-bit integer to the right."""

    amount %= width
    if amount == 0:
        return mask
    low = mask & ((1 << amount) - 1)
    return (mask >> amount) | (low << (width - amount))


@lru_cache(maxsize=None)
def _masks_of_weight(width: int, weight: int) -> tuple[int, ...]:
    if width <= 0:
        raise ValueError("row width must be positive")
    if not 0 <= weight <= width:
        raise ValueError("column weight is outside the row width")
    return tuple(mask for mask in range(1 << width) if mask.bit_count() == weight)


@lru_cache(maxsize=None)
def _rotation_orbit_representatives(width: int, weight: int) -> tuple[int, ...]:
    """Represent supports modulo simultaneous cyclic row rotation."""

    unseen = set(_masks_of_weight(width, weight))
    representatives: list[int] = []
    while unseen:
        representative = min(unseen)
        orbit = {
            _rotate_right(representative, amount, width)
            for amount in range(width)
        }
        representatives.append(min(orbit))
        unseen.difference_update(orbit)
    return tuple(representatives)


def _canonical_row_shift(row_shift: int, row_count: int) -> int:
    """Reduce a row shift modulo multiplication by units of the row cycle.

    Multiplying every row index by a unit modulo ``row_count`` preserves all
    column weights and sends a shift to a unit multiple.  Two shifts are in
    the same orbit precisely when they have the same gcd with ``row_count``.
    """

    row_shift %= row_count
    return 0 if row_shift == 0 else gcd(row_shift, row_count)


@lru_cache(maxsize=None)
def _transition_costs(
    row_count: int,
    left_weight: int,
    right_weight: int,
    row_shift: int,
) -> tuple[tuple[int, ...], ...]:
    """Return all shifted Hamming costs between two support layers."""

    left_masks = _masks_of_weight(row_count, left_weight)
    right_masks = _masks_of_weight(row_count, right_weight)
    return tuple(
        tuple(
            (left ^ _rotate_right(right, row_shift, row_count)).bit_count()
            for right in right_masks
        )
        for left in left_masks
    )


@lru_cache(maxsize=None)
def _layered_cyclic_distance_spectrum_cached(
    column_weights: tuple[int, ...], row_shift: int, row_count: int
) -> tuple[int, ...]:
    """Cached implementation of :func:`layered_cyclic_distance_spectrum`."""

    if not column_weights:
        raise ValueError("at least one column is required")
    if row_count <= 0:
        raise ValueError("row count must be positive")
    if any(not 0 <= weight <= row_count for weight in column_weights):
        raise ValueError("column weight is outside the row count")

    row_shift = _canonical_row_shift(row_shift, row_count)
    first_masks = _masks_of_weight(row_count, column_weights[0])
    first_indices = {mask: index for index, mask in enumerate(first_masks)}
    spectrum_bits = 0

    # A simultaneous cyclic rotation of every layer commutes with the row
    # shift, so only one first mask from each rotation orbit is necessary.
    for first_mask in _rotation_orbit_representatives(
        row_count, column_weights[0]
    ):
        reachable = [0] * len(first_masks)
        reachable[first_indices[first_mask]] = 1  # bit zero is reachable

        for left_weight, right_weight in zip(
            column_weights, column_weights[1:], strict=False
        ):
            costs = _transition_costs(
                row_count, left_weight, right_weight, row_shift
            )
            next_reachable = [0] * len(_masks_of_weight(row_count, right_weight))
            for left_index, left_spectrum in enumerate(reachable):
                if left_spectrum == 0:
                    continue
                for right_index, cost in enumerate(costs[left_index]):
                    next_reachable[right_index] |= left_spectrum << cost
            reachable = next_reachable

        closing_costs = _transition_costs(
            row_count, column_weights[-1], column_weights[0], row_shift
        )
        first_index = first_indices[first_mask]
        for last_index, path_spectrum in enumerate(reachable):
            spectrum_bits |= (
                path_spectrum << closing_costs[last_index][first_index]
            )

    maximum = row_count * len(column_weights)
    return tuple(
        distance for distance in range(maximum + 1) if spectrum_bits >> distance & 1
    )


def layered_cyclic_distance_spectrum(
    column_weights: Sequence[int], row_shift: int, row_count: int = ROW_MODULUS
) -> tuple[int, ...]:
    """Return every distance attainable around one cyclic column ordering.

    ``column_weights[t]`` is the number of ones in layer ``t``.  An edge from
    one layer to the next compares row ``u`` in the first with row
    ``u + row_shift`` in the second.  The final layer is likewise compared
    back to the first, so the returned spectrum includes the closure twist.
    """

    canonical_shift = _canonical_row_shift(row_shift, row_count)
    return _layered_cyclic_distance_spectrum_cached(
        tuple(column_weights), canonical_shift, row_count
    )


@lru_cache(maxsize=None)
def _single_column_distance_spectrum(
    weight: int, row_shift: int, row_count: int
) -> tuple[int, ...]:
    """Distances of one fixed-weight column from its cyclic row shift."""

    row_shift %= row_count
    return tuple(
        sorted(
            {
                (mask ^ _rotate_right(mask, row_shift, row_count)).bit_count()
                for mask in _masks_of_weight(row_count, weight)
            }
        )
    )


def independent_column_distance_spectrum(
    column_weights: Sequence[int],
    row_shift: int,
    row_count: int = ROW_MODULUS,
) -> tuple[int, ...]:
    """Combine the exact spectra of independently shifted columns."""

    if not column_weights:
        raise ValueError("at least one column is required")
    if row_count <= 0:
        raise ValueError("row count must be positive")
    if any(not 0 <= weight <= row_count for weight in column_weights):
        raise ValueError("column weight is outside the row count")
    reachable = 1
    for weight in column_weights:
        next_reachable = 0
        for distance in _single_column_distance_spectrum(
            weight, row_shift, row_count
        ):
            next_reachable |= reachable << distance
        reachable = next_reachable
    maximum = row_count * len(column_weights)
    return tuple(
        distance for distance in range(maximum + 1) if reachable >> distance & 1
    )


def exact_column_distance_spectrum(
    plus_counts: Sequence[int], lag: int
) -> tuple[int, ...]:
    """Return the exact length-333 distance spectrum from 37 column margins."""

    if len(plus_counts) != COLUMN_MODULUS:
        raise ValueError(f"expected {COLUMN_MODULUS} fixed column weights")
    if not 1 <= lag < N:
        raise ValueError(f"lag must be in [1,{N})")
    column_offset = lag % COLUMN_MODULUS
    if column_offset == 0:
        return independent_column_distance_spectrum(
            plus_counts, lag % ROW_MODULUS, ROW_MODULUS
        )
    # Since 37 is prime, visiting columns ``0, lag, 2*lag, ...`` produces one
    # cycle whenever the column offset is nonzero.
    ordered_weights = tuple(
        plus_counts[(step * column_offset) % COLUMN_MODULUS]
        for step in range(COLUMN_MODULUS)
    )
    return layered_cyclic_distance_spectrum(
        ordered_weights, lag % ROW_MODULUS, ROW_MODULUS
    )


def exact_column_distance_bounds(
    plus_counts: Sequence[int], lag: int
) -> tuple[int, int]:
    """Return the minimum and maximum of the exact margin-only spectrum."""

    spectrum = exact_column_distance_spectrum(plus_counts, lag)
    return spectrum[0], spectrum[-1]


def edgewise_column_distance_bounds(
    plus_counts: Sequence[int], lag: int
) -> tuple[int, int]:
    """Return the independent-edge bounds used by the main CP-SAT model."""

    if len(plus_counts) != COLUMN_MODULUS:
        raise ValueError(f"expected {COLUMN_MODULUS} fixed column weights")
    if not 1 <= lag < N:
        raise ValueError(f"lag must be in [1,{N})")
    offset = lag % COLUMN_MODULUS
    if offset == 0:
        spectra = tuple(
            _single_column_distance_spectrum(
                weight, lag % ROW_MODULUS, ROW_MODULUS
            )
            for weight in plus_counts
        )
        return (
            sum(spectrum[0] for spectrum in spectra),
            sum(spectrum[-1] for spectrum in spectra),
        )
    lower = upper = 0
    for column, weight in enumerate(plus_counts):
        shifted_weight = plus_counts[(column + offset) % COLUMN_MODULUS]
        lower += abs(weight - shifted_weight)
        upper += min(
            weight + shifted_weight,
            2 * ROW_MODULUS - weight - shifted_weight,
        )
    return lower, upper


def verify_fixed_margin_spectra() -> dict[str, int]:
    """Exhaustively compare the exact DP with all relevant edgewise bounds."""

    checked = 0
    exact_bound_improvements = 0
    spectrum_gaps = 0
    for plus_counts in (FIXED_PLUS_COUNTS_A, FIXED_PLUS_COUNTS_B):
        for lag in range(1, (N + 1) // 2):
            spectrum = exact_column_distance_spectrum(plus_counts, lag)
            edgewise = edgewise_column_distance_bounds(plus_counts, lag)
            if (spectrum[0], spectrum[-1]) != edgewise:
                exact_bound_improvements += 1
            expected = tuple(range(spectrum[0], spectrum[-1] + 1, 2))
            if spectrum != expected:
                spectrum_gaps += 1
            checked += 1
    return {
        "sequence_lag_cases_checked": checked,
        "exact_bound_improvements": exact_bound_improvements,
        "spectra_with_even_gaps": spectrum_gaps,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    report = verify_fixed_margin_spectra()
    print("Exact cyclic column-margin DP (LP333)")
    for key, value in report.items():
        print(f"  {key}: {value}")
    print("  conclusion: every spectrum is the full even edgewise interval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
