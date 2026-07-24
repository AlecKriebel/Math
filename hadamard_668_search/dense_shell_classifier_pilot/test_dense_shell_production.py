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
from run_dense_shell_production import (  # noqa: E402
    Active,
    BUILD_FLAGS,
    Job,
    aggregate_child_rss_mib,
    cleanup_active,
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
                "dense-shell-production-shard-v1",
            )
            self.assertEqual(parsed["shard_complete"], "1")
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
