import unittest

from verifiers.verify_local_hybrid_degree3_rank_color import verify


class LocalHybridDegreeThreeRankColorTest(unittest.TestCase):
    def test_exact_certificate(self):
        result = verify()
        self.assertEqual(result["triple_type_count"], 21)
        self.assertEqual(result["color_wedges"][0][0], 275)
        self.assertEqual(result["color_wedges"][0][1], 30)
        self.assertEqual(result["color_wedges"][1][1], 3)
        self.assertLess(result["rank_five_residual"], 0)
        self.assertGreater(
            result["color_covariance_minimum_positive_minor"], 0
        )
        self.assertEqual(
            len(result["individual_color_degree_sequences"]), 5
        )
        self.assertLess(result["degree_4_failure"], 0)
        self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
