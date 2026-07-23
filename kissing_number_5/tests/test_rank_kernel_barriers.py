import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_rank_kernel_barriers.py"
SPEC = importlib.util.spec_from_file_location("verify_rank_kernel_barriers", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RankKernelBarrierTests(unittest.TestCase):
    def test_finite_field_counterexample(self):
        result = MODULE.verify_finite_field_counterexample()
        self.assertEqual(result["full_order"], 49)
        self.assertEqual(result["full_rank_M"], 19)
        self.assertEqual(result["principal_order"], 41)
        self.assertLessEqual(result["principal_rank_M"], 19)
        self.assertEqual(result["clique_quadratic_form_M"], Fraction(-2))

    def test_d6_polynomial_kernel(self):
        result = MODULE.verify_d6_kernel()
        self.assertEqual(result["order"], 60)
        self.assertEqual(result["rank"], 27)
        self.assertLess(result["rank"], result["order"] / 2)


if __name__ == "__main__":
    unittest.main()
