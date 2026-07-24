#!/usr/bin/env python3
"""Tests for the mod-seven LP(333) phase cyclic-decoder audit."""

from __future__ import annotations

import unittest

import verify_lp333_order3_phase_cyclic_decoder as decoder


class PhaseCyclicDecoderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = decoder.verify()

    def test_complete_scalar_split(self) -> None:
        split = self.result["complete_split"]
        self.assertEqual(split["phi9_factors"], ("X^3-2", "X^3-4"))
        self.assertEqual(split["coefficient_field_size"], 343)
        self.assertEqual(split["coefficient_frobenius_mod_37"], 10)
        self.assertEqual(split["scalar_factors_per_component"], 13)
        self.assertEqual(split["period_transform_rank"], 13)
        self.assertEqual(split["period_transform_zero_entries"], 0)
        self.assertEqual(split["coordinate_product_basis_checks"], 9)

    def test_single_factor_has_no_strong_bch_distance(self) -> None:
        self.assertEqual(
            self.result["complete_split"][
                "single_factor_unrestricted_kernel_distance"
            ],
            2,
        )

    def test_local_alphabet_census(self) -> None:
        alphabets = self.result["coefficient_alphabets"]
        self.assertEqual(
            alphabets["one_channel_alphabet_sizes"],
            (1, 9, 27),
        )
        self.assertEqual(
            alphabets["two_channel_alphabet_histogram"],
            (
                (1, 9),
                (9, 36),
                (27, 6),
                (81, 36),
                (243, 12),
                (729, 1),
            ),
        )
        self.assertEqual(alphabets["maximum_two_channel_local_alphabet"], 729)

    def test_affine_compatibility_count(self) -> None:
        compatibility = self.result["affine_compatibility"]
        self.assertEqual(compatibility["factor_target_mod_7"], 6)
        self.assertEqual(compatibility["factor_plus_vectors"], 117_648)
        self.assertEqual(
            compatibility["compatible_minus_vectors_per_plus"],
            343,
        )
        self.assertEqual(
            compatibility["compatibility_entries"],
            40_353_264,
        )

    def test_factor_orientation(self) -> None:
        orientation = self.result["factor_orientation"]
        self.assertEqual(orientation["factor_orientation_checks"], 13)
        self.assertEqual(orientation["target_at_every_factor"], 6)
        self.assertEqual(len(orientation["inverse_factor_rows"]), 13)

    def test_quadratic_join_is_not_additive(self) -> None:
        self.assertFalse(
            self.result["nonadditivity"][
                "quadratic_block_signature_additive"
            ]
        )

    def test_architecture_barriers(self) -> None:
        bounds = self.result["architecture_bounds"]
        self.assertEqual(bounds["raw_one_factor_states"], 7**12)
        self.assertGreater(
            bounds["raw_one_factor_states"],
            bounds["known_profile_signature_fallback"],
        )
        self.assertEqual(bounds["raw_phase_trits"], 54)
        self.assertEqual(bounds["uniform_phase_gauge_trits"], 0)
        self.assertEqual(bounds["balanced_half_entries"], 3**27)
        self.assertEqual(bounds["largest_three_block_list"], 3**18)
        self.assertEqual(bounds["smallest_three_block_pair_join"], 3**36)
        self.assertEqual(bounds["largest_four_block_list"], 3**14)
        self.assertEqual(bounds["smallest_four_block_pair_join"], 3**26)
        self.assertEqual(bounds["largest_four_block_pair_join"], 3**28)
        self.assertEqual(bounds["balanced_four_block_pair_join"], 3**27)
        self.assertEqual(bounds["factor_field_products"], 26)
        self.assertEqual(bounds["scalar_product_tables"], 234)
        self.assertEqual(bounds["rows_per_scalar_product_table"], 49)
        self.assertEqual(bounds["total_scalar_product_table_rows"], 11_466)

    def test_certificate_is_pinned(self) -> None:
        self.assertEqual(
            self.result["certificate_sha256"],
            decoder.EXPECTED_CERTIFICATE_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
