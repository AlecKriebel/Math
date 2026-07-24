#!/usr/bin/env python3
"""Tests for the non-certifying full catalog screen."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_screen import (  # noqa: E402
    OBSERVED_UNSAT,
    screen_instance,
)


CATALOG = ROOT / "data" / "r55_42some.g6"
SOURCE = ROOT / "src" / "core_completion_proof_solver.cpp"
COVERAGE = ROOT / "verify" / "core_completion_catalog_screen_coverage.py"


class CoreCompletionCatalogScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        compiler = shutil.which("clang++") or shutil.which("c++")
        if compiler is None:
            raise unittest.SkipTest("no C++17 compiler available")
        cls.temporary = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temporary.name)
        cls.solver = cls.root / "solver"
        compiled = subprocess.run(
            (
                compiler,
                "-O2",
                "-std=c++17",
                str(SOURCE),
                "-o",
                str(cls.solver),
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        if compiled.returncode:
            raise AssertionError(compiled.stderr)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def make_one_record(
        self, name: str
    ) -> tuple[Path, dict[str, object]]:
        output = self.root / name
        return output, screen_instance(
            (1, 0),
            catalog=CATALOG,
            catalog_sha256=hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
            solver=self.solver,
            solver_sha256=hashlib.sha256(self.solver.read_bytes()).hexdigest(),
            output_dir=output,
            seconds_limit=10.0,
            node_limit=1_000_000,
            python=Path(sys.executable),
            exhaustive_verifier=ROOT / "verify" / "exhaustive_verify.py",
            bitset_verifier=ROOT / "build" / "bitset_verify",
        )

    def test_unsat_screen_is_explicitly_unchecked(self) -> None:
        output, result = self.make_one_record("unchecked")
        self.assertEqual(result["classification"], OBSERVED_UNSAT)
        self.assertEqual(
            result["evidence_category"],
            "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        )
        self.assertFalse(result["negative_certified"])
        self.assertFalse(result["proof_generated"])
        self.assertFalse(result["proof_checked"])
        self.assertFalse(any(output.rglob("*.bin")))

    def test_coverage_checker_rejects_one_of_13776(self) -> None:
        output, _ = self.make_one_record("incomplete")
        record = json.loads(
            next((output / "records").rglob("*.json")).read_text(
                encoding="utf-8"
            )
        )
        summary = self.root / "incomplete_summary.json"
        summary.write_text(
            json.dumps({"instances": [record]}) + "\n",
            encoding="utf-8",
        )
        checked = subprocess.run(
            (
                sys.executable,
                str(COVERAGE),
                "--summary",
                str(summary),
                "--catalog",
                str(CATALOG),
                "--solver",
                str(self.solver),
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(checked.returncode, 0)
        result = json.loads(checked.stdout)
        self.assertFalse(result["coverage_valid"])
        self.assertEqual(result["actual_pair_count"], 1)
        self.assertEqual(result["expected_pair_count"], 13_776)


if __name__ == "__main__":
    unittest.main()
