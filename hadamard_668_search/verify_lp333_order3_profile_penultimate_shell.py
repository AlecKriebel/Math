#!/usr/bin/env python3
"""Exclude the (n_9,n_3,n_0)=(5,3,16) LP(333) profile shell.

The existing opposite-class condition first localizes all three norm-three
letters in one quartet.  Once those three letters are fixed, the remaining
five norm-nine letters are multiples of three, so their mutual correlation
terms vanish modulo nine.  The six reversal-independent nonzero
correlations are therefore affine functions of the five high letters.

This verifier enumerates the localized medium frames modulo the exact
profile symmetry, joins exact aggregate and affine modulo-nine signatures
by meet in the middle, and replays every surviving full assignment through
an independent 37-lag integer Eisenstein correlation implementation.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from typing import Iterable, Sequence

from verify_lp333_order3_char37_transfer import (
    CLASS_OF,
    CLASSES,
    PROFILES,
    profile_norm,
    row_sum_targets,
    signed_profile_integer,
)
from verify_lp333_order3_profile9 import profile_correlation_table
from verify_lp333_order3_profile_zero_symmetry import (
    verify_symbolic_correlation_covariance,
)


Eisenstein = tuple[int, int]
Identifiers = tuple[int, ...]
Assignment = tuple[Identifiers, Identifiers]
Target = tuple[int, int, int, int]
FrameTarget = tuple[Assignment, Target]
Quartet = tuple[int, int, int, int]

P = 37
CLASS_COUNT = 12
ZERO_VALUES: tuple[Eisenstein, Eisenstein] = ((-1, 0), (2, 0))

ZERO_ID = 5
MEDIUM_IDS: tuple[int, ...] = (1, 2, 4, 6, 7, 8)
HIGH_IDS: tuple[int, ...] = (0, 3, 9)

EXPECTED_CERTIFICATE_SHA256 = (
    "51c25095c92ba49c4c7c493373bb68f7d9c0c4671d65490413ae140c2b0aad69"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def e_add(*values: Eisenstein) -> Eisenstein:
    return (
        sum(value[0] for value in values),
        sum(value[1] for value in values),
    )


def e_subtract(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] - right[0], left[1] - right[1]


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_conjugate(value: Eisenstein) -> Eisenstein:
    return value[0] - value[1], -value[1]


def e_norm(value: Eisenstein) -> int:
    return value[0] * value[0] - value[0] * value[1] + value[1] * value[1]


def raw_profile_value(profile_id: int) -> Eisenstein:
    first, second, third = PROFILES[profile_id]
    return first - third, second - third


def coefficient(
    channel: int,
    class_index: int,
    profile_id: int,
) -> Eisenstein:
    """Reconstruct a signed profile coefficient without the imported helper."""

    epsilon = 1 if class_index % 2 == 0 else -1
    factor = -epsilon if channel == 0 else epsilon
    value = raw_profile_value(profile_id)
    return factor * value[0], factor * value[1]


def pair_signature(left_id: int, right_id: int) -> Eisenstein:
    """Return conjugate(z(left))+z(right) modulo three."""

    value = e_add(
        e_conjugate(raw_profile_value(left_id)),
        raw_profile_value(right_id),
    )
    return value[0] % 3, value[1] % 3


def aggregate(assignment: Assignment) -> Target:
    result: list[int] = []
    for channel, identifiers in enumerate(assignment):
        value = (0, 0)
        for class_index, profile_id in enumerate(identifiers):
            value = e_add(
                value,
                coefficient(channel, class_index, profile_id),
            )
        result.extend(value)
    return tuple(result)  # type: ignore[return-value]


def norm_counts(assignment: Assignment) -> tuple[int, int, int]:
    counts = Counter(
        profile_norm(profile_id)
        for identifiers in assignment
        for profile_id in identifiers
    )
    return counts[9], counts[3], counts[0]


def direct_physical_correlations(
    assignment: Assignment,
) -> tuple[Eisenstein, ...]:
    """Compute all 37 exact correlations independently in physical space."""

    words: list[tuple[Eisenstein, ...]] = []
    for channel, identifiers in enumerate(assignment):
        if len(identifiers) != CLASS_COUNT:
            raise ValueError("each profile channel must have twelve letters")
        word = [ZERO_VALUES[channel]]
        for column in range(1, P):
            class_index = CLASS_OF[column]
            word.append(
                coefficient(
                    channel,
                    class_index,
                    identifiers[class_index],
                )
            )
        words.append(tuple(word))

    physical = []
    for lag in range(P):
        value = (0, 0)
        for word in words:
            for column in range(P):
                value = e_add(
                    value,
                    e_multiply(
                        word[(column + lag) % P],
                        e_conjugate(word[column]),
                    ),
                )
        if lag == 0:
            value = value[0] - 167, value[1]
        physical.append(value)
    return tuple(physical)


def invariant_table(
    physical: Sequence[Eisenstein],
) -> tuple[Eisenstein, ...]:
    if len(physical) != P:
        raise ValueError("a physical table must have 37 entries")
    table = [tuple(physical[0])]
    for part in CLASSES:
        representative = tuple(physical[part[0]])
        if any(tuple(physical[column]) != representative for column in part):
            raise AssertionError("a profile correlation lost H-invariance")
        table.append(representative)
    for class_index in range(6):
        if table[1 + class_index + 6] != e_conjugate(
            table[1 + class_index]
        ):
            raise AssertionError("correlation reversal ceased to be conjugation")
    return tuple(table)


def direct_table(assignment: Assignment) -> tuple[Eisenstein, ...]:
    return invariant_table(direct_physical_correlations(assignment))


def quartet_histogram() -> Counter[tuple[int, int]]:
    """Census legal quartets by (number of medium, number of high letters)."""

    result: Counter[tuple[int, int]] = Counter()
    for quartet in product(range(len(PROFILES)), repeat=4):
        if pair_signature(quartet[0], quartet[1]) != pair_signature(
            quartet[2], quartet[3]
        ):
            continue
        result[
            (
                sum(profile_norm(value) == 3 for value in quartet),
                sum(profile_norm(value) == 9 for value in quartet),
            )
        ] += 1
    return result


def medium_frame_target_pairs() -> set[FrameTarget]:
    """Enumerate the three-medium projection and compatible row-sum targets."""

    targets = row_sum_targets()
    result: set[FrameTarget] = set()
    for pair_index in range(6):
        for quartet in product(MEDIUM_IDS + (ZERO_ID,), repeat=4):
            if sum(value in MEDIUM_IDS for value in quartet) != 3:
                continue
            if pair_signature(quartet[0], quartet[1]) != pair_signature(
                quartet[2], quartet[3]
            ):
                continue
            identifiers_a = [ZERO_ID] * CLASS_COUNT
            identifiers_b = [ZERO_ID] * CLASS_COUNT
            identifiers_a[pair_index] = quartet[0]
            identifiers_a[pair_index + 6] = quartet[1]
            identifiers_b[pair_index] = quartet[2]
            identifiers_b[pair_index + 6] = quartet[3]
            assignment = tuple(identifiers_a), tuple(identifiers_b)
            medium_aggregate = aggregate(assignment)
            for target in targets:
                if all(
                    (target[index] - medium_aggregate[index]) % 3 == 0
                    for index in range(4)
                ):
                    result.add((assignment, target))
    return result


CONJUGATE_PROFILE_IDS: tuple[int, ...] = tuple(
    PROFILES.index((profile[0], profile[2], profile[1]))
    for profile in PROFILES
)


def transform_assignment(
    assignment: Assignment,
    rotation: int,
    star_a: bool,
    star_b: bool,
) -> Assignment:
    """Apply the exact C6 x C2_A x C2_B profile action."""

    result = []
    for identifiers, use_star in (
        (assignment[0], star_a),
        (assignment[1], star_b),
    ):
        offset = (2 * (rotation % 6) + (6 if use_star else 0)) % 12
        word = tuple(
            identifiers[(class_index + offset) % 12]
            for class_index in range(12)
        )
        if use_star:
            word = tuple(CONJUGATE_PROFILE_IDS[value] for value in word)
        result.append(word)
    return result[0], result[1]


def conjugate_target_pair(value: Sequence[int]) -> Eisenstein:
    return int(value[0]) - int(value[1]), -int(value[1])


def transform_target(
    target: Target,
    star_a: bool,
    star_b: bool,
) -> Target:
    left: Eisenstein = target[0], target[1]
    right: Eisenstein = target[2], target[3]
    if star_a:
        left = conjugate_target_pair(left)
    if star_b:
        right = conjugate_target_pair(right)
    return (*left, *right)


def images(frame_target: FrameTarget) -> set[FrameTarget]:
    assignment, target = frame_target
    return {
        (
            transform_assignment(
                assignment,
                rotation,
                star_a,
                star_b,
            ),
            transform_target(target, star_a, star_b),
        )
        for rotation in range(6)
        for star_a in (False, True)
        for star_b in (False, True)
    }


def frame_target_orbits(
    frame_targets: Iterable[FrameTarget],
) -> tuple[tuple[FrameTarget, set[FrameTarget]], ...]:
    universe = set(frame_targets)
    unseen = set(universe)
    result = []
    while unseen:
        representative = min(unseen)
        orbit = images(representative)
        if not orbit <= universe:
            raise AssertionError("medium frame/target pairs are not symmetry closed")
        unseen.difference_update(orbit)
        result.append((representative, orbit))
    return tuple(sorted(result, key=lambda row: row[0]))


def decode_assignment(
    medium_frame: Assignment,
    slots: Sequence[tuple[int, int]],
    code: int,
) -> Assignment:
    identifiers = [list(medium_frame[0]), list(medium_frame[1])]
    for slot_index, (channel, class_index) in enumerate(slots):
        state = code >> (2 * slot_index) & 3
        if state:
            identifiers[channel][class_index] = HIGH_IDS[state - 1]
    return tuple(identifiers[0]), tuple(identifiers[1])


def case_signatures(
    frame_target: FrameTarget,
) -> tuple[int, tuple[Assignment, ...]]:
    """Join exact aggregate and affine modulo-nine signatures for one frame."""

    medium_frame, target = frame_target
    baseline = direct_table(medium_frame)
    medium_aggregate = aggregate(medium_frame)
    quotient_target = tuple(
        (target[index] - medium_aggregate[index]) // 3
        for index in range(4)
    )
    if any(
        target[index] - medium_aggregate[index]
        != 3 * quotient_target[index]
        for index in range(4)
    ):
        raise AssertionError("a medium frame has an inexact aggregate quotient")
    if any(
        value[coordinate] % 3
        for value in baseline[1:]
        for coordinate in (0, 1)
    ):
        raise AssertionError("a legal medium frame failed correlation mod three")
    wanted_correlation = tuple(
        (-baseline[1 + class_index][coordinate] // 3) % 3
        for class_index in range(6)
        for coordinate in (0, 1)
    )

    slots: list[tuple[int, int]] = []
    options: list[
        tuple[tuple[Target, tuple[int, ...]], ...]
    ] = []
    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            if medium_frame[channel][class_index] != ZERO_ID:
                continue
            slots.append((channel, class_index))
            rows = []
            for high_id in HIGH_IDS:
                identifiers = [
                    list(medium_frame[0]),
                    list(medium_frame[1]),
                ]
                identifiers[channel][class_index] = high_id
                one_high = tuple(identifiers[0]), tuple(identifiers[1])
                table = direct_table(one_high)
                correlation = []
                for part_index in range(1, 7):
                    delta = e_subtract(table[part_index], baseline[part_index])
                    if delta[0] % 3 or delta[1] % 3:
                        raise AssertionError(
                            "a high-letter affine increment is not divisible by 3"
                        )
                    correlation.extend(
                        ((delta[0] // 3) % 3, (delta[1] // 3) % 3)
                    )
                value = coefficient(channel, class_index, high_id)
                if value[0] % 3 or value[1] % 3:
                    raise AssertionError("a high coefficient is not divisible by 3")
                aggregate_increment = [0, 0, 0, 0]
                aggregate_increment[2 * channel] = value[0] // 3
                aggregate_increment[2 * channel + 1] = value[1] // 3
                rows.append(
                    (
                        tuple(aggregate_increment),
                        tuple(correlation),
                    )
                )
            options.append(tuple(rows))
    if len(slots) != 21:
        raise AssertionError("a three-medium frame must leave 21 high/zero slots")

    split = 10
    left_signatures: dict[
        tuple[int, Target, tuple[int, ...]], list[int]
    ] = defaultdict(list)
    left_aggregates: Counter[tuple[int, Target]] = Counter()

    def enumerate_left(
        index: int,
        high_count: int,
        aggregate_value: Target,
        correlation_value: tuple[int, ...],
        code: int,
    ) -> None:
        if index == split:
            left_signatures[
                (high_count, aggregate_value, correlation_value)
            ].append(code)
            left_aggregates[(high_count, aggregate_value)] += 1
            return
        enumerate_left(
            index + 1,
            high_count,
            aggregate_value,
            correlation_value,
            code,
        )
        if high_count == 5:
            return
        for state, (aggregate_increment, correlation_increment) in enumerate(
            options[index],
            start=1,
        ):
            enumerate_left(
                index + 1,
                high_count + 1,
                tuple(
                    aggregate_value[coordinate]
                    + aggregate_increment[coordinate]
                    for coordinate in range(4)
                ),  # type: ignore[arg-type]
                tuple(
                    (
                        correlation_value[coordinate]
                        + correlation_increment[coordinate]
                    )
                    % 3
                    for coordinate in range(12)
                ),
                code | state << (2 * index),
            )

    enumerate_left(0, 0, (0, 0, 0, 0), (0,) * 12, 0)

    aggregate_count = 0
    survivors: list[Assignment] = []

    def enumerate_right(
        index: int,
        high_count: int,
        aggregate_value: Target,
        correlation_value: tuple[int, ...],
        code: int,
    ) -> None:
        nonlocal aggregate_count
        if index == len(options):
            left_count = 5 - high_count
            if not 0 <= left_count <= 5:
                return
            aggregate_complement: Target = tuple(
                quotient_target[coordinate] - aggregate_value[coordinate]
                for coordinate in range(4)
            )  # type: ignore[assignment]
            aggregate_count += left_aggregates.get(
                (left_count, aggregate_complement),
                0,
            )
            correlation_complement = tuple(
                (
                    wanted_correlation[coordinate]
                    - correlation_value[coordinate]
                )
                % 3
                for coordinate in range(12)
            )
            for left_code in left_signatures.get(
                (
                    left_count,
                    aggregate_complement,
                    correlation_complement,
                ),
                (),
            ):
                survivors.append(
                    decode_assignment(
                        medium_frame,
                        slots,
                        left_code | code,
                    )
                )
            return
        enumerate_right(
            index + 1,
            high_count,
            aggregate_value,
            correlation_value,
            code,
        )
        if high_count == 5:
            return
        for state, (aggregate_increment, correlation_increment) in enumerate(
            options[index],
            start=1,
        ):
            enumerate_right(
                index + 1,
                high_count + 1,
                tuple(
                    aggregate_value[coordinate]
                    + aggregate_increment[coordinate]
                    for coordinate in range(4)
                ),  # type: ignore[arg-type]
                tuple(
                    (
                        correlation_value[coordinate]
                        + correlation_increment[coordinate]
                    )
                    % 3
                    for coordinate in range(12)
                ),
                code | state << (2 * index),
            )

    enumerate_right(split, 0, (0, 0, 0, 0), (0,) * 12, 0)
    if len(survivors) != len(set(survivors)):
        raise AssertionError("the additive join emitted a duplicate assignment")
    return aggregate_count, tuple(sorted(survivors))


def medium_projection(assignment: Assignment) -> Assignment:
    return tuple(
        tuple(
            profile_id if profile_norm(profile_id) == 3 else ZERO_ID
            for profile_id in identifiers
        )
        for identifiers in assignment
    )  # type: ignore[return-value]


def verify_penultimate_shell() -> dict[str, object]:
    """Replay the complete shell exclusion and return exact censuses."""

    if tuple(
        profile_id
        for profile_id in range(len(PROFILES))
        if profile_norm(profile_id) == 0
    ) != (ZERO_ID,):
        raise AssertionError("the norm-zero profile alphabet changed")
    if tuple(
        profile_id
        for profile_id in range(len(PROFILES))
        if profile_norm(profile_id) == 3
    ) != MEDIUM_IDS:
        raise AssertionError("the norm-three profile alphabet changed")
    if tuple(
        profile_id
        for profile_id in range(len(PROFILES))
        if profile_norm(profile_id) == 9
    ) != HIGH_IDS:
        raise AssertionError("the norm-nine profile alphabet changed")

    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            for profile_id in range(len(PROFILES)):
                if coefficient(
                    channel,
                    class_index,
                    profile_id,
                ) != signed_profile_integer(
                    channel,
                    class_index,
                    profile_id,
                ):
                    raise AssertionError(
                        "the independent coefficient reconstruction disagrees"
                    )

    # This is the universal algebraic reason for affine correlation modulo 9:
    # every product of two possible high coefficients vanishes modulo 9.
    high_coefficients = tuple(
        coefficient(channel, class_index, profile_id)
        for channel in range(2)
        for class_index in range(CLASS_COUNT)
        for profile_id in HIGH_IDS
    )
    for left in high_coefficients:
        for right in high_coefficients:
            value = e_multiply(left, e_conjugate(right))
            if value[0] % 9 or value[1] % 9:
                raise AssertionError("a high-high product survived modulo nine")
    for profile_id in (ZERO_ID, *HIGH_IDS):
        value = raw_profile_value(profile_id)
        if value[0] % 3 or value[1] % 3:
            raise AssertionError(
                "an endpoint letter can change a pair signature modulo three"
            )

    covariance = verify_symbolic_correlation_covariance()
    if covariance != {
        "lag_representatives": 13,
        "universal_monomial_checks": 2_200_368,
    }:
        raise AssertionError("the universal profile symmetry audit changed")

    local_histogram = quartet_histogram()
    expected_local_histogram = Counter(
        {
            (0, 0): 1,
            (0, 1): 12,
            (0, 2): 54,
            (0, 3): 108,
            (0, 4): 81,
            (2, 0): 108,
            (2, 1): 648,
            (2, 2): 972,
            (3, 0): 216,
            (3, 1): 648,
            (4, 0): 486,
        }
    )
    if local_histogram != expected_local_histogram:
        raise AssertionError("the universal local quartet census changed")
    if any(medium_count == 1 for medium_count, _ in local_histogram):
        raise AssertionError("a legal quartet gained exactly one medium letter")

    frame_targets = medium_frame_target_pairs()
    frames = {assignment for assignment, _ in frame_targets}
    if len(frames) != 1_296 or len(frame_targets) != 1_944:
        raise AssertionError("the medium frame/target census changed")
    frame_target_counts = Counter(target for _, target in frame_targets)
    expected_frame_target_counts = Counter(
        {
            (-3, -3, -4, -2): 324,
            (-3, -3, -2, 2): 324,
            (0, 3, -4, -2): 324,
            (0, 3, -2, 2): 324,
            (4, -1, 0, 0): 324,
            (5, 1, 0, 0): 324,
        }
    )
    if frame_target_counts != expected_frame_target_counts:
        raise AssertionError("the compatible medium-frame targets changed")

    orbits = frame_target_orbits(frame_targets)
    orbit_sizes = Counter(len(orbit) for _, orbit in orbits)
    if len(orbits) != 90 or orbit_sizes != Counter({24: 72, 12: 18}):
        raise AssertionError("the medium frame/target quotient changed")

    pre_mod9_by_target: Counter[Target] = Counter()
    representative_survivors: list[tuple[Assignment, Target]] = []
    representative_case_records = []
    for representative, orbit in orbits:
        aggregate_count, survivors = case_signatures(representative)
        for _, target in orbit:
            pre_mod9_by_target[target] += aggregate_count
        for assignment in survivors:
            representative_survivors.append(
                (assignment, representative[1])
            )
        representative_case_records.append(
            (
                representative,
                len(orbit),
                aggregate_count,
                survivors,
            )
        )

    expected_pre_mod9_by_target = Counter(
        {
            (-3, -3, -4, -2): 5_748_834,
            (-3, -3, -2, 2): 5_748_834,
            (0, 3, -4, -2): 5_748_834,
            (0, 3, -2, 2): 5_748_834,
            (4, -1, 0, 0): 5_819_400,
            (5, 1, 0, 0): 5_819_400,
        }
    )
    if pre_mod9_by_target != expected_pre_mod9_by_target:
        raise AssertionError("the pre-modulo-nine shell census changed")
    if sum(pre_mod9_by_target.values()) != 34_634_136:
        raise AssertionError("the pre-modulo-nine shell total changed")
    if len(representative_survivors) != 30:
        raise AssertionError("the representative modulo-nine census changed")

    # Expand all representative completion sets, not just one completion from
    # each orbit.  This handles size-twelve frame orbits without assuming that
    # their stabilizers fix individual high-letter completions.
    expanded: set[tuple[Assignment, Target]] = set()
    for assignment, target in representative_survivors:
        for rotation in range(6):
            for star_a in (False, True):
                for star_b in (False, True):
                    transformed = transform_assignment(
                        assignment,
                        rotation,
                        star_a,
                        star_b,
                    )
                    transformed_target = transform_target(
                        target,
                        star_a,
                        star_b,
                    )
                    if (
                        medium_projection(transformed),
                        transformed_target,
                    ) not in frame_targets:
                        raise AssertionError(
                            "a full completion left its medium-frame orbit"
                        )
                    expanded.add((transformed, transformed_target))
    if len(expanded) != 552:
        raise AssertionError("the full modulo-nine survivor census changed")
    post_mod9_by_target = Counter(target for _, target in expanded)
    expected_post_mod9_by_target = Counter(
        {
            (-3, -3, -4, -2): 42,
            (-3, -3, -2, 2): 42,
            (0, 3, -4, -2): 42,
            (0, 3, -2, 2): 42,
            (4, -1, 0, 0): 192,
            (5, 1, 0, 0): 192,
        }
    )
    if post_mod9_by_target != expected_post_mod9_by_target:
        raise AssertionError("the post-modulo-nine target census changed")

    bad_histogram: Counter[int] = Counter()
    exact_records = []
    for assignment, target in sorted(expanded):
        if norm_counts(assignment) != (5, 3, 16):
            raise AssertionError("a survivor left the selected norm shell")
        if aggregate(assignment) != target:
            raise AssertionError("a survivor has the wrong exact aggregate")
        for pair_index in range(6):
            if pair_signature(
                assignment[0][pair_index],
                assignment[0][pair_index + 6],
            ) != pair_signature(
                assignment[1][pair_index],
                assignment[1][pair_index + 6],
            ):
                raise AssertionError("a survivor failed a local quartet equation")

        physical = direct_physical_correlations(assignment)
        table = invariant_table(physical)
        if table != profile_correlation_table(*assignment):
            raise AssertionError(
                "the detached 37-lag replay disagrees with the profile table"
            )
        if table[0] != (0, 0):
            raise AssertionError("a shell survivor has the wrong origin energy")
        if any(
            value[coordinate] % 9
            for value in table[1:]
            for coordinate in (0, 1)
        ):
            raise AssertionError("an affine-sieve survivor failed modulo nine")
        bad_count = sum(value != (0, 0) for value in table[1:])
        bad_histogram[bad_count] += 1
        exact_records.append((assignment, target, physical, table))

    expected_bad_histogram = Counter({6: 24, 10: 144, 12: 384})
    if bad_histogram != expected_bad_histogram:
        raise AssertionError("the exact shell failure histogram changed")
    if bad_histogram.get(0):
        raise AssertionError("the penultimate shell gained an exact profile")

    certificate = (
        tuple(sorted(local_histogram.items())),
        tuple(sorted(frame_target_counts.items())),
        tuple((row[0], row[1], row[2], row[3]) for row in representative_case_records),
        tuple(sorted(pre_mod9_by_target.items())),
        tuple(sorted(post_mod9_by_target.items())),
        tuple(sorted(bad_histogram.items())),
        tuple(exact_records),
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_CERTIFICATE_SHA256
    ):
        raise AssertionError("the penultimate-shell certificate hash changed")

    return {
        "norm_shell": (5, 3, 16),
        "legal_quartet_weight_histogram": tuple(
            sorted(local_histogram.items())
        ),
        "medium_frame_count": len(frames),
        "medium_frame_target_count": len(frame_targets),
        "medium_frame_target_counts": tuple(
            sorted(frame_target_counts.items())
        ),
        "medium_frame_target_orbit_count": len(orbits),
        "medium_frame_target_orbit_sizes": tuple(
            sorted(orbit_sizes.items())
        ),
        "universal_symmetry_monomial_checks": covariance[
            "universal_monomial_checks"
        ],
        "pre_mod9_count": sum(pre_mod9_by_target.values()),
        "pre_mod9_target_counts": tuple(
            sorted(pre_mod9_by_target.items())
        ),
        "representative_mod9_survivor_count": len(
            representative_survivors
        ),
        "post_mod9_count": len(expanded),
        "post_mod9_target_counts": tuple(
            sorted(post_mod9_by_target.items())
        ),
        "physical_lags_replayed": P * len(expanded),
        "bad_class_histogram": tuple(sorted(bad_histogram.items())),
        "exact_profile_count": 0,
        "shell_excluded": True,
        "constructor_cut": "n_9 <= 4",
        "certificate_sha256": certificate_hash,
    }


def main() -> None:
    result = verify_penultimate_shell()
    print(json.dumps(result, indent=2))
    print(
        "PASS: the (n_9,n_3,n_0)=(5,3,16) profile shell is excluded exactly"
    )
    print("CONSTRUCTOR CUT: n_9 <= 4")
    print("STATUS: this is not an LP(333) or a Hadamard matrix")


if __name__ == "__main__":
    main()
