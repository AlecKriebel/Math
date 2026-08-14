from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "independent_verifier"))
from certificate_checks import verify_certificate  # noqa: E402


class CertificateTests(unittest.TestCase):
    def test_rational_yes(self):
        data = {
            "certificate_type": "real_algebraic_sample_yes",
            "variables": ["x", "z"],
            "coefficient_field": {"type": "rational"},
            "equations": ["x - 3", "x*z**2 - 1"],
            "values": ["3", "1/3**(1/2)"],
        }
        # The square root is not rational and must be rejected in a rational field.
        with self.assertRaises(ValueError):
            verify_certificate(data)

        valid = {
            "certificate_type": "real_algebraic_sample_yes",
            "variables": ["x"],
            "coefficient_field": {"type": "rational"},
            "equations": ["x**2 - 4"],
            "values": ["2"],
        }
        self.assertEqual(verify_certificate(valid), "YES_CERTIFICATE_OK")

    def test_algebraic_strict_inequality_encoding(self):
        data = {
            "certificate_type": "real_algebraic_sample_yes",
            "variables": ["g", "z"],
            "coefficient_field": {
                "type": "real_algebraic",
                "symbol": "alpha",
                "minimal_polynomial": "alpha**2 - 3",
                "isolating_interval": ["1", "2"],
            },
            "equations": ["g - 3", "g*z**2 - 1"],
            "values": ["3", "alpha/3"],
        }
        self.assertEqual(verify_certificate(data), "YES_CERTIFICATE_OK")
        bad = copy.deepcopy(data)
        bad["values"][1] = "alpha/2"
        with self.assertRaises(ValueError):
            verify_certificate(bad)

    def test_rational_nullstellensatz(self):
        data = {
            "certificate_type": "real_nullstellensatz_no",
            "variables": ["x"],
            "coefficient_field": {"type": "rational"},
            "equations": ["x**2 + 1"],
            "sum_of_squares": ["x"],
            "multipliers": ["-1"],
        }
        self.assertEqual(verify_certificate(data), "NO_CERTIFICATE_OK")
        data["multipliers"] = ["1"]
        with self.assertRaises(ValueError):
            verify_certificate(data)

    def test_algebraic_identity(self):
        # Over Q(sqrt(2)), the infeasible equation x^2+alpha^2=0 has
        # -1=(x/alpha)^2-(x^2+alpha^2)/2.
        data = {
            "certificate_type": "real_nullstellensatz_no",
            "variables": ["x"],
            "coefficient_field": {
                "type": "real_algebraic",
                "symbol": "alpha",
                "minimal_polynomial": "alpha**2 - 2",
                "isolating_interval": ["1", "2"],
            },
            "equations": ["x**2 + alpha**2"],
            "sum_of_squares": ["alpha*x/2"],
            "multipliers": ["-1/2"],
        }
        # (alpha*x/2)^2=x^2/2, giving -1 after the multiplier term.
        self.assertEqual(verify_certificate(data), "NO_CERTIFICATE_OK")

    def test_bad_isolating_interval(self):
        data = {
            "certificate_type": "real_algebraic_sample_yes",
            "variables": ["x"],
            "coefficient_field": {
                "type": "real_algebraic",
                "symbol": "alpha",
                "minimal_polynomial": "alpha**2 - 2",
                "isolating_interval": ["-2", "2"],
            },
            "equations": ["x**2 - 2"],
            "values": ["alpha"],
        }
        with self.assertRaises(ValueError):
            verify_certificate(data)


if __name__ == "__main__":
    unittest.main()
