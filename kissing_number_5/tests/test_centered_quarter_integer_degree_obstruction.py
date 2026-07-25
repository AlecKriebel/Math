#!/usr/bin/env python3
"""Regression tests for the exact integer degree-moment verifier."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_centered_quarter_integer_degree_obstruction import (
    verify,
)


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "certificates"
    / "centered_quarter_integer_degree_obstruction.json"
)
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"


class IntegerDegreeObstructionTest(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify(CERTIFICATE, SOURCE)
        self.assertEqual(result["row_types_checked"], 27041)
        self.assertTrue(result["expected_value"].startswith("-"))

    def test_tampered_coefficient_is_rejected(self) -> None:
        certificate = json.loads(CERTIFICATE.read_text())
        certificate["quadratic_terms"][0]["coefficient"] *= -1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(certificate))
            with self.assertRaises(AssertionError):
                verify(path, SOURCE)


if __name__ == "__main__":
    unittest.main()
