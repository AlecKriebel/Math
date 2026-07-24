#!/usr/bin/env python3
"""Verify the primitive-eighth-root vertical-pair five-comb sieve.

This extends ``verify_five_comb_root4_vertical.py`` in exactly the same
delimited vertical-placement slice.  The two polarizations of one directed
pair occupy translated carrier slots ``g`` and ``g+4`` (physical
translations ``g`` and ``20+g``), while the even and odd halves remain
independent projections of the physical high-lag table.  Rejection is
therefore sound for this slice; survival is only a necessary condition.

At a primitive eighth root ``zeta=(1+i)/sqrt(2)``, write the completed
four-row evaluation as

    E + zeta O,              E,O in Z[i]^4.

The exact spectral equation ``sum |E+zeta O|^2 = 334`` is equivalent to
the two integer equations

    sum (|E|^2+|O|^2) = 334,
    sum Re((1-i) E conjugate(O)) = 0.

The first equation is the rational coefficient and the second is the
coefficient of ``sqrt(2)``.  Both are imposed below after the existing
roots ``+1,-1,i`` join.  The inventory feature now retains the ordinary
and alternating sums of both length-five lobe words.

No arbitrary-placement claim, base sequence, or Hadamard matrix is made.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
from typing import Iterable, Iterator, Sequence

from verify_five_comb_high_lag_boundary import (
    decode_e2_boundary_row,
    e2_boundary_rows,
    normalized_projective_labels,
)
from verify_five_comb_paired_lobes import (
    EXPECTED_DIRECTED_PAIR_SHA256,
    VECTORS,
    WORDS,
    valid_directed_pair_inventories,
)
from verify_five_comb_root12_sieve import (
    ROOT_PROFILES,
    ROOT_PROFILE_COUNTS,
    hole_sums,
    midpoint_catalog,
    structural_core,
    target_shell,
)


EXPECTED_FEATURE_COUNT = 108
EXPECTED_FEATURE_CLASS_COUNT = 87_695
EXPECTED_INVENTORY_COUNT = 768_512
EXPECTED_CORE4_SURVIVORS = (4, 0, 12_307, 101_157, 26_543)
EXPECTED_CORE4_CLASS_SURVIVORS = (4, 0, 1_973, 11_528, 2_509)
EXPECTED_CORE4_RELATION_SHA256 = (
    "7fd0597c2f7b75bcc604b99bca759e54487f2d53a61fb7a37d0c5d95e42f96f3"
)
EXPECTED_CORE4_SURVIVOR_SHA256 = (
    "1533a8d7b698104efdf9a02610e6d96150d7f43b7afbf68df6f91cf23a6135e4"
)
EXPECTED_CORE4_CLASS_SURVIVOR_SHA256 = (
    "9df4aba1bdbd258f5114cbfed9148a78f1593c4a98f8ed6e800362d73fa2cda7"
)
EXPECTED_CORE27_SURVIVORS = (27, 0, 0, 65_868, 0)
EXPECTED_CORE27_RELATION_SHA256 = (
    "4de8ebc0c28d8d11abc475dcacfecea0baa0b63a098415af8875cc2d2dd9f11c"
)
EXPECTED_CORE27_SURVIVOR_SHA256 = (
    "0be791f30d80f710b6e7a49740a0b7e1890364037eaf5a3ad049f0e975802f59"
)
EXPECTED_CORE27_CLASS_SURVIVOR_SHA256 = (
    "ce90670432090cd957ede45a8e9b6814650a06bf3a917dc39845013eaf376fd8"
)

Vector = tuple[int, int, int, int]
Gaussian = tuple[int, int]
GaussianVector = tuple[Gaussian, Gaussian, Gaussian, Gaussian]
Feature = tuple[int, int, int, int, int]
FeatureMultiset = tuple[int, int, int, int]


def records_sha256(rows: Iterable[Sequence[int]]) -> str:
    digest = sha256()
    for row in rows:
        digest.update((",".join(map(str, row)) + "\n").encode())
    return digest.hexdigest()


def alternating_sum(word: Sequence[int]) -> int:
    return sum((1 if index % 2 == 0 else -1) * value for index, value in enumerate(word))


def root8_features() -> tuple[Feature, ...]:
    features = tuple(
        sorted(
            {
                (
                    sum(first),
                    sum(second),
                    second[-1],
                    alternating_sum(first),
                    alternating_sum(second),
                )
                for first in WORDS
                for second in WORDS
            }
        )
    )
    if len(features) != EXPECTED_FEATURE_COUNT:
        raise AssertionError("the primitive-eight feature count changed")
    return features


def inventory_catalog() -> dict[str, object]:
    """Classify all valid directed-pair inventories by root-8 features."""

    features = root8_features()
    feature_index = {feature: index for index, feature in enumerate(features)}
    code_feature = tuple(
        feature_index[
            (
                sum(WORDS[code // 16]),
                sum(WORDS[code % 16]),
                WORDS[code % 16][-1],
                alternating_sum(WORDS[code // 16]),
                alternating_sum(WORDS[code % 16]),
            )
        ]
        for code in range(256)
    )

    digest = sha256()
    feature_classes: Counter[FeatureMultiset] = Counter()
    for inventory in valid_directed_pair_inventories():
        digest.update((",".join(map(str, inventory)) + "\n").encode())
        feature_classes[
            tuple(sorted(code_feature[code] for code in inventory))
        ] += 1

    if digest.hexdigest() != EXPECTED_DIRECTED_PAIR_SHA256:
        raise AssertionError("the directed-pair inventory digest changed")
    if sum(feature_classes.values()) != EXPECTED_INVENTORY_COUNT:
        raise AssertionError("the directed-pair inventory count changed")
    if len(feature_classes) != EXPECTED_FEATURE_CLASS_COUNT:
        raise AssertionError("the root-8 feature-class count changed")

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
    if set(class_profile.values()) != set(ROOT_PROFILES):
        raise AssertionError("a root-8 feature class has an unknown root profile")

    return {
        "features": features,
        "feature_classes": feature_classes,
        "class_profile": class_profile,
    }


def _iter_set_bits(value: int) -> Iterator[int]:
    while value:
        bit = value & -value
        yield bit.bit_length() - 1
        value -= bit


def _cartesian_pair_bits(left: int, right: int, feature_count: int) -> int:
    result = 0
    for index in _iter_set_bits(left):
        result |= right << (feature_count * index)
    return result


def gaussian_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gaussian_add_i_times(left: Gaussian, right: Gaussian) -> Gaussian:
    """Return ``left + i*right`` in integer Cartesian coordinates."""

    return left[0] - right[1], left[1] + right[0]


def rational_norm(even: GaussianVector, odd: GaussianVector) -> int:
    return sum(
        real * real + imag * imag
        for vector in (even, odd)
        for real, imag in vector
    )


def sqrt2_coefficient(even: GaussianVector, odd: GaussianVector) -> int:
    """Return ``sum Re((1-i) E conjugate(O))``."""

    return sum(
        even_real * (odd_real - odd_imag)
        + even_imag * (odd_real + odd_imag)
        for (even_real, even_imag), (odd_real, odd_imag) in zip(
            even, odd, strict=True
        )
    )


def verify_primitive_eight_split() -> dict[str, int]:
    """Exhaust the norm split and carrier formula independently."""

    split_checks = 0
    for even_real, even_imag, odd_real, odd_imag in product(
        range(-2, 3), repeat=4
    ):
        rational = (
            even_real * even_real
            + even_imag * even_imag
            + odd_real * odd_real
            + odd_imag * odd_imag
        )
        irrational = (
            even_real * (odd_real - odd_imag)
            + even_imag * (odd_real + odd_imag)
        )

        # Independently represent sqrt(2)*Re(E+zeta O) and
        # sqrt(2)*Im(E+zeta O) as pairs ``r+s*sqrt(2)``. Their squared
        # sum is twice the desired norm.
        scaled_real = (odd_real - odd_imag, even_real)
        scaled_imag = (odd_real + odd_imag, even_imag)

        def square_quadratic(value):
            constant, root = value
            return (
                constant * constant + 2 * root * root,
                2 * constant * root,
            )

        direct_real = square_quadratic(scaled_real)
        direct_imag = square_quadratic(scaled_imag)
        direct_twice_norm = (
            direct_real[0] + direct_imag[0],
            direct_real[1] + direct_imag[1],
        )
        if direct_twice_norm != (2 * rational, 2 * irrational):
            raise AssertionError("the primitive-eight norm split failed")
        split_checks += 1

    def add_monomial(coefficients, exponent, value):
        reduced = exponent % 8
        if reduced >= 4:
            reduced -= 4
            value = -value
        coefficients[reduced] += value

    carrier_checks = 0
    for first, second in product(WORDS, repeat=2):
        p_alternating = alternating_sum(first)
        q_alternating = alternating_sum(second)
        for epsilon, upper, lower in product((-1, 1), repeat=3):
            coefficients = [0, 0, 0, 0]
            for index, value in enumerate(first):
                add_monomial(coefficients, 4 * index, upper * value)
                add_monomial(coefficients, 20 + 4 * index, lower * value)
            for index, value in enumerate(second):
                add_monomial(
                    coefficients,
                    42 + 4 * index,
                    upper * epsilon * value,
                )
                add_monomial(
                    coefficients,
                    62 + 4 * index,
                    -lower * epsilon * value,
                )
            expected = (
                p_alternating * (upper - lower),
                0,
                epsilon * q_alternating * (upper + lower),
                0,
            )
            if tuple(coefficients) != expected:
                raise AssertionError("the direct root-8 carrier formula failed")
            carrier_checks += 1

    hole_checks = 0
    for eta, tail, h0, h1, h8, h9, h12 in product((-1, 1), repeat=7):
        even, odd = primitive_eight_holes(
            eta, tail, h0, h1, h8, h9, h12
        )
        row_holes = (
            ((40, h0), (41, h1), (82, eta), (83, tail)),
            ((40, h0), (41, h1), (82, eta), (83, -tail)),
            ((40, h8), (41, h9), (82, -eta)),
            ((40, h8), (41, h12), (82, -eta)),
        )
        for row, entries in enumerate(row_holes):
            coefficients = [0, 0, 0, 0]
            for exponent, value in entries:
                add_monomial(coefficients, exponent, value)
            reconstructed = (
                even[row][0],
                odd[row][0],
                even[row][1],
                odd[row][1],
            )
            if tuple(coefficients) != reconstructed:
                raise AssertionError("the direct root-8 hole formula failed")
            hole_checks += 1

    return {
        "split_checks": split_checks,
        "carrier_checks": carrier_checks,
        "hole_checks": hole_checks,
    }


def geometry_by_core():
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
    return geometry


def primitive_eight_holes(
    eta: int,
    tail: int,
    h0: int,
    h1: int,
    h8: int,
    h9: int,
    h12: int,
) -> tuple[GaussianVector, GaussianVector]:
    """Return ``E,O`` for the fourteen physical holes at a root of order 8."""

    even = (
        (h0, eta),
        (h0, eta),
        (h8, -eta),
        (h8, -eta),
    )
    odd = (
        (h1, tail),
        (h1, -tail),
        (h9, 0),
        (h12, 0),
    )
    return even, odd


def verify(
    selected_cores: Sequence[int] | None = None,
) -> dict[str, object]:
    """Run the exact roots 1,2,4,8 vertical-pair sieve."""

    verify_primitive_eight_split()
    catalog = inventory_catalog()
    features = catalog["features"]
    feature_classes = catalog["feature_classes"]
    class_profile = catalog["class_profile"]
    if not isinstance(features, tuple) or not isinstance(
        feature_classes, Counter
    ) or not isinstance(class_profile, dict):
        raise TypeError("the primitive-eight catalog has an unexpected schema")

    feature_count = len(features)
    profile_index = {
        profile: index for index, profile in enumerate(ROOT_PROFILES)
    }
    midpoint = midpoint_catalog(target_shell())
    geometry = geometry_by_core()
    cores = tuple(selected_cores) if selected_cores is not None else tuple(range(1, 32))
    if any(core < 1 or core > 31 for core in cores):
        raise ValueError("cores must lie in 1,...,31")

    survivor_rows = []
    class_rows = []
    relation_hashes = []
    for core in cores:
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
                p_alternating,
                q_alternating,
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
                    at_zeta_before_phase = tuple(
                        (
                            p_alternating
                            * (
                                upper_orientation
                                * VECTORS[upper_label][row]
                                - lower_orientation
                                * VECTORS[lower_label][row]
                            ),
                            upper_epsilon
                            * q_alternating
                            * (
                                upper_orientation
                                * VECTORS[upper_label][row]
                                + lower_orientation
                                * VECTORS[lower_label][row]
                            ),
                        )
                        for row in range(4)
                    )
                    result[
                        at_one, at_i_before_phase, at_zeta_before_phase
                    ] |= 1 << feature_index
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
            for (first_one, first_i, first_zeta), first_bits in first_states:
                for (second_one, second_i, second_zeta), second_bits in second_states:
                    at_one = tuple(
                        first_one[row] + second_one[row] for row in range(4)
                    )
                    at_i = tuple(
                        first_i[row] - second_i[row] for row in range(4)
                    )
                    at_zeta = tuple(
                        gaussian_add_i_times(first_zeta[row], second_zeta[row])
                        for row in range(4)
                    )
                    result[at_one, at_i, at_zeta] |= _cartesian_pair_bits(
                        first_bits, second_bits, feature_count
                    )
            return tuple(result.items())

        def union_half(keys):
            result = defaultdict(int)
            for key in keys:
                for state, pair_bits in half_map(key):
                    result[state] |= pair_bits
            return result

        relation = [0] * (feature_count * feature_count)
        for (eta, tail), (even_keys, odd_keys) in geometry[core].items():
            even_states = union_half(even_keys)
            odd_states = union_half(odd_keys)
            odd_by_one = defaultdict(list)
            for (odd_one, odd_i, odd_zeta), pair_bits in odd_states.items():
                odd_by_one[odd_one].append((odd_i, odd_zeta, pair_bits))

            for (even_one, even_i, even_zeta), even_pair_bits in even_states.items():
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
                        hole_even_zeta, hole_odd_zeta = primitive_eight_holes(
                            eta, tail, h0, h1, h8, h9, h12
                        )
                        completed_even_zeta = tuple(
                            gaussian_add(even_zeta[row], hole_even_zeta[row])
                            for row in range(4)
                        )
                        for first_target in first_targets:
                            required_odd = tuple(
                                first_target[row]
                                - even_one[row]
                                - holes_at_one[row]
                                for row in range(4)
                            )
                            for odd_i, odd_zeta, odd_pair_bits in odd_by_one.get(
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
                                completed_odd_zeta = tuple(
                                    gaussian_add(
                                        odd_zeta[row], hole_odd_zeta[row]
                                    )
                                    for row in range(4)
                                )
                                if (
                                    rational_norm(
                                        completed_even_zeta,
                                        completed_odd_zeta,
                                    )
                                    != 334
                                ):
                                    continue
                                if (
                                    sqrt2_coefficient(
                                        completed_even_zeta,
                                        completed_odd_zeta,
                                    )
                                    != 0
                                ):
                                    continue
                                for even_pair in _iter_set_bits(even_pair_bits):
                                    relation[even_pair] |= odd_pair_bits

        inventory_survivors = [0] * 4
        class_survivors = [0] * 4
        for multiset, multiplicity in feature_classes.items():
            survives = False
            for assignment in set(permutations(multiset)):
                left = assignment[0] * feature_count + assignment[2]
                right = assignment[1] * feature_count + assignment[3]
                if (relation[left] >> right) & 1:
                    survives = True
                    break
            if survives:
                index = profile_index[class_profile[multiset]]
                inventory_survivors[index] += multiplicity
                class_survivors[index] += 1

        survivor_row = (core, *inventory_survivors)
        class_row = (core, *class_survivors)
        relation_hash = sha256(
            b"".join(
                value.to_bytes(
                    (feature_count * feature_count + 7) // 8,
                    "little",
                )
                for value in relation
            )
        ).hexdigest()
        retained_survivors = {
            4: EXPECTED_CORE4_SURVIVORS,
            27: EXPECTED_CORE27_SURVIVORS,
        }
        retained_relations = {
            4: EXPECTED_CORE4_RELATION_SHA256,
            27: EXPECTED_CORE27_RELATION_SHA256,
        }
        if core in retained_survivors:
            if survivor_row != retained_survivors[core]:
                raise AssertionError(
                    f"the retained core-{core} root-8 census changed"
                )
            if relation_hash != retained_relations[core]:
                raise AssertionError(
                    f"the retained core-{core} relation changed"
                )
        if core == 4 and class_row != EXPECTED_CORE4_CLASS_SURVIVORS:
            raise AssertionError("the retained core-4 class census changed")
        survivor_rows.append(survivor_row)
        class_rows.append(class_row)
        relation_hashes.append(
            (
                core,
                relation_hash,
            )
        )
        group_map.cache_clear()
        half_map.cache_clear()

    survivors = tuple(survivor_rows)
    class_survivors = tuple(class_rows)
    weighted_rejection = sum(
        ROOT_PROFILE_COUNTS[index] - row[index + 1]
        for row in survivors
        for index in range(4)
    )
    rejected_cells = sum(
        value == 0 for row in survivors for value in row[1:]
    )
    survivor_hash = records_sha256(survivors)
    class_survivor_hash = records_sha256(class_survivors)
    retained_selected_hashes = {
        (4,): (
            EXPECTED_CORE4_SURVIVOR_SHA256,
            EXPECTED_CORE4_CLASS_SURVIVOR_SHA256,
        ),
        (27,): (
            EXPECTED_CORE27_SURVIVOR_SHA256,
            EXPECTED_CORE27_CLASS_SURVIVOR_SHA256,
        ),
    }
    if cores in retained_selected_hashes:
        expected_survivor, expected_class = retained_selected_hashes[cores]
        if survivor_hash != expected_survivor:
            raise AssertionError("the retained selected-core survivor hash changed")
        if class_survivor_hash != expected_class:
            raise AssertionError("the retained selected-core class hash changed")
    return {
        "inventories": sum(feature_classes.values()),
        "feature_classes": len(feature_classes),
        "cores": cores,
        "survivors": survivors,
        "class_survivors": class_survivors,
        "weighted_rejection": weighted_rejection,
        "rejected_profile_core_cells": rejected_cells,
        "survivor_sha256": survivor_hash,
        "class_survivor_sha256": class_survivor_hash,
        "relation_hashes": tuple(relation_hashes),
    }


def parse_cores(text: str) -> tuple[int, ...]:
    if text == "all":
        return tuple(range(1, 32))
    result = tuple(int(item) for item in text.split(",") if item)
    if not result:
        raise argparse.ArgumentTypeError("at least one core is required")
    if any(core < 1 or core > 31 for core in result):
        raise argparse.ArgumentTypeError("cores must lie in 1,...,31")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cores",
        type=parse_cores,
        default=tuple(range(1, 32)),
        help="comma-separated structural cores, or 'all' (default)",
    )
    args = parser.parse_args()
    result = verify(args.cores)
    print(
        "PASS: vertical-pair Phi_1/Phi_2/Phi_4/Phi_8 join classifies "
        f"{result['inventories']} inventories in "
        f"{result['feature_classes']} refined feature classes"
    )
    for row in result["survivors"]:
        print("survivors=" + ",".join(map(str, row)))
    for row in result["class_survivors"]:
        print("class_survivors=" + ",".join(map(str, row)))
    print(
        "weighted_rejection="
        f"{result['weighted_rejection']} "
        "rejected_profile_core_cells="
        f"{result['rejected_profile_core_cells']}"
    )
    print(f"survivor_sha256={result['survivor_sha256']}")
    print(f"class_survivor_sha256={result['class_survivor_sha256']}")
    for core, digest in result["relation_hashes"]:
        print(f"relation_sha256[{core}]={digest}")


if __name__ == "__main__":
    main()
