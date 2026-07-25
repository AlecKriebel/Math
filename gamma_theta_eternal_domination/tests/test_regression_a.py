from __future__ import annotations

import sys
import unittest
from itertools import combinations, permutations
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_a.core import (  # noqa: E402
    BitGraph,
    alpha,
    dominating_masks,
    domination_number,
    eternal_domination_number,
    eternal_fixed_point,
    independent_domination_number,
    theta,
)


def all_labeled_graphs(n: int):
    edges = tuple(combinations(range(n), 2))
    for code in range(1 << len(edges)):
        yield BitGraph.from_edges(
            n, (edge for position, edge in enumerate(edges) if code >> position & 1)
        )


def _all_guards_can_move(graph: BitGraph, old: int, new: int) -> bool:
    old_vertices = [v for v in range(graph.n) if old >> v & 1]
    new_vertices = [v for v in range(graph.n) if new >> v & 1]
    for destinations in permutations(new_vertices):
        if all(
            u == v or graph.adj[u] >> v & 1
            for u, v in zip(old_vertices, destinations)
        ):
            return True
    return False


def wrong_all_guards_fixed_point_exists(graph: BitGraph, k: int) -> bool:
    """Deliberate mutant: any number of guards may move on one attack."""

    active = set(dominating_masks(graph, k))
    while active:
        doomed = set()
        for configuration in active:
            for attacked in range(graph.n):
                if configuration >> attacked & 1:
                    continue
                if not any(
                    successor >> attacked & 1
                    and _all_guards_can_move(graph, configuration, successor)
                    for successor in active
                ):
                    doomed.add(configuration)
                    break
        if not doomed:
            return True
        active -= doomed
    return False


class ExhaustiveSmallRegression(unittest.TestCase):
    def test_all_labeled_graphs_through_order_five(self) -> None:
        tested = 0
        for n in range(6):
            for graph in all_labeled_graphs(n):
                tested += 1
                values = (
                    domination_number(graph),
                    independent_domination_number(graph),
                    alpha(graph),
                    eternal_domination_number(graph),
                    theta(graph),
                )
                self.assertEqual(tuple(sorted(values)), values, graph.to_graph6())
                self.assertEqual(
                    BitGraph.from_graph6(graph.to_graph6()), graph, graph.to_graph6()
                )
        self.assertEqual(tested, 1100)


class ModelMutationTraps(unittest.TestCase):
    def test_all_guards_move_mutant_is_detected_by_c5(self) -> None:
        graph = BitGraph.cycle(5)
        self.assertTrue(wrong_all_guards_fixed_point_exists(graph, 2))
        self.assertFalse(eternal_fixed_point(graph, 2).exists)
        self.assertEqual(eternal_domination_number(graph), 3)

    def test_occupied_attacks_are_absent_from_certificate(self) -> None:
        graph = BitGraph.complete(4)
        result = eternal_fixed_point(graph, 1)
        for configuration in result.family:
            attacked_vertices = {
                attack
                for (source, attack), _response in result.responses.items()
                if source == configuration
            }
            self.assertEqual(len(attacked_vertices), graph.n - 1)
            self.assertTrue(
                all(not (configuration >> attack & 1) for attack in attacked_vertices)
            )

    def test_dominating_configuration_filter_is_explicit(self) -> None:
        graph = BitGraph.path(3)
        # A mutant which begins from all singleton sets has three states; the
        # required dominating-state universe contains only the middle vertex.
        self.assertEqual(dominating_masks(graph, 1), (0b010,))

    def test_complement_confusion_is_detected_by_complete_graph(self) -> None:
        graph = BitGraph.complete(4)
        self.assertEqual(theta(graph), 1)
        # Coloring G rather than its complement would return four.
        self.assertEqual(theta(graph.complement()), 4)


if __name__ == "__main__":
    unittest.main()
