#!/usr/bin/env python3
"""Focused tests for the order-three LP(333) difference-family lift."""

from __future__ import annotations

import unittest

from verify_lp333_order3_difference_family import (
    BLOCK_IDS,
    CATALOG_DATA_ROWS,
    CATALOG_SHA256,
    CATALOG_WITNESS,
    CATALOG_WITNESS_INDEX,
    EXPECTED_NONZERO_CLASS_RESIDUALS,
    WITNESS_CLASS_EXPONENTS,
    block_sets,
    cyclotomic_classes,
    reconstruct_class_words,
    verify_catalog,
    verify_difference_family_equivalence,
    verify_expansion_and_pure_axis,
    verify_nonzero_class_residuals,
)


class OrderThreeDifferenceFamilyTests(unittest.TestCase):
    def test_catalog_hash_count_and_witness(self) -> None:
        result = verify_catalog()
        self.assertEqual(result["sha256"], CATALOG_SHA256)
        self.assertEqual(result["data_rows"], CATALOG_DATA_ROWS)
        self.assertEqual(result["unique_rows"], CATALOG_DATA_ROWS)
        self.assertEqual(result["witness_index"], CATALOG_WITNESS_INDEX)
        self.assertEqual(result["witness"], CATALOG_WITNESS)

    def test_block_reconstruction_and_classes(self) -> None:
        self.assertEqual(tuple(len(group) for group in BLOCK_IDS), (6, 6, 6, 6))
        self.assertEqual(
            tuple(len(group) for group in block_sets().values()),
            (6, 6, 6, 6),
        )
        self.assertEqual(reconstruct_class_words(), WITNESS_CLASS_EXPONENTS)

        classes = cyclotomic_classes()
        self.assertEqual(len(classes), 12)
        self.assertTrue(all(len(part) == 3 for part in classes))
        self.assertEqual(
            set().union(*(set(part) for part in classes)),
            set(range(1, 37)),
        )

    def test_incidence_and_difference_family_equivalence(self) -> None:
        result = verify_difference_family_equivalence()
        self.assertEqual(result["blocks"], 24)
        self.assertEqual(result["block_size"], 3)
        self.assertEqual(result["intersection_totals"], (18, 18, 18, 18))
        self.assertEqual(result["signature_sum"], (0, 0, 0, 0))
        self.assertEqual(result["lifted_catalog_word"], CATALOG_WITNESS)

    def test_expansion_compression_and_pure_axis(self) -> None:
        result = verify_expansion_and_pure_axis()
        self.assertEqual(result["shape"], (9, 37))
        self.assertEqual(result["classes"], 12)
        self.assertEqual(result["class_size"], 3)
        self.assertEqual(result["full_phase_sum"], (1, 0))
        self.assertEqual(result["binary_sums"], (1, 1))
        self.assertEqual(result["row_sums"], CATALOG_WITNESS)
        self.assertEqual(result["row_sum_profile"], (297,) + (-37,) * 8)
        self.assertEqual(
            result["zero_column_lag_profile"], (333,) + (-1,) * 8
        )

    def test_residual_matrix_proves_non_candidate_status(self) -> None:
        result = verify_nonzero_class_residuals()
        self.assertEqual(result["residuals"], EXPECTED_NONZERO_CLASS_RESIDUALS)
        self.assertEqual(result["reversal_independent_equations"], 54)
        self.assertEqual(result["bad_equations"], 51)
        self.assertEqual(result["residual_energy"], 8_320)
        self.assertEqual(result["max_abs_residual"], 30)
        self.assertEqual(result["weighted_row_residual_sums"], (0,) * 5)
        self.assertEqual(result["nonzero_column_axis_bad_classes"], 6)
        self.assertFalse(result["is_lp333_candidate"])


if __name__ == "__main__":
    unittest.main()
