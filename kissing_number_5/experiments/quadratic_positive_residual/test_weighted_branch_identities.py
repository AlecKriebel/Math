from __future__ import annotations

import unittest

from experiments.quadratic_positive_residual.verify_weighted_branch_identities import (
    verify,
)


class WeightedBranchIdentityTest(unittest.TestCase):
    def test_exact_identities_and_counterexamples(self) -> None:
        report = verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["sharp_regular_simplex"]["support"], 6)
        self.assertEqual(report["full_support_nonuniform_D5"]["support"], 40)
        self.assertEqual(report["sparse_support_D5"]["support"], 32)
        self.assertEqual(report["twelve_support_D5"]["support"], 12)


if __name__ == "__main__":
    unittest.main()
