from __future__ import annotations

from itertools import combinations
import random
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from coverage_checker.graph import Graph  # noqa: E402
from edge_toggle_evaluation_checker.math_core import (  # noqa: E402
    build_domination_proof,
    build_fixed_point_proof,
    deserialize_blockers,
    deserialize_rounds,
    dominating_configurations,
    serialize_blockers,
    serialize_rounds,
    verify_complete_empty_trace,
    verify_domination_proof,
)


def cycle(order: int) -> Graph:
    return Graph.from_edges(
        order, ((vertex, (vertex + 1) % order) for vertex in range(order))
    )


def graph_from_edge_mask(order: int, edge_mask: int) -> Graph:
    possible = tuple(combinations(range(order), 2))
    return Graph.from_edges(
        order,
        (
            edge
            for index, edge in enumerate(possible)
            if edge_mask & (1 << index)
        ),
    )


def frozenset_oracle(graph: Graph, guard_count: int) -> bool:
    def dominates(state: frozenset[int]) -> bool:
        return all(
            vertex in state
            or any(graph.has_edge(vertex, guard) for guard in state)
            for vertex in range(graph.order)
        )

    active = {
        frozenset(state)
        for state in combinations(range(graph.order), guard_count)
        if dominates(frozenset(state))
    }
    while active:
        doomed: set[frozenset[int]] = set()
        for state in active:
            for attacked in set(range(graph.order)) - state:
                if not any(
                    frozenset((state - {guard}) | {attacked}) in active
                    and graph.has_edge(guard, attacked)
                    and dominates(
                        frozenset((state - {guard}) | {attacked})
                    )
                    for guard in state
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return True
        active.difference_update(doomed)
    return False


class DominationProofTests(unittest.TestCase):
    def test_explicit_exhaustive_proofs_for_c5_and_c7(self) -> None:
        for graph, expected in ((cycle(5), 2), (cycle(7), 3)):
            proof = build_domination_proof(graph)
            self.assertEqual(proof.gamma, expected)
            self.assertTrue(
                verify_domination_proof(
                    graph,
                    proof.gamma,
                    proof.dominating_witness_mask,
                    proof.lower_blockers,
                )
            )
            self.assertEqual(
                len(proof.lower_blockers),
                len(tuple(combinations(range(graph.order), expected - 1))),
            )
            payload = serialize_blockers(proof.lower_blockers)
            self.assertEqual(
                deserialize_blockers(payload), proof.lower_blockers
            )

    def test_domination_tampering_fails(self) -> None:
        graph = cycle(7)
        proof = build_domination_proof(graph)
        blockers = list(proof.lower_blockers)
        blockers[0] = (blockers[0][0], next(iter(range(graph.order))))
        self.assertFalse(
            verify_domination_proof(
                graph,
                proof.gamma,
                proof.dominating_witness_mask,
                tuple(blockers),
            )
        )
        self.assertFalse(
            verify_domination_proof(
                graph,
                proof.gamma,
                proof.dominating_witness_mask,
                proof.lower_blockers[:-1],
            )
        )

    def test_gamma_outside_target_fails_closed(self) -> None:
        complete = Graph.from_edges(4, combinations(range(4), 2))
        with self.assertRaisesRegex(ValueError, "two or three"):
            build_domination_proof(complete)


class FixedPointTraceTests(unittest.TestCase):
    def test_empty_traces_round_trip(self) -> None:
        for graph, guard_count in ((cycle(5), 2), (cycle(7), 3)):
            proof = build_fixed_point_proof(graph, guard_count)
            self.assertFalse(proof.surviving_configurations)
            self.assertGreater(proof.initial_count, 0)
            self.assertEqual(
                sum(len(round_) for round_ in proof.deletion_rounds),
                proof.initial_count,
            )
            payload = serialize_rounds(proof.deletion_rounds)
            decoded = deserialize_rounds(payload)
            self.assertEqual(decoded, proof.deletion_rounds)
            self.assertTrue(
                verify_complete_empty_trace(
                    graph,
                    guard_count,
                    decoded,
                    proof.trace_sha256,
                    proof.initial_count,
                )
            )

    def test_nonempty_fixed_point_is_not_an_empty_certificate(self) -> None:
        graph = cycle(5)
        proof = build_fixed_point_proof(graph, 3)
        self.assertTrue(proof.surviving_configurations)
        self.assertFalse(
            verify_complete_empty_trace(
                graph,
                3,
                proof.deletion_rounds,
                proof.trace_sha256,
                proof.initial_count,
            )
        )

    def test_tampered_incomplete_and_occupied_attack_traces_fail(self) -> None:
        graph = cycle(5)
        proof = build_fixed_point_proof(graph, 2)
        rounds = [list(round_) for round_ in proof.deletion_rounds]
        rounds[0] = rounds[0][1:]
        self.assertFalse(
            verify_complete_empty_trace(
                graph,
                2,
                tuple(tuple(round_) for round_ in rounds),
                proof.trace_sha256,
                proof.initial_count,
            )
        )
        occupied = [list(round_) for round_ in proof.deletion_rounds]
        state, _attack = occupied[0][0]
        occupied[0][0] = (state, (state & -state).bit_length() - 1)
        occupied_tuple = tuple(tuple(round_) for round_ in occupied)
        self.assertFalse(
            verify_complete_empty_trace(
                graph,
                2,
                occupied_tuple,
                proof.trace_sha256,
                proof.initial_count,
            )
        )
        self.assertFalse(
            verify_complete_empty_trace(
                graph,
                2,
                proof.deletion_rounds,
                "0" * 64,
                proof.initial_count,
            )
        )

    def test_frozenset_differential_all_graphs_through_order_four(self) -> None:
        for order in range(1, 5):
            edge_count = order * (order - 1) // 2
            for edge_mask in range(1 << edge_count):
                graph = graph_from_edge_mask(order, edge_mask)
                for guard_count in range(1, order + 1):
                    proof = build_fixed_point_proof(graph, guard_count)
                    with self.subTest(
                        order=order,
                        edge_mask=edge_mask,
                        guard_count=guard_count,
                    ):
                        self.assertEqual(
                            bool(proof.surviving_configurations),
                            frozenset_oracle(graph, guard_count),
                        )

    def test_random_order_six_differential(self) -> None:
        randomizer = random.Random(20260725)
        for _ in range(50):
            graph = graph_from_edge_mask(
                6, randomizer.randrange(1 << 15)
            )
            for guard_count in (2, 3):
                self.assertEqual(
                    bool(
                        build_fixed_point_proof(
                            graph, guard_count
                        ).surviving_configurations
                    ),
                    frozenset_oracle(graph, guard_count),
                )

    def test_initial_family_contains_only_dominating_ordinary_sets(self) -> None:
        graph = cycle(7)
        configurations = dominating_configurations(graph, 3)
        self.assertTrue(configurations)
        self.assertTrue(all(mask.bit_count() == 3 for mask in configurations))


if __name__ == "__main__":
    unittest.main()
