import unittest

from verifiers.verify_local_hybrid_degree3_rank import verify


class LocalHybridDegreeThreeRankTest(unittest.TestCase):
    def test_exact_certificate(self):
        result = verify()
        self.assertEqual(result["triple_type_count"], 20)
        self.assertEqual(result["deep_0_wedges"], 275)
        self.assertEqual(result["deep_01_wedges"], 308)
        self.assertEqual(result["mixed_01_wedges"], 30)
        self.assertEqual(result["type_1_wedges"], 3)
        self.assertLess(result["rank_five_residual"], 0)
        self.assertLess(result["color_variance_violation"], 0)
        self.assertLess(result["degree_4_failure"], 0)
        self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
