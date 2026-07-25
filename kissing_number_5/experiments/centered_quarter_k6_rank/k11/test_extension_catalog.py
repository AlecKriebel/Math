from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
PATH = HERE / "verify_extension_catalog.py"
SPEC = importlib.util.spec_from_file_location("verify_k11_catalog", PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class K11ExtensionCatalogTests(unittest.TestCase):
    def test_exact_catalog_completeness(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["labeled_extensions"], 1642)
        self.assertEqual(result["distinct_triangle_count_vectors"], 1508)

    def test_tampered_catalog_is_rejected(self) -> None:
        lines = VERIFY.CATALOG_PATH.read_text().splitlines()
        fields = lines[1].split(",")
        fields[1] = str((int(fields[1]) + 1) % 7)
        lines[1] = ",".join(fields)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.csv"
            path.write_text("\n".join(lines) + "\n")
            with mock.patch.object(VERIFY, "CATALOG_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()


if __name__ == "__main__":
    unittest.main()
