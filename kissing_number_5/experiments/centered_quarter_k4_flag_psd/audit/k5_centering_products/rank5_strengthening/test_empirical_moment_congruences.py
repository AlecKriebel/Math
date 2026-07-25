#!/usr/bin/env python3
"""Tests for the combined raw empirical moment verifier."""

from __future__ import annotations

import unittest

from verify_empirical_moment_congruences import (
    UNORDERED_TRIPLE_TOTAL,
    h1_from_raw_pair_counts,
    h2_from_raw_data,
    self_test,
    synthetic_pair_counts,
)


class EmpiricalMomentCongruenceTest(unittest.TestCase):
    def test_complete_self_test(self) -> None:
        self_test()

    def test_control_values(self) -> None:
        counts = synthetic_pair_counts()
        _, x1 = h1_from_raw_pair_counts(counts)
        _, _, x2, y2 = h2_from_raw_data(
            counts,
            [64] * UNORDERED_TRIPLE_TOTAL,
        )
        self.assertEqual(x1, 20972)
        self.assertEqual(x2 % 210, 82)
        self.assertEqual((x2 - 21 * x1 - 40) % 2100, 0)
        self.assertEqual(y2 % 210, 66)
        self.assertEqual((y2 - 10 * x2 - 2) % 49, 0)


if __name__ == "__main__":
    unittest.main()
