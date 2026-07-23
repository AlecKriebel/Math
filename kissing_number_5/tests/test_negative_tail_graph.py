import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_negative_tail_graph.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_negative_tail_graph", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NegativeTailGraphTests(unittest.TestCase):
    def test_exact_summary(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["vertices"], 41)
        self.assertEqual(result["edge_lower_bound"], 23)
        self.assertEqual(result["ordered_negative_pair_lower_bound"], 46)

    def test_sharp_example(self):
        edges, n = MODULE.sharp_graph()
        self.assertEqual(n, 41)
        self.assertEqual(len(edges), 23)
        self.assertTrue(MODULE.is_triangle_free(edges, n))
        self.assertEqual(MODULE.independent_number_bitset(edges, n), 20)


if __name__ == "__main__":
    unittest.main()
