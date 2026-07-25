"""Regression tests for the exact Perron/robust-depth barrier."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "verify_perron_robust_depth_hybrid", HERE / "verify.py"
)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class PerronRobustDepthHybridTest(unittest.TestCase):
    def test_certificate(self) -> None:
        report = VERIFY.verify_all()
        self.assertEqual(report["scalar_family"]["sample_size"], 41)
        self.assertEqual(report["d5_depth"]["guaranteed_each_side"], 8)
        self.assertEqual(report["d5_duplicate"]["violating_pairs"], 1)
        self.assertEqual(report["centered_endpoint"]["rho"], "42")

    def test_quadratic_field_signs(self) -> None:
        q = VERIFY.Quadratic
        self.assertGreater(q(0, 1, 3).sign(), 0)
        self.assertGreater((q(0, 1, 3) - q(3, 0, 3) / 2).sign(), 0)
        self.assertLess((q(0, 1, 3) - q(7, 0, 3) / 4).sign(), 0)


if __name__ == "__main__":
    unittest.main()
