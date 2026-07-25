import unittest

from verifiers.verify_local5_degree5_exact_separator import verify


class Local5Degree5ExactSeparatorTest(unittest.TestCase):
    def test_exact_dual_separator(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["feasible_triangle_types"], 21)
        self.assertEqual(result["active_inequalities"], 14)
        self.assertGreater(
            result["dual_lower_bound_for_minus_margin"], 0
        )
        self.assertEqual(
            set(result["nonbasic_coefficients"]), {6, 7, 10}
        )
        self.assertTrue(
            all(
                value < 0
                for value in result["nonbasic_coefficients"].values()
            )
        )


if __name__ == "__main__":
    unittest.main()
