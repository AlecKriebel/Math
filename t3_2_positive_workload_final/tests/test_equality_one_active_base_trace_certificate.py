from fractions import Fraction
import unittest

import equality_one_active_base_trace_certificate as certificate


class EqualityOneActiveBaseTraceCertificateTest(unittest.TestCase):
    def test_exact_q_identity(self) -> None:
        self.assertEqual(
            {
                label: certificate.q_increment(delta)
                for label, delta in certificate.REACTION_DELTAS.items()
            },
            {
                "0->BC": 0,
                "BC->0": 0,
                "B->A": 0,
                "A->AB": -1,
                "AB->2B": 0,
                "2B->B": 1,
            },
        )

    def test_only_two_reactions_change_a(self) -> None:
        self.assertEqual(
            {
                label: certificate.a_increment(delta)
                for label, delta in certificate.REACTION_DELTAS.items()
                if certificate.a_increment(delta)
            },
            {"B->A": 1, "AB->2B": -1},
        )

    def test_exact_a_clock_jump_chain(self) -> None:
        kappa_up = Fraction(2, 3)
        kappa_down = Fraction(5, 7)
        for population in (1, 2, 11):
            up, down = certificate.a_clock_jump_probabilities(
                population, kappa_up, kappa_down
            )
            self.assertEqual(up + down, 1)
            self.assertEqual(up / down, kappa_up / (kappa_down * population))

    def test_promotion_ceiling_has_factorial_tail(self) -> None:
        kappa_up = Fraction(3, 2)
        kappa_down = Fraction(4, 5)
        previous = Fraction(1)
        for ceiling in range(2, 14):
            probability = certificate.a_ceiling_probability(
                ceiling, kappa_up, kappa_down
            )
            self.assertLess(probability, previous)
            self.assertLessEqual(
                probability,
                certificate.a_ceiling_factorial_bound(
                    ceiling, kappa_up, kappa_down
                ),
            )
            previous = probability

    def test_leading_sign_is_rate_independently_negative(self) -> None:
        for phi in (Fraction(1, 100), Fraction(1, 2), Fraction(999, 1000)):
            self.assertEqual(certificate.leading_powered_drift_sign(phi), -1)

    def test_stopped_powered_episode_has_one_full_power_gap(self) -> None:
        self.assertEqual(
            certificate.stopped_power_scaling(4),
            {
                "successful_expected_power": 3,
                "failed_positive_expected_power": 2,
                "strict_power_gap": 1,
            },
        )

    def test_claim_flags_remain_false(self) -> None:
        payload = certificate.certificate()
        self.assertFalse(payload["local_base_trace_analytic_theorem_certified"])
        self.assertFalse(payload["pair_recurrence_certified"])
        self.assertFalse(payload["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
