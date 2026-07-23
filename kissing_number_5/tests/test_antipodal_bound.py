import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_antipodal_bound.py"
SPEC = importlib.util.spec_from_file_location("verify_antipodal_bound", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AntipodalBoundTests(unittest.TestCase):
    def test_exact_certificate(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["line_upper_bound_before_equality_elimination"], 21)
        self.assertEqual(result["forbidden_row_count"], Fraction(64, 5))
        self.assertEqual(result["antipodal_point_count"], 40)
        self.assertEqual(
            result["maximum_absolute_inner_product"], Fraction(1, 2)
        )

    def test_dimension_five_normalization(self):
        polynomials = MODULE.normalized_gegenbauer(10)
        self.assertEqual(len(polynomials), 11)
        self.assertTrue(
            all(sum(polynomial, Fraction(0)) == 1
                for polynomial in polynomials)
        )

    def test_d5_representatives_are_distinct_lines(self):
        lines = MODULE.d5_line_representatives()
        self.assertEqual(len(lines), 20)
        self.assertEqual(len(set(lines)), 20)
        self.assertFalse(any(tuple(-x for x in row) in set(lines) for row in lines))


if __name__ == "__main__":
    unittest.main()
