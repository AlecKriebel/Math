#!/usr/bin/env python3
"""Focused tests for the LP(333) multiplier row-sum obstruction."""

from __future__ import annotations

from collections import Counter
import unittest

from verify_lp333_multiplier_row_sum import (
    EXPECTED_ALL_CORE_COUNTS,
    EXPECTED_CANONICAL_COUNTS,
    EXPECTED_CHANNEL_COUNTS,
    EXPECTED_H3_ENERGY_PAIRS,
    EXPECTED_ZERO_CORES,
    TARGET_PROFILE,
    channel_energy_distribution,
    classes_for_subgroup_size,
    sign_words,
    verify_all_zero_cores,
    verify_canonical_census,
    verify_h3_witness,
    verify_phi3_shell,
    verify_transition_sum_identities,
    verify_zero_core_normalization,
    zero_core_catalog,
    CANONICAL_ZERO_EXPONENTS,
)


class MultiplierRowSumTests(unittest.TestCase):
    def test_transition_sum_identity(self) -> None:
        self.assertEqual(
            verify_transition_sum_identities(),
            {18: 2, 9: 4, 6: 6, 3: 12},
        )
        for h, expected_classes in ((18, 2), (9, 4), (6, 6), (3, 12)):
            self.assertEqual(len(classes_for_subgroup_size(h)), expected_classes)

    def test_zero_core_filter_and_normalization(self) -> None:
        self.assertEqual(len(zero_core_catalog()), EXPECTED_ZERO_CORES)
        self.assertEqual(
            verify_zero_core_normalization(),
            {"actions": EXPECTED_ZERO_CORES, "orbit": EXPECTED_ZERO_CORES},
        )

    def test_canonical_projection_counts(self) -> None:
        census = verify_canonical_census()
        for h in (18, 9, 6):
            self.assertEqual(
                (
                    census[h]["energy_sum_states"],
                    census[h]["profiles"],
                    census[h]["target_hits"],
                ),
                EXPECTED_CANONICAL_COUNTS[h],
            )
            self.assertEqual(
                census[h]["channel_states"], EXPECTED_CHANNEL_COUNTS[h]
            )
        self.assertEqual(census[3]["channel_states"], EXPECTED_CHANNEL_COUNTS[3])
        self.assertEqual(
            census[3]["energy_sum_states"], EXPECTED_H3_ENERGY_PAIRS
        )

    def test_h3_boundary_witness(self) -> None:
        witness = verify_h3_witness()
        self.assertEqual(witness["sum"], (1, 0))
        self.assertEqual(witness["energy"], 297)
        self.assertEqual(witness["profile"], TARGET_PROFILE)
        self.assertEqual(sum(witness["p"]), 0)
        self.assertEqual(sum(witness["q"]), 0)
        self.assertEqual(
            witness["left_energy"] + witness["right_energy"], 96
        )

        a_signs, b_signs = sign_words(CANONICAL_ZERO_EXPONENTS)
        left = channel_energy_distribution(a_signs, 3)
        right = channel_energy_distribution(b_signs, 3)
        self.assertEqual(sum(left.values()), EXPECTED_CHANNEL_COUNTS[3])
        self.assertEqual(left, right)

    def test_all_zero_core_replay(self) -> None:
        replay = verify_all_zero_cores()
        for h in (18, 9, 6):
            self.assertEqual(replay[h]["zero_cores"], EXPECTED_ZERO_CORES)
            self.assertEqual(
                replay[h]["total_states"], EXPECTED_ALL_CORE_COUNTS[h]
            )
            self.assertEqual(replay[h]["target_hits"], 0)

    def test_phi3_corollary(self) -> None:
        states = verify_phi3_shell()
        self.assertEqual(len(states), 4)
        self.assertEqual(
            {state[0] for state in states},
            {(0, -2)},
        )


if __name__ == "__main__":
    unittest.main()
