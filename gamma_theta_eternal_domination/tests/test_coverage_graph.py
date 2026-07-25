from __future__ import annotations

import itertools
import random
import sys
import unittest
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from coverage_checker.graph import (  # noqa: E402
    MAX_ORDER,
    Graph,
    add_extension,
    are_isomorphic,
    find_isomorphism,
    parse_graph6,
)


def graph_from_edge_mask(order: int, mask: int) -> Graph:
    edges: list[tuple[int, int]] = []
    position = 0
    for second in range(1, order):
        for first in range(second):
            if mask & (1 << position):
                edges.append((first, second))
            position += 1
    return Graph.from_edges(order, edges)


def brute_force_isomorphic(left: Graph, right: Graph) -> bool:
    if left.order != right.order:
        return False
    for permutation in itertools.permutations(range(left.order)):
        if left.relabel(permutation) == right:
            return True
    return False


class StrictGraph6Tests(unittest.TestCase):
    def test_known_records_and_header(self) -> None:
        triangle = Graph.from_edges(3, ((0, 1), (0, 2), (1, 2)))
        empty = Graph.from_edges(3, ())
        self.assertEqual(triangle.to_graph6(), "Bw")
        self.assertEqual(empty.to_graph6(), "B?")
        self.assertEqual(parse_graph6("Bw"), triangle)
        self.assertEqual(parse_graph6(b"Bw"), triangle)
        self.assertEqual(parse_graph6(">>graph6<<Bw"), triangle)

    def test_exhaustive_round_trip_through_order_five(self) -> None:
        for order in range(6):
            edge_count = order * (order - 1) // 2
            for mask in range(1 << edge_count):
                graph = graph_from_edge_mask(order, mask)
                with self.subTest(order=order, mask=mask):
                    record = graph.to_graph6()
                    self.assertEqual(Graph.from_graph6(record), graph)
                    self.assertEqual(Graph.from_graph6(record).to_graph6(), record)

    def test_rejects_malformed_noncanonical_and_extended_records(self) -> None:
        malformed: tuple[object, ...] = (
            "",
            b"",
            ">>graph6<<",
            "B",
            "B??",
            "Bw?",
            "Bw\n",
            " Bw",
            "Bw ",
            ":Bw",
            "&Bw",
            "~???",
            "~~??????",
            "~??Bw",  # noncanonical extended encoding of a small order
            ">>graph6<<>>graph6<<Bw",
            "\u2603",
            123,
            bytearray(b"Bw"),
        )
        for record in malformed:
            with self.subTest(record=record):
                with self.assertRaises(ValueError):
                    parse_graph6(record)  # type: ignore[arg-type]

    def test_rejects_nonzero_padding_and_orders_over_limit(self) -> None:
        # Bx has K3's three edge bits followed by padding 001.
        with self.assertRaisesRegex(ValueError, "padding"):
            parse_graph6("Bx")
        # 'L' encodes order 13 in the ordinary graph6 order form.
        with self.assertRaisesRegex(ValueError, "limit"):
            parse_graph6("L" + "?" * 13)


class GraphValidationTests(unittest.TestCase):
    def test_rejects_invalid_graph_objects_and_edges(self) -> None:
        invalid_constructors = (
            lambda: Graph(-1, ()),
            lambda: Graph(2, (0,)),
            lambda: Graph(2, [0, 0]),  # type: ignore[arg-type]
            lambda: Graph(2, (1, 0)),  # loop at vertex zero
            lambda: Graph(2, (4, 0)),  # out-of-range bit
            lambda: Graph(2, (2, 0)),  # asymmetric edge
            lambda: Graph(1, (-1,)),
            lambda: Graph(True, ()),  # type: ignore[arg-type]
            lambda: Graph(1, (False,)),  # type: ignore[arg-type]
        )
        for constructor in invalid_constructors:
            with self.assertRaises(ValueError):
                constructor()

        bad_edge_sets = (
            ((0, 0),),
            ((0, 2),),
            ((0, 1), (1, 0)),
            ((0, True),),
            ((0,),),
        )
        for edges in bad_edge_sets:
            with self.subTest(edges=edges):
                with self.assertRaises(ValueError):
                    Graph.from_edges(2, edges)  # type: ignore[arg-type]

    def test_relabel_requires_a_permutation(self) -> None:
        path = Graph.from_edges(4, ((0, 1), (1, 2), (2, 3)))
        for invalid in ((0, 1, 2), (0, 1, 2, 2), (0, 1, 2, 4)):
            with self.assertRaises(ValueError):
                path.relabel(invalid)


