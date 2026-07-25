import unittest

from verifiers.verify_local_hybrid_degree3 import verify


class LocalHybridDegreeThreeTest(unittest.TestCase):
    def test_exact_certificate(self):
        result = verify()
        self.assertEqual(result["triple_type_count"], 20)
        self.assertEqual(
            result["minimum_3_by_3_determinant"].numerator, 278991
        )
        self.assertEqual(result["deep_0_wedges"], 275)
        self.assertEqual(result["deep_01_wedges"], 308)
        self.assertEqual(result["mixed_01_wedges"], 30)
        self.assertEqual(result["type_1_wedges"], 3)
        self.assertGreater(result["rank_five_violation"], 0)
        self.assertGreater(
            result["color_covariance_minimum_positive_minor"], 0
        )
        self.assertLess(result["first_degree_4_failure"], 0)
        self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
