from fractions import Fraction
import unittest

import equality_bc_trigger_pdmp as trace


class EqualityBCTriggerPDMPTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rates = trace.Rates(
            alpha=Fraction(2),
            beta=Fraction(3),
            lam=Fraction(5),
            mu=Fraction(7),
            nu=Fraction(11),
            delta=Fraction(13),
        )

    def test_exact_q_increment_table(self):
        expected = {
            "0_to_BC": 0,
            "BC_to_0": 0,
            "B_to_A": 0,
            "A_to_AB": -1,
            "AB_to_2B": 0,
            "2B_to_B": 1,
        }
        self.assertEqual(
            {
                reaction: trace.q_increment(reaction)
                for reaction in trace.REACTION_DELTAS
            },
            expected,
        )

    def test_trigger_two_term_coefficients(self):
        c1, c2 = trace.trigger_asymptotic_coefficients(self.rates)
        self.assertEqual(c1, Fraction(5, 3))
        self.assertEqual(c2, Fraction(-10, 3))

        for n in (10_000, 20_000):
            direct = trace.direct_trigger_probability(n, self.rates)
            # The direct first-event term has a different N^-2
            # coefficient; this assertion only checks its N^-1 scale.
            self.assertLess(abs(n * direct - c1), Fraction(1, 100))

    def test_exact_positive_history_and_limit(self):
        coefficient = trace.positive_unit_leading_coefficient(self.rates)
        self.assertEqual(coefficient, Fraction(26, 9))
        n = 100_000
        scaled = n * n * trace.positive_unit_history_probability(
            n, self.rates
        )
        self.assertLess(abs(scaled - coefficient), Fraction(1, 100))

    def test_killed_potential_and_strict_drift(self):
        self.assertEqual(trace.killed_potential(0, self.rates), 0)
        self.assertGreater(trace.killed_potential(1, self.rates), 0)
        self.assertLess(
            trace.killed_potential(1, self.rates),
            self.rates.beta,
        )
        self.assertLess(
            trace.power_drift_leading_coefficient(
                Fraction(9, 10), self.rates
            ),
            0,
        )

    def test_claim_scope(self):
        payload = trace.certificate()
        self.assertFalse(payload["physical_c3_found_by_this_trace"])
        self.assertFalse(payload["global_pair_recurrence_certified"])
        self.assertFalse(
            payload["all_higher_raw_duration_moments_uniform"]
        )


if __name__ == "__main__":
    unittest.main()
