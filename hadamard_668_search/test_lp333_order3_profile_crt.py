#!/usr/bin/env python3
"""Tests for the LP(333) profile local-global CRT theorem."""

from __future__ import annotations

import unittest

import verify_lp333_order3_profile_crt as theorem


class ProfileCrtTest(unittest.TestCase):
    def test_ideal_arithmetic_and_threshold(self) -> None:
        result = theorem.verify_ideal_arithmetic()
        self.assertEqual(result["first_sufficient_lambda_power"], 3)
        self.assertEqual(result["lambda_squared_kernel_minimum_norm"], 12321)
        self.assertEqual(result["lambda_cubed_kernel_minimum_norm"], 36963)
        self.assertEqual(result["cauchy_norm_bound"], 27889)
        self.assertEqual(result["kernel_points_in_cauchy_disk"], ((0, 0),))

    def test_explicit_crt_quotients(self) -> None:
        for quotient in ((0, 0), (1, 0), (0, 1), (-3, 2), (5, -4)):
            value = theorem.e_multiply(
                theorem.CRT_KERNEL_GENERATOR, quotient
            )
            self.assertEqual(theorem.crt_kernel_quotient(value), quotient)
        self.assertIsNone(theorem.crt_kernel_quotient((37, 0)))
        self.assertIsNone(theorem.crt_kernel_quotient((3, -3)))

    def test_characteristic37_transfer_equivalence(self) -> None:
        _, identifiers_a, identifiers_b = (
            theorem.PROFILE9_SHARD_WITNESSES[0]
        )
        result = theorem.verify_characteristic37_equivalence(
            identifiers_a, identifiers_b
        )
        self.assertFalse(result["physical_zero_mod_37"])
        self.assertFalse(result["transfer_zero_mod_37"])
        basis = theorem.verify_characteristic37_basis_orientation()
        self.assertEqual(basis["basis_orientation_checks"], 26)

    def test_profile_corpus(self) -> None:
        result = theorem.verify_profile_corpus()
        self.assertEqual(result["transfer_rank"], 13)
        self.assertEqual(result["fixed_profile_tuples"], 22)
        self.assertEqual(result["lambda_cube_survivors"], 22)
        self.assertEqual(result["characteristic37_survivors"], 0)
        self.assertEqual(result["exact_zero_survivors"], 0)
        self.assertEqual(result["aggregate_shard_exclusions"], 0)


if __name__ == "__main__":
    unittest.main()
