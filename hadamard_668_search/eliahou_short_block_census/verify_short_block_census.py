#!/usr/bin/env python3
"""Derive and verify the nine all-short-block Eliahou census models.

This is independent of ``eliahou_global_quotient_plan``: it rebuilds every
integer quadratic from the original case definitions, performs its own
binary elimination, proves the four-clique split, and derives the dynamic
reflection-gauge work count.  It may emit the binary array payload consumed
by the C++ range kernel, but it never performs a full census.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import struct
import sys
from typing import Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
AUDIT = SEARCH / "eliahou_char3_jet_audit"
sys.path[:0] = [str(JET), str(AUDIT), str(SEARCH)]

import search_char3_local as local  # noqa: E402
import search_eliahou_antifold_sat as anti  # noqa: E402


CASES = tuple(range(21, 30))
EXPECTED_Q_INDICES = tuple(range(2, 20, 2))
CERTIFICATE = HERE / "SHORT_BLOCK_CERTIFICATE.json"
MAGIC = b"H668GQ2\0"
QUOTIENT_STATES = 1 << 18
NORMAL_ROWS_PER_CASE = 412_316_860_416
EXCEPTIONAL_SURCHARGE = 786_432


def compact_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":")
        ).encode("ascii")
    ).hexdigest()


def rank_mod2(matrix: np.ndarray) -> int:
    work = np.asarray(matrix, dtype=np.uint8).copy() & 1
    row = 0
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        pivot = row + int(choices[0])
        work[[row, pivot]] = work[[pivot, row]]
        for other in np.flatnonzero(work[:, column]):
            if other != row:
                work[other] ^= work[row]
        row += 1
        if row == work.shape[0]:
            break
    return row


def affine_parameterization(
    matrix: np.ndarray, rhs: np.ndarray
) -> tuple[tuple[int, ...], tuple[int, ...], np.ndarray, np.ndarray]:
    """Deterministic binary RREF, particular point, and row null basis."""

    matrix = np.asarray(matrix, dtype=np.uint8) & 1
    rhs = np.asarray(rhs, dtype=np.uint8) & 1
    work = np.column_stack((matrix, rhs))
    row = 0
    pivots: list[int] = []
    for column in range(matrix.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        pivot = row + int(choices[0])
        work[[row, pivot]] = work[[pivot, row]]
        for other in np.flatnonzero(work[:, column]):
            if other != row:
                work[other] ^= work[row]
        pivots.append(column)
        row += 1
        if row == matrix.shape[0]:
            break
    if any(
        not np.any(equation[:-1]) and equation[-1]
        for equation in work
    ):
        raise ValueError("binary affine system is inconsistent")
    free = tuple(
        column
        for column in range(matrix.shape[1])
        if column not in pivots
    )
    particular = np.zeros(matrix.shape[1], dtype=np.uint8)
    for equation, pivot in enumerate(pivots):
        particular[pivot] = work[equation, -1]
    basis = np.zeros((len(free), matrix.shape[1]), dtype=np.uint8)
    for basis_index, free_column in enumerate(free):
        basis[basis_index, free_column] = 1
        for equation, pivot in enumerate(pivots):
            basis[basis_index, pivot] = work[equation, free_column]
    if not np.array_equal(matrix @ particular & 1, rhs):
        raise AssertionError("binary particular point failed replay")
    if np.any(matrix @ basis.T & 1):
        raise AssertionError("binary null basis failed replay")
    return tuple(pivots), free, particular, basis


def solve_unique_affine(
    matrix: np.ndarray, rhs: np.ndarray
) -> np.ndarray | None:
    """Solve an overdetermined full-column-rank binary system."""

    try:
        _, free, particular, _ = affine_parameterization(matrix, rhs)
    except ValueError:
        return None
    if free:
        raise AssertionError("projected quotient constraint is not unique")
    return particular


def pair_coefficient(
    quadratic: np.ndarray,
    pair_left: Sequence[int],
    pair_right: Sequence[int],
    parity_left: int,
    parity_right: int,
) -> np.ndarray:
    a, b = pair_left
    c, d = pair_right
    sign_left = 1 if parity_left == 0 else -1
    sign_right = 1 if parity_right == 0 else -1
    return (
        sign_left * sign_right * quadratic[:, a, c]
        + sign_left * quadratic[:, a, d]
        + sign_right * quadratic[:, b, c]
        + quadratic[:, b, d]
    )


def known_case26_parities(
    keys: Sequence[tuple[str, int]],
    pairs: Sequence[Sequence[int]],
) -> np.ndarray:
    selected = {
        (str(block), int(cell))
        for block, cell in json.loads(
            (AUDIT / "CASE26_MOD2_BEST_DEFECT2.json").read_text()
        )["selected"]
    }
    support = np.array(
        [int(key in selected) for key in keys], dtype=np.uint8
    )
    return np.array(
        [int(support[list(pair)].sum() & 1) for pair in pairs],
        dtype=np.uint8,
    )


def derive_case(case_number: int) -> dict[str, object]:
    if case_number not in CASES:
        raise ValueError(f"case must be one of {CASES}")
    case, keys, _, constant, linear, quadratic = local.arrays(case_number)
    expected_index = EXPECTED_Q_INDICES[case_number - CASES[0]]
    if (case.block, case.index) != ("S", expected_index):
        raise AssertionError("canonical short-block case ordering changed")
    if (
        len(keys) != 78
        or constant.shape != (20,)
        or linear.shape != (20, 78)
        or quadratic.shape != (20, 78, 78)
    ):
        raise AssertionError("short-block integer model dimensions changed")
    if np.any(quadratic & 1):
        raise AssertionError("the characteristic-two layer is not affine")

    affine = np.remainder(linear, 2).astype(np.uint8)
    groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for variable in range(len(keys)):
        groups[tuple(map(int, affine[:, variable]))].append(variable)
    if len(groups) != 39 or any(len(group) != 2 for group in groups.values()):
        raise AssertionError("the 39 equal-syndrome reflected pairs changed")
    pairs = tuple(tuple(group) for group in groups.values())
    quotient_matrix = np.array(list(groups), dtype=np.uint8).T
    quotient_with_weight = np.vstack(
        (quotient_matrix, np.ones((1, 39), dtype=np.uint8))
    )
    quotient_rhs = np.append(
        np.remainder(-constant, 2), 1
    ).astype(np.uint8)
    pivots, free, particular, basis = affine_parameterization(
        quotient_with_weight, quotient_rhs
    )
    if len(free) != 18 or len(pivots) != 21:
        raise AssertionError("the quotient rank/dimension changed")

    central_candidates = [
        pair_index
        for pair_index, pair in enumerate(pairs)
        if {keys[index] for index in pair}
        == {("L", 20), ("S", 20)}
    ]
    if len(central_candidates) != 1:
        raise AssertionError("the central reflected pair is not unique")
    central = central_candidates[0]
    left_pairs = tuple(
        pair_index
        for pair_index, pair in enumerate(pairs)
        if pair_index != central and keys[pair[0]][0] == "L"
    )
    right_pairs = tuple(
        pair_index
        for pair_index, pair in enumerate(pairs)
        if pair_index != central and keys[pair[0]][0] == "S"
    )
    if (len(left_pairs), len(right_pairs)) != (20, 18):
        raise AssertionError("the noncentral L/S pair counts changed")
    projection_ranks = {
        "L": rank_mod2(basis[:, left_pairs]),
        "S": rank_mod2(basis[:, right_pairs]),
        "L_plus_central": rank_mod2(
            basis[:, left_pairs + (central,)]
        ),
        "S_plus_central": rank_mod2(
            basis[:, right_pairs + (central,)]
        ),
    }
    if projection_ranks != {
        "L": 18,
        "S": 18,
        "L_plus_central": 18,
        "S_plus_central": 18,
    }:
        raise AssertionError("an L/S quotient projection lost rank")

    pair_phases = np.zeros(39, dtype=np.uint8)
    for block_pairs in (left_pairs, right_pairs):
        reference = block_pairs[0]
        for pair_index in block_pairs[1:]:
            pattern = tuple(
                int(
                    np.any(
                        np.remainder(
                            pair_coefficient(
                                quadratic,
                                pairs[reference],
                                pairs[pair_index],
                                reference_parity,
                                pair_parity,
                            ),
                            3,
                        )
                    )
                )
                for reference_parity in (0, 1)
                for pair_parity in (0, 1)
            )
            if pattern == (1, 0, 0, 1):
                pair_phases[pair_index] = 0
            elif pattern == (0, 1, 1, 0):
                pair_phases[pair_index] = 1
            else:
                raise AssertionError("the four-clique phase law failed")

    zero_checks = 0
    nonzero_checks = 0
    for left in range(39):
        if left == central:
            continue
        block_left = keys[pairs[left][0]][0]
        for right in range(left + 1, 39):
            if right == central:
                continue
            block_right = keys[pairs[right][0]][0]
            for parity_left in (0, 1):
                for parity_right in (0, 1):
                    coefficient = pair_coefficient(
                        quadratic,
                        pairs[left],
                        pairs[right],
                        parity_left,
                        parity_right,
                    )
                    separated = block_left != block_right or (
                        parity_left ^ int(pair_phases[left])
                    ) != (
                        parity_right ^ int(pair_phases[right])
                    )
                    nonzero = bool(np.any(np.remainder(coefficient, 3)))
                    if separated:
                        zero_checks += 1
                        if nonzero:
                            raise AssertionError(
                                "a forced-zero clique coupling survived"
                            )
                    else:
                        nonzero_checks += 1
                        if not nonzero:
                            raise AssertionError(
                                "a within-clique coupling vanished"
                            )
    if (zero_checks, nonzero_checks) != (2126, 686):
        raise AssertionError("the complete coupling-check census changed")

    # The quotient coordinate is the 18-vector multiplying the rows of
    # ``basis``.  Since both block projections have full rank, an all-zero
    # L projection can occur at most once and is found by one exact solve.
    no_left_coefficients = solve_unique_affine(
        basis[:, left_pairs].T, particular[list(left_pairs)]
    )
    no_left_indices: list[int] = []
    if no_left_coefficients is not None:
        point = (
            particular
            ^ ((no_left_coefficients @ basis) & 1).astype(np.uint8)
        )
        if np.any(point[list(left_pairs)]):
            raise AssertionError("the all-even-L solve failed replay")
        if not np.any(point[list(right_pairs)]):
            raise AssertionError("the fallback S gauge is absent")
        no_left_indices.append(
            sum(
                int(value) << bit
                for bit, value in enumerate(no_left_coefficients)
            )
        )

    noncentral = left_pairs + right_pairs
    no_noncentral = solve_unique_affine(
        basis[:, noncentral].T, particular[list(noncentral)]
    )
    if no_noncentral is not None:
        raise AssertionError(
            "a quotient has no odd noncentral reflection pair"
        )
    expected_exception_count = 1 if case.index in (8, 14) else 0
    if len(no_left_indices) != expected_exception_count:
        raise AssertionError("the dynamic-gauge exception count changed")

    l_gauge_states = QUOTIENT_STATES - len(no_left_indices)
    s_gauge_states = len(no_left_indices)
    l_gauge_rows = 2 * ((1 << 19) + (1 << 18))
    s_gauge_rows = 2 * ((1 << 20) + (1 << 17))
    join_rows = (
        l_gauge_states * l_gauge_rows
        + s_gauge_states * s_gauge_rows
    )
    expected_join_rows = (
        NORMAL_ROWS_PER_CASE
        + expected_exception_count * EXCEPTIONAL_SURCHARGE
    )
    if join_rows != expected_join_rows:
        raise AssertionError("the dynamic-gauge work count changed")

    physical_rows = np.asarray(anti.direct_rows(case, set()), dtype=np.int8)
    if physical_rows.shape != (4, 42):
        raise AssertionError("the physical anti-fold row shape changed")
    variable_blocks = np.array(
        [0 if block == "L" else 1 for block, _ in keys],
        dtype=np.uint8,
    )
    variable_cells = np.array(
        [cell for _, cell in keys], dtype=np.uint8
    )
    pinned = (
        known_case26_parities(keys, pairs)
        if case_number == 26
        else particular.copy()
    )
    if case_number == 26:
        delta = pinned ^ particular
        coefficients = solve_unique_affine(basis.T, delta)
        if coefficients is None:
            raise AssertionError("known case-26 parity left the quotient")

    model = {
        "constant": constant.astype("<i2"),
        "linear": linear.astype("<i2"),
        "quadratic": quadratic.astype("<i2"),
        "pairs": np.asarray(pairs, dtype=np.uint8),
        "pair_blocks": np.array(
            [
                2
                if pair_index == central
                else (0 if keys[pair[0]][0] == "L" else 1)
                for pair_index, pair in enumerate(pairs)
            ],
            dtype=np.uint8,
        ),
        "pair_phases": pair_phases,
        "particular": particular,
        "basis": basis,
        "pinned": pinned,
        "physical_rows": physical_rows,
        "variable_blocks": variable_blocks,
        "variable_cells": variable_cells,
    }
    result: dict[str, object] = {
        "case": case_number,
        "block": case.block,
        "q_index": case.index,
        "normalized_equations": 20,
        "support_variables": 78,
        "reflected_pairs": 39,
        "quotient_rank": len(pivots),
        "quotient_dimension": len(free),
        "quotient_states": QUOTIENT_STATES,
        "central_pair_index": central,
        "central_pair": [
            list(keys[index]) for index in pairs[central]
        ],
        "noncentral_pairs": {"L": len(left_pairs), "S": len(right_pairs)},
        "projection_ranks": projection_ranks,
        "four_clique_zero_checks": zero_checks,
        "four_clique_nonzero_checks": nonzero_checks,
        "pair_phases_sha256": compact_hash(pair_phases.tolist()),
        "particular_sha256": compact_hash(particular.tolist()),
        "basis_sha256": compact_hash(basis.tolist()),
        "every_quotient_has_odd_noncentral_pair": True,
        "gauge_policy": "lowest odd noncentral L pair, else S pair",
        "L_gauge_states": l_gauge_states,
        "S_fallback_gauge_states": s_gauge_states,
        "S_fallback_quotient_indices": no_left_indices,
        "join_rows": join_rows,
        "_model": model,
    }
    encoded = model_bytes(result)
    result["model_sha256"] = hashlib.sha256(encoded).hexdigest()
    result["model_bytes"] = len(encoded)
    return result


def model_bytes(result: dict[str, object]) -> bytes:
    model = result["_model"]
    chunks = [
        struct.pack(
            "<8s5I",
            MAGIC,
            int(result["normalized_equations"]),
            int(result["support_variables"]),
            int(result["reflected_pairs"]),
            int(result["quotient_dimension"]),
            int(result["central_pair_index"]),
        )
    ]
    for name in ("constant", "linear", "quadratic"):
        chunks.append(np.asarray(model[name], dtype="<i2").tobytes())
    for name in (
        "pairs",
        "pair_blocks",
        "pair_phases",
        "particular",
        "basis",
        "pinned",
    ):
        chunks.append(np.asarray(model[name], dtype=np.uint8).tobytes())
    chunks.append(np.asarray(model["physical_rows"], dtype=np.int8).tobytes())
    for name in ("variable_blocks", "variable_cells"):
        chunks.append(np.asarray(model[name], dtype=np.uint8).tobytes())
    return b"".join(chunks)


def public_result(result: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in result.items() if key != "_model"}


def derive_all() -> dict[str, object]:
    records = [public_result(derive_case(case)) for case in CASES]
    total = sum(int(record["join_rows"]) for record in records)
    if total != 3_710_853_316_608:
        raise AssertionError("the nine-case exact work total changed")
    result = {
        "schema": "h668-eliahou-short-block-census-algebra-v1",
        "cases": records,
        "case_count": len(records),
        "normal_rows_per_case": NORMAL_ROWS_PER_CASE,
        "exceptional_surcharge_per_case": EXCEPTIONAL_SURCHARGE,
        "exceptional_cases": [24, 27],
        "total_join_rows": total,
    }
    result["semantic_sha256"] = compact_hash(result)
    return result


def verify_certificate(result: dict[str, object]) -> None:
    if not CERTIFICATE.exists():
        return
    expected = json.loads(CERTIFICATE.read_text())
    if result != expected:
        raise AssertionError("short-block frozen certificate changed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=int, choices=CASES)
    parser.add_argument("--write-model", type=Path)
    parser.add_argument("--no-certificate-check", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = derive_all()
    if not args.no_certificate_check:
        verify_certificate(result)
    if args.case is not None:
        selected = derive_case(args.case)
        if args.write_model is not None:
            args.write_model.write_bytes(model_bytes(selected))
        payload = public_result(selected)
    else:
        if args.write_model is not None:
            raise ValueError("--write-model requires --case")
        payload = result
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("PASS: all nine short-block quotient/gauge models verified")


if __name__ == "__main__":
    main()
