import unittest

from verifiers.verify_degree2_bv_barrier import verify


class DegreeTwoBVBarrierTest(unittest.TestCase):
    def test_exact_certificate(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertGreater(result["degree_2_k2_scalar"], 0)
        self.assertLess(result["degree_3_k1_failed_minor"], 0)
        self.assertEqual(result["deep_middle_wedge_count"], 1056)
        self.assertEqual(result["negative_4_by_4_count"], 14608)


if __name__ == "__main__":
    unittest.main()
