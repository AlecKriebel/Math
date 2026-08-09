import unittest
from fractions import Fraction

from bimolecular_pr.episode_bounds import (
    episode_continuation_probability,
    scalar_envelope_branch,
    target_following_path_probability,
)
from bimolecular_pr.network import Channel, Network
from bimolecular_pr.target_augmented import (
    entropy_rewrite_signature,
    expected_increment_signature,
)


class EpisodeTests(unittest.TestCase):
    def test_scalar_envelope_all_branches_and_boundary(self):
        boundary = scalar_envelope_branch(Fraction(1, 2), Fraction(-2))
        self.assertEqual(boundary.branch, "endpoint")
        self.assertEqual(boundary.maximizer, 1)
        interior = scalar_envelope_branch(Fraction(1, 2), Fraction(-3))
        self.assertEqual(interior.branch, "interior")
        self.assertEqual(interior.maximizer, Fraction(2, 3))

    def test_target_following_path_probability(self):
        phases = [
            (Fraction(1, 3), Fraction(1, 2)),
            (Fraction(3, 5), Fraction(2, 7)),
        ]
        self.assertEqual(target_following_path_probability(phases), Fraction(1, 35))

    def test_zero_length_path_probability(self):
        self.assertEqual(target_following_path_probability([]), 1)

    def test_invalid_episode_probability_is_rejected(self):
        with self.assertRaises(ValueError):
            episode_continuation_probability(Fraction(4, 3), Fraction(1, 2))
        with self.assertRaises(ValueError):
            episode_continuation_probability(Fraction(1, 3), Fraction(0))

    def test_exact_entropy_identity_with_zero_source(self):
        network = Network(
            ("A",),
            (
                Channel((0,), (1,), Fraction(2), "immigration"),
                Channel((1,), (0,), Fraction(3), "death"),
            ),
        )
        state = (2,)
        for target in ((0,), (1,)):
            self.assertEqual(
                expected_increment_signature(network, state, target),
                entropy_rewrite_signature(network, state, target),
            )

    def test_entropy_identity_aggregates_parallel_source_rates(self):
        network = Network(
            ("A",),
            (
                Channel((0,), (1,), Fraction(2, 3), "first"),
                Channel((0,), (1,), Fraction(5, 7), "parallel"),
                Channel((1,), (0,), Fraction(11, 5), "return"),
            ),
        )
        state = (3,)
        for target in ((0,), (1,)):
            self.assertEqual(
                expected_increment_signature(network, state, target),
                entropy_rewrite_signature(network, state, target),
            )


if __name__ == "__main__":
    unittest.main()
