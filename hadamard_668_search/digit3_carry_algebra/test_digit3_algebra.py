#!/usr/bin/env python3
"""Pinned dependency-free tests for the digit-3 carry research."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import audit_digit3_carry as carry
import audit_digit3_xl as xl
import verify_e1_origin_exact_dp as e1_exact


class DigitThreeCarryTests(unittest.TestCase):
    def test_exact_carry_identity_and_delayed_row(self) -> None:
        result = carry.audit()
        self.assertEqual(
            carry.compact_hash(result),
            "a862b985fac4fe153465e03fdda51b82d"
            "eccdb9020c82aff5600d9c96b68d427",
        )
        self.assertEqual(
            result["exact_coordinate_identity"],
            "F=A+(3Q-A)omega",
        )
        self.assertEqual(
            result["jacobian_at_witness"],
            {
                "quadratic_rank": 18,
                "cubic_rank": 19,
                "combined_rank": 36,
                "combined_shape": (37, 36),
                "newton_correction": None,
            },
        )
        delayed = result["delayed_e1_origin"]
        self.assertEqual(delayed["raw_grouped_forms"], 42)
        self.assertEqual(
            delayed["digit3"]["remaining_affine_dimension"], 35
        )
        self.assertEqual(
            delayed["digit4_after_digit3"][
                "polar_rank_on_digit3_hyperplane"
            ],
            14,
        )

    def test_exact_e1_origin_orientation_count(self) -> None:
        result = e1_exact.audit()
        self.assertEqual(
            e1_exact.compact_hash(result),
            "0f5d0a8dc5364cd1c9d440d14b08a9c9"
            "bc40ad698c5dd207f841b828cd1dce83",
        )
        self.assertEqual(result["admissible_histogram_pairs"], 30)
        self.assertEqual(
            result["exact_orientation_solutions"], 596_095_200
        )
        self.assertEqual(result["orientation_space"], 3**22)

    def test_degree_three_xl_rank(self) -> None:
        result = xl.audit()
        self.assertEqual(
            xl.compact_hash(result),
            "a92083fcb42ba0d9745bc7907b26e5238"
            "04a7ee49f05e5f272bbc009db637bd6",
        )
        self.assertEqual(result["xl_rows"], 666)
        self.assertEqual(result["monomials"]["total"], 8401)
        self.assertEqual(
            result["ranks"],
            {
                "original_quadric_span": 18,
                "full_xl": 666,
                "cubic_projection": 648,
                "quadratic_or_lower_intersection": 18,
                "linear_or_lower_intersection": 0,
                "constant_only_intersection": 0,
                "new_quadratic_or_lower_beyond_original_span": 0,
            },
        )
        self.assertEqual(
            result["conclusions"],
            {
                "degree_3_refutation": False,
                "new_linear_consequence": False,
                "new_quadratic_consequence": False,
            },
        )


if __name__ == "__main__":
    unittest.main()
