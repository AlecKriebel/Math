#!/usr/bin/env python3
"""Regression tests for the universal five-bin integer row facet."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_fixed41_coarse_bin_integer_degree_obstruction import (
    VerificationError,
    verify,
)


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "certificates"
    / "fixed41_coarse_bin_integer_degree_obstruction.json"
)
SOURCE = (
    ROOT
    / "certificates"
    / "fixed41_bv_fullradial_k16_pseudodistribution.json"
)


class Fixed41CoarseBinIntegerDegreeTest(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify(CERTIFICATE, SOURCE)
        self.assertEqual(result["row_types_checked"], 32136)
        self.assertEqual(result["zero_count"], 54)
        self.assertTrue(result["expected_value"].startswith("-"))

    def test_tampered_coefficient_is_rejected(self) -> None:
        certificate = json.loads(CERTIFICATE.read_text())
        certificate["quadratic_terms"][0]["coefficient"] *= -1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / CERTIFICATE.name
            path.write_text(json.dumps(certificate))
            with self.assertRaises(VerificationError):
                verify(path, SOURCE)

    def test_tampered_source_is_rejected(self) -> None:
        source = json.loads(SOURCE.read_text())
        source["alpha"][0] = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / SOURCE.name
            path.write_text(json.dumps(source))
            with self.assertRaises(VerificationError):
                verify(CERTIFICATE, path)


if __name__ == "__main__":
    unittest.main()
