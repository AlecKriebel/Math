import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_one_sided_tukey.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_one_sided_tukey", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OneSidedTukeyTests(unittest.TestCase):
    def test_exact_certificate(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["A_4_sqrt3_upper_bound"], 33)
        self.assertLess(result["delsarte_objective_approx"], 34)
        self.assertEqual(result["one_sided_kissing_upper_bound"], 38)
        self.assertEqual(result["size_38_profiles"], [(32, 6), (33, 5)])

    def test_gegenbauer_normalization(self):
        basis = MODULE.gegenbauer_dimension_four(11)
        self.assertEqual(len(basis), 12)
        self.assertTrue(
            all(MODULE.pevaluate(polynomial, MODULE.ONE) == MODULE.ONE
                for polynomial in basis)
        )

    def test_exact_quadratic_sign(self):
        certificate = MODULE.load_certificate()
        coefficients = certificate["factor_polynomial"][
            "r_coefficients_ascending"
        ]
        r = MODULE.rational_poly(coefficients)
        discriminant = r[1][0] ** 2 - 4 * r[0][0] * r[2][0]
        self.assertEqual(discriminant, MODULE.Q(-4831, 10000))
        self.assertLess(discriminant, 0)


if __name__ == "__main__":
    unittest.main()
