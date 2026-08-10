from fractions import Fraction
import unittest

import one_active_nested_entry_obstruction as obstruction


class OneActiveNestedEntryObstructionTests(unittest.TestCase):
    def test_pair_is_in_exact_candidate_branch(self):
        result = obstruction.certificate()
        self.assertEqual(
            result["pair"],
            (("0", "AC"), ("2A", "2B", "AB", "BC")),
        )
        self.assertFalse(result["uniform_old_debt_service_probability"])
        self.assertTrue(result["stopped_network_trace_certified"])
        self.assertFalse(result["global_recurrence_certified"])

    def test_positive_debt_returns_to_the_inactive_base(self):
        state, debt = obstruction.apply_history(100)
        self.assertEqual(state, (0, 0, 102))
        self.assertEqual(debt, 2)

    def test_service_race_vanishes_like_inverse_C(self):
        alpha = Fraction(3, 2)
        beta = Fraction(5, 4)
        values = [
            obstruction.second_birth_before_exit_probability(
                n, alpha, beta
            )
            for n in (10, 100, 1000)
        ]
        self.assertGreater(values[0], values[1])
        self.assertGreater(values[1], values[2])
        self.assertEqual(
            limit := alpha / beta,
            Fraction(6, 5),
        )
        self.assertLess(abs(1000 * values[-1] - limit), Fraction(1, 500))

    def test_activation_and_formal_quadratic_coefficients(self):
        gamma = obstruction.leading_activation_coefficient(
            Fraction(2), Fraction(3), Fraction(5)
        )
        self.assertEqual(gamma, Fraction(10, 9))
        coefficient = obstruction.quadratic_trace_coefficient(
            gamma,
            first_loss_moment=Fraction(2, 5),
            second_loss_moment=Fraction(1, 4),
        )
        self.assertLess(coefficient, 0)


if __name__ == "__main__":
    unittest.main()
