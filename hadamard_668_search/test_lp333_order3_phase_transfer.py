#!/usr/bin/env python3
"""Tests for the LP(333) trivial-character phase transfer."""

from __future__ import annotations

import unittest

import verify_lp333_order3_phase_transfer as transfer
from verify_lp333_order3_labeled_jet import (
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
)
from verify_lp333_order3_profile9 import PINNED_PROFILE_IDS
from verify_lp333_order3_profile9_shards import PROFILE9_SHARD_WITNESSES
from verify_lp333_order3_trit_lift import (
    TRIT_SURVIVOR_MASKS_A,
    TRIT_SURVIVOR_MASKS_B,
)


class OrderThreePhaseTransferTests(unittest.TestCase):
    def test_phase_sum_convolution_is_exact(self) -> None:
        identifiers = PROFILE9_SHARD_WITNESSES[0][1]
        for residue in range(3):
            positive, negative = transfer.fiber_phase_counts(
                0,
                identifiers,
                residue,
            )
            distribution = transfer.phase_sum_distribution(
                0,
                identifiers,
                residue,
            )
            self.assertEqual(
                sum(distribution.values()),
                3 ** (positive + negative),
            )

    def test_pinned_transfer_contains_both_fixtures(self) -> None:
        pinned = transfer.audit_profile_transfer(*PINNED_PROFILE_IDS)
        labelled = transfer.audit_fixture(
            LABELLED_SURVIVOR_MASKS_A,
            LABELLED_SURVIVOR_MASKS_B,
            pinned,
        )
        trit = transfer.audit_fixture(
            TRIT_SURVIVOR_MASKS_A,
            TRIT_SURVIVOR_MASKS_B,
            pinned,
        )
        self.assertEqual(labelled, trit)
        self.assertEqual(
            labelled["signatures"],
            ((69, (32, 15)), (98, (-32, -15))),
        )

    def test_all_profile_shards_replay(self) -> None:
        result = transfer.verify()
        self.assertEqual(result["profile_shards"], 22)
        self.assertEqual(result["diagnostic_zero_gate_failures"], 23)
        self.assertEqual(result["aggregate_shard_exclusions"], 0)
        self.assertEqual(result["minimum_compatible_signatures"], 22)
        self.assertEqual(result["maximum_compatible_signatures"], 87)
        self.assertEqual(result["minimum_compatible_catalog_rows"], 45)
        self.assertEqual(result["maximum_compatible_catalog_rows"], 98)
        self.assertEqual(result["labelled_fixtures_checked"], 2)

    def test_transfer_prunes_every_shard(self) -> None:
        result = transfer.verify()
        total = result["total_assignments_per_shard"]
        for accepted in result["accepted_assignment_counts"]:
            self.assertGreater(accepted, 0)
            self.assertLess(accepted, total)
            self.assertGreater(total // accepted, 100_000)

    def test_phase_transfer_equals_catalog_intersection(self) -> None:
        _, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
        phase = transfer.audit_profile_transfer(
            identifiers_a,
            identifiers_b,
        )
        catalog = transfer.catalog_phase_sum_intersection(
            identifiers_a,
            identifiers_b,
        )
        self.assertEqual(
            phase["phase_sum_corpus"],
            catalog["phase_sum_corpus"],
        )
        self.assertEqual(
            phase["accepted_assignments"],
            catalog["accepted_assignments"],
        )


if __name__ == "__main__":
    unittest.main()
