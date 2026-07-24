#!/usr/bin/env python3
"""Regression tests for the quarter-grid H1 variance lattice."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_quarter_grid_h1_variance_lattice import (
    DEFAULT_CERTIFICATE,
    VerificationError,
    verify,
)


class QuarterGridH1VarianceLatticeTest(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify()
        self.assertEqual(result["energy_denominator"], 328)
        self.assertEqual(result["scaled_variance_residue_mod_5"], 2)
        self.assertEqual(
            result["allowed_V_at_most_3_over_10"],
            ["1/20", "7/40", "3/10"],
        )

    def test_tampered_residue_is_rejected(self) -> None:
        certificate = json.loads(DEFAULT_CERTIFICATE.read_text())
        certificate["scaled_variance_residue_mod_5"] = 3
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / DEFAULT_CERTIFICATE.name
            path.write_text(json.dumps(certificate))
            with self.assertRaises(VerificationError):
                verify(path)

    def test_tampered_endpoint_is_rejected(self) -> None:
        certificate = json.loads(DEFAULT_CERTIFICATE.read_text())
        certificate["first_nonnegative_levels"][2]["V"] = "299/1000"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / DEFAULT_CERTIFICATE.name
            path.write_text(json.dumps(certificate))
            with self.assertRaises(VerificationError):
                verify(path)


if __name__ == "__main__":
    unittest.main()
