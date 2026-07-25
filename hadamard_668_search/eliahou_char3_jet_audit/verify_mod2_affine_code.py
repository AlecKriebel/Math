#!/usr/bin/env python3
"""Derive and verify the exact characteristic-two affine parameterization."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from math import comb
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
sys.path[:0] = [str(JET), str(SEARCH)]

import search_char3_local as local  # noqa: E402
import search_char3_cp_sat as cp  # noqa: E402


def rref_parameterization(
    matrix: np.ndarray, rhs: np.ndarray
) -> tuple[list[int], list[int], np.ndarray, np.ndarray]:
    """Return pivots, free columns, particular point, and null basis."""

    work = np.column_stack(
        ((matrix & 1).astype(np.uint8), (rhs & 1).astype(np.uint8))
    )
    row = 0
    pivots = []
    for column in range(matrix.shape[1]):
        candidates = np.flatnonzero(work[row:, column])
        if not len(candidates):
            continue
        pivot = row + int(candidates[0])
        work[[row, pivot]] = work[[pivot, row]]
        for other in np.flatnonzero(work[:, column]):
            if other != row:
                work[other] ^= work[row]
        pivots.append(column)
        row += 1
        if row == matrix.shape[0]:
            break
    assert not any(
        not np.any(line[:-1]) and line[-1] for line in work
    )
    free = [
        column
        for column in range(matrix.shape[1])
        if column not in pivots
    ]
    particular = np.zeros(matrix.shape[1], dtype=np.uint8)
    for equation, pivot in enumerate(pivots):
        particular[pivot] = work[equation, -1]
    basis = np.zeros((len(free), matrix.shape[1]), dtype=np.uint8)
    for basis_index, free_column in enumerate(free):
        basis[basis_index, free_column] = 1
        for equation, pivot in enumerate(pivots):
            basis[basis_index, pivot] = work[equation, free_column]
    assert np.array_equal((matrix @ particular) & 1, rhs & 1)
    assert not np.any((matrix @ basis.T) & 1)
    return pivots, free, particular, basis


def audit(case_number: int) -> dict:
    case, keys, _, constant, linear, quadratic = local.arrays(case_number)
    assert not np.any(quadratic & 1)
    affine = (linear & 1).astype(np.uint8)
    rhs = (-constant & 1).astype(np.uint8)
    with_weight = np.vstack(
        [affine, np.ones((1, len(keys)), dtype=np.uint8)]
    )
    with_weight_rhs = np.append(rhs, 1).astype(np.uint8)
    pivots, free, particular, basis = rref_parameterization(
        with_weight, with_weight_rhs
    )
    assert len(pivots) == 21
    assert len(free) == len(keys) - 21

    groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for variable in range(len(keys)):
        groups[
            tuple(map(int, affine[:, variable]))
        ].append(variable)
    group_sizes = sorted(map(len, groups.values()))
    expected_sizes = [2] * 39 if case_number == 26 else [1] + [2] * 39
    assert group_sizes == expected_sizes
    quotient = np.array(list(groups), dtype=np.uint8).T
    quotient_augmented = np.vstack(
        [quotient, np.ones((1, len(groups)), dtype=np.uint8)]
    )
    _, quotient_free, quotient_particular, quotient_basis = (
        rref_parameterization(
        quotient_augmented, with_weight_rhs
        )
    )
    expected_quotient_dimension = 18 if case_number == 26 else 19
    assert len(quotient_free) == expected_quotient_dimension

    # Enumerate only the small parity quotient, not the 57/58 dimensional
    # full affine code.  Lift counts to exact weight 39 are then closed-form.
    pair_positions = [
        index
        for index, group in enumerate(groups.values())
        if len(group) == 2
    ]
    singleton_positions = [
        index
        for index, group in enumerate(groups.values())
        if len(group) == 1
    ]
    quotient_weight_enumerator: dict[int, int] = defaultdict(int)
    fixed_weight_supports = 0
    point = quotient_particular.copy()
    previous_gray = 0
    for integer in range(1 << len(quotient_free)):
        if integer:
            gray = integer ^ (integer >> 1)
            changed = gray ^ previous_gray
            basis_index = changed.bit_length() - 1
            point ^= quotient_basis[basis_index]
            previous_gray = gray
        quotient_weight_enumerator[int(point.sum())] += 1
        odd_pairs = int(point[pair_positions].sum())
        even_pairs = len(pair_positions) - odd_pairs
        singleton_weight = int(point[singleton_positions].sum())
        remaining = 39 - singleton_weight - odd_pairs
        if remaining >= 0 and remaining % 2 == 0:
            doubled_pairs = remaining // 2
            if doubled_pairs <= even_pairs:
                fixed_weight_supports += (
                    (1 << odd_pairs) * comb(even_pairs, doubled_pairs)
                )

    payload = {
        "case": case_number,
        "block": case.block,
        "q_index": case.index,
        "ordered_keys": [[block, cell] for block, cell in keys],
        "pivots": pivots,
        "free": free,
        "particular": particular.tolist(),
        "basis": basis.tolist(),
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()
    return {
        "case": case_number,
        "block": case.block,
        "q_index": case.index,
        "support_variables": len(keys),
        "normalized_equations": 20,
        "odd_quadratic_coefficients": int(
            np.count_nonzero(quadratic & 1)
        ),
        "affine_rank": 20,
        "weight_parity_rank": len(pivots),
        "weight_parity_dimension": len(free),
        "syndrome_groups": len(groups),
        "syndrome_group_size_histogram": {
            str(size): group_sizes.count(size)
            for size in sorted(set(group_sizes))
        },
        "quotient_affine_dimension": len(quotient_free),
        "fiber_dimension": sum(size - 1 for size in group_sizes),
        "quotient_weight_enumerator": {
            str(weight): count
            for weight, count in sorted(
                quotient_weight_enumerator.items()
            )
        },
        "exact_weight_39_supports": fixed_weight_supports,
        "particular_weight": int(particular.sum()),
        "basis_weight_histogram": {
            str(weight): int(
                np.count_nonzero(np.sum(basis, axis=1) == weight)
            )
            for weight in sorted(set(map(int, np.sum(basis, axis=1))))
        },
        "parameterization_sha256": hashlib.sha256(canonical).hexdigest(),
    }


def replay_best_point() -> None:
    payload = json.loads(
        (HERE / "CASE26_MOD2_BEST_DEFECT2.json").read_text()
    )
    case_number = int(payload["case"])
    case, keys, equations, constant, linear, quadratic = local.arrays(
        case_number
    )
    assert case.block == payload["block"]
    assert case.index == payload["q_index"]
    selected = {
        (str(block), int(cell))
        for block, cell in payload["selected"]
    }
    assert len(selected) == 39
    chosen = np.array(
        [int(key in selected) for key in keys], dtype=np.int8
    )
    values = local.exact_values(
        chosen, constant, linear, quadratic
    )
    assert values.tolist() == payload["normalized_residuals"]
    assert not np.any(values & 1)
    assert int(np.count_nonzero(np.remainder(values, 3))) == 2
    # A direct physical replay must agree with the expanded equations.
    direct = cp.replay(case, tuple(sorted(selected)), equations, 2)
    assert direct["normalized_residuals"] == values.tolist()


def main() -> None:
    results = [audit(case_number) for case_number in (0, 26)]
    assert [record["weight_parity_dimension"] for record in results] == [
        58,
        57,
    ]
    replay_best_point()
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
