from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_a.core import (  # noqa: E402
    BitGraph,
    alpha,
    domination_number,
    eternal_domination_number,
    eternal_fixed_point,
    independent_domination_number,
    theta,
    verify_eternal_result,
)


class Graph6Tests(unittest.TestCase):
    def test_round_trip_small_named_graphs(self) -> None:
        graphs = [
            BitGraph.edgeless(0),
            BitGraph.edgeless(5),
            BitGraph.complete(5),
            BitGraph.path(7),
            BitGraph.cycle(7),
        ]
        for graph in graphs:
            with self.subTest(graph=graph):
                self.assertEqual(BitGraph.from_graph6(graph.to_graph6()), graph)

    def test_known_graph6_records(self) -> None:
        self.assertEqual(BitGraph.complete(3).to_graph6(), "Bw")
        self.assertEqual(BitGraph.edgeless(3).to_graph6(), "B?")

    def test_rejects_wrong_graph6_payload_length_and_padding(self) -> None:
        for record in (
            "B",
            "B??",
            "Bw?",
            "??",
            "@?",
            "~???",
            "~~??????",
        ):
            with self.subTest(graph6=record):
                with self.assertRaises(ValueError):
                    BitGraph.from_graph6(record)
        with self.assertRaises(ValueError):
            BitGraph.from_graph6("B@")


class ExactParameterTests(unittest.TestCase):
    def assert_parameters(
        self, graph: BitGraph, expected: tuple[int, int, int, int, int]
    ) -> None:
        actual = (
            domination_number(graph),
            independent_domination_number(graph),
            alpha(graph),
            eternal_domination_number(graph),
            theta(graph),
        )
        self.assertEqual(actual, expected)

    def test_complete_graphs(self) -> None:
        for n in range(1, 8):
            self.assert_parameters(BitGraph.complete(n), (1, 1, 1, 1, 1))

    def test_edgeless_graphs(self) -> None:
        for n in range(1, 8):
            self.assert_parameters(BitGraph.edgeless(n), (n, n, n, n, n))

    def test_empty_graph(self) -> None:
        self.assert_parameters(BitGraph.edgeless(0), (0, 0, 0, 0, 0))

    def test_c5(self) -> None:
        self.assert_parameters(BitGraph.cycle(5), (2, 2, 2, 3, 3))

    def test_two_published_order_ten_near_misses(self) -> None:
        # MacGillivray--Mynhardt--Virgile (2022), Table 9.
        for record, size in (("IEhbtj{ro", 26), ("IEhbtn{ro", 27)):
            graph = BitGraph.from_graph6(record)
            with self.subTest(graph6=record):
                self.assertEqual(graph.n, 10)
                self.assertEqual(graph.size, size)
                self.assert_parameters(graph, (2, 2, 3, 3, 4))

    def test_paths(self) -> None:
        expected_gamma = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3}
        for n, gamma in expected_gamma.items():
            graph = BitGraph.path(n)
            self.assertEqual(domination_number(graph), gamma)
            self.assertLessEqual(alpha(graph), eternal_domination_number(graph))

    def test_parameter_chain_on_small_named_graphs(self) -> None:
        graphs = [
            *(BitGraph.path(n) for n in range(1, 9)),
            *(BitGraph.cycle(n) for n in range(3, 9)),
            *(BitGraph.complete(n) for n in range(1, 9)),
            *(BitGraph.edgeless(n) for n in range(1, 9)),
        ]
        for graph in graphs:
            values = (
                domination_number(graph),
                independent_domination_number(graph),
                alpha(graph),
                eternal_domination_number(graph),
                theta(graph),
            )
            with self.subTest(graph6=graph.to_graph6(), values=values):
                self.assertEqual(tuple(sorted(values)), values)

    def test_generated_eternal_certificate(self) -> None:
        for graph in (BitGraph.cycle(5), BitGraph.path(6), BitGraph.complete(5)):
            k = eternal_domination_number(graph)
            result = eternal_fixed_point(graph, k)
            self.assertTrue(verify_eternal_result(graph, result))

    def test_malformed_eternal_certificate_fails_closed(self) -> None:
        graph = BitGraph.cycle(5)
        result = eternal_fixed_point(graph, 3)
        key = next(iter(result.responses))
        _, successor = result.responses[key]

        negative_guard_responses = dict(result.responses)
        negative_guard_responses[key] = (-1, successor)
        self.assertFalse(
            verify_eternal_result(
                graph, replace(result, responses=negative_guard_responses)
            )
        )

        out_of_range_successor_responses = dict(result.responses)
        guard, _ = result.responses[key]
        out_of_range_successor_responses[key] = (guard, 1 << graph.n)
        self.assertFalse(
            verify_eternal_result(
                graph,
                replace(result, responses=out_of_range_successor_responses),
            )
        )

        extra_response = dict(result.responses)
        extra_response[(0, 0)] = (0, 0)
        self.assertFalse(
            verify_eternal_result(
                graph, replace(result, responses=extra_response)
            )
        )

    def test_occupied_vertices_are_not_attack_colors(self) -> None:
        graph = BitGraph.path(3)
        result = eternal_fixed_point(graph, 1)
        self.assertFalse(result.exists)
        # The central singleton dominates, but attacks at its two unoccupied
        # leaves force a move to a nondominating singleton.
        self.assertEqual(domination_number(graph), 1)
        self.assertEqual(eternal_domination_number(graph), 2)


if __name__ == "__main__":
    unittest.main()
