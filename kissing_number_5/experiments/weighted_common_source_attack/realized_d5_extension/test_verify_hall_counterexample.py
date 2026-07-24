#!/usr/bin/env python3

from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import unittest

import verify_hall_counterexample as verifier


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "verify_hall_counterexample.py"


class HallCounterexampleTests(unittest.TestCase):
    def test_verifier_normal_and_optimized(self):
        for optimized in (False, True):
            command = [sys.executable]
            if optimized:
                command.append("-O")
            command.append(str(VERIFIER))
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"neighborhood_union_size": 1', result.stdout)

    def test_exact_quadratic_order(self):
        root_three = verifier.Quad(0, 1)
        self.assertGreater(root_three, Fraction(3, 2))
        self.assertLess(root_three, 2)
        self.assertEqual(root_three * root_three, 3)

    def test_counterexample_is_on_closed_kissing_boundary(self):
        result = verifier.verify()
        self.assertEqual(result["mutual_inner_product"], "1/2")
        self.assertEqual(result["points"], 2)
        self.assertEqual(result["full_conflict_degrees"], [5, 5])
        self.assertEqual(result["full_conflict_union_size"], 9)


if __name__ == "__main__":
    unittest.main()
