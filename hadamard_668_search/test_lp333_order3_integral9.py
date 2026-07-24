#!/usr/bin/env python3
"""Focused tests for the exact integral primitive-nine sieve."""

from __future__ import annotations

import unittest

from verify_lp333_order3_integral9 import (
    EXPECTED_PINNED_TABLE_SHA256,
    EXPECTED_TRIT_TABLE_SHA256,
    audit_known_modular_survivors,
    equidistribution_remainder,
    invariant_correlation_table,
    primitive9_remainder,
    validate_integral_primitive9,
    verify_divisibility_criterion,
)
from verify_lp333_order3_labeled_jet import (
    LABELLED_SURVIVOR_AGGREGATE,
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
)


class OrderThreeIntegralNineTests(unittest.TestCase):
    def test_phi9_divisibility_is_triple_equidistribution(self) -> None:
        result = verify_divisibility_criterion()
        self.assertEqual(
            result["cyclotomic_polynomial"],
            (1, 0, 0, 1, 0, 0, 1),
        )
        self.assertEqual(result["test_vectors"], 21)
        self.assertEqual(result["equidistribution_groups"], 3)
        self.assertEqual(result["integer_equations_per_column_class"], 6)
        divisible = (5, 7, 11, 5, 7, 11, 5, 7, 11)
        self.assertEqual(primitive9_remainder(divisible), (0,) * 6)
        self.assertEqual(equidistribution_remainder(divisible), (0,) * 6)

    def test_known_modular_survivors_fail_integrally(self) -> None:
        result = audit_known_modular_survivors()
        pinned = result["pinned"]
        trit = result["trit"]
        self.assertEqual(
            pinned["correlation_table_sha256"],
            EXPECTED_PINNED_TABLE_SHA256,
        )
        self.assertEqual(
            trit["correlation_table_sha256"],
            EXPECTED_TRIT_TABLE_SHA256,
        )
        self.assertEqual(pinned["bad_equidistribution_groups"], 36)
        self.assertEqual(trit["bad_equidistribution_groups"], 36)
        self.assertEqual(pinned["nonzero_integer_equations"], 59)
        self.assertEqual(trit["nonzero_integer_equations"], 66)
        self.assertEqual(pinned["maximum_absolute_defect"], 24)
        self.assertEqual(trit["maximum_absolute_defect"], 21)
        self.assertEqual(pinned["defect_gcd"], 3)
        self.assertEqual(trit["defect_gcd"], 3)
        self.assertTrue(pinned["all_defects_divisible_by_three"])
        self.assertTrue(trit["all_defects_divisible_by_three"])
        self.assertFalse(pinned["exact_integral_survivor"])
        self.assertFalse(trit["exact_integral_survivor"])

    def test_zero_column_class_is_already_exact(self) -> None:
        table = invariant_correlation_table(
            LABELLED_SURVIVOR_MASKS_A,
            LABELLED_SURVIVOR_MASKS_B,
        )
        self.assertEqual(table[0], (167,) * 9)
        with self.assertRaisesRegex(
            ValueError, "exact primitive-nine equidistribution failed"
        ):
            validate_integral_primitive9(
                LABELLED_SURVIVOR_AGGREGATE,
                LABELLED_SURVIVOR_MASKS_A,
                LABELLED_SURVIVOR_MASKS_B,
            )


if __name__ == "__main__":
    unittest.main()
