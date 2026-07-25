import unittest

from verifiers.verify_weighted_residual_barrier import verify


class WeightedResidualBarrierTest(unittest.TestCase):
    def test_exact_pseudo_incidence(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["deep_0_wedges"], 275)
        self.assertEqual(result["deep_01_wedges"], 308)
        self.assertGreater(result["weighted_residual_scalar"], 0)
        self.assertLess(result["rejected_k0_direction"], 0)
        self.assertLess(result["rejected_k1_direction"], 0)
        self.assertLess(result["first_degree_3_failure"], 0)


if __name__ == "__main__":
    unittest.main()
