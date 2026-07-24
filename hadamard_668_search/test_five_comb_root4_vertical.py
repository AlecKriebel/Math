#!/usr/bin/env python3
"""Focused regression test for the vertical-pair Phi_4 sieve."""

from __future__ import annotations

import unittest

import verify_five_comb_root4_vertical as verifier


class FiveCombRoot4VerticalTest(unittest.TestCase):
    def test_complete_dependency_free_verifier(self) -> None:
        result = verifier.verify()
        self.assertEqual(result["inventories"], 768_512)
        self.assertEqual(result["feature_classes"], 8_729)
        self.assertEqual(result["weighted_rejection"], 906_241)
        self.assertEqual(result["additional_rejection"], 75_713)
        self.assertEqual(result["rejected_profile_core_cells"], 11)


if __name__ == "__main__":
    unittest.main()
