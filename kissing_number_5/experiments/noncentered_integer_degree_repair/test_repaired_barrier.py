#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from experiments.noncentered_integer_degree_repair.verify_repaired_barrier import (
    VerificationError,
    verify,
)


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "candidate_exact_6.json"
ALL = HERE / "all_harmonics_certificate_6.json"
MIXTURE = HERE / "integer_row_mixture_6.json"
ROOT = Path(__file__).resolve().parents[2]
SCRIPT = HERE / "verify_repaired_barrier.py"


class RepairedBarrierTest(unittest.TestCase):
    def run_optimized(
        self, all_harmonics: Path = ALL
    ) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(ROOT)
        return subprocess.run(
            [
                sys.executable,
                "-O",
                str(SCRIPT),
                "--source",
                str(SOURCE),
                "--all-harmonics",
                str(all_harmonics),
                "--mixture",
                str(MIXTURE),
            ],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )

    def test_exact_repaired_witness(self) -> None:
        result = verify(SOURCE, ALL, MIXTURE)
        self.assertEqual(result["sharp_rank_kernels"], 27)
        self.assertEqual(result["integer_row_atoms"], 26)

    def test_tampered_mixture_is_rejected(self) -> None:
        data = json.loads(MIXTURE.read_text())
        data["atoms"][0]["weight"] = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / MIXTURE.name
            path.write_text(json.dumps(data))
            with self.assertRaises((VerificationError, ValueError, AssertionError)):
                verify(SOURCE, ALL, path)

    def test_exact_repaired_witness_under_optimized_python(self) -> None:
        result = self.run_optimized()
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["all_harmonic_tail"], "k>=600")

    def test_tampered_source_hash_rejected_under_optimized_python(self) -> None:
        data = json.loads(ALL.read_text())
        data["source_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ALL.name
            path.write_text(json.dumps(data))
            result = self.run_optimized(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source certificate SHA-256 mismatch", result.stderr)

    def test_tampered_minimum_pivot_rejected_under_optimized_python(self) -> None:
        data = json.loads(ALL.read_text())
        data["minimum_finite_ldl_pivot"]["value"] = "-1"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ALL.name
            path.write_text(json.dumps(data))
            result = self.run_optimized(path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "stored minimum harmonic-pivot value mismatch",
            result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
