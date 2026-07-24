#!/usr/bin/env python3
"""Verify the first binary lift of the distance-41 anti-fold problem.

This checker uses exact integer arithmetic and the Python standard library.
It derives a rank-21 affine system (including retained-weight parity) for
each reciprocal-q case and computes selected coset weight counts by the
MacWilliams transform.  The layer is necessary but not sufficient.
"""

from __future__ import annotations

from collections import Counter
import json
from random import Random
from typing import Sequence

import verify_eliahou_adjacent42_repair as adjacent
import verify_eliahou_antifold42 as antifold


FOLD = 42
TARGET_SUPPORT = 39

Polynomial = tuple[int, ...]
Variable = tuple[str, int]
BinaryEquation = tuple[int, int]

EXPECTED_COUNTS = {
    ("L", 0): 51_310_052_181_007_034,
    ("L", 2): 25_953_942_447_362_002,
    ("S", 2): 25_968_969_218_639_808,
}


def surviving_q_pairs() -> tuple[tuple[str, int], ...]:
    long_catalog, short_catalog = adjacent.q_pair_signature_catalogs()
    result = [
        ("L", index)
        for signature in ((-2, 0), (0, 2))
        for index in long_catalog[signature]
    ]
    result.extend(("S", index) for index in short_catalog[(0, 0)])
    if len(result) != 39:
        raise AssertionError("the root-compatible q-pair catalog changed")
    return tuple(result)


