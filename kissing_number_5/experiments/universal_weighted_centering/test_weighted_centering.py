from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent


def load_verifier():
    path = HERE / "verify_weighted_centering.py"
    specification = importlib.util.spec_from_file_location(
        "verify_weighted_centering", path
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class WeightedCenteringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_verifier()
        cls.report = cls.module.verify()

    def test_exact_d5_weight_families(self) -> None:
        self.assertEqual(self.report["status"], "PASS")
        self.assertEqual(self.report["d5_open_hemisphere_depth"], 8)
        self.assertEqual(
            self.report["ill_conditioned_family"]["covariance_rank"],
            5,
        )
        self.assertEqual(
            self.report["two_point_family"]["covariance_rank"],
            1,
        )

    def test_scope_does_not_overclaim(self) -> None:
        self.assertIn("arbitrary centering-weight choice", self.report["scope"])
        self.assertIn(
            "not counterexamples to optimized weight-selection claims",
            self.report["scope"],
        )

    def test_deletion_depth_alone_has_no_quantitative_balance(self) -> None:
        report = self.report["deletion_depth_only_counterexample"]
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["minimum_open_hemisphere_count"], 16)
        self.assertEqual(report["intact_pairs_after_six_deletions"], 14)
        self.assertEqual(report["radial_reach_upper_bound"], "1/1000")
        self.assertEqual(report["max_min_weight_upper_bound"], "1/1000")
        self.assertTrue(report["explicit_pair_is_not_kissing"])


if __name__ == "__main__":
    unittest.main()
