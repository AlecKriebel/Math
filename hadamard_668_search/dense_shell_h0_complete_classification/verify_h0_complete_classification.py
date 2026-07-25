#!/usr/bin/env python3
"""Dependency-free audit of the complete dense-shell h=0 classification.

The certificate is frozen from the strict 729-shard production aggregate.
This verifier does not import the classifier or read its ignored output.  It
reconstructs the mathematical objects directly with Python integer arithmetic.
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

# ID i records the plus-counts in the three residues of an order-three class.
PROFILE_ALPHABET = (
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

# a + b*w in Z[w], w^2+w+1=0.
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


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("ascii")


def sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def raw_profile(identifier: int) -> E:
    p0, p1, p2 = PROFILE_ALPHABET[identifier]
    return p0 - p2, p1 - p2


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
        raise AssertionError("the classes do not partition F_37^*")
    return tuple(classes), tuple(class_of)


def compressed_values(
    ids_a: Sequence[int], ids_b: Sequence[int]
) -> tuple[tuple[E, ...], tuple[E, ...]]:
    result = []
    for channel, identifiers in enumerate((ids_a, ids_b)):
        if len(identifiers) != CLASS_COUNT:
            raise AssertionError("a profile word is not length twelve")
        values = [(-1, 0) if channel == 0 else (2, 0)]
        for class_index, identifier in enumerate(identifiers):
            if not 0 <= int(identifier) < len(PROFILE_ALPHABET):
                raise AssertionError("profile identifier outside alphabet")
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
        result.append(
            (values[channel][0],)
            + tuple(
                values[channel][class_of[position] + 1]
                for position in range(1, P)
            )
        )
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
        for candidate in range(len(PROFILE_ALPHABET))
        if raw_profile(candidate) == wanted
    ]
    if len(matches) != 1:
        raise AssertionError("profile conjugation is not unique")
    return matches[0]


def action_signature(group_element: int) -> tuple[tuple[int, int], ...]:
    """For each output slot return (input slot, conjugation parity)."""
    if not 0 <= group_element < GROUP_ORDER:
        raise AssertionError("group element out of range")
    rotation = group_element // 4
    result = []
    for channel in range(2):
        star = (
            bool((group_element // 2) % 2)
            if channel == 0
            else bool(group_element % 2)
        )
        offset = (2 * rotation + (6 if star else 0)) % CLASS_COUNT
        result.extend(
            (
                channel * CLASS_COUNT
                + (class_index + offset) % CLASS_COUNT,
                int(star),
            )
            for class_index in range(CLASS_COUNT)
        )
    return tuple(result)


def compose_signatures(
    left: Sequence[tuple[int, int]],
    right: Sequence[tuple[int, int]],
) -> tuple[tuple[int, int], ...]:
    """Signature of applying right first and then left."""
    return tuple(
        (
            right[source][0],
            parity ^ right[source][1],
        )
        for source, parity in left
    )


def reconstruct_action() -> tuple[tuple[int, ...], ...]:
    signatures = tuple(action_signature(group) for group in range(GROUP_ORDER))
    if len(set(signatures)) != GROUP_ORDER:
        raise AssertionError("the advertised action is not faithful")
    table = []
    for left in range(GROUP_ORDER):
        row = []
        for right in range(GROUP_ORDER):
            composed = compose_signatures(signatures[left], signatures[right])
            matches = [
                group
                for group, signature in enumerate(signatures)
                if signature == composed
            ]
            if len(matches) != 1:
                raise AssertionError("the 24 transformations are not closed")
            row.append(matches[0])
        table.append(tuple(row))
    table_tuple = tuple(table)
    if any(
        table_tuple[0][group] != group
        or table_tuple[group][0] != group
        for group in range(GROUP_ORDER)
    ):
        raise AssertionError("element zero is not the identity")
    for group in range(GROUP_ORDER):
        if not any(
            table_tuple[group][inverse] == 0
            and table_tuple[inverse][group] == 0
            for inverse in range(GROUP_ORDER)
        ):
            raise AssertionError("an action element lacks an inverse")
    for left in range(GROUP_ORDER):
        for middle in range(GROUP_ORDER):
            for right in range(GROUP_ORDER):
                if table_tuple[table_tuple[left][middle]][right] != (
                    table_tuple[left][table_tuple[middle][right]]
                ):
                    raise AssertionError("the action table is not associative")
    return table_tuple


def transform_assignment(
    identifiers: Sequence[int], group_element: int
) -> tuple[int, ...]:
    if len(identifiers) != 2 * CLASS_COUNT:
        raise AssertionError("assignment length changed")
    result = []
    for source, parity in action_signature(group_element):
        identifier = int(identifiers[source])
        result.append(
            conjugate_profile_id(identifier) if parity else identifier
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


def record_core(record: dict[str, object]) -> dict[str, object]:
    return {
        key: record[key]
        for key in (
            "label",
            "source_shards",
            "target_index",
            "target",
            "profile_ids_a",
            "profile_ids_b",
            "production_digest",
            "stabilizer_elements",
            "orbit_size",
        )
    }


def verify_profile(
    record: dict[str, object],
    classes: Sequence[Sequence[int]],
    class_of: Sequence[int],
) -> tuple[dict[str, object], frozenset[tuple[int, ...]]]:
    label = str(record["label"])
    ids_a = tuple(map(int, record["profile_ids_a"]))  # type: ignore[arg-type]
    ids_b = tuple(map(int, record["profile_ids_b"]))  # type: ignore[arg-type]
    joined = ids_a + ids_b
    target_index = int(record["target_index"])
    target = tuple(map(int, record["target"]))  # type: ignore[arg-type]
    if sha256_json(record_core(record)) != record["record_sha256"]:
        raise AssertionError(f"{label}: record hash changed")
    if not 0 <= target_index < len(TARGETS):
        raise AssertionError(f"{label}: target index out of range")
    if target != TARGETS[target_index]:
        raise AssertionError(f"{label}: target index and value disagree")

    values = compressed_values(ids_a, ids_b)
    if aggregate(values) != target:
        raise AssertionError(f"{label}: aggregate target failed")
    physical = expand_physical(values, class_of)
    correlations = physical_correlations(physical)
    if correlations[0] != (167, 0):
        raise AssertionError(f"{label}: zero-lag correlation changed")
    failed_lags = [
        lag for lag in range(1, P) if correlations[lag] != (0, 0)
    ]
    if failed_lags:
        raise AssertionError(
            f"{label}: nonzero correlations failed at {failed_lags}"
        )

    shell_counts = {
        norm: sum(
            e_norm(raw_profile(identifier)) == norm
            for identifier in joined
        )
        for norm in (0, 3, 9)
    }
    if (
        shell_counts[9], shell_counts[3], shell_counts[0]
    ) != (0, 18, 6):
        raise AssertionError(f"{label}: h=0 shell counts changed")

    images = tuple(
        transform_assignment(joined, group)
        for group in range(GROUP_ORDER)
    )
    orbit = tuple(sorted(set(images)))
    stabilizer = tuple(
        group for group, image in enumerate(images) if image == joined
    )
    if list(stabilizer) != record["stabilizer_elements"]:
        raise AssertionError(f"{label}: stabilizer changed")
    if len(orbit) != int(record["orbit_size"]):
        raise AssertionError(f"{label}: orbit size changed")
    if len(stabilizer) * len(orbit) != GROUP_ORDER:
        raise AssertionError(f"{label}: orbit-stabilizer failed")
    if joined != orbit[0]:
        raise AssertionError(f"{label}: representative is not canonical")
    if sha256_json([list(image) for image in orbit]) != record[
        "orbit_sha256"
    ]:
        raise AssertionError(f"{label}: orbit digest changed")

    replay = {
        "aggregate": list(target),
        "correlations": [list(value) for value in correlations],
        "physical_a": [list(value) for value in physical[0]],
        "physical_b": [list(value) for value in physical[1]],
    }
    if sha256_json(replay) != record["physical_replay_sha256"]:
        raise AssertionError(f"{label}: physical replay digest changed")
    compact = tuple(
        correlations[classes[index][0]]
        for index in range(CLASS_COUNT // 2)
    )
    digest = production_digest(joined, compact, target_index)
    if digest != record["production_digest"]:
        raise AssertionError(f"{label}: production digest changed")

    return (
        {
            "label": label,
            "digest": digest,
            "target_index": target_index,
            "orbit_size": len(orbit),
            "stabilizer_order": len(stabilizer),
            "physical_lags_replayed": len(correlations),
        },
        frozenset(orbit),
    )


def verify_census(
    census: dict[str, object],
    records: Sequence[dict[str, object]],
    orbit_weight: int,
) -> None:
    if sha256_json(
        {key: value for key, value in census.items() if key != "semantic_sha256"}
    ) != census["semantic_sha256"]:
        raise AssertionError("census semantic hash changed")
    expected = {
        "aggregate_file_sha256":
            "3bccde87f456bfcd2f0c3da6ac8cf9cb3635538e831a95951003068ae87cae86",
        "manifest_file_sha256":
            "690cdc3836fc0dcd9d465ad88ad4b39ab0eede899202ea8acf7e9a8366129973",
        "source_sha256":
            "ef7c77598396c1050d13848b5fde536eba4e8b1426c6554705a1015fbc7f3404",
        "binary_sha256":
            "17f635cda50e487ed23b77b34e08a3f0ebf207a15d3f86a204f3d3ddc6f809de",
        "prefix_shards": 729,
        "complete": True,
        "upper_exact_scope": "char2_mod9_intersection",
        "burnside_weighted_partition_check": "PASS",
        "retained_witnesses_independently_replayed": 152,
        "retained_exact_orbits_across_shards": 18,
        "distinct_canonical_exact_profile_orbits": 18,
        "status": "PASS: every required prefix shard is complete",
    }
    for key, value in expected.items():
        if census.get(key) != value:
            raise AssertionError(f"census field {key} changed")
    if census["prefix_shards"] != 27 * 27:
        raise AssertionError("the prefix grid is not 27 by 27")

    counters = census["counters"]
    pinned_counters = {
        "affine_aggregate_hits": 707978968614,
        "canonical_decorations_processed": 1999128,
        "canonical_decorations_seen": 1999128,
        "char2_hits": 14639544,
        "char2_mod9_hits": 19986,
        "char2_post_mod9_lambda_hits": 64,
        "detached_replays": 20004,
        "exact_target_hits": 29984637430,
        "exact_zero_hits": 18,
        "high_phase_cases": 1999128,
        "mod27_hits": 18,
        "mod9_hits": 41152428,
        "post_mod9_lambda_hits": 64,
        "primitive_flag_phase_leaves": 1062513179946,
        "raw_decorations_seen": 47730304,
        "raw_skeletons_seen": 47730304,
        "rejected_local_phase_cases": 37274,
        "weighted_affine_aggregate_hits": 16919114399712,
        "weighted_char2_hits": 349534344,
        "weighted_decorations_processed": 47730304,
        "weighted_exact_target_hits": 715870991160,
        "weighted_exact_zero_hits": 360,
        "weighted_mod9_hits": 982368720,
        "weighted_post_mod9_lambda_hits": 1464,
        "weighted_primitive_flag_phase_leaves": 25368365895696,
    }
    if counters != pinned_counters:
        raise AssertionError("global production counters changed")
    diagnostics = {
        "diagnostic_assignment_idlex_mod9_hits": 711550,
        "diagnostic_weighted_assignment_idlex_mod9_hits": 17072040,
    }
    if census["diagnostic_counters"] != diagnostics:
        raise AssertionError("global diagnostic counters changed")
    if counters["canonical_decorations_seen"] != (
        counters["canonical_decorations_processed"]
    ):
        raise AssertionError("a canonical decoration was skipped")
    if counters["raw_decorations_seen"] != (
        counters["weighted_decorations_processed"]
    ):
        raise AssertionError("Burnside weighted decoration total failed")
    if counters["exact_zero_hits"] != len(records):
        raise AssertionError("canonical exact-hit count disagrees")
    if counters["weighted_exact_zero_hits"] != orbit_weight:
        raise AssertionError("weighted exact hits disagree with orbit sizes")
    if counters["mod27_hits"] != counters["exact_zero_hits"]:
        raise AssertionError("mod-27/exact accounting changed")
    if counters["post_mod9_lambda_hits"] < counters["exact_zero_hits"]:
        raise AssertionError("post-mod-9/exact accounting changed")


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["schema"] != (
        "h668-dense-shell-h0-complete-classification-v1"
    ):
        raise AssertionError("certificate schema changed")
    if certificate["prime"] != P:
        raise AssertionError("prime changed")
    classes, class_of = cyclotomic_classes(
        certificate["subgroup"], int(certificate["class_generator"])
    )

    action = certificate["action"]
    if (
        action["name"], action["order"]
    ) != ("C6_x_C2A_x_C2B", GROUP_ORDER):
        raise AssertionError("action metadata changed")
    table = reconstruct_action()
    if sha256_json([list(row) for row in table]) != action[
        "multiplication_table_sha256"
    ]:
        raise AssertionError("action multiplication-table digest changed")

    records = certificate["profiles"]
    if len(records) != 18:
        raise AssertionError("the frozen profile count is not eighteen")
    keys = [
        (
            tuple(record["profile_ids_a"]) + tuple(record["profile_ids_b"]),
            int(record["target_index"]),
        )
        for record in records
    ]
    if any(left >= right for left, right in zip(keys, keys[1:])):
        raise AssertionError("profile representatives are not strictly sorted")
    if len({record["label"] for record in records}) != len(records):
        raise AssertionError("profile labels are not unique")
    if len({record["production_digest"] for record in records}) != len(records):
        raise AssertionError("production digests are not unique")

    summaries = []
    orbits = []
    for record in records:
        summary, orbit = verify_profile(record, classes, class_of)
        summaries.append(summary)
        orbits.append(orbit)
    intersections = 0
    pair_count = 0
    for left in range(len(orbits)):
        for right in range(left + 1, len(orbits)):
            pair_count += 1
            intersections += len(orbits[left] & orbits[right])
    if pair_count != 153 or intersections:
        raise AssertionError("the 18 representatives are not inequivalent")

    orbit_weight = sum(summary["orbit_size"] for summary in summaries)
    verify_census(certificate["census"], records, orbit_weight)
    if sha256_json([record_core(record) for record in records]) != certificate[
        "profile_table_sha256"
    ]:
        raise AssertionError("profile-table digest changed")
    return {
        "status": "PASS",
        "profiles": summaries,
        "profile_count": len(records),
        "pairwise_comparisons": pair_count,
        "pairwise_orbit_intersections": intersections,
        "weighted_orbit_size": orbit_weight,
        "physical_correlations_replayed": len(records) * P,
        "prefix_shards_certified_by_provenance": 729,
    }


def main() -> None:
    result = verify()
    for summary in result.pop("profiles"):
        print(
            "{label}: digest={digest} target={target_index} "
            "orbit={orbit_size} stabilizer={stabilizer_order} "
            "lags={physical_lags_replayed}".format(**summary)
        )
    for key, value in result.items():
        print(f"{key}={value}")
    print("PASS: complete 18-orbit dense-shell h=0 classification")
    print("STATUS: profile classification only; not an LP(333) or H(668)")


if __name__ == "__main__":
    main()