def pair_sum(left: Sequence[int], right: Sequence[int]) -> Polynomial:
    if any((a + b) % 2 for a, b in zip(left, right)):
        raise ValueError("row sum is not even")
    return tuple((a + b) // 2 for a, b in zip(left, right))


def pair_difference(
    left: Sequence[int], right: Sequence[int]
) -> Polynomial:
    if any((a - b) % 2 for a, b in zip(left, right)):
        raise ValueError("row difference is not even")
    return tuple((a - b) // 2 for a, b in zip(left, right))


def normalized_pair_rows(
    rows: Sequence[Sequence[int]],
) -> tuple[Polynomial, Polynomial, Polynomial, Polynomial]:
    """Return P=(A+B)/2, Q=(C+D)/2, R=(A-B)/2, S=(C-D)/2."""

    return (
        pair_sum(rows[0], rows[1]),
        pair_sum(rows[2], rows[3]),
        pair_difference(rows[0], rows[1]),
        pair_difference(rows[2], rows[3]),
    )


def available_variables(block: str, index: int) -> tuple[Variable, ...]:
    long_cells, short_cells = antifold.available_s_support_cells(
        block, index
    )
    return tuple(
        [("L", cell) for cell in long_cells]
        + [("S", cell) for cell in short_cells]
    )


def q_adjusted_seed(block: str, index: int) -> list[list[int]]:
    rows = [
        list(row)
        for row in antifold.antifold_quadruple(adjacent.eliahou_base())
    ]
    active_row = 1 if block == "L" else 3
    for cell in antifold.q_pair_cells(block, index):
        rows[active_row][cell] = 0
    return rows


def sparse_and_variable_rows(
    block: str, index: int
) -> tuple[
    tuple[Polynomial, Polynomial, Polynomial, Polynomial],
    tuple[Variable, ...],
    list[list[int]],
]:
    rows = q_adjusted_seed(block, index)
    variables = available_variables(block, index)
    sparse = [row[:] for row in rows]
    for variable_block, cell in variables:
        first_row = 0 if variable_block == "L" else 2
        sparse[first_row][cell] = 0
        sparse[first_row + 1][cell] = 0
    return normalized_pair_rows(sparse), variables, rows


def add_scaled_basis(
    base: Polynomial, cell: int, value: int
) -> Polynomial:
    result = list(base)
    result[cell] += 2 * value
    return tuple(result)


def first_bit_system(
    block: str, index: int
) -> tuple[int, tuple[BinaryEquation, ...]]:
    """Return variable count and an exact F_2 system on retained cells."""

    (p_zero, q_zero, r_value, s_value), variables, raw = (
        sparse_and_variable_rows(block, index)
    )
    fixed = antifold.negacyclic_norm_coefficients(
        (p_zero, q_zero, r_value, s_value)
    )
    target = (167,) + (0,) * (FOLD - 1)
    if any((wanted - value) % 2 for wanted, value in zip(target, fixed)):
        raise AssertionError("the normalized constant term is not even")
    right_hand_side = tuple(
        ((wanted - value) // 2) & 1
        for wanted, value in zip(target, fixed)
    )

    columns: list[tuple[int, ...]] = []
    for variable_block, cell in variables:
        first_row = 0 if variable_block == "L" else 2
        sign = raw[first_row][cell] // 2
        if sign not in (-1, 1):
            raise AssertionError("a variable cell is not a seed-opposite pair")
        trial_p = (
            add_scaled_basis(p_zero, cell, sign)
            if variable_block == "L"
            else p_zero
        )
        trial_q = (
            add_scaled_basis(q_zero, cell, sign)
            if variable_block == "S"
            else q_zero
        )
        trial = antifold.negacyclic_norm_coefficients(
            (trial_p, trial_q, r_value, s_value)
        )
        if any((value - base) % 2 for value, base in zip(trial, fixed)):
            raise AssertionError("a first-bit column is not integral")
        columns.append(
            tuple(
                ((value - base) // 2) & 1
                for value, base in zip(trial, fixed)
            )
        )

    equations = []
    for coefficient in range(FOLD):
        mask = sum(
            columns[column][coefficient] << column
            for column in range(len(variables))
        )
        equations.append((mask, right_hand_side[coefficient]))

    # The variables mark retained cells.  Selecting 39 cells leaves n-39.
    equations.append(
        ((1 << len(variables)) - 1, (len(variables) - TARGET_SUPPORT) & 1)
    )
    return len(variables), tuple(equations)


def row_reduce(
    equations: Sequence[BinaryEquation],
) -> tuple[BinaryEquation, ...]:
    pivots: dict[int, BinaryEquation] = {}
    for original_mask, original_value in equations:
        mask = original_mask
        value = original_value
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (mask, value)
                break
            pivot_mask, pivot_value = pivots[pivot]
            mask ^= pivot_mask
            value ^= pivot_value
        if not mask and value:
            raise ValueError("inconsistent binary system")
    return tuple(pivots[pivot] for pivot in sorted(pivots, reverse=True))


def krawtchouk(length: int, degree: int, weight: int) -> int:
    if degree == 0:
        return 1
    previous = 1
    current = length - 2 * weight
    if degree == 1:
        return current
    for index in range(1, degree):
        following = (
            (length - 2 * weight) * current
            - (length - index + 1) * previous
        ) // (index + 1)
        previous, current = current, following
    return current


def affine_weight_count(
    length: int,
    basis: Sequence[BinaryEquation],
    target_weight: int,
) -> int:
    """Count one affine-code weight using the exact MacWilliams transform."""

    positive: Counter[int] = Counter()
    negative: Counter[int] = Counter()
    word = 0
    phase = 0
    previous_gray = 0
    positive[0] = 1
    for counter in range(1, 1 << len(basis)):
        gray = counter ^ (counter >> 1)
        changed = gray ^ previous_gray
        row = (changed & -changed).bit_length() - 1
        word ^= basis[row][0]
        phase ^= basis[row][1]
        # Keep the checker compatible with the older system Python used by
        # some clean-room replay environments.
        (negative if phase else positive)[bin(word).count("1")] += 1
        previous_gray = gray

    total = sum(
        (positive[weight] - negative[weight])
        * krawtchouk(length, target_weight, weight)
        for weight in set(positive) | set(negative)
    )
    divisor = 1 << len(basis)
    if total % divisor:
        raise AssertionError("the MacWilliams count is not integral")
    return total // divisor


def verify_pair_transform() -> None:
    rng = Random(668422)
    cases = surviving_q_pairs()
    for _ in range(24):
        block, index = cases[rng.randrange(len(cases))]
        variables = available_variables(block, index)
        support = rng.sample(variables, TARGET_SUPPORT)
        long_support = [cell for side, cell in support if side == "L"]
        short_support = [cell for side, cell in support if side == "S"]
        rows = antifold.boundary_antifold_rows(
            block, index, long_support, short_support
        )
        original = antifold.negacyclic_norm_coefficients(rows)
        normalized = antifold.negacyclic_norm_coefficients(
            normalized_pair_rows(rows)
        )
        if original != tuple(2 * value for value in normalized):
            raise AssertionError("the row-pair norm transform failed")
        if original[0] != 334 or normalized[0] != 167:
            raise AssertionError("the automatic zero-lag target changed")


def verify() -> dict[str, object]:
    verify_pair_transform()
    ranks: Counter[tuple[int, int]] = Counter()
    bases: dict[tuple[str, int], tuple[int, tuple[BinaryEquation, ...]]] = {}
    for case in surviving_q_pairs():
        length, equations = first_bit_system(*case)
        basis = row_reduce(equations)
        ranks[(length, len(basis))] += 1
        bases[case] = (length, basis)
    if ranks != Counter({(78, 21): 38, (79, 21): 1}):
        raise AssertionError("the first-bit rank census changed")

    pinned_counts = {}
    for case, expected in EXPECTED_COUNTS.items():
        length, basis = bases[case]
        target_weight = length - TARGET_SUPPORT
        actual = affine_weight_count(length, basis, target_weight)
        if actual != expected:
            raise AssertionError(
                f"the pinned affine weight count changed for {case}"
            )
        pinned_counts[f"{case[0]}{case[1]}"] = actual

    return {
        "status": (
            "verified rank-21 necessary first-bit layer; "
            "no distance-41 exclusion claimed"
        ),
        "q_pair_cases": len(bases),
        "distinct_antifold_instances": 30,
        "rank_histogram": {
            f"length_{length}_rank_{rank}": count
            for (length, rank), count in sorted(ranks.items())
        },
        "pinned_target_weight_counts": pinned_counts,
        "scope": (
            "the affine layer is necessary but leaves many supports; "
            "the integer anti-fold equations remain"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
