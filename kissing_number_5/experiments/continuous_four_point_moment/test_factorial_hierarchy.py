#!/usr/bin/env python3

import unittest

from experiments.continuous_four_point_moment.verify_factorial_farkas_independent import (
    verify as verify_independent,
)
from experiments.continuous_four_point_moment.verify_factorial_hierarchy import (
    verify,
)


class FactorialHierarchyTest(unittest.TestCase):
    def test_primary_exact_verifier(self):
        report = verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["K6_cap_violations"], 11)
        self.assertEqual(report["K7_cap_violations"], 19)

    def test_independent_farkas_verifier(self):
        report = verify_independent()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["pool_columns"], 1782)
        self.assertEqual(report["joint_augmented_columns"], 1783)


if __name__ == "__main__":
    unittest.main()
