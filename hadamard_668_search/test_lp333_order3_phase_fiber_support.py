#!/usr/bin/env python3
"""Tests for the LP(333) phase-fiber primitive-support theorem."""

from __future__ import annotations

import unittest

import verify_lp333_order3_phase_fiber_support as support


class PhaseFiberSupportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = support.verify()

    def test_cyclotomic_kernel(self) -> None:
        irreducible = self.result["cyclotomic_irreducibility"]
        kernel = self.result["invariant_kernel"]
        self.assertEqual(irreducible["reduction_prime"], 13)
        self.assertEqual(irreducible["order_mod_37"], 36)
        self.assertEqual(irreducible["rabin_proper_degrees"], (18, 12))
        self.assertEqual(irreducible["degree_over_Q_omega"], 36)
        self.assertEqual(kernel["invariant_word_dimension"], 13)
        self.assertEqual(kernel["primitive_image_rank"], 12)
        self.assertEqual(kernel["kernel_dimension"], 1)
        self.assertEqual(kernel["kernel_word"], "Phi_37")

    def test_fixed_zero_activity(self) -> None:
        fixed = self.result["fixed_zero_activity"]
        self.assertEqual(fixed["forced_nonzero_count"], 5)
        self.assertEqual(
            fixed["forced_nonzero_fibers"],
            ("A0", "A1", "A2", "B1", "B2"),
        )
        self.assertEqual(fixed["optional_fiber"], "B0")
        self.assertEqual(fixed["zero_column_norms"], (1, 1, 1, 0, 1, 1))

    def test_prime_167_norm_gap(self) -> None:
        gap = self.result["norm_gap"]
        self.assertTrue(gap["base_prime_inert"])
        self.assertEqual(gap["H_fixed_field_degree_over_Q_omega"], 12)
        self.assertEqual(gap["primitive_prime_count"], 2)
        self.assertEqual(
            gap["primitive_relative_residue_degrees"],
            (6, 6),
        )
        self.assertEqual(
            gap["strict_energy_norm_upper_bound"],
            support.P**12,
        )
        self.assertEqual(
            gap["coordinate_zero_divisibility_threshold"],
            support.P**12,
        )
        self.assertGreater(
            gap["constant_unit_trivial_norm"],
            gap["trivial_energy"],
        )

    def test_zero_pattern_stratification(self) -> None:
        strata = self.result["support_strata"]
        self.assertEqual(strata["raw_joint_zero_patterns"], 4096)
        self.assertEqual(strata["mismatched_zero_patterns_eliminated"], 4032)
        self.assertEqual(
            strata["matching_patterns_eliminated_by_fixed_activity"],
            62,
        )
        self.assertEqual(strata["total_zero_patterns_eliminated"], 4094)
        self.assertEqual(
            strata["allowed_common_zero_sets"],
            ((), ("B0",)),
        )
        self.assertEqual(strata["allowed_joint_zero_pattern_count"], 2)
        self.assertEqual(strata["rank_one_physical_zero_sets"], ((),))
        self.assertEqual(strata["B0_zero_branch_minimum_plane_rank"], 2)

    def test_pinned_certificate(self) -> None:
        self.assertEqual(
            self.result["certificate_sha256"],
            support.EXPECTED_CERTIFICATE_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
