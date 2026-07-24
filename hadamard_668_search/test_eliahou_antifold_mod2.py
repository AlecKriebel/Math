#!/usr/bin/env python3
"""Focused tests for the binary anti-fold lift."""

from __future__ import annotations

import unittest

import verify_eliahou_antifold_mod2 as mod2


class EliahouAntifoldMod2Tests(unittest.TestCase):
    def test_pair_sum_difference_norm_transform(self) -> None:
        mod2.verify_pair_transform()

    def test_all_first_bit_systems_have_rank_21(self) -> None:
        histogram = {}
        for case in mod2.surviving_q_pairs():
            length, equations = mod2.first_bit_system(*case)
            rank = len(mod2.row_reduce(equations))
            histogram[(length, rank)] = histogram.get((length, rank), 0) + 1
        self.assertEqual(histogram, {(78, 21): 38, (79, 21): 1})

    def test_pinned_affine_weight_counts(self) -> None:
        for case, expected in mod2.EXPECTED_COUNTS.items():
            length, equations = mod2.first_bit_system(*case)
            basis = mod2.row_reduce(equations)
            self.assertEqual(
                mod2.affine_weight_count(
                    length, basis, length - mod2.TARGET_SUPPORT
                ),
                expected,
            )


if __name__ == "__main__":
    unittest.main()
