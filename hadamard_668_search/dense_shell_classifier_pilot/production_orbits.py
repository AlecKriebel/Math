#!/usr/bin/env python3
"""Strict parsing and detached replay of retained exact-profile orbits."""

from __future__ import annotations

from dataclasses import dataclass
import re

from production_common import TARGETS, require_nonnegative_integer
from verify_dense_shell_classifier_pilot import (
    parse_exact,
    parse_ints,
    raw_profile,
    replay_witness,
)


RECORD_PATTERN = re.compile(r"exact_orbit_(\d{6})_(.+)")
RECORD_SUFFIXES = frozenset(
    {
        "present",
        "target_index",
        "target",
        "ids_a",
        "ids_b",
        "exact",
        "canonical",
        "char2",
        "mod9",
        "post_mod9_lambda",
        "mod27",
        "exact_zero",
        "digest",
    }
)
META_KEYS = frozenset(
    {
        "exact_orbit_mode",
        "exact_orbit_collection",
        "exact_orbit_count",
    }
)


@dataclass(frozen=True)
class ExactOrbit:
    ids_a: tuple[int, ...]
    ids_b: tuple[int, ...]
    target_index: int
    target: tuple[int, ...]
    exact: tuple[tuple[int, int], ...]
    digest: str

    @property
    def key(self) -> tuple[tuple[int, ...], int]:
        return self.ids_a + self.ids_b, self.target_index

    def as_dict(self) -> dict[str, object]:
        return {
            "ids_a": list(self.ids_a),
            "ids_b": list(self.ids_b),
            "target_index": self.target_index,
            "target": list(self.target),
            "exact": [list(pair) for pair in self.exact],
            "digest": self.digest,
            "canonical": True,
            "char2": True,
            "mod9": True,
            "post_mod9_lambda": True,
            "mod27": True,
            "exact_zero": True,
            "physical_lags_independently_replayed": 37,
        }


def _conjugate_profile_id(identifier: int) -> int:
    wanted_a, wanted_b = raw_profile(identifier)
    wanted = (wanted_a - wanted_b, -wanted_b)
    matches = [
        candidate
        for candidate in range(10)
        if raw_profile(candidate) == wanted
    ]
    if len(matches) != 1:
        raise AssertionError("profile alphabet lost conjugation closure")
    return matches[0]


CONJUGATE_PROFILE_IDS = tuple(
    _conjugate_profile_id(identifier) for identifier in range(10)
)


