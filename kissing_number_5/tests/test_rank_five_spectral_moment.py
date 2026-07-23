import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_rank_five_spectral_moment.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_rank_five_spectral_moment", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RankFiveSpectralMomentTests(unittest.TestCase):
    def test_certificate(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertGreater(
            Fraction(result["rank_five_squared_violation"]), 0
        )
        self.assertGreater(
            Fraction(result["normalized_squared_violation"]), 0
        )
        self.assertTrue(result["d5_equality"])
        self.assertTrue(result["sharp_small_code_equality"])
        self.assertTrue(result["centered_quartic_bounds_checked"])
        self.assertTrue(result["centered_sixth_identity_checked"])
        self.assertEqual(Fraction(result["cross_polytope_p4"]), 80)
        self.assertGreater(
            Fraction(result["weighted_residual_rank_violation"]), 0
        )
        self.assertTrue(result["newton_e6_identity_checked"])

    def test_newton_identity_nonzero_case(self):
        values = [Fraction(i) for i in range(1, 7)]
        power = MODULE.power_sums(values)
        self.assertEqual(
            MODULE.newton_e6_numerator(power),
            720 * MODULE.elementary_six(values),
        )

    def test_rank_deficient_centered_moments(self):
        MODULE.verify_centered_rank_five_moments(
            [Fraction(1), Fraction(2), Fraction(5)]
        )

    def test_four_cycle_partition(self):
        result = MODULE.verify_four_cycle_expansion()
        self.assertEqual(result["p4"], 80)
        self.assertEqual(result["disjoint_matching"], 8)
        self.assertEqual(result["determinant_integral"], 192)


if __name__ == "__main__":
    unittest.main()
