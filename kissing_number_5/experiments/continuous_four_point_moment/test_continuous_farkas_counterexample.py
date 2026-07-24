#!/usr/bin/env python3

import unittest

from experiments.continuous_four_point_moment.verify_continuous_farkas_counterexample import (
    verify,
)


class ContinuousFarkasCounterexampleTest(unittest.TestCase):
    def test_exact_rank_five_counterexample(self):
        report = verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["rank"], 5)
        self.assertEqual(report["farkas_atom_value"], -2109)
        self.assertEqual(report["off_grid_inner_products"], ["-2/3", "1/3"])


if __name__ == "__main__":
    unittest.main()
