#!/usr/bin/env python3
"""Resume, partition, watchdog, and SAT-stop tests for the full k=2 runner."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_k2_full_screen import (  # noqa: E402
    FAILED_SAT,
    RunControl,
    expected_shard_bytes,
    parse_shards,
    run_shard,
    shard_filename,
)
from core_completion_k2_compact import (  # noqa: E402
    HEADER_STRUCT,
    MAGIC,
    RECORD_STRUCT,
)
from core_completion_catalog_batch import sha256_file  # noqa: E402


CATALOG = ROOT / "data" / "r55_42some.g6"
CATALOG_SHA256 = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
BENCHMARK = (
    ROOT
    / "results"
    / "core_completion_catalog_k2_compact_benchmark_v1"
    / "line_001.k2scrn"
)
COVERAGE = ROOT / "verify" / "core_completion_k2_full_screen_coverage.py"
PRODUCER_SOURCE = ROOT / "src" / "core_completion_k2_compact_screen_solver.cpp"
INCLUDED_SOURCE = ROOT / "src" / "core_completion_k2_persistent_solver.cpp"
PARSER_SOURCE = ROOT / "src" / "core_completion_k2_compact.py"
RUNNER = ROOT / "src" / "core_completion_k2_full_screen.py"
EXHAUSTIVE = ROOT / "verify" / "exhaustive_verify.py"
BITSET = ROOT / "build" / "bitset_verify"
CATALOG_AUDIT = (
    ROOT / "results" / "verification" / "r55_42some_catalog_dual_check.json"
)


def balanced_shards() -> list[dict[str, int]]:
    return [
        {
            "shard": shard,
            "line_start": 1 + 82 * shard,
            "line_end": 82 + 82 * shard,
            "pair_count": 82 * 861,
            "record_bytes": 64 + 82 * 861 * 48,
        }
        for shard in range(4)
    ]


def write_synthetic_shard(
    path: Path, start: int, end: int
) -> tuple[int, str]:
    count = (end - start + 1) * 861
    payload = bytearray(
        HEADER_STRUCT.pack(
            MAGIC,
            64,
            48,
            start,
            end,
            count,
            123,
            40,
            3,
            bytes.fromhex(CATALOG_SHA256),
            b"\0" * 8,
        )
    )
    index = 0
    for line in range(start, end + 1):
        for left in range(41):
            for right in range(left + 1, 42):
                payload.extend(
                    RECORD_STRUCT.pack(
                        line,
                        left,
                        right,
                        0,
                        0,
                        780,
                        390,
                        390,
                        0,
                        0,
                        0,
                        0,
                        390,
                        390,
                        1,
                        0,
                        1,
                        0,
                        1,
                        index,
                    )
                )
                index += 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return len(payload), hashlib.sha256(payload).hexdigest()


class CoreCompletionK2FullScreenTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def make_control(self, output: Path) -> RunControl:
        return RunControl(
            output_dir=output,
            deadline=time.monotonic() + 30.0,
            output_byte_cap=50_000_000,
            reserve_bytes=0,
        )

    def test_four_balanced_shards_cover_exact_full_product(self) -> None:
        shards = parse_shards({"shards": balanced_shards()})
        self.assertEqual(len(shards), 4)
        self.assertEqual(sum(item["pair_count"] for item in shards), 282_408)
        self.assertEqual(
            sum(expected_shard_bytes(item) for item in shards),
            13_555_840,
        )

    @unittest.skipUnless(BENCHMARK.is_file(), "compact benchmark unavailable")
    def test_valid_completed_shard_is_reused_and_partial_is_preserved(
        self,
    ) -> None:
        output = self.root / "resume"
        shard = {
            "shard": 0,
            "line_start": 1,
            "line_end": 1,
            "pair_count": 861,
            "record_bytes": 41_392,
        }
        records = output / "shards" / shard_filename(shard)
        records.parent.mkdir(parents=True)
        shutil.copyfile(BENCHMARK, records)
        Path(f"{records}.partial").write_bytes(b"diagnostic prefix")
        outcome = run_shard(
            shard=shard,
            catalog=CATALOG,
            catalog_sha256=CATALOG_SHA256,
            solver=self.root / "must-not-run",
            output_dir=output,
            plan_sha256="a" * 64,
            seconds_limit=0.5,
            node_limit=100_000,
            control=self.make_control(output),
            python=Path(sys.executable),
            exhaustive_verifier=ROOT / "verify" / "exhaustive_verify.py",
            bitset_verifier=ROOT / "build" / "bitset_verify",
        )
        self.assertEqual(outcome["kind"], "COMPLETE")
        self.assertTrue(outcome["result"]["reused_validated_shard"])
        self.assertFalse(Path(f"{records}.partial").exists())
        self.assertEqual(
            len(list((output / "diagnostics").glob("*.preserved"))), 1
        )

    def test_watchdog_stops_on_output_cap(self) -> None:
        output = self.root / "watchdog"
        output.mkdir()
        control = RunControl(
            output_dir=output,
            deadline=time.monotonic() + 30.0,
            output_byte_cap=10,
            reserve_bytes=0,
        )
        thread = threading.Thread(target=control.watchdog)
        thread.start()
        (output / "too-large").write_bytes(b"x" * 11)
        thread.join(timeout=3.0)
        self.assertFalse(thread.is_alive())
        self.assertEqual(control.reason, "OUTPUT_BYTE_CAP_EXCEEDED")

    def test_sat_is_atomically_preserved_and_stops_ordinary_work(self) -> None:
        output = self.root / "sat"
        output.mkdir()
        fake = self.root / "fake-sat"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            "print(json.dumps({"
            "'record_type':'SAT','status':'SAT','catalog_line':1,"
            "'deleted_left':0,'deleted_right':1,"
            "'negative_clauses':0,'positive_clauses':0,'clauses':0,"
            "'nodes':1,'branches':0,'leaves':0,'unit_assignments':0,"
            "'max_depth':0,'elapsed_seconds':0.0,'true_variables':[]"
            "}), flush=True)\n"
            "print(json.dumps({"
            "'record_type':'SHARD','status':'SAT_STOP',"
            "'completed_records':0,'expected_records':861"
            "}), flush=True)\n"
            "raise SystemExit(10)\n",
            encoding="utf-8",
        )
        fake.chmod(0o755)
        shard = {
            "shard": 0,
            "line_start": 1,
            "line_end": 1,
            "pair_count": 861,
            "record_bytes": 41_392,
        }
        control = self.make_control(output)
        outcome = run_shard(
            shard=shard,
            catalog=CATALOG,
            catalog_sha256=CATALOG_SHA256,
            solver=fake,
            output_dir=output,
            plan_sha256="b" * 64,
            seconds_limit=0.5,
            node_limit=100_000,
            control=control,
            python=Path(sys.executable),
            exhaustive_verifier=ROOT / "verify" / "exhaustive_verify.py",
            bitset_verifier=ROOT / "build" / "bitset_verify",
        )
        self.assertEqual(outcome["kind"], "SAT")
        self.assertEqual(outcome["sat"]["classification"], FAILED_SAT)
        self.assertTrue(control.stop_event.is_set())
        self.assertTrue(
            list((output / "sat_candidates").rglob("*.model.json"))
        )
        self.assertTrue(
            list((output / "sat_candidates").rglob("*.verification.json"))
        )

    def test_independent_coverage_checker_accepts_exact_synthetic_full_set(
        self,
    ) -> None:
        output = self.root / "coverage"
        shards = balanced_shards()
        plan = {
            "catalog_sha256": CATALOG_SHA256,
            "catalog_dual_verification_sha256": sha256_file(CATALOG_AUDIT),
            "producer_source_sha256": sha256_file(PRODUCER_SOURCE),
            "included_solver_source_sha256": sha256_file(INCLUDED_SOURCE),
            "producer_binary_sha256": sha256_file(PRODUCER_SOURCE),
            "independent_parser_sha256": sha256_file(PARSER_SOURCE),
            "runner_source_sha256": sha256_file(RUNNER),
            "coverage_checker_sha256": sha256_file(COVERAGE),
            "python_executable_sha256": sha256_file(Path(sys.executable)),
            "exhaustive_sat_verifier_sha256": sha256_file(EXHAUSTIVE),
            "bitset_sat_verifier_sha256": sha256_file(BITSET),
            "jobs": 4,
            "seconds_limit_per_instance": 0.5,
            "node_limit_per_instance": 100_000,
            "max_wall_seconds": 10_800.0,
            "output_byte_cap": 50_000_000,
            "free_disk_reserve_bytes": 0,
            "expected_binary_bytes": 13_555_840,
            "worst_case_retained_output_bytes": 16_055_840,
            "shards": shards,
        }
        plan_path = self.root / "plan.json"
        plan_path.write_text(
            json.dumps(plan, sort_keys=True) + "\n", encoding="utf-8"
        )
        plan_sha256 = sha256_file(plan_path)
        results: list[dict[str, object]] = []
        for shard in shards:
            records = output / "shards" / shard_filename(shard)
            record_bytes, records_sha256 = write_synthetic_shard(
                records, shard["line_start"], shard["line_end"]
            )
            result = {
                "status": "COMPLETE",
                "shard": shard["shard"],
                "line_start": shard["line_start"],
                "line_end": shard["line_end"],
                "record_count": shard["pair_count"],
                "unsat_count": shard["pair_count"],
                "limit_count": 0,
                "record_bytes": record_bytes,
                "records_sha256": records_sha256,
                "plan_sha256": plan_sha256,
                "negative_certified_count": 0,
                "proof_generated": False,
                "proof_checked": False,
            }
            result_path = records.with_name(records.stem + ".result.json")
            result_path.write_text(
                json.dumps(result, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
            results.append(result)
        summary = {
            "status": "COMPLETE",
            "plan_sha256": plan_sha256,
            "catalog_sha256": CATALOG_SHA256,
            "jobs": 4,
            "seconds_limit_per_instance": 0.5,
            "node_limit_per_instance": 100_000,
            "max_wall_seconds": 10_800.0,
            "runtime_seconds": 1.0,
            "expected_pair_count": 282_408,
            "actual_pair_count": 282_408,
            "exact_pair_coverage": True,
            "expected_binary_bytes": 13_555_840,
            "actual_binary_bytes": 13_555_840,
            "counts": {
                "OBSERVED_UNSAT_UNCHECKED": 282_408,
                "LIMIT_NO_CONCLUSION": 0,
                "DUAL_VERIFIED_SAT_CONSTRUCTION": 0,
                "SAT_MODEL_VERIFICATION_FAILED": 0,
                "ERROR": 0,
            },
            "negative_certified_count": 0,
            "proof_generation": False,
            "proof_replay": False,
            "shards": results,
            "existing_bytes_at_launch": 0,
            "required_free_at_launch_bytes": 50_000_000,
            "free_disk_before_bytes": 50_000_000,
            "free_disk_reserve_bytes": 0,
            "output_byte_cap": 50_000_000,
        }
        summary_path = output / "summary.json"
        summary_path.write_text(
            json.dumps(summary, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        checked = subprocess.run(
            (
                sys.executable,
                str(COVERAGE),
                "--summary",
                str(summary_path),
                "--plan",
                str(plan_path),
                "--catalog",
                str(CATALOG),
                "--producer-source",
                str(PRODUCER_SOURCE),
                "--included-solver-source",
                str(INCLUDED_SOURCE),
                "--solver",
                str(PRODUCER_SOURCE),
                "--parser-source",
                str(PARSER_SOURCE),
                "--runner",
                str(RUNNER),
                "--python-executable",
                sys.executable,
                "--exhaustive-verifier",
                str(EXHAUSTIVE),
                "--bitset-verifier",
                str(BITSET),
                "--catalog-audit",
                str(CATALOG_AUDIT),
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(checked.returncode, 0, checked.stderr)
        result = json.loads(checked.stdout)
        self.assertTrue(result["valid"])
        self.assertTrue(result["exact_pair_coverage"])
        self.assertEqual(result["actual_pair_count"], 282_408)


if __name__ == "__main__":
    unittest.main()
