#!/usr/bin/env python3
"""Verify and size the complete case-26 quotient-census architecture.

This script does not perform the complete census.  It proves the universal
four-component decomposition used by the proposed C++ kernel, enumerates the
small 18-dimensional characteristic-two quotient, and emits exact work
counts.  With ``--write-model`` it also writes a compact, derived binary model
for the benchmark kernel; that file is disposable build input, not a
mathematical certificate.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import struct
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
AUDIT = SEARCH / "eliahou_char3_jet_audit"
sys.path[:0] = [str(JET), str(AUDIT), str(SEARCH)]

import search_char3_local as local  # noqa: E402
import search_eliahou_antifold_sat as anti  # noqa: E402
from verify_mod2_affine_code import rref_parameterization  # noqa: E402


MAGIC = b"H668GQ2\0"


def rank_mod2(matrix: np.ndarray) -> int:
    """Return the binary rank of a small matrix."""

    work = np.asarray(matrix, dtype=np.uint8).copy() & 1
    row = 0
    for column in range(work.shape[1]):
        candidates = np.flatnonzero(work[row:, column])
        if not len(candidates):
            continue
        pivot = row + int(candidates[0])
        work[[row, pivot]] = work[[pivot, row]]
        for other in np.flatnonzero(work[:, column]):
            if other != row:
                work[other] ^= work[row]
        row += 1
        if row == work.shape[0]:
            break
    return row


def derive() -> dict[str, object]:
    """Derive the quotient, universal split, and exact operation counts."""

    case, keys, _, constant, linear, quadratic = local.arrays(26)
    if (case.block, case.index) != ("S", 12):
        raise AssertionError("canonical case 26 changed")
    if len(keys) != 78 or len(constant) != 20:
        raise AssertionError("case-26 dimensions changed")

    # Equal characteristic-two columns are the 39 reflected syndrome pairs.
    groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    affine = np.remainder(linear, 2).astype(np.uint8)
    for variable in range(len(keys)):
        groups[tuple(map(int, affine[:, variable]))].append(variable)
    if len(groups) != 39 or any(len(group) != 2 for group in groups.values()):
        raise AssertionError("the reflected-pair partition changed")
    pairs = tuple(tuple(group) for group in groups.values())

    quotient_matrix = np.array(list(groups), dtype=np.uint8).T
    quotient_with_weight = np.vstack(
        [quotient_matrix, np.ones((1, 39), dtype=np.uint8)]
    )
    quotient_rhs = np.append(
        np.remainder(-constant, 2), 1
    ).astype(np.uint8)
    _, free, particular, basis = rref_parameterization(
        quotient_with_weight, quotient_rhs
    )
    if len(free) != 18:
        raise AssertionError("the quotient dimension changed")

    central = next(
        pair_index
        for pair_index, pair in enumerate(pairs)
        if {keys[index] for index in pair}
        == {("L", 20), ("S", 20)}
    )
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
    if len(left_pairs) != 20 or len(right_pairs) != 18:
        raise AssertionError("the blockwise reflected-pair counts changed")

    # The S projection is a bijection from the 18-dimensional quotient onto
    # all 18-bit S parity patterns.  The L projection is injective too, but
    # lands in an affine codimension-two code in F_2^20.  Thus identical
    # component masks cannot be cached across distinct quotient states.
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
        raise AssertionError("the quotient projection ranks changed")

    # In pair coordinates, parity 0 uses the column (+1,+1), while parity 1
    # uses (-1,+1).  There is a fixed binary "phase" on the reflected pairs:
    # within each block, a coupling is nonzero exactly when
    #
    #   parity_i xor phase_i == parity_j xor phase_j.
    #
    # Thus the four components are block x phase-adjusted parity, not raw
    # even/odd parity.  Derive the phases from one reference vertex in each
    # block and then check every pair and all four parity choices.
    pair_phases = np.zeros(39, dtype=np.uint8)
    for block_pairs in (left_pairs, right_pairs):
        reference = block_pairs[0]
        a_reference, b_reference = pairs[reference]
        for pair_index in block_pairs[1:]:
            a_pair, b_pair = pairs[pair_index]
            patterns = []
            for reference_parity in (0, 1):
                reference_sign = 1 if reference_parity == 0 else -1
                for pair_parity in (0, 1):
                    pair_sign = 1 if pair_parity == 0 else -1
                    coefficient = (
                        reference_sign
                        * pair_sign
                        * quadratic[:, a_reference, a_pair]
                        + reference_sign
                        * quadratic[:, a_reference, b_pair]
                        + pair_sign
                        * quadratic[:, b_reference, a_pair]
                        + quadratic[:, b_reference, b_pair]
                    )
                    patterns.append(
                        int(np.any(np.remainder(coefficient, 3)))
                    )
            if tuple(patterns) == (1, 0, 0, 1):
                pair_phases[pair_index] = 0
            elif tuple(patterns) == (0, 1, 1, 0):
                pair_phases[pair_index] = 1
            else:
                raise AssertionError(
                    "a reference coupling has no signed-complete pattern"
                )

    universal_zero_checks = 0
    same_class_nonzero_checks = 0
    for left in range(len(pairs)):
        if left == central:
            continue
        a_left, b_left = pairs[left]
        left_block = keys[a_left][0]
        for right in range(left + 1, len(pairs)):
            if right == central:
                continue
            a_right, b_right = pairs[right]
            right_block = keys[a_right][0]
            for left_parity in (0, 1):
                left_sign = 1 if left_parity == 0 else -1
                for right_parity in (0, 1):
                    right_sign = 1 if right_parity == 0 else -1
                    coefficient = (
                        left_sign
                        * right_sign
                        * quadratic[:, a_left, a_right]
                        + left_sign * quadratic[:, a_left, b_right]
                        + right_sign * quadratic[:, b_left, a_right]
                        + quadratic[:, b_left, b_right]
                    )
                    separated = left_block != right_block or (
                        (left_parity ^ int(pair_phases[left]))
                        != (right_parity ^ int(pair_phases[right]))
                    )
                    if separated:
                        universal_zero_checks += 1
                        if np.any(np.remainder(coefficient, 3)):
                            raise AssertionError(
                                "the universal four-way split failed"
                            )
                    elif np.any(np.remainder(coefficient, 3)):
                        same_class_nonzero_checks += 1
                    else:
                        raise AssertionError(
                            "a same-color coupling unexpectedly vanished"
                        )
    if same_class_nonzero_checks == 0:
        raise AssertionError("the retained components lost all interactions")

    pinned_selected = {
        (str(block), int(cell))
        for block, cell in json.loads(
            (
                AUDIT / "CASE26_MOD2_BEST_DEFECT2.json"
            ).read_text()
        )["selected"]
    }
    pinned_support = np.array(
        [int(key in pinned_selected) for key in keys], dtype=np.uint8
    )
    pinned_parities = np.array(
        [
            int(pinned_support[list(pair)].sum() & 1)
            for pair in pairs
        ],
        dtype=np.uint8,
    )
    physical_rows = np.asarray(
        anti.direct_rows(case, set()), dtype=np.int8
    )
    if physical_rows.shape != (4, 42):
        raise AssertionError("the physical anti-fold rows changed")
    variable_blocks = np.array(
        [0 if block == "L" else 1 for block, _ in keys],
        dtype=np.uint8,
    )
    variable_cells = np.array(
        [cell for _, cell in keys], dtype=np.uint8
    )

    seen_s = np.zeros(1 << 18, dtype=np.uint8)
    seen_l: set[int] = set()
    component_rows = {
        "L_color_0": 0,
        "L_color_1": 0,
        "S_color_0": 0,
        "S_color_1": 0,
    }
    whole_weight_39_supports = 0
    quotient_weight_histogram: dict[int, int] = defaultdict(int)
    component_size_histogram: dict[tuple[int, int, int, int], int] = (
        defaultdict(int)
    )
    maximum_component_rows_one_quotient = 0
    pinned_quotient_index = None
    point = particular.copy()
    previous_gray = 0
    for integer in range(1 << 18):
        if integer:
            gray = integer ^ (integer >> 1)
            changed = gray ^ previous_gray
            point ^= basis[changed.bit_length() - 1]
            previous_gray = gray

        if np.array_equal(point, pinned_parities):
            pinned_quotient_index = integer
        left_mask = sum(
            int(point[pair_index]) << bit
            for bit, pair_index in enumerate(left_pairs)
        )
        right_mask = sum(
            int(point[pair_index]) << bit
            for bit, pair_index in enumerate(right_pairs)
        )
        if right_mask >= len(seen_s) or seen_s[right_mask]:
            raise AssertionError("the S projection is not bijective")
        seen_s[right_mask] = 1
        seen_l.add(left_mask)

        left_color_1 = int(
            np.count_nonzero(
                point[list(left_pairs)]
                ^ pair_phases[list(left_pairs)]
            )
        )
        right_color_1 = int(
            np.count_nonzero(
                point[list(right_pairs)]
                ^ pair_phases[list(right_pairs)]
            )
        )
        odd_pairs = int(point.sum())
        if odd_pairs % 2 != 1:
            raise AssertionError("quotient weight parity changed")
        even_pairs = 39 - odd_pairs
        whole_weight_39_supports += (
            (1 << odd_pairs) * comb(even_pairs, even_pairs // 2)
        )
        quotient_weight_histogram[odd_pairs] += 1
        component_size_histogram[
            (
                20 - left_color_1,
                left_color_1,
                18 - right_color_1,
                right_color_1,
            )
        ] += 1
        component_rows["L_color_0"] += 1 << (20 - left_color_1)
        component_rows["L_color_1"] += 1 << left_color_1
        component_rows["S_color_0"] += 1 << (18 - right_color_1)
        component_rows["S_color_1"] += 1 << right_color_1
        maximum_component_rows_one_quotient = max(
            maximum_component_rows_one_quotient,
            (1 << (20 - left_color_1))
            + (1 << left_color_1)
            + (1 << (18 - right_color_1))
            + (1 << right_color_1),
        )

    if not np.all(seen_s) or len(seen_l) != 1 << 18:
        raise AssertionError("a quotient projection lost injectivity")
    if pinned_quotient_index is None:
        raise AssertionError("the pinned quotient was not found")
    pinned_quotient_binary_index = (
        pinned_quotient_index ^ (pinned_quotient_index >> 1)
    )
    if whole_weight_39_supports != 25_941_166_955_843_488:
        raise AssertionError("the whole fixed-weight slice count changed")
    expected_component_rows = {
        "L_color_0": 871_563_240,
        "L_color_1": 871_563_240,
        "S_color_0": 387_420_489,
        "S_color_1": 387_420_489,
    }
    if component_rows != expected_component_rows:
        raise AssertionError("the aggregate component-row counts changed")

    quotient_states = 1 << 18
    right_hash_entries = quotient_states * (1 << 18)
    left_hash_probes = quotient_states * (1 << 20)
    fixed_join_rows = right_hash_entries + left_hash_probes
    return {
        "case": 26,
        "block": case.block,
        "q_index": case.index,
        "normalized_equations": 20,
        "support_variables": 78,
        "reflected_pairs": 39,
        "quotient_dimension": 18,
        "quotient_states": quotient_states,
        "left_pairs_excluding_central": 20,
        "right_pairs_excluding_central": 18,
        "central_pair_index": central,
        "central_pair": [
            list(keys[pairs[central][0]]),
            list(keys[pairs[central][1]]),
        ],
        "projection_ranks": projection_ranks,
        "distinct_left_parity_patterns": len(seen_l),
        "distinct_right_parity_patterns": int(seen_s.sum()),
        "universal_zero_coupling_checks": universal_zero_checks,
        "same_class_nonzero_coupling_checks": same_class_nonzero_checks,
        "universal_components": [
            "L_color_0",
            "L_color_1",
            "S_color_0",
            "S_color_1",
        ],
        "pair_phases": pair_phases.tolist(),
        "component_rows": component_rows,
        "aggregate_component_rows": sum(component_rows.values()),
        "right_hash_entries_per_central_value": right_hash_entries,
        "left_hash_probes_per_central_value": left_hash_probes,
        "join_rows_per_central_value": fixed_join_rows,
        "central_values_per_quotient": 2,
        "right_hash_entries_total": 2 * right_hash_entries,
        "left_hash_probes_total": 2 * left_hash_probes,
        "join_rows_total": 2 * fixed_join_rows,
        "whole_weight_39_supports": whole_weight_39_supports,
        "quotient_weight_histogram": {
            str(weight): count
            for weight, count in sorted(quotient_weight_histogram.items())
        },
        "component_size_profiles": len(component_size_histogram),
        "maximum_component_size": max(
            max(profile) for profile in component_size_histogram
        ),
        "maximum_component_rows_one_quotient": (
            maximum_component_rows_one_quotient
        ),
        "pinned_quotient_gray_index": pinned_quotient_index,
        "pinned_quotient_binary_index": (
            pinned_quotient_binary_index
        ),
        "pinned_pair_parities": pinned_parities.tolist(),
        "_model": {
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
            "particular": particular.astype(np.uint8),
            "basis": basis.astype(np.uint8),
            "pinned_parities": pinned_parities,
            "physical_rows": physical_rows,
            "variable_blocks": variable_blocks,
            "variable_cells": variable_cells,
        },
    }


def model_bytes(result: dict[str, object]) -> bytes:
    """Encode the derived arrays for the single-core C++ benchmark."""

    model = result["_model"]
    header = struct.pack(
        "<8s5I",
        MAGIC,
        result["normalized_equations"],
        result["support_variables"],
        result["reflected_pairs"],
        result["quotient_dimension"],
        result["central_pair_index"],
    )
    chunks = [header]
    for name in ("constant", "linear", "quadratic"):
        chunks.append(np.asarray(model[name], dtype="<i2").tobytes())
    for name in (
        "pairs",
        "pair_blocks",
        "pair_phases",
        "particular",
        "basis",
        "pinned_parities",
    ):
        chunks.append(np.asarray(model[name], dtype=np.uint8).tobytes())
    chunks.append(
        np.asarray(model["physical_rows"], dtype=np.int8).tobytes()
    )
    for name in ("variable_blocks", "variable_cells"):
        chunks.append(np.asarray(model[name], dtype=np.uint8).tobytes())
    return b"".join(chunks)


def public_result(result: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in result.items() if key != "_model"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-model",
        type=Path,
        help="write disposable binary input for benchmark_global_quotient.cpp",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = derive()
    payload = public_result(result)
    encoded = model_bytes(result)
    payload["benchmark_model_sha256"] = sha256(encoded).hexdigest()
    payload["benchmark_model_bytes"] = len(encoded)
    if args.write_model is not None:
        args.write_model.write_bytes(encoded)
        payload["benchmark_model_path"] = str(args.write_model)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
