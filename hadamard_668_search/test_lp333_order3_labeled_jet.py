#!/usr/bin/env python3
"""Dependency-free tests for the exact labelled primitive-nine checkpoint."""

from __future__ import annotations

import unittest

from verify_lp333_order3_labeled_jet import (
    FIELD_MODULI,
    INVARIANT_GENERATOR_POLYNOMIAL,
    LABELLED_SURVIVOR_AGGREGATE,
    LABELLED_SURVIVOR_CATALOG_INDEX,
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
    validate_labelled_certificate,
    verify_invariant_algebra_split,
    verify_pinned_labelled_survivor,
)


class OrderThreeLabelledJetTests(unittest.TestCase):
    def test_exact_invariant_algebra_split(self) -> None:
        result = verify_invariant_algebra_split()
        self.assertEqual(result["algebra_dimension"], 13)
        self.assertEqual(result["split_dimensions"], (1, 6, 6))
        self.assertEqual(result["split_rank"], 13)
        self.assertEqual(result["field_size"], 729)
        self.assertEqual(result["field_moduli"], FIELD_MODULI)
        self.assertEqual(
            result["generator_polynomial"],
            INVARIANT_GENERATOR_POLYNOMIAL,
        )
        self.assertEqual(result["nonzero_field_elements_checked"], 1_456)
        self.assertEqual(result["basis_products_checked"], 338)

    def test_pinned_catalog_survivor_replays(self) -> None:
        self.assertTrue(
            all(
                bin(mask).count("1") == 3
                for mask in (
                    LABELLED_SURVIVOR_MASKS_A
                    + LABELLED_SURVIVOR_MASKS_B
                )
            )
        )
        result = verify_pinned_labelled_survivor()
        self.assertEqual(
            result["catalog_index"],
            LABELLED_SURVIVOR_CATALOG_INDEX,
        )
        self.assertEqual(result["class_words"], 24)
        self.assertEqual(result["physical_columns"], 37)
        self.assertEqual(result["exact_zero_column_lags"], 4)
        self.assertEqual(result["jet_equations"], 222)
        self.assertTrue(result["valid"])

    def test_certificate_is_not_a_margin_only_check(self) -> None:
        # Exchange rows zero and one between two same-weight classes.  This
        # preserves every row margin and both class weights, but not the
        # correlation equations.
        changed_a = (
            50,
            LABELLED_SURVIVOR_MASKS_A[1],
            41,
            *LABELLED_SURVIVOR_MASKS_A[3:],
        )
        with self.assertRaisesRegex(
            ValueError, "exact zero-column-lag equation failed"
        ):
            validate_labelled_certificate(
                LABELLED_SURVIVOR_AGGREGATE,
                changed_a,
                LABELLED_SURVIVOR_MASKS_B,
            )


if __name__ == "__main__":
    unittest.main()
