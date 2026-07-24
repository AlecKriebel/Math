#!/usr/bin/env python3
"""Focused tests for the order-three primitive-nine ramified jet."""

from __future__ import annotations

import unittest

from verify_lp333_order3_primitive9_jet import (
    EXPECTED_STRICTNESS_HASH,
    EXPECTED_WORD_JET_HASH,
    verify_digit_one_equivalence,
    verify_ramified_ring,
    verify_strict_higher_digits,
    verify_word_jets,
    verify_zero_column,
)


class OrderThreePrimitiveNineJetTests(unittest.TestCase):
    def test_ramified_ring(self) -> None:
        result = verify_ramified_ring()
        self.assertEqual(result["jet_ring"], "F3[pi]/(pi^6)")
        self.assertEqual(result["defect"], 162)
        self.assertEqual(result["defect_pi_valuation"], 24)

    def test_zero_column(self) -> None:
        result = verify_zero_column()
        self.assertEqual(result["primitive9_reciprocal_power"], 5)
        self.assertEqual(
            result["combined_correlation"],
            (10, 5, 5, 5, 5, 5, 5, 5, 5),
        )

    def test_word_jet_exhaustion(self) -> None:
        result = verify_word_jets()
        self.assertEqual(result["weight_three_words"], 84)
        self.assertEqual(result["word_jet_hash"], EXPECTED_WORD_JET_HASH)

    def test_digit_one_is_eisenstein_sieve(self) -> None:
        result = verify_digit_one_equivalence()
        self.assertEqual(result["profile_quadruples"], 10_000)
        self.assertEqual(result["coefficient_one_survivors"], 3_334)
        self.assertTrue(result["matches_eisenstein_pair_sieve"])

    def test_higher_digits_are_strict(self) -> None:
        result = verify_strict_higher_digits()
        self.assertEqual(result["origin_energy"], 54)
        self.assertEqual(result["coefficient_one_pairs"], 6)
        self.assertGreaterEqual(result["first_failing_digit"], 2)
        self.assertEqual(result["strictness_hash"], EXPECTED_STRICTNESS_HASH)
        self.assertFalse(result["is_lp333_candidate"])


if __name__ == "__main__":
    unittest.main()
