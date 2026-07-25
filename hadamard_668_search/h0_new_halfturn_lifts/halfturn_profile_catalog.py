#!/usr/bin/env python3
"""Discover half-turn-fixed exact h0 profiles from a strict v2 aggregate."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
EXACT_ROOT = SEARCH_ROOT / "dense_shell_exact_profile_h0"
sys.path.insert(0, str(EXACT_ROOT))

import verify_exact_profile_h0 as exact_profile  # noqa: E402


AGGREGATE_SCHEMA = "dense-shell-production-aggregate-v2"
PREFIX_SHARDS = 27 * 27
HEX_DIGEST = re.compile(r"0x[0-9a-f]{16}")
REQUIRED_TRUE_FLAGS = (
    "canonical",
    "char2",
    "mod9",
    "post_mod9_lambda",
    "mod27",
    "exact_zero",
)


def profile_stabilizer(
    ids_a: Sequence[int],
    ids_b: Sequence[int],
) -> tuple[int, ...]:
    identifiers = tuple(map(int, ids_a)) + tuple(map(int, ids_b))
    return tuple(
        group
        for group in range(exact_profile.GROUP_ORDER)
        if exact_profile.transform_assignment(identifiers, group)
        == identifiers
    )


def fixed_by_class_halfturn(
    ids_a: Sequence[int],
    ids_b: Sequence[int],
) -> bool:
    left = tuple(map(int, ids_a))
    right = tuple(map(int, ids_b))
    return (
        len(left) == len(right) == 12
        and left[:6] == left[6:]
        and right[:6] == right[6:]
    )


def replay_exact_profile(
    ids_a: Sequence[int],
    ids_b: Sequence[int],
    target: Sequence[int],
    target_index: int,
    digest: str,
) -> None:
    """Replay the aggregate, all 37 lags, canonical action, and digest."""

    left = tuple(map(int, ids_a))
    right = tuple(map(int, ids_b))
    target_tuple = tuple(map(int, target))
    if len(left) != 12 or len(right) != 12:
        raise ValueError("an aggregate profile word is not length twelve")
    if any(not 0 <= identifier < 10 for identifier in left + right):
        raise ValueError("an aggregate profile identifier is out of range")
    if not 0 <= target_index < len(exact_profile.TARGETS):
        raise ValueError("an aggregate target index is out of range")
    if exact_profile.TARGETS[target_index] != target_tuple:
        raise ValueError("an aggregate target and target index disagree")
    if HEX_DIGEST.fullmatch(digest) is None:
        raise ValueError("an aggregate digest is malformed")

    classes, class_of = exact_profile.cyclotomic_classes((1, 26, 10), 2)
    if len(classes) != 12:
        raise AssertionError("the order-three class system changed")
    compressed = exact_profile.compressed_values(left, right)
    if exact_profile.aggregate(compressed) != target_tuple:
        raise ValueError("an aggregate profile fails its target")
    physical = exact_profile.expand_physical(compressed, class_of)
    correlations = exact_profile.physical_correlations(physical)
    if correlations[0] != (167, 0) or correlations[1:] != ((0, 0),) * 36:
        raise ValueError("an aggregate profile fails its all-37 replay")
    if exact_profile.production_digest(
        left + right,
        ((0, 0),) * 6,
        target_index,
    ) != digest:
        raise ValueError("an aggregate profile digest changed")
    orbit = tuple(
        exact_profile.transform_assignment(left + right, group)
        for group in range(exact_profile.GROUP_ORDER)
    )
    if left + right != min(orbit):
        raise ValueError("an aggregate profile is not canonical")


def normalize_orbit(row: object) -> dict[str, object]:
    if not isinstance(row, dict):
        raise ValueError("an exact-profile orbit row is not an object")
    for flag in REQUIRED_TRUE_FLAGS:
        if row.get(flag) is not True:
            raise ValueError(f"an exact-profile orbit lost flag {flag}")
    if row.get("physical_lags_independently_replayed") != 37:
        raise ValueError("an exact-profile orbit lost its 37-lag replay")
    exact = row.get("exact")
    if (
        not isinstance(exact, list)
        or len(exact) != 6
        or any(pair != [0, 0] for pair in exact)
    ):
        raise ValueError("an exact-profile orbit is not exact at six classes")
    sources = row.get("source_shards")
    if (
        not isinstance(sources, list)
        or not sources
        or sources != sorted(sources)
        or any(not isinstance(source, str) for source in sources)
    ):
        raise ValueError("an exact-profile orbit has malformed sources")

    ids_a = tuple(map(int, row["ids_a"]))
    ids_b = tuple(map(int, row["ids_b"]))
    target = tuple(map(int, row["target"]))
    target_index = int(row["target_index"])
    digest = str(row["digest"])
    replay_exact_profile(
        ids_a, ids_b, target, target_index, digest
    )
    stabilizer = profile_stabilizer(ids_a, ids_b)
    orbit_size = exact_profile.GROUP_ORDER // len(stabilizer)
    if orbit_size * len(stabilizer) != exact_profile.GROUP_ORDER:
        raise AssertionError("orbit-stabilizer failed")
    return {
        "digest": digest,
        "ids_a": ids_a,
        "ids_b": ids_b,
        "target": target,
        "target_index": target_index,
        "source_shards": tuple(sources),
        "stabilizer_elements": stabilizer,
        "stabilizer_order": len(stabilizer),
        "orbit_size": orbit_size,
        "halfturn_fixed": fixed_by_class_halfturn(ids_a, ids_b),
    }


def profiles_from_strict_aggregate(path: Path) -> dict[str, object]:
    """Return every half-turn-fixed exact h0 profile in a strict aggregate."""

    aggregate = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(aggregate, dict):
        raise ValueError("the strict aggregate is not an object")
    if aggregate.get("schema") != AGGREGATE_SCHEMA:
        raise ValueError("the strict aggregate schema changed")
    if aggregate.get("status") != (
        "PASS: every required prefix shard is complete"
    ):
        raise ValueError("the strict aggregate does not have PASS status")
    for hash_key in ("source_sha256", "binary_sha256"):
        value = aggregate.get(hash_key)
        if (
            not isinstance(value, str)
            or re.fullmatch(r"[0-9a-f]{64}", value) is None
        ):
            raise ValueError(f"the strict aggregate {hash_key} is malformed")

    shells = aggregate.get("shells")
    if not isinstance(shells, dict) or not isinstance(shells.get("h0"), dict):
        raise ValueError("the strict aggregate has no h0 shell")
    h0 = shells["h0"]
    if (
        h0.get("complete") is not True
        or h0.get("prefix_shards") != PREFIX_SHARDS
        or h0.get("upper_exact_scope") != "char2_mod9_intersection"
        or h0.get("burnside_weighted_partition_check") != "PASS"
    ):
        raise ValueError("the strict h0 shell is incomplete or malformed")
    rows = h0.get("exact_profile_orbits")
    if not isinstance(rows, list):
        raise ValueError("the strict h0 orbit catalog is malformed")
    if h0.get("distinct_canonical_exact_profile_orbits") != len(rows):
        raise ValueError("the strict h0 distinct-orbit count changed")

    normalized = tuple(normalize_orbit(row) for row in rows)
    keys = tuple(
        (
            tuple(record["ids_a"]) + tuple(record["ids_b"]),
            int(record["target_index"]),
        )
        for record in normalized
    )
    if any(left >= right for left, right in zip(keys, keys[1:])):
        raise ValueError("the strict h0 orbit catalog is not strictly sorted")
    digests = tuple(str(record["digest"]) for record in normalized)
    if len(set(digests)) != len(digests):
        raise ValueError("the strict h0 orbit catalog repeats a digest")
    halfturn_profiles = tuple(
        record for record in normalized if record["halfturn_fixed"]
    )
    if any(
        12 not in record["stabilizer_elements"]
        for record in halfturn_profiles
    ):
        raise AssertionError("a six-class repeat lost group element 12")
    return {
        "schema": "lp333-h0-halfturn-profile-catalog-v2",
        "aggregate_path": str(path.resolve()),
        "aggregate_source_sha256": aggregate["source_sha256"],
        "aggregate_binary_sha256": aggregate["binary_sha256"],
        "all_exact_h0_orbits": len(normalized),
        "halfturn_fixed_orbits": len(halfturn_profiles),
        "profiles": halfturn_profiles,
    }
