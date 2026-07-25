#!/usr/bin/env python3
"""Independent NumPy cross-checks for three C++ quotient-kernel counts."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
AUDIT = SEARCH / "eliahou_char3_jet_audit"
FIXED = SEARCH / "eliahou_defect2_math"
sys.path[:0] = [str(JET), str(AUDIT), str(FIXED), str(SEARCH)]

import search_char3_local as local  # noqa: E402
import search_char3_cp_sat as cp  # noqa: E402
import verify_fixed_quotient_join as fixed  # noqa: E402
from verify_mod2_affine_code import rref_parameterization  # noqa: E402


EXPECTED = {0: 50, 131_071: 70, 262_143: 56}


def shared_model():
    case, keys, equations, constant, linear, quadratic = local.arrays(26)
    groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for variable in range(len(keys)):
        groups[
            tuple(map(int, np.remainder(linear[:, variable], 2)))
        ].append(variable)
    pairs = tuple(tuple(group) for group in groups.values())
    quotient = np.array(list(groups), dtype=np.uint8).T
    augmented = np.vstack(
        [quotient, np.ones((1, len(pairs)), dtype=np.uint8)]
    )
    rhs = np.append(
        np.remainder(-constant, 2), 1
    ).astype(np.uint8)
    _, free, particular, basis = rref_parameterization(augmented, rhs)
    if len(free) != 18:
        raise AssertionError("the quotient dimension changed")
    central = next(
        pair_index
        for pair_index, pair in enumerate(pairs)
        if {keys[index] for index in pair}
        == {("L", 20), ("S", 20)}
    )
    return (
        case,
        keys,
        equations,
        constant,
        linear,
        quadratic,
        pairs,
        particular,
        basis,
        central,
    )


def reference_count(
    index: int, enumerate_records: bool = False
) -> dict[str, object]:
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
    ) = shared_model()
    parities = particular.copy()
    for bit in range(18):
        if (index >> bit) & 1:
            parities ^= basis[bit]

    base = np.zeros(len(keys), dtype=np.int64)
    substitution = np.zeros(
        (len(keys), len(pairs)), dtype=np.int64
    )
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
            linear[equation, variable] += (
                int(
                    column
                    @ raw_quadratic[equation]
                    @ column
                )
                // 2
            )
        for left in range(39):
            for right in range(left + 1, 39):
                quadratic[equation, left, right] = int(
                    substitution[:, left]
                    @ raw_quadratic[equation]
                    @ substitution[:, right]
                )

    components = fixed.interaction_components(quadratic, central)
    left_components = sorted(
        (
            component
            for component in components
            if keys[pairs[component[0]][0]][0] == "L"
        )
    )
    right_components = sorted(
        (
            component
            for component in components
            if keys[pairs[component[0]][0]][0] == "S"
        )
    )
    if (
        len(left_components) != 2
        or len(right_components) != 2
        or sum(map(len, left_components)) != 20
        or sum(map(len, right_components)) != 18
    ):
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
    matches = 0
    records: list[dict[str, object]] = []
    for central_value in (0, 1):
        tables = [
            fixed.component_table(
                reduction, component, central_value
            )
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
            - central_value
            * reduction.linear[:, reduction.central],
            3,
        )
        required = required_full_even - (
            central_value if parities[central] == 0 else 0
        )
        for left_weight in range(21):
            right_weight = required - left_weight
            left_indices = np.flatnonzero(
                left_weights == left_weight
            )
            right_indices = np.flatnonzero(
                right_weights == right_weight
            )
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
            left_unique, left_multiplicity = np.unique(
                left_signatures, return_counts=True
            )
            right_unique, right_multiplicity = np.unique(
                right_signatures, return_counts=True
            )
            common, left_places, right_places = np.intersect1d(
                left_unique,
                right_unique,
                assume_unique=True,
                return_indices=True,
            )
            matches += int(
                np.sum(
                    left_multiplicity[left_places].astype(np.int64)
                    * right_multiplicity[right_places].astype(np.int64)
                )
            )
            if not enumerate_records:
                continue
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
                        support = (
                            reduction.base
                            + reduction.substitution @ state
                        )
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
                        if (
                            direct["normalized_residuals"]
                            != values.tolist()
                        ):
                            raise AssertionError(
                                "reference physical replay disagrees"
                            )
                        pair_state = sum(
                            int(chosen) << pair_index
                            for pair_index, chosen in enumerate(state)
                        )
                        records.append(
                            {
                                "quotient_index": index,
                                "central_value": central_value,
                                "pair_state": pair_state,
                                "normalized_residuals": values.tolist(),
                                "nonzero_lags": int(
                                    np.count_nonzero(values)
                                ),
                                "l1": int(np.abs(values).sum()),
                                "linf": int(np.abs(values).max()),
                            }
                        )
    records.sort(
        key=lambda record: (
            record["central_value"],
            record["pair_state"],
        )
    )
    if enumerate_records and len(records) != matches:
        raise AssertionError("reference reconstruction lost survivors")
    return {
        "quotient_index": index,
        "component_sizes": [
            len(component) for component in reduction.components
        ],
        "joint_mod6_supports": matches,
        **({"records": records} if enumerate_records else {}),
    }


def main() -> None:
    records = []
    for index, expected in EXPECTED.items():
        record = reference_count(index)
        if record["joint_mod6_supports"] != expected:
            raise AssertionError(
                f"quotient {index} changed from {expected}"
            )
        records.append(record)
    print(json.dumps(records, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
