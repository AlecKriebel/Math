import unittest
from fractions import Fraction

from bimolecular_pr.network import Channel, Network, falling_factorial
from bimolecular_pr.target_augmented import (
    direct_exp_increment,
    exp_potential_increment,
    marked_successor,
)


class NetworkTests(unittest.TestCase):
    def test_residual_identity_for_distinct_outcome(self):
        state = (5, 3)
        target = (1, 1)
        channel = Channel((2, 0), (0, 1), Fraction(2), "r")
        self.assertEqual(
            direct_exp_increment(state, target, channel),
            exp_potential_increment(state, target, channel.source),
        )

    def test_residual_identity_with_zero_carried_target(self):
        state = (4, 2)
        target = (0, 0)
        channel = Channel((1, 1), (2, 0), Fraction(3), "r")
        self.assertEqual(
            direct_exp_increment(state, target, channel),
            exp_potential_increment(state, target, channel.source),
        )

    def test_zero_pure_binary_and_mixed_falling_factorials(self):
        self.assertEqual(falling_factorial((3, 4), (0, 0)), 1)
        self.assertEqual(falling_factorial((3, 4), (2, 0)), 6)
        self.assertEqual(falling_factorial((3, 4), (1, 1)), 12)

    def test_disabled_falling_factorial_and_successor(self):
        channel = Channel((2,), (1,), Fraction(1))
        self.assertEqual(falling_factorial((1,), channel.source), 0)
        with self.assertRaises(ValueError):
            Network(("A",), (channel,)).successor((1,), channel)

    def test_parallel_and_same_displacement_channels(self):
        network = Network(
            ("A", "B"),
            (
                Channel((0, 0), (1, 0), Fraction(2), "a"),
                Channel((0, 0), (1, 0), Fraction(3), "b"),
                Channel((1, 0), (0, 1), Fraction(1), "c"),
                Channel((2, 0), (1, 1), Fraction(1), "d"),
            ),
        )
        combined = network.combined_parallel()
        self.assertEqual(len(combined.channels), 3)
        self.assertTrue(
            any(channel.rate == 5 and channel.source == (0, 0) for channel in combined.channels)
        )

    def test_null_self_channel_is_removed_on_combination(self):
        network = Network(
            ("A",),
            (
                Channel((0,), (0,), Fraction(7), "null"),
                Channel((0,), (1,), Fraction(2), "birth"),
                Channel((1,), (0,), Fraction(3), "death"),
            ),
        ).combined_parallel()
        self.assertEqual(len(network.channels), 2)
        self.assertTrue(all(channel.source != channel.target for channel in network.channels))

    def test_mark_actual_channel_not_displacement(self):
        first = Channel((1, 0), (0, 1), Fraction(1), "first")
        second = Channel((2, 0), (1, 1), Fraction(1), "second")
        self.assertEqual(first.displacement, second.displacement)
        self.assertNotEqual(
            marked_successor((2, 0), first)[1],
            marked_successor((2, 0), second)[1],
        )

    def test_target_following_cycle_has_zero_increment(self):
        channels = (
            Channel((0, 0), (1, 1), Fraction(1), "trigger"),
            Channel((1, 1), (0, 1), Fraction(1), "drain"),
            Channel((0, 1), (0, 0), Fraction(1), "reset"),
        )
        for channel in channels:
            self.assertEqual(
                direct_exp_increment(channel.source, channel.source, channel),
                1,
            )

    def test_strong_connectivity(self):
        network = Network(
            ("A",),
            (
                Channel((0,), (1,), Fraction(1)),
                Channel((1,), (0,), Fraction(1)),
            ),
        )
        self.assertTrue(network.strongly_connected())


if __name__ == "__main__":
    unittest.main()
