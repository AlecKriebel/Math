"""Independent entry points for the exact Lorentzian graph certificate."""

from __future__ import annotations

import unittest

from verifiers.verify_lorentzian_inertia_graph import verify


class LorentzianInertiaGraphTests(unittest.TestCase):
    def test_fast_algebra_and_graph_checks(self) -> None:
        result = verify(check_depth=False)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["number_of_points"], 41)
        self.assertEqual(result["A_rank"], 6)
        self.assertEqual(
            result["A_inertia_positive_negative_zero"], (5, 1, 35)
        )
        self.assertEqual(result["H_rank"], 6)
        self.assertEqual(result["contact_edges"], 0)
        self.assertGreaterEqual(
            result["minimum_negative_pseudo_inner_product_degree"], 7
        )
        self.assertEqual(
            len(result["disjoint_positive_direction_circuits"]), 2
        )
        self.assertEqual(
            result["D5_calibration"]["D5_W_spectrum"],
            "41^1, 1^34, (-15)^5",
        )
        self.assertEqual(
            result["D5_calibration"]["D5_trace_W_cubed"], 52080
        )

    def test_exact_open_hemisphere_depth(self) -> None:
        result = verify(check_depth=True)
        self.assertEqual(result["open_hemisphere_depth"], 14)
        self.assertEqual(
            sorted(result["depth_witness_positive_negative"]), [14, 23]
        )


if __name__ == "__main__":
    unittest.main()
