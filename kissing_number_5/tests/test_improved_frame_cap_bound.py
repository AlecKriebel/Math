import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_improved_frame_cap_bound.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_improved_frame_cap_bound", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ImprovedFrameCapBoundTests(unittest.TestCase):
    def test_certificate(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["projected_code_bound"], 30)
        self.assertEqual(
            Fraction(result["strict_frame_lower_bound"]),
            Fraction(15059, 40000),
        )
        self.assertGreater(
            Fraction(result["strict_frame_lower_bound"]),
            Fraction(result["previous_frame_lower_bound"]),
        )
        self.assertTrue(result["small_variance_completion_survives"])

    def test_basis_normalization(self):
        basis = MODULE.gegenbauer_4_basis(11)
        self.assertTrue(all(sum(polynomial) == 1 for polynomial in basis))


if __name__ == "__main__":
    unittest.main()
