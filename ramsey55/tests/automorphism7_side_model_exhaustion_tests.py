#!/usr/bin/env python3
"""Tests for the exact C7 side-model exhaustion encoding."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for directory in (ROOT / "src", ROOT / "verify"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import automorphism7_side_model_exhaustion as generator  # noqa: E402
import automorphism7_side_model_exhaustion_check as checker  # noqa: E402


class SideModelExhaustionTests(unittest.TestCase):
    def test_independent_side_formula_counts(self) -> None:
        clauses = checker.side_formula(checker.side_edge_table())
        self.assertEqual(len(clauses), 3618)
        self.assertEqual(sum(all(literal < 0 for literal in c) for c in clauses), 843)
        self.assertEqual(sum(all(literal > 0 for literal in c) for c in clauses), 2775)

    def test_blocker_falsifies_exactly_its_model(self) -> None:
        model = int("001000001100100101111110100100", 2)
        observed = generator.model_blocker(model)
        self.assertEqual(observed, checker.blocker(model))
        self.assertFalse(generator.model_satisfies(model, (observed,)))
        self.assertTrue(
            all(
                generator.model_satisfies(model ^ (1 << bit), (observed,))
                for bit in range(30)
            )
        )

    def test_bitset_replay_detects_failure(self) -> None:
        models = [0, 1, 2, 3]
        valid, failure = checker.all_models_satisfy(models, ((1, 2),))
        self.assertFalse(valid)
        self.assertEqual(failure, {"clause_index": 0, "model_position": 0, "model": 0})
        self.assertTrue(generator.all_models_satisfy([1, 2, 3], ((1, 2),)))


if __name__ == "__main__":
    unittest.main()
