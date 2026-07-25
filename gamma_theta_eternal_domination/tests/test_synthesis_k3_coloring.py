from __future__ import annotations

import sys
import unittest
from itertools import combinations
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from synthesis_k3.coloring import find_coloring  # noqa: E402


def brute_force_three_colorable(
    order: int, edges: tuple[tuple[int, int], ...]
) -> bool:
    edge_set = {tuple(sorted(edge)) for edge in edges}
    for encoded in range(3**order):
        value = encoded
        colors = []
        for _ in range(order):
            colors.append(value % 3)
            value //= 3
        if all(colors[first] != colors[second] for first, second in edge_set):
            return True
    return False


class ExactColoringTests(unittest.TestCase):
    def test_known_graphs(self) -> None:
        k4 = tuple(combinations(range(4), 2))
        self.assertIsNone(find_coloring(4, k4))
        c5 = tuple((vertex, (vertex + 1) % 5) for vertex in range(5))
        coloring = find_coloring(5, c5)
        self.assertIsNotNone(coloring)
        assert coloring is not None
        self.assertTrue(all(coloring[a] != coloring[b] for a, b in c5))

    def test_every_labeled_graph_through_order_four(self) -> None:
        for order in range(5):
            pairs = tuple(combinations(range(order), 2))
            for mask in range(1 << len(pairs)):
                edges = tuple(
                    pair
                    for index, pair in enumerate(pairs)
                    if mask >> index & 1
                )
                expected = brute_force_three_colorable(order, edges)
                actual = find_coloring(order, edges)
                self.assertEqual(actual is not None, expected)

    def test_malformed_inputs(self) -> None:
        with self.assertRaises(ValueError):
            find_coloring(-1, ())
        with self.assertRaises(ValueError):
            find_coloring(3, ((0, 0),))
        with self.assertRaises(ValueError):
            find_coloring(3, ((0, 3),))
        with self.assertRaises(ValueError):
            find_coloring(3, ((0, 1), (1, 0)))


if __name__ == "__main__":
    unittest.main()
