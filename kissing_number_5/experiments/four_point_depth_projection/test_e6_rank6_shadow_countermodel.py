import unittest

from experiments.four_point_depth_projection.verify_e6_rank6_shadow_countermodel import (
    verify,
)


class E6RankSixShadowCountermodelTest(unittest.TestCase):
    def test_exact_countermodel(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["cardinality"], 41)
        self.assertEqual(result["gram_rank"], 6)
        self.assertEqual(result["maximum_inner_product"].numerator, 1)
        self.assertEqual(result["maximum_inner_product"].denominator, 2)
        self.assertEqual(result["frame_subsets_checked"], 38760)
        self.assertEqual(
            result["common_pair_capacity_maxima"],
            {"-2": 0, "-1": 1, "0": 5, "1": 7},
        )


if __name__ == "__main__":
    unittest.main()
