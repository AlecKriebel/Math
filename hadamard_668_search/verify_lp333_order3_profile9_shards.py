#!/usr/bin/env python3
"""Replay profile-ideal survivors for all 22 order-three LP(333) shards.

The characteristic-37 checkpoint reduces the row-sum catalog to 22
four-coordinate aggregate targets.  For every target, this verifier pins
one pair of twelve-profile words satisfying simultaneously:

* the exact aggregate target;
* total Eisenstein profile norm 54;
* all six opposite-class local mod-three conditions; and
* the exact primitive-nine profile ideal test on all twelve nonzero
  cyclotomic classes.

The witnesses are profile assignments only.  They do not assert that the
profiles have a labelled nine-row lift, an LP(333), or a Hadamard matrix.
"""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Sequence

from verify_lp333_order3_char37_transfer import (
    PROFILES,
    pair_signature,
    profile_norm,
    row_sum_targets,
    signed_profile_integer,
)
from verify_lp333_order3_profile9 import audit_profile_table


Target = tuple[int, int, int, int]
Identifiers = tuple[int, ...]
ShardWitness = tuple[Target, Identifiers, Identifiers]

EXPECTED_WITNESS_SHA256 = (
    "92fbf448260334f3e4a9b7d1cfb82046d3cb5043721bd5fcb09fbcb4aeaab43f"
)
EXPECTED_PROFILE_TABLES_SHA256 = (
    "27a3fc0c11e745e05e3da8ca273cde3535419009e78cb2ce34ca83fc074b1a78"
)
EXPECTED_PERIODIC_TARGETS_SHA256 = (
    "e7d395500053eeb4346260d545affbb1baea35f01a6793ef48d6b3a3ee9c8628"
)


