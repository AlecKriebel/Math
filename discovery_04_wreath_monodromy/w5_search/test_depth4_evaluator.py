#!/usr/bin/env python3
"""Regression tests for the depth-agnostic quotient-tower evaluator."""

from __future__ import annotations

import unittest

from finite_field_norm_depth4 import deepest_norm, tower_profile


class DepthFourEvaluatorTests(unittest.TestCase):
    def test_depth_three_reproduces_banked_w4_certificate(self) -> None:
        self.assertEqual(
            tower_profile(1009, 801, inverse_depth=3),
            {
                "dimension": 27,
                "discriminant_norms": (497, 650, 840, 0),
                "leading_norms": (2, 511, 972, 127),
                "reconstruction_guard_norms": (
                    763,
                    881,
                    827,
                    437,
                    517,
                    668,
                    247,
                    706,
                    985,
                ),
            },
        )

    def test_fast_path_matches_full_profile_at_depth_four(self) -> None:
        profile = tower_profile(7, 3, inverse_depth=4)
        self.assertEqual(profile["dimension"], 81)
        self.assertEqual(
            deepest_norm(7, 3, inverse_depth=4),
            profile["discriminant_norms"][-1],
        )

    def test_depth_zero_is_the_target_discriminant(self) -> None:
        profile = tower_profile(23, 3, inverse_depth=0)
        self.assertEqual(profile["dimension"], 1)
        self.assertEqual(profile["discriminant_norms"], (10,))
        self.assertEqual(deepest_norm(23, 3, inverse_depth=0), 10)


if __name__ == "__main__":
    unittest.main()
