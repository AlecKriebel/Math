#!/usr/bin/env python3
"""Tests for the fail-closed double-forced production checker."""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

import e2_double_forced_result_check as checker  # noqa: E402


def disjoint_cliques(sizes: tuple[int, ...]) -> tuple[int, ...]:
    adjacency = [0] * checker.ORDER
    first = 0
    for size in sizes:
        for left in range(first, first + size):
            for right in range(left + 1, first + size):
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
        first += size
    return tuple(adjacency)


class DoubleForcedResultCheckTests(unittest.TestCase):
    def test_frozen_production_artifacts_accept(self) -> None:
        result = checker.check(ROOT)
        self.assertTrue(result["valid"], result.get("fatal_error"))
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(
            result["metrics"]["output_objective_distribution"],
            {"2": 1878},
        )

    def test_graph6_round_trip_and_objective_recount(self) -> None:
        adjacency = disjoint_cliques((5,))
        code = checker.encode_graph6(adjacency)
        self.assertEqual(checker.decode_graph6(code), adjacency)
        clique_count = checker.count_five_cliques(adjacency)
        self.assertEqual(clique_count, 1)
        self.assertGreater(checker.exact_objective(adjacency), 1)
        self.assertGreaterEqual(
            checker.exact_objective(adjacency, reject_above=3), 3
        )

    def test_counter_tamper_is_rejected(self) -> None:
        result = checker.read_json(ROOT / checker.SEARCH_RESULT_PATH)
        plan = checker.read_json(ROOT / checker.SEARCH_PLAN_PATH)
        changed = copy.deepcopy(result)
        changed["rollouts"] -= 1
        checks = checker.validate_search_counters(changed, plan)
        self.assertFalse(checks["counter_rollouts"])
        self.assertFalse(checks["rollout_schedule_identity"])
        self.assertFalse(checks["terminal_E2_and_exhausted_identity"])

    def test_recorded_paths_are_strict(self) -> None:
        planned = "results/constructive/run/output.g6"
        artifact = ROOT / planned
        self.assertTrue(
            checker.recorded_path_matches(
                planned, planned, artifact, ROOT
            )
        )
        self.assertTrue(
            checker.recorded_path_matches(
                f"ramsey55/{planned}", planned, artifact, ROOT
            )
        )
        self.assertTrue(
            checker.recorded_path_matches(
                str(artifact.resolve()), planned, artifact, ROOT
            )
        )
        self.assertFalse(
            checker.recorded_path_matches(
                "other/output.g6", planned, artifact, ROOT
            )
        )

    def test_missing_project_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = checker.check(Path(directory))
        self.assertFalse(result["valid"])
        self.assertEqual(result["status"], "INVALID")
        self.assertFalse(result["checks"]["fatal_error_absent"])


if __name__ == "__main__":
    unittest.main()
