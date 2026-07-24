from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_harmonic_rank_frame_barrier import verify


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "certificates"
    / "fixed41_bv_fullradial_k16_pseudodistribution.json"
)


class HarmonicRankFrameBarrierTests(unittest.TestCase):
    def test_certificate_passes(self) -> None:
        result = verify(SOURCE)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(result["checked_harmonic_subsets"]), 11)

    def test_tampered_mass_is_rejected(self) -> None:
        payload = json.loads(SOURCE.read_text())
        payload["alpha"][0] = "1"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(payload))
            with self.assertRaises(AssertionError):
                verify(path)


if __name__ == "__main__":
    unittest.main()
