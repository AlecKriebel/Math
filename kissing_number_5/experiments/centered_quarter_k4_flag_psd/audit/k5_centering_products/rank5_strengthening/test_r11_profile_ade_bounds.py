#!/usr/bin/env python3
"""Regression test for the r11 ADE profile application."""

from __future__ import annotations

import unittest

from verify_r11_profile_ade_bounds import self_test


class R11ProfileAdeBoundsTest(unittest.TestCase):
    def test_all_exported_profiles(self) -> None:
        summary = self_test()
        self.assertEqual(summary["profiles"], 38)
        self.assertEqual(summary["maximum_plus_one"], 6)


if __name__ == "__main__":
    unittest.main()
