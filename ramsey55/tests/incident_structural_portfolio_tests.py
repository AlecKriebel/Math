#!/usr/bin/env python3
"""Tests for the deterministic incident-boundary completion portfolio."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from incident_structural_portfolio import build_plan, free_edge_count  # noqa: E402
from incident_structural_portfolio_check import audit_plan  # noqa: E402


class IncidentStructuralPortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = build_plan()

    def test_exact_representative_geometry_and_sequences(self) -> None:
        expected = {
            "class01": {
                "conflict_union": [1, 3, 11, 25, 35, 37],
                "near_pressure": [17, 39, 33, 32, 23, 42],
                "row_diversity": [26, 28, 0, 8, 32, 41],
            },
            "class02": {
                "conflict_union": [8, 19, 25, 27, 29, 30],
                "near_pressure": [28, 41, 12, 0, 38, 35],
                "row_diversity": [12, 22, 17, 20, 34, 2],
            },
        }
        for representative in self.plan["representatives"]:
            wanted = expected[representative["class_id"]]
            self.assertEqual(
                representative["conflict_union"], wanted["conflict_union"]
            )
            self.assertEqual(
                representative["selection_sequences"]["near_pressure"]["vertices"],
                wanted["near_pressure"],
            )
            self.assertEqual(
                representative["selection_sequences"]["row_diversity"]["vertices"],
                wanted["row_diversity"],
            )

    def test_exact_balanced_coverage_and_free_edge_counts(self) -> None:
        self.assertEqual(len(self.plan["instances"]), 16)
        self.assertEqual(
            {size: free_edge_count(43, size) for size in (9, 10, 11, 12)},
            {9: 342, 10: 375, 11: 407, 12: 438},
        )
        for class_id in ("class01", "class02"):
            for policy in ("near_pressure", "row_diversity"):
                selected = [
                    record
                    for record in self.plan["instances"]
                    if record["class_id"] == class_id
                    and record["policy"] == policy
                ]
                self.assertEqual(
                    [record["boundary_size"] for record in selected],
                    [9, 10, 11, 12],
                )
                for earlier, later in zip(selected, selected[1:]):
                    self.assertLess(
                        set(earlier["incident_vertices"]),
                        set(later["incident_vertices"]),
                    )

    def test_solver_and_budget_portfolio_is_frozen(self) -> None:
        expected_budgets = {9: 400_000, 10: 300_000, 11: 200_000, 12: 150_000}
        self.assertEqual(
            {
                record["solver"]
                for record in self.plan["instances"]
            },
            {"Glucose3", "MapleChrono"},
        )
        self.assertTrue(
            all(
                record["conflict_budget"]
                == expected_budgets[record["boundary_size"]]
                for record in self.plan["instances"]
            )
        )

    def test_independent_checker_accepts_and_rejects_tamper(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            good_path = Path(directory) / "good.json"
            good_path.write_text(
                json.dumps(self.plan, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
            self.assertTrue(audit_plan(good_path)["accepted"])
            changed = json.loads(good_path.read_text(encoding="utf-8"))
            changed["instances"][0]["incident_vertices"][-1] = 42
            bad_path = Path(directory) / "bad.json"
            bad_path.write_text(
                json.dumps(changed, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
            bad_audit = audit_plan(bad_path)
            self.assertFalse(bad_audit["accepted"])
            self.assertFalse(bad_audit["checks"]["instances_exact"])


if __name__ == "__main__":
    unittest.main()
