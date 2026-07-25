from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
PATH = HERE / "verify_direct_k7_triangle_extension.py"
SPEC = importlib.util.spec_from_file_location("verify_direct_k7", PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class DirectK7TriangleExtensionTests(unittest.TestCase):
    def test_exact_extension(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["positive_atoms"], 51)
        self.assertEqual(
            result["all_sixth_and_seventh_order_principal_determinants"], 0
        )

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
            "edge_color_indices_01_02_03_04_05_06_12_13_14_15_16_23_24_25_26_34_35_36_45_46_56"
        ][0] = 0
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "CERTIFICATE_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()


if __name__ == "__main__":
    unittest.main()
