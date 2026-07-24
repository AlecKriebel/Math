#!/usr/bin/env python3
"""Profile-level Eisenstein obstruction from exact primitive-nine equality.

If the exact row correlations at a fixed column lag are periodic modulo
three, their order-three Fourier value determines the three common values.
That Fourier value depends only on the 24 residue profiles, not on any
within-residue placement.

Writing lambda=1-omega in Z[omega], exact periodicity and the fixed total
correlation 1503 force every nonzero-column profile correlation into the
ideal

    3 lambda Z[omega],       Norm(3 lambda)=27.

Conversely, ideal membership reconstructs the unique candidate correlation
triple with sum 501.  It remains only a necessary profile condition because
the reconstructed counts still have to be realized by labelled words.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from typing import Sequence

from verify_lp333_order3_char37_transfer import (
    CLASS_OF,
    CLASSES,
    PAIRED_LAYER_WITNESSES,
    PROFILES,
)
from verify_lp333_order3_integral9 import invariant_correlation_table
from verify_lp333_order3_labeled_jet import (
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
    P,
    ROWS,
    ZERO_A_PLUS,
    ZERO_B_PLUS,
)
from verify_lp333_order3_trit_lift import (
    PINNED_PROFILES,
    TRIT_SURVIVOR_MASKS_A,
    TRIT_SURVIVOR_MASKS_B,
)


Eisenstein = tuple[int, int]  # a+b*omega, omega^2+omega+1=0.
Profile = tuple[int, int, int]

EXPECTED_PAIRED_PROFILE_TABLES_SHA256 = (
    "ee30efce6b0b64af57a54c15f94bc446444bd2a972e36713c271d7259d1c7b62"
)
EXPECTED_PINNED_PROFILE_TABLE_SHA256 = (
    "acc2d3f660270800b74096bd35945621763b6d6fa18b8d6a0d9feef982242ef2"
)
EXPECTED_PINNED_TARGETS_SHA256 = (
    "75e7464c751de1dcc2405157d8769641c0b7407e9357a3546ab9c0df36392383"
)

PARTS = ((0,),) + CLASSES


def e_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] + right[0], left[1] + right[1]


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_conjugate(value: Eisenstein) -> Eisenstein:
    return value[0] - value[1], -value[1]


def e_norm(value: Eisenstein) -> int:
    return value[0] * value[0] - value[0] * value[1] + value[1] * value[1]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def residue_counts(word: Sequence[int]) -> Profile:
    if len(word) != ROWS:
        raise ValueError("a row word must have length nine")
    return tuple(
        sum(int(word[row]) for row in range(residue, ROWS, 3))
        for residue in range(3)
    )  # type: ignore[return-value]


def residue_eisenstein(counts: Sequence[int]) -> Eisenstein:
    if len(counts) != 3:
        raise ValueError("residue counts must have length three")
    return int(counts[0]) - int(counts[2]), int(counts[1]) - int(counts[2])


ZERO_EISENSTEIN = (
    residue_eisenstein(residue_counts(ZERO_A_PLUS)),
    residue_eisenstein(residue_counts(ZERO_B_PLUS)),
)


def actual_profile_counts(
    channel: int, class_index: int, profile: Profile
) -> Profile:
    high_weight = (
        class_index % 2 == 0 if channel == 0 else class_index % 2 == 1
    )
    return (
        tuple(3 - value for value in profile)
        if high_weight
        else profile
    )  # type: ignore[return-value]


def profile_ids(
    profiles: Sequence[Sequence[Profile]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if len(profiles) != 2 or any(len(channel) != 12 for channel in profiles):
        raise ValueError("profiles must have shape 2 by 12")
    return tuple(
        tuple(PROFILES.index(tuple(profile)) for profile in channel)
        for channel in profiles
    )  # type: ignore[return-value]


PINNED_PROFILE_IDS = profile_ids(PINNED_PROFILES)


def profile_column_values(
    channel: int, identifiers: Sequence[int]
) -> tuple[Eisenstein, ...]:
    if channel not in (0, 1) or len(identifiers) != 12:
        raise ValueError("expected one channel and twelve profile IDs")
    result = [ZERO_EISENSTEIN[channel]]
    for column in range(1, P):
        class_index = CLASS_OF[column]
        profile_id = int(identifiers[class_index])
        if not 0 <= profile_id < len(PROFILES):
            raise ValueError("profile ID outside the ten-state catalog")
        counts = actual_profile_counts(
            channel, class_index, PROFILES[profile_id]
        )
        result.append(residue_eisenstein(counts))
    return tuple(result)


def profile_correlation_table(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> tuple[Eisenstein, ...]:
    """Return the order-three Fourier correlation on 13 invariant parts."""

    values = (
        profile_column_values(0, identifiers_a),
        profile_column_values(1, identifiers_b),
    )
    physical = []
    for column_lag in range(P):
        coefficient = (0, 0)
        for channel in values:
            for column in range(P):
                coefficient = e_add(
                    coefficient,
                    e_multiply(
                        channel[(column + column_lag) % P],
                        e_conjugate(channel[column]),
                    ),
                )
        if column_lag == 0:
            coefficient = coefficient[0] - 167, coefficient[1]
        physical.append(coefficient)
    result = []
    for part in PARTS:
        representative = physical[part[0]]
        if any(physical[column] != representative for column in part):
            raise AssertionError("the profile correlation lost class invariance")
        result.append(representative)
    return tuple(result)


def weight_correlation_totals() -> tuple[int, ...]:
    """Return the placement-independent total over all nine row lags."""

    weights = [[5], [5]]
    for channel in range(2):
        for column in range(1, P):
            class_index = CLASS_OF[column]
            high_weight = (
                class_index % 2 == 0
                if channel == 0
                else class_index % 2 == 1
            )
            weights[channel].append(6 if high_weight else 3)
    return tuple(
        sum(
            weights[channel][(column + lag) % P]
            * weights[channel][column]
            for channel in range(2)
            for column in range(P)
        )
        - (167 if lag == 0 else 0)
        for lag in range(P)
    )


def lies_in_three_lambda(value: Eisenstein) -> bool:
    """Test membership in 3(1-omega) Z[omega]."""

    first, second = value
    return (
        first % 3 == 0
        and second % 3 == 0
        and (first // 3 + second // 3) % 3 == 0
    )


def lambda3_digits(value: Eisenstein) -> tuple[int, int, int]:
    """Reduce an Eisenstein integer in the basis 1,lambda,lambda^2.

    Here ``lambda=1-omega`` and, modulo ``lambda^3``, one has
    ``3=-lambda^2``.
    """

    first, second = value
    constant = first + second
    constant_digit = constant % 3
    integer_quotient = (constant - constant_digit) // 3
    return (
        constant_digit,
        (-second) % 3,
        (-integer_quotient) % 3,
    )


def reconstruct_periodic_target(
    value: Eisenstein,
) -> tuple[int, int, int] | None:
    """Recover q_0,q_1,q_2 with sum 501 from the profile Fourier value."""

    if not lies_in_three_lambda(value):
        return None
    first, second = value[0] // 3, value[1] // 3
    third = (501 - first - second) // 3
    result = third + first, third + second, third
    if sum(result) != 501:
        raise AssertionError("the reconstructed target has the wrong sum")
    return result


def moment_from_exact_correlations(
    correlations: Sequence[int],
) -> Eisenstein:
    if len(correlations) != ROWS:
        raise ValueError("an exact correlation row must have length nine")
    totals = tuple(
        sum(correlations[residue::3]) for residue in range(3)
    )
    return residue_eisenstein(totals)


def audit_profile_table(
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> dict[str, object]:
    table = profile_correlation_table(identifiers_a, identifiers_b)
    failures = tuple(
        class_index
        for class_index, value in enumerate(table[1:])
        if not lies_in_three_lambda(value)
    )
    targets = tuple(
        reconstruct_periodic_target(value) for value in table
    )
    reversal_checks = 0
    for class_index in range(6):
        if table[class_index + 7] != e_conjugate(table[class_index + 1]):
            raise AssertionError("profile reversal/conjugation failed")
        reversal_checks += 1
    physical_sum = table[0]
    nonzero_sum = (0, 0)
    for value in table[1:]:
        nonzero_sum = e_add(nonzero_sum, value)
        physical_sum = e_add(
            physical_sum,
            (3 * value[0], 3 * value[1]),
        )
    return {
        "table": table,
        "table_sha256": compact_hash(table),
        "zero_coefficient": table[0],
        "nonzero_coefficient_sum": nonzero_sum,
        "physical_coefficient_sum": physical_sum,
        "failing_nonzero_classes": failures,
        "failing_class_count": len(failures),
        "reversal_checks": reversal_checks,
        "targets": targets,
        "all_nonzero_targets_integral": not failures,
        "all_targets_in_correlation_range": all(
            target is not None
            and all(0 <= value <= 334 for value in target)
            for target in targets
        ),
    }


def verify_pinned_profile_targets() -> dict[str, object]:
    audit = audit_profile_table(*PINNED_PROFILE_IDS)
    if audit["table_sha256"] != EXPECTED_PINNED_PROFILE_TABLE_SHA256:
        raise AssertionError("the pinned profile table changed")
    if not audit["all_nonzero_targets_integral"]:
        raise AssertionError("the pinned profiles lost their integral targets")
    if compact_hash(audit["targets"]) != EXPECTED_PINNED_TARGETS_SHA256:
        raise AssertionError("the pinned periodic targets changed")

    # The two distinct labelled certificates share these profiles.  Their
    # exact order-three moments must agree with the profile calculation.
    for masks_a, masks_b in (
        (LABELLED_SURVIVOR_MASKS_A, LABELLED_SURVIVOR_MASKS_B),
        (TRIT_SURVIVOR_MASKS_A, TRIT_SURVIVOR_MASKS_B),
    ):
        exact_table = invariant_correlation_table(masks_a, masks_b)
        moments = tuple(
            moment_from_exact_correlations(row) for row in exact_table
        )
        if moments != audit["table"]:
            raise AssertionError("profile and labelled Fourier moments disagree")
    return {
        "active_profile_classes": 12,
        "displayed_conjugate_pair_conditions": 6,
        "independent_ideal_conditions": 5,
        "ideal_norm": 27,
        "periodic_targets": audit["targets"],
        "target_hash": EXPECTED_PINNED_TARGETS_SHA256,
        "table_hash": EXPECTED_PINNED_PROFILE_TABLE_SHA256,
    }


def audit_prior_paired_witnesses() -> dict[str, object]:
    tables = []
    failure_histogram: Counter[int] = Counter()
    for _, identifiers_a, identifiers_b in PAIRED_LAYER_WITNESSES:
        audit = audit_profile_table(identifiers_a, identifiers_b)
        if audit["zero_coefficient"] != (0, 0):
            raise AssertionError("a paired witness lost its origin energy")
        if audit["physical_coefficient_sum"] != (0, 0):
            raise AssertionError("a paired witness lost its global moment sum")
        if audit["nonzero_coefficient_sum"] != (0, 0):
            raise AssertionError("a paired witness lost its nonzero class sum")
        obstruction_trits = tuple(
            lambda3_digits(audit["table"][class_index + 1])[2]
            for class_index in range(6)
        )
        if any(
            lambda3_digits(value)[:2] != (0, 0)
            for value in audit["table"]
        ):
            raise AssertionError("a paired witness lost its lower ideal digits")
        if sum(obstruction_trits) % 3:
            raise AssertionError("the six ideal trits lost their global dependency")
        failures = audit["failing_nonzero_classes"]
        if not failures or any(
            (class_index + 6) % 12 not in failures
            for class_index in failures
        ):
            raise AssertionError("the ideal failures lost reversal pairing")
        failure_histogram[len(failures)] += 1
        tables.append(audit["table"])
    table_hash = compact_hash(tuple(tables))
    if table_hash != EXPECTED_PAIRED_PROFILE_TABLES_SHA256:
        raise AssertionError("the paired profile-correlation corpus changed")
    return {
        "prior_profile_witnesses": len(PAIRED_LAYER_WITNESSES),
        "profile_witnesses_passing_new_ideal_test": 0,
        "failing_class_histogram": tuple(sorted(failure_histogram.items())),
        "independent_ideal_conditions": 5,
        "profile_table_corpus_sha256": table_hash,
        "shard_exclusions": 0,
    }


def verify_all() -> dict[str, object]:
    totals = weight_correlation_totals()
    if totals != (1503,) * P:
        raise AssertionError("the total correlation is not placement-independent")
    return {
        "total_correlation_per_column_lag": totals[0],
        "ideal": "3(1-omega)",
        "ideal_norm": 27,
        "pinned": verify_pinned_profile_targets(),
        "prior": audit_prior_paired_witnesses(),
    }


def main() -> None:
    result = verify_all()
    prior = result["prior"]
    print(
        "total_correlation_per_column_lag="
        f"{result['total_correlation_per_column_lag']}"
    )
    print(f"profile_ideal={result['ideal']}")
    print(f"profile_ideal_norm={result['ideal_norm']}")
    print(
        "displayed_conjugate_pair_conditions="
        f"{result['pinned']['displayed_conjugate_pair_conditions']}"
    )
    print(
        "independent_ideal_conditions="
        f"{result['pinned']['independent_ideal_conditions']}"
    )
    print(
        "prior_profile_witnesses_failing="
        f"{prior['prior_profile_witnesses']}"
    )
    print(f"failing_class_histogram={prior['failing_class_histogram']}")
    print("PASS: exact primitive-nine profile ideal reconstructed")
    print("STATUS: 22 prior profile assignments fail; no shard excluded")


if __name__ == "__main__":
    main()
