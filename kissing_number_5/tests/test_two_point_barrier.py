import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_two_point_barrier.py"
SPEC = importlib.util.spec_from_file_location("verify_two_point_barrier", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TwoPointBarrierTests(unittest.TestCase):
    def test_exact_witness(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["mass"], 41)
        self.assertEqual(result["minimum_moment"], Fraction(1027, 16000))
        self.assertEqual(result["minimum_moment_degree"], 2)

    def test_normalization_and_recurrence(self):
        for t in MODULE.NODES:
            values = MODULE.zonal_values(t, 12)
            self.assertEqual(values[0], 1)
            self.assertEqual(values[1], t)
        self.assertTrue(
            all(value == 1 for value in MODULE.zonal_values(Fraction(1), 20))
        )

    def test_strict_support_and_pair_parity(self):
        self.assertTrue(all(t < Fraction(1, 2) for t in MODULE.NODES))
        self.assertTrue(all(count % 2 == 0 for count in MODULE.COUNTS))
        self.assertEqual(sum(MODULE.COUNTS), 41 * 40)


if __name__ == "__main__":
    unittest.main()
