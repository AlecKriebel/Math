import unittest
from fractions import Fraction

from bimolecular_pr.network import Channel, Network


def bounded_reachable(network, initial, total_cap, steps=8):
    seen = {initial}
    frontier = {initial}
    for _ in range(steps):
        next_frontier = set()
        for state in frontier:
            for channel in network.enabled_channels(state):
                successor = network.successor(state, channel)
                if sum(successor) <= total_cap and successor not in seen:
                    seen.add(successor)
                    next_frontier.add(successor)
        frontier = next_frontier
    return seen


class BoundaryLatticeTests(unittest.TestCase):
    def test_coordinate_face_is_closed_under_reachable_transitions(self):
        network = Network(
            ("A", "B"),
            (
                Channel((1, 0), (2, 0), Fraction(1)),
                Channel((2, 0), (1, 0), Fraction(1)),
            ),
        )
        reachable = bounded_reachable(network, (1, 0), total_cap=4)
        self.assertEqual(reachable, {(1, 0), (2, 0), (3, 0), (4, 0)})
        self.assertTrue(all(state[1] == 0 for state in reachable))

    def test_parity_restricted_path(self):
        network = Network(
            ("A",),
            (
                Channel((0,), (2,), Fraction(1)),
                Channel((2,), (0,), Fraction(1)),
            ),
        )
        reachable = bounded_reachable(network, (0,), total_cap=8, steps=8)
        self.assertEqual(reachable, {(0,), (2,), (4,), (6,), (8,)})
        self.assertTrue(all(state[0] % 2 == 0 for state in reachable))
        self.assertEqual(network.successor((4,), network.channels[1]), (2,))

    def test_singleton_absorbing_class_is_separate(self):
        network = Network(
            ("A",),
            (
                Channel((1,), (2,), Fraction(1)),
                Channel((2,), (1,), Fraction(1)),
            ),
        )
        self.assertEqual(network.enabled_channels((0,)), ())
        self.assertNotEqual(network.enabled_channels((1,)), ())
        self.assertEqual(bounded_reachable(network, (0,), total_cap=4), {(0,)})

    def test_two_state_finite_irreducible_class(self):
        network = Network(
            ("A", "B"),
            (
                Channel((1, 0), (0, 1), Fraction(2)),
                Channel((0, 1), (1, 0), Fraction(3)),
            ),
        )
        finite_class = {(1, 0), (0, 1)}
        for state in finite_class:
            successors = {
                network.successor(state, channel)
                for channel in network.enabled_channels(state)
            }
            self.assertEqual(successors, finite_class - {state})


if __name__ == "__main__":
    unittest.main()
