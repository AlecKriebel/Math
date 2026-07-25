from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
VERIFIER_PATH = HERE / "verify_direct_k6_triangle_extension.py"
SPEC = importlib.util.spec_from_file_location("verify_direct_k6", VERIFIER_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class DirectK6TriangleExtensionTests(unittest.TestCase):
    def test_exact_extension(self) -> None:
        report = VERIFY.verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["positive_atoms"], 51)
        self.assertEqual(report["all_full_determinants"], 0)

    def test_tampered_weight_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        data["atoms"][0]["weight"] = str(
            Q(data["atoms"][0]["weight"]) + Q(1, 10**12)
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "CERTIFICATE_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()

    def test_tampered_edge_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        data["atoms"][0][
            "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
        ][0] = 0
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "CERTIFICATE_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()


if __name__ == "__main__":
    unittest.main()
