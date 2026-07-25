import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = ROOT / "verifiers" / "verify_tverberg_moment_barrier.py"
CERTIFICATE_PATH = ROOT / "certificates" / "tverberg_moment_counterexample.json"
SPEC = importlib.util.spec_from_file_location("tverberg_verifier", VERIFIER_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class TverbergMomentBarrierTests(unittest.TestCase):
    def test_exact_counterexample(self):
        result = MODULE.verify(CERTIFICATE_PATH)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["rank"], 5)
        self.assertEqual(result["maximum_inner_product"], "2/5")

    def test_one_lower_factor_coefficient(self):
        actual = MODULE.moment_coefficients(MODULE.interval_product(1))
        self.assertEqual(actual[2], MODULE.F(-3, 2))

    def test_tampered_block_fails(self):
        data = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
        data["A"][0][0] = -3
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(AssertionError):
                MODULE.verify(path)


if __name__ == "__main__":
    unittest.main()
