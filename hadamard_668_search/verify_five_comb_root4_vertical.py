#!/usr/bin/env python3
"""Verify the exact Phi_4 extension of the vertical-pair root sieve.

The scope is the same explicitly delimited vertical placement as the second
stage in ``verify_five_comb_root12_sieve.py``: the two polarizations of one
directed pair occupy slots ``(g,g+4)``.  The even and odd halves are still
independent projections of the physical high-lag table, so infeasibility is
sound for this slice while feasibility remains a relaxation.

For a directed pair with word sums ``p,q``, a carrier of polarization
``epsilon`` has amplitudes

    p + epsilon*q  at root 1,
    p - epsilon*q  at root i.

Thus the two polarizations swap amplitudes at root i.  The verifier retains
this coupling exactly.  Groups 0 and 2 contribute the real root-i vector
with opposite phases, while groups 1 and 3 do the same for the imaginary
vector.  The existing midpoint join enforces roots +/-1 first; an exact
Gaussian norm then enforces Phi_4.

This checker does not cover arbitrary placement and does not yet impose the
Phi_8 or Phi_16 stages.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
from typing import Iterable, Sequence

from verify_five_comb_high_lag_boundary import (
    decode_e2_boundary_row,
    e2_boundary_rows,
    normalized_projective_labels,
)
from verify_five_comb_paired_lobes import VECTORS
from verify_five_comb_root12_sieve import (
    FEATURE_COUNT,
    EXPECTED_VERTICAL_SURVIVORS,
    ROOT_PROFILES,
    ROOT_PROFILE_COUNTS,
    _cartesian_pair_bits,
    _iter_set_bits,
    hole_sums,
    inventory_catalog,
    midpoint_catalog,
    structural_core,
    target_shell,
)


EXPECTED_SURVIVORS = tuple(
    (core, *((
        (0, 38_544, 569_956, 116_064)
        if core == 4
        else (0, 0, 568_038, 107_602)
        if core == 9
        else (43_948, 33_760, 569_956, 108_558)
        if core == 12
        else (0, 0, 569_956, 116_064)
        if core == 15
        else (0, 0, 569_375, 107_737)
        if core == 18
        else (0, 38_544, 569_956, 116_064)
        if core == 20
        else (43_948, 38_544, 569_769, 116_064)
        if core == 23
        else (0, 0, 229_408, 0)
        if core == 27
        else ROOT_PROFILE_COUNTS
    ) if core else (0, 0, 0, 0)))
    for core in range(32)
)
EXPECTED_CLASS_SURVIVORS = tuple(
    (core, *((
        (0, 580, 6_191, 1_442)
        if core == 4
        else (0, 0, 6_179, 1_294)
        if core == 9
        else (516, 484, 6_191, 1_323)
        if core == 12
        else (0, 0, 6_191, 1_442)
        if core == 15
        else (0, 0, 6_185, 1_294)
        if core == 18
        else (0, 580, 6_191, 1_442)
        if core == 20
        else (516, 580, 6_179, 1_442)
        if core == 23
        else (0, 0, 2_864, 0)
        if core == 27
        else (516, 580, 6_191, 1_442)
    ) if core else (0, 0, 0, 0)))
    for core in range(32)
)
EXPECTED_SURVIVOR_SHA256 = (
    "e02bd6c38f70bf4000f9454accdcda7cfa602282fcfd421a61a0d74c4068c09e"
)
EXPECTED_CLASS_SURVIVOR_SHA256 = (
    "e7d7c93bfb2317c2485dcd93a08e8218b72d105bffa9b70861b3e9261c30d6bb"
)
EXPECTED_WEIGHTED_REJECTION = 906_241
EXPECTED_ADDITIONAL_REJECTION = 75_713
EXPECTED_REJECTED_PROFILE_CORE_CELLS = 11


def records_sha256(rows: Iterable[Sequence[int]]) -> str:
    digest = sha256()
    for row in rows:
        digest.update((",".join(map(str, row)) + "\n").encode())
    return digest.hexdigest()


def verify() -> dict[str, object]:
    catalog = inventory_catalog()
    features = catalog["features"]
    feature_classes = catalog["feature_classes"]
    class_profile = catalog["class_profile"]
    profile_index = {
        profile: index for index, profile in enumerate(ROOT_PROFILES)
    }
    class_permutations = {
        multiset: tuple(set(permutations(multiset)))
        for multiset in feature_classes
    }
    midpoint = midpoint_catalog(target_shell())

    geometry = defaultdict(lambda: defaultdict(lambda: [set(), set()]))
    for boundary_row in e2_boundary_rows():
        parameters, gauge_signs = decode_e2_boundary_row(boundary_row)
        core = structural_core(parameters)
        if core == 0:
            continue
        labels = normalized_projective_labels(parameters)
        sigma = gauge_signs[:3]
        tau = gauge_signs[3:]
        for eta, tail in product((-1, 1), repeat=2):
            upper_orientation = (
                1,
                sigma[0] * eta * tail,
                sigma[1],
                sigma[2] * eta * tail,
            )
            lower_gauge = (
                tau[0] * eta,
                tau[1] * tail,
                tau[2] * eta,
                tau[3] * tail,
            )
            geometry[core][eta, tail][0].add(
                (
                    0,
                    labels[0],
                    labels[4],
                    upper_orientation[0],
                    lower_gauge[0],
                    2,
                    labels[2],
                    labels[6],
                    upper_orientation[2],
                    lower_gauge[2],
                )
            )
            geometry[core][eta, tail][1].add(
                (
                    1,
                    labels[1],
                    labels[5],
                    upper_orientation[1],
                    lower_gauge[1],
                    3,
                    labels[3],
                    labels[7],
                    upper_orientation[3],
                    lower_gauge[3],
                )
            )

    survivor_rows = [(0, 0, 0, 0, 0)]
    class_rows = [(0, 0, 0, 0, 0)]
    for core in range(1, 32):
        @lru_cache(maxsize=None)
        def group_map(
            group: int,
            upper_label: int,
            lower_label: int,
            upper_orientation: int,
            lower_gauge: int,
        ):
            result = defaultdict(int)
            for feature_index, (
                p_sum,
                q_sum,
                q_terminal,
            ) in enumerate(features):
                for upper_epsilon in (-1, 1):
                    lower_epsilon = -upper_epsilon
                    lower_orientation = (
                        lower_gauge * lower_epsilon * q_terminal
                    )
                    at_one = tuple(
                        upper_orientation
                        * (p_sum + upper_epsilon * q_sum)
                        * VECTORS[upper_label][row]
                        + lower_orientation
                        * (p_sum + lower_epsilon * q_sum)
                        * VECTORS[lower_label][row]
                        for row in range(4)
                    )
                    at_i_before_phase = tuple(
                        upper_orientation
                        * (p_sum - upper_epsilon * q_sum)
                        * VECTORS[upper_label][row]
                        + lower_orientation
                        * (p_sum - lower_epsilon * q_sum)
                        * VECTORS[lower_label][row]
                        for row in range(4)
                    )
                    result[at_one, at_i_before_phase] |= 1 << feature_index
            return tuple(result.items())

        @lru_cache(maxsize=None)
        def half_map(key):
            (
                first_group,
                first_upper_label,
                first_lower_label,
                first_upper_orientation,
                first_lower_gauge,
                second_group,
                second_upper_label,
                second_lower_label,
                second_upper_orientation,
                second_lower_gauge,
            ) = key
            result = defaultdict(int)
            first_states = group_map(
                first_group,
                first_upper_label,
                first_lower_label,
                first_upper_orientation,
                first_lower_gauge,
            )
            second_states = group_map(
                second_group,
                second_upper_label,
                second_lower_label,
                second_upper_orientation,
                second_lower_gauge,
            )
            for (first_one, first_i), first_bits in first_states:
                for (second_one, second_i), second_bits in second_states:
                    at_one = tuple(
                        first_one[row] + second_one[row]
                        for row in range(4)
                    )
                    # The groups differ by two modulo four, so their
                    # root-i phases are negatives.
                    at_i = tuple(
                        first_i[row] - second_i[row] for row in range(4)
                    )
                    result[at_one, at_i] |= _cartesian_pair_bits(
                        first_bits, second_bits
                    )
            return tuple(result.items())

        def union_half(keys):
            result = defaultdict(int)
            for key in keys:
                for state, pair_bits in half_map(key):
                    result[state] |= pair_bits
            return result

        relation = [0] * (FEATURE_COUNT * FEATURE_COUNT)
        for (eta, tail), (even_keys, odd_keys) in geometry[core].items():
            even_states = union_half(even_keys)
            odd_states = union_half(odd_keys)
            odd_by_one = defaultdict(list)
            for (odd_one, odd_i), pair_bits in odd_states.items():
                odd_by_one[odd_one].append((odd_i, pair_bits))

            for (even_one, even_i), even_pair_bits in even_states.items():
                for h0, h8 in product((-1, 1), repeat=2):
                    half_hole_sum = (
                        h0 + eta,
                        h0 + eta,
                        h8 - eta,
                        h8 - eta,
                    )
                    root_i_real_holes = (
                        h0 - eta,
                        h0 - eta,
                        h8 + eta,
                        h8 + eta,
                    )
                    first_targets = midpoint.get(
                        tuple(
                            even_one[row] + half_hole_sum[row]
                            for row in range(4)
                        ),
                        (),
                    )
                    for h1, h9, h12 in product((-1, 1), repeat=3):
                        holes_at_one, _holes_at_minus_one = hole_sums(
                            eta, tail, h0, h1, h8, h9, h12
                        )
                        root_i_imaginary_holes = (
                            h1 - tail,
                            h1 + tail,
                            h9,
                            h12,
                        )
                        for first_target in first_targets:
                            required_odd = tuple(
                                first_target[row]
                                - even_one[row]
                                - holes_at_one[row]
                                for row in range(4)
                            )
                            for odd_i, odd_pair_bits in odd_by_one.get(
                                required_odd, ()
                            ):
                                root_i_norm = sum(
                                    (
                                        even_i[row]
                                        + root_i_real_holes[row]
                                    )
                                    ** 2
                                    + (
                                        odd_i[row]
                                        + root_i_imaginary_holes[row]
                                    )
                                    ** 2
                                    for row in range(4)
                                )
                                if root_i_norm != 334:
                                    continue
                                for even_pair in _iter_set_bits(
                                    even_pair_bits
                                ):
                                    relation[even_pair] |= odd_pair_bits

        inventory_survivors = [0] * 4
        class_survivors = [0] * 4
        for multiset, multiplicity in feature_classes.items():
            survives = any(
                (
                    relation[
                        assignment[0] * FEATURE_COUNT + assignment[2]
                    ]
                    >> (
                        assignment[1] * FEATURE_COUNT + assignment[3]
                    )
                )
                & 1
                for assignment in class_permutations[multiset]
            )
            if survives:
                index = profile_index[class_profile[multiset]]
                inventory_survivors[index] += multiplicity
                class_survivors[index] += 1

        survivor_rows.append((core, *inventory_survivors))
        class_rows.append((core, *class_survivors))
        group_map.cache_clear()
        half_map.cache_clear()

    survivors = tuple(survivor_rows)
    class_survivors = tuple(class_rows)
    if survivors != EXPECTED_SURVIVORS:
        raise AssertionError("the Phi_4 inventory-survivor table changed")
    if class_survivors != EXPECTED_CLASS_SURVIVORS:
        raise AssertionError("the Phi_4 class-survivor table changed")

    survivor_hash = records_sha256(survivors)
    class_survivor_hash = records_sha256(class_survivors)
    if survivor_hash != EXPECTED_SURVIVOR_SHA256:
        raise AssertionError("the Phi_4 inventory-survivor hash changed")
    if class_survivor_hash != EXPECTED_CLASS_SURVIVOR_SHA256:
        raise AssertionError("the Phi_4 class-survivor hash changed")

    weighted_rejection = sum(
        ROOT_PROFILE_COUNTS[index] - row[index + 1]
        for row in survivors[1:]
        for index in range(4)
    )
    if weighted_rejection != EXPECTED_WEIGHTED_REJECTION:
        raise AssertionError("the Phi_4 weighted rejection count changed")

    additional_rejection = sum(
        old[index] - new[index]
        for old, new in zip(
            EXPECTED_VERTICAL_SURVIVORS[1:], survivors[1:], strict=True
        )
        for index in range(1, 5)
    )
    if additional_rejection != EXPECTED_ADDITIONAL_REJECTION:
        raise AssertionError("the incremental Phi_4 rejection count changed")

    rejected_cells = sum(
        value == 0 for row in survivors[1:] for value in row[1:]
    )
    if rejected_cells != EXPECTED_REJECTED_PROFILE_CORE_CELLS:
        raise AssertionError("the Phi_4 profile/core cell count changed")

    return {
        "inventories": sum(feature_classes.values()),
        "feature_classes": len(feature_classes),
        "survivors": survivors,
        "class_survivors": class_survivors,
        "weighted_rejection": weighted_rejection,
        "additional_rejection": additional_rejection,
        "rejected_profile_core_cells": rejected_cells,
        "survivor_sha256": survivor_hash,
        "class_survivor_sha256": class_survivor_hash,
    }


def main() -> None:
    result = verify()
    print(
        "PASS: vertical-pair Phi_1/Phi_2/Phi_4 join classifies "
        f"{result['inventories']} inventories in "
        f"{result['feature_classes']} root/terminal classes"
    )
    print(
        "PASS: rejects "
        f"{result['rejected_profile_core_cells']} profile/core cells and "
        f"{result['weighted_rejection']} weighted inventory/core states"
    )
    print(
        "additional_phi4_rejection="
        f"{result['additional_rejection']}"
    )
    print(f"survivor_sha256={result['survivor_sha256']}")
    print(
        "class_survivor_sha256="
        f"{result['class_survivor_sha256']}"
    )


if __name__ == "__main__":
    main()
