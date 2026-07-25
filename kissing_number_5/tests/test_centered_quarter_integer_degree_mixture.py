#!/usr/bin/env python3
"""Regression tests for the exact integer degree-moment mixture."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_centered_quarter_integer_degree_mixture import verify


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT / "certificates" / "centered_quarter_integer_degree_mixture.json"
)
SOURCE = (
    ROOT
    / "experiments"
    / "centered_integer_degree_moments"
    / "repaired_pair_triple_local_3.json"
)


class IntegerDegreeMixtureTest(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify(CERTIFICATE, SOURCE)
        self.assertEqual(result["positive_atoms"], 18)
        self.assertTrue(result["exact_pair_moment_match"])

    def test_tampered_weight_is_rejected(self) -> None:
        certificate = json.loads(CERTIFICATE.read_text())
        certificate["atoms"][0]["weight"] = "1/2"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(certificate))
            with self.assertRaises(AssertionError):
                verify(path, SOURCE)


if __name__ == "__main__":
    unittest.main()
