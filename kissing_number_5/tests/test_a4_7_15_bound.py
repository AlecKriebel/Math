from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_a4_7_15_bound import VerificationError, verify


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "a4_7_15_delsarte.json"


class A4SevenFifteenthsTests(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        self.assertEqual(verify(CERTIFICATE)["integer_bound"], 23)

    def test_tampered_coefficient_is_rejected(self) -> None:
        payload = json.loads(CERTIFICATE.read_text())
        payload["gegenbauer_coefficients"][0] = "1/10"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(payload))
            with self.assertRaises(VerificationError):
                verify(path)

    def test_tampered_objective_is_rejected(self) -> None:
        payload = json.loads(CERTIFICATE.read_text())
        payload["delsarte_objective"] = "23"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(payload))
            with self.assertRaises(VerificationError):
                verify(path)


if __name__ == "__main__":
    unittest.main()
