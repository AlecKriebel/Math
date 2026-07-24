#!/usr/bin/env python3
"""Dependency-free tests for the exact primitive-nine trit lift."""

from __future__ import annotations

from itertools import product
from math import comb
import unittest

from verify_lp333_order3_trit_lift import (
    PINNED_PROFILES,
    TRIT_SURVIVOR_MASKS_A,
    TRIT_SURVIVOR_MASKS_B,
    affine_upper_system,
    normalized_mask_from_profile_trits,
    profile_from_normalized_mask,
    profiles_from_masks,
    trits_from_masks,
    verify_pinned_trit_linearization,
)


class OrderThreeTritLiftTests(unittest.TestCase):
    def test_profile_trits_biject_with_all_local_placements(self) -> None:
        profiles = tuple(
            (first, second, 3 - first - second)
            for first in range(4)
            for second in range(4)
            if 0 <= 3 - first - second <= 3
        )
        self.assertEqual(len(profiles), 10)
        for profile in profiles:
            active_count = sum(count in (1, 2) for count in profile)
            masks = {
                normalized_mask_from_profile_trits(profile, trits)
                for trits in product(range(3), repeat=active_count)
            }
            self.assertEqual(
                len(masks),
                comb(3, profile[0])
                * comb(3, profile[1])
                * comb(3, profile[2]),
            )
            self.assertTrue(
                all(profile_from_normalized_mask(mask) == profile for mask in masks)
            )

    def test_pinned_upper_system_has_exact_rank_eighteen(self) -> None:
        result = verify_pinned_trit_linearization()
        self.assertEqual(result["active_trits"], 54)
        self.assertEqual(result["physical_equation_coordinates"], 39)
        self.assertEqual(result["affine_rank"], 18)
        self.assertEqual(result["affine_nullity"], 36)
        self.assertTrue(result["consistent"])
        self.assertEqual(result["local_assignments"], 352)
        self.assertEqual(result["upper_deltas"], 54)
        self.assertEqual(result["square_zero_products"], 2_916)
        self.assertEqual(result["replayed_jet_equations"], 222)

    def test_independently_found_trit_certificate_satisfies_system(self) -> None:
        self.assertEqual(
            profiles_from_masks(
                TRIT_SURVIVOR_MASKS_A,
                TRIT_SURVIVOR_MASKS_B,
            ),
            PINNED_PROFILES,
        )
        trits = trits_from_masks(
            PINNED_PROFILES,
            TRIT_SURVIVOR_MASKS_A,
            TRIT_SURVIVOR_MASKS_B,
        )
        self.assertTrue(affine_upper_system(PINNED_PROFILES).accepts(trits))


if __name__ == "__main__":
    unittest.main()