PROFILE9_SHARD_WITNESSES: tuple[ShardWitness, ...] = (
    (
        (-3, -3, -4, -2),
        (2, 4, 6, 3, 3, 5, 7, 7, 8, 3, 5, 5),
        (5, 6, 5, 5, 5, 5, 2, 5, 1, 5, 5, 5),
    ),
    (
        (-3, -3, -2, 2),
        (5, 5, 5, 9, 8, 0, 5, 5, 5, 5, 7, 5),
        (5, 5, 5, 5, 7, 9, 5, 5, 5, 0, 5, 9),
    ),
    (
        (-3, 0, -3, -3),
        (5, 2, 5, 1, 8, 5, 5, 9, 7, 5, 5, 5),
        (5, 6, 4, 6, 4, 5, 3, 2, 5, 5, 3, 5),
    ),
    (
        (-3, 0, 0, 3),
        (0, 5, 5, 5, 5, 5, 9, 5, 5, 5, 5, 0),
        (9, 5, 5, 5, 5, 9, 3, 5, 5, 5, 5, 5),
    ),
    (
        (-1, -2, -5, -1),
        (1, 6, 5, 5, 3, 5, 9, 5, 5, 5, 6, 5),
        (1, 5, 5, 5, 8, 5, 0, 4, 5, 9, 5, 5),
    ),
    (
        (-1, -2, -4, 1),
        (5, 1, 5, 5, 5, 7, 5, 5, 5, 5, 5, 5),
        (0, 7, 5, 3, 6, 5, 5, 0, 5, 9, 1, 4),
    ),
    (
        (0, 3, -4, -2),
        (5, 3, 7, 5, 5, 5, 7, 9, 8, 4, 5, 8),
        (2, 5, 8, 6, 5, 6, 5, 9, 5, 5, 5, 5),
    ),
    (
        (0, 3, -2, 2),
        (3, 7, 9, 1, 7, 5, 4, 8, 5, 6, 5, 6),
        (5, 7, 5, 5, 6, 8, 8, 8, 5, 5, 5, 5),
    ),
    (
        (1, -1, 2, -2),
        (0, 5, 2, 3, 3, 5, 5, 5, 6, 6, 5, 0),
        (5, 5, 8, 5, 5, 5, 5, 5, 7, 6, 5, 5),
    ),
    (
        (1, -1, 4, 2),
        (1, 5, 1, 4, 5, 5, 5, 7, 5, 5, 8, 2),
        (4, 1, 5, 8, 6, 2, 7, 4, 8, 9, 5, 1),
    ),
    (
        (1, 2, -5, -1),
        (5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 7, 5),
        (0, 7, 5, 5, 4, 2, 3, 7, 3, 5, 5, 3),
    ),
    (
        (1, 2, -4, 1),
        (5, 5, 5, 5, 6, 5, 5, 5, 7, 3, 5, 9),
        (5, 0, 0, 5, 5, 4, 5, 5, 1, 5, 2, 8),
    ),
    (
        (2, -2, -4, -2),
        (1, 6, 5, 8, 5, 5, 5, 5, 3, 5, 5, 0),
        (5, 6, 5, 2, 5, 5, 4, 5, 5, 9, 3, 5),
    ),
    (
        (2, -2, -2, 2),
        (5, 5, 5, 5, 5, 9, 5, 8, 8, 5, 6, 5),
        (0, 5, 1, 0, 4, 5, 5, 4, 3, 5, 5, 5),
    ),
    (
        (2, 1, 2, -2),
        (4, 9, 6, 5, 5, 5, 7, 5, 5, 5, 5, 5),
        (1, 3, 6, 1, 5, 4, 5, 3, 5, 6, 5, 4),
    ),
    (
        (2, 1, 4, 2),
        (0, 5, 5, 5, 1, 2, 5, 4, 5, 5, 5, 4),
        (5, 6, 5, 0, 9, 5, 5, 5, 5, 5, 8, 9),
    ),
    (
        (3, 0, 0, -3),
        (5, 5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 9),
        (5, 5, 5, 3, 5, 5, 5, 5, 5, 5, 3, 3),
    ),
    (
        (3, 0, 3, 3),
        (2, 5, 4, 5, 8, 9, 5, 7, 5, 5, 7, 5),
        (4, 4, 8, 5, 1, 5, 3, 5, 9, 5, 5, 5),
    ),
    (
        (4, -1, 0, 0),
        (1, 5, 1, 5, 5, 8, 6, 5, 1, 4, 5, 1),
        (5, 5, 0, 0, 6, 2, 5, 5, 5, 2, 1, 7),
    ),
    (
        (4, 2, -4, -2),
        (5, 5, 5, 9, 5, 6, 8, 9, 5, 5, 7, 5),
        (5, 5, 5, 9, 0, 1, 2, 5, 5, 5, 7, 5),
    ),
    (
        (4, 2, -2, 2),
        (1, 5, 5, 5, 5, 5, 5, 3, 5, 9, 8, 7),
        (7, 5, 5, 5, 6, 5, 0, 5, 3, 5, 5, 7),
    ),
    (
        (5, 1, 0, 0),
        (4, 5, 5, 7, 5, 5, 6, 8, 5, 9, 5, 2),
        (5, 1, 5, 9, 0, 5, 8, 5, 5, 2, 5, 4),
    ),
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def audit_shard_witness(
    target: Sequence[int],
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
) -> dict[str, object]:
    """Replay one profile witness without invoking a search solver."""

    normalized_target = tuple(int(value) for value in target)
    if len(normalized_target) != 4:
        raise ValueError("an aggregate target must have four coordinates")
    identifiers = (
        tuple(int(value) for value in identifiers_a),
        tuple(int(value) for value in identifiers_b),
    )
    if any(len(channel) != 12 for channel in identifiers):
        raise ValueError("each channel must contain twelve profile IDs")
    if any(
        not 0 <= profile_id < len(PROFILES)
        for channel in identifiers
        for profile_id in channel
    ):
        raise ValueError("a profile ID lies outside the ten-state catalog")

    aggregate = []
    for channel in range(2):
        value = [0, 0]
        for class_index, profile_id in enumerate(identifiers[channel]):
            contribution = signed_profile_integer(
                channel, class_index, profile_id
            )
            value[0] += contribution[0]
            value[1] += contribution[1]
        aggregate.extend(value)
    if tuple(aggregate) != normalized_target:
        raise ValueError("the profile assignment has the wrong aggregate")

    energy = sum(
        profile_norm(profile_id)
        for channel in identifiers
        for profile_id in channel
    )
    if energy != 54:
        raise ValueError("the profile assignment has the wrong energy")

    for class_index in range(6):
        if pair_signature(
            identifiers[0][class_index],
            identifiers[0][class_index + 6],
        ) != pair_signature(
            identifiers[1][class_index],
            identifiers[1][class_index + 6],
        ):
            raise ValueError("an opposite-class local condition failed")

    ideal = audit_profile_table(*identifiers)
    if ideal["zero_coefficient"] != (0, 0):
        raise ValueError("the origin profile coefficient is nonzero")
    if ideal["physical_coefficient_sum"] != (0, 0):
        raise ValueError("the global profile moment is nonzero")
    if ideal["failing_nonzero_classes"]:
        raise ValueError("a primitive-nine profile ideal test failed")
    if not ideal["all_nonzero_targets_integral"]:
        raise ValueError("a periodic target was not integral")
    if not ideal["all_targets_in_correlation_range"]:
        raise ValueError("a reconstructed periodic target left its range")

    return {
        "target": normalized_target,
        "energy": energy,
        "local_conditions": 6,
        "profile_ideal_tests": 12,
        "profile_table": ideal["table"],
        "periodic_targets": ideal["targets"],
        "valid": True,
    }


def verify_profile9_shard_witnesses() -> dict[str, object]:
    expected_targets = row_sum_targets()
    witness_targets = tuple(
        witness[0] for witness in PROFILE9_SHARD_WITNESSES
    )
    if witness_targets != expected_targets:
        raise AssertionError("the profile witnesses do not cover the 22 shards")
    if len(set(witness_targets)) != len(witness_targets):
        raise AssertionError("a profile shard target was duplicated")

    profile_tables = []
    periodic_targets = []
    for target, identifiers_a, identifiers_b in PROFILE9_SHARD_WITNESSES:
        audit = audit_shard_witness(target, identifiers_a, identifiers_b)
        profile_tables.append(audit["profile_table"])
        periodic_targets.append(audit["periodic_targets"])

    witness_hash = compact_hash(PROFILE9_SHARD_WITNESSES)
    table_hash = compact_hash(tuple(profile_tables))
    target_hash = compact_hash(tuple(periodic_targets))
    if EXPECTED_WITNESS_SHA256 and witness_hash != EXPECTED_WITNESS_SHA256:
        raise AssertionError("the profile-shard witness corpus changed")
    if (
        EXPECTED_PROFILE_TABLES_SHA256
        and table_hash != EXPECTED_PROFILE_TABLES_SHA256
    ):
        raise AssertionError("the profile correlation tables changed")
    if (
        EXPECTED_PERIODIC_TARGETS_SHA256
        and target_hash != EXPECTED_PERIODIC_TARGETS_SHA256
    ):
        raise AssertionError("the reconstructed periodic targets changed")

    return {
        "aggregate_shards": len(expected_targets),
        "profile_assignments": len(PROFILE9_SHARD_WITNESSES),
        "aggregate_energy_checks": len(PROFILE9_SHARD_WITNESSES),
        "local_conditions_checked": 6 * len(PROFILE9_SHARD_WITNESSES),
        "profile_ideal_tests_checked": 12 * len(PROFILE9_SHARD_WITNESSES),
        "witness_sha256": witness_hash,
        "profile_tables_sha256": table_hash,
        "periodic_targets_sha256": target_hash,
        "shard_exclusions": 0,
        "labelled_lifts_asserted": 0,
    }


def main() -> None:
    result = verify_profile9_shard_witnesses()
    print(f"aggregate_shards={result['aggregate_shards']}")
    print(f"profile_assignments={result['profile_assignments']}")
    print(f"local_conditions_checked={result['local_conditions_checked']}")
    print(
        "profile_ideal_tests_checked="
        f"{result['profile_ideal_tests_checked']}"
    )
    print(f"witness_sha256={result['witness_sha256']}")
    print(f"profile_tables_sha256={result['profile_tables_sha256']}")
    print(f"periodic_targets_sha256={result['periodic_targets_sha256']}")
    print("PASS: all 22 profile-ideal shard witnesses replayed")
    print("STATUS: every aggregate shard survives at profile level")
    print("STATUS: no labelled lift, LP(333), or H(668) asserted")


if __name__ == "__main__":
    main()
