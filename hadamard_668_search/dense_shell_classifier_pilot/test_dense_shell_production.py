#!/usr/bin/env python3
"""Regression tests for resumable dense-shell production infrastructure."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from production_common import (  # noqa: E402
    BURNSIDE,
    EXPECTED_WORKLOAD,
    PREFIX_COUNT,
    parse_key_value_output,
    partition_audit,
    workload_audit,
)
from production_orbits import (  # noqa: E402
    validate_exact_orbit_output,
)
from run_dense_shell_production import (  # noqa: E402
    Active,
    BUILD_FLAGS,
    Job,
    aggregate_child_rss_mib,
    cleanup_active,
    validate_result as validate_runner_result,
)
from aggregate_dense_shell_production import (  # noqa: E402
    validate_result_record as validate_aggregate_result,
)


RUNNER = HERE / "run_dense_shell_production.py"
AGGREGATOR = HERE / "aggregate_dense_shell_production.py"


class DenseShellProductionTest(unittest.TestCase):
    def test_exact_prefix_partition_and_residue_workload(self) -> None:
        partition = partition_audit()
        workload = workload_audit()
        for shell in ("h1", "h0"):
            row = partition["shells"][shell]
            self.assertEqual(row["prefix_count"], PREFIX_COUNT)
            self.assertEqual(
                row["raw_skeletons"],
                BURNSIDE[shell]["raw_skeletons"],
            )
            self.assertEqual(
                row["raw_decorations"],
                BURNSIDE[shell]["raw_decorations"],
            )
            self.assertEqual(
                row["canonical_decorations"],
                BURNSIDE[shell]["canonical_decorations"],
            )
            for key, expected in EXPECTED_WORKLOAD[shell].items():
                self.assertEqual(
                    workload["shells"][shell][key], expected
                )
        self.assertEqual(
            workload["combined_residue_union_affine_upper"],
            47_855_051_781_696,
        )
        self.assertEqual(
            workload["combined_primitive_leaf_upper"],
            71_779_465_554_048,
        )

    def test_zero_prefix_runner_is_atomic_and_resumable(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="h668-production-smoke-"
        ) as raw:
            output = Path(raw) / "production"
            command = [
                sys.executable,
                str(RUNNER),
                "--output",
                str(output),
                "--shell",
                "h0",
                "--prefix",
                "13",
                "13",
                "--workers",
                "1",
            ]
            first = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertIn("complete h0-p13-p13", first.stdout)
            result_path = output / "results" / "h0-p13-p13.json"
            result = json.loads(result_path.read_text())
            parsed = result["parsed"]
            self.assertEqual(
                parsed["schema"],
                "dense-shell-production-shard-v2",
            )
            self.assertEqual(parsed["shard_complete"], "1")
            self.assertEqual(parsed["exact_orbit_mode"], "enumerate")
            self.assertEqual(
                parsed["exact_orbit_collection"], "complete_shard"
            )
            self.assertEqual(parsed["exact_orbit_count"], "0")
            self.assertEqual(parsed["raw_skeletons_seen"], "0")
            self.assertEqual(
                parsed["upper_exact_scope"],
                "char2_mod9_intersection",
            )
            original_bytes = result_path.read_bytes()
            original_mtime = result_path.stat().st_mtime_ns

            second = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertIn("1 already complete", second.stdout)
            self.assertEqual(result_path.read_bytes(), original_bytes)
            self.assertEqual(
                result_path.stat().st_mtime_ns, original_mtime
            )

            manifest = json.loads(
                (output / "manifest.json").read_text()
            )
            self.assertEqual(
                manifest["schema"],
                "dense-shell-production-manifest-v2",
            )
            self.assertEqual(
                manifest["exact_orbit_policy"]["mode"],
                "exhaustive_per_prefix_shard",
            )
            self.assertIn(
                "--enumerate-exact-orbits",
                manifest["production_command_template"],
            )
            self.assertEqual(
                manifest["build_provenance"]["flags"],
                list(BUILD_FLAGS),
            )
            self.assertEqual(
                len(
                    manifest["build_provenance"][
                        "cache_key_sha256"
                    ]
                ),
                64,
            )
            binary = Path(manifest["binary_path"])
            for shell in ("h1", "h0"):
                census = subprocess.run(
                    [
                        str(binary),
                        "--shell",
                        shell,
                        "--count-decorations",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                data = parse_key_value_output(census.stdout)
                row = partition_audit((shell,))["shells"][shell]
                self.assertEqual(
                    int(data["raw_skeletons"]),
                    row["raw_skeletons"],
                )
                self.assertEqual(
                    int(data["raw_decorations"]),
                    row["raw_decorations"],
                )
                self.assertEqual(
                    int(data["canonical_decorations"]),
                    row["canonical_decorations"],
                )

            incomplete = subprocess.run(
                [
                    sys.executable,
                    str(AGGREGATOR),
                    "--output",
                    str(output),
                    "--shell",
                    "h0",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertNotEqual(incomplete.returncode, 0)
            self.assertIn(
                "result set mismatch",
                incomplete.stdout + incomplete.stderr,
            )

    def test_complete_shard_rejects_skip_semantics(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="h668-production-cli-"
        ) as raw:
            binary = Path(raw) / "classifier"
            subprocess.run(
                [
                    "clang++",
                    "-O2",
                    "-std=c++20",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    str(HERE / "dense_shell_classifier_pilot.cpp"),
                    "-o",
                    str(binary),
                ],
                check=True,
                timeout=120,
            )
            rejected = subprocess.run(
                [
                    str(binary),
                    "--shell",
                    "h0",
                    "--complete-shard",
                    "--enumerate-exact-orbits",
                    "--prefix",
                    "13",
                    "13",
                    "--skip",
                    "1",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertNotIn("shard_complete=1", rejected.stdout)

    def test_v1_output_fails_closed_before_compilation(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="h668-production-v1-boundary-"
        ) as raw:
            output = Path(raw) / "production"
            candidate = output / "candidates" / "h0-p00-p05.json"
            candidate.parent.mkdir(parents=True)
            manifest = output / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema":
                            "dense-shell-production-manifest-v1",
                        "runner_version":
                            "dense-shell-production-runner-v1",
                        "source_sha256": "old-source",
                    }
                )
            )
            candidate.write_text("frozen raw candidate\n")
            before = {
                path.relative_to(output): path.read_bytes()
                for path in output.rglob("*")
                if path.is_file()
            }
            rejected = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--output",
                    str(output),
                    "--shell",
                    "h0",
                    "--prefix",
                    "13",
                    "13",
                    "--workers",
                    "1",
                    "--dry-run",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn(
                "incompatible provenance line",
                rejected.stdout + rejected.stderr,
            )
            after = {
                path.relative_to(output): path.read_bytes()
                for path in output.rglob("*")
                if path.is_file()
            }
            self.assertEqual(after, before)
            self.assertFalse((output / "bin").exists())

    def test_nontrivial_prefix_replays_only_joint_gate(self) -> None:
        """Pin a complete positive-work shard and its replay scope."""

        with tempfile.TemporaryDirectory(
            prefix="h668-production-replay-scope-"
        ) as raw:
            binary = Path(raw) / "classifier"
            subprocess.run(
                [
                    "clang++",
                    "-O3",
                    "-DNDEBUG",
                    "-std=c++20",
                    "-Wall",
                    "-Wextra",
                    "-Wpedantic",
                    "-Werror",
                    str(HERE / "dense_shell_classifier_pilot.cpp"),
                    "-o",
                    str(binary),
                ],
                check=True,
                timeout=120,
            )
            completed = subprocess.run(
                [
                    str(binary),
                    "--shell",
                    "h0",
                    "--complete-shard",
                    "--enumerate-exact-orbits",
                    "--prefix",
                    "1",
                    "13",
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            parsed = parse_key_value_output(completed.stdout)
            expected = {
                "shard_id": "h0-p01-p13",
                "upper_exact_scope": "char2_mod9_intersection",
                "raw_skeletons_seen": "1296",
                "canonical_decorations_processed": "42",
                "primitive_flag_phase_leaves": "19131876",
                "exact_target_hits": "554761",
                "char2_hits": "284",
                "mod9_hits": "753",
                "char2_mod9_hits": "0",
                "detached_replays": "0",
                "post_mod9_lambda_hits": "0",
                "mod27_hits": "0",
                "exact_zero_hits": "0",
                "witness_char2_mod9_present": "0",
                "witness_post_mod9_lambda_present": "0",
                "witness_exact_present": "0",
                "exact_orbit_mode": "enumerate",
                "exact_orbit_collection": "complete_shard",
                "exact_orbit_count": "0",
                "shard_complete": "1",
            }
            for key, value in expected.items():
                self.assertEqual(parsed[key], value)

    def test_discovered_exact_prefix_enumerates_canonical_orbit(
        self,
    ) -> None:
        """Exercise census retention on the independently certified hit."""

        with tempfile.TemporaryDirectory(
            prefix="h668-production-exact-orbit-"
        ) as raw:
            binary = Path(raw) / "classifier"
            subprocess.run(
                [
                    "clang++",
                    "-O3",
                    "-DNDEBUG",
                    "-std=c++20",
                    "-Wall",
                    "-Wextra",
                    "-Wpedantic",
                    "-Werror",
                    str(HERE / "dense_shell_classifier_pilot.cpp"),
                    "-o",
                    str(binary),
                ],
                check=True,
                timeout=120,
            )
            command = [
                str(binary),
                "--shell",
                "h0",
                "--prefix",
                "0",
                "5",
                "--skip",
                "35879",
                "--limit",
                "2",
                "--enumerate-exact-orbits",
            ]
            outputs = []
            for _ in range(2):
                completed = subprocess.run(
                    command,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                outputs.append(
                    parse_key_value_output(completed.stdout)
                )
            first, second = outputs
            exact_keys = {
                key
                for key in first
                if key.startswith("exact_orbit_")
                or key.startswith("witness_exact_")
            }
            self.assertEqual(
                {key: first[key] for key in exact_keys},
                {key: second[key] for key in exact_keys},
            )
            self.assertEqual(first["exact_zero_hits"], "1")
            self.assertEqual(first["exact_orbit_count"], "1")
            self.assertEqual(
                first["canonical_decorations_processed"], "2"
            )
            self.assertEqual(
                first["exact_orbit_000000_digest"],
                "0x7395e771c01b49bf",
            )
            self.assertEqual(
                first["exact_orbit_000000_ids_a"],
                "1,2,6,1,5,1,4,5,1,5,7,4",
            )
            self.assertEqual(
                first["exact_orbit_000000_ids_b"],
                "2,4,2,4,4,6,5,5,8,1,5,8",
            )
            orbits = validate_exact_orbit_output(
                first, "h0", expected_collection="bounded_stream"
            )
            self.assertEqual(len(orbits), 1)
            self.assertEqual(orbits[0].target_index, 3)

            corrupted = dict(first)
            corrupted["exact_orbit_000000_digest"] = "0x0"
            with self.assertRaises(ValueError):
                validate_exact_orbit_output(
                    corrupted,
                    "h0",
                    expected_collection="bounded_stream",
                )

            stopped = subprocess.run(
                [
                    str(binary),
                    "--shell",
                    "h0",
                    "--prefix",
                    "0",
                    "5",
                    "--skip",
                    "35879",
                    "--limit",
                    "2",
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            stopped_output = parse_key_value_output(stopped.stdout)
            self.assertEqual(
                stopped_output["exact_orbit_mode"], "stop_on_first"
            )
            self.assertEqual(
                stopped_output["canonical_decorations_processed"], "1"
            )
            self.assertEqual(stopped_output["exact_orbit_count"], "0")
            self.assertEqual(
                stopped_output["witness_exact_digest"],
                "0x7395e771c01b49bf",
            )

            production = dict(first)
            production.update(
                {
                    "schema": "dense-shell-production-shard-v2",
                    "mode": "complete_shard",
                    "shell": "h0",
                    "shard_id": "h0-p00-p05",
                    "prefix_first": "0",
                    "prefix_second": "5",
                    "upper_exact_scope":
                        "char2_mod9_intersection",
                    "shard_complete": "1",
                    "exact_orbit_collection": "complete_shard",
                }
            )
            transcript = "".join(
                f"{key}={value}\n"
                for key, value in production.items()
            )
            fake_binary = str(Path(raw) / "classifier")
            production_command = [
                fake_binary,
                "--shell",
                "h0",
                "--complete-shard",
                "--enumerate-exact-orbits",
                "--prefix",
                "0",
                "5",
            ]
            record = {
                "schema": "dense-shell-production-result-v2",
                "runner_version":
                    "dense-shell-production-runner-v2",
                "shard_id": "h0-p00-p05",
                "shell": "h0",
                "prefix_first": 0,
                "prefix_second": 5,
                "source_sha256": "source",
                "binary_sha256": "binary",
                "command": production_command,
                "returncode": 0,
                "complete": True,
                "candidate": False,
                "parsed": production,
                "transcript": transcript,
            }
            validate_runner_result(
                record,
                shell="h0",
                first=0,
                second=5,
                source_hash="source",
                binary_hash="binary",
                command=production_command,
            )
            _, aggregate_orbits = validate_aggregate_result(
                record,
                path=Path(raw) / "synthetic-result.json",
                shell="h0",
                first=0,
                second=5,
                manifest={
                    "binary_path": fake_binary,
                    "source_sha256": "source",
                    "binary_sha256": "binary",
                },
            )
            self.assertEqual(aggregate_orbits, orbits)

    def test_cleanup_terminates_owned_children(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="h668-production-cleanup-"
        ) as raw:
            transcript = Path(raw) / "active.transcript"
            with transcript.open("wb") as stream:
                process = subprocess.Popen(
                    [sys.executable, "-c", "import time; time.sleep(30)"],
                    stdout=stream,
                    stderr=subprocess.STDOUT,
                )
            job = Job(
                shell="h0",
                first=13,
                second=13,
                result_path=Path(raw) / "unused.json",
                command=["unused"],
                workload_proxy=0,
            )
            active = {
                process.pid: Active(
                    job=job,
                    process=process,
                    transcript=transcript,
                    started=0.0,
                )
            }
            self.assertGreater(aggregate_child_rss_mib(active), 0)
            cleanup_active(active)
            self.assertEqual(active, {})
            self.assertIsNotNone(process.poll())
            self.assertFalse(transcript.exists())


if __name__ == "__main__":
    unittest.main()
