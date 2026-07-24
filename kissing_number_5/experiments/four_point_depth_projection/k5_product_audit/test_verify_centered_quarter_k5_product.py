from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path
import tempfile
import unittest

from .verify_centered_quarter_k5_product import (
    CERTIFICATE,
    EXTENSION,
    SOURCE,
    verify,
)
from .verify_two_violations_independent import audit as independent_audit


class CenteredQuarterK5ProductAuditTests(unittest.TestCase):
    def test_two_exact_violations(self) -> None:
        report = verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["positive_orbits"], 51)
        self.assertEqual(report["distinct_labeled_atoms"], 2940)
        self.assertEqual(report["applicable_rows"], 7)
        self.assertEqual(
            report["violated_rows"],
            [("-1/2", "1/2", 1), ("-1/4", "1/2", 3)],
        )
        self.assertEqual(
            report["strongest_normalized_slack"],
            Q(-7819447598603429, 2083692000000000000),
        )

    def test_tampered_claim_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = json.loads(CERTIFICATE.read_text())
            data["rows"][2]["scaled_slack_right_minus_left"] = "0"
            path = Path(directory) / CERTIFICATE.name
            path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
            with self.assertRaises(AssertionError):
                verify(SOURCE, EXTENSION, path)

    def test_independent_small_verifier(self) -> None:
        reports = independent_audit()
        self.assertEqual(len(reports), 2)
        self.assertEqual(
            reports[0]["exact_scaled_violation"],
            "7819447598603429/228000000000000",
        )


if __name__ == "__main__":
    unittest.main()
