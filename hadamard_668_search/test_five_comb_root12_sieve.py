#!/usr/bin/env python3
"""Focused regression test for the paired-lobe roots +/-1 sieve."""

from __future__ import annotations

import unittest

import verify_five_comb_root12_sieve as verifier


class FiveCombRoot12SieveTest(unittest.TestCase):
    def test_complete_dependency_free_verifier(self) -> None:
        result = verifier.verify_all()
        self.assertEqual(result["target_shell"], 672)
        self.assertEqual(result["target_midpoints"], 116_389)
        self.assertEqual(result["inventories"], 768_512)
        self.assertEqual(result["octet_profiles"], 35)
        self.assertEqual(result["component_profiles"], 652)
        self.assertEqual(result["feature_classes"], 8_729)
        self.assertEqual(result["arbitrary_rejections"], 78)
        self.assertEqual(result["arbitrary_nonzero_rejections"], 46)
        self.assertEqual(result["arbitrary_weighted_rejection"], 2_576_920)
        self.assertEqual(result["vertical_weighted_rejection"], 830_528)
        self.assertEqual(result["vertical_profile_core_rejections"], 10)


if __name__ == "__main__":
    unittest.main()
