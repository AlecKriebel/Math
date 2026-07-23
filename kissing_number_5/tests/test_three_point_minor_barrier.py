import unittest
from fractions import Fraction as Q

from verifiers.verify_three_point_minor_barrier import verify


class ThreePointMinorBarrierTest(unittest.TestCase):
    def test_exact_certificate(self):
        result = verify()
        self.assertEqual(result["pair_classes"], (16, 66, 132, 65, 261, 280))
        self.assertEqual(result["distance_two_pairs"], 246)
        self.assertEqual(result["maximum_pfender_row"], Q(17657, 20000))
        self.assertEqual(
            result["minimum_3_by_3"],
            (Q(34771, 400000), (0, 1, 33)),
        )
        self.assertEqual(
            result["minimum_4_by_4"],
            (Q(-2436203, 3125000), (0, 2, 7, 34)),
        )
        self.assertEqual(result["negative_4_by_4_count"], 10670)
        self.assertEqual(result["negative_4_by_4_pattern_count"], 192)
        self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
