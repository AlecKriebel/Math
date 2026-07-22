from __future__ import annotations

from itertools import product
import unittest

from verify_variable_q_seed_quad_radius import (
    check_radius,
    quad_preserving_distances,
)


def brute_distances(first: tuple[int, ...], second: tuple[int, ...], radius: int):
    length = len(first)
    best = {}
    for flips in product((0, 1), repeat=2 * length):
        cost = sum(flips)
        if cost > radius:
            continue
        valid = True
        for left in range(length // 2):
            right = length - 1 - left
            positions = (left, right, length + left, length + right)
            if sum(flips[position] for position in positions) % 2:
                valid = False
                break
        if not valid:
            continue
        delta = [0, 0, 0, 0]
        for sequence_offset, sequence in ((0, first), (2, second)):
            for coordinate, sign in enumerate(sequence):
                position = coordinate + (length if sequence_offset else 0)
                if flips[position]:
                    delta[sequence_offset + coordinate % 2] -= sign
        key = tuple(delta)
        best[key] = min(cost, best.get(key, 10**9))
    return best


class VariableQSeedQuadRadiusTests(unittest.TestCase):
    def test_dynamic_program_matches_brute_force_even_length(self) -> None:
        first = (1, -1, 1, 1)
        second = (-1, -1, 1, -1)
        self.assertEqual(
            quad_preserving_distances(first, second, 8),
            brute_distances(first, second, 8),
        )

    def test_dynamic_program_matches_brute_force_odd_length(self) -> None:
        first = (1, -1, -1)
        second = (-1, 1, -1)
        self.assertEqual(
            quad_preserving_distances(first, second, 6),
            brute_distances(first, second, 6),
        )

    def test_radius_thirteen_is_excluded(self) -> None:
        result = check_radius(13)
        self.assertTrue(result.excluded)
        self.assertEqual(len(result.targets), 85)

    def test_margin_plus_quad_frontier_is_fourteen(self) -> None:
        result = check_radius(14)
        self.assertFalse(result.excluded)
        survivors = tuple(
            record
            for record in result.targets
            if record.quad_distance is not None
            and record.quad_distance <= result.radius
        )
        self.assertEqual(len(survivors), 18)
        self.assertEqual({record.shard for record in survivors}, {0, 6, 24})
        self.assertTrue(
            all(
                record.margin_distance == 14 and record.quad_distance == 14
                for record in survivors
            )
        )


if __name__ == "__main__":
    unittest.main()
