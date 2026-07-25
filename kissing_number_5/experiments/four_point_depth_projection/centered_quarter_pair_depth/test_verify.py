"""Regression tests for the exact continuum pair-depth audit."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("verify.py")
SPEC = importlib.util.spec_from_file_location(
    "centered_quarter_pair_depth_verify", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VERIFY
SPEC.loader.exec_module(VERIFY)


class CenteredQuarterPairDepthTest(unittest.TestCase):
    def test_exact_continuum_audit(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(
            result["global_minimum_slack"],
            "9426027066077596589/342712500000000000",
        )
        self.assertEqual(
            result["global_minimum_base_inner_product"], "1/4"
        )
        self.assertEqual(
            result["attaining_direction"], "(lambda,mu)=(1,-1)"
        )
        self.assertEqual(
            result["base_results"]["0"]["critical_slopes"], 48
        )

    def test_source_tampering_is_rejected(self) -> None:
        source = json.loads(VERIFY.SOURCE.read_text())
        source["alpha"][0] = "1"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(source))
            with self.assertRaises(AssertionError):
                VERIFY.verify(path)


if __name__ == "__main__":
    unittest.main()
