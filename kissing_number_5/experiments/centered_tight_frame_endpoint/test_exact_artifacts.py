from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "verify_centered_tight_bv.py"


def load_verifier():
    specification = importlib.util.spec_from_file_location(
        "verify_centered_tight_bv", VERIFIER
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class CenteredTightEndpointArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.verifier = load_verifier()
        cls.report = cls.verifier.verify()

    def test_exact_pair_triple_certificate(self) -> None:
        self.assertEqual(self.report["status"], "PASS")
        self.assertEqual(self.report["w0_rank"], 9)
        self.assertEqual(self.report["w1_rank"], 9)
        self.assertEqual(self.report["w2_rank"], 10)
        self.assertEqual(self.report["sharp_harmonic_rank_cuts_checked"], 27)

    def test_adversarial_scope_boundary_is_recorded(self) -> None:
        self.assertEqual(self.report["stratified_capacity_rows_audited"], 48)
        self.assertEqual(self.report["stratified_capacity_failures"], 4)
        self.assertLess(
            self.verifier.Q(
                self.report["minimum_stratified_capacity_slack"]
            ),
            0,
        )
        source = json.loads(
            (HERE / "centered_tight_bv_pseudodistribution.json").read_text()
        )
        self.assertIn("not a Gram matrix", source["scope"])
        self.assertIn("four", source["known_failure"])


if __name__ == "__main__":
    unittest.main()
