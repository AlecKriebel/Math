import unittest

from verifiers.verify_positive_circuit_pair_catalog import verify


class PositiveCircuitPairCatalogTest(unittest.TestCase):
    def test_exact_d5_catalog_and_rank_six_near_counterexample(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["d5_circuit_size_pairs"], 15)
        self.assertEqual(result["d5_open_hemisphere_minimum"], 8)
        self.assertEqual(result["rank_six_near_counterexample_size"], 41)
        self.assertEqual(result["rank_six_near_counterexample_rank"], 6)
        self.assertEqual(
            result["conclusion"],
            "circuit sizes and two kernel vectors alone do not separate",
        )


if __name__ == "__main__":
    unittest.main()
