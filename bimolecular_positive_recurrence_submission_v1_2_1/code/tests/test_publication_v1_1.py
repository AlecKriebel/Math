import unittest
from fractions import Fraction

from bimolecular_pr.episode_bounds import scalar_envelope_pointwise_increment
from bimolecular_pr.network import Channel, Network
from bimolecular_pr.publication_v1_calibrations import (
    rate_degeneration_asymptotic_coefficient,
)
from bimolecular_pr.publication_v1_1_calibrations import (
    ack_marked_target_episode,
    ack_marked_target_log_coefficient,
    ack_unshifted_entropy_drift,
    directed_cycle_return_occupation,
    rate_degeneration_fixed_m_limit,
)
from bimolecular_pr.state_cycle import (
    finite_accessibility_is_symmetric,
    finite_reachability,
    finite_transition_graph,
    lifted_return_cycle,
)
from bimolecular_pr.target_augmented import (
    add_weighted_signature,
    expected_increment_signature,
    rational_log_signature,
)


def ack_network(rates):
    k1, k2, k3, k4, k5 = rates
    a = (1, 0, 0)
    ab = (1, 1, 0)
    ac = (1, 0, 1)
    c = (0, 0, 1)
    two_b = (0, 2, 0)
    return Network(
        ("A", "B", "C"),
        (
            Channel(a, ab, k1, "r1"),
            Channel(ab, ac, k2, "r2"),
            Channel(ac, c, k3, "r3"),
            Channel(c, two_b, k4, "r4"),
            Channel(two_b, a, k5, "r5"),
        ),
    )


def weighted_episode_signature(network, n):
    phases = (
        ((n, 1, 0), (1, 0, 0), network.channels[0]),
        ((n, 2, 0), (1, 1, 0), network.channels[1]),
        ((n, 1, 1), (1, 0, 1), network.channels[2]),
        ((n - 1, 1, 1), (0, 0, 1), None),
    )
    out = {}
    reach_probability = Fraction(1)
    for state, target, designated in phases:
        add_weighted_signature(
            out,
            expected_increment_signature(network, state, target),
            reach_probability,
        )
        if designated is not None:
            reach_probability *= (
                network.propensity(state, designated) / network.total_rate(state)
            )
    return out


def formal_episode_signature(episode, n):
    out = {}
    add_weighted_signature(
        out, rational_log_signature(Fraction(2)), episode.log2_coefficient
    )
    add_weighted_signature(
        out, rational_log_signature(Fraction(n)), episode.log_n_coefficient
    )
    add_weighted_signature(
        out,
        rational_log_signature(Fraction(n - 1)),
        episode.log_n_minus_one_coefficient,
    )
    return out


class PublicationV11StateCycleTests(unittest.TestCase):
    def test_lifted_return_cycle_handles_zero_complex_and_boundary(self):
        network = Network(
            ("A",),
            (
                Channel((0,), (1,), Fraction(2), "birth"),
                Channel((1,), (0,), Fraction(3), "death"),
            ),
        )
        checked = 0
        for state in ((0,), (1,), (4,)):
            for channel in network.enabled_channels(state):
                witness = lifted_return_cycle(network, state, channel)
                self.assertEqual(witness.states[0], state)
                self.assertEqual(witness.states[-1], state)
                self.assertTrue(all(value >= 0 for x in witness.states for value in x))
                checked += 1
        self.assertEqual(checked, 5)

    def test_lifted_cycles_allow_multiple_linkages_parallel_channels_and_same_displacement(self):
        # The two linkage classes are {A,B} and {2A,A+B}.  The first and
        # third displayed reactions have the same population displacement.
        network = Network(
            ("A", "B"),
            (
                Channel((1, 0), (0, 1), Fraction(2), "a_to_b_1"),
                Channel((1, 0), (0, 1), Fraction(5), "a_to_b_parallel"),
                Channel((0, 1), (1, 0), Fraction(3), "b_to_a"),
                Channel((2, 0), (1, 1), Fraction(7), "two_a_to_ab"),
                Channel((1, 1), (2, 0), Fraction(11), "ab_to_two_a"),
            ),
        )
        self.assertFalse(network.strongly_connected())
        state = (4, 3)
        for channel in network.enabled_channels(state):
            witness = lifted_return_cycle(network, state, channel)
            self.assertEqual(witness.states[-1], state)
            self.assertEqual(
                witness.residual,
                tuple(a - b for a, b in zip(state, channel.source)),
            )

    def test_finite_reachability_is_symmetric_with_boundary_and_parity_classes(self):
        network = Network(
            ("A", "B"),
            (
                Channel((2, 0), (0, 2), Fraction(2), "forward"),
                Channel((0, 2), (2, 0), Fraction(3), "backward"),
            ),
        )
        shell = {(a, 4 - a) for a in range(5)}
        graph = finite_transition_graph(network, shell)
        self.assertTrue(finite_accessibility_is_symmetric(graph))
        self.assertEqual(finite_reachability(graph, (0, 4)), {(0, 4), (2, 2), (4, 0)})
        self.assertEqual(finite_reachability(graph, (1, 3)), {(1, 3), (3, 1)})
        for state in shell:
            reachable = finite_reachability(graph, state)
            self.assertTrue(
                all(successor in reachable for x in reachable for successor in graph[x])
            )

    def test_absorbing_singleton_is_closed_reachability_class(self):
        network = Network(
            ("A",),
            (
                Channel((1,), (2,), Fraction(1), "up"),
                Channel((2,), (1,), Fraction(1), "down"),
            ),
        )
        graph = finite_transition_graph(network, {(0,)})
        self.assertEqual(graph, {(0,): frozenset()})
        self.assertEqual(finite_reachability(graph, (0,)), {(0,)})
        self.assertTrue(finite_accessibility_is_symmetric(graph))


