#!/usr/bin/env python3
"""Dependency-free verifier for the exact h=0 order-three profile."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Sequence


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "certificate.json"
P = 37
CLASS_COUNT = 12
GROUP_ORDER = 24

# A profile ID is the triple of plus-counts in the three row residues.
PROFILES = (
    (0, 0, 3),
    (0, 1, 2),
    (0, 2, 1),
    (0, 3, 0),
    (1, 0, 2),
    (1, 1, 1),
    (1, 2, 0),
    (2, 0, 1),
    (2, 1, 0),
    (3, 0, 0),
)

TARGETS = (
    (-3, -3, -4, -2), (-3, -3, -2, 2), (-3, 0, -3, -3),
    (-3, 0, 0, 3), (-1, -2, -5, -1), (-1, -2, -4, 1),
    (0, 3, -4, -2), (0, 3, -2, 2), (1, -1, 2, -2),
    (1, -1, 4, 2), (1, 2, -5, -1), (1, 2, -4, 1),
    (2, -2, -4, -2), (2, -2, -2, 2), (2, 1, 2, -2),
    (2, 1, 4, 2), (3, 0, 0, -3), (3, 0, 3, 3),
    (4, -1, 0, 0), (4, 2, -4, -2), (4, 2, -2, 2),
    (5, 1, 0, 0),
)

E = tuple[int, int]


def e_add(left: E, right: E) -> E:
    return left[0] + right[0], left[1] + right[1]


def e_scale(factor: int, value: E) -> E:
    return factor * value[0], factor * value[1]


def e_conjugate(value: E) -> E:
    return value[0] - value[1], -value[1]


def e_multiply(left: E, right: E) -> E:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_norm(value: E) -> int:
    a, b = value
    return a * a - a * b + b * b


def raw_profile(identifier: int) -> E:
    p0, p1, p2 = PROFILES[identifier]
    return p0 - p2, p1 - p2


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("ascii")


def sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def cyclotomic_classes(
    subgroup: Sequence[int], generator: int
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    classes = []
    class_of = [-1] * P
    power = 1
    for class_index in range(CLASS_COUNT):
        part = tuple(power * int(member) % P for member in subgroup)
        if len(set(part)) != 3:
            raise AssertionError("a cyclotomic class is not a triple")
        classes.append(part)
        for value in part:
            if value == 0 or class_of[value] != -1:
                raise AssertionError("cyclotomic classes overlap")
            class_of[value] = class_index
        power = generator * power % P
    if set().union(*(set(part) for part in classes)) != set(range(1, P)):
        raise AssertionError("cyclotomic classes do not cover F_37^*")
    return tuple(classes), tuple(class_of)


def compressed_values(
    ids_a: Sequence[int], ids_b: Sequence[int]
) -> tuple[tuple[E, ...], tuple[E, ...]]:
    result = []
    for channel, identifiers in enumerate((ids_a, ids_b)):
        if len(identifiers) != CLASS_COUNT:
            raise AssertionError("a profile word must have length twelve")
        values = [(-1, 0) if channel == 0 else (2, 0)]
        for class_index, identifier in enumerate(identifiers):
            if not 0 <= int(identifier) < len(PROFILES):
                raise AssertionError("profile ID outside the alphabet")
            epsilon = 1 if class_index % 2 == 0 else -1
            factor = -epsilon if channel == 0 else epsilon
            values.append(e_scale(factor, raw_profile(int(identifier))))
        result.append(tuple(values))
    return tuple(result)  # type: ignore[return-value]


def aggregate(values: Sequence[Sequence[E]]) -> tuple[int, int, int, int]:
    result = []
    for channel in range(2):
        total = (0, 0)
        for value in values[channel][1:]:
            total = e_add(total, value)
        result.extend(total)
    return tuple(result)  # type: ignore[return-value]


def expand_physical(
    values: Sequence[Sequence[E]], class_of: Sequence[int]
) -> tuple[tuple[E, ...], tuple[E, ...]]:
    result = []
    for channel in range(2):
        word = [values[channel][0]]
        word.extend(
            values[channel][class_of[position] + 1]
            for position in range(1, P)
        )
        result.append(tuple(word))
    return tuple(result)  # type: ignore[return-value]


def physical_correlations(
    physical: Sequence[Sequence[E]],
) -> tuple[E, ...]:
    result = []
    for lag in range(P):
        total = (0, 0)
        for channel in range(2):
            for source in range(P):
                total = e_add(
                    total,
                    e_multiply(
                        physical[channel][(source + lag) % P],
                        e_conjugate(physical[channel][source]),
                    ),
                )
        result.append(total)
    return tuple(result)


def conjugate_profile_id(identifier: int) -> int:
    wanted = e_conjugate(raw_profile(identifier))
    matches = [
        candidate
        for candidate in range(len(PROFILES))
        if raw_profile(candidate) == wanted
    ]
    if len(matches) != 1:
        raise AssertionError("profile conjugation is not unique")
    return matches[0]


def transform_assignment(
    identifiers: Sequence[int], group_element: int
) -> tuple[int, ...]:
    rotation = group_element // 4
    result = []
    for channel in range(2):
        star = (
            bool((group_element // 2) % 2)
            if channel == 0
            else bool(group_element % 2)
        )
        offset = (2 * rotation + (6 if star else 0)) % CLASS_COUNT
        for class_index in range(CLASS_COUNT):
            identifier = int(
                identifiers[
                    channel * CLASS_COUNT
                    + (class_index + offset) % CLASS_COUNT
                ]
            )
            result.append(
                conjugate_profile_id(identifier) if star else identifier
            )
    return tuple(result)


def mix64(value: int) -> int:
    mask = (1 << 64) - 1
    value &= mask
    value ^= value >> 30
    value = value * 0xBF58476D1CE4E5B9 & mask
    value ^= value >> 27
    value = value * 0x94D049BB133111EB & mask
    return (value ^ (value >> 31)) & mask


def production_digest(
    identifiers: Sequence[int],
    exact: Sequence[E],
    target_index: int,
) -> str:
    mask = (1 << 64) - 1
    digest = 0x66833337
    for slot, identifier in enumerate(identifiers):
        digest ^= mix64(int(identifier) + 17 * (slot + 1))
    for lag, (a, b) in enumerate(exact):
        digest ^= mix64((a & mask) + 257 * (lag + 1))
        digest ^= mix64((b & mask) + 65537 * (lag + 1))
    digest ^= mix64(target_index + 1)
    return f"0x{digest & mask:x}"


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    core = {
        "schema": certificate["schema"],
        "prime": certificate["prime"],
        "subgroup": certificate["subgroup"],
        "class_generator": certificate["class_generator"],
        "target": certificate["target"],
        "profile_ids_a": certificate["profile_ids_a"],
        "profile_ids_b": certificate["profile_ids_b"],
    }
    if sha256_json(core) != certificate["semantic_sha256"]:
        raise AssertionError("certificate semantic hash changed")
    if certificate["prime"] != P:
        raise AssertionError("certificate prime changed")

    identifiers = (
        tuple(map(int, certificate["profile_ids_a"])),
        tuple(map(int, certificate["profile_ids_b"])),
    )
    target = tuple(map(int, certificate["target"]))
    target_index = int(certificate["target_index"])
    if TARGETS[target_index] != target:
        raise AssertionError("target index and target disagree")

    classes, class_of = cyclotomic_classes(
        certificate["subgroup"], int(certificate["class_generator"])
    )
    values = compressed_values(*identifiers)
    if aggregate(values) != target:
        raise AssertionError("exact aggregate target failed")
    physical = expand_physical(values, class_of)
    correlations = physical_correlations(physical)
    expected = certificate["expected_profile_correlations"]
    if tuple(expected["zero_lag"]) != correlations[0]:
        raise AssertionError("zero-lag profile correlation changed")
    if any(
        value != tuple(expected["all_36_nonzero_lags"])
        for value in correlations[1:]
    ):
        raise AssertionError("a nonzero physical correlation is nonzero")

    shell_counts = {0: 0, 3: 0, 9: 0}
    for identifier in identifiers[0] + identifiers[1]:
        norm = e_norm(raw_profile(identifier))
        if norm not in shell_counts:
            raise AssertionError("profile norm outside the h=0 shell")
        shell_counts[norm] += 1
    shell = certificate["shell"]
    if (
        shell_counts[9],
        shell_counts[3],
        shell_counts[0],
    ) != (
        shell["norm_9_profiles"],
        shell["norm_3_profiles"],
        shell["norm_0_profiles"],
    ):
        raise AssertionError("profile shell counts changed")

    joined = identifiers[0] + identifiers[1]
    images = tuple(
        transform_assignment(joined, group)
        for group in range(GROUP_ORDER)
    )
    orbit = tuple(sorted(set(images)))
    stabilizer = tuple(
        group for group, image in enumerate(images) if image == joined
    )
    group_record = certificate["group"]
    if (
        GROUP_ORDER,
        len(stabilizer),
        len(orbit),
        list(stabilizer),
        joined == orbit[0],
    ) != (
        group_record["order"],
        group_record["stabilizer_order"],
        group_record["orbit_size"],
        group_record["stabilizer_elements"],
        group_record["canonical"],
    ):
        raise AssertionError("group orbit/stabilizer certificate changed")
    if sha256_json([list(image) for image in orbit]) != certificate[
        "orbit_sha256"
    ]:
        raise AssertionError("orbit semantic hash changed")

    replay = {
        "aggregate": list(target),
        "correlations": [list(value) for value in correlations],
        "physical_a": [list(value) for value in physical[0]],
        "physical_b": [list(value) for value in physical[1]],
    }
    if sha256_json(replay) != certificate["physical_replay_sha256"]:
        raise AssertionError("physical replay semantic hash changed")
    compact = tuple(
        correlations[classes[lag][0]] for lag in range(6)
    )
    digest = production_digest(joined, compact, target_index)
    if digest != certificate["production_digest"]:
        raise AssertionError("production digest failed independent replay")

    return {
        "target": target,
        "profile_ids": len(joined),
        "physical_lags_replayed": len(correlations),
        "zero_nontrivial_correlations": sum(
            value == (0, 0) for value in correlations[1:]
        ),
        "norm_9_profiles": shell_counts[9],
        "norm_3_profiles": shell_counts[3],
        "norm_0_profiles": shell_counts[0],
        "group_order": GROUP_ORDER,
        "stabilizer_order": len(stabilizer),
        "orbit_size": len(orbit),
        "canonical": joined == orbit[0],
        "semantic_sha256": certificate["semantic_sha256"],
        "orbit_sha256": certificate["orbit_sha256"],
        "physical_replay_sha256":
            certificate["physical_replay_sha256"],
        "production_digest": digest,
        "status": "PASS",
    }


def main() -> None:
    result = verify()
    for key, value in result.items():
        print(f"{key}={value}")
    print("PASS: independent all-37 exact h=0 profile replay")
    print("STATUS: exact profile only; no labelled LP(333) or H(668)")


if __name__ == "__main__":
    main()
