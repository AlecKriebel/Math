from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_centered_quarter_k4_extension import verify


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
EXTENSION = ROOT / "certificates" / "centered_quarter_k4_extension.json"


class CenteredQuarterK4ExtensionTests(unittest.TestCase):
    def test_exact_extension(self) -> None:
        report = verify(SOURCE, EXTENSION)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["positive_extension_atoms"], 51)
        self.assertEqual(report["triangle_face_marginal"], "exact")

    def test_tampered_weight_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = json.loads(EXTENSION.read_text())
            data["atoms"][0]["weight"] = str(
                Fraction(data["atoms"][0]["weight"])
                + Fraction(1, 10**12)
            )
            path = Path(directory) / EXTENSION.name
            path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
            with self.assertRaises(AssertionError):
                verify(SOURCE, path)


if __name__ == "__main__":
    unittest.main()
