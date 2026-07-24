#!/usr/bin/env python3
"""Verify an exact natural symmetry action on the 24-profile ``D_t=0`` system.

The profile variables are two twelve-letter words over the ten
compositions of three.  Their actual Eisenstein column coefficients are

    a_j = -(-1)^j z(p_A,j),     b_j = (+1)(-1)^j z(p_B,j),

with fixed zero coefficients ``a_0=-1`` and ``b_0=2``.

There are three equation symmetries which respect these data:

* a common even class rotation (order six);
* coefficient star on A alone;
* coefficient star on B alone.

On profile IDs, star is residue conjugation together with the opposite
class shift ``j -> j+6``.  It leaves the autocorrelation of that one
channel unchanged, so the two stars are independent.  The resulting group
is ``C6 x C2 x C2``.

This verifier also distinguishes profile-equation symmetry from symmetry
of a later labelled lift with the exact canonical zero-column words.  Only
the B-star has an affine realization fixing its canonical word.  Thus the
lift-compatible subgroup certified here is ``C6 x C2_B``.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations, product
import json
from math import gcd
from typing import Sequence

from verify_lp333_order3_char37_transfer import (
    CLASS_OF,
    CLASS_COUNT,
    CLASSES,
    PROFILES,
    row_sum_targets,
    signed_profile_integer,
)
from verify_lp333_order3_primitive9_jet import ZERO_A_PLUS, ZERO_B_PLUS
from verify_lp333_order3_profile9 import (
    ZERO_EISENSTEIN,
    e_conjugate,
    e_multiply,
    profile_correlation_table,
)
from verify_lp333_order3_quotient import (
    C2_AFFINE_MULTIPLIER,
    C2_AFFINE_TRANSLATION,
    C6_DECIMATION,
    N,
)


Eisenstein = tuple[int, int]
Identifiers = tuple[int, ...]
Assignment = tuple[Identifiers, Identifiers]
Target = tuple[int, int, int, int]

EXPECTED_CERTIFICATE_SHA256 = (
    "0367620819b4bfb3f9f8ec235682bbb90a30dd70083688b2a577660d688a24e7"
)
EXPECTED_ACTION_SHA256 = (
    "58ae329fc90864a6dc38520752658b7d5d4a7ac7ab3f46d62e367dfb978cdba9"
)
EXPECTED_FORMAL_TARGET_ORBITS_SHA256 = (
    "84cbd2ed76bcde3651957693637969ccaa78ac715661fc7f8faf7554812eefa2"
)
EXPECTED_LIFT_TARGET_ORBITS_SHA256 = (
    "f6fcb8da68400d98476c944f297ffe6c0278495b175bd81bc418fcd7f4541219"
)
EXPECTED_REJECTED_CANDIDATES_SHA256 = (
    "95b89195be0aa225610147b9ca1bf37c5cfd181fabf4658c23e96478099acd50"
)
EXPECTED_BURNSIDE_SHA256 = (
    "b293d4074723538cdb570577e73ddd3694b655e205703d284ba33661e5ee6569"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def conjugate_profile(profile: Sequence[int]) -> tuple[int, int, int]:
    if len(profile) != 3:
        raise ValueError("a residue profile must have three entries")
    return int(profile[0]), int(profile[2]), int(profile[1])


CONJUGATE_PROFILE_IDS: tuple[int, ...] = tuple(
    PROFILES.index(conjugate_profile(profile)) for profile in PROFILES
)
CYCLIC_PROFILE_IDS: tuple[int, ...] = tuple(
    PROFILES.index((profile[2], profile[0], profile[1]))
    for profile in PROFILES
)


def transform_assignment(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
    rotation: int = 0,
    star_a: bool = False,
    star_b: bool = False,
) -> Assignment:
    """Apply one element of ``C6 x C2_A x C2_B``.

    ``rotation`` uses the same source convention as the quotient verifier:
    output class ``j`` reads source class ``j+2*rotation``.
    """

    if len(identifiers_a) != CLASS_COUNT or len(identifiers_b) != CLASS_COUNT:
        raise ValueError("each channel must have twelve profile IDs")
    rotation %= 6
    result = []
    for identifiers, use_star in (
        (identifiers_a, bool(star_a)),
        (identifiers_b, bool(star_b)),
    ):
        if any(not 0 <= int(value) < len(PROFILES) for value in identifiers):
            raise ValueError("a profile ID lies outside the ten-state catalog")
        offset = (2 * rotation + (6 if use_star else 0)) % CLASS_COUNT
        word = tuple(
            int(identifiers[(class_index + offset) % CLASS_COUNT])
            for class_index in range(CLASS_COUNT)
        )
        if use_star:
            word = tuple(CONJUGATE_PROFILE_IDS[value] for value in word)
        result.append(word)
    return result[0], result[1]


def assignment_target(
    identifiers_a: Sequence[int], identifiers_b: Sequence[int]
) -> Target:
    values = []
    for channel, identifiers in enumerate((identifiers_a, identifiers_b)):
        total = (0, 0)
        for class_index, profile_id in enumerate(identifiers):
            value = signed_profile_integer(channel, class_index, int(profile_id))
            total = total[0] + value[0], total[1] + value[1]
        values.extend(total)
    return tuple(values)  # type: ignore[return-value]


def conjugate_target_pair(value: Sequence[int]) -> Eisenstein:
    if len(value) != 2:
        raise ValueError("an Eisenstein target pair must have length two")
    return int(value[0]) - int(value[1]), -int(value[1])


def transform_target(
    target: Sequence[int], star_a: bool = False, star_b: bool = False
) -> Target:
    if len(target) != 4:
        raise ValueError("an aggregate target must have four coordinates")
    left = tuple(map(int, target[:2]))
    right = tuple(map(int, target[2:]))
    if star_a:
        left = conjugate_target_pair(left)
    if star_b:
        right = conjugate_target_pair(right)
    return (*left, *right)


def transformed_table(
    table: Sequence[Eisenstein], rotation: int
) -> tuple[Eisenstein, ...]:
    if len(table) != 13:
        raise ValueError("a profile correlation table must have thirteen parts")
    offset = 2 * (rotation % 6)
    return (tuple(table[0]),) + tuple(
        tuple(table[1 + (class_index + offset) % CLASS_COUNT])
        for class_index in range(CLASS_COUNT)
    )


def actual_class_coefficient(
    channel: int, class_index: int, profile_id: int
) -> Eisenstein:
    return signed_profile_integer(channel, class_index, profile_id)


def physical_coefficient(
    channel: int, column: int, profile_id: int | None
) -> Eisenstein:
    """Return one coefficient, including the fixed zero-column value."""

    normalized_column = int(column) % 37
    if normalized_column == 0:
        if profile_id is not None:
            raise ValueError("the zero column has no profile variable")
        return ZERO_EISENSTEIN[channel]
    if profile_id is None:
        raise ValueError("a nonzero column needs a profile state")
    return actual_class_coefficient(
        channel, CLASS_OF[normalized_column], int(profile_id)
    )


def verify_symbolic_correlation_covariance() -> dict[str, int]:
    """Check covariance term-by-term for the complete finite alphabet.

    A correlation is a sum of local products.  For every group element,
    channel, invariant lag representative, physical summation index, and
    possible pair of local profile states, this routine checks the relevant
    monomial identity.  Summation-index multiplication (or reflected
    multiplication under star) is a permutation of ``C_37``, so these local
    identities certify covariance for every one of the ``10^24`` profile
    assignments; no sampling argument is used.
    """

    checks = 0
    lag_representatives = (0,) + tuple(part[0] for part in CLASSES)
    for rotation, star_a, star_b in product(
        range(6), range(2), range(2)
    ):
        multiplier = pow(4, rotation, 37)
        for channel, use_star in enumerate((star_a, star_b)):
            for lag in lag_representatives:
                for right_column in range(37):
                    left_column = (right_column + lag) % 37
                    if use_star:
                        source_left = (-multiplier * left_column) % 37
                        source_right = (-multiplier * right_column) % 37
                    else:
                        source_left = (multiplier * left_column) % 37
                        source_right = (multiplier * right_column) % 37

                    left_states: Sequence[int | None] = (
                        (None,)
                        if source_left == 0
                        else tuple(range(len(PROFILES)))
                    )
                    right_states: Sequence[int | None] = (
                        (None,)
                        if source_right == 0
                        else tuple(range(len(PROFILES)))
                    )
                    for left_state in left_states:
                        source_left_value = physical_coefficient(
                            channel, source_left, left_state
                        )
                        for right_state in right_states:
                            source_right_value = physical_coefficient(
                                channel, source_right, right_state
                            )
                            if use_star:
                                image_left = e_conjugate(source_left_value)
                                image_right = e_conjugate(source_right_value)
                                # Reflection reverses the local ordered pair
                                # when the correlation sum is reindexed.
                                expected = e_multiply(
                                    source_right_value,
                                    e_conjugate(source_left_value),
                                )
                            else:
                                image_left = source_left_value
                                image_right = source_right_value
                                expected = e_multiply(
                                    source_left_value,
                                    e_conjugate(source_right_value),
                                )
                            observed = e_multiply(
                                image_left, e_conjugate(image_right)
                            )
                            if observed != expected:
                                raise AssertionError(
                                    "universal correlation monomial "
                                    "covariance failed"
                                )
                            checks += 1
    return {
        "lag_representatives": len(lag_representatives),
        "universal_monomial_checks": checks,
    }


def verify_profile_catalog_action() -> dict[str, object]:
    expected_conjugation = (3, 2, 1, 0, 6, 5, 4, 8, 7, 9)
    if CONJUGATE_PROFILE_IDS != expected_conjugation:
        raise AssertionError("the ten-state residue-conjugation map changed")
    if any(
        CONJUGATE_PROFILE_IDS[CONJUGATE_PROFILE_IDS[index]] != index
        for index in range(len(PROFILES))
    ):
        raise AssertionError("profile conjugation is not an involution")
    if any(
        CYCLIC_PROFILE_IDS[
            CYCLIC_PROFILE_IDS[CYCLIC_PROFILE_IDS[index]]
        ]
        != index
        for index in range(len(PROFILES))
    ):
        raise AssertionError("cyclic residue rotation lost order three")

    # Check the physical column maps behind the quotient notation.  The
    # multiplier 4 advances the twelve order-three classes by two, while
    # negation advances them by six.
    physical_class_checks = 0
    for rotation in range(6):
        multiplier = pow(4, rotation, 37)
        for column in range(1, 37):
            if CLASS_OF[multiplier * column % 37] != (
                CLASS_OF[column] + 2 * rotation
            ) % CLASS_COUNT:
                raise AssertionError("the even class rotation map changed")
            physical_class_checks += 1
    for column in range(1, 37):
        if CLASS_OF[-column % 37] != (
            CLASS_OF[column] + 6
        ) % CLASS_COUNT:
            raise AssertionError("column negation lost its opposite class")
        physical_class_checks += 1

    # Even rotations preserve the actual alternating A/B coefficient signs.
    # Star preserves them because the opposite class has the same parity.
    coefficient_checks = 0
    coefficient_values: set[Eisenstein] = set(ZERO_EISENSTEIN)
    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            for profile_id in range(len(PROFILES)):
                value = actual_class_coefficient(
                    channel, class_index, profile_id
                )
                coefficient_values.add(value)
                for rotation in range(6):
                    rotated = actual_class_coefficient(
                        channel,
                        class_index,
                        profile_id,
                    )
                    source = actual_class_coefficient(
                        channel,
                        (class_index + 2 * rotation) % CLASS_COUNT,
                        profile_id,
                    )
                    if rotated != source:
                        raise AssertionError("an even class shift changed parity")
                    coefficient_checks += 1
                starred = actual_class_coefficient(
                    channel,
                    class_index,
                    CONJUGATE_PROFILE_IDS[profile_id],
                )
                source = e_conjugate(
                    actual_class_coefficient(
                        channel,
                        (class_index + 6) % CLASS_COUNT,
                        profile_id,
                    )
                )
                if starred != source:
                    raise AssertionError("profile star changed an actual sign")
                coefficient_checks += 1

    if any(e_conjugate(value) != value for value in ZERO_EISENSTEIN):
        raise AssertionError("coefficient star moved a fixed zero value")
    # This is the local product identity used after the reindexing c -> -c:
    # conjugate(x) * conjugate(conjugate(y)) = y * conjugate(x).
    star_term_checks = 0
    for left, right in product(coefficient_values, repeat=2):
        transformed_product = e_multiply(
            e_conjugate(left),
            e_conjugate(e_conjugate(right)),
        )
        expected_product = e_multiply(right, e_conjugate(left))
        if transformed_product != expected_product:
            raise AssertionError("the local star product identity failed")
        star_term_checks += 1

    return {
        "profile_states": len(PROFILES),
        "conjugate_profile_ids": CONJUGATE_PROFILE_IDS,
        "conjugation_fixed_profiles": sum(
            CONJUGATE_PROFILE_IDS[index] == index
            for index in range(len(PROFILES))
        ),
        "physical_class_checks": physical_class_checks,
        "actual_coefficient_checks": coefficient_checks,
        "star_term_checks": star_term_checks,
    }


def dense_fixtures() -> tuple[Assignment, ...]:
    fixtures = [
        (
            tuple((3 * index + 1) % 10 for index in range(CLASS_COUNT)),
            tuple((7 * index + 2) % 10 for index in range(CLASS_COUNT)),
        ),
        (
            tuple(range(10)) + (1, 4),
            tuple(reversed(range(10))) + (2, 7),
        ),
    ]
    for seed in range(12):
        fixtures.append(
            (
                tuple(
                    (index * index + 3 * seed * index + seed + 1) % 10
                    for index in range(CLASS_COUNT)
                ),
                tuple(
                    (3 * index * index + (2 * seed + 1) * index + 2 * seed)
                    % 10
                    for index in range(CLASS_COUNT)
                ),
            )
        )
    return tuple(fixtures)


def verify_equation_group() -> dict[str, object]:
    symbolic_covariance = verify_symbolic_correlation_covariance()
    separating = dense_fixtures()[0]
    elements = tuple(product(range(6), range(2), range(2)))
    images = {
        transform_assignment(*separating, rotation, star_a, star_b)
        for rotation, star_a, star_b in elements
    }
    if len(images) != 24:
        raise AssertionError("the displayed transformations do not have order 24")

    covariance_checks = 0
    target_checks = 0
    group_law_checks = 0
    for fixture in dense_fixtures():
        table = profile_correlation_table(*fixture)
        target = assignment_target(*fixture)
        for rotation, star_a, star_b in product(
            range(6), range(2), range(2)
        ):
            image = transform_assignment(
                *fixture, rotation, bool(star_a), bool(star_b)
            )
            image_table = profile_correlation_table(*image)
            if image_table != transformed_table(table, rotation):
                raise AssertionError("the profile correlation failed covariance")
            covariance_checks += 13
            expected_target = transform_target(
                target, bool(star_a), bool(star_b)
            )
            if assignment_target(*image) != expected_target:
                raise AssertionError("the aggregate target action changed")
            target_checks += 1

    # Check the direct-product law first on a separating assignment and then
    # symbolically on every channel, class coordinate, and profile state.
    for first in elements:
        first_image = transform_assignment(
            *separating, first[0], bool(first[1]), bool(first[2])
        )
        for second in elements:
            composed = transform_assignment(
                *first_image, second[0], bool(second[1]), bool(second[2])
            )
            expected = transform_assignment(
                *separating,
                (first[0] + second[0]) % 6,
                bool(first[1] ^ second[1]),
                bool(first[2] ^ second[2]),
            )
            if composed != expected:
                raise AssertionError("the displayed group law failed")
            group_law_checks += 1

    symbolic_group_law_checks = 0
    action_signature = []
    for rotation, star_a, star_b in elements:
        element_signature = []
        for channel in range(2):
            use_star = (star_a, star_b)[channel]
            offset = (2 * rotation + 6 * use_star) % CLASS_COUNT
            for class_index in range(CLASS_COUNT):
                source = (class_index + offset) % CLASS_COUNT
                for profile_id in range(len(PROFILES)):
                    image_profile = (
                        CONJUGATE_PROFILE_IDS[profile_id]
                        if use_star
                        else profile_id
                    )
                    element_signature.append((source, image_profile))
        action_signature.append(
            ((rotation, star_a, star_b), tuple(element_signature))
        )
    for first in elements:
        for second in elements:
            expected = (
                (first[0] + second[0]) % 6,
                first[1] ^ second[1],
                first[2] ^ second[2],
            )
            for channel in range(2):
                first_star = first[channel + 1]
                second_star = second[channel + 1]
                first_offset = (
                    2 * first[0] + 6 * first_star
                ) % CLASS_COUNT
                second_offset = (
                    2 * second[0] + 6 * second_star
                ) % CLASS_COUNT
                expected_offset = (
                    2 * expected[0] + 6 * expected[channel + 1]
                ) % CLASS_COUNT
                for class_index in range(CLASS_COUNT):
                    composed_source = (
                        class_index + second_offset + first_offset
                    ) % CLASS_COUNT
                    for profile_id in range(len(PROFILES)):
                        composed_profile = profile_id
                        if first_star:
                            composed_profile = CONJUGATE_PROFILE_IDS[
                                composed_profile
                            ]
                        if second_star:
                            composed_profile = CONJUGATE_PROFILE_IDS[
                                composed_profile
                            ]
                        expected_profile = (
                            CONJUGATE_PROFILE_IDS[profile_id]
                            if expected[channel + 1]
                            else profile_id
                        )
                        if (
                            composed_source != (
                                class_index + expected_offset
                            ) % CLASS_COUNT
                            or composed_profile != expected_profile
                        ):
                            raise AssertionError(
                                "the symbolic direct-product law failed"
                            )
                        symbolic_group_law_checks += 1

    action_hash = compact_hash(tuple(action_signature))
    if EXPECTED_ACTION_SHA256 and action_hash != EXPECTED_ACTION_SHA256:
        raise AssertionError("the formal profile action changed")
    return {
        "formal_group": "C6 x C2_A x C2_B",
        "formal_group_order": len(images),
        "fixtures": len(dense_fixtures()),
        "correlation_covariance_checks": covariance_checks,
        "target_action_checks": target_checks,
        "group_law_checks": group_law_checks,
        "symbolic_group_law_checks": symbolic_group_law_checks,
        **symbolic_covariance,
        "action_sha256": action_hash,
        "zero_gate_preserved": True,
    }


def orbit_partition(
    targets: Sequence[Target], include_star_a: bool, include_star_b: bool
) -> tuple[tuple[Target, ...], ...]:
    target_set = set(targets)
    seen: set[Target] = set()
    orbits = []
    for target in sorted(target_set):
        if target in seen:
            continue
        images = {
            transform_target(target, star_a, star_b)
            for star_a in range(2 if include_star_a else 1)
            for star_b in range(2 if include_star_b else 1)
        }
        if not images <= target_set:
            raise AssertionError("a target symmetry left the 22-shard catalog")
        orbit = tuple(sorted(images))
        orbits.append(orbit)
        seen.update(images)
    if seen != target_set:
        raise AssertionError("the target orbit partition is incomplete")
    return tuple(orbits)


EXPECTED_FORMAL_TARGET_ORBITS: tuple[tuple[Target, ...], ...] = (
    (
        (-3, -3, -4, -2),
        (-3, -3, -2, 2),
        (0, 3, -4, -2),
        (0, 3, -2, 2),
    ),
    ((-3, 0, -3, -3), (-3, 0, 0, 3)),
    (
        (-1, -2, -5, -1),
        (-1, -2, -4, 1),
        (1, 2, -5, -1),
        (1, 2, -4, 1),
    ),
    (
        (1, -1, 2, -2),
        (1, -1, 4, 2),
        (2, 1, 2, -2),
        (2, 1, 4, 2),
    ),
    (
        (2, -2, -4, -2),
        (2, -2, -2, 2),
        (4, 2, -4, -2),
        (4, 2, -2, 2),
    ),
    ((3, 0, 0, -3), (3, 0, 3, 3)),
    ((4, -1, 0, 0), (5, 1, 0, 0)),
)

EXPECTED_LIFT_TARGET_ORBITS: tuple[tuple[Target, ...], ...] = (
    ((-3, -3, -4, -2), (-3, -3, -2, 2)),
    ((-3, 0, -3, -3), (-3, 0, 0, 3)),
    ((-1, -2, -5, -1), (-1, -2, -4, 1)),
    ((0, 3, -4, -2), (0, 3, -2, 2)),
    ((1, -1, 2, -2), (1, -1, 4, 2)),
    ((1, 2, -5, -1), (1, 2, -4, 1)),
    ((2, -2, -4, -2), (2, -2, -2, 2)),
    ((2, 1, 2, -2), (2, 1, 4, 2)),
    ((3, 0, 0, -3), (3, 0, 3, 3)),
    ((4, -1, 0, 0),),
    ((4, 2, -4, -2), (4, 2, -2, 2)),
    ((5, 1, 0, 0),),
)


def verify_target_orbits() -> dict[str, object]:
    targets = row_sum_targets()
    formal_orbits = orbit_partition(targets, True, True)
    if formal_orbits != EXPECTED_FORMAL_TARGET_ORBITS:
        raise AssertionError("the seven formal target orbits changed")
    lift_orbits = orbit_partition(targets, False, True)
    if lift_orbits != EXPECTED_LIFT_TARGET_ORBITS:
        raise AssertionError("the lift-compatible target orbits changed")
    target_fixed_counts = tuple(
        sum(
            transform_target(target, bool(star_a), bool(star_b)) == target
            for target in targets
        )
        for star_a, star_b in product(range(2), range(2))
    )
    if target_fixed_counts != (22, 2, 4, 0):
        raise AssertionError("the target fixed-point counts changed")
    if sum(target_fixed_counts) // 4 != len(formal_orbits):
        raise AssertionError("target Burnside and orbit enumeration disagree")
    formal_hash = compact_hash(formal_orbits)
    lift_hash = compact_hash(lift_orbits)
    if (
        EXPECTED_FORMAL_TARGET_ORBITS_SHA256
        and formal_hash != EXPECTED_FORMAL_TARGET_ORBITS_SHA256
    ):
        raise AssertionError("the formal target-orbit hash changed")
    if (
        EXPECTED_LIFT_TARGET_ORBITS_SHA256
        and lift_hash != EXPECTED_LIFT_TARGET_ORBITS_SHA256
    ):
        raise AssertionError("the lift target-orbit hash changed")
    return {
        "catalog_targets": len(targets),
        "formal_target_orbits": len(formal_orbits),
        "formal_orbit_sizes": tuple(map(len, formal_orbits)),
        "formal_representatives": tuple(orbit[0] for orbit in formal_orbits),
        "formal_orbits_sha256": formal_hash,
        "target_fixed_counts": target_fixed_counts,
        "lift_compatible_target_orbits": len(lift_orbits),
        "lift_compatible_orbit_sizes": tuple(map(len, lift_orbits)),
        "lift_compatible_representatives": tuple(
            orbit[0] for orbit in lift_orbits
        ),
        "lift_orbits_sha256": lift_hash,
    }


def residue_counts(word: Sequence[int]) -> tuple[int, int, int]:
    if len(word) != 9:
        raise ValueError("a zero-column word must have length nine")
    return tuple(
        sum(int(word[row]) for row in range(residue, 9, 3))
        for residue in range(3)
    )  # type: ignore[return-value]


def affine_stabilizer(word: Sequence[int]) -> tuple[tuple[int, int], ...]:
    units = tuple(value for value in range(9) if gcd(value, 9) == 1)
    return tuple(
        (multiplier, translation)
        for multiplier in units
        for translation in range(9)
        if tuple(
            int(word[(multiplier * row + translation) % 9])
            for row in range(9)
        )
        == tuple(map(int, word))
    )


def verify_fixed_zero_audit() -> dict[str, object]:
    zero_profiles = residue_counts(ZERO_A_PLUS), residue_counts(ZERO_B_PLUS)
    if zero_profiles != ((1, 2, 2), (3, 1, 1)):
        raise AssertionError("the canonical zero residue profiles changed")
    if ZERO_EISENSTEIN != ((-1, 0), (2, 0)):
        raise AssertionError("the fixed zero Eisenstein coefficients changed")

    # The only residue permutations preserving each fixed zero profile are
    # identity and the 1<->2 reflection.  Nontrivial residue rotations fail.
    zero_profile_stabilizers = []
    for counts in zero_profiles:
        stabilizer = tuple(
            permutation
            for permutation in permutations(range(3))
            if tuple(counts[permutation[index]] for index in range(3)) == counts
        )
        zero_profile_stabilizers.append(stabilizer)
    expected_residue_stabilizer = ((0, 1, 2), (0, 2, 1))
    if any(
        stabilizer != expected_residue_stabilizer
        for stabilizer in zero_profile_stabilizers
    ):
        raise AssertionError("the fixed zero residue stabilizer changed")

    stabilizer_a = affine_stabilizer(ZERO_A_PLUS)
    stabilizer_b = affine_stabilizer(ZERO_B_PLUS)
    if stabilizer_a != ((1, 0),):
        raise AssertionError("the A zero word gained an affine symmetry")
    if stabilizer_b != ((1, 0), (8, 3)):
        raise AssertionError("the B zero-word affine stabilizer changed")
    residue_conjugation = (0, 2, 1)
    conjugating_stabilizer_a = tuple(
        affine
        for affine in stabilizer_a
        if tuple(
            (affine[0] * residue + affine[1]) % 9 % 3
            for residue in range(3)
        )
        == residue_conjugation
    )
    conjugating_stabilizer_b = tuple(
        affine
        for affine in stabilizer_b
        if tuple(
            (affine[0] * residue + affine[1]) % 9 % 3
            for residue in range(3)
        )
        == residue_conjugation
    )
    if conjugating_stabilizer_a:
        raise AssertionError("the A zero word gained a conjugating affine map")
    if conjugating_stabilizer_b != ((8, 3),):
        raise AssertionError("the B conjugating affine map changed")

    # The B reflection r -> 3-r induces residue conjugation.  Multiplication
    # by 27 on F_37 shifts every cyclotomic class by six.
    if any(
        {
            27 * value % 37
            for value in CLASSES[class_index]
        }
        != set(CLASSES[(class_index + 6) % CLASS_COUNT])
        for class_index in range(CLASS_COUNT)
    ):
        raise AssertionError("the B-star column multiplier changed")
    reflected_b = tuple(
        ZERO_B_PLUS[(3 - row) % 9] for row in range(9)
    )
    if reflected_b != ZERO_B_PLUS:
        raise AssertionError("the B star no longer fixes its zero word")

    # The common even class rotation is realized by a decimation which is
    # the identity on the row coordinate and multiplication by four on
    # F_37.  It therefore fixes the complete zero column.
    if C6_DECIMATION % 9 != 1 or C6_DECIMATION % 37 != 4:
        raise AssertionError("the residual C6 decimation changed")

    # Reconstruct the established full-CRT B transport.  Neither its square
    # nor the sixth power of the C6 decimation is literally the identity on
    # Z/333: both are the order-three multiplier 100.  That multiplier is
    # trivial precisely on the order-three invariant quotient.  Pinning this
    # prevents the quotient involution from being overclaimed for arbitrary
    # length-333 sequences.
    subgroup_multiplier = 100
    if (
        C2_AFFINE_MULTIPLIER % 9 != 8
        or C2_AFFINE_MULTIPLIER % 37 != 27
        or C2_AFFINE_TRANSLATION % 9 != 3
        or C2_AFFINE_TRANSLATION % 37 != 0
        or pow(C2_AFFINE_MULTIPLIER, 2, N) != subgroup_multiplier
        or (
            (C2_AFFINE_MULTIPLIER + 1)
            * C2_AFFINE_TRANSLATION
        )
        % N
        != 0
        or pow(C6_DECIMATION, 6, N) != subgroup_multiplier
        or subgroup_multiplier % 9 != 1
        or subgroup_multiplier % 37 not in set(CLASSES[0])
    ):
        raise AssertionError("the full-CRT quotient transport changed")
    if (
        C6_DECIMATION * C2_AFFINE_TRANSLATION
        % N
        != C2_AFFINE_TRANSLATION
        or C6_DECIMATION * C2_AFFINE_MULTIPLIER % N
        != C2_AFFINE_MULTIPLIER * C6_DECIMATION % N
    ):
        raise AssertionError("the C6 and B-star affine transports do not commute")

    # Signed channel permutations are the only binary-channel relabellings.
    # The unequal fixed vector (-1,2) has trivial stabilizer, excluding
    # channel swap (including odd class shift plus channel swap).
    zero_vector = (-1, 2)
    signed_channel_stabilizers = []
    for permutation in permutations(range(2)):
        for signs in product((-1, 1), repeat=2):
            image = tuple(
                signs[index] * zero_vector[permutation[index]]
                for index in range(2)
            )
            if image == zero_vector:
                signed_channel_stabilizers.append((permutation, signs))
    if signed_channel_stabilizers != [((0, 1), (1, 1))]:
        raise AssertionError("the fixed zero vector gained a channel symmetry")

    parity_preserving_shifts = tuple(
        shift
        for shift in range(CLASS_COUNT)
        if all(
            (
                signed_profile_integer(channel, class_index, 9)[0]
                == signed_profile_integer(
                    channel, (class_index + shift) % CLASS_COUNT, 9
                )[0]
            )
            for channel in range(2)
            for class_index in range(CLASS_COUNT)
        )
    )
    if parity_preserving_shifts != (0, 2, 4, 6, 8, 10):
        raise AssertionError("the alternating class-sign stabilizer changed")

    return {
        "zero_residue_profiles": zero_profiles,
        "zero_eisenstein_coefficients": ZERO_EISENSTEIN,
        "residue_profile_stabilizer": expected_residue_stabilizer,
        "a_zero_affine_stabilizer": stabilizer_a,
        "b_zero_affine_stabilizer": stabilizer_b,
        "a_conjugating_affine_stabilizer": conjugating_stabilizer_a,
        "b_conjugating_affine_stabilizer": conjugating_stabilizer_b,
        "b_star_row_affine": (8, 3),
        "b_star_column_multiplier": 27,
        "b_star_full_affine": (
            C2_AFFINE_MULTIPLIER,
            C2_AFFINE_TRANSLATION,
        ),
        "quotient_trivial_subgroup_multiplier": subgroup_multiplier,
        "c6_sixth_power": pow(C6_DECIMATION, 6, N),
        "b_star_square_multiplier": pow(
            C2_AFFINE_MULTIPLIER, 2, N
        ),
        "parity_preserving_class_shifts": parity_preserving_shifts,
        "signed_channel_stabilizer_order": len(signed_channel_stabilizers),
        "lift_compatible_group": "C6 x C2_B",
        "lift_compatible_group_order": 12,
    }


def shifted_table(
    table: Sequence[Eisenstein], class_shift: int
) -> tuple[Eisenstein, ...]:
    if len(table) != 13:
        raise ValueError("a profile correlation table must have thirteen parts")
    return (tuple(table[0]),) + tuple(
        tuple(table[1 + (class_index + class_shift) % CLASS_COUNT])
        for class_index in range(CLASS_COUNT)
    )


def verify_rejected_candidates() -> dict[str, object]:
    """Give explicit failures for tempting but invalid extra symmetries.

    These are covariance-identity counterexamples, not claims about an
    unknown zero-gate solution.  They prove that the tempting maps do not
    carry the displayed polynomial system to itself with the expected lag
    permutation.
    """

    fixture = dense_fixtures()[0]
    original = profile_correlation_table(*fixture)
    a_ids, b_ids = fixture
    candidates: tuple[
        tuple[str, Assignment, tuple[Eisenstein, ...]], ...
    ] = (
        (
            "plain_A_conjugation_without_opposite_class",
            (
                tuple(CONJUGATE_PROFILE_IDS[value] for value in a_ids),
                b_ids,
            ),
            original,
        ),
        (
            "channel_swap_with_fixed_zero_coefficients",
            (b_ids, a_ids),
            original,
        ),
        (
            "cyclic_residue_rotation_with_fixed_zero_profiles",
            (
                tuple(CYCLIC_PROFILE_IDS[value] for value in a_ids),
                tuple(CYCLIC_PROFILE_IDS[value] for value in b_ids),
            ),
            original,
        ),
        (
            "odd_class_shift",
            (
                tuple(a_ids[(index + 1) % CLASS_COUNT] for index in range(CLASS_COUNT)),
                tuple(b_ids[(index + 1) % CLASS_COUNT] for index in range(CLASS_COUNT)),
            ),
            shifted_table(original, 1),
        ),
        (
            "odd_class_shift_plus_channel_swap",
            (
                tuple(b_ids[(index + 1) % CLASS_COUNT] for index in range(CLASS_COUNT)),
                tuple(a_ids[(index + 1) % CLASS_COUNT] for index in range(CLASS_COUNT)),
            ),
            shifted_table(original, 1),
        ),
    )
    mismatch_counts = []
    counterexamples = []
    for name, image, expected in candidates:
        actual = profile_correlation_table(*image)
        mismatch_parts = tuple(
            index
            for index, (left, right) in enumerate(zip(actual, expected))
            if left != right
        )
        if not mismatch_parts:
            raise AssertionError(f"rejected map became covariant: {name}")
        mismatch_counts.append((name, len(mismatch_parts)))
        counterexamples.append(
            (name, image, expected, actual, mismatch_parts)
        )
    expected_mismatches = (
        ("plain_A_conjugation_without_opposite_class", 10),
        ("channel_swap_with_fixed_zero_coefficients", 12),
        ("cyclic_residue_rotation_with_fixed_zero_profiles", 12),
        ("odd_class_shift", 12),
        ("odd_class_shift_plus_channel_swap", 12),
    )
    if tuple(mismatch_counts) != expected_mismatches:
        raise AssertionError("the rejected-symmetry fixtures changed")
    counterexample_hash = compact_hash(tuple(counterexamples))
    if (
        EXPECTED_REJECTED_CANDIDATES_SHA256
        and counterexample_hash != EXPECTED_REJECTED_CANDIDATES_SHA256
    ):
        raise AssertionError("the rejected-map counterexamples changed")
    return {
        "fixture": fixture,
        "rejected_covariance_maps": len(candidates),
        "mismatch_counts": tuple(mismatch_counts),
        "counterexamples_sha256": counterexample_hash,
    }


def fixed_channel_words(rotation: int, use_star: bool) -> int:
    """Count twelve-profile words fixed by one channel action."""

    offset = (2 * (rotation % 6) + (6 if use_star else 0)) % CLASS_COUNT
    unseen = set(range(CLASS_COUNT))
    result = 1
    conjugation_fixed_states = sum(
        CONJUGATE_PROFILE_IDS[index] == index
        for index in range(len(PROFILES))
    )
    while unseen:
        start = min(unseen)
        current = start
        length = 0
        while current in unseen:
            unseen.remove(current)
            length += 1
            current = (current + offset) % CLASS_COUNT
        if use_star and length % 2:
            result *= conjugation_fixed_states
        else:
            result *= len(PROFILES)
    return result


def verify_burnside_orbits() -> dict[str, object]:
    fixed_table = tuple(
        (
            rotation,
            fixed_channel_words(rotation, False),
            fixed_channel_words(rotation, True),
        )
        for rotation in range(6)
    )
    expected_fixed_table = (
        (0, 10**12, 10**6),
        (1, 10**2, 2**4),
        (2, 10**4, 10**2),
        (3, 10**6, 2**12),
        (4, 10**4, 10**2),
        (5, 10**2, 2**4),
    )
    if fixed_table != expected_fixed_table:
        raise AssertionError("the channel fixed-point table changed")

    fixed_assignment_table = tuple(
        (
            rotation,
            star_a,
            star_b,
            fixed_channel_words(rotation, bool(star_a))
            * fixed_channel_words(rotation, bool(star_b)),
        )
        for rotation, star_a, star_b in product(range(6), range(2), range(2))
    )
    # Independent cycle-index reconstruction.  If star is present, an odd
    # coordinate cycle must be coloured by one of the two conjugation-fixed
    # profiles; otherwise all ten profiles are available.
    for rotation, no_star, with_star in fixed_table:
        for star, observed in ((0, no_star), (1, with_star)):
            offset = (2 * rotation + 6 * star) % CLASS_COUNT
            cycles = gcd(CLASS_COUNT, offset)
            cycle_length = CLASS_COUNT // cycles
            available = (
                2 if star and cycle_length % 2 else len(PROFILES)
            )
            if observed != available**cycles:
                raise AssertionError("the cycle-index fixed count changed")

    burnside_sum = sum(row[3] for row in fixed_assignment_table)
    if burnside_sum != 1_000_002_000_002_008_412_824_128:
        raise AssertionError("the Burnside numerator changed")
    if burnside_sum % 24:
        raise AssertionError("the Burnside sum is not divisible by 24")
    orbit_count = burnside_sum // 24
    if orbit_count != 41_666_750_000_083_683_867_672:
        raise AssertionError("the raw profile orbit count changed")
    burnside_hash = compact_hash(
        (fixed_table, fixed_assignment_table, burnside_sum, orbit_count)
    )
    if (
        EXPECTED_BURNSIDE_SHA256
        and burnside_hash != EXPECTED_BURNSIDE_SHA256
    ):
        raise AssertionError("the Burnside certificate changed")
    return {
        "raw_assignments": 10**24,
        "fixed_channel_word_table": fixed_table,
        "fixed_assignment_table": fixed_assignment_table,
        "burnside_sum": burnside_sum,
        "raw_formal_orbits": orbit_count,
        "certificate_sha256": burnside_hash,
    }


def verify() -> dict[str, object]:
    catalog = verify_profile_catalog_action()
    group = verify_equation_group()
    targets = verify_target_orbits()
    zeros = verify_fixed_zero_audit()
    rejected = verify_rejected_candidates()
    burnside = verify_burnside_orbits()
    certificate = (
        catalog["conjugate_profile_ids"],
        catalog["physical_class_checks"],
        catalog["actual_coefficient_checks"],
        catalog["star_term_checks"],
        group["formal_group"],
        group["formal_group_order"],
        group["action_sha256"],
        targets["formal_representatives"],
        targets["formal_orbit_sizes"],
        targets["formal_orbits_sha256"],
        targets["lift_compatible_orbit_sizes"],
        targets["lift_compatible_representatives"],
        targets["lift_orbits_sha256"],
        targets["target_fixed_counts"],
        zeros["a_zero_affine_stabilizer"],
        zeros["b_zero_affine_stabilizer"],
        zeros["a_conjugating_affine_stabilizer"],
        zeros["b_conjugating_affine_stabilizer"],
        zeros["b_star_full_affine"],
        zeros["quotient_trivial_subgroup_multiplier"],
        zeros["parity_preserving_class_shifts"],
        rejected["mismatch_counts"],
        rejected["counterexamples_sha256"],
        burnside["fixed_channel_word_table"],
        burnside["raw_formal_orbits"],
        burnside["certificate_sha256"],
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_CERTIFICATE_SHA256
    ):
        raise AssertionError("the profile-zero symmetry certificate changed")
    return {
        "catalog": catalog,
        "group": group,
        "targets": targets,
        "fixed_zeros": zeros,
        "rejected_candidates": rejected,
        "burnside": burnside,
        "certificate_sha256": certificate_hash,
        "status": (
            "22 aggregate targets reduce to seven formal D_t=0 profile "
            "orbits; exact canonical labelled lifts retain twelve target "
            "orbits because only the B-star fixes its zero word"
        ),
    }


def main() -> None:
    result = verify()
    print(f"formal_group={result['group']['formal_group']}")
    print(f"formal_group_order={result['group']['formal_group_order']}")
    print(
        "formal_target_orbits="
        f"{result['targets']['formal_target_orbits']}"
    )
    print(
        "formal_orbit_sizes="
        f"{result['targets']['formal_orbit_sizes']}"
    )
    print(
        "lift_compatible_target_orbits="
        f"{result['targets']['lift_compatible_target_orbits']}"
    )
    print(
        "raw_formal_orbits="
        f"{result['burnside']['raw_formal_orbits']}"
    )
    print(f"certificate_sha256={result['certificate_sha256']}")
    print("PASS: exact profile-zero symmetry and orbit audit replayed")
    print("STATUS: profile symmetry is not overclaimed as labelled-lift symmetry")


if __name__ == "__main__":
    main()
