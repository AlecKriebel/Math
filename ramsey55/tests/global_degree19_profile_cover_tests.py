#!/usr/bin/env python3
"""Tests for the exact minmax-degree-19 profile cover."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

import global_degree19_profile_cover as production
import global_degree19_profile_cover_check as checker
from direct_ramsey_cnf import canonical_counter_extension


class Degree19ProfileCoverTests(unittest.TestCase):
    def test_independent_profile_census_and_complement_cover(self) -> None:
        self.assertEqual(production.profiles(), checker.independent_profiles())
        self.assertEqual(
            len(production.profiles()), production.EXPECTED_PROFILE_COUNT
        )
        audit = checker.complement_orbit_audit()
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["admissible_count"], 88_550)
        self.assertEqual(audit["fixed_count"], 0)
        self.assertEqual(audit["canonical_count"], 44_275)

    def test_every_profile_obeys_parity_endpoint_and_orientation(self) -> None:
        for profile in production.profiles():
            self.assertEqual(sum(profile), production.ORDER)
            self.assertEqual((profile[0] + profile[2] + profile[4]) % 2, 0)
            self.assertGreater(profile[0] + profile[4], 0)
            self.assertGreater(
                (profile[0], profile[1]), (profile[4], profile[3])
            )
            self.assertNotEqual(profile, checker.complement_profile(profile))

    def test_exact_degree_units_accept_only_intended_degree(self) -> None:
        instance = production.direct_instance()
        vertex = 11
        incident = instance.counters[2 * vertex].input_literals
        for requested in production.DEGREES:
            units = production.exact_degree_units(vertex, requested)
            self.assertEqual(len(units), 2)
            self.assertTrue(all(literal < 0 for literal in units))
            for actual in range(18, 25):
                primary = {
                    abs(literal): index < actual
                    for index, literal in enumerate(incident)
                }
                assignment = dict(primary)
                for counter in instance.counters[
                    2 * vertex : 2 * vertex + 2
                ]:
                    assignment.update(
                        canonical_counter_extension(counter, primary)
                    )
                accepted = all(
                    assignment[abs(literal)] == (literal > 0)
                    for literal in units
                )
                self.assertEqual(accepted, actual == requested)

    def test_profile_units_are_distinct_false_thresholds(self) -> None:
        sample_indices = (
            0,
            1,
            len(production.profiles()) // 2,
            len(production.profiles()) - 2,
            len(production.profiles()) - 1,
        )
        for index in sample_indices:
            units = production.profile_units(production.profiles()[index])
            self.assertEqual(len(units), 86)
            self.assertEqual(len(set(map(abs, units))), 86)
            self.assertTrue(all(literal < 0 for literal in units))

    def test_selector_union_counts_and_hash_agreement(self) -> None:
        profile_count = production.EXPECTED_PROFILE_COUNT
        clauses = 1 + 86 * profile_count
        self.assertEqual(clauses, 3_807_651)
        self.assertEqual(
            production.BASE_VARIABLE_COUNT + profile_count, 109_678
        )
        self.assertEqual(
            production.BASE_CLAUSE_COUNT + clauses, 5_859_783
        )
        self.assertEqual(
            production.clause_stream_sha256(production.selector_clauses()),
            checker.clause_hash(checker.independent_selector_clauses()),
        )


if __name__ == "__main__":
    unittest.main()
