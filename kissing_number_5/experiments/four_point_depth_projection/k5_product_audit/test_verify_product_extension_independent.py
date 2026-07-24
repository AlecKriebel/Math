from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from .verify_product_extension_independent import EXTENSION, SOURCE, verify


class ProductExtensionIndependentTests(unittest.TestCase):
    def test_exact_extension(self) -> None:
        report = verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["positive_atoms"], 64)
        self.assertEqual(report["distinct_product_rows_checked"], 560)
        self.assertEqual(report["zero_product_rows"], 89)

    def test_tampered_extension_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = json.loads(EXTENSION.read_text())
            data["atoms"][0]["weight"] = "1"
            path = Path(directory) / EXTENSION.name
            path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):
                verify(SOURCE, path)


if __name__ == "__main__":
    unittest.main()
