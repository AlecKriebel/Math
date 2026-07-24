#!/usr/bin/env python3
"""Regression tests for the higher-digit certificate and lattice."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import solve_lambda_prefix_sat as prefix
import verify_bounded_search_checkpoints as checkpoints
import verify_digit2_row7_census as census
import verify_full_second_digit_witness as witness
import verify_stage_2_5_witnesses as stage_2_5


class HigherDigitTests(unittest.TestCase):
    def test_prefix_lattice(self) -> None:
        self.assertEqual(prefix.prefix_lattice(0), (1, 3))
        self.assertEqual(prefix.prefix_lattice(1), (3, None))
        self.assertEqual(prefix.prefix_lattice(2), (3, 9))
        self.assertEqual(prefix.prefix_lattice(3), (9, None))
        self.assertEqual(prefix.prefix_lattice(4), (9, 27))
        self.assertEqual(prefix.prefix_lattice(5), (27, None))
        self.assertEqual(prefix.prefix_lattice(8), (81, 243))

    def test_integral_lattice_matches_exact_digits(self) -> None:
        for first in range(-18, 19):
            for second_value in range(-18, 19):
                digits = prefix.second.lambda_digits(
                    (first, second_value), 9
                )
                for maximum_digit in range(9):
                    coordinate_modulus, sum_modulus = (
                        prefix.prefix_lattice(maximum_digit)
                    )
                    lattice = (
                        first % coordinate_modulus == 0
                        and second_value % coordinate_modulus == 0
                        and (
                            sum_modulus is None
                            or (first + second_value) % sum_modulus == 0
                        )
                    )
                    direct = all(
                        digits[index] == 0
                        for index in range(maximum_digit + 1)
                    )
                    self.assertEqual(lattice, direct)

    def test_witness(self) -> None:
        result = witness.audit()
        self.assertEqual(result["zero_digit_prefix"], 3)
        self.assertEqual(result["digit_3_nonzero_rows"], 17)
        self.assertEqual(
            result["proper_supergroup_fixed"],
            (False, False, False, False, False),
        )
        self.assertEqual(
            result["exactness_cutoff"]["maximum_lambda_valuation"], 8
        )
        self.assertEqual(
            result["exactness_cutoff"][
                "digits_sufficient_for_exact_zero"
            ],
            9,
        )

    def test_bounded_checkpoints(self) -> None:
        result = checkpoints.audit()
        self.assertEqual(result["digit_3_objectives"], (9, 5, 8, 8, 9))
        self.assertEqual(result["digit_4_objective"], 17)
        self.assertEqual(result["localized_stage_2_5_objective"], 11)
        self.assertEqual(result["row_margin_digit_2_union"], "UNKNOWN")
        self.assertEqual(result["row_margin_digit_2_shards"], 8)
        self.assertEqual(
            result["row_margin_permutation_objective"], (2, 9)
        )
        self.assertEqual(result["all_statuses"], "UNKNOWN")

    def test_stage_2_5_witnesses(self) -> None:
        result = stage_2_5.audit()
        self.assertEqual(result["bounded_digit_2_hits"], 9)
        self.assertEqual(result["bounded_stage_2_5_hits"], 2)
        self.assertEqual(result["viable_stage_2_5_hits"], 0)
        self.assertEqual(
            tuple(
                point["digit_3_nonzero_rows"]
                for point in result["witnesses"]
            ),
            (11, 16),
        )
        self.assertFalse(
            any(
                point["row_margin_join_holds"]
                for point in result["witnesses"]
            )
        )

    def test_digit_2_census(self) -> None:
        result = census.audit()
        self.assertEqual(result["total_digit_2_hits"], 9)
        self.assertEqual(result["total_stage_2_5_hits"], 2)
        self.assertEqual(result["total_row_margin_compatible_hits"], 0)


if __name__ == "__main__":
    unittest.main()
