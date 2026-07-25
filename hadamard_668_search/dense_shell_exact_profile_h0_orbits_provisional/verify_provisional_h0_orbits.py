#!/usr/bin/env python3
"""Dependency-free audit of five inequivalent exact dense-shell h=0 profiles.

The three profiles marked ``new`` came from completed production prefixes
h0-p00-p07 and h0-p00-p08.  This verifier deliberately imports no production
code.  It reconstructs the order-three cyclotomic classes, performs all
37 correlations in integer Eisenstein arithmetic, rebuilds the exact
24-element profile action, and compares every pair of orbits.
"""

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

# ID i is the three plus-counts of its three row residues.
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

# a + b*w, where w^2 + w + 1 = 0
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
    covered = set().union(*(set(part) for part in classes))
    if covered != set(range(1, P)):
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


def all_physical_correlations(
    physical: Sequence[Sequence[E]],
) -> tuple[E, ...]:
    """Directly evaluate both channels at every lag in Z[w]."""
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
    """Exact C6 x C2(A-star) x C2(B-star) production action."""
    if len(identifiers) != 2 * CLASS_COUNT:
        raise AssertionError("assignment length changed")
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


def verify_profile(
    record: dict[str, object],
    classes: Sequence[Sequence[int]],
    class_of: Sequence[int],
) -> tuple[dict[str, object], frozenset[tuple[int, ...]]]:
    label = str(record["label"])
    ids_a = tuple(map(int, record["profile_ids_a"]))  # type: ignore[arg-type]
    ids_b = tuple(map(int, record["profile_ids_b"]))  # type: ignore[arg-type]
    joined = ids_a + ids_b
    target = tuple(map(int, record["target"]))  # type: ignore[arg-type]
    target_index = int(record["target_index"])

    core = {
        "label": label,
        "target": list(target),
        "target_index": target_index,
        "profile_ids_a": list(ids_a),
        "profile_ids_b": list(ids_b),
    }
    if sha256_json(core) != record["semantic_sha256"]:
        raise AssertionError(f"{label}: semantic hash changed")
    if TARGETS[target_index] != target:
        raise AssertionError(f"{label}: target index and target disagree")

    values = compressed_values(ids_a, ids_b)
    if aggregate(values) != target:
        raise AssertionError(f"{label}: aggregate target failed")
    physical = expand_physical(values, class_of)
    correlations = all_physical_correlations(physical)
    expected_correlations = record["expected_profile_correlations"]
    if correlations[0] != tuple(expected_correlations["zero_lag"]):
        raise AssertionError(f"{label}: zero-lag equation failed")
    expected_nonzero = tuple(
        expected_correlations["all_36_nonzero_lags"]
    )
    failed_lags = [
        lag for lag in range(1, P)
        if correlations[lag] != expected_nonzero
    ]
    if failed_lags:
        raise AssertionError(
            f"{label}: nonzero equations failed at {failed_lags}"
        )

    shell_counts = {
        norm: sum(
            e_norm(raw_profile(identifier)) == norm
            for identifier in joined
        )
        for norm in (0, 3, 9)
    }
    expected_shell = record["shell"]
    if (
        shell_counts[9],
        shell_counts[3],
        shell_counts[0],
    ) != (
        expected_shell["norm_9_profiles"],
        expected_shell["norm_3_profiles"],
        expected_shell["norm_0_profiles"],
    ):
        raise AssertionError(f"{label}: shell census changed")

    images = tuple(
        transform_assignment(joined, group)
        for group in range(GROUP_ORDER)
    )
    orbit = tuple(sorted(set(images)))
    stabilizer = tuple(
        group for group, image in enumerate(images) if image == joined
    )
    group_record = record["group"]
    group_replay = (
        GROUP_ORDER,
        len(stabilizer),
        len(orbit),
        list(stabilizer),
        joined == orbit[0],
    )
    group_expected = (
        group_record["order"],
        group_record["stabilizer_order"],
        group_record["orbit_size"],
        group_record["stabilizer_elements"],
        group_record["canonical"],
    )
    if group_replay != group_expected:
        raise AssertionError(f"{label}: group certificate changed")
    if sha256_json([list(image) for image in orbit]) != record[
        "orbit_sha256"
    ]:
        raise AssertionError(f"{label}: orbit hash changed")

    replay = {
        "aggregate": list(target),
        "correlations": [list(value) for value in correlations],
        "physical_a": [list(value) for value in physical[0]],
        "physical_b": [list(value) for value in physical[1]],
    }
    if sha256_json(replay) != record["physical_replay_sha256"]:
        raise AssertionError(f"{label}: physical replay hash changed")
    compact = tuple(
        correlations[classes[lag][0]]
        for lag in range(CLASS_COUNT // 2)
    )
    digest = production_digest(joined, compact, target_index)
    if digest != record["production_digest"]:
        raise AssertionError(f"{label}: production digest changed")

    summary = {
        "label": label,
        "status": record["status"],
        "target": target,
        "physical_lags_replayed": len(correlations),
        "zero_nontrivial_correlations": sum(
            value == (0, 0) for value in correlations[1:]
        ),
        "shell_n9_n3_n0": (
            shell_counts[9], shell_counts[3], shell_counts[0]
        ),
        "orbit_size": len(orbit),
        "stabilizer_order": len(stabilizer),
        "canonical": joined == orbit[0],
        "production_digest": digest,
    }
    return summary, frozenset(orbit)


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["prime"] != P:
        raise AssertionError("prime changed")
    action = certificate["action"]
    if (
        action["name"], action["order"]
    ) != ("C6_x_C2A_x_C2B", GROUP_ORDER):
        raise AssertionError("profile action changed")
    classes, class_of = cyclotomic_classes(
        certificate["subgroup"], int(certificate["class_generator"])
    )

    records = certificate["profiles"]
    summaries = []
    orbits: dict[str, frozenset[tuple[int, ...]]] = {}
    for record in records:
        summary, orbit = verify_profile(record, classes, class_of)
        label = str(record["label"])
        if label in orbits:
            raise AssertionError(f"duplicate label {label}")
        summaries.append(summary)
        orbits[label] = orbit

    labels = tuple(orbits)
    pair_count = 0
    intersections = 0
    for left_index, left in enumerate(labels):
        for right in labels[left_index + 1:]:
            pair_count += 1
            intersections += len(orbits[left] & orbits[right])
    comparison = certificate["comparison"]
    status_counts = {
        status: sum(record["status"] == status for record in records)
        for status in ("reference", "new")
    }
    if (
        len(records),
        status_counts["reference"],
        status_counts["new"],
        pair_count,
        intersections,
    ) != (
        comparison["profile_count"],
        comparison["reference_profile_count"],
        comparison["new_profile_count"],
        comparison["pair_count"],
        comparison["all_pairwise_orbit_intersections"],
    ):
        raise AssertionError("pairwise comparison certificate changed")

    return {
        "profiles": summaries,
        "profile_count": len(records),
        "new_profile_count": status_counts["new"],
        "pairwise_comparisons": pair_count,
        "pairwise_orbit_intersections": intersections,
        "all_five_orbits_inequivalent": intersections == 0,
        "status": "PASS",
    }


def main() -> None:
    result = verify()
    for summary in result.pop("profiles"):
        print(
            "{label}: target={target} lags={physical_lags_replayed} "
            "nonzero_zero={zero_nontrivial_correlations} "
            "shell={shell_n9_n3_n0} orbit={orbit_size} "
            "stabilizer={stabilizer_order} canonical={canonical} "
            "digest={production_digest}".format(**summary)
        )
    for key, value in result.items():
        print(f"{key}={value}")
    print("PASS: five pairwise-inequivalent exact h=0 profile orbits")
    print("STATUS: profiles only; no labelled LP(333) or H(668)")


if __name__ == "__main__":
    main()
