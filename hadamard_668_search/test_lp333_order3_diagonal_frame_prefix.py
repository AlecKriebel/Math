#!/usr/bin/env python3
"""Tests for the exact diagonal-frame augmentation/T1 prefix."""

from __future__ import annotations

import unittest

from verify_lp333_order3_diagonal_frame_prefix import (
    EXPECTED_COUNTS,
    EXPECTED_RESULT_SHA256,
    RAW_PHASE_ASSIGNMENTS,
    sequence_summary,
    verify_diagonal_frame_prefix,
)


class DiagonalFramePrefixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = verify_diagonal_frame_prefix()

    def test_complete_count_replay(self) -> None:
        self.assertEqual(self.result["profile_tuples"], 22)
        self.assertEqual(
            self.result["raw_assignments_per_tuple"],
            RAW_PHASE_ASSIGNMENTS,
        )
        self.assertEqual(self.result["profile_tuples_surviving_prefix"], 22)
        self.assertEqual(self.result["full_diagonal_assignments_asserted"], 0)
        self.assertEqual(
            self.result["result_sha256"],
            EXPECTED_RESULT_SHA256,
        )

    def test_state_widths(self) -> None:
        self.assertEqual(self.result["transfer_formula_checks"], 129)
        self.assertEqual(self.result["largest_sequence_summary"], 444)
        self.assertEqual(self.result["largest_joined_prefix"], 666)

    def test_pinned_count_extrema(self) -> None:
        prefix_counts = tuple(value[2] for value in EXPECTED_COUNTS)
        self.assertEqual(
            min(prefix_counts),
            self.result["smallest_prefix_survivors"],
        )
        self.assertEqual(
            max(prefix_counts),
            self.result["largest_prefix_survivors"],
        )
        self.assertTrue(all(value > 0 for value in prefix_counts))

    def test_zero_sequence_summary(self) -> None:
        self.assertEqual(sequence_summary((0, 0)), (((0, 0), 1),))


if __name__ == "__main__":
    unittest.main()
