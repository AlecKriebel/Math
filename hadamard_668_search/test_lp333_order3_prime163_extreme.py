#!/usr/bin/env python3
"""Tests for the prime-163 extreme-sector obstruction."""

from __future__ import annotations

import unittest

import verify_lp333_order3_prime163_extreme as theorem


class Prime163ExtremeTest(unittest.TestCase):
    def test_explicit_principal_prime_factorization(self) -> None:
        result = theorem.verify_field_arithmetic()
        self.assertEqual(result["full_frobenius_order"], 36)
        self.assertEqual(result["quotient_frobenius_order"], 12)
        self.assertEqual(result["degree_L_over_Q"], 24)
        self.assertEqual(result["residue_degrees"], (12, 12))
        self.assertEqual(
            result["prime_absolute_norms"], (163**12, 163**12)
        )
        self.assertEqual(
            result["principal_generators"], ((14, 3), (11, -3))
        )
        self.assertFalse(result["class_group_computation_needed"])

    def test_cm_unit_rigidity(self) -> None:
        result = theorem.verify_unit_rigidity()
        self.assertEqual(result["roots_of_unity_in_L"], 6)
        self.assertEqual(result["norm_163_eisenstein_element_count"], 12)
        self.assertEqual(
            set(result["norm_163_eisenstein_elements"]),
            set(theorem.norm_solutions(163)),
        )

    def test_fourier_contradiction(self) -> None:
        result = theorem.verify_fourier_obstruction()
        self.assertTrue(result["primitive_fourier_values_forced_constant"])
        self.assertEqual(result["candidate_pairs"], 144)
        self.assertEqual(result["candidate_pairs_satisfying_identity"], 0)
        self.assertGreater(
            result["reverse_triangle_lower_bound_squared"],
            result["required_value_squared"],
        )

    def test_exact_extreme_sector_census(self) -> None:
        result = theorem.verify_extreme_sector_census()
        self.assertEqual(
            result["extreme_physical_channel_energies"], (163, 4)
        )
        self.assertEqual(result["unrestricted_channel_words"], 10**12)
        self.assertEqual(result["zero_signature_pair_bucket"], 34)
        self.assertEqual(
            result["target_counts"],
            (
                ((4, -1, 0, 0), 1_151_042_580, 1_617_192),
                ((5, 1, 0, 0), 1_151_042_580, 1_617_192),
            ),
        )
        self.assertEqual(
            result["extreme_assignments_excluded_total"], 3_234_384
        )

    def test_scope_does_not_close_shards(self) -> None:
        result = theorem.verify_extreme_sector_census()
        self.assertEqual(result["aggregate_shards_excluded"], 0)
        self.assertEqual(
            result["nonextreme_local_witness_physical_energies"],
            (
                ((4, -1, 0, 0), (37, 130)),
                ((5, 1, 0, 0), (37, 130)),
            ),
        )


if __name__ == "__main__":
    unittest.main()
