import unittest

from verifiers.verify_edge_conditioned_k4_exact_obstruction import verify


class EdgeConditionedK4ExactObstructionTest(unittest.TestCase):
    def test_exact_k4_orbit_and_farkas_certificate(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["feasible_triangle_types"], 21)
        self.assertEqual(result["gram_psd_k4_orbits"], 198)
        self.assertEqual(result["feasible_labeled_k4_patterns"], 3213)
        self.assertLess(result["special_covariance_constant"], 0)
        self.assertEqual(result["continuous_counting_violation"], 24)
        self.assertEqual(
            result["conclusion"],
            "exact one-row Farkas contradiction",
        )


if __name__ == "__main__":
    unittest.main()
