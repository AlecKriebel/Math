#!/usr/bin/env python3
"""Tests for the characteristic-37 order-three transfer theorem."""

from __future__ import annotations

import unittest

from verify_lp333_order3_char37_transfer import (
    EXPECTED_FIXTURE_HASH,
    EXPECTED_PAIRED_WITNESS_HASH,
    EXPECTED_TRANSFER_HASH,
    TRANSFER_FACTORS,
    verify_fixture_equivalence,
    verify_paired_layer_witnesses,
    verify_transfer_linear_algebra,
)


class Characteristic37TransferTests(unittest.TestCase):
    def test_transfer_linear_algebra(self) -> None:
        result = verify_transfer_linear_algebra()
        self.assertEqual(result["dimension"], 13)
        self.assertEqual(result["rank"], 13)
        self.assertEqual(result["determinant"], 11)
        self.assertEqual(result["transfer_hash"], EXPECTED_TRANSFER_HASH)
        self.assertEqual(TRANSFER_FACTORS[:3], (1, 19, 35))

    def test_physical_and_cyclotomic_equivalence(self) -> None:
        result = verify_fixture_equivalence()
        self.assertEqual(result["fixtures"], 373)
        self.assertEqual(result["fixture_hash"], EXPECTED_FIXTURE_HASH)
        self.assertEqual(result["physical_transfer_checks"], 373)
        self.assertEqual(result["cyclotomic_equations_per_fixture"], 12)

    def test_paired_layer_witnesses(self) -> None:
        result = verify_paired_layer_witnesses()
        self.assertEqual(result["aggregate_shards"], 22)
        self.assertEqual(result["surviving_first_two_coefficients"], 22)
        self.assertEqual(
            result["higher_bad_histogram"],
            ((6, 1), (8, 7), (9, 14)),
        )
        self.assertEqual(
            result["paired_witness_hash"],
            EXPECTED_PAIRED_WITNESS_HASH,
        )
        self.assertFalse(result["is_full_mod37_witness"])


if __name__ == "__main__":
    unittest.main()
