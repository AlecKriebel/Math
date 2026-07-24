#!/usr/bin/env python3
"""Exclude the norm-nine endpoint of the LP(333) order-three profile shell.

The 24 normalized profile letters have Eisenstein norms 0, 3, or 9 and
total norm 54.  This verifier treats the endpoint with six norm-nine
letters and eighteen zero letters.

Every nonzero-column coefficient in this endpoint is divisible by 3.
Consequently, at a nonzero lag, all correlation terms away from the fixed
zero column are divisible by 9.  The two terms incident with the zero
column therefore give a local modulo-nine condition on one opposite-class
quartet.  This reduces each quartet from 4^4=256 states to 40.

An exact six-layer dynamic program then applies the complete row-sum target
catalog and the six-letter energy condition.  It leaves 288 assignments,
forming twelve full profile-symmetry orbits.  Exact integer Eisenstein
correlation excludes every orbit.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
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
from verify_lp333_order3_profile_zero_symmetry import transform_assignment


Eisenstein = tuple[int, int]
Identifiers = tuple[int, ...]
Assignment = tuple[Identifiers, Identifiers]
Target = tuple[int, int, int, int]
Quartet = tuple[int, int, int, int]

P = 37
CLASS_COUNT = 12
ZERO_VALUES: tuple[Eisenstein, Eisenstein] = ((-1, 0), (2, 0))

EXPECTED_ENDPOINT_CERTIFICATE_SHA256 = (
    "addf4ad655ca1ca16eaef5aebf8787eb14e8a56676e73e05f68e905fc9f45b5a"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def e_add(*values: Eisenstein) -> Eisenstein:
    return (
        sum(value[0] for value in values),
        sum(value[1] for value in values),
    )


def e_scale(scalar: int, value: Eisenstein) -> Eisenstein:
    return scalar * value[0], scalar * value[1]


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_conjugate(value: Eisenstein) -> Eisenstein:
    return value[0] - value[1], -value[1]


def endpoint_ids() -> tuple[int, ...]:
    """Return the one norm-zero and three norm-nine profile letters."""

    identifiers = tuple(
        index for index in range(len(PROFILES)) if profile_norm(index) in (0, 9)
    )
    if identifiers != (0, 3, 5, 9):
        raise AssertionError("the endpoint profile alphabet changed")
    norms = Counter(profile_norm(index) for index in identifiers)
    if norms != Counter({9: 3, 0: 1}):
        raise AssertionError("the endpoint norm multiplicities changed")
    return identifiers


def incident_zero_column_term(
    class_index: int,
    quartet: Quartet,
) -> Eisenstein:
    """Return the two-channel terms incident with the fixed zero column."""

    a_forward = signed_profile_integer(0, class_index, quartet[0])
    a_reverse = signed_profile_integer(
        0, class_index + 6, quartet[1]
    )
    b_forward = signed_profile_integer(1, class_index, quartet[2])
    b_reverse = signed_profile_integer(
        1, class_index + 6, quartet[3]
    )
    return e_add(
        e_scale(-1, a_forward),
        e_scale(-1, e_conjugate(a_reverse)),
        e_scale(2, b_forward),
        e_scale(2, e_conjugate(b_reverse)),
    )


def divisible_by_nine(value: Eisenstein) -> bool:
    return value[0] % 9 == 0 and value[1] % 9 == 0


def quartet_aggregate(
    class_index: int,
    quartet: Quartet,
) -> Target:
    result: list[int] = []
    for channel, forward, reverse in (
        (0, quartet[0], quartet[1]),
        (1, quartet[2], quartet[3]),
    ):
        left = signed_profile_integer(channel, class_index, forward)
        right = signed_profile_integer(channel, class_index + 6, reverse)
        total = e_add(left, right)
        result.extend(total)
    return tuple(result)  # type: ignore[return-value]


def high_count(quartet: Quartet) -> int:
    return sum(profile_norm(identifier) == 9 for identifier in quartet)


def local_quartets(
    class_index: int,
) -> tuple[tuple[Quartet, Target, int, Eisenstein], ...]:
    """Enumerate the exact local modulo-nine endpoint alphabet."""

    if not 0 <= class_index < 6:
        raise ValueError("an opposite-class pair is indexed by 0,...,5")
    alphabet = endpoint_ids()
    result = []
    for a_forward in alphabet:
        for a_reverse in alphabet:
            for b_forward in alphabet:
                for b_reverse in alphabet:
                    quartet = (
                        a_forward,
                        a_reverse,
                        b_forward,
                        b_reverse,
                    )
                    incident = incident_zero_column_term(
                        class_index, quartet
                    )
                    if divisible_by_nine(incident):
                        result.append(
                            (
                                quartet,
                                quartet_aggregate(class_index, quartet),
                                high_count(quartet),
                                incident,
                            )
                        )
    return tuple(result)


def reconstruct_assignment(
    path: Sequence[Quartet],
) -> Assignment:
    if len(path) != 6:
        raise ValueError("an endpoint path must contain six quartets")
    identifiers_a = [5] * CLASS_COUNT
    identifiers_b = [5] * CLASS_COUNT
    for class_index, quartet in enumerate(path):
        identifiers_a[class_index] = quartet[0]
        identifiers_a[class_index + 6] = quartet[1]
        identifiers_b[class_index] = quartet[2]
        identifiers_b[class_index + 6] = quartet[3]
    return tuple(identifiers_a), tuple(identifiers_b)


def enumerate_endpoint_candidates() -> dict[Target, tuple[Assignment, ...]]:
    """Apply the local cut, energy, and all 22 aggregate targets exactly."""

    target_set = set(row_sum_targets())
    prefixes: dict[
        tuple[int, int, int, int, int], list[tuple[Quartet, ...]]
    ] = {(0, 0, 0, 0, 0): [()]}
    for class_index in range(6):
        next_prefixes: dict[
            tuple[int, int, int, int, int], list[tuple[Quartet, ...]]
        ] = defaultdict(list)
        for key, paths in prefixes.items():
            for quartet, aggregate, count, _ in local_quartets(class_index):
                next_count = key[4] + count
                if next_count > 6:
                    continue
                next_key = (
                    key[0] + aggregate[0],
                    key[1] + aggregate[1],
                    key[2] + aggregate[2],
                    key[3] + aggregate[3],
                    next_count,
                )
                next_prefixes[next_key].extend(
                    path + (quartet,) for path in paths
                )
        prefixes = next_prefixes

    result: dict[Target, tuple[Assignment, ...]] = {}
    for target in sorted(target_set):
        paths = prefixes.get((*target, 6), ())
        assignments = tuple(
            sorted(reconstruct_assignment(path) for path in paths)
        )
        if assignments:
            result[target] = assignments
    return result


def assignment_target(assignment: Assignment) -> Target:
    result = []
    for channel, identifiers in enumerate(assignment):
        total = (0, 0)
        for class_index, identifier in enumerate(identifiers):
            total = e_add(
                total,
                signed_profile_integer(
                    channel, class_index, identifier
                ),
            )
        result.extend(total)
    return tuple(result)  # type: ignore[return-value]


def direct_physical_table(assignment: Assignment) -> tuple[Eisenstein, ...]:
    """Independently reconstruct all 37 exact physical correlations."""

    words: list[tuple[Eisenstein, ...]] = []
    for channel, identifiers in enumerate(assignment):
        word = [ZERO_VALUES[channel]]
        for column in range(1, P):
            word.append(
                signed_profile_integer(
                    channel,
                    CLASS_OF[column],
                    identifiers[CLASS_OF[column]],
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

    table = [physical[0]]
    for part in CLASSES:
        representative = physical[part[0]]
        if any(physical[column] != representative for column in part):
            raise AssertionError("the endpoint correlation lost H-invariance")
        table.append(representative)
    return tuple(table)


def symmetry_orbits(
    assignments: Iterable[Assignment],
) -> tuple[tuple[Assignment, ...], ...]:
    unseen = set(assignments)
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {
            transform_assignment(
                *representative,
                rotation=rotation,
                star_a=star_a,
                star_b=star_b,
            )
            for rotation in range(6)
            for star_a in (False, True)
            for star_b in (False, True)
        }
        if not orbit <= unseen | {
            member for prior in orbits for member in prior
        }:
            raise AssertionError("endpoint candidates are not symmetry closed")
        current = tuple(sorted(orbit & unseen))
        if not current:
            raise AssertionError("an endpoint orbit was empty")
        unseen.difference_update(current)
        orbits.append(current)
    return tuple(sorted(orbits, key=lambda orbit: orbit[0]))


def verify_endpoint_shell() -> dict[str, object]:
    """Replay the complete endpoint exclusion and return its census."""

    alphabet = endpoint_ids()
    # Every nonzero endpoint coefficient is a multiple of three.  Thus every
    # product away from the fixed zero column is a multiple of nine.
    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            for identifier in alphabet:
                value = signed_profile_integer(
                    channel, class_index, identifier
                )
                if value[0] % 3 or value[1] % 3:
                    raise AssertionError(
                        "an endpoint coefficient is not divisible by three"
                    )

    local_tables = tuple(local_quartets(index) for index in range(6))
    if tuple(len(table) for table in local_tables) != (40,) * 6:
        raise AssertionError("the local modulo-nine census changed")
    local_high_histograms = tuple(
        tuple(sorted(Counter(row[2] for row in table).items()))
        for table in local_tables
    )
    expected_local_histogram = ((0, 1), (2, 12), (4, 27))
    if local_high_histograms != (expected_local_histogram,) * 6:
        raise AssertionError("the local endpoint weight pattern changed")

    candidates_by_target = enumerate_endpoint_candidates()
    target_counts = tuple(
        (target, len(assignments))
        for target, assignments in candidates_by_target.items()
    )
    expected_target_counts = (
        ((-3, 0, -3, -3), 72),
        ((-3, 0, 0, 3), 72),
        ((3, 0, 0, -3), 72),
        ((3, 0, 3, 3), 72),
    )
    if target_counts != expected_target_counts:
        raise AssertionError("the endpoint aggregate census changed")

    assignments = tuple(
        assignment
        for values in candidates_by_target.values()
        for assignment in values
    )
    if len(assignments) != 288 or len(set(assignments)) != 288:
        raise AssertionError("the endpoint candidate total changed")

    for target, values in candidates_by_target.items():
        for assignment in values:
            if assignment_target(assignment) != target:
                raise AssertionError("an endpoint assignment has wrong target")
            if (
                sum(
                    profile_norm(identifier)
                    for channel in assignment
                    for identifier in channel
                )
                != 54
            ):
                raise AssertionError("an endpoint assignment has wrong energy")
            if (
                sum(
                    profile_norm(identifier) == 9
                    for channel in assignment
                    for identifier in channel
                )
                != 6
            ):
                raise AssertionError("an endpoint assignment has wrong support")

    orbits = symmetry_orbits(assignments)
    if len(orbits) != 12 or tuple(map(len, orbits)) != (24,) * 12:
        raise AssertionError("the endpoint symmetry quotient changed")

    bad_histogram: Counter[int] = Counter()
    representative_bad_counts = []
    exact_tables = []
    for assignment in assignments:
        table = direct_physical_table(assignment)
        if table != profile_correlation_table(*assignment):
            raise AssertionError(
                "the independent endpoint correlations disagree"
            )
        if table[0] != (0, 0):
            raise AssertionError("the endpoint origin equation changed")
        if any(
            value[0] % 9 or value[1] % 9 for value in table[1:]
        ):
            raise AssertionError("a local modulo-nine cut failed globally")
        bad_count = sum(value != (0, 0) for value in table[1:])
        bad_histogram[bad_count] += 1
        exact_tables.append(table)
    if bad_histogram != Counter({12: 264, 10: 24}):
        raise AssertionError("the endpoint exact-correlation census changed")
    if bad_histogram.get(0):
        raise AssertionError("the endpoint shell gained an exact profile")

    for orbit in orbits:
        counts = {
            sum(
                value != (0, 0)
                for value in direct_physical_table(member)[1:]
            )
            for member in orbit
        }
        if len(counts) != 1:
            raise AssertionError("bad-class count changed inside an orbit")
        representative_bad_counts.append(next(iter(counts)))
    if Counter(representative_bad_counts) != Counter({12: 11, 10: 1}):
        raise AssertionError("the orbit-level endpoint failures changed")

    certificate = (
        tuple((index, len(table)) for index, table in enumerate(local_tables)),
        local_high_histograms,
        target_counts,
        assignments,
        tuple(orbit[0] for orbit in orbits),
        tuple(sorted(bad_histogram.items())),
        tuple(representative_bad_counts),
        tuple(exact_tables),
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_ENDPOINT_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_ENDPOINT_CERTIFICATE_SHA256
    ):
        raise AssertionError("the endpoint certificate hash changed")

    return {
        "endpoint_profile_ids": alphabet,
        "raw_quartets_per_opposite_pair": len(alphabet) ** 4,
        "local_quartets_per_opposite_pair": tuple(
            len(table) for table in local_tables
        ),
        "local_high_count_histogram": expected_local_histogram,
        "row_sum_target_count": len(row_sum_targets()),
        "surviving_target_counts": target_counts,
        "candidate_count": len(assignments),
        "symmetry_orbit_count": len(orbits),
        "symmetry_orbit_sizes": tuple(map(len, orbits)),
        "bad_class_histogram": tuple(sorted(bad_histogram.items())),
        "representative_bad_class_histogram": tuple(
            sorted(Counter(representative_bad_counts).items())
        ),
        "exact_profile_count": 0,
        "endpoint_excluded": True,
        "certificate_sha256": certificate_hash,
    }


def main() -> None:
    result = verify_endpoint_shell()
    print(json.dumps(result, indent=2))
    print(
        "PASS: the six-norm-nine endpoint profile shell is excluded exactly"
    )
    print("STATUS: this is not an LP(333) or a Hadamard matrix")


if __name__ == "__main__":
    main()