class PublicationV11AlgebraTests(unittest.TestCase):
    def test_corrected_fixed_m_rate_limit_is_a_times_one_plus_p(self):
        result = rate_degeneration_fixed_m_limit(7, Fraction(2, 3), Fraction(5, 4))
        self.assertEqual(
            result.limit_log_m_coefficient,
            result.a_log_m_coefficient * (1 + result.continue_from_a),
        )
        self.assertGreater(result.limit_log_m_coefficient, 0)
        self.assertEqual(result.limit_log_m_minus_one_coefficient, 0)

    def test_rate_example_log_coefficient_is_exact(self):
        self.assertEqual(
            rate_degeneration_asymptotic_coefficient(Fraction(5), Fraction(2)),
            Fraction(-2, 7),
        )

    def test_scalar_envelope_monotonicity_on_exact_grid(self):
        count = 0
        for q in (Fraction(1, 9), Fraction(1, 2), Fraction(7, 5)):
            for p in (Fraction(1, 13), Fraction(3, 7), Fraction(1)):
                for lower, upper in (
                    (Fraction(-20), Fraction(-20)),
                    (Fraction(-20), Fraction(-1, 3)),
                    (Fraction(-1, 3), Fraction(8)),
                ):
                    increment = scalar_envelope_pointwise_increment(q, p, lower, upper)
                    self.assertEqual(increment, q * p * (upper - lower))
                    self.assertGreaterEqual(increment, 0)
                    count += 1
        self.assertEqual(count, 27)

    def test_ack_example_unshifted_drift(self):
        drift = ack_unshifted_entropy_drift(11, Fraction(7, 5))
        self.assertEqual(drift.log2_coefficient, Fraction(154, 5))
        self.assertEqual(drift.constant, Fraction(-77, 5))

    def test_ack_carried_target_A_is_explicitly_reachable(self):
        n = 7
        network = ack_network((Fraction(1),) * 5)
        state = (1, 0, 0)
        # Each three-reaction block raises A by one and restores B to zero.
        for _ in range(n - 2):
            state = network.successor(state, network.channels[0])
            state = network.successor(state, network.channels[0])
            state = network.successor(state, network.channels[4])
        self.assertEqual(state, (n - 1, 0, 0))
        for _ in range(3):
            state = network.successor(state, network.channels[0])
        self.assertEqual(state, (n - 1, 3, 0))
        state = network.successor(state, network.channels[4])
        self.assertEqual(state, (n, 1, 0))
        self.assertEqual(network.channels[4].target, (1, 0, 0))

    def test_ack_complete_episode_formula_matches_generic_factorial_identity(self):
        rate_sets = (
            (Fraction(1), Fraction(2), Fraction(3), Fraction(5), Fraction(7)),
            (
                Fraction(2, 3),
                Fraction(5, 4),
                Fraction(7, 6),
                Fraction(11, 5),
                Fraction(13, 7),
            ),
        )
        for rates in rate_sets:
            network = ack_network(rates)
            for n in (2, 7, 12):
                episode = ack_marked_target_episode(n, *rates)
                self.assertEqual(
                    formal_episode_signature(episode, n),
                    weighted_episode_signature(network, n),
                )

    def test_ack_episode_has_strict_negative_logarithmic_coefficient(self):
        coefficient = ack_marked_target_log_coefficient(
            Fraction(2), Fraction(3), Fraction(5)
        )
        alpha = (
            Fraction(2, 5)
            * Fraction(6, 8)
            * Fraction(5, 10)
        )
        self.assertEqual(coefficient, -alpha)
        self.assertLess(coefficient, 0)

    def test_three_state_stationary_return_cycle_normalization(self):
        rates = (Fraction(2), Fraction(3), Fraction(5))
        result = directed_cycle_return_occupation(rates)
        self.assertEqual(result.expected_cycle_time, Fraction(31, 30))
        self.assertEqual(sum(result.stationary, Fraction(0)), 1)
        stationary_fluxes = tuple(
            probability * rate
            for probability, rate in zip(result.stationary, rates)
        )
        self.assertEqual(len(set(stationary_fluxes)), 1)


if __name__ == "__main__":
    unittest.main()
