#!/usr/bin/env python3
"""Tests for the independent global-branch checker."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from global_ramsey_branch_check import (  # noqa: E402
    EXPECTED_GENERATOR_ID,
    check_branch,
    independent_units,
)


class GlobalRamseyBranchCheckTests(unittest.TestCase):
    def materialize_fixture(
        self, root: Path, *, corrupt_unit: bool = False
    ) -> tuple[Path, Path, Path]:
        base = root / "base.cnf"
        branch = root / "branch.cnf"
        metadata = root / "branch.json"
        base.write_text(
            "c base\np cnf 50 2\n1 2 0\n-1 3 0\n",
            encoding="ascii",
        )
        units = list(independent_units(43, 18))
        if corrupt_unit:
            units[-1] *= -1
        branch_text = (
            "c base\n"
            f"c branch_generator {EXPECTED_GENERATOR_ID}\n"
            "c vertex0_degree 18\n"
            "p cnf 50 44\n"
            "1 2 0\n"
            "-1 3 0\n"
            + "".join(f"{literal} 0\n" for literal in units)
        )
        branch.write_text(branch_text, encoding="ascii")
        metadata.write_text(
            json.dumps(
                {
                    "generator": EXPECTED_GENERATOR_ID,
                    "order": 43,
                    "degree": 18,
                    "base_cnf_sha256": hashlib.sha256(
                        base.read_bytes()
                    ).hexdigest(),
                    "cnf_sha256": hashlib.sha256(
                        branch.read_bytes()
                    ).hexdigest(),
                    "unit_literals": list(independent_units(43, 18)),
                    "variable_count": 50,
                    "clause_count": 44,
                    "cnf_bytes": branch.stat().st_size,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return base, branch, metadata

    def test_accepts_exact_copy_plus_units(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base, branch, metadata = self.materialize_fixture(Path(directory))
            result = check_branch(base, branch, metadata, 18)
            self.assertTrue(result["valid"])

    def test_rejects_corrupt_unit_even_with_matching_file_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base, branch, metadata = self.materialize_fixture(
                Path(directory), corrupt_unit=True
            )
            result = check_branch(base, branch, metadata, 18)
            self.assertFalse(result["valid"])
            self.assertFalse(
                result["checks"]["remaining_clauses_are_expected_units"]
            )


if __name__ == "__main__":
    unittest.main()
