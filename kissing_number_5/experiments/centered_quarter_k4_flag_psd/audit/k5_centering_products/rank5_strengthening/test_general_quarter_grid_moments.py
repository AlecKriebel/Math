#!/usr/bin/env python3
"""Tests for the noncentered quarter-grid moment verifier."""

from __future__ import annotations

import unittest

from verify_general_quarter_grid_moments import (
    endpoint_counts,
    h1_y_branches,
    invariants,
    r11_control_counts,
    self_test,
)


class GeneralQuarterGridMomentTest(unittest.TestCase):
    def test_self_test(self) -> None:
        self_test()

    def test_r12_endpoint(self) -> None:
        result = invariants(endpoint_counts())
        self.assertEqual(result["A"], -81)
        self.assertEqual(result["X1"], 7)
        self.assertEqual(result["X2"], 1237)
        self.assertEqual(result["X2"] % 210, 187)

    def test_r11_q2367_q2368_controls(self) -> None:
        q_values = [
            invariants(counts)["Q"]
            for counts in r11_control_counts()
        ]
        self.assertEqual(q_values, [2367, 2368])
        self.assertEqual(
            h1_y_branches(2367),
            (-231, -156, -81, -6, 69, 144, 219, 294),
        )


if __name__ == "__main__":
    unittest.main()
