from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from .verify_induced_k5_product import K6_CERTIFICATE, SOURCE, verify


class InducedK5ProductAuditTests(unittest.TestCase):
    def test_exact_audit(self) -> None:
        report = verify(authenticate_catalog=False)
        self.assertEqual(report["status"], "CERTIFIED_VIOLATIONS")
        self.assertEqual(report["k6_positive_atoms"], 51)
        self.assertEqual(report["induced_raw_labeled_faces"], 306)
        self.assertEqual(report["induced_positive_unlabeled_k5_orbits"], 266)
        self.assertEqual(report["distinct_product_rows_checked"], 560)
        self.assertEqual(report["violated_product_rows"], 41)
        self.assertEqual(report["zero_product_rows"], 62)
        self.assertEqual(
            report["strongest_violation_direction"], "-(y+z)"
        )

    def test_tampered_k6_certificate_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = json.loads(K6_CERTIFICATE.read_text())
            data["atoms"][0]["weight"] = "1"
            path = Path(directory) / K6_CERTIFICATE.name
            path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):
                verify(
                    source_path=SOURCE,
                    k6_certificate_path=path,
                    authenticate_catalog=False,
                )


if __name__ == "__main__":
    unittest.main()
