#!/usr/bin/env python3
"""Focused regressions for the sparse-B relative-norm certificate."""

from __future__ import annotations

import unittest

from verify_lp333_order3_sparse_b_norm import (
    EXPECTED_CERTIFICATE_SHA256,
    NORM_TYPES,
    verify,
)


class SparseBNormTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = verify()

    def test_orbit_and_raw_counts(self) -> None:
        self.assertEqual(self.result["raw_words"], 396)
        self.assertEqual(len(self.result["lift_safe_orbit_sizes"]), 34)
        self.assertEqual(len(self.result["field_orbit_sizes"]), 17)
        self.assertEqual(self.result["obstructed_raw_words"], 312)
        self.assertEqual(self.result["surviving_raw_words"], 84)

    def test_four_relative_norm_types(self) -> None:
        survivors = tuple(
            (entry.separation, entry.value)
            for entry in NORM_TYPES
            if entry.status == "relative_norm"
        )
        self.assertEqual(
            survivors,
            (
                (1, (-1, -2)),
                (3, (-2, -1)),
                (6, (-2, -1)),
                (6, (-1, -2)),
            ),
        )
        self.assertEqual(self.result["surviving_lift_safe_orbits"], 8)

    def test_local_obstruction_split(self) -> None:
        statuses = tuple(row["status"] for row in self.result["rows"])
        self.assertEqual(statuses.count("inert_11"), 12)
        self.assertEqual(statuses.count("inert_101"), 1)
        self.assertEqual(statuses.count("relative_norm"), 4)
        self.assertFalse(
            any(
                row["p11_simple_primes"]
                or row["p101_simple_primes"]
                for row in self.result["rows"]
                if row["status"] == "relative_norm"
            )
        )

    def test_certificate_hash(self) -> None:
        self.assertTrue(EXPECTED_CERTIFICATE_SHA256)
        self.assertEqual(
            self.result["certificate_sha256"],
            EXPECTED_CERTIFICATE_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
