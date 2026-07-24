#!/usr/bin/env python3
"""Tests for the physical trivial-branch obstruction."""

from __future__ import annotations

import unittest

import verify_lp333_phase_cone_trivial_branch as verifier


class PhaseConeTrivialBranchTests(unittest.TestCase):
    def test_phi9_margin_kernel(self) -> None:
        result = verifier.verify_phi9_margin_kernel()
        self.assertEqual(result["ord_9_167"], 6)
        self.assertEqual(result["evaluation_rank"], 6)
        self.assertEqual(result["kernel_dimension"], 3)
        self.assertEqual(result["multiples_of_167_in_difference_interval"], (0,))
        self.assertEqual(result["per_channel_plus_count"], 167)
        self.assertTrue(result["individual_zero_coordinate_impossible"])
        self.assertTrue(result["joint_trivial_zero_branch_impossible"])

    def test_explicit_coordinate_formula(self) -> None:
        fixtures = (
            (19, 20, 21, 18, 17, 16, 15, 14, 27),
            (17, 18, 19, 17, 18, 19, 17, 18, 19),
            (37, 0, 0, 0, 37, 0, 0, 0, 37),
        )
        for margins in fixtures:
            self.assertEqual(
                verifier.margin_coordinate(margins),
                verifier.polynomial_coordinate(margins),
            )
        self.assertEqual(
            verifier.margin_coordinate(fixtures[1]),
            verifier.F_ZERO,
        )
        self.assertEqual(sum(fixtures[1]), 162)
        self.assertNotEqual(162 % 3, 167 % 3)

    def test_catalog_image(self) -> None:
        result = verifier.verify_catalog_image()
        self.assertEqual(result["catalog_rows"], 1756)
        self.assertEqual(result["per_channel_plus_count"], 167)
        self.assertEqual(result["fixed_zero_plus_counts"], (5, 5))
        self.assertEqual(result["distinct_coordinate_pairs"], 1411)
        self.assertEqual(result["distinct_projective_ratios"], 1411)
        self.assertEqual(
            result["pair_multiplicity_histogram"],
            ((1, 1066), (2, 345)),
        )
        self.assertEqual(result["abstract_norm_minus_one_ratios"], 4_657_464)
        self.assertTrue(result["ratio_determines_unique_catalog_scale"])

    def test_full_verifier(self) -> None:
        result = verifier.verify()
        self.assertEqual(set(result), {"margin_kernel", "catalog_image"})


if __name__ == "__main__":
    unittest.main()
