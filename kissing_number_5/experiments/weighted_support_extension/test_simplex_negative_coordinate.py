from __future__ import annotations

from fractions import Fraction as Q
import subprocess
import sys
import unittest

from experiments.weighted_support_extension.verify_simplex_negative_coordinate import (
    VerificationError,
    verify,
)


class SimplexNegativeCoordinateTest(unittest.TestCase):
    def test_exact_threshold(self) -> None:
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["unique_feasible_endpoint_count"], 2)
        self.assertEqual(
            [case["feasible"] for case in result["vertex_cases"]],
            [False, False, True, False, False, False],
        )

    def test_tampered_rho_is_rejected(self) -> None:
        with self.assertRaises(VerificationError):
            verify(Q(1, 4), Q(1, 21))

    def test_optimized_mode_normal_and_tamper(self) -> None:
        module = (
            "experiments.weighted_support_extension."
            "verify_simplex_negative_coordinate"
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
            "from experiments.weighted_support_extension."
            "verify_simplex_negative_coordinate import verify;"
            "verify(Q(1,4),Q(1,21))"
        )
        tampered = subprocess.run(
            [sys.executable, "-O", "-c", code],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(tampered.returncode, 0)
        self.assertIn("unexpected rho representation", tampered.stderr)


if __name__ == "__main__":
    unittest.main()
