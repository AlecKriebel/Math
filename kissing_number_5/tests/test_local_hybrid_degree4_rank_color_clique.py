import unittest

from verifiers.verify_local_hybrid_degree4_rank_color_clique import verify


class LocalHybridDegree4RankColorCliqueTest(unittest.TestCase):
    def test_exact_certificate(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["triple_type_count"], 20)
        self.assertEqual(result["negative_union_minimum_degree"], 22)
        self.assertTrue(result["all_nontrivial_color_unions_graphical"])
        self.assertGreater(result["anchored_cap_kernel_sum"], 0)
        self.assertLess(result["degree_5_failure"], 0)


if __name__ == "__main__":
    unittest.main()
