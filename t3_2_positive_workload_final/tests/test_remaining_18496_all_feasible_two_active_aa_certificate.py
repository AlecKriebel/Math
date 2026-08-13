"""Regression tests for the exact all-feasible-two-active AA identity."""

from __future__ import annotations

import unittest

import remaining_18496_all_feasible_two_active_aa_certificate as target


class AllFeasibleTwoActiveAACertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = target.certificate()

    def test_dependencies_are_exact(self) -> None:
        self.assertEqual(target.dependency_sha256(), target.EXPECTED_DEPENDENCY_SHA256)

    def test_every_feasible_two_active_row_is_aa(self) -> None:
        self.assertGreater(self.result["feasible_two_active_incidences"], 0)
        self.assertEqual(self.result["unavailable_linkage_rows"], 0)
        self.assertEqual(
            set(self.result["unordered_kind_histogram"]),
            {"C/C", "C/Q", "C/U", "Q/Q", "Q/U", "U/U"},
        )

    def test_corrected_cut_split(self) -> None:
        self.assertEqual(self.result["corrected_cut_failures"], 3_084)
        self.assertEqual(
            self.result["feasible_two_active_incidences"],
            self.result["corrected_cut_passes"]
            + self.result["corrected_cut_failures"],
        )

    def test_fingerprints_are_pinned(self) -> None:
        self.assertEqual(
            self.result["feasible_incidence_sha256"],
            target.EXPECTED_FEASIBLE_INCIDENCE_SHA256,
        )
        self.assertEqual(self.result["identity_sha256"], target.EXPECTED_IDENTITY_SHA256)

    def test_scope_is_finite_geometry_only(self) -> None:
        self.assertFalse(
            self.result["orientation_rate_population_or_history_enumeration"]
        )
        self.assertFalse(self.result["recurrence_claim"])


if __name__ == "__main__":
    unittest.main()
