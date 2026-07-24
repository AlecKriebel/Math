#!/usr/bin/env python3
"""Tests for the 22 primitive-nine profile-ideal shard witnesses."""

from __future__ import annotations

import unittest

from verify_lp333_order3_profile9_shards import (
    EXPECTED_PERIODIC_TARGETS_SHA256,
    EXPECTED_PROFILE_TABLES_SHA256,
    EXPECTED_WITNESS_SHA256,
    PROFILE9_SHARD_WITNESSES,
    audit_shard_witness,
    verify_profile9_shard_witnesses,
)


class Profile9ShardWitnessTests(unittest.TestCase):
    def test_complete_catalog_replay(self) -> None:
        result = verify_profile9_shard_witnesses()
        self.assertEqual(result["aggregate_shards"], 22)
        self.assertEqual(result["profile_assignments"], 22)
        self.assertEqual(result["local_conditions_checked"], 132)
        self.assertEqual(result["profile_ideal_tests_checked"], 264)
        self.assertEqual(result["shard_exclusions"], 0)
        self.assertEqual(result["labelled_lifts_asserted"], 0)
        self.assertEqual(result["witness_sha256"], EXPECTED_WITNESS_SHA256)
        self.assertEqual(
            result["profile_tables_sha256"],
            EXPECTED_PROFILE_TABLES_SHA256,
        )
        self.assertEqual(
            result["periodic_targets_sha256"],
            EXPECTED_PERIODIC_TARGETS_SHA256,
        )

    def test_single_witness_api(self) -> None:
        target, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
        result = audit_shard_witness(target, identifiers_a, identifiers_b)
        self.assertTrue(result["valid"])
        self.assertEqual(result["energy"], 54)
        self.assertEqual(result["local_conditions"], 6)
        self.assertEqual(result["profile_ideal_tests"], 12)

    def test_tampered_witness_is_rejected(self) -> None:
        target, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
        tampered = ((identifiers_a[0] + 1) % 10,) + identifiers_a[1:]
        with self.assertRaises(ValueError):
            audit_shard_witness(target, tampered, identifiers_b)


if __name__ == "__main__":
    unittest.main()
