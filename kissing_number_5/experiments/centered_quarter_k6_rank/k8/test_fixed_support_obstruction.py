from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
PATH = HERE / "verify_fixed_support_obstruction.py"
SPEC = importlib.util.spec_from_file_location("verify_k8_fixed", PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class FixedK7SupportK8Tests(unittest.TestCase):
    def test_exact_obstruction(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["support_compatible_labeled_k8"], 0)

    def test_tampered_source_hash_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        data["source_k7_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "CERTIFICATE_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()


if __name__ == "__main__":
    unittest.main()
