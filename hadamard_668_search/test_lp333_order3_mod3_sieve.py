#!/usr/bin/env python3
"""Regression tests for the LP(333) order-three Eisenstein reduction."""

from __future__ import annotations

import unittest

from verify_lp333_order3_mod3_sieve import (
    EXPECTED_MOD3_PAIR_HASH,
    EXPECTED_MOD3_SHARD_WITNESS_HASH,
    EXPECTED_PROFILE_HASH,
    EXPECTED_STATE_MULTIPLICITY_HASH,
    EXPECTED_T_SHARD_HASH,
    verify_equation_reduction,
    verify_local_fourier_identity,
    verify_mod3_pair_sieve,
    verify_profile_factorization,
    verify_t_shards,
)


class OrderThreeEisensteinTests(unittest.TestCase):
    def test_profile_factorization(self) -> None:
        result = verify_profile_factorization()
        self.assertEqual(result["profile_hash"], EXPECTED_PROFILE_HASH)
        self.assertEqual(result["profiles"], 10)
        self.assertEqual(result["profile_norm_histogram"], ((0, 1), (3, 6), (9, 3)))
        self.assertEqual(result["compressed_states_per_parity"], (100, 100))
        self.assertEqual(result["word_lifts_per_parity"], (7_056, 7_056))
        self.assertEqual(
            result["state_multiplicity_hash"],
            EXPECTED_STATE_MULTIPLICITY_HASH,
        )

    def test_local_fourier_identity(self) -> None:
        result = verify_local_fourier_identity()
        self.assertEqual(result["local_vectors"], 22)
        self.assertEqual(result["bilinear_checks"], 484)

    def test_equation_reduction(self) -> None:
        result = verify_equation_reduction()
        self.assertEqual(result["original_reversal_independent_equations"], 20)
        self.assertEqual(result["independent_integer_equations"], 13)
        self.assertEqual(result["linear_dependencies"], 7)
        self.assertEqual(result["binary_targets"], ((662, -6, -6), (-6, -6, -6)))
        self.assertEqual(result["qpsk_targets"], ((331, -3, -3), (-3, -3, -3)))

    def test_row_sum_shards(self) -> None:
        result = verify_t_shards()
        self.assertEqual(result["catalog_rows"], 1_756)
        self.assertEqual(result["aggregate_shards"], 22)
        self.assertEqual(
            result["norm_pair_census"],
            (
                ((19, 148), 4),
                ((28, 139), 4),
                ((64, 103), 2),
                ((91, 76), 8),
                ((100, 67), 2),
                ((163, 4), 2),
            ),
        )
        self.assertEqual(result["shard_hash"], EXPECTED_T_SHARD_HASH)

    def test_mod3_pair_sieve(self) -> None:
        result = verify_mod3_pair_sieve()
        self.assertEqual(
            result["pair_signatures"],
            (((0, 0), 34), ((1, 2), 33), ((2, 1), 33)),
        )
        self.assertEqual(result["raw_choices_per_negation_pair"], 10_000)
        self.assertEqual(result["survivors_per_negation_pair"], 3_334)
        self.assertEqual(
            result["sieved_six_pair_space"],
            1_373_389_026_282_611_799_616,
        )
        self.assertFalse(result["is_decisive"])
        self.assertEqual(result["mod3_hash"], EXPECTED_MOD3_PAIR_HASH)
        self.assertEqual(result["aggregate_shards_surviving"], 22)
        self.assertEqual(
            result["shard_witness_hash"],
            EXPECTED_MOD3_SHARD_WITNESS_HASH,
        )


if __name__ == "__main__":
    unittest.main()
