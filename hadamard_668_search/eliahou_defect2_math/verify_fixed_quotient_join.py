#!/usr/bin/env python3
"""Exact fixed-quotient join around the pinned case-26 defect-two point.

The characteristic-two columns occur in 39 equal-syndrome reflected
pairs.  Freeze the 39 pair parities to those of the pinned point.  Each
pair then has one binary state: orientation for an odd pair, or empty/full
for an even pair.  Exact weight 39 says that exactly eight of the sixteen
even pairs are full.

After substitution in the twenty characteristic-three jet equations, the
quadratic interaction graph has a central articulation variable.  For
each value of that variable, the graph splits into components of sizes
10, 10, 10, and 8.  This script enumerates each component and performs an
exact residue-vector meet in the middle.  It therefore certifies the
complete fixed-quotient slice without enumerating its 107,961,384,960
supports individually.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import hashlib
from math import comb
import json
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
AUDIT = SEARCH / "eliahou_char3_jet_audit"
sys.path[:0] = [str(JET), str(SEARCH), str(AUDIT)]

import search_char3_cp_sat as cp  # noqa: E402
import search_char3_local as local  # noqa: E402
from verify_mod2_affine_code import rref_parameterization  # noqa: E402


CENTER_PATH = AUDIT / "CASE26_MOD2_BEST_DEFECT2.json"
CERTIFICATE_PATH = HERE / "CASE26_FIXED_QUOTIENT_MOD6_CENSUS.json"


@dataclass(frozen=True)
class Reduction:
    keys: tuple[tuple[str, int], ...]
    equations: tuple[object, ...]
    constant: np.ndarray
    linear: np.ndarray
    quadratic: np.ndarray
    base: np.ndarray
    substitution: np.ndarray
    pair_parities: tuple[int, ...]
    pairs: tuple[tuple[int, int], ...]
    center: np.ndarray
    central: int
    components: tuple[tuple[int, ...], ...]
    quotient_dimension: int
    whole_char2_weight_39_supports: int


def pack_residues(values: np.ndarray) -> np.ndarray:
    """Injectively pack twenty trits in a uint64 using two bits per trit."""

    residues = np.asarray(values, dtype=np.uint64)
    if residues.ndim != 2 or residues.shape[1] != 20:
        raise AssertionError("expected an n by 20 residue array")
    if np.any(residues > 2):
        raise AssertionError("only residues 0, 1, 2 may be packed")
    packed = np.zeros(len(residues), dtype=np.uint64)
    for coordinate in range(20):
        packed |= residues[:, coordinate] << np.uint64(2 * coordinate)
    return packed


def interaction_components(
    quadratic: np.ndarray, central: int
) -> tuple[tuple[int, ...], ...]:
    vertices = [index for index in range(39) if index != central]
    adjacency = {index: set() for index in vertices}
    for left in vertices:
        for right in vertices:
            if left < right and np.any(quadratic[:, left, right] % 3):
                adjacency[left].add(right)
                adjacency[right].add(left)

    components = []
    while adjacency:
        stack = [next(iter(adjacency))]
        component = set(stack)
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in component:
                    component.add(neighbor)
                    stack.append(neighbor)
        for vertex in component:
            del adjacency[vertex]
        components.append(tuple(sorted(component)))
    return tuple(sorted(components, key=lambda part: (-len(part), part)))


def derive_reduction() -> Reduction:
    center_payload = json.loads(CENTER_PATH.read_text())
    case, keys, equations, raw_constant, raw_linear, raw_quadratic = (
        local.arrays(26)
    )
    if (case.block, case.index) != ("S", 12):
        raise AssertionError("canonical case 26 changed")
    center_selected = {
        (str(block), int(cell))
        for block, cell in center_payload["selected"]
    }
    center = np.array(
        [int(key in center_selected) for key in keys], dtype=np.int64
    )
    if int(center.sum()) != 39:
        raise AssertionError("pinned center no longer has weight 39")

    # Equal characteristic-two columns define the reflected pairs.
    groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    affine = np.remainder(raw_linear, 2)
    for variable in range(len(keys)):
        groups[
            tuple(map(int, affine[:, variable]))
        ].append(variable)
    if len(groups) != 39 or any(len(group) != 2 for group in groups.values()):
        raise AssertionError("the 39 reflected syndrome pairs changed")
    pairs = tuple(tuple(group) for group in groups.values())

    # x = base + substitution*y is an exact integer identity on Boolean y.
    # Odd pairs use (1-y,y); even pairs use (y,y).
    base = np.zeros(len(keys), dtype=np.int64)
    substitution = np.zeros((len(keys), len(pairs)), dtype=np.int64)
    pair_parities = []
    for pair_index, pair in enumerate(pairs):
        parity = int(center[list(pair)].sum() % 2)
        pair_parities.append(parity)
        left, right = pair
        if parity:
            base[left] = 1
            substitution[left, pair_index] = -1
            substitution[right, pair_index] = 1
        else:
            substitution[left, pair_index] = 1
            substitution[right, pair_index] = 1
    if pair_parities.count(1) != 23 or pair_parities.count(0) != 16:
        raise AssertionError("the pinned quotient parity profile changed")

    # This fixed parity vector is one point in the complete 18-dimensional
    # characteristic-two quotient.  Enumerate that small quotient to pin the
    # scope denominator and the size of the full fixed-weight affine slice.
    quotient_matrix = np.array(list(groups), dtype=np.uint8).T
    quotient_with_weight = np.vstack(
        [quotient_matrix, np.ones((1, 39), dtype=np.uint8)]
    )
    quotient_rhs = np.append(
        np.remainder(-raw_constant, 2), 1
    ).astype(np.uint8)
    _, quotient_free, quotient_particular, quotient_basis = (
        rref_parameterization(quotient_with_weight, quotient_rhs)
    )
    quotient_dimension = len(quotient_free)
    if quotient_dimension != 18:
        raise AssertionError("the characteristic-two quotient changed")
    if not np.array_equal(
        np.remainder(
            quotient_with_weight @ np.array(pair_parities), 2
        ),
        quotient_rhs,
    ):
        raise AssertionError("the pinned pair parities left the quotient")
    whole_char2_weight_39_supports = 0
    quotient_point = quotient_particular.copy()
    previous_gray = 0
    for integer in range(1 << quotient_dimension):
        if integer:
            gray = integer ^ (integer >> 1)
            changed = gray ^ previous_gray
            quotient_point ^= quotient_basis[changed.bit_length() - 1]
            previous_gray = gray
        odd_pairs = int(quotient_point.sum())
        if odd_pairs % 2 != 1:
            raise AssertionError("weight parity failed in the quotient")
        even_pairs = 39 - odd_pairs
        whole_char2_weight_39_supports += (
            (1 << odd_pairs) * comb(even_pairs, even_pairs // 2)
        )
    if whole_char2_weight_39_supports != 25_941_166_955_843_488:
        raise AssertionError("the complete characteristic-two count changed")

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
                int(column @ raw_quadratic[equation] @ column) // 2
            )
        for left in range(39):
            for right in range(left + 1, 39):
                quadratic[equation, left, right] = int(
                    substitution[:, left]
                    @ raw_quadratic[equation]
                    @ substitution[:, right]
                )

    # Recover the pinned center in the new coordinates and check the exact,
    # not merely modular, substituted polynomial.
    center_state = np.zeros(39, dtype=np.int64)
    for pair_index, (left, right) in enumerate(pairs):
        if pair_parities[pair_index]:
            center_state[pair_index] = center[right]
        else:
            center_state[pair_index] = center[left]
    if not np.array_equal(base + substitution @ center_state, center):
        raise AssertionError("failed to recover the pinned center")

    def substituted_values(state: np.ndarray) -> np.ndarray:
        values = constant + linear @ state
        for left in range(39):
            for right in range(left + 1, 39):
                if state[left] and state[right]:
                    values += quadratic[:, left, right]
        return values

    if not np.array_equal(
        substituted_values(center_state),
        local.exact_values(
            center, raw_constant, raw_linear, raw_quadratic
        ),
    ):
        raise AssertionError("exact substitution failed at the center")
    rng = np.random.default_rng(668_261_911)
    for _ in range(32):
        state = rng.integers(0, 2, size=39, dtype=np.int64)
        physical_state = base + substitution @ state
        if not np.array_equal(
            substituted_values(state),
            local.exact_values(
                physical_state,
                raw_constant,
                raw_linear,
                raw_quadratic,
            ),
        ):
            raise AssertionError("exact quadratic substitution failed")

    central = next(
        pair_index
        for pair_index, pair in enumerate(pairs)
        if {keys[index] for index in pair}
        == {("L", 20), ("S", 20)}
    )
    components = interaction_components(quadratic, central)
    if tuple(map(len, components)) != (10, 10, 10, 8):
        raise AssertionError("the four-component contraction changed")
    # No quadratic term may cross components after the central variable is
    # removed.  This is the algebraic reason the join is complete.
    component_of = {
        variable: part
        for part, component in enumerate(components)
        for variable in component
    }
    for left in range(39):
        for right in range(left + 1, 39):
            if (
                left != central
                and right != central
                and component_of[left] != component_of[right]
                and np.any(quadratic[:, left, right] % 3)
            ):
                raise AssertionError("an interaction crosses components")

    return Reduction(
        keys=keys,
        equations=equations,
        constant=np.remainder(constant, 3),
        linear=np.remainder(linear, 3),
        quadratic=np.remainder(quadratic, 3),
        base=base,
        substitution=substitution,
        pair_parities=tuple(pair_parities),
        pairs=pairs,
        center=center,
        central=central,
        components=components,
        quotient_dimension=quotient_dimension,
        whole_char2_weight_39_supports=whole_char2_weight_39_supports,
    )


def component_table(
    reduction: Reduction,
    component: tuple[int, ...],
    central_value: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return mod-3 contribution and even-pair weight for all states."""

    width = len(component)
    state_numbers = np.arange(1 << width, dtype=np.uint16)
    states = (
        (
            state_numbers[:, np.newaxis]
            >> np.arange(width, dtype=np.uint16)
        )
        & 1
    ).astype(np.int16)
    effective_linear = reduction.linear[:, component].copy()
    for local_index, variable in enumerate(component):
        left, right = sorted((variable, reduction.central))
        effective_linear[:, local_index] = np.remainder(
            effective_linear[:, local_index]
            + central_value * reduction.quadratic[:, left, right],
            3,
        )
    values = np.remainder(states @ effective_linear.T, 3)
    for local_left in range(width):
        for local_right in range(local_left + 1, width):
            left, right = sorted(
                (component[local_left], component[local_right])
            )
            coefficient = reduction.quadratic[:, left, right]
            if np.any(coefficient):
                values = np.remainder(
                    values
                    + (
                        states[:, local_left] * states[:, local_right]
                    )[:, np.newaxis]
                    * coefficient[np.newaxis, :],
                    3,
                )
    even_positions = [
        local_index
        for local_index, variable in enumerate(component)
        if reduction.pair_parities[variable] == 0
    ]
    weights = states[:, even_positions].sum(axis=1).astype(np.int8)
    return values.astype(np.uint8), weights


