#!/usr/bin/env python3
"""Tamper tests for the repaired local K4/K5 exact certificate."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from .verify_repaired_local_flags import ROOT, verify


AUDIT = Path(__file__).resolve().parent
CERTIFICATE = AUDIT / "repaired_local_k4_k5_extension.json"
SOURCE = (
    ROOT
    / "experiments"
    / "centered_integer_degree_moments"
    / "repaired_pair_triple_local_3.json"
)


class RepairedLocalFlagsTest(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify(CERTIFICATE, SOURCE)
        self.assertEqual(result["k4"]["positive_atoms"], 51)
        self.assertEqual(result["k5"]["positive_atoms"], 51)

    def test_tampered_weight_is_rejected(self) -> None:
        certificate = json.loads(CERTIFICATE.read_text())
        certificate["k5"]["atoms"][0]["weight"] = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / CERTIFICATE.name
            path.write_text(json.dumps(certificate))
            with self.assertRaises(AssertionError):
                verify(path, SOURCE)

    def test_tampered_edge_is_rejected(self) -> None:
        certificate = json.loads(CERTIFICATE.read_text())
        key = "edge_color_indices_01_02_03_12_13_23"
        certificate["k4"]["atoms"][0][key][0] = 7
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / CERTIFICATE.name
            path.write_text(json.dumps(certificate))
            with self.assertRaises(AssertionError):
                verify(path, SOURCE)


if __name__ == "__main__":
    unittest.main()
