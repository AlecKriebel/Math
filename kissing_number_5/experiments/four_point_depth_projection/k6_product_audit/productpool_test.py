from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path
import tempfile
import unittest

from .directaudit_k6_product import EXPECTED_WORST, audit
from .productpool_verify import EXTENSION, POOL, SOURCE, verify


class K6ProductAuditTests(unittest.TestCase):
    def test_stored_direct_extension_is_refuted(self) -> None:
        report = audit()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["product_rows_checked"], 560)
        self.assertEqual(report["negative_product_rows"], 41)
        self.assertEqual(report["worst_twice_symmetrized_slack"], EXPECTED_WORST)

    def test_exact_alternative_extension(self) -> None:
        report = verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["positive_atoms"], 74)
        self.assertEqual(report["product_rows"], 560)
        self.assertEqual(report["zero_product_rows"], 113)
        self.assertEqual(
            report["minimum_positive_twice_symmetrized_slack"],
            Q(4741606889923, 12500000000000),
        )

    def test_tampered_alternative_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = json.loads(EXTENSION.read_text())
            data["atoms"][0]["weight"] = "0"
            path = Path(directory) / EXTENSION.name
            path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
            with self.assertRaises(AssertionError):
                verify(SOURCE, POOL, path)


if __name__ == "__main__":
    unittest.main()
