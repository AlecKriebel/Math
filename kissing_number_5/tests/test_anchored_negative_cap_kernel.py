import unittest

from verifiers.verify_anchored_negative_cap_kernel import verify


class AnchoredNegativeCapKernelTest(unittest.TestCase):
    def test_exact_aggregate_evaluations(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertGreater(result["local_full_negative_total"], 0)
        self.assertGreater(result["local_minimum_subset_total"], 0)
        self.assertGreater(
            result["historical_full_nonpositive_total_normalized"], 0
        )
        self.assertGreater(
            result["historical_minimum_subset_total_normalized"], 0
        )
        self.assertGreater(result["d5_direct_and_aggregate_total"], 0)
        self.assertEqual(
            result["conclusion"],
            "strict positive slack; neither witness separated",
        )


if __name__ == "__main__":
    unittest.main()
