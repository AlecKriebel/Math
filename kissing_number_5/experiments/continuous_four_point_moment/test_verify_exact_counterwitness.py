#!/usr/bin/env python3

import unittest

from experiments.continuous_four_point_moment.verify_exact_counterwitness import (
    verify,
)


class ExactCounterWitnessTest(unittest.TestCase):
    def test_exact_counterwitness(self):
        report = verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["positive_rank_five_k6_atoms"], 74)
        self.assertEqual(report["measure_masses"]["alpha"], "40")
        self.assertEqual(report["measure_masses"]["nu"], "1560")
        self.assertEqual(report["measure_masses"]["rho"], "59280")
        self.assertEqual(report["sharp_harmonic_rank_cuts"], 27)
        self.assertEqual(report["product_slack"], "0")


if __name__ == "__main__":
    unittest.main()
