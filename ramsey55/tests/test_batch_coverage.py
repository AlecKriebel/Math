#!/usr/bin/env python3
"""Coverage guards for the all-42 fixed-core certificate claims."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BatchCoverageTests(unittest.TestCase):
    def test_tree_checker_rejects_incomplete_all_42_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / "core_completion_delete_00.cnf").write_text(
                "p cnf 1 1\n1 0\n", encoding="ascii"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "verify" / "core_completion_batch_check.py"),
                    "--input-dir",
                    str(directory),
                    "--expect-all-42",
                    "--output",
                    str(directory / "summary.json"),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("deletion-label coverage mismatch", result.stderr)

    def test_formula_checker_rejects_incomplete_all_42_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / "core_completion_delete_00.cnf").write_text(
                "p cnf 1 1\n1 0\n", encoding="ascii"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "verify" / "core_completion_cnf_check.py"),
                    "--graph",
                    str(ROOT / "data" / "exoo42_constructed.g6"),
                    "--cnf-dir",
                    str(directory),
                    "--expect-all-42",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("deletion-label coverage mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
