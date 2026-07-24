#!/usr/bin/env python3
"""Verify the orientation-free anti-fold reduction at distance 41.

The checker uses exact integer arithmetic and the standard library only.  It
does not certify any SAT/UNSAT result; its job is to verify the mathematical
reduction that turns the remaining distance-41 lane into a binary support
problem.
"""

from __future__ import annotations

from itertools import product
import json
from random import Random
from typing import Sequence

import verify_eliahou_adjacent42_repair as adjacent


FOLD = 42

Polynomial = tuple[int, ...]
Quadruple = tuple[Polynomial, Polynomial, Polynomial, Polynomial]


def antifold42(sequence: Sequence[int]) -> Polynomial:
    """Reduce a length-84/83 row modulo z^42+1."""

    if len(sequence) not in (adjacent.LONG, adjacent.SHORT):
        raise ValueError("the anti-fold expects a row of length 84 or 83")
    return tuple(
        sequence[index]
        - (
            sequence[index + FOLD]
            if index + FOLD < len(sequence)
            else 0
        )
        for index in range(FOLD)
    )


def antifold_quadruple(sequences: Quadruple) -> Quadruple:
    return tuple(antifold42(row) for row in sequences)  # type: ignore[return-value]


def negacyclic_norm_coefficients(sequences: Quadruple) -> Polynomial:
    """Return sum X(z)X(z^-1) in Z[z]/(z^42+1)."""

    result = [0] * FOLD
    for sequence in sequences:
        if len(sequence) != FOLD:
            raise ValueError("negacyclic rows must have length 42")
        for left, right in product(range(FOLD), repeat=2):
            exponent = left - right
            wrap_sign = 1
            if exponent < 0:
                exponent += FOLD
                wrap_sign = -1
            result[exponent] += (
                wrap_sign * sequence[left] * sequence[right]
            )
    return tuple(result)


def antifold_correlations_from_aperiodic(
    correlations: Sequence[int],
) -> Polynomial:
    """Reduce the aperiodic norm coefficients modulo z^42+1."""

    if len(correlations) != adjacent.LONG:
        raise ValueError("expected lags 0 through 83")
    result = [correlations[0] - 2 * correlations[42]]
    for lag in range(1, 21):
        result.append(
            correlations[lag]
            - correlations[42 - lag]
            - correlations[42 + lag]
            + correlations[84 - lag]
        )
    result.append(0)
    result.extend(-value for value in reversed(result[1:21]))
    return tuple(result)


def opposite_separation_pairs(sequences: Quadruple) -> int:
    return sum(
        row[index] == -row[index + FOLD]
        for row in sequences
        for index in range(len(row) - FOLD)
    )


def q_pair_cells(block: str, first_index: int) -> tuple[int, int]:
    length = adjacent.LONG if block == "L" else adjacent.SHORT
    return first_index % FOLD, (length - 1 - first_index) % FOLD


def s_support_cells(block: str) -> tuple[int, ...]:
    if block == "L":
        return tuple(range(41))
    if block == "S":
        return tuple(range(1, 40))
    raise ValueError("block must be L or S")


