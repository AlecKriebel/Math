#!/usr/bin/env python3
"""Verify the connected dense-shell character/classifier audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
PILOT = HERE.parent / "dense_shell_classifier_pilot"
AUDIT_CPP = HERE / "audit_dense_shell_e2e.cpp"
CLASSIFIER_CPP = PILOT / "dense_shell_classifier_pilot.cpp"
RESULTS = HERE / "benchmark_results.json"

sys.path.insert(0, str(PILOT))
from production_common import parse_key_value_output  # noqa: E402
from verify_dense_shell_classifier_pilot import replay_witness  # noqa: E402


FLAGS = (
    "-O3",
    "-DNDEBUG",
    "-std=c++20",
    "-Wall",
    "-Wextra",
    "-Wpedantic",
    "-Werror",
)


def require(actual: dict[str, str], expected: dict[str, str]) -> None:
    for key, value in expected.items():
        if actual.get(key) != value:
            raise AssertionError(
                f"{key}: {actual.get(key)!r} != {value!r}"
            )


def compile_cpp(source: Path, output: Path) -> None:
    subprocess.run(
        ["clang++", *FLAGS, str(source), "-o", str(output)],
        check=True,
        timeout=120,
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run_parsed(command: list[str], timeout: int = 60) -> dict[str, str]:
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return parse_key_value_output(completed.stdout)


def verify() -> dict[str, int | str]:
    measurements = json.loads(RESULTS.read_text(encoding="utf-8"))
    if measurements.get("schema") != "dense-shell-e2e-benchmark-v2":
        raise AssertionError("benchmark result schema changed")
    source_hashes = measurements["source_sha256"]
    if source_hashes["classifier_v2_enumeration"] != sha256(CLASSIFIER_CPP):
        raise AssertionError("classifier source/measurement hash mismatch")
    if source_hashes["connected_audit"] != sha256(AUDIT_CPP):
        raise AssertionError("audit source/measurement hash mismatch")
    if (
        measurements["replay_scope_after_fix"]["detached_replays"] != 0
        or measurements["connected_actual_character_audit"][
            "actual_mod9_zero_fiber"
        ]
        != 729
        or measurements["v2_single_rate_projection"][
            "combined_single_core_hours"
        ]
        != 51.71744770044008
    ):
        raise AssertionError("benchmark result certificate changed")

    with tempfile.TemporaryDirectory(prefix="h668-dense-e2e-") as raw:
        temporary = Path(raw)
        audit_binary = temporary / "audit"
        classifier_binary = temporary / "classifier"
        compile_cpp(AUDIT_CPP, audit_binary)
        compile_cpp(CLASSIFIER_CPP, classifier_binary)

        audit = run_parsed([str(audit_binary)])
        require(
            audit,
            {
                "schema": "dense-shell-e2e-audit-v1",
                "status": "PASS",
                "shell": "h0",
                "prefix_first": "1",
                "prefix_second": "13",
                "legal_local_states": "27",
                "raw_skeletons": "1296",
                "canonical_decorations": "42",
                "weighted_canonical_decorations": "600",
                "selected_decoration_orbit": "24",
                "support_mask": "15978365",
                "support_cell": "5,12,12,0",
                "lower_affine_dimension": "12",
                "lower_affine_points": "531441",
                "actual_mod9_zero_fiber": "729",
                "benchmark_polar_differences": "459",
                "exact_target_points": "21702",
                "exact_target_mod9_points": "34",
                "exact_target_post_mod9_points": "1",
                "character_evaluations": "729",
                "character_inversion_fibers": "729",
                "actual_family_benchmark_evaluations": "11943936",
                "actual_family_benchmark_checksum": "0x733d190d92918655",
                "recovered_target": "2",
                "recovered_digest": "0xc8ac157d026d3025",
                "recovered_assignment_orbit": "24",
            },
        )

        production = run_parsed(
            [
                str(classifier_binary),
                "--shell",
                "h0",
                "--complete-shard",
                "--prefix",
                "1",
                "13",
                "--enumerate-exact-orbits",
            ]
        )
        require(
            production,
            {
                "schema": "dense-shell-production-shard-v2",
                "shard_id": "h0-p01-p13",
                "raw_skeletons_seen": "1296",
                "canonical_decorations_processed": "42",
                "weighted_decorations_processed": "600",
                "primitive_flag_phase_leaves": "19131876",
                "affine_aggregate_hits": "13817466",
                "exact_target_hits": "554761",
                "char2_hits": "284",
                "mod9_hits": "753",
                "char2_mod9_hits": "0",
                "detached_replays": "0",
                "post_mod9_lambda_hits": "0",
                "exact_zero_hits": "0",
                "exact_orbit_mode": "enumerate",
                "exact_orbit_count": "0",
                "shard_complete": "1",
            },
        )

        bounded = run_parsed(
            [
                str(classifier_binary),
                "--shell",
                "h0",
                "--prefix",
                "1",
                "13",
                "--limit",
                "42",
            ]
        )
        for key in (
            "raw_skeletons_seen",
            "canonical_decorations_processed",
            "weighted_decorations_processed",
            "primitive_flag_phase_leaves",
            "affine_aggregate_hits",
            "exact_target_hits",
            "char2_hits",
            "mod9_hits",
            "char2_mod9_hits",
        ):
            if bounded[key] != production[key]:
                raise AssertionError(f"bounded/production {key} mismatch")
        require(
            bounded,
            {
                "detached_replays": "755",
                "post_mod9_lambda_hits": "7",
                "exact_zero_hits": "0",
                "witness_post_mod9_lambda_present": "1",
                "witness_post_mod9_lambda_target_index": "2",
                "witness_post_mod9_lambda_digest": "0xc8ac157d026d3025",
                "witness_post_mod9_lambda_exact_zero": "0",
            },
        )
        replay_witness(bounded, "witness_post_mod9_lambda", "h0")

    print("PASS: connected dense-shell end-to-end audit")
    print("prefix=h0-p01-p13")
    print("raw_skeletons=1296")
    print("canonical_decorations=42")
    print("actual_mod9_zero_fiber=729")
    print("exact_target_post_mod9_points=1")
    print("benchmark_polar_differences=459")
    print("production_detached_replays=0")
    return {
        "status": "PASS",
        "prefix": "h0-p01-p13",
        "raw_skeletons": 1296,
        "canonical_decorations": 42,
        "actual_mod9_zero_fiber": 729,
        "exact_target_post_mod9_points": 1,
        "benchmark_polar_differences": 459,
        "production_detached_replays": 0,
    }


if __name__ == "__main__":
    verify()
