#!/usr/bin/env python3
"""Independently replay a small short-block range with the NumPy join."""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import struct
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
FIXED = SEARCH / "eliahou_defect2_math"
sys.path[:0] = [str(JET), str(FIXED), str(SEARCH), str(HERE)]

import search_char3_cp_sat as cp  # noqa: E402
import search_char3_local as local  # noqa: E402
import verify_fixed_quotient_join as fixed  # noqa: E402
import verify_short_block_census as plan  # noqa: E402


def shared_model(case_number: int):
    case, keys, equations, constant, linear, quadratic = local.arrays(
        case_number
    )
    derived = plan.derive_case(case_number)
    model = derived["_model"]
    pairs = tuple(
        tuple(map(int, pair)) for pair in np.asarray(model["pairs"])
    )
    return (
        case,
        keys,
        equations,
        constant,
        linear,
        quadratic,
        pairs,
        np.asarray(model["particular"], dtype=np.uint8),
        np.asarray(model["basis"], dtype=np.uint8),
        int(derived["central_pair_index"]),
    )


def score(record: dict[str, object]) -> tuple[int, ...]:
    return (
        int(record["nonzero_lags"]),
        int(record["l1"]),
        int(record["linf"]),
        int(record["quotient_index"]),
        int(record["central_value"]),
        int(record["pair_state"]),
    )


