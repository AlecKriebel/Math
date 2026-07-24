import unittest

from verifiers.verify_local5_degree5_necessary_rank_separator import verify


class Local5Degree5NecessaryRankSeparatorTest(unittest.TestCase):
    def test_exact_necessary_rank_separator(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["rank_band_mode"], "outer")
        self.assertEqual(
            result["variant"], "necessary-rank-outer-bands"
        )
        self.assertGreater(
            result["dual_lower_bound_for_minus_margin"], 0
        )
        self.assertEqual(
            set(result["nonbasic_coefficients"]), {6, 7, 10}
        )


if __name__ == "__main__":
    unittest.main()
