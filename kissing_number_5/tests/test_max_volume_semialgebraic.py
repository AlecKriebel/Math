import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = ROOT / "verifiers" / "verify_max_volume_semialgebraic.py"
CERTIFICATE_PATH = (
    ROOT / "certificates" / "max_volume_semialgebraic_reduction.json"
)

SPEC = importlib.util.spec_from_file_location("max_volume_verifier", VERIFIER_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class MaxVolumeSemialgebraicVerifierTests(unittest.TestCase):
    def test_certificate_passes(self):
        result = MODULE.verify(CERTIFICATE_PATH)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["projected_code_upper_bound"], 32)
        self.assertEqual(result["semialgebraic_variable_count"], 190)

    def test_tampered_coefficient_fails(self):
        data = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
        data["gegenbauer_coefficients"][2] = "1"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(AssertionError):
                MODULE.verify(path)

    def test_tampered_determinant_bound_fails(self):
        data = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
        data["basis_gram_determinant_lower_bound"] = "1/100"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(AssertionError):
                MODULE.verify(path)


if __name__ == "__main__":
    unittest.main()
