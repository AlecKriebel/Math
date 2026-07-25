"""Tests for the exact fixed-D5 saturation verifier."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
VERIFIER = RESEARCH_ROOT / "verifiers" / "verify_d5_saturation.py"


def load_verifier_module():
    specification = importlib.util.spec_from_file_location(
        "verify_d5_saturation", VERIFIER
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class D5SaturationVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.verifier = load_verifier_module()

    def test_exact_root_enumeration(self) -> None:
        report = self.verifier.verify_root_configuration()
        self.assertEqual(report["root_count"], 40)
        self.assertEqual(
            report["unnormalized_distinct_inner_products"],
            [-2, -1, 0, 1],
        )
        self.assertEqual(
            report["normalized_max_distinct_inner_product"], "1/2"
        )

    def test_exact_polynomial_identity(self) -> None:
        report = self.verifier.verify_universal_inequality_identity()
        self.assertEqual(
            report["difference_coefficients"], ["1/4", "5/2", "-11/4"]
        )

    def test_sharp_constant_and_strict_gap(self) -> None:
        report = self.verifier.verify_sharp_constant()
        self.assertEqual(report["saturation_lower_bound_squared"], "2/5")
        self.assertEqual(report["kissing_threshold_squared"], "1/4")
        self.assertEqual(report["strict_squared_gap"], "3/20")

    def test_command_line_report(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(VERIFIER)],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(completed.stdout)
        self.assertEqual(
            report["claim"],
            "fixed D5 is saturated against adding one point",
        )
        self.assertEqual(report["arithmetic"], "exact integers and fractions")


if __name__ == "__main__":
    unittest.main()
