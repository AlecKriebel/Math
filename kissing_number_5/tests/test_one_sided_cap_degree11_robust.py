from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = ROOT / "verifiers" / "verify_one_sided_cap_degree11_robust.py"
SPEC = importlib.util.spec_from_file_location("cap_degree11_robust", VERIFIER_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class OneSidedCapDegree11RobustTests(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["minimum_height"], -Q(1, 300))
        self.assertEqual(result["dual_objective"], Q(16939, 484))
        self.assertEqual(result["enlarged_cap_upper_bound"], 34)

    def test_affine_substitution_commutes_with_evaluation(self) -> None:
        polynomial = {
            (2, 1, 0): Q(7, 5),
            (0, 0, 3): -Q(4, 9),
            (1, 1, 1): Q(11, 13),
        }
        shifts = (-Q(1, 300), -Q(1, 300), Q(-1))
        scales = (Q(301, 300), Q(301, 300), Q(3, 2))
        transformed = VERIFY.affine_substitute(polynomial, shifts, scales)
        point = (Q(2, 7), Q(3, 8), Q(5, 11))

        def evaluate(poly, values):
            return sum(
                coefficient
                * values[0] ** exponent[0]
                * values[1] ** exponent[1]
                * values[2] ** exponent[2]
                for exponent, coefficient in poly.items()
            )

        mapped = tuple(
            shift + scale * value
            for shift, scale, value in zip(shifts, scales, point, strict=True)
        )
        self.assertEqual(
            evaluate(transformed, point),
            evaluate(polynomial, mapped),
        )

    def test_tampered_minimum_height_is_rejected(self) -> None:
        data = json.loads(VERIFY.ROBUST_CERTIFICATE_PATH.read_text())
        data["minimum_height"] = "-1/299"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "ROBUST_CERTIFICATE_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()

    def test_tampered_tree_digest_is_rejected(self) -> None:
        data = json.loads(VERIFY.ROBUST_CERTIFICATE_PATH.read_text())
        data["bernstein_tree_manifest"]["leaf_digest_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "ROBUST_CERTIFICATE_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()


if __name__ == "__main__":
    unittest.main()
