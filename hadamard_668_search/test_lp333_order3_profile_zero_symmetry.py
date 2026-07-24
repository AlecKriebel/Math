#!/usr/bin/env python3
"""Tests for the exact 24-profile zero-gate symmetry audit."""

from __future__ import annotations

import unittest

import verify_lp333_order3_profile_zero_symmetry as symmetry


class ProfileZeroSymmetryTests(unittest.TestCase):
    def test_profile_catalog_action(self) -> None:
        result = symmetry.verify_profile_catalog_action()
        self.assertEqual(result["conjugation_fixed_profiles"], 2)
        self.assertEqual(result["physical_class_checks"], 252)
        self.assertEqual(result["actual_coefficient_checks"], 1_680)
        self.assertEqual(result["star_term_checks"], 225)

    def test_formal_group_and_covariance(self) -> None:
        result = symmetry.verify_equation_group()
        self.assertEqual(result["formal_group_order"], 24)
        self.assertEqual(result["group_law_checks"], 24**2)
        self.assertEqual(result["symbolic_group_law_checks"], 138_240)
        self.assertEqual(result["lag_representatives"], 13)
        self.assertEqual(result["universal_monomial_checks"], 2_200_368)
        self.assertEqual(
            result["action_sha256"],
            symmetry.EXPECTED_ACTION_SHA256,
        )
        self.assertTrue(result["zero_gate_preserved"])

    def test_target_orbits(self) -> None:
        result = symmetry.verify_target_orbits()
        self.assertEqual(result["catalog_targets"], 22)
        self.assertEqual(result["formal_target_orbits"], 7)
        self.assertEqual(result["target_fixed_counts"], (22, 2, 4, 0))
        self.assertEqual(
            result["formal_orbits_sha256"],
            symmetry.EXPECTED_FORMAL_TARGET_ORBITS_SHA256,
        )
        self.assertEqual(result["lift_compatible_target_orbits"], 12)
        self.assertEqual(
            result["lift_compatible_orbit_sizes"],
            (2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1),
        )
        self.assertEqual(
            result["lift_orbits_sha256"],
            symmetry.EXPECTED_LIFT_TARGET_ORBITS_SHA256,
        )

    def test_fixed_zero_caveat(self) -> None:
        result = symmetry.verify_fixed_zero_audit()
        self.assertEqual(result["a_zero_affine_stabilizer"], ((1, 0),))
        self.assertEqual(
            result["b_zero_affine_stabilizer"], ((1, 0), (8, 3))
        )
        self.assertEqual(result["a_conjugating_affine_stabilizer"], ())
        self.assertEqual(
            result["b_conjugating_affine_stabilizer"], ((8, 3),)
        )
        self.assertEqual(result["b_star_full_affine"], (323, 111))
        self.assertEqual(result["b_star_square_multiplier"], 100)
        self.assertEqual(result["c6_sixth_power"], 100)
        self.assertEqual(result["lift_compatible_group_order"], 12)

    def test_burnside_count(self) -> None:
        result = symmetry.verify_burnside_orbits()
        self.assertEqual(
            result["burnside_sum"],
            1_000_002_000_002_008_412_824_128,
        )
        self.assertEqual(
            result["raw_formal_orbits"],
            41_666_750_000_083_683_867_672,
        )
        self.assertEqual(
            result["certificate_sha256"],
            symmetry.EXPECTED_BURNSIDE_SHA256,
        )

    def test_rejected_candidate_symmetries(self) -> None:
        result = symmetry.verify_rejected_candidates()
        self.assertEqual(result["rejected_covariance_maps"], 5)
        self.assertTrue(
            all(count > 0 for _, count in result["mismatch_counts"])
        )
        self.assertEqual(
            result["counterexamples_sha256"],
            symmetry.EXPECTED_REJECTED_CANDIDATES_SHA256,
        )

    def test_full_replay(self) -> None:
        result = symmetry.verify()
        self.assertEqual(
            result["targets"]["formal_orbit_sizes"],
            (4, 2, 4, 4, 4, 2, 2),
        )
        self.assertEqual(
            result["fixed_zeros"]["signed_channel_stabilizer_order"],
            1,
        )
        self.assertEqual(
            result["certificate_sha256"],
            symmetry.EXPECTED_CERTIFICATE_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
