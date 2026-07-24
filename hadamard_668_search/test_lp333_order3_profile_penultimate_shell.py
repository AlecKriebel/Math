#!/usr/bin/env python3
"""Tests for the exact LP(333) penultimate profile-shell exclusion."""

from __future__ import annotations

import unittest

import verify_lp333_order3_profile_penultimate_shell as penultimate


class ProfilePenultimateShellTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = penultimate.verify_penultimate_shell()

    def test_universal_quartet_localization(self) -> None:
        self.assertEqual(
            self.result["legal_quartet_weight_histogram"],
            (
                ((0, 0), 1),
                ((0, 1), 12),
                ((0, 2), 54),
                ((0, 3), 108),
                ((0, 4), 81),
                ((2, 0), 108),
                ((2, 1), 648),
                ((2, 2), 972),
                ((3, 0), 216),
                ((3, 1), 648),
                ((4, 0), 486),
            ),
        )
        self.assertEqual(self.result["medium_frame_count"], 1_296)
        self.assertEqual(self.result["medium_frame_target_count"], 1_944)

    def test_medium_frame_symmetry_quotient(self) -> None:
        self.assertEqual(
            self.result["medium_frame_target_counts"],
            (
                ((-3, -3, -4, -2), 324),
                ((-3, -3, -2, 2), 324),
                ((0, 3, -4, -2), 324),
                ((0, 3, -2, 2), 324),
                ((4, -1, 0, 0), 324),
                ((5, 1, 0, 0), 324),
            ),
        )
        self.assertEqual(
            self.result["medium_frame_target_orbit_count"],
            90,
        )
        self.assertEqual(
            self.result["medium_frame_target_orbit_sizes"],
            ((12, 18), (24, 72)),
        )
        self.assertEqual(
            self.result["universal_symmetry_monomial_checks"],
            2_200_368,
        )

    def test_complete_affine_modulo_nine_census(self) -> None:
        self.assertEqual(self.result["pre_mod9_count"], 34_634_136)
        self.assertEqual(
            self.result["pre_mod9_target_counts"],
            (
                ((-3, -3, -4, -2), 5_748_834),
                ((-3, -3, -2, 2), 5_748_834),
                ((0, 3, -4, -2), 5_748_834),
                ((0, 3, -2, 2), 5_748_834),
                ((4, -1, 0, 0), 5_819_400),
                ((5, 1, 0, 0), 5_819_400),
            ),
        )
        self.assertEqual(
            self.result["representative_mod9_survivor_count"],
            30,
        )
        self.assertEqual(self.result["post_mod9_count"], 552)
        self.assertEqual(
            self.result["post_mod9_target_counts"],
            (
                ((-3, -3, -4, -2), 42),
                ((-3, -3, -2, 2), 42),
                ((0, 3, -4, -2), 42),
                ((0, 3, -2, 2), 42),
                ((4, -1, 0, 0), 192),
                ((5, 1, 0, 0), 192),
            ),
        )

    def test_detached_exact_exclusion(self) -> None:
        self.assertEqual(self.result["physical_lags_replayed"], 20_424)
        self.assertEqual(
            self.result["bad_class_histogram"],
            ((6, 24), (10, 144), (12, 384)),
        )
        self.assertEqual(self.result["exact_profile_count"], 0)
        self.assertTrue(self.result["shell_excluded"])
        self.assertEqual(self.result["constructor_cut"], "n_9 <= 4")
        self.assertEqual(
            self.result["certificate_sha256"],
            penultimate.EXPECTED_CERTIFICATE_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
