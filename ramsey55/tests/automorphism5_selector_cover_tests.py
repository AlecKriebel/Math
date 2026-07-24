#!/usr/bin/env python3
"""Tests for the independent order-5 selector-cover checker."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

import automorphism5_selector_cover_check as checker  # noqa: E402


class Automorphism5SelectorCoverTests(unittest.TestCase):
    def test_fixed_graph_normalization_covers_all_eight_graphs(self) -> None:
        result = checker.normalized_fixed_graph_cover()
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["records"]), 8)

    def test_degree_interval_forces_four_moved_cycles(self) -> None:
        result = checker.degree_normalization()
        self.assertTrue(result["valid"])
        self.assertEqual(
            result["possibilities"], {"0": [4], "1": [4], "2": [4]}
        )

    def test_exact_type_and_orientation_counts(self) -> None:
        full = checker.independent_type_schedule(include_hard=True)
        ordinary = checker.independent_type_schedule(include_hard=False)
        self.assertEqual(len(full), 59)
        self.assertEqual(len(ordinary), 58)
        self.assertIn(("one_edge", checker.HARD_COUNTS), full)
        self.assertNotIn(("one_edge", checker.HARD_COUNTS), ordinary)
        self.assertEqual(len(checker.independent_orientations()), 80)

    def test_materialized_ordinary_formula_matches_independently(self) -> None:
        result = checker.check(
            ROOT
            / "certificates"
            / "order43_automorphism5_ordinary58_selector_cover.cnf",
            ROOT
            / "certificates"
            / "order43_automorphism5_ordinary58_selector_cover.metadata.json",
        )
        self.assertTrue(result["valid"])
        self.assertTrue(result["structural_valid"])
        self.assertFalse(result["full_cycle_type_covered"])


if __name__ == "__main__":
    unittest.main()
