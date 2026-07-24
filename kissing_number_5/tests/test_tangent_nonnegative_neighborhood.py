import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_tangent_nonnegative_neighborhood.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_tangent_nonnegative_neighborhood", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TangentNonnegativeNeighborhoodTest(unittest.TestCase):
    def test_exact_certificate(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(
            result["hypothetical_41_minimum_negative_degree"], 7
        )
        self.assertEqual(
            result["hypothetical_41_minimum_negative_edges"], 144
        )


if __name__ == "__main__":
    unittest.main()
