#!/usr/bin/env python3
"""Tests for the exact LP(333) endpoint-profile exclusion."""

from __future__ import annotations

import unittest

import verify_lp333_order3_profile_endpoint_shell as endpoint


class ProfileEndpointShellTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = endpoint.verify_endpoint_shell()

    def test_local_modulo_nine_reduction(self) -> None:
        self.assertEqual(
            self.result["local_quartets_per_opposite_pair"],
            (40,) * 6,
        )
        self.assertEqual(
            self.result["local_high_count_histogram"],
            ((0, 1), (2, 12), (4, 27)),
        )

    def test_complete_aggregate_census(self) -> None:
        self.assertEqual(self.result["row_sum_target_count"], 22)
        self.assertEqual(self.result["candidate_count"], 288)
        self.assertEqual(
            self.result["surviving_target_counts"],
            (
                ((-3, 0, -3, -3), 72),
                ((-3, 0, 0, 3), 72),
                ((3, 0, 0, -3), 72),
                ((3, 0, 3, 3), 72),
            ),
        )

    def test_symmetry_quotient(self) -> None:
        self.assertEqual(self.result["symmetry_orbit_count"], 12)
        self.assertEqual(self.result["symmetry_orbit_sizes"], (24,) * 12)

    def test_exact_exclusion(self) -> None:
        self.assertEqual(
            self.result["bad_class_histogram"],
            ((10, 24), (12, 264)),
        )
        self.assertEqual(
            self.result["representative_bad_class_histogram"],
            ((10, 1), (12, 11)),
        )
        self.assertEqual(self.result["exact_profile_count"], 0)
        self.assertTrue(self.result["endpoint_excluded"])
        self.assertEqual(
            self.result["certificate_sha256"],
            endpoint.EXPECTED_ENDPOINT_CERTIFICATE_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
