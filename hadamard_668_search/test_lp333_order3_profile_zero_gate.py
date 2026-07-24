#!/usr/bin/env python3
"""Focused tests for the exact full-LP order-three profile gate."""

from __future__ import annotations

import unittest

from verify_lp333_order3_profile9 import moment_from_exact_correlations
from verify_lp333_order3_profile_zero_gate import (
    aggregate_shard_target,
    full_lp_plus_intersection_from_paf,
    profile_zero_gate,
    verify,
)
from verify_lp333_order3_labeled_jet import LABELLED_SURVIVOR_AGGREGATE
from verify_lp333_order3_profile9_shards import PROFILE9_SHARD_WITNESSES


class ProfileZeroGateTests(unittest.TestCase):
    def test_full_lp_target_has_zero_order3_moment(self) -> None:
        self.assertEqual(full_lp_plus_intersection_from_paf(-2), 167)
        self.assertEqual(
            moment_from_exact_correlations((167,) * 9),
            (0, 0),
        )
        with self.assertRaises(ValueError):
            full_lp_plus_intersection_from_paf(-1)

    def test_row695_selects_ideal_witness_eight(self) -> None:
        target = aggregate_shard_target(LABELLED_SURVIVOR_AGGREGATE)
        self.assertEqual(target, (1, -1, 2, -2))
        self.assertEqual(PROFILE9_SHARD_WITNESSES[8][0], target)

    def test_ideal_membership_is_strictly_weaker_than_zero(self) -> None:
        _, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[8]
        result = profile_zero_gate(identifiers_a, identifiers_b)
        self.assertTrue(result["ideal_compatible"])
        self.assertFalse(result["passes_full_lp_zero_moment_gate"])
        self.assertEqual(result["nonzero_class_violation_count"], 12)

    def test_complete_fixed_profile_corpus(self) -> None:
        result = verify()
        corpus = result["ideal_witness_corpus"]
        self.assertEqual(corpus["fixed_profile_assignments_audited"], 22)
        self.assertEqual(corpus["fixed_profile_exclusions"], 22)
        self.assertEqual(corpus["aggregate_shard_exclusions"], 0)
        self.assertEqual(
            corpus["nonzero_class_failure_histogram"],
            ((10, 1), (12, 21)),
        )
        self.assertTrue(
            result["row695"]["original_and_same_shard_witness_excluded"]
        )


if __name__ == "__main__":
    unittest.main()
