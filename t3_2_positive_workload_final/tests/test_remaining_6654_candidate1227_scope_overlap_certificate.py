"""Tests for the candidate-1227 versus 6,654 exact scope comparison."""

from __future__ import annotations

import unittest

import remaining_6654_candidate1227_scope_overlap_certificate as target


class Candidate1227ScopeOverlapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = target.certificate()

    def test_exact_byte_dependencies(self) -> None:
        self.assertEqual(target.dependency_sha256(), target.EXPECTED_DEPENDENCY_SHA256)

    def test_direct_and_orbit_overlap_are_empty(self) -> None:
        self.assertEqual(self.result["direct_candidate_overlap"], 0)
        self.assertEqual(self.result["s3_reversal_orbit_overlap"], 0)
        self.assertEqual(self.result["candidate_orbit_overlap_with_entire_18496"], 0)

    def test_normalized_support_overlap_is_empty(self) -> None:
        self.assertEqual(self.result["normalized_support_type_overlap"], 0)
        self.assertEqual(self.result["normalized_support_cap_type_overlap"], 0)

    def test_profile_only_router_is_not_exhaustive(self) -> None:
        self.assertEqual(self.result["new_pairs_with_aa_failure"], 1_596)
        self.assertEqual(self.result["old_router_syntactic_failure_rows"], 1_836)
        self.assertEqual(self.result["one_active_only_pairs_with_router_failure"], 396)

    def test_claim_boundary(self) -> None:
        self.assertFalse(self.result["orientation_rate_population_or_history_enumeration"])
        self.assertFalse(self.result["recurrence_claim"])


if __name__ == "__main__":
    unittest.main()

