from fractions import Fraction
import unittest

import moving_cutoff_fourth_power_regression as regression


class MovingCutoffFourthPowerRegressionTest(unittest.TestCase):
    def test_exact_exponent_sum(self) -> None:
        delta = Fraction(1, 8)
        row = regression.boundary_exponents(delta)
        self.assertEqual(row["raw_boundary_probability"], Fraction(-9, 4))
        self.assertEqual(
            row["completed_boundary_probability"], Fraction(-1, 4)
        )
        self.assertEqual(row["boundary_endpoint_cost"], Fraction(25, 8))
        self.assertEqual(row["expected_boundary_cost"], Fraction(23, 8))

    def test_sharp_displayed_threshold(self) -> None:
        self.assertTrue(regression.cutoff_is_lower_order(Fraction(1, 8)))
        self.assertFalse(regression.cutoff_is_lower_order(Fraction(1, 7)))
        self.assertFalse(regression.cutoff_is_lower_order(Fraction(1, 6)))

    def test_canonical_cutoff(self) -> None:
        self.assertEqual(regression.canonical_cutoff(), Fraction(1, 8))


if __name__ == "__main__":
    unittest.main()
