#!/usr/bin/env python3
"""Focused tests for the first lambda-adic phase digit."""

from __future__ import annotations

import unittest

import verify_lp333_order3_phase_hensel as hensel
from verify_lp333_order3_profile9_shards import PROFILE9_SHARD_WITNESSES


class OrderThreePhaseHenselTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = hensel.verify()

    def test_exact_rank_census(self) -> None:
        self.assertEqual(self.result["profile_witnesses"], 22)
        self.assertEqual(self.result["first_digit_survivors"], 21)
        self.assertEqual(self.result["generic_rank"], 18)
        self.assertEqual(self.result["generic_nullity"], 36)
        self.assertEqual(self.result["exceptional_rank_pair"], (16, 17))
        self.assertEqual(
            self.result["excluded_fixed_profile_witnesses"],
            ((3, hensel.EXCLUDED_PINNED_TARGET),),
        )
        self.assertEqual(self.result["excluded_aggregate_shards"], 0)

    def test_displayed_system_shape(self) -> None:
        self.assertEqual(self.result["placement_trits_per_witness"], 54)
        self.assertEqual(self.result["displayed_first_digit_equations"], 20)
        self.assertEqual(self.result["identically_zero_rows_per_witness"], 2)

    def test_explicit_inconsistency_certificate(self) -> None:
        target, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[3]
        audit = hensel.audit_profile_witness(
            target,
            identifiers_a,
            identifiers_b,
            3,
        )
        self.assertFalse(audit["consistent"])
        self.assertEqual(
            audit["inconsistency_certificate"],
            hensel.EXPECTED_EXCLUSION_MULTIPLIERS,
        )

    def test_profile_identifier_bounds(self) -> None:
        _, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
        with self.assertRaises(ValueError):
            hensel.profiles_from_ids((-1,) + identifiers_a[1:], identifiers_b)
        with self.assertRaises(ValueError):
            hensel.profiles_from_ids(
                (len(hensel.PROFILES),) + identifiers_a[1:],
                identifiers_b,
            )


if __name__ == "__main__":
    unittest.main()
