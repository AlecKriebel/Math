from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from .verify_direct_k6_product_semantics import CERTIFICATE, SOURCE, verify


class DirectK6ProductSemanticsTests(unittest.TestCase):
    def test_exact_audit(self) -> None:
        report = verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["positive_atoms"], 51)
        self.assertEqual(report["rows_checked"], 560)
        self.assertEqual(report["violating_rows"], 41)
        self.assertEqual(report["rank"], "every atom exactly 5")

    def test_tampering_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = json.loads(CERTIFICATE.read_text())
            data["atoms"][0]["weight"] = "1"
            path = Path(directory) / CERTIFICATE.name
            path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):
                verify(SOURCE, path)


if __name__ == "__main__":
    unittest.main()
