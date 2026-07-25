import unittest

from experiments.four_point_depth_projection.k5_product_audit.verify_alternative_extension import (
    verify,
)


class AlternativeK5ProductExtensionTest(unittest.TestCase):
    def test_exact_alternative_extension(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["positive_atoms"], 64)
        self.assertEqual(result["product_direction_states"], 560)
        self.assertEqual(result["global_minimum_product_slack"], 0)


if __name__ == "__main__":
    unittest.main()
