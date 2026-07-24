from __future__ import annotations

import unittest

from experiments.four_point_depth_projection.k7_product_audit import (
    verify_k6_support_no_k7_lift as glue,
)


class K6SupportNoK7LiftTests(unittest.TestCase):
    def test_complete_support_obstruction(self) -> None:
        report = glue.verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["labeled_k6_support"], 49800)
        self.assertEqual(
            report["primary_gluing"]["last_edge_color_trials"], 553700
        )
        self.assertEqual(report["support_compatible_labeled_k7"], 0)
        self.assertEqual(
            report["available_k7_pool_crosscheck"][
                "maximum_supported_k6_faces"
            ],
            2,
        )

    def test_synthetic_constant_color_support_has_one_lift(self) -> None:
        # The all-zero K6 orbit has one labeled element.  Of the seven
        # choices for the missing K7 edge, only color zero makes all seven
        # K6 faces all-zero.  This guards against a verifier that would
        # accidentally reject every support.
        labeled, orbit_sizes = glue.expand_labeled_support(
            ((0,) * 15,)
        )
        self.assertEqual(len(labeled), 1)
        self.assertEqual(dict(orbit_sizes), {1: 1})
        for pair in ((6, 5), (0, 1)):
            report = glue.enumerate_for_face_pair(
                labeled, pair[0], pair[1]
            )
            self.assertEqual(
                report["compatible_ordered_k6_face_pairs"], 1
            )
            self.assertEqual(report["last_edge_color_trials"], 7)
            self.assertEqual(
                report["supported_face_count_histogram"], {2: 6, 7: 1}
            )
            self.assertEqual(
                report["support_compatible_labeled_k7"], 1
            )


if __name__ == "__main__":
    unittest.main()
