#!/usr/bin/env python3
"""Exhaustive semantic tests for two-new-vertex core completion CNFs."""

from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_sat import (  # noqa: E402
    build_core_completion_instance,
    completed_adjacency,
    count_forbidden_sets,
    formula_is_satisfied,
    induced_core,
    render_dimacs,
    variable_for_unknown_edge,
)
from graph_io import encode_graph6  # noqa: E402


def graph_from_edge_mask(vertex_count: int, edge_mask: int) -> list[int]:
    adjacency = [0] * vertex_count
    bit_index = 0
    for right in range(1, vertex_count):
        for left in range(right):
            if (edge_mask >> bit_index) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit_index += 1
    return adjacency


def independent_forbidden_counts(
    adjacency: list[int], forbidden_size: int
) -> tuple[int, int]:
    cliques = 0
    independent_sets = 0
    required_edges = forbidden_size * (forbidden_size - 1) // 2
    for subset in itertools.combinations(range(len(adjacency)), forbidden_size):
        edges = 0
        for offset, left in enumerate(subset):
            for right in subset[offset + 1 :]:
                edges += bool(adjacency[left] & (1 << right))
        cliques += edges == required_edges
        independent_sets += edges == 0
    return cliques, independent_sets


class CoreCompletionSatTests(unittest.TestCase):
    def test_variable_bijection(self) -> None:
        for core_count in range(1, 8):
            variables = {
                variable_for_unknown_edge(core_count, core, new)
                for core in range(core_count)
                for new in (core_count, core_count + 1)
            }
            variables.add(
                variable_for_unknown_edge(
                    core_count, core_count, core_count + 1
                )
            )
            self.assertEqual(variables, set(range(1, 2 * core_count + 2)))

    def test_exhaustive_target_three_semantics(self) -> None:
        # Every valid labeled (3,3;m) core through m=5, followed by every
        # assignment to the 2m+1 unknown edges.
        checked_cores = 0
        checked_assignments = 0
        for core_count in range(1, 6):
            edge_count = core_count * (core_count - 1) // 2
            for edge_mask in range(1 << edge_count):
                core = graph_from_edge_mask(core_count, edge_mask)
                if independent_forbidden_counts(core, 3) != (0, 0):
                    continue
                instance = build_core_completion_instance(core, 3)
                checked_cores += 1
                for assignment in itertools.product(
                    (False, True), repeat=instance.variable_count
                ):
                    cnf_valid = formula_is_satisfied(
                        instance.clauses, assignment
                    )
                    graph_valid = independent_forbidden_counts(
                        completed_adjacency(core, assignment), 3
                    ) == (0, 0)
                    self.assertEqual(
                        cnf_valid,
                        graph_valid,
                        (core_count, edge_mask, assignment),
                    )
                    checked_assignments += 1
        self.assertEqual(checked_cores, 39)
        self.assertEqual(checked_assignments, 34_632)

    def test_delete_relabels_core_in_increasing_original_order(self) -> None:
        graph = graph_from_edge_mask(5, 0b1011010011)
        core, originals = induced_core(graph, 2)
        self.assertEqual(originals, (0, 1, 3, 4))
        for left, right in itertools.combinations(range(4), 2):
            self.assertEqual(
                bool(core[left] & (1 << right)),
                bool(graph[originals[left]] & (1 << originals[right])),
            )

    def test_dimacs_is_deterministic_and_has_expected_clause_widths(self) -> None:
        # C5 is a valid (3,3;5) core. With target 3, one-new clauses have
        # width two and two-new clauses have width three.
        core = [0] * 5
        for left, right in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0)):
            core[left] |= 1 << right
            core[right] |= 1 << left
        instance = build_core_completion_instance(core, 3)
        text = render_dimacs(
            instance,
            base_graph6=encode_graph6(core),
            base_file_sha256="2" * 64,
            deleted_original_vertex=5,
            core_original_vertices=tuple(range(5)),
        )
        self.assertEqual(
            text,
            render_dimacs(
                instance,
                base_graph6=encode_graph6(core),
                base_file_sha256="2" * 64,
                deleted_original_vertex=5,
                core_original_vertices=tuple(range(5)),
            ),
        )
        widths = {len(clause) for clause in instance.clauses}
        self.assertEqual(widths, {2, 3})


if __name__ == "__main__":
    unittest.main()
