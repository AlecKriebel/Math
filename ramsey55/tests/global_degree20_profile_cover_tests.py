#!/usr/bin/env python3
"""Tests for the exact degree-20 profile cover."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

import global_degree20_profile_cover as production
import global_degree20_profile_cover_check as checker
from direct_ramsey_cnf import canonical_counter_extension


class Degree20ProfileCoverTests(unittest.TestCase):
    def test_independent_profile_census_matches(self) -> None:
        self.assertEqual(production.profiles(), checker.independent_profiles())
        self.assertEqual(len(production.profiles()), 253)
        self.assertTrue(checker.complement_orbit_audit()["valid"])

    def test_exact_degree_units_accept_only_intended_degree(self) -> None:
        instance = production.direct_instance()
        vertex = 7
        incident = instance.counters[2 * vertex].input_literals
        for requested in production.DEGREES:
            units = production.exact_degree_units(vertex, requested)
            for actual in range(18, 25):
                primary = {
                    abs(literal): index < actual
                    for index, literal in enumerate(incident)
                }
                assignment = dict(primary)
                for counter in instance.counters[2 * vertex : 2 * vertex + 2]:
                    assignment.update(
                        canonical_counter_extension(counter, primary)
                    )
                accepted = all(
                    assignment[abs(literal)] == (literal > 0)
                    for literal in units
                )
                self.assertEqual(accepted, actual == requested)

    def test_every_profile_has_all_distinct_threshold_units(self) -> None:
        for profile in production.profiles():
            units = production.profile_units(profile)
            self.assertEqual(len(units), 86)
            self.assertEqual(len(set(map(abs, units))), 86)
            self.assertTrue(all(literal < 0 for literal in units))

    def test_selector_union_counts(self) -> None:
        plan = production.build_plan()
        union = plan["selector_union"]
        self.assertEqual(union["selector_variable_count"], 253)
        self.assertEqual(
            union["selector_implication_clause_count"], 253 * 86
        )
        self.assertEqual(union["appended_clause_count"], 1 + 253 * 86)


if __name__ == "__main__":
    unittest.main()
