from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent


def load_verifier():
    path = HERE / "verify.py"
    specification = importlib.util.spec_from_file_location(
        "weighted_two_design_verify", path
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class WeightedTwoDesignAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = load_verifier().verify()

    def test_known_forty_point_codes(self) -> None:
        self.assertEqual(
            sorted(self.report["known_40_point_codes"]),
            ["D5", "L5", "Q5", "R5"],
        )
        for report in self.report["known_40_point_codes"].values():
            self.assertEqual(report["uniform_covariance_diagonal"], ["1/5"] * 5)

    def test_exact_centered_kissing_counterexample(self) -> None:
        report = self.report["kissing_counterexample"]
        self.assertEqual(report["cardinality"], 32)
        self.assertTrue(report["antipodal"])
        self.assertTrue(report["centered"])
        self.assertEqual(report["separator_values"], ["2"])

    def test_depth_and_frame_are_not_enough(self) -> None:
        report = self.report["depth_frame_countermodel"]
        self.assertEqual(report["cardinality"], 41)
        self.assertEqual(report["open_hemisphere_depth_lower_bound"], 16)
        self.assertEqual(report["deletion_interiority"], 6)
        self.assertEqual(report["frame_floor"], "15059/40000")
        self.assertFalse(report["is_kissing_code"])

    def test_scope_does_not_overclaim(self) -> None:
        self.assertIn(
            "Neither example refutes",
            self.report["scope"],
        )


if __name__ == "__main__":
    unittest.main()
