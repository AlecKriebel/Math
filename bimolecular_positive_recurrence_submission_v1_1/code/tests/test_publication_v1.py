import unittest
from fractions import Fraction

from bimolecular_pr.publication_v1_calibrations import (
    absorbing_singleton_stationary,
    rate_degeneration_asymptotic_coefficient,
    rate_degeneration_episode,
    stopped_foster_increment,
    two_state_return_cycle_occupation,
)


class PublicationV1CalibrationTests(unittest.TestCase):
    def test_rate_degeneration_exact_finite_recursion(self):
        m = 7
        kappa_0 = Fraction(2, 3)
        kappa_1 = Fraction(5, 4)
        kappa_2 = Fraction(7, 6)
        result = rate_degeneration_episode(m, kappa_0, kappa_1, kappa_2)

        total_a = kappa_0 + kappa_1 * m
        total_ab = kappa_0 + (kappa_1 + kappa_2) * m
        total_zero = kappa_0 + kappa_1 * (m - 1)
        branch_log_m = (
            kappa_0 / total_a
            + (kappa_1 * m / total_a) * (kappa_0 / total_ab)
        )
        branch_log_m_minus_one = (
            (kappa_1 * m / total_a)
            * (kappa_2 * m / total_ab)
            * (-kappa_1 * (m - 1) / total_zero)
        )
        self.assertEqual(result.log_m_coefficient, branch_log_m)
        self.assertEqual(
            result.log_m_minus_one_coefficient,
            branch_log_m_minus_one,
        )
        self.assertGreater(result.log_m_coefficient, 0)
        self.assertLess(result.log_m_minus_one_coefficient, 0)

    def test_rate_degeneration_asymptotic_coefficient(self):
        self.assertEqual(
            rate_degeneration_asymptotic_coefficient(Fraction(5), Fraction(2)),
            Fraction(-2, 7),
        )
        tiny = rate_degeneration_asymptotic_coefficient(
            Fraction(1),
            Fraction(1, 1_000_000),
        )
        self.assertEqual(tiny, Fraction(-1, 1_000_001))
        self.assertLess(abs(tiny), Fraction(1, 1_000_000))

    def test_stopped_random_time_foster_increment(self):
        # From potential 2, jump equally to potentials 0 and 2: E[Delta V] = -1.
        self.assertEqual(
            stopped_foster_increment(
                Fraction(2),
                ((Fraction(1, 2), Fraction(0)), (Fraction(1, 2), Fraction(2))),
            ),
            0,
        )
        # At the stopped exceptional state W_n is constant.
        self.assertEqual(
            stopped_foster_increment(
                Fraction(0),
                (),
                in_exceptional_set=True,
            ),
            0,
        )

    def test_two_state_return_cycle_occupation_is_stationary(self):
        result = two_state_return_cycle_occupation(Fraction(2), Fraction(3))
        self.assertEqual(result.occupation_0, Fraction(1, 2))
        self.assertEqual(result.occupation_1, Fraction(1, 3))
        self.assertEqual(result.expected_cycle_time, Fraction(5, 6))
        self.assertEqual(result.stationary_0, Fraction(3, 5))
        self.assertEqual(result.stationary_1, Fraction(2, 5))
        self.assertEqual(result.stationary_0 * 2, result.stationary_1 * 3)
        self.assertEqual(result.stationary_0 + result.stationary_1, 1)

    def test_absorbing_singleton_has_point_mass_stationary_law(self):
        self.assertEqual(
            absorbing_singleton_stationary((0, 0)),
            {(0, 0): Fraction(1)},
        )


if __name__ == "__main__":
    unittest.main()
