#!/usr/bin/env python3
"""Focused tests for the primitive-eight vertical-pair sieve."""

from __future__ import annotations

from collections import Counter
import unittest

from verify_five_comb_root12_sieve import ROOT_PROFILES, ROOT_PROFILE_COUNTS
from verify_five_comb_root8_vertical import (
    EXPECTED_CORE4_CLASS_SURVIVORS,
    EXPECTED_CORE4_RELATION_SHA256,
    EXPECTED_CORE4_SURVIVORS,
    EXPECTED_CORE27_RELATION_SHA256,
    EXPECTED_CORE27_SURVIVORS,
    EXPECTED_FEATURE_CLASS_COUNT,
    EXPECTED_FEATURE_COUNT,
    EXPECTED_INVENTORY_COUNT,
    inventory_catalog,
    rational_norm,
    sqrt2_coefficient,
    verify_primitive_eight_split,
)


class FiveCombRootEightVerticalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = inventory_catalog()

    def test_direct_primitive_eight_arithmetic(self) -> None:
        self.assertEqual(
            verify_primitive_eight_split(),
            {
                "split_checks": 625,
                "carrier_checks": 2_048,
                "hole_checks": 512,
            },
        )

    def test_refined_inventory_catalog(self) -> None:
        self.assertEqual(len(self.catalog["features"]), EXPECTED_FEATURE_COUNT)
        self.assertEqual(
            len(self.catalog["feature_classes"]),
            EXPECTED_FEATURE_CLASS_COUNT,
        )
        self.assertEqual(
            sum(self.catalog["feature_classes"].values()),
            EXPECTED_INVENTORY_COUNT,
        )
        profile_counts = Counter()
        for feature_class, multiplicity in self.catalog[
            "feature_classes"
        ].items():
            profile_counts[self.catalog["class_profile"][feature_class]] += (
                multiplicity
            )
        self.assertEqual(
            tuple(profile_counts[profile] for profile in ROOT_PROFILES),
            ROOT_PROFILE_COUNTS,
        )

    def test_norm_coefficient_split(self) -> None:
        even = ((1, 2), (3, 4), (-2, 1), (0, -3))
        odd = ((-1, 1), (2, -2), (3, 0), (-2, -1))
        self.assertEqual(rational_norm(even, odd), 68)
        self.assertEqual(sqrt2_coefficient(even, odd), 16)

    def test_retained_core_certificate_shapes(self) -> None:
        self.assertEqual(
            EXPECTED_CORE4_SURVIVORS,
            (4, 0, 12_307, 101_157, 26_543),
        )
        self.assertEqual(
            EXPECTED_CORE4_CLASS_SURVIVORS,
            (4, 0, 1_973, 11_528, 2_509),
        )
        self.assertEqual(len(EXPECTED_CORE4_RELATION_SHA256), 64)
        self.assertEqual(EXPECTED_CORE27_SURVIVORS, (27, 0, 0, 65_868, 0))
        self.assertEqual(len(EXPECTED_CORE27_RELATION_SHA256), 64)


if __name__ == "__main__":
    unittest.main()
