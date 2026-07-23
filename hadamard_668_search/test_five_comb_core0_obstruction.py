#!/usr/bin/env python3
"""Focused regression test for the projective-core-zero obstruction."""

from __future__ import annotations

import unittest

import verify_five_comb_core0_obstruction as verifier


class FiveCombCoreZeroObstructionTest(unittest.TestCase):
    def test_complete_dependency_free_verifier(self) -> None:
        result = verifier.verify_all()
        self.assertEqual(result["core_label_maps"], 128)
        self.assertEqual(result["bounded_row_square_checks"], 614_656)
        self.assertEqual(result["closest_row_square_residual"], 2)
        self.assertEqual(result["core_parameter_rows"], 8)
        self.assertEqual(result["core_full_rows"], 288)
        self.assertEqual(result["paired_inventories"], 768_512)


if __name__ == "__main__":
    unittest.main()
