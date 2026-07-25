from __future__ import annotations

from itertools import permutations
import random
import sys
import unittest
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from edge_toggle_coverage_checker.graph import (  # noqa: E402
    Graph,
    Graph6Error,
    find_isomorphism,
    verify_isomorphism,
)


def _brute_isomorphic(left: Graph, right: Graph) -> bool:
    return any(
        verify_isomorphism(left, right, permutation)
        for permutation in permutations(range(left.order))
    )


class EdgeToggleCoverageGraphTests(unittest.TestCase):
    def test_graph6_roundtrip_all_order_five_labeled_graphs(self) -> None:
        pairs = tuple(
            (first, second)
            for second in range(1, 5)
            for first in range(second)
        )
        for mask in range(1 << len(pairs)):
            graph = Graph.from_edges(
                5,
                (
                    pair
                    for index, pair in enumerate(pairs)
                    if mask & (1 << index)
                ),
            )
            encoded = graph.to_graph6()
            self.assertEqual(Graph.from_graph6(encoded), graph)
            self.assertEqual(Graph.from_graph6(b">>graph6<<" + encoded.encode()), graph)

    def test_strict_graph6_rejects_malformed_records(self) -> None:
        for record in ("", "~??", "D?", "Dzz", "D~|"):
            with self.subTest(record=record):
                with self.assertRaises((Graph6Error, ValueError)):
                    Graph.from_graph6(record)
        graph = Graph.from_edges(5, ((0, 1),))
        encoded = graph.to_graph6()
        malformed_padding = encoded[:-1] + chr(ord(encoded[-1]) + 1)
        with self.assertRaises(Graph6Error):
            Graph.from_graph6(malformed_padding)

    def test_every_pair_toggle_is_involutive(self) -> None:
        graph = Graph.from_edges(
            7, ((0, 1), (1, 2), (2, 3), (4, 5), (5, 6))
        )
        for second in range(1, graph.order):
            for first in range(second):
                toggled = graph.toggled(first, second)
                self.assertNotEqual(
                    graph.has_edge(first, second),
                    toggled.has_edge(first, second),
                )
                self.assertEqual(toggled.toggled(first, second), graph)

    def test_exact_isomorphism_witnesses_relabelings(self) -> None:
        randomizer = random.Random(0xE7A9)
        for order in range(1, 9):
            for _ in range(30):
                graph = Graph.from_edges(
                    order,
                    (
                        (first, second)
                        for second in range(1, order)
                        for first in range(second)
                        if randomizer.randrange(2)
                    ),
                )
                permutation = list(range(order))
                randomizer.shuffle(permutation)
                relabeled = graph.relabeled(permutation)
                witness = find_isomorphism(graph, relabeled)
                self.assertIsNotNone(witness)
                assert witness is not None
                self.assertTrue(verify_isomorphism(graph, relabeled, witness))

    def test_isomorphism_decision_agrees_with_bruteforce_order_five(self) -> None:
        randomizer = random.Random(314159)
        pairs = tuple(
            (first, second)
            for second in range(1, 5)
            for first in range(second)
        )
        graphs = [
            Graph.from_edges(
                5,
                (
                    pair
                    for index, pair in enumerate(pairs)
                    if mask & (1 << index)
                ),
            )
            for mask in (randomizer.randrange(1 << 10) for _ in range(80))
        ]
        for left, right in zip(graphs[::2], graphs[1::2], strict=True):
            found = find_isomorphism(left, right)
            brute = _brute_isomorphic(left, right)
            self.assertEqual(found is not None, brute)
            if found is not None:
                self.assertTrue(verify_isomorphism(left, right, found))

    def test_same_degree_nonisomorphic_graphs_are_rejected(self) -> None:
        cycle_six = Graph.from_edges(
            6, ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0))
        )
        two_triangles = Graph.from_edges(
            6, ((0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3))
        )
        self.assertEqual(sorted(cycle_six.degrees), sorted(two_triangles.degrees))
        self.assertIsNone(find_isomorphism(cycle_six, two_triangles))


if __name__ == "__main__":
    unittest.main()
