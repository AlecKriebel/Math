from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_r18_residual_q_energy import (
    DEFAULT_CERTIFICATE,
    VerificationError,
    verify,
)


class R18ResidualQEnergyTests(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(
            result["full_code_unordered_residual_cycle_lower_bound"],
            "2048/315",
        )
        self.assertEqual(
            result["weighted_unordered_residual_cycle_lower_bound"], "64/9"
        )

    def test_tampered_harmonic_coefficient_is_rejected(self) -> None:
        data = json.loads(DEFAULT_CERTIFICATE.read_text())
        data["gegenbauer_coefficients"]["P4"] = "2049/945"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify(path)

    def test_tampered_residual_bound_is_rejected(self) -> None:
        data = json.loads(DEFAULT_CERTIFICATE.read_text())
        data["weighted_unordered_residual_cycle_lower_bound"] = "63/9"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify(path)


if __name__ == "__main__":
    unittest.main()
