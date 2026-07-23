import unittest
from fractions import Fraction as Q

from verifiers.verify_four_point_wedge import verify


class FourPointWedgeTest(unittest.TestCase):
    def test_exact_certificate(self):
        result = verify()
        self.assertEqual(result["pair_classes"], (16, 66, 132, 65, 261, 280))
        self.assertEqual(result["distance_two_pairs"], 246)
        self.assertEqual(result["maximum_common_at_9_over_20"], 8)
        self.assertEqual(result["maximum_pfender_row"], Q(17657, 20000))
        self.assertEqual(result["negative_center_minimum"], Q(161, 1600))
        self.assertEqual(
            result["failing_triple_determinant"],
            Q(-1963857, 4000000),
        )
        self.assertEqual(result["minimum_moment_unnormalized"], Q(30261, 16000))
        self.assertEqual(result["minimum_moment_degree"], 2)
        self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
