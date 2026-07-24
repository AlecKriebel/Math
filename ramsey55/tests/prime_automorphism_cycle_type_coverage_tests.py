#!/usr/bin/env python3
"""Tests for the prime-order automorphism cycle-type coverage audit."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verify" / "prime_automorphism_cycle_type_coverage.py"
SPEC = importlib.util.spec_from_file_location("prime_coverage", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(MODULE_PATH)
coverage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coverage)


class PrimeAutomorphismCoverageTests(unittest.TestCase):
    def test_direct_degree_exclusions_have_no_allowed_degree(self) -> None:
        for cycle_type in coverage.DIRECT_DEGREE_EXCLUSIONS:
            self.assertEqual(
                coverage.fixed_vertex_degree_options(*cycle_type), ()
            )

    def test_p23_cross_count_and_clique_contradictions(self) -> None:
        result = coverage.p23_arithmetic()
        self.assertEqual(result["feasible_low_counts"], [0, 1, 19, 20])
        self.assertEqual(result["complement_representatives"], [0, 1])
        self.assertGreaterEqual(result["low_zero_clique_lower_bound"], 5)
        self.assertGreaterEqual(result["low_one_clique_lower_bound"], 5)
        self.assertTrue(result["contradiction"])

    def test_inventory_lists_every_prime_cycle_type_once(self) -> None:
        all_types = coverage.all_prime_cycle_types()
        self.assertEqual(len(all_types), len(set(all_types)))
        for prime, cycles in all_types:
            self.assertTrue(coverage.is_prime(prime))
            self.assertGreaterEqual(cycles, 1)
            self.assertGreaterEqual(coverage.ORDER - prime * cycles, 0)

    def test_artifact_bound_coverage_audit(self) -> None:
        result = coverage.check(ROOT)
        self.assertTrue(result["valid"])
        self.assertTrue(result["large_prime_cycle_types_complete"])
        self.assertFalse(result["classification_complete"])
        self.assertGreater(result["uncovered_cycle_type_count"], 0)


if __name__ == "__main__":
    unittest.main()
