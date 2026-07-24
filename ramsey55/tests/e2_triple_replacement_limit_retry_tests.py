#!/usr/bin/env python3
"""Plan, target-extraction, and worker tests for the limit retry."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from core_completion_catalog_batch import parse_last_json  # noqa: E402
from core_completion_k2 import build_k2_completion_instance  # noqa: E402
from e2_triple_replacement_limit_retry import (  # noqa: E402
    extract_limit_targets,
    formula_sha256,
    induced_core_three,
    make_plan,
    validate_plan,
)
from e2_triple_replacement_limit_retry_check import run_check  # noqa: E402
from graph_io import read_graph  # noqa: E402


BASE_PLAN = (
    ROOT
    / "results"
    / "benchmark_plans"
    / "e2_triple_replacement_screen_v1.json"
)
BASE_COVERAGE = (
    ROOT
    / "results"
    / "constructive"
    / "e2_triple_replacement_screen_v1"
    / "coverage.json"
)
BASE_SHARDS = (
    ROOT
    / "results"
    / "constructive"
    / "e2_triple_replacement_screen_v1"
    / "shards"
)
CORPUS = ROOT / "data" / "e2_complement_class_representatives.g6"
PYTHON311 = Path("/opt/homebrew/opt/python@3.11/bin/python3.11")
PYSAT_ROOT = Path("/tmp/ramsey55-pysat.4YSXId")
RUNNER = ROOT / "src" / "e2_triple_replacement_limit_retry.py"
CHECKER = ROOT / "verify" / "e2_triple_replacement_limit_retry_check.py"
TESTS = ROOT / "tests" / "e2_triple_replacement_limit_retry_tests.py"
EXHAUSTIVE = ROOT / "verify" / "exhaustive_verify.py"
BITSET = ROOT / "build" / "bitset_verify"


class E2TripleLimitRetryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not (PYTHON311.exists() and PYSAT_ROOT.exists()):
            raise unittest.SkipTest("pinned Python/PySAT runtime is absent")
        cls.base_plan = json.loads(BASE_PLAN.read_text(encoding="utf-8"))
        cls.targets = extract_limit_targets(cls.base_plan, BASE_SHARDS)

    def test_exact_target_extraction(self) -> None:
        coverage = json.loads(BASE_COVERAGE.read_text(encoding="utf-8"))
        self.assertEqual(len(self.targets), coverage["totals"]["limit_count"])
        self.assertEqual(len(self.targets), 117)
        self.assertEqual(
            [target["target"] for target in self.targets],
            list(range(117)),
        )
        self.assertEqual(
            [
                (target["input_index"], target["triple_ordinal"])
                for target in self.targets
            ],
            sorted(
                (
                    target["input_index"],
                    target["triple_ordinal"],
                )
                for target in self.targets
            ),
        )

    def make_temp_plan(self, directory: Path) -> Path:
        plan_path = directory / "retry-plan.json"
        make_plan(
            plan_path=plan_path,
            base_plan_path=BASE_PLAN,
            base_coverage_path=BASE_COVERAGE,
            base_shard_dir=BASE_SHARDS,
            output_dir=(
                ROOT
                / "results"
                / "constructive"
                / "e2_triple_replacement_retry_test_unused"
            ),
            python_executable=PYTHON311,
            pysat_root=PYSAT_ROOT,
            checker=CHECKER,
            tests=TESTS,
            exhaustive=EXHAUSTIVE,
            bitset=BITSET,
            conflict_budget=10_000_000,
            worker_timeout=60,
            output_byte_cap=10_000_000,
            reserve_bytes=1,
        )
        return plan_path

    def test_plan_freezes_exact_base_limits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.make_temp_plan(Path(directory))
            plan = validate_plan(plan_path)
            self.assertEqual(plan["target_count"], 117)
            self.assertEqual(plan["targets"], self.targets)
            self.assertEqual(plan["solver"], "PySAT Cadical195")
            with self.assertRaises(FileExistsError):
                self.make_temp_plan(Path(directory))

    def test_worker_formula_and_unsat_observation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.make_temp_plan(Path(directory))
            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(PYSAT_ROOT)
            completed = subprocess.run(
                (
                    str(PYTHON311),
                    str(RUNNER),
                    "--worker",
                    "--plan",
                    str(plan_path),
                    "--target-index",
                    "0",
                ),
                text=True,
                capture_output=True,
                check=False,
                timeout=30,
                env=environment,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = parse_last_json(completed.stdout, "retry test worker")
            self.assertEqual(result["status"], "UNSAT")
            target = self.targets[0]
            adjacency = read_graph(CORPUS, target["input_index"])
            core = induced_core_three(
                adjacency, tuple(target["deleted_vertices"])
            )
            instance = build_k2_completion_instance(core)
            self.assertEqual(
                result["formula_sha256"], formula_sha256(instance.clauses)
            )
            self.assertEqual(result["clauses"], len(instance.clauses))
            self.assertFalse(result["proof_generated"])

    def test_checker_fails_closed_on_missing_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path = self.make_temp_plan(root)
            record_dir = root / "empty"
            record_dir.mkdir()
            with self.assertRaises(ValueError):
                run_check(plan_path, record_dir)


if __name__ == "__main__":
    unittest.main()
