#!/usr/bin/env python3
"""Tests for the exact prime-167 invariant-algebra split."""

from __future__ import annotations

import unittest

import verify_lp333_order3_prime167_split as split


class Prime167SplitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = split.verify()

    def test_equality_case_and_fixed_profile_corpus(self) -> None:
        equality = self.result["equality_case"]
        corpus = self.result["profile_corpus"]
        self.assertEqual(
            equality["certificate_sha256"],
            split.EXPECTED_EQUALITY_CASE_SHA256,
        )
        self.assertEqual(equality["root_of_unity_intersection_order"], 1)
        self.assertFalse(equality["energy_divisible_by_shift_order"])
        self.assertEqual(corpus["energy_shell_fixtures"], 22)
        self.assertEqual(corpus["prime167_modular_survivors"], 0)
        self.assertEqual(corpus["exact_profile_survivors"], 0)
        self.assertEqual(corpus["aggregate_shard_exclusions"], 0)

    def test_field_split_and_star(self) -> None:
        field = self.result["field_split"]
        star = self.result["star_and_crt"]
        self.assertEqual(
            field["certificate_sha256"],
            split.EXPECTED_FIELD_SPLIT_SHA256,
        )
        self.assertEqual(field["full_primitive_factor_degrees_over_k"], (18, 18))
        self.assertEqual(field["invariant_primitive_degrees_over_k"], (6, 6))
        self.assertEqual(field["factor_irreducible"], (True, True))
        self.assertEqual(field["period_basis_ranks"], (6, 6))
        self.assertEqual(
            (
                star["plus_star_frobenius_exponent"],
                star["minus_star_frobenius_exponent"],
            ),
            (5, 7),
        )
        self.assertEqual(star["star_exponent_sum_mod_12"], 0)
        self.assertEqual(star["roundtrip_fixtures"], 6)

    def test_complete_solution_counts(self) -> None:
        result = self.result["parameterization"]
        expected_trivial = 1 + (split.P**2 - 1) * (split.P + 1)
        expected_primitive = (
            split.E_SIZE**2 + (split.E_SIZE**2 - 1) * split.E_SIZE
        )
        self.assertTrue(result["parameterization_complete"])
        self.assertEqual(result["trivial_branches"], ("zero", "nonzero"))
        self.assertEqual(
            result["primitive_branches"],
            ("degenerate", "nondegenerate"),
        )
        self.assertEqual(result["norm_minus_one_ratio_count"], split.P + 1)
        self.assertEqual(result["trivial_solution_count"], expected_trivial)
        self.assertEqual(result["primitive_solution_count"], expected_primitive)
        self.assertEqual(result["nondegenerate_parameter_fixtures"], 7)
        self.assertEqual(result["degenerate_parameter_fixtures"], 3)
        self.assertEqual(
            result["full_solution_count"],
            expected_trivial * expected_primitive,
        )
        self.assertEqual(result["solution_branch_fixtures"], 4)
        self.assertEqual(
            result["certificate_sha256"],
            split.EXPECTED_PARAMETER_FIXTURE_SHA256,
        )

    def test_trivial_zero_and_nonzero_recovery(self) -> None:
        self.assertEqual(
            split.recover_trivial_parameters(split.K_ZERO, split.K_ZERO),
            ("zero",),
        )
        coordinates = split.trivial_parameterization(
            (9, 14),
            split.TRIVIAL_NORM_MINUS_ONE_RATIO,
        )
        recovered = split.recover_trivial_parameters(*coordinates)
        self.assertEqual(recovered[0], "nonzero")
        self.assertEqual(recovered[1], (9, 14))
        self.assertEqual(
            recovered[2],
            split.TRIVIAL_NORM_MINUS_ONE_RATIO,
        )
        with self.assertRaises(ValueError):
            split.trivial_parameterization(split.K_ONE, split.K_ONE)
        with self.assertRaises(ValueError):
            split.trivial_parameterization(
                split.K_ZERO,
                split.TRIVIAL_NORM_MINUS_ONE_RATIO,
            )

    def test_primitive_degenerate_and_nondegenerate_recovery(self) -> None:
        free_a = split.field_fixture(91)
        free_b = split.field_fixture(92)
        minus_a, minus_b = split.primitive_degenerate_parameterization(
            free_a, free_b
        )
        self.assertEqual(
            split.recover_primitive_parameters(
                split.L_ZERO,
                minus_a,
                split.L_ZERO,
                minus_b,
            ),
            ("degenerate", free_a, free_b),
        )

        plus_a = split.field_fixture(93)
        plus_b = split.field_fixture(94)
        tau = split.field_fixture(95)
        minus_a, minus_b = split.primitive_parameterization(
            plus_a, plus_b, tau
        )
        self.assertEqual(
            split.recover_primitive_parameters(
                plus_a,
                minus_a,
                plus_b,
                minus_b,
            ),
            ("nondegenerate", tau),
        )
        axis = split.field_fixture(96)
        for plus_a, plus_b in (
            (axis, split.L_ZERO),
            (split.L_ZERO, axis),
        ):
            minus_a, minus_b = split.primitive_parameterization(
                plus_a, plus_b, tau
            )
            self.assertEqual(
                split.recover_primitive_parameters(
                    plus_a,
                    minus_a,
                    plus_b,
                    minus_b,
            ),
            ("nondegenerate", tau),
        )

        axis_value = split.field_fixture(96)
        for axis_a, axis_b in (
            (axis_value, split.L_ZERO),
            (split.L_ZERO, axis_value),
        ):
            axis_minus_a, axis_minus_b = split.primitive_parameterization(
                axis_a, axis_b, tau
            )
            self.assertEqual(
                split.recover_primitive_parameters(
                    axis_a,
                    axis_minus_a,
                    axis_b,
                    axis_minus_b,
                ),
                ("nondegenerate", tau),
            )
        with self.assertRaises(ValueError):
            split.primitive_parameterization(
                split.L_ZERO,
                split.L_ZERO,
                split.L_ZERO,
            )


if __name__ == "__main__":
    unittest.main()
