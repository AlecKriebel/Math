#!/usr/bin/env python3
"""Focused tests for the primitive-nine profile ideal obstruction."""

from __future__ import annotations

import unittest

from verify_lp333_order3_profile9 import (
    EXPECTED_PAIRED_PROFILE_TABLES_SHA256,
    EXPECTED_PINNED_PROFILE_TABLE_SHA256,
    EXPECTED_PINNED_TARGETS_SHA256,
    PINNED_PROFILE_IDS,
    audit_prior_paired_witnesses,
    audit_profile_table,
    e_norm,
    lambda3_digits,
    lies_in_three_lambda,
    reconstruct_periodic_target,
    verify_all,
    verify_pinned_profile_targets,
    weight_correlation_totals,
)


class OrderThreeProfileNineTests(unittest.TestCase):
    def test_ideal_membership_reconstructs_unique_sum_501_triple(self) -> None:
        value = (27, 27)
        self.assertTrue(lies_in_three_lambda(value))
        self.assertEqual(
            reconstruct_periodic_target(value),
            (170, 170, 161),
        )
        self.assertEqual(e_norm(value) % 27, 0)
        self.assertEqual(lambda3_digits(value), (0, 0, 0))
        for failure in ((6, -3), (0, -15), (-30, -18)):
            self.assertFalse(lies_in_three_lambda(failure))
            self.assertIsNone(reconstruct_periodic_target(failure))
            self.assertNotEqual(lambda3_digits(failure), (0, 0, 0))

    def test_pinned_profiles_fix_all_thirteen_targets(self) -> None:
        result = verify_pinned_profile_targets()
        self.assertEqual(result["active_profile_classes"], 12)
        self.assertEqual(result["displayed_conjugate_pair_conditions"], 6)
        self.assertEqual(result["independent_ideal_conditions"], 5)
        self.assertEqual(result["ideal_norm"], 27)
        self.assertEqual(result["table_hash"], EXPECTED_PINNED_PROFILE_TABLE_SHA256)
        self.assertEqual(result["target_hash"], EXPECTED_PINNED_TARGETS_SHA256)
        targets = result["periodic_targets"]
        self.assertEqual(len(targets), 13)
        self.assertEqual(targets[0], (167, 167, 167))
        self.assertEqual(targets[1], (170, 170, 161))
        self.assertTrue(all(sum(target) == 501 for target in targets))

        audit = audit_profile_table(*PINNED_PROFILE_IDS)
        self.assertEqual(audit["zero_coefficient"], (0, 0))
        self.assertEqual(audit["nonzero_coefficient_sum"], (0, 0))
        self.assertEqual(audit["physical_coefficient_sum"], (0, 0))
        self.assertEqual(audit["failing_nonzero_classes"], ())
        self.assertEqual(audit["reversal_checks"], 6)

    def test_all_prior_profile_witnesses_fail_new_ideal(self) -> None:
        result = audit_prior_paired_witnesses()
        self.assertEqual(result["prior_profile_witnesses"], 22)
        self.assertEqual(result["profile_witnesses_passing_new_ideal_test"], 0)
        self.assertEqual(result["independent_ideal_conditions"], 5)
        self.assertEqual(
            result["failing_class_histogram"],
            ((4, 4), (6, 1), (8, 10), (10, 4), (12, 3)),
        )
        self.assertEqual(
            result["profile_table_corpus_sha256"],
            EXPECTED_PAIRED_PROFILE_TABLES_SHA256,
        )
        self.assertEqual(result["shard_exclusions"], 0)

    def test_global_weight_moment_is_placement_independent(self) -> None:
        self.assertEqual(weight_correlation_totals(), (1503,) * 37)
        result = verify_all()
        self.assertEqual(result["total_correlation_per_column_lag"], 1503)
        self.assertEqual(result["ideal"], "3(1-omega)")
        self.assertEqual(result["ideal_norm"], 27)


if __name__ == "__main__":
    unittest.main()
