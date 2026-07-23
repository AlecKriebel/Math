import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_split_kernel_full_interval.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_split_kernel_full_interval", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SplitKernelFullIntervalTests(unittest.TestCase):
    def test_certificate(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["order"], 41)
        self.assertEqual(result["rank_A"], 5)
        self.assertEqual(result["rank_B"], 14)
        self.assertEqual(result["rank_R"], 19)
        self.assertEqual(result["rank_K"], 19)
        self.assertEqual(result["negative_eigenvalues_K"], 1)
        self.assertTrue(result["full_interval_verified"])
        self.assertTrue(result["linear_source_violates_code_bound"])

    def test_machin_interval(self):
        lower, upper = MODULE.pi_bounds(30, 8)
        self.assertLess(lower, upper)
        self.assertGreater(lower, MODULE.Q(3))
        self.assertLess(upper, MODULE.Q(22, 7))


if __name__ == "__main__":
    unittest.main()
