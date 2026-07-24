#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_noncentered_integer_degree_mixture import (
    VerificationError,
    verify,
)


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "experiments"
    / "noncentered_integer_degree_repair"
    / "integer_row_mixture_6.json"
)
SOURCE = (
    ROOT
    / "experiments"
    / "noncentered_integer_degree_repair"
    / "candidate_exact_6.json"
)


class NoncenteredIntegerDegreeMixtureTest(unittest.TestCase):
    def test_exact_mixture(self) -> None:
        result = verify(CERTIFICATE, SOURCE)
        self.assertEqual(result["positive_atoms"], 26)
        self.assertEqual(result["complete_row_types"], 855168)

    def test_tampered_weight_is_rejected(self) -> None:
        data = json.loads(CERTIFICATE.read_text())
        data["atoms"][0]["weight"] = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / CERTIFICATE.name
            path.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify(path, SOURCE)

    def test_tampered_source_is_rejected(self) -> None:
        data = json.loads(SOURCE.read_text())
        data["alpha"][0] = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / SOURCE.name
            path.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify(CERTIFICATE, path)


if __name__ == "__main__":
    unittest.main()
