#!/usr/bin/env python3
"""Independently verify the second exact dense-shell h=0 profile orbit."""

from __future__ import annotations

import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
REFERENCE = PARENT / "dense_shell_exact_profile_h0"
sys.path.insert(0, str(REFERENCE))

import verify_exact_profile_h0 as algebra  # noqa: E402


CERTIFICATE = HERE / "certificate.json"
FIRST_CERTIFICATE = REFERENCE / "certificate.json"


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
    if algebra.sha256_json(core) != certificate["semantic_sha256"]:
        raise AssertionError("semantic certificate hash changed")
    if certificate["prime"] != algebra.P:
        raise AssertionError("prime changed")

    ids_a = tuple(map(int, certificate["profile_ids_a"]))
    ids_b = tuple(map(int, certificate["profile_ids_b"]))
    joined = ids_a + ids_b
    target = tuple(map(int, certificate["target"]))
    target_index = int(certificate["target_index"])
    if algebra.TARGETS[target_index] != target:
        raise AssertionError("target index and target disagree")

    classes, class_of = algebra.cyclotomic_classes(
        certificate["subgroup"], int(certificate["class_generator"])
    )
    values = algebra.compressed_values(ids_a, ids_b)
    if algebra.aggregate(values) != target:
        raise AssertionError("aggregate target failed")
    physical = algebra.expand_physical(values, class_of)
    correlations = algebra.physical_correlations(physical)
    if correlations[0] != (167, 0):
        raise AssertionError("zero-lag energy changed")
    if any(value != (0, 0) for value in correlations[1:]):
        raise AssertionError("a nonzero physical lag failed")

    shell_counts = {
        norm: sum(
            algebra.e_norm(algebra.raw_profile(identifier)) == norm
            for identifier in joined
        )
        for norm in (0, 3, 9)
    }
    expected_shell = certificate["shell"]
    if (
        shell_counts[9],
        shell_counts[3],
        shell_counts[0],
    ) != (
        expected_shell["norm_9_profiles"],
        expected_shell["norm_3_profiles"],
        expected_shell["norm_0_profiles"],
    ):
        raise AssertionError("shell census changed")

    images = tuple(
        algebra.transform_assignment(joined, group)
        for group in range(algebra.GROUP_ORDER)
    )
    orbit = tuple(sorted(set(images)))
    stabilizer = tuple(
        group for group, image in enumerate(images) if image == joined
    )
    expected_group = certificate["group"]
    if (
        len(orbit),
        len(stabilizer),
        list(stabilizer),
        joined == orbit[0],
    ) != (
        expected_group["orbit_size"],
        expected_group["stabilizer_order"],
        expected_group["stabilizer_elements"],
        expected_group["canonical"],
    ):
        raise AssertionError("orbit/stabilizer certificate changed")
    if algebra.sha256_json([list(image) for image in orbit]) != certificate[
        "orbit_sha256"
    ]:
        raise AssertionError("orbit hash changed")

    first = json.loads(FIRST_CERTIFICATE.read_text(encoding="utf-8"))
    first_joined = tuple(first["profile_ids_a"] + first["profile_ids_b"])
    first_orbit = {
        algebra.transform_assignment(first_joined, group)
        for group in range(algebra.GROUP_ORDER)
    }
    if set(orbit) & first_orbit:
        raise AssertionError("the two claimed profile orbits intersect")

    replay = {
        "aggregate": list(target),
        "correlations": [list(value) for value in correlations],
        "physical_a": [list(value) for value in physical[0]],
        "physical_b": [list(value) for value in physical[1]],
    }
    if algebra.sha256_json(replay) != certificate[
        "physical_replay_sha256"
    ]:
        raise AssertionError("physical replay hash changed")
    compact = tuple(
        correlations[classes[lag][0]]
        for lag in range(algebra.CLASS_COUNT // 2)
    )
    digest = algebra.production_digest(joined, compact, target_index)
    if digest != certificate["production_digest"]:
        raise AssertionError("production digest changed")

    return {
        "target": target,
        "physical_lags_replayed": len(correlations),
        "zero_nontrivial_correlations": sum(
            value == (0, 0) for value in correlations[1:]
        ),
        "shell_n9_n3_n0": (
            shell_counts[9],
            shell_counts[3],
            shell_counts[0],
        ),
        "orbit_size": len(orbit),
        "stabilizer_order": len(stabilizer),
        "canonical": joined == orbit[0],
        "disjoint_from_first_h0_orbit": True,
        "production_digest": digest,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}={value}")
    print("PASS: independent all-37 replay of second exact h=0 orbit")
