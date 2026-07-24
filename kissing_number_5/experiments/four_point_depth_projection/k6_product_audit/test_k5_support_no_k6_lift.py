import unittest

from experiments.four_point_depth_projection.k6_product_audit.verify_k5_support_no_k6_lift import (
    verify,
)


class K5SupportNoK6LiftTest(unittest.TestCase):
    def test_exact_k5_support_has_no_k6_lift(self) -> None:
        report = verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["support_compatible_labeled_k6"], 0)
        self.assertEqual(report["last_edge_color_trials"], 104118)
        self.assertEqual(report["available_pool_rows"], 137296)
        self.assertEqual(
            report["maximum_supported_faces_in_available_pool_atom"], 4
        )


if __name__ == "__main__":
    unittest.main()