def available_s_support_cells(
    q_block: str, q_index: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    removed = set(q_pair_cells(q_block, q_index))
    long_cells = tuple(
        cell
        for cell in s_support_cells("L")
        if q_block != "L" or cell not in removed
    )
    short_cells = tuple(
        cell
        for cell in s_support_cells("S")
        if q_block != "S" or cell not in removed
    )
    return long_cells, short_cells


def boundary_antifold_rows(
    q_block: str,
    q_index: int,
    long_support: Sequence[int],
    short_support: Sequence[int],
) -> Quadruple:
    """Build anti-fold rows from the q pair and binary s supports."""

    rows = [list(row) for row in antifold_quadruple(adjacent.eliahou_base())]
    active_row = 1 if q_block == "L" else 3
    for cell in q_pair_cells(q_block, q_index):
        rows[active_row][cell] = 0
    for block, support in (("L", long_support), ("S", short_support)):
        first_row = 0 if block == "L" else 2
        for cell in support:
            rows[first_row][cell] = 0
            rows[first_row + 1][cell] = 0
    return tuple(tuple(row) for row in rows)  # type: ignore[return-value]


def flip_original_endpoint(
    sequences: Quadruple, row: int, coordinate: int
) -> Quadruple:
    changed = [list(values) for values in sequences]
    changed[row][coordinate] *= -1
    return tuple(tuple(values) for values in changed)  # type: ignore[return-value]


def verify_orientation_independence() -> None:
    """Check both endpoint choices for all 80 eligible s half-pairs."""

    base = adjacent.eliahou_base()
    for block, cells in (
        ("L", s_support_cells("L")),
        ("S", s_support_cells("S")),
    ):
        first_row = 0 if block == "L" else 2
        for cell in cells:
            expected = [list(row) for row in antifold_quadruple(base)]
            expected[first_row][cell] = 0
            expected[first_row + 1][cell] = 0
            expected_value: Quadruple = tuple(
                tuple(row) for row in expected
            )  # type: ignore[assignment]

            lower = base
            upper = base
            for row in (first_row, first_row + 1):
                lower = flip_original_endpoint(lower, row, cell)
                upper = flip_original_endpoint(upper, row, cell + FOLD)
            assert antifold_quadruple(lower) == expected_value
            assert antifold_quadruple(upper) == expected_value


def verify() -> dict[str, object]:
    base = adjacent.eliahou_base()
    correlations = adjacent.base_correlations(base)
    seed_antifold = antifold_quadruple(base)
    direct = negacyclic_norm_coefficients(seed_antifold)
    derived = antifold_correlations_from_aperiodic(correlations)
    assert direct == derived
    assert {
        index: value for index, value in enumerate(direct) if value
    } == {
        0: 654,
        4: -512,
        8: 384,
        12: -256,
        16: 128,
        26: -128,
        30: 256,
        34: -384,
        38: 512,
    }
    assert len(direct) == FOLD
    assert opposite_separation_pairs(base) == 163
    assert direct[0] == 2 + 4 * opposite_separation_pairs(base)

    rng = Random(6684242)
    for _ in range(24):
        fixture: Quadruple = (
            tuple(rng.randrange(-3, 4) for _ in range(adjacent.LONG)),
            tuple(rng.randrange(-3, 4) for _ in range(adjacent.LONG)),
            tuple(rng.randrange(-3, 4) for _ in range(adjacent.SHORT)),
            tuple(rng.randrange(-3, 4) for _ in range(adjacent.SHORT)),
        )
        assert negacyclic_norm_coefficients(
            antifold_quadruple(fixture)
        ) == antifold_correlations_from_aperiodic(
            adjacent.base_correlations(fixture)
        )

    verify_orientation_independence()

    long_catalog, short_catalog = adjacent.q_pair_signature_catalogs()
    surviving_pairs = [
        ("L", index)
        for signature in ((-2, 0), (0, 2))
        for index in long_catalog[signature]
    ] + [
        ("S", index)
        for index in short_catalog[(0, 0)]
    ]
    assert len(surviving_pairs) == 39
    unique_instances = {
        (block, frozenset(q_pair_cells(block, index)))
        for block, index in surviving_pairs
    }
    assert len(unique_instances) == 30

    short_indices = set(short_catalog[(0, 0)])
    assert short_indices == set(range(2, 20, 2)) | set(range(22, 40, 2))
    for index in range(2, 20, 2):
        reflected_index = 40 - index
        assert q_pair_cells("S", index) == tuple(
            reversed(q_pair_cells("S", reflected_index))
        )
        long_cells, short_cells = available_s_support_cells("S", index)
        long_support = long_cells[:19]
        short_support = short_cells[:20]
        assert boundary_antifold_rows(
            "S", index, long_support, short_support
        ) == boundary_antifold_rows(
            "S", reflected_index, long_support, short_support
        )

    candidate_counts = {}
    for block, index in surviving_pairs:
        long_cells, short_cells = available_s_support_cells(block, index)
        count = len(long_cells) + len(short_cells)
        candidate_counts[count] = candidate_counts.get(count, 0) + 1
        assert count in (78, 79)

        # Any 39-cell support zeros 78 anti-fold entries.  The q pair zeros
        # two more, so zero-lag energy is always 654-80*4=334.
        take_long = min(20, len(long_cells))
        long_support = long_cells[:take_long]
        short_support = short_cells[: 39 - take_long]
        rows = boundary_antifold_rows(
            block, index, long_support, short_support
        )
        assert negacyclic_norm_coefficients(rows)[0] == 334

    assert candidate_counts == {78: 38, 79: 1}

    return {
        "status": (
            "verified orientation-free binary anti-fold reduction; "
            "no H(668) claimed"
        ),
        "seed_antifold_energy": direct[0],
        "seed_opposite_separation42_pairs": 163,
        "target_antifold_energy": 334,
        "distance41_q_pairs": len(surviving_pairs),
        "distinct_binary_antifold_instances": len(unique_instances),
        "distance41_outer_profiles": 78,
        "binary_s_support_size": 39,
        "available_support_cells_distribution": candidate_counts,
        "necessary_equation": (
            "sum N_-(D_A,D_B,D_C,D_D)=334 in Z[z]/(z^42+1)"
        ),
        "scope": (
            "the anti-fold equation is necessary; this checker does not "
            "certify SAT or UNSAT of its 78 boundary cases"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