def _transform_assignment(
    identifiers: tuple[int, ...], group: int
) -> tuple[int, ...]:
    if len(identifiers) != 24:
        raise AssertionError("assignment length changed")
    rotation = group // 4
    result = [0] * 24
    for channel in range(2):
        star = bool((group // (2 if channel == 0 else 1)) % 2)
        offset = (2 * rotation + (6 if star else 0)) % 12
        for index in range(12):
            identifier = identifiers[
                12 * channel + (index + offset) % 12
            ]
            if star:
                identifier = CONJUGATE_PROFILE_IDS[identifier]
            result[12 * channel + index] = identifier
    return tuple(result)


def _is_canonical(identifiers: tuple[int, ...]) -> bool:
    return identifiers == min(
        _transform_assignment(identifiers, group)
        for group in range(24)
    )


def _assert_binary_one(
    parsed: dict[str, str], key: str
) -> None:
    if parsed.get(key) != "1":
        raise ValueError(f"{key} must be 1 for an exact-profile orbit")


def _same_witness(
    parsed: dict[str, str], left: str, right: str
) -> bool:
    return all(
        parsed.get(f"{left}_{suffix}")
        == parsed.get(f"{right}_{suffix}")
        for suffix in RECORD_SUFFIXES
        if suffix != "present"
    )


def validate_exact_orbit_output(
    parsed: dict[str, str],
    shell: str,
    *,
    expected_collection: str,
) -> tuple[ExactOrbit, ...]:
    """Validate, canonically order, and independently replay every orbit."""

    if parsed.get("exact_orbit_mode") != "enumerate":
        raise ValueError("exact-orbit output is not in enumeration mode")
    if parsed.get("exact_orbit_collection") != expected_collection:
        raise ValueError(
            "exact-orbit collection scope mismatch "
            f"({parsed.get('exact_orbit_collection')!r} != "
            f"{expected_collection!r})"
        )
    count = require_nonnegative_integer(parsed, "exact_orbit_count")

    record_fields: dict[int, set[str]] = {}
    for key in parsed:
        if not key.startswith("exact_orbit_") or key in META_KEYS:
            continue
        match = RECORD_PATTERN.fullmatch(key)
        if match is None:
            raise ValueError(f"malformed exact-orbit output key {key!r}")
        index = int(match.group(1))
        record_fields.setdefault(index, set()).add(match.group(2))
    if set(record_fields) != set(range(count)):
        raise ValueError("exact-orbit record indices are not contiguous")
    for index, suffixes in record_fields.items():
        if suffixes != RECORD_SUFFIXES:
            raise ValueError(
                f"exact_orbit_{index:06d} field set mismatch"
            )

    result: list[ExactOrbit] = []
    for index in range(count):
        prefix = f"exact_orbit_{index:06d}"
        for suffix in (
            "present",
            "canonical",
            "char2",
            "mod9",
            "post_mod9_lambda",
            "mod27",
            "exact_zero",
        ):
            _assert_binary_one(parsed, f"{prefix}_{suffix}")
        try:
            replay_witness(parsed, prefix, shell)
        except (
            AssertionError,
            IndexError,
            KeyError,
            ValueError,
        ) as error:
            raise ValueError(
                f"{prefix}: detached all-37 replay failed: {error}"
            ) from error

        ids_a = parse_ints(parsed[f"{prefix}_ids_a"])
        ids_b = parse_ints(parsed[f"{prefix}_ids_b"])
        identifiers = ids_a + ids_b
        if (
            len(identifiers) != 24
            or any(not 0 <= identifier < 10 for identifier in identifiers)
        ):
            raise ValueError(
                f"{prefix}: profile identifiers are out of range"
            )
        if not _is_canonical(identifiers):
            raise ValueError(f"{prefix}: identifiers are not canonical")
        target_index = int(parsed[f"{prefix}_target_index"])
        if not 0 <= target_index < len(TARGETS):
            raise ValueError(f"{prefix}: target index is out of range")
        target = parse_ints(parsed[f"{prefix}_target"])
        if target != TARGETS[target_index]:
            raise ValueError(
                f"{prefix}: target and target index disagree"
            )
        exact = parse_exact(parsed[f"{prefix}_exact"])
        if any(pair != (0, 0) for pair in exact):
            raise ValueError(f"{prefix}: correlations are not exact zero")
        result.append(
            ExactOrbit(
                ids_a=ids_a,
                ids_b=ids_b,
                target_index=target_index,
                target=target,
                exact=exact,
                digest=parsed[f"{prefix}_digest"],
            )
        )

    keys = [orbit.key for orbit in result]
    if any(left >= right for left, right in zip(keys, keys[1:])):
        raise ValueError(
            "exact-profile orbits are duplicated or not canonically sorted"
        )

    exact_hits = require_nonnegative_integer(parsed, "exact_zero_hits")
    weighted_hits = require_nonnegative_integer(
        parsed, "weighted_exact_zero_hits"
    )
    if (exact_hits == 0) != (count == 0):
        raise ValueError(
            "exact-zero hit counter and retained-orbit count disagree"
        )
    if exact_hits < count or weighted_hits < exact_hits:
        raise ValueError("exact-zero hit accounting is inconsistent")

    witness_present = require_nonnegative_integer(
        parsed, "witness_exact_present"
    )
    if witness_present not in (0, 1):
        raise ValueError("witness_exact_present is not binary")
    if witness_present != bool(count):
        raise ValueError(
            "witness_exact presence and retained-orbit count disagree"
        )
    if count:
        try:
            replay_witness(parsed, "witness_exact", shell)
        except (
            AssertionError,
            IndexError,
            KeyError,
            ValueError,
        ) as error:
            raise ValueError(
                f"witness_exact detached replay failed: {error}"
            ) from error
        if parsed.get("witness_exact_canonical") != "1":
            raise ValueError("witness_exact is not marked canonical")
        if not _same_witness(
            parsed, "witness_exact", "exact_orbit_000000"
        ):
            raise ValueError(
                "witness_exact is not the first canonical orbit"
            )
    return tuple(result)
