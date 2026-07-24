#!/usr/bin/env python3
"""Focused regressions for the complete LP(333) search estimate."""

from __future__ import annotations

import unittest

from verify_complete_remaining_search_estimate import audit


class CompleteRemainingSearchEstimateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = audit()

    def test_dense_shell_counts(self) -> None:
        self.assertEqual(
            self.result["support_counts_h1_h0"],
            (510_384, 107_476),
        )
        self.assertEqual(
            self.result["signed_skeleton_counts_h1_h0"],
            (59_743_488, 47_730_304),
        )

    def test_complete_work_bounds(self) -> None:
        self.assertEqual(
            self.result["five_shell_two_affine_points"],
            750_473_176_484_995_605,
        )
        self.assertEqual(self.result["shell_two_row_margin_shards"], 405)
        self.assertEqual(
            self.result["character_evaluation_counts"][
                "unbatched_high_positions"
            ],
            426_772_416_384,
        )

    def test_exactness_cutoff_inequality(self) -> None:
        bounds = self.result["exactness_inequality"]
        self.assertLess(
            bounds["residual_norm_bound"], bounds["lambda_nine_norm"]
        )


if __name__ == "__main__":
    unittest.main()