def reference_records(
    case_number: int, quotient_index: int
) -> list[dict[str, object]]:
    (
        case,
        keys,
        equations,
        raw_constant,
        raw_linear,
        raw_quadratic,
        pairs,
        particular,
        basis,
        central,
    ) = shared_model(case_number)
    parities = particular.copy()
    for bit in range(18):
        if (quotient_index >> bit) & 1:
            parities ^= basis[bit]

    base = np.zeros(len(keys), dtype=np.int64)
    substitution = np.zeros((len(keys), 39), dtype=np.int64)
    for pair_index, (left, right) in enumerate(pairs):
        base[left] = int(parities[pair_index])
        substitution[left, pair_index] = (
            -1 if parities[pair_index] else 1
        )
        substitution[right, pair_index] = 1

    constant = local.exact_values(
        base, raw_constant, raw_linear, raw_quadratic
    ).astype(np.int64)
    gradient = raw_linear.astype(np.int64) + np.einsum(
        "eij,j->ei", raw_quadratic.astype(np.int64), base
    )
    linear = gradient @ substitution
    quadratic = np.zeros((20, 39, 39), dtype=np.int64)
    for equation in range(20):
        for variable in range(39):
            column = substitution[:, variable]
            linear[equation, variable] += int(
                column @ raw_quadratic[equation] @ column
            ) // 2
        for left in range(39):
            for right in range(left + 1, 39):
                quadratic[equation, left, right] = int(
                    substitution[:, left]
                    @ raw_quadratic[equation]
                    @ substitution[:, right]
                )

    components = fixed.interaction_components(quadratic, central)
    left_components = sorted(
        component
        for component in components
        if keys[pairs[component[0]][0]][0] == "L"
    )
    right_components = sorted(
        component
        for component in components
        if keys[pairs[component[0]][0]][0] == "S"
    )
    if (
        len(left_components),
        len(right_components),
        sum(map(len, left_components)),
        sum(map(len, right_components)),
    ) != (2, 2, 20, 18):
        raise AssertionError("the four-component split changed")
    reduction = fixed.Reduction(
        keys=keys,
        equations=equations,
        constant=np.remainder(constant, 3),
        linear=np.remainder(linear, 3),
        quadratic=np.remainder(quadratic, 3),
        base=base,
        substitution=substitution,
        pair_parities=tuple(map(int, parities)),
        pairs=pairs,
        center=np.zeros(len(keys), dtype=np.int64),
        central=central,
        components=tuple(left_components + right_components),
        quotient_dimension=18,
        whole_char2_weight_39_supports=0,
    )

    odd_pairs = int(parities.sum())
    required_full_even = (39 - odd_pairs) // 2
    records: list[dict[str, object]] = []
    for central_value in (0, 1):
        tables = [
            fixed.component_table(reduction, component, central_value)
            for component in reduction.components
        ]
        left_values, left_weights, left_radix = fixed.pair_table(
            tables[0], tables[1]
        )
        right_values, right_weights, right_radix = fixed.pair_table(
            tables[2], tables[3]
        )
        target = np.remainder(
            -reduction.constant
            - central_value * reduction.linear[:, reduction.central],
            3,
        )
        required = required_full_even - (
            central_value if parities[central] == 0 else 0
        )
        for left_weight in range(21):
            right_weight = required - left_weight
            left_indices = np.flatnonzero(left_weights == left_weight)
            right_indices = np.flatnonzero(right_weights == right_weight)
            if not len(left_indices) or not len(right_indices):
                continue
            left_signatures = fixed.pack_residues(
                np.remainder(
                    target[np.newaxis, :]
                    - left_values[left_indices].astype(np.int16),
                    3,
                )
            )
            right_signatures = fixed.pack_residues(
                right_values[right_indices]
            )
            common = np.intersect1d(
                np.unique(left_signatures),
                np.unique(right_signatures),
                assume_unique=True,
            )
            for signature in common:
                matching_left = left_indices[
                    np.flatnonzero(left_signatures == signature)
                ]
                matching_right = right_indices[
                    np.flatnonzero(right_signatures == signature)
                ]
                for left_index in matching_left:
                    for right_index in matching_right:
                        state = fixed.state_from_join(
                            reduction,
                            central_value,
                            int(left_index),
                            int(right_index),
                            left_radix,
                            right_radix,
                        )
                        support = reduction.base + reduction.substitution @ state
                        if int(support.sum()) != 39:
                            raise AssertionError(
                                "reference join violated weight 39"
                            )
                        values = local.exact_values(
                            support,
                            raw_constant,
                            raw_linear,
                            raw_quadratic,
                        ).astype(np.int64)
                        if np.any(np.remainder(values, 6)):
                            raise AssertionError(
                                "reference join lost mod-6 divisibility"
                            )
                        selected = tuple(
                            key
                            for key, chosen in zip(keys, support)
                            if chosen
                        )
                        direct = cp.replay(
                            case, selected, equations, 6
                        )
                        if direct["normalized_residuals"] != values.tolist():
                            raise AssertionError(
                                "physical replay disagrees with polynomial"
                            )
                        pair_state = sum(
                            int(chosen) << pair_index
                            for pair_index, chosen in enumerate(state)
                        )
                        records.append(
                            {
                                "quotient_index": quotient_index,
                                "central_value": central_value,
                                "pair_state": pair_state,
                                "normalized_residuals": values.tolist(),
                                "nonzero_lags":
                                    int(np.count_nonzero(values)),
                                "l1": int(np.abs(values).sum()),
                                "linf": int(np.abs(values).max()),
                            }
                        )
    records.sort(
        key=lambda record: (
            record["central_value"], record["pair_state"]
        )
    )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--allow-large", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    if (
        manifest.get("schema")
        != "h668-eliahou-short-block-range-v1"
        or manifest.get("status") != "complete"
    ):
        raise RuntimeError("input is not a complete short-block range")
    case_number = int(manifest["case"])
    start = int(manifest["start"])
    states = int(manifest["states"])
    if states > 2 and not args.allow_large:
        raise RuntimeError(
            "independent NumPy replay is capped at two quotients"
        )

    digest = hashlib.sha256()
    records: list[dict[str, object]] = []
    for quotient_index in range(start, start + states):
        records.extend(reference_records(case_number, quotient_index))
    for record in records:
        digest.update(
            struct.pack(
                "<IBQ20h",
                int(record["quotient_index"]),
                int(record["central_value"]),
                int(record["pair_state"]),
                *map(int, record["normalized_residuals"]),
            )
        )
    exact = [
        record for record in records if int(record["nonzero_lags"]) == 0
    ]
    best = min(records, key=score) if records else None
    expected = {
        "joint_mod6_supports": len(records),
        "integer_polynomial_checks": len(records),
        "bitpacked_physical_replays": len(records),
        "exact_integer_supports": len(exact),
        "survivor_stream_sha256": digest.hexdigest(),
        "best_witness": best,
        "exact_candidates": exact,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise AssertionError(
                f"independent replay mismatch at {key}"
            )
    print(
        json.dumps(
            {
                "status": "PASS",
                "case": case_number,
                "start": start,
                "states": states,
                **expected,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
