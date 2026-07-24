from __future__ import annotations

from fractions import Fraction as Q
import subprocess
import sys
import unittest

from experiments.quadratic_positive_residual.verify_weighted_branch_identities import (
    VerificationError,
    verify_design,
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

    def test_bad_weights_are_rejected(self) -> None:
        simplex_gram = [
            [Q(1) if i == j else -Q(1, 5) for j in range(6)]
            for i in range(6)
        ]
        with self.assertRaises(VerificationError):
            verify_design(simplex_gram, [Q(1, 5)] * 6)

    def test_optimized_mode_normal_and_tamper(self) -> None:
        module = (
            "experiments.quadratic_positive_residual."
            "verify_weighted_branch_identities"
        )
        valid = subprocess.run(
            [sys.executable, "-O", "-m", module],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertIn('"status": "PASS"', valid.stdout)

        code = (
            "from fractions import Fraction as Q;"
            "from experiments.quadratic_positive_residual."
            "verify_weighted_branch_identities import verify_design;"
            "g=[[Q(1) if i==j else -Q(1,5) for j in range(6)]"
            " for i in range(6)];"
            "verify_design(g,[Q(1,5)]*6)"
        )
        tampered = subprocess.run(
            [sys.executable, "-O", "-c", code],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(tampered.returncode, 0)
        self.assertIn("weights do not sum to one", tampered.stderr)


if __name__ == "__main__":
    unittest.main()
