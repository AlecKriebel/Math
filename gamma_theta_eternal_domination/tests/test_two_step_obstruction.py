from __future__ import annotations

from dataclasses import replace
from itertools import combinations
import sys
import unittest
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.private_obstruction import find_private_obstruction
from search.two_step_obstruction import (
    FailedFirstMove,
    FailedSecondMove,
    find_two_step_obstruction,
    is_secure_configuration,
    legal_dominating_successors,
    verify_two_step_obstruction,
)
from verifier_a.core import BitGraph, alpha, dominating_masks


def _graph_from_code(order: int, code: int) -> BitGraph:
    edges = tuple(combinations(range(order), 2))
    return BitGraph.from_edges(
        order,
        (
            edge
            for position, edge in enumerate(edges)
            if code & (1 << position)
        ),
    )


def _depth_two_oracle(graph: BitGraph) -> set[int]:
    guard_count = alpha(graph)
    level_zero = set(dominating_masks(graph, guard_count))

    def predecessor_kernel(active: set[int]) -> set[int]:
        result: set[int] = set()
        for configuration in level_zero:
            for attacked in range(graph.n):
                if configuration & (1 << attacked):
                    continue
                for guard in range(graph.n):
                    if not configuration & (1 << guard):
                        continue
                    if not graph.adj[attacked] & (1 << guard):
                        continue
                    successor = (
                        configuration ^ (1 << guard) ^ (1 << attacked)
                    )
                    if successor in active:
                        break
                else:
                    break
            else:
                result.add(configuration)
        return result

    return predecessor_kernel(predecessor_kernel(level_zero))


class TwoStepObstructionTests(unittest.TestCase):
    def test_c7_passes_one_step_but_fails_two_steps(self) -> None:
        graph = BitGraph.cycle(7)
        self.assertIsNone(find_private_obstruction(graph))
        obstruction = find_two_step_obstruction(graph)
        self.assertIsNotNone(obstruction)
        assert obstruction is not None
        self.assertTrue(obstruction.genuinely_two_step)
        self.assertTrue(verify_two_step_obstruction(graph, obstruction))

        independent = sum(1 << vertex for vertex in (0, 2, 4))
        self.assertTrue(is_secure_configuration(graph, independent))

    def test_c6_has_no_two_step_obstruction(self) -> None:
        graph = BitGraph.cycle(6)
        self.assertIsNone(find_two_step_obstruction(graph))

    def test_successor_helper_rejects_nonattacks(self) -> None:
        graph = BitGraph.cycle(7)
        configuration = sum(1 << vertex for vertex in (0, 2, 4))
        for attacked in (-1, graph.n, True, 0):
            with self.subTest(attacked=attacked):
                with self.assertRaises(ValueError):
                    tuple(
                        legal_dominating_successors(
                            graph, configuration, attacked
                        )
                    )
        with self.assertRaises(ValueError):
            tuple(legal_dominating_successors(graph, -1, 1))

    def test_finder_equals_oracle_through_order_five(self) -> None:
        for order in range(1, 6):
            edge_count = order * (order - 1) // 2
            for code in range(1 << edge_count):
                graph = _graph_from_code(order, code)
                maximum_independent = {
                    mask
                    for mask in dominating_masks(graph, alpha(graph))
                    if graph.is_independent(mask)
                }
                oracle_rejects = (
                    not maximum_independent <= _depth_two_oracle(graph)
                )
                obstruction = find_two_step_obstruction(graph)
                self.assertEqual(obstruction is not None, oracle_rejects)
                if obstruction is not None:
                    self.assertTrue(
                        verify_two_step_obstruction(graph, obstruction)
                    )

    def test_checker_rejects_tampered_two_step_records(self) -> None:
        graph = BitGraph.cycle(7)
        obstruction = find_two_step_obstruction(graph)
        self.assertIsNotNone(obstruction)
        assert obstruction is not None
        self.assertTrue(verify_two_step_obstruction(graph, obstruction))

        self.assertFalse(
            verify_two_step_obstruction(
                graph, replace(obstruction, attack=graph.n)
            )
        )
        self.assertFalse(
            verify_two_step_obstruction(
                graph,
                replace(
                    obstruction,
                    failed_first_moves=obstruction.failed_first_moves
                    + (obstruction.failed_first_moves[0],),
                ),
            )
        )

        two_step_index = next(
            index
            for index, record in enumerate(obstruction.failed_first_moves)
            if record.second_attack is not None
        )
        record = obstruction.failed_first_moves[two_step_index]
        self.assertTrue(record.second_failures)
        tampered_second = replace(
            record.second_failures[0], newly_undominated=0
        )
        tampered_record = replace(
            record,
            second_failures=(tampered_second,) + record.second_failures[1:],
        )
        records = list(obstruction.failed_first_moves)
        records[two_step_index] = tampered_record
        self.assertFalse(
            verify_two_step_obstruction(
                graph,
                replace(obstruction, failed_first_moves=tuple(records)),
            )
        )

    def test_checker_rejects_wrong_record_modes(self) -> None:
        graph = BitGraph.cycle(7)
        obstruction = find_two_step_obstruction(graph)
        self.assertIsNotNone(obstruction)
        assert obstruction is not None
        first = obstruction.failed_first_moves[0]
        malformed = FailedFirstMove(
            guard=first.guard,
            first_undominated=first.first_undominated,
            second_attack=0,
            second_failures=(FailedSecondMove(0, 0),),
        )
        self.assertFalse(
            verify_two_step_obstruction(
                graph,
                replace(
                    obstruction,
                    failed_first_moves=(malformed,)
                    + obstruction.failed_first_moves[1:],
                ),
            )
        )


if __name__ == "__main__":
    unittest.main()
