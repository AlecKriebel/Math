from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
VERIFIER_PATH = HERE / "verify_fixed_support_obstruction.py"
SPEC = importlib.util.spec_from_file_location("verify_k6_fixed", VERIFIER_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class FixedSupportK6ObstructionTests(unittest.TestCase):
    def test_exact_obstruction(self) -> None:
        report = VERIFY.verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["rank_at_most_five_k6_orbits"], 4)
        self.assertEqual(report["k5_face_types_represented"], [0, 21, 39, 46])

    def test_tampered_source_hash_is_rejected(self) -> None:
        data = json.loads(VERIFY.OBSTRUCTION_PATH.read_text())
        data["source_k5_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "OBSTRUCTION_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()

    def test_tampered_farkas_pairing_is_rejected(self) -> None:
        data = json.loads(VERIFY.OBSTRUCTION_PATH.read_text())
        data["farkas_certificate"]["target_pairing"] = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "OBSTRUCTION_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()


if __name__ == "__main__":
    unittest.main()
