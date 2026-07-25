from __future__ import annotations

from itertools import combinations, permutations
import random
import sys
import unittest
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from coverage_checker.graph import Graph  # noqa: E402
from evaluation_checker.math_core import (  # noqa: E402
    configuration_from_mask,
    deserialize_deletion_rounds,
    failed_dominating_pair_witnesses,
    first_dominating_set,
    first_independent_set,
    greatest_fixed_point,
    is_dominating,
    is_independent,
    mask_of,
    nonindependent_subset_witnesses,
    serialize_deletion_rounds,
    verify_empty_fixed_point_trace,
)


def cycle(order: int) -> Graph:
    return Graph.from_edges(
        order, ((vertex, (vertex + 1) % order) for vertex in range(order))
    )


def complete(order: int) -> Graph:
    return Graph.from_edges(order, combinations(range(order), 2))


def complement(graph: Graph) -> Graph:
    return Graph.from_edges(
        graph.order,
        (
            (first, second)
            for first, second in combinations(range(graph.order), 2)
            if not graph.has_edge(first, second)
        ),
    )


def integer_oracle(graph: Graph, guard_count: int) -> bool:
    """Separate integer-mask fixed point used only for differential tests."""

    full = (1 << graph.order) - 1

    def dominates(mask: int) -> bool:
        covered = mask
        for vertex in range(graph.order):
            if mask & (1 << vertex):
                covered |= graph.neighbors[vertex]
        return covered == full

    active = {
        sum(1 << vertex for vertex in subset)
        for subset in combinations(range(graph.order), guard_count)
        if dominates(sum(1 << vertex for vertex in subset))
    }
    while True:
        doomed: set[int] = set()
        for state in active:
            for attack in range(graph.order):
                if state & (1 << attack):
                    continue
                if not any(
                    graph.has_edge(guard, attack)
                    and ((state ^ (1 << guard)) | (1 << attack)) in active
                    for guard in range(graph.order)
                    if state & (1 << guard)
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return bool(active)
        active.difference_update(doomed)


def all_guards_move_mutant(graph: Graph, guard_count: int) -> bool:
    """Wrong all-guards-may-move game, for a regression trap."""

    configurations = tuple(
        frozenset(subset)
        for subset in combinations(range(graph.order), guard_count)
        if is_dominating(graph, subset)
    )
    active = set(configurations)

    def can_route(old: frozenset[int], new: frozenset[int]) -> bool:
        for targets in permutations(new):
            if all(
                source == target or graph.has_edge(source, target)
                for source, target in zip(sorted(old), targets, strict=True)
            ):
                return True
        return False

    while True:
        doomed = set()
        for state in active:
            for attack in set(range(graph.order)) - state:
                if not any(
                    attack in successor
                    and can_route(state, successor)
                    for successor in active
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return bool(active)
        active.difference_update(doomed)


def missing_domination_mutant(
    graph: Graph, guard_count: int
) -> tuple[bool, int]:
    active = {
        frozenset(subset)
        for subset in combinations(range(graph.order), guard_count)
    }
    initial_count = len(active)
    while True:
        doomed = set()
        for state in active:
            for attack in set(range(graph.order)) - state:
                if not any(
                    graph.has_edge(guard, attack)
                    and frozenset((state - {guard}) | {attack}) in active
                    for guard in state
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return bool(active), initial_count
        active.difference_update(doomed)


class StaticPredicateTests(unittest.TestCase):
    def test_named_witnesses_and_exhaustive_negative_scans(self) -> None:
        path_four = Graph.from_edges(4, ((0, 1), (1, 2), (2, 3)))
        self.assertTrue(is_dominating(path_four, (1, 2)))
        self.assertFalse(is_dominating(path_four, (0,)))
        self.assertTrue(is_independent(path_four, (0, 2)))
        self.assertFalse(is_independent(path_four, (1, 2)))
        self.assertEqual(mask_of((0, 2)), 0b0101)
        self.assertEqual(
            configuration_from_mask(path_four, 0b0101),
            frozenset((0, 2)),
        )

        c5 = cycle(5)
        self.assertIsNone(first_dominating_set(c5, 1, 1))
        self.assertIsNotNone(first_dominating_set(c5, 2, 2))
        self.assertIsNotNone(first_independent_set(c5, 2))
        self.assertIsNone(first_independent_set(c5, 3))
        pair_failures = failed_dominating_pair_witnesses(cycle(7))
        self.assertIsNotNone(pair_failures)
        self.assertEqual(len(pair_failures or ()), 21)
        self.assertIsNotNone(nonindependent_subset_witnesses(c5, 3))
        self.assertIsNone(nonindependent_subset_witnesses(c5, 2))


class OneGuardFixedPointTests(unittest.TestCase):
    def test_c5_empty_two_guard_trace_round_trip(self) -> None:
        graph = cycle(5)
        result = greatest_fixed_point(graph, 2)
        self.assertFalse(result.family)
        self.assertGreater(result.initial_count, 0)
        self.assertTrue(
            verify_empty_fixed_point_trace(
                graph,
                2,
                result.deletion_rounds,
                result.trace_sha256,
            )
        )
        payload = serialize_deletion_rounds(result.deletion_rounds)
        decoded = deserialize_deletion_rounds(graph, payload)
        self.assertEqual(decoded, result.deletion_rounds)
        self.assertTrue(
            verify_empty_fixed_point_trace(
                graph, 2, decoded, result.trace_sha256
            )
        )

    def test_tampered_trace_fails_closed(self) -> None:
        graph = cycle(5)
        result = greatest_fixed_point(graph, 2)
        payload = serialize_deletion_rounds(result.deletion_rounds)
        payload[0][0][1] = next(
            iter(configuration_from_mask(graph, payload[0][0][0]))
        )
        decoded = deserialize_deletion_rounds(graph, payload)
        self.assertFalse(
            verify_empty_fixed_point_trace(graph, 2, decoded)
        )
        self.assertFalse(
            verify_empty_fixed_point_trace(
                graph, 2, result.deletion_rounds, "0" * 64
            )
        )
        self.assertFalse(
            verify_empty_fixed_point_trace(graph, 2, (((),),))  # type: ignore[arg-type]
        )

    def test_nonempty_named_families(self) -> None:
        self.assertTrue(greatest_fixed_point(complete(5), 1).family)
        self.assertTrue(greatest_fixed_point(cycle(5), 3).family)

    def test_integer_mask_differential_all_graphs_through_order_four(self) -> None:
        for order in range(1, 5):
            edges = tuple(combinations(range(order), 2))
            for edge_mask in range(1 << len(edges)):
                graph = Graph.from_edges(
                    order,
                    (
                        edge
                        for index, edge in enumerate(edges)
                        if edge_mask & (1 << index)
                    ),
                )
                for guard_count in range(1, order + 1):
                    with self.subTest(
                        graph=graph.to_graph6(), k=guard_count
                    ):
                        self.assertEqual(
                            bool(
                                greatest_fixed_point(
                                    graph, guard_count
                                ).family
                            ),
                            integer_oracle(graph, guard_count),
                        )

    def test_random_order_five_differential(self) -> None:
        randomizer = random.Random(20260725)
        possible = tuple(combinations(range(5), 2))
        for _ in range(100):
            graph = Graph.from_edges(
                5,
                (
                    edge
                    for edge in possible
                    if randomizer.randrange(2)
                ),
            )
            for guard_count in range(1, 6):
                self.assertEqual(
                    bool(greatest_fixed_point(graph, guard_count).family),
                    integer_oracle(graph, guard_count),
                )


class ModelMutationTraps(unittest.TestCase):
    def test_all_guards_move_mutant_is_detected(self) -> None:
        graph = cycle(5)
        self.assertFalse(greatest_fixed_point(graph, 2).family)
        self.assertTrue(all_guards_move_mutant(graph, 2))

    def test_missing_domination_mutant_is_detected(self) -> None:
        graph = cycle(5)
        correct = greatest_fixed_point(graph, 2)
        mutant_result, mutant_initial_count = missing_domination_mutant(
            graph, 2
        )
        self.assertFalse(correct.family)
        # Closure eventually deletes the mutant's nondominating states too:
        # every surviving state must already have a neighboring guard for
        # every unoccupied attack, hence must dominate.  The independent
        # integrity check is therefore on the initial configuration universe.
        self.assertFalse(mutant_result)
        self.assertEqual(correct.initial_count, 5)
        self.assertEqual(mutant_initial_count, 10)

    def test_occupied_attack_and_complement_confusion_are_detected(self) -> None:
        graph = complete(4)
        correct = greatest_fixed_point(graph, 1)
        self.assertTrue(correct.family)
        # A mutant that demands an edge move to every occupied attack deletes
        # every one-guard state: the sole guard cannot traverse a loop.
        self.assertTrue(
            all(
                not any(
                    graph.has_edge(guard, attacked)
                    for guard in state
                )
                for state in correct.family
                for attacked in state
            )
        )
        self.assertFalse(greatest_fixed_point(complement(graph), 1).family)


if __name__ == "__main__":
    unittest.main()