class ExtensionTests(unittest.TestCase):
    def test_extension_has_exact_requested_neighborhood(self) -> None:
        host = Graph.from_edges(4, ((0, 1), (1, 2), (2, 3)))
        extension = add_extension(host, 0b0101)
        self.assertEqual(host.add_extension(0b0101), extension)
        self.assertEqual(extension.order, 5)
        self.assertEqual(extension.neighbors[4], 0b0101)
        self.assertEqual(
            tuple(
                (first, second)
                for first, second in extension.edges()
                if second < 4
            ),
            tuple(host.edges()),
        )
        self.assertTrue(extension.has_edge(0, 4))
        self.assertFalse(extension.has_edge(1, 4))
        self.assertTrue(extension.has_edge(2, 4))
        self.assertFalse(extension.has_edge(3, 4))

    def test_extension_rejects_empty_out_of_range_and_order_thirteen(self) -> None:
        host = Graph.from_edges(3, ((0, 1),))
        for mask in (0, -1, 1 << 3, True):
            with self.subTest(mask=mask):
                with self.assertRaises(ValueError):
                    add_extension(host, mask)
        maximum = Graph.from_edges(MAX_ORDER, ())
        with self.assertRaises(ValueError):
            add_extension(maximum, 1)


class ExactIsomorphismTests(unittest.TestCase):
    def assert_witness(
        self, left: Graph, right: Graph, expected: bool
    ) -> None:
        mapping = find_isomorphism(left, right)
        self.assertEqual(mapping is not None, expected)
        self.assertEqual(are_isomorphic(left, right), expected)
        if mapping is not None:
            self.assertEqual(left.relabel(mapping), right)

    def test_named_isomorphic_and_nonisomorphic_regular_graphs(self) -> None:
        cycle_six = Graph.from_edges(
            6, ((vertex, (vertex + 1) % 6) for vertex in range(6))
        )
        two_triangles = Graph.from_edges(
            6,
            (
                (0, 1),
                (0, 2),
                (1, 2),
                (3, 4),
                (3, 5),
                (4, 5),
            ),
        )
        prism = Graph.from_edges(
            6,
            (
                (0, 1),
                (1, 2),
                (2, 0),
                (3, 4),
                (4, 5),
                (5, 3),
                (0, 3),
                (1, 4),
                (2, 5),
            ),
        )
        complete_bipartite = Graph.from_edges(
            6, ((left, right) for left in range(3) for right in range(3, 6))
        )
        self.assert_witness(cycle_six, two_triangles, False)
        self.assert_witness(prism, complete_bipartite, False)

        permutation = (5, 2, 4, 1, 3, 0)
        self.assert_witness(prism, prism.relabel(permutation), True)

    def test_against_brute_force_for_all_graph_pairs_through_order_four(
        self,
    ) -> None:
        for order in range(5):
            edge_count = order * (order - 1) // 2
            graphs = [
                graph_from_edge_mask(order, mask)
                for mask in range(1 << edge_count)
            ]
            for first_index, left in enumerate(graphs):
                for right in graphs[first_index:]:
                    expected = brute_force_isomorphic(left, right)
                    with self.subTest(
                        order=order,
                        left=left.to_graph6(),
                        right=right.to_graph6(),
                    ):
                        self.assertEqual(are_isomorphic(left, right), expected)

    def test_random_relabelings_and_small_brute_force_differential(self) -> None:
        randomizer = random.Random(20260725)
        for order in range(1, 7):
            edge_count = order * (order - 1) // 2
            for _ in range(20):
                left = graph_from_edge_mask(
                    order, randomizer.randrange(1 << edge_count)
                )
                permutation = list(range(order))
                randomizer.shuffle(permutation)
                self.assert_witness(left, left.relabel(permutation), True)

            for _ in range(15):
                left = graph_from_edge_mask(
                    order, randomizer.randrange(1 << edge_count)
                )
                right = graph_from_edge_mask(
                    order, randomizer.randrange(1 << edge_count)
                )
                self.assertEqual(
                    are_isomorphic(left, right),
                    brute_force_isomorphic(left, right),
                )

    def test_order_twelve_relabeling(self) -> None:
        randomizer = random.Random(12012026)
        edges = [
            (first, second)
            for second in range(1, 12)
            for first in range(second)
            if randomizer.randrange(3) == 0
        ]
        graph = Graph.from_edges(12, edges)
        permutation = list(range(12))
        randomizer.shuffle(permutation)
        self.assert_witness(graph, graph.relabel(permutation), True)


if __name__ == "__main__":
    unittest.main()
