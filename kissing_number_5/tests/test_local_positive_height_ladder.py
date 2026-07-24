#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_local_positive_height_ladder import (
    VerificationError,
    verify,
)


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "local_positive_height_ladder.json"


class LocalPositiveHeightLadderTests(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify(CERTIFICATE)
        self.assertEqual(
            result["integer_bounds"],
            {"3/10": 22, "1/3": 21, "3/8": 20, "2/5": 19},
        )

    def test_tampered_coefficient_is_rejected(self) -> None:
        data = json.loads(CERTIFICATE.read_text())
        data["bounds"][0]["gegenbauer_coefficients"][0] = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify(path)

    def test_missing_component_is_rejected(self) -> None:
        data = json.loads(CERTIFICATE.read_text())
        data["bounds"][2]["components"].pop()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify(path)


if __name__ == "__main__":
    unittest.main()
