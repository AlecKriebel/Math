#!/usr/bin/env python3
"""Independent verifier regression test for the saved production portfolio."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "verify_portfolio", ROOT / "verify_portfolio.py"
)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VERIFY)


class PortfolioVerificationTests(unittest.TestCase):
    def test_saved_portfolio(self):
        path = ROOT / "portfolio.json"
        if not path.exists():
            self.skipTest("production portfolio has not yet been generated")
        report = VERIFY.verify(path)
        self.assertEqual(
            report["status"],
            "VERIFIED NUMERICAL REPORTING — NOT AN EXACT CODE",
        )
        self.assertEqual(set(report["best_by_cardinality"]), {"41", "42", "43", "44"})


if __name__ == "__main__":
    unittest.main()
