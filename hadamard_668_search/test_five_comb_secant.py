#!/usr/bin/env python3
"""Regression tests for the finite five-comb carrier classification."""

from __future__ import annotations

import unittest

from verify_five_comb_secant import (
    autocorrelation_sum,
    complementary_multiset_count,
    complementary_quartets,
    polarized_carriers,
    quartet_symmetry_representatives,
)


class FiveCombFamilyTests(unittest.TestCase):
    def test_small_family_counts(self) -> None:
        self.assertEqual(
            tuple(complementary_multiset_count(size) for size in range(1, 9)),
            (0, 0, 0, 48, 0, 0, 0, 1_246),
        )

    def test_quartet_orbits(self) -> None:
        self.assertEqual(len(complementary_quartets()), 48)
        self.assertEqual(len(quartet_symmetry_representatives()), 17)

    def test_every_quartet_gives_flat_32_channel_family(self) -> None:
        for quartet in complementary_quartets():
            carriers = polarized_carriers(quartet) * 4
            self.assertEqual(
                tuple(autocorrelation_sum(carriers, lag) for lag in range(59)),
                (320,) + (0,) * 58,
            )


if __name__ == "__main__":
    unittest.main()
