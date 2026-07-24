#!/usr/bin/env python3
"""Verify the first exact dyadic sieve for paired-lobe five-combs.

This standard-library checker retains two deliberately different scopes.

``arbitrary-placement``
    Every assignment of the eight carrier amplitudes to the eight slots is
    relaxed to an arbitrary permutation and arbitrary independent signs.
    The exact physical hole fiber and the physical high-lag *parameter*
    projection are retained.  Infeasibility is therefore a valid necessary
    obstruction for the complete distinct-lobe family, while feasibility is
    only a relaxation.

``vertical-pair``
    The two polarizations of each directed pair occupy slots ``(g,g+4)``.
    The physical high-lag table is projected independently onto the even and
    odd two-component halves.  This loses compatibility information between
    the halves, so it is again a necessary relaxation, but only for this
    explicitly delimited vertical-pair placement slice.

At roots 1 and -1, let E and O be the four-row sums from even and odd slots,
and let H+ and H- be the corresponding hole sums.  The two spectral
conditions are

    ||E + O + H+||^2 = 334,
    ||E - O + H-||^2 = 334.

There are exactly 672 ordered target vectors T with squared norm 334 and
the required row parities.  If A and B are the two completed target vectors,

    (A+B)/2 = E + (H+ + H-)/2.

This midpoint identity is the exact two-pair-plus-two-pair hash join used
below.  It is the Phi_1/Phi_2 stage of the order-16 dyadic compression, not
the still-unchecked Phi_4/Phi_8/Phi_16 stages.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
from typing import Iterable, Iterator, Sequence

from verify_five_comb_high_lag_boundary import (
    canonical_rows_sha256,
    decode_e2_boundary_row,
    e2_boundary_rows,
    e2_parameter_rows,
    normalized_projective_labels,
)
from verify_five_comb_paired_lobes import (
    EXPECTED_DIRECTED_PAIR_SHA256,
    SIGNATURES,
    VECTORS,
    WORDS,
    valid_directed_pair_inventories,
)


TARGET_NORM = 334
FEATURE_COUNT = 40

ROOT_PROFILES = (
    (0, 0, 0, 0, 2, 2, 6, 6),
    (0, 0, 0, 2, 2, 2, 2, 8),
    (0, 0, 2, 2, 2, 4, 4, 6),
    (2, 2, 2, 2, 4, 4, 4, 4),
)
ROOT_PROFILE_COUNTS = (43_948, 38_544, 569_956, 116_064)

EXPECTED_E2_PARAMETER_COUNT = 2_434
EXPECTED_E2_FULL_COUNT = 10_934
EXPECTED_E2_PARAMETER_SHA256 = (
    "85972db2c71b3e1415705017b0f3f1e57aab3f7cba880104c8f60d83c687d2c0"
)
EXPECTED_E2_FULL_SHA256 = (
    "441c25786c4a0bc56f9e86c84bf9c8c8252595a9f75298aad960c31320aeb6b4"
)

EXPECTED_TARGET_COUNT = 672
EXPECTED_TARGET_MIDPOINT_COUNT = 116_389
EXPECTED_OCTET_PROFILE_COUNT = 35
EXPECTED_PAIR_SIGNATURE_TYPE_COUNT = 50
EXPECTED_COMPONENT_SIGNATURE_PROFILE_COUNT = 652
EXPECTED_ROOT_TERMINAL_FEATURE_CLASS_COUNT = 8_729

# Each row is ``(core, compatible profile 0, ..., compatible profile 3)``.
EXPECTED_ARBITRARY_COMPATIBLE = (
    (0, 0, 0, 0, 0),
    (1, 64, 64, 64, 64),
    (2, 120, 120, 120, 120),
    (3, 112, 112, 112, 112),
    (4, 20, 20, 20, 20),
    (5, 64, 64, 64, 64),
    (6, 120, 120, 120, 120),
    (7, 64, 64, 64, 64),
    (8, 24, 24, 24, 24),
    (9, 48, 64, 64, 64),
    (10, 60, 60, 60, 60),
    (11, 124, 124, 124, 124),
    (12, 32, 32, 32, 32),
    (13, 64, 64, 64, 64),
    (14, 128, 128, 128, 128),
    (15, 64, 64, 64, 64),
    (16, 44, 46, 46, 46),
    (17, 120, 120, 120, 120),
    (18, 44, 58, 58, 50),
    (19, 48, 48, 48, 48),
    (20, 30, 32, 32, 32),
    (21, 112, 112, 112, 112),
    (22, 112, 112, 112, 112),
    (23, 64, 64, 64, 64),
    (24, 52, 52, 52, 52),
    (25, 120, 120, 120, 120),
    (26, 116, 116, 116, 116),
    (27, 32, 28, 32, 32),
    (28, 54, 54, 54, 54),
    (29, 120, 120, 120, 120),
    (30, 128, 128, 128, 128),
    (31, 88, 88, 88, 88),
)
EXPECTED_ARBITRARY_COMPATIBLE_SHA256 = (
    "5642c89d258731c1b588b59df404596946010ca4d608fad97a121630fd5b76f0"
)
EXPECTED_ARBITRARY_REJECTED_COUNT = 78
EXPECTED_ARBITRARY_NONZERO_REJECTED_COUNT = 46
EXPECTED_ARBITRARY_WEIGHTED_REJECTION = 2_576_920
EXPECTED_ARBITRARY_REJECTED_SHA256 = (
    "97dcaf453e87ef59a7b803fb560a97e4a1ac57788088e5392b2c8574e6e8de5d"
)

# Inventory survival counts for the vertical-pair slice, by root profile.
_ALL_INVENTORIES = ROOT_PROFILE_COUNTS
EXPECTED_VERTICAL_SURVIVORS = tuple(
    (core, *((
        (0, 0, 569_956, 116_064)
        if core in (9, 15, 18)
        else (0, 38_544, 569_956, 116_064)
        if core == 20
        else (0, 0, 229_408, 0)
        if core == 27
        else _ALL_INVENTORIES
    ) if core else (0, 0, 0, 0)))
    for core in range(32)
)
EXPECTED_VERTICAL_WEIGHTED_REJECTION = 830_528
EXPECTED_VERTICAL_PROFILE_CORE_REJECTIONS = 10
EXPECTED_VERTICAL_SURVIVOR_SHA256 = (
    "493d617f55c95d24ca2749e5726942e6265cdf4eea1b0ccf245ea9cd5987d342"
)
EXPECTED_VERTICAL_CLASS_SURVIVOR_SHA256 = (
    "81d80e6f4cd643c652e714e58163841b74067beff57156b8a7d953b57198c78e"
)

EXPECTED_ENDPOINT_SPLIT = Counter(
    {
        (0, 4): 11_398,
        (1, 3): 175_968,
        (2, 2): 393_780,
        (3, 1): 175_968,
        (4, 0): 11_398,
    }
)


Vector = tuple[int, int, int, int]
Profile = tuple[int, ...]
FeatureMultiset = tuple[int, int, int, int]


def records_sha256(rows: Iterable[Sequence[int]]) -> str:
    """Hash comma-separated integer records terminated by LF."""

    digest = sha256()
    for row in rows:
        digest.update((",".join(map(str, row)) + "\n").encode())
    return digest.hexdigest()


def structural_core(parameters: Sequence[int]) -> int:
    """Pack the five structural projective bits as a little-endian integer."""

    return sum(parameters[index] << index for index in range(5))


def target_shell() -> tuple[Vector, ...]:
    """Return all ordered row-sum vectors with norm 334 and row parities."""

    result = []
    for first in range(-84, 85, 2):
        for second in range(-84, 85, 2):
            for third in range(-83, 84, 2):
                remainder = (
                    TARGET_NORM
                    - first * first
                    - second * second
                    - third * third
                )
                if remainder < 0:
                    continue
                fourth = int(remainder**0.5)
                if fourth * fourth != remainder or fourth % 2 == 0:
                    continue
                for signed_fourth in {fourth, -fourth}:
                    if -83 <= signed_fourth <= 83:
                        result.append(
                            (first, second, third, signed_fourth)
                        )
    shell = tuple(sorted(result))
    if len(shell) != EXPECTED_TARGET_COUNT or len(set(shell)) != len(shell):
        raise AssertionError("the 334-shell count changed")
    return shell


def midpoint_catalog(
    shell: Sequence[Vector],
) -> dict[Vector, tuple[Vector, ...]]:
    """Index ordered shell pairs by their integral midpoint."""

    result: defaultdict[Vector, list[Vector]] = defaultdict(list)
    for first in shell:
        for second in shell:
            midpoint = tuple(
                (first[row] + second[row]) // 2 for row in range(4)
            )
            if any(
                2 * midpoint[row] != first[row] + second[row]
                for row in range(4)
            ):
                raise AssertionError("a target midpoint was not integral")
            result[midpoint].append(first)
    catalog = {key: tuple(values) for key, values in result.items()}
    if len(catalog) != EXPECTED_TARGET_MIDPOINT_COUNT:
        raise AssertionError("the target-midpoint count changed")
    if sum(map(len, catalog.values())) != len(shell) ** 2:
        raise AssertionError("the midpoint catalog lost an ordered pair")
    return catalog


def hole_sums(
    eta: int,
    tail: int,
    h0: int,
    h1: int,
    h8: int,
    h9: int,
    h12: int,
) -> tuple[Vector, Vector]:
    """Return the exact hole evaluations at roots +1 and -1."""

    plus = (
        h0 + h1 + eta + tail,
        h0 + h1 + eta - tail,
        h8 + h9 - eta,
        h8 + h12 - eta,
    )
    minus = (
        h0 - h1 + eta - tail,
        h0 - h1 + eta + tail,
        h8 - h9 - eta,
        h8 - h12 - eta,
    )
    return plus, minus


def word_signature_sum(pair_code: int) -> tuple[int, ...]:
    first, second = divmod(pair_code, 16)
    return tuple(
        SIGNATURES[first][lag] + SIGNATURES[second][lag]
        for lag in range(4)
    )


def pair_root_profile(pair_code: int) -> tuple[int, int]:
    first, second = divmod(pair_code, 16)
    left = sum(WORDS[first])
    right = sum(WORDS[second])
    return tuple(sorted((abs(left + right), abs(left - right))))


def root_terminal_features() -> tuple[tuple[int, int, int], ...]:
    """Return the 40 exact pair features used by the vertical slice."""

    features = tuple(
        sorted(
            {
                (sum(first), sum(second), second[-1])
                for first in WORDS
                for second in WORDS
            }
        )
    )
    if len(features) != FEATURE_COUNT:
        raise AssertionError("the root/terminal feature count changed")
    return features


def inventory_catalog() -> dict[str, object]:
    """Reconstruct all component/profile classes in one MITM inventory pass."""

    features = root_terminal_features()
    feature_index = {feature: index for index, feature in enumerate(features)}
    code_feature = tuple(
        feature_index[
            (
                sum(WORDS[code // 16]),
                sum(WORDS[code % 16]),
                WORDS[code % 16][-1],
            )
        ]
        for code in range(256)
    )

    digest = sha256()
    feature_classes: Counter[FeatureMultiset] = Counter()
    octet_profiles = set()
    component_profiles = set()
    component_to_root: defaultdict[tuple[tuple[int, ...], ...], set[Profile]]
    component_to_root = defaultdict(set)
    profile_counts: Counter[Profile] = Counter()
    endpoint_split: Counter[tuple[int, int]] = Counter()

    for inventory in valid_directed_pair_inventories():
        digest.update((",".join(map(str, inventory)) + "\n").encode())
        feature_multiset = tuple(sorted(code_feature[code] for code in inventory))
        feature_classes[feature_multiset] += 1

        word_indices = tuple(code // 16 for code in inventory) + tuple(
            code % 16 for code in inventory
        )
        octet_profiles.add(
            tuple(sorted(SIGNATURES[index] for index in word_indices))
        )
        component_profile = tuple(
            sorted(word_signature_sum(code) for code in inventory)
        )
        component_profiles.add(component_profile)
        root_profile = tuple(
            sorted(
                magnitude
                for code in inventory
                for magnitude in pair_root_profile(code)
            )
        )
        component_to_root[component_profile].add(root_profile)
        profile_counts[root_profile] += 1
        endpoint_split[
            (
                sum(WORDS[code // 16][-1] > 0 for code in inventory),
                sum(WORDS[code % 16][-1] > 0 for code in inventory),
            )
        ] += 1

    if digest.hexdigest() != EXPECTED_DIRECTED_PAIR_SHA256:
        raise AssertionError("the directed-pair inventory digest changed")
    if sum(feature_classes.values()) != 768_512:
        raise AssertionError("the directed-pair inventory count changed")
    if len(feature_classes) != EXPECTED_ROOT_TERMINAL_FEATURE_CLASS_COUNT:
        raise AssertionError("the root/terminal feature-class count changed")
    if len(octet_profiles) != EXPECTED_OCTET_PROFILE_COUNT:
        raise AssertionError("the octet signature-profile count changed")
    if (
        len({word_signature_sum(code) for code in range(256)})
        != EXPECTED_PAIR_SIGNATURE_TYPE_COUNT
    ):
        raise AssertionError("the directed-pair signature-type count changed")
    if len(component_profiles) != EXPECTED_COMPONENT_SIGNATURE_PROFILE_COUNT:
        raise AssertionError("the four-component signature count changed")
    if any(len(images) != 1 for images in component_to_root.values()):
        raise AssertionError(
            "a component signature profile has two root profiles"
        )
    if tuple(profile_counts[profile] for profile in ROOT_PROFILES) != (
        ROOT_PROFILE_COUNTS
    ):
        raise AssertionError("the four root-profile counts changed")
    if endpoint_split != EXPECTED_ENDPOINT_SPLIT:
        raise AssertionError("the five endpoint-split counts changed")

    class_profile = {
        multiset: tuple(
            sorted(
                magnitude
                for feature in multiset
                for magnitude in (
                    abs(features[feature][0] + features[feature][1]),
                    abs(features[feature][0] - features[feature][1]),
                )
            )
        )
        for multiset in feature_classes
    }
    if {
        class_profile[multiset] for multiset in feature_classes
    } != set(ROOT_PROFILES):
        raise AssertionError("a feature class has an unknown root profile")

    return {
        "features": features,
        "feature_classes": feature_classes,
        "class_profile": class_profile,
        "octet_profiles": len(octet_profiles),
        "component_profiles": len(component_profiles),
        "profile_counts": profile_counts,
        "endpoint_split": endpoint_split,
    }


def profile_splits(profile: Profile) -> tuple[tuple[Profile, Profile], ...]:
    """Split eight amplitudes into four even-slot and four odd-slot values."""

    result = set()
    indices = range(8)
    for selected in combinations(indices, 4):
        selected_set = set(selected)
        even = tuple(sorted(profile[index] for index in selected_set))
        odd = tuple(
            sorted(
                profile[index]
                for index in indices
                if index not in selected_set
            )
        )
        result.add((even, odd))
    return tuple(sorted(result))


def arbitrary_placement_sieve(
    midpoint: dict[Vector, tuple[Vector, ...]],
) -> dict[str, object]:
    """Run the placement-independent root-profile relaxation."""

    @lru_cache(maxsize=None)
    def signed_sums(labels: tuple[int, ...], magnitudes: Profile) -> frozenset[Vector]:
        result = set()
        for assigned in set(permutations(magnitudes)):
            for signs in product((-1, 1), repeat=4):
                result.add(
                    tuple(
                        sum(
                            signs[slot]
                            * assigned[slot]
                            * VECTORS[labels[slot]][row]
                            for slot in range(4)
                        )
                        for row in range(4)
                    )
                )
        return frozenset(result)

    @lru_cache(maxsize=None)
    def cached_splits(profile: Profile) -> tuple[tuple[Profile, Profile], ...]:
        return profile_splits(profile)

    def is_feasible(labels: Sequence[int], profile: Profile) -> bool:
        even_labels = tuple(labels[index] for index in (0, 2, 4, 6))
        odd_labels = tuple(labels[index] for index in (1, 3, 5, 7))
        for even_magnitudes, odd_magnitudes in cached_splits(profile):
            even_vectors = signed_sums(even_labels, even_magnitudes)
            odd_vectors = signed_sums(odd_labels, odd_magnitudes)
            for even in even_vectors:
                for eta, h0, h8 in product((-1, 1), repeat=3):
                    half_hole_sum = (
                        h0 + eta,
                        h0 + eta,
                        h8 - eta,
                        h8 - eta,
                    )
                    first_targets = midpoint.get(
                        tuple(
                            even[row] + half_hole_sum[row]
                            for row in range(4)
                        ),
                        (),
                    )
                    if not first_targets:
                        continue
                    for tail, h1, h9, h12 in product((-1, 1), repeat=4):
                        holes_at_one, _holes_at_minus_one = hole_sums(
                            eta, tail, h0, h1, h8, h9, h12
                        )
                        for first_target in first_targets:
                            required_odd = tuple(
                                first_target[row]
                                - even[row]
                                - holes_at_one[row]
                                for row in range(4)
                            )
                            if required_odd in odd_vectors:
                                return True
        return False

    parameters = e2_parameter_rows()
    if (
        len(parameters) != EXPECTED_E2_PARAMETER_COUNT
        or canonical_rows_sha256(parameters) != EXPECTED_E2_PARAMETER_SHA256
    ):
        raise AssertionError("the physical parameter table changed")

    compatible: defaultdict[int, list[int]] = defaultdict(lambda: [0] * 4)
    rejected = []
    for parameter_row in parameters:
        core = structural_core(parameter_row)
        labels = normalized_projective_labels(parameter_row)
        for profile_index, profile in enumerate(ROOT_PROFILES):
            if is_feasible(labels, profile):
                compatible[core][profile_index] += 1
            else:
                rejected.append((*parameter_row, profile_index))

    compatible_rows = tuple(
        (core, *compatible[core]) for core in range(32)
    )
    if compatible_rows != EXPECTED_ARBITRARY_COMPATIBLE:
        raise AssertionError("the arbitrary-placement compatibility table changed")
    if (
        records_sha256(compatible_rows)
        != EXPECTED_ARBITRARY_COMPATIBLE_SHA256
    ):
        raise AssertionError("the arbitrary-placement table hash changed")
    if len(rejected) != EXPECTED_ARBITRARY_REJECTED_COUNT:
        raise AssertionError("the arbitrary-placement rejection count changed")
    nonzero_rejected = tuple(
        row for row in rejected if structural_core(row[:12]) != 0
    )
    if len(nonzero_rejected) != EXPECTED_ARBITRARY_NONZERO_REJECTED_COUNT:
        raise AssertionError("the nonzero-core rejection count changed")

    weighted_rejection = sum(
        ROOT_PROFILE_COUNTS[row[-1]] for row in nonzero_rejected
    )
    if weighted_rejection != EXPECTED_ARBITRARY_WEIGHTED_REJECTION:
        raise AssertionError("the weighted arbitrary rejection count changed")

    signed_sums.cache_clear()
    cached_splits.cache_clear()
    return {
        "compatible": compatible_rows,
        "rejected": tuple(rejected),
        "nonzero_rejected": nonzero_rejected,
        "weighted_rejection": weighted_rejection,
    }


def _iter_set_bits(value: int) -> Iterator[int]:
    while value:
        bit = value & -value
        yield bit.bit_length() - 1
        value -= bit


def _cartesian_pair_bits(left: int, right: int) -> int:
    result = 0
    for index in _iter_set_bits(left):
        result |= right << (FEATURE_COUNT * index)
    return result


def vertical_pair_sieve(
    midpoint: dict[Vector, tuple[Vector, ...]],
    catalog: dict[str, object],
) -> dict[str, object]:
    """Run the projected high-lag sieve for the vertical-pair slice."""

    features = catalog["features"]
    feature_classes = catalog["feature_classes"]
    class_profile = catalog["class_profile"]
    if not isinstance(features, tuple) or not isinstance(
        feature_classes, Counter
    ) or not isinstance(class_profile, dict):
        raise TypeError("the inventory catalog has an unexpected schema")

    class_permutations = {
        multiset: tuple(sorted(set(permutations(multiset))))
        for multiset in feature_classes
    }

    @lru_cache(maxsize=None)
    def group_map(
        group: int,
        upper_label: int,
        lower_label: int,
        upper_orientation: int,
        lower_gauge: int,
    ) -> tuple[tuple[Vector, int], ...]:
        result: defaultdict[Vector, int] = defaultdict(int)
        for feature_index, (p_sum, q_sum, q_terminal) in enumerate(features):
            for upper_epsilon in (-1, 1):
                lower_epsilon = -upper_epsilon
                lower_orientation = (
                    lower_gauge * lower_epsilon * q_terminal
                )
                vector = tuple(
                    upper_orientation
                    * (p_sum + upper_epsilon * q_sum)
                    * VECTORS[upper_label][row]
                    + lower_orientation
                    * (p_sum + lower_epsilon * q_sum)
                    * VECTORS[lower_label][row]
                    for row in range(4)
                )
                result[vector] |= 1 << feature_index
        return tuple(result.items())

    @lru_cache(maxsize=None)
    def half_map(key: tuple[int, ...]) -> tuple[tuple[Vector, int], ...]:
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
        result: defaultdict[Vector, int] = defaultdict(int)
        for first_vector, first_bits in group_map(
            first_group,
            first_upper_label,
            first_lower_label,
            first_upper_orientation,
            first_lower_gauge,
        ):
            for second_vector, second_bits in group_map(
                second_group,
                second_upper_label,
                second_lower_label,
                second_upper_orientation,
                second_lower_gauge,
            ):
                vector = tuple(
                    first_vector[row] + second_vector[row]
                    for row in range(4)
                )
                result[vector] |= _cartesian_pair_bits(
                    first_bits, second_bits
                )
        return tuple(result.items())

    full_rows = e2_boundary_rows()
    if (
        len(full_rows) != EXPECTED_E2_FULL_COUNT
        or canonical_rows_sha256(full_rows) != EXPECTED_E2_FULL_SHA256
    ):
        raise AssertionError("the physical full boundary table changed")

    # Project the table independently onto the even and odd halves.  This
    # intentional relaxation can add states but cannot delete a true state.
    geometry: defaultdict[
        int,
        defaultdict[tuple[int, int], list[set[tuple[int, ...]]]],
    ] = defaultdict(lambda: defaultdict(lambda: [set(), set()]))
    for boundary_row in full_rows:
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

    def union_half(keys: Iterable[tuple[int, ...]]) -> dict[Vector, int]:
        result: defaultdict[Vector, int] = defaultdict(int)
        for key in keys:
            for vector, pair_bits in half_map(key):
                result[vector] |= pair_bits
        return dict(result)

    profile_index = {
        profile: index for index, profile in enumerate(ROOT_PROFILES)
    }
    survivor_rows = [(0, 0, 0, 0, 0)]
    survivor_class_rows = [(0, 0, 0, 0, 0)]
    rejected_profile_core_cells = 0

    for core in range(1, 32):
        relation = [0] * (FEATURE_COUNT * FEATURE_COUNT)
        for (eta, tail), (even_keys, odd_keys) in geometry[core].items():
            even_states = union_half(even_keys)
            odd_states = union_half(odd_keys)
            for even, even_pair_bits in even_states.items():
                for h0, h8 in product((-1, 1), repeat=2):
                    half_hole_sum = (
                        h0 + eta,
                        h0 + eta,
                        h8 - eta,
                        h8 - eta,
                    )
                    first_targets = midpoint.get(
                        tuple(
                            even[row] + half_hole_sum[row]
                            for row in range(4)
                        ),
                        (),
                    )
                    if not first_targets:
                        continue
                    for h1, h9, h12 in product((-1, 1), repeat=3):
                        holes_at_one, _holes_at_minus_one = hole_sums(
                            eta, tail, h0, h1, h8, h9, h12
                        )
                        for first_target in first_targets:
                            required_odd = tuple(
                                first_target[row]
                                - even[row]
                                - holes_at_one[row]
                                for row in range(4)
                            )
                            odd_pair_bits = odd_states.get(required_odd)
                            if odd_pair_bits is None:
                                continue
                            for even_pair in _iter_set_bits(even_pair_bits):
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

        rejected_profile_core_cells += sum(
            value == 0 for value in inventory_survivors
        )
        survivor_rows.append((core, *inventory_survivors))
        survivor_class_rows.append((core, *class_survivors))

    survivor_rows_tuple = tuple(survivor_rows)
    if survivor_rows_tuple != EXPECTED_VERTICAL_SURVIVORS:
        raise AssertionError("the vertical-pair survivor table changed")
    if rejected_profile_core_cells != EXPECTED_VERTICAL_PROFILE_CORE_REJECTIONS:
        raise AssertionError("the vertical profile/core rejection count changed")

    weighted_rejection = sum(
        ROOT_PROFILE_COUNTS[index] - row[index + 1]
        for row in survivor_rows_tuple[1:]
        for index in range(4)
    )
    if weighted_rejection != EXPECTED_VERTICAL_WEIGHTED_REJECTION:
        raise AssertionError("the weighted vertical rejection count changed")

    group_map.cache_clear()
    half_map.cache_clear()
    return {
        "survivors": survivor_rows_tuple,
        "class_survivors": tuple(survivor_class_rows),
        "weighted_rejection": weighted_rejection,
        "rejected_profile_core_cells": rejected_profile_core_cells,
    }


def verify_all() -> dict[str, object]:
    shell = target_shell()
    midpoint = midpoint_catalog(shell)
    catalog = inventory_catalog()
    arbitrary = arbitrary_placement_sieve(midpoint)
    vertical = vertical_pair_sieve(midpoint, catalog)
    result = {
        "target_shell": len(shell),
        "target_midpoints": len(midpoint),
        "inventories": sum(catalog["feature_classes"].values()),
        "octet_profiles": catalog["octet_profiles"],
        "component_profiles": catalog["component_profiles"],
        "feature_classes": len(catalog["feature_classes"]),
        "arbitrary_rejections": len(arbitrary["rejected"]),
        "arbitrary_nonzero_rejections": len(
            arbitrary["nonzero_rejected"]
        ),
        "arbitrary_weighted_rejection": arbitrary["weighted_rejection"],
        "vertical_weighted_rejection": vertical["weighted_rejection"],
        "vertical_profile_core_rejections": vertical[
            "rejected_profile_core_cells"
        ],
        "arbitrary_rejected_sha256": records_sha256(
            arbitrary["rejected"]
        ),
        "vertical_survivor_sha256": records_sha256(
            vertical["survivors"]
        ),
        "vertical_class_survivor_sha256": records_sha256(
            vertical["class_survivors"]
        ),
    }
    if (
        result["arbitrary_rejected_sha256"]
        != EXPECTED_ARBITRARY_REJECTED_SHA256
    ):
        raise AssertionError("the arbitrary rejected-row hash changed")
    if (
        result["vertical_survivor_sha256"]
        != EXPECTED_VERTICAL_SURVIVOR_SHA256
    ):
        raise AssertionError("the vertical survivor-row hash changed")
    if (
        result["vertical_class_survivor_sha256"]
        != EXPECTED_VERTICAL_CLASS_SURVIVOR_SHA256
    ):
        raise AssertionError("the vertical class-survivor hash changed")
    return result


def main() -> None:
    result = verify_all()
    print(
        "PASS: 768512 inventories -> 35 octet profiles -> "
        "652 component-signature profiles -> 8729 root/terminal classes"
    )
    print(
        "PASS: arbitrary-placement Phi_1/Phi_2 relaxation rejects "
        f"{result['arbitrary_nonzero_rejections']} new map/profile rows; "
        f"weighted states {result['arbitrary_weighted_rejection']}"
    )
    print(
        "PASS: vertical-pair projected join rejects "
        f"{result['vertical_profile_core_rejections']} profile/core cells; "
        f"weighted inventory/core states {result['vertical_weighted_rejection']}"
    )
    print(
        "arbitrary_rejected_sha256="
        f"{result['arbitrary_rejected_sha256']}"
    )
    print(
        "vertical_survivor_sha256="
        f"{result['vertical_survivor_sha256']}"
    )
    print(
        "vertical_class_survivor_sha256="
        f"{result['vertical_class_survivor_sha256']}"
    )


if __name__ == "__main__":
    main()
