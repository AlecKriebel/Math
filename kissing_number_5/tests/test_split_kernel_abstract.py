import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_split_kernel_abstract.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_split_kernel_abstract", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SplitKernelAbstractTests(unittest.TestCase):
    def test_certificate(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["order"], 41)
        self.assertEqual(result["rank_A"], 5)
        self.assertEqual(result["rank_B"], 14)
        self.assertLessEqual(result["rank_R"], 19)
        self.assertLessEqual(result["rank_K"], 20)
        self.assertTrue(result["all_K_offdiagonal_nonpositive"])
        self.assertTrue(result["full_entry_range_violated"])
        self.assertTrue(result["d5_extension_with_full_range_impossible"])

    def test_quadratic_field_signs(self):
        q = MODULE.Q
        Quad = MODULE.Quad
        self.assertGreater(Quad(-q(3, 10), q(1, 4)).sign(), 0)
        self.assertLess(Quad(-q(3, 5), -q(1, 4)).sign(), 0)


if __name__ == "__main__":
    unittest.main()
