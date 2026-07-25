#!/usr/bin/env python3
"""Regression test for the exact ADE core-shell verifier."""

from __future__ import annotations

import unittest

from verify_ade_core_shells import self_test


class AdeCoreShellTest(unittest.TestCase):
    def test_complete_exact_enumeration(self) -> None:
        results = self_test()
        self.assertEqual(results["A5"]["maximum"], 6)
        self.assertEqual(results["D5"]["maximum"], 16)
        self.assertEqual(results["D4+A1"]["maximum"], 2)
        self.assertEqual(results["D4_rank4"]["clique_number"], 16)
        self.assertEqual(results["D4_rank4_eleven"]["omissions"], 12)
        self.assertEqual(
            results["r11_character_bounds"]["cover_lower_bounds"],
            {1: 4, 2: 6, 3: 6},
        )


if __name__ == "__main__":
    unittest.main()
