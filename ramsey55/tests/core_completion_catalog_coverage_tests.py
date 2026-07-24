#!/usr/bin/env python3
"""Coverage-guard tests for catalog fixed-core classifications."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "verify" / "core_completion_catalog_coverage_check.py"


class CoreCompletionCatalogCoverageTests(unittest.TestCase):
    def test_rejects_missing_planned_pair(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = root / "plan.json"
            summary = root / "summary.json"
            plan.write_text(
                json.dumps(
                    {
                        "pairs": [
                            {"catalog_line": 1, "deleted_vertex": 0},
                            {"catalog_line": 2, "deleted_vertex": 17},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            summary.write_text(
                json.dumps(
                    {
                        "instances": [
                            {"catalog_line": 1, "deleted_vertex": 0}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            checked = subprocess.run(
                (
                    sys.executable,
                    str(CHECKER),
                    "--summary",
                    str(summary),
                    "--pairs-plan",
                    str(plan),
                ),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("coverage mismatch", checked.stderr)

    def test_rejects_duplicate_actual_pair(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = root / "plan.json"
            summary = root / "summary.json"
            plan.write_text(
                json.dumps(
                    {
                        "pairs": [
                            {"catalog_line": 1, "deleted_vertex": 0}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            summary.write_text(
                json.dumps(
                    {
                        "instances": [
                            {"catalog_line": 1, "deleted_vertex": 0},
                            {"catalog_line": 1, "deleted_vertex": 0},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            checked = subprocess.run(
                (
                    sys.executable,
                    str(CHECKER),
                    "--summary",
                    str(summary),
                    "--pairs-plan",
                    str(plan),
                ),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("duplicate fixed-core pairs", checked.stderr)


if __name__ == "__main__":
    unittest.main()
