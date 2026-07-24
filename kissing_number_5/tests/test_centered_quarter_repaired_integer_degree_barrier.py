#!/usr/bin/env python3
"""Integrated exact tests for the repaired integer-degree witness."""

from __future__ import annotations

from pathlib import Path
import unittest

from verifiers.verify_centered_quarter_bv_all_harmonics import (
    verify as verify_all_harmonics,
)
from verifiers.verify_centered_quarter_integer_degree_mixture import (
    verify as verify_integer_mixture,
)


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "centered_integer_degree_moments"
SOURCE = EXPERIMENT / "repaired_pair_triple_local_3.json"
TAIL = EXPERIMENT / "repaired_local_3_all_harmonics.json"
MIXTURE = ROOT / "certificates" / "centered_quarter_integer_degree_mixture.json"


class RepairedIntegerDegreeBarrierTest(unittest.TestCase):
    def test_all_harmonics_and_rank_cuts(self) -> None:
        result = verify_all_harmonics(SOURCE, TAIL)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["w0_rank"], 6)
        self.assertEqual(result["w1_rank"], 5)
        self.assertEqual(result["sharp_harmonic_rank_cuts_checked"], 27)

    def test_exact_integer_degree_mixture(self) -> None:
        result = verify_integer_mixture(MIXTURE, SOURCE)
        self.assertEqual(result["positive_atoms"], 18)
        self.assertTrue(result["exact_pair_moment_match"])


if __name__ == "__main__":
    unittest.main()
