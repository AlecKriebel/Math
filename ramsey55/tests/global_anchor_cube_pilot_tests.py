from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

import global_anchor_cube_pilot as worker  # noqa: E402
import global_anchor_cube_pilot_check as checker  # noqa: E402


class GlobalAnchorCubePilotTests(unittest.TestCase):
    def test_independent_schedules_match_frozen_cover_plans(self) -> None:
        d18_plan = json.loads(
            (
                ROOT
                / "results/benchmark_plans/global_anchor_degree18_extension_v1.json"
            ).read_text(encoding="utf-8")
        )
        d1920_plan = json.loads(
            (
                ROOT
                / "results/benchmark_plans/global_anchor_cube_cover_v1.json"
            ).read_text(encoding="utf-8")
        )
        for degree, plan in ((18, d18_plan), (19, d1920_plan), (20, d1920_plan)):
            branch = worker.branch_from_plan(plan, degree)
            production = worker.cube_schedule(branch, degree)
            independent = checker.expected_schedule(degree)
            self.assertEqual(production, independent)
            self.assertEqual(len(production), 143)

    def test_orbit_partition_and_selector_endpoints(self) -> None:
        representatives, owner = checker.representatives_and_owner()
        self.assertEqual(len(owner), 35_714)
        self.assertEqual(len(representatives), 143)
        schedule = checker.expected_schedule(18)
        self.assertEqual(schedule[0]["selector"], 65_404)
        self.assertEqual(schedule[-1]["selector"], 65_546)
        self.assertEqual(schedule[0]["full_cube_assumption_count"], 70)
        self.assertEqual(
            checker.expected_schedule(19)[0]["full_cube_assumption_count"], 156
        )
        self.assertEqual(
            checker.expected_schedule(20)[0]["full_cube_assumption_count"], 156
        )

    def test_selector_assumption_hash_agreement(self) -> None:
        for selector in (65_404, 65_475, 65_546):
            self.assertEqual(
                worker.selector_assumption_sha256(selector),
                checker.selector_assumption_hash(selector),
            )

    def test_streaming_model_replay_and_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cnf = Path(directory) / "tiny.cnf"
            cnf.write_text(
                "c test\np cnf 3 3\n1 -2 0\n2 3 0\n-3 0\n",
                encoding="ascii",
            )
            self.assertEqual(
                worker.replay_dimacs_model(cnf, [1, 2, -3], [1]), (3, 3)
            )
            self.assertEqual(
                checker.replay_dimacs_truth(cnf, {1, 2}, 1), (3, 3)
            )
            with self.assertRaisesRegex(ValueError, "falsifies DIMACS clause"):
                worker.replay_dimacs_model(cnf, [-1, 2, -3], [-1])
            with self.assertRaisesRegex(ValueError, "falsifies DIMACS clause"):
                checker.replay_dimacs_truth(cnf, {2}, 2)

    def test_decode_primary_model(self) -> None:
        model = [-variable for variable in range(1, 904)]
        adjacency = worker.decode_primary_model(model)
        self.assertEqual(len(adjacency), 43)
        self.assertTrue(all(neighbors == 0 for neighbors in adjacency))


if __name__ == "__main__":
    unittest.main()