def pair_table(
    left: tuple[np.ndarray, np.ndarray],
    right: tuple[np.ndarray, np.ndarray],
) -> tuple[np.ndarray, np.ndarray, int]:
    left_values, left_weights = left
    right_values, right_weights = right
    values = np.remainder(
        left_values[:, np.newaxis, :]
        + right_values[np.newaxis, :, :],
        3,
    ).reshape((-1, 20))
    weights = (
        left_weights[:, np.newaxis] + right_weights[np.newaxis, :]
    ).reshape(-1)
    return values, weights, len(right_values)


def state_from_join(
    reduction: Reduction,
    central_value: int,
    left_index: int,
    right_index: int,
    left_radix: int,
    right_radix: int,
) -> np.ndarray:
    first, second = divmod(left_index, left_radix)
    third, fourth = divmod(right_index, right_radix)
    state = np.zeros(39, dtype=np.int64)
    state[reduction.central] = central_value
    for component, state_number in zip(
        reduction.components, (first, second, third, fourth)
    ):
        state[list(component)] = (
            state_number >> np.arange(len(component))
        ) & 1
    return state


def census() -> dict[str, object]:
    reduction = derive_reduction()
    _, _, _, raw_constant, raw_linear, raw_quadratic = local.arrays(26)
    join_counts = []
    survivors = []

    for central_value in (0, 1):
        tables = [
            component_table(reduction, component, central_value)
            for component in reduction.components
        ]
        left_values, left_weights, left_radix = pair_table(
            tables[0], tables[1]
        )
        right_values, right_weights, right_radix = pair_table(
            tables[2], tables[3]
        )
        target = np.remainder(
            -reduction.constant
            - central_value * reduction.linear[:, reduction.central],
            3,
        )

        for left_weight in range(9):
            right_weight = 8 - left_weight
            left_indices = np.flatnonzero(left_weights == left_weight)
            right_indices = np.flatnonzero(right_weights == right_weight)
            if not len(left_indices) or not len(right_indices):
                continue
            complement = np.remainder(
                target[np.newaxis, :]
                - left_values[left_indices].astype(np.int16),
                3,
            )
            left_signatures = pack_residues(complement)
            right_signatures = pack_residues(right_values[right_indices])
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
            matches = int(
                np.sum(
                    left_multiplicity[left_places].astype(np.int64)
                    * right_multiplicity[right_places].astype(np.int64)
                )
            )
            join_counts.append(
                {
                    "central_value": central_value,
                    "left_even_weight": left_weight,
                    "right_even_weight": right_weight,
                    "left_states": len(left_indices),
                    "right_states": len(right_indices),
                    "common_signatures": len(common),
                    "supports": matches,
                }
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
                        state = state_from_join(
                            reduction,
                            central_value,
                            int(left_index),
                            int(right_index),
                            left_radix,
                            right_radix,
                        )
                        support = (
                            reduction.base + reduction.substitution @ state
                        )
                        if int(support.sum()) != 39:
                            raise AssertionError("join violated exact weight")
                        values = local.exact_values(
                            support,
                            raw_constant,
                            raw_linear,
                            raw_quadratic,
                        ).astype(np.int64)
                        if np.any(np.remainder(values, 6)):
                            raise AssertionError(
                                "join emitted a non-mod-6 support"
                            )
                        selected = tuple(
                            key
                            for key, chosen in zip(reduction.keys, support)
                            if chosen
                        )
                        direct = cp.replay(
                            local.arrays(26)[0],
                            selected,
                            reduction.equations,
                            6,
                        )
                        if direct["normalized_residuals"] != values.tolist():
                            raise AssertionError(
                                "physical replay disagrees with the join"
                            )
                        survivors.append(
                            {
                                "selected": [
                                    [block, cell] for block, cell in selected
                                ],
                                "normalized_residuals": values.tolist(),
                                "nonzero_lags": int(np.count_nonzero(values)),
                                "l1": int(np.abs(values).sum()),
                                "linf": int(np.abs(values).max()),
                                "hamming_distance_from_center": int(
                                    np.count_nonzero(
                                        support != reduction.center
                                    )
                                ),
                            }
                        )

    survivors.sort(
        key=lambda record: (
            record["nonzero_lags"],
            record["l1"],
            record["linf"],
            record["hamming_distance_from_center"],
            record["selected"],
        )
    )
    canonical_survivors = json.dumps(
        survivors, sort_keys=True, separators=(",", ":")
    ).encode()
    quotient_payload = {
        "pair_parities": list(reduction.pair_parities),
        "pairs": [
            [
                [reduction.keys[left][0], reduction.keys[left][1]],
                [reduction.keys[right][0], reduction.keys[right][1]],
            ]
            for left, right in reduction.pairs
        ],
    }
    quotient_sha256 = hashlib.sha256(
        json.dumps(
            quotient_payload, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()
    return {
        "case": 26,
        "block": "S",
        "q_index": 12,
        "syndrome_pairs": 39,
        "affine_quotient_dimension": reduction.quotient_dimension,
        "affine_quotient_states": 1 << reduction.quotient_dimension,
        "quotient_states_covered": 1,
        "quotient_states_remaining": (
            (1 << reduction.quotient_dimension) - 1
        ),
        "odd_pairs": 23,
        "even_pairs": 16,
        "fixed_quotient_weight_39_supports": (
            (1 << 23) * comb(16, 8)
        ),
        "whole_char2_weight_39_supports": (
            reduction.whole_char2_weight_39_supports
        ),
        "central_pair": [["L", 20], ["S", 20]],
        "component_sizes_after_conditioning": [10, 10, 10, 8],
        "join_counts": join_counts,
        "joint_mod6_supports": len(survivors),
        "exact_supports": sum(
            not record["nonzero_lags"] for record in survivors
        ),
        "minimum_nonzero_lags": min(
            record["nonzero_lags"] for record in survivors
        ),
        "minimum_l1": min(record["l1"] for record in survivors),
        "quotient_sha256": quotient_sha256,
        "survivor_census_sha256": hashlib.sha256(
            canonical_survivors
        ).hexdigest(),
        "best_witness": survivors[0],
    }


def main() -> None:
    result = census()
    if CERTIFICATE_PATH.exists():
        pinned = json.loads(CERTIFICATE_PATH.read_text())
        if result != pinned:
            raise AssertionError("recomputed census differs from certificate")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
