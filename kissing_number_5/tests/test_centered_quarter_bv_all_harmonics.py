from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_centered_quarter_bv_all_harmonics import verify


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
TAIL = ROOT / "certificates" / "centered_quarter_bv_all_harmonics.json"


class CenteredQuarterBVAllHarmonicsTests(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        report = verify(SOURCE, TAIL)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["w0_rank"], 6)
        self.assertEqual(report["w1_rank"], 5)
        self.assertEqual(report["pair_moment_degree_one"], "0")

    def test_tampered_mass_is_rejected_after_rehash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            source_data = json.loads(SOURCE.read_text())
            source_data["alpha"][0] = str(
                Fraction(source_data["alpha"][0]) + Fraction(1, 10**12)
            )
            source_path = temporary / SOURCE.name
            source_path.write_text(
                json.dumps(source_data, indent=2, sort_keys=True) + "\n"
            )
            tail_data = json.loads(TAIL.read_text())
            tail_data["source_sha256"] = hashlib.sha256(
                source_path.read_bytes()
            ).hexdigest()
            tail_path = temporary / TAIL.name
            tail_path.write_text(
                json.dumps(tail_data, indent=2, sort_keys=True) + "\n"
            )
            with self.assertRaises(AssertionError):
                verify(source_path, tail_path)


if __name__ == "__main__":
    unittest.main()
