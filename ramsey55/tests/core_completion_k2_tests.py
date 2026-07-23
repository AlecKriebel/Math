#!/usr/bin/env python3
"""Independent semantic tests for three-new-vertex completion CNFs."""

from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_k2_sat import (  # noqa: E402
    build_core_completion_k2_instance,
    completed_adjacency,
    formula_is_satisfied,
    induced_core,
    render_dimacs,
    variable_for_unknown_edge,
)
from graph_io import encode_graph6  # noqa: E402


def graph_from_mask(order: int, mask: int) -> list[int]:
    adjacency = [0] * order
    index = 0
    for right in range(1, order):
        for left in range(right):
            if (mask >> index) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            index += 1
    return adjacency


def direct_forbidden_counts(
    adjacency: list[int], forbidden_size: int
) -> tuple[int, int]:
    cliques = independent_sets = 0
    required = forbidden_size * (forbidden_size - 1) // 2
    for vertices in itertools.combinations(range(len(adjacency)), forbidden_size):
        edges = 0
        for offset, left in enumerate(vertices):
            for right in vertices[offset + 1 :]:
                edges += bool(adjacency[left] & (1 << right))
        cliques += edges == required
        independent_sets += edges == 0
    return cliques, independent_sets


class CoreCompletionK2Tests(unittest.TestCase):
    def test_variable_mapping_is_a_bijection(self) -> None:
        for core_count in range(0, 7):
            variables = {
                variable_for_unknown_edge(core_count, 3, left, right)
                for left, right in itertools.combinations(
                    range(core_count + 3), 2
                )
                if right >= core_count
            }
            expected_count = 3 * core_count + 3
            self.assertEqual(variables, set(range(1, expected_count + 1)))

    def test_exhaustive_target_three_semantics(self) -> None:
        checked_cores = 0
        checked_assignments = 0
        for core_count in range(0, 4):
            fixed_edges = core_count * (core_count - 1) // 2
            for core_mask in range(1 << fixed_edges):
                core = graph_from_mask(core_count, core_mask)
                if direct_forbidden_counts(core, 3) != (0, 0):
                    continue
                instance = build_core_completion_k2_instance(
                    core, forbidden_size=3
                )
                checked_cores += 1
                for assignment in itertools.product(
                    (False, True), repeat=instance.variable_count
                ):
                    cnf_value = formula_is_satisfied(
                        instance.clauses, assignment
                    )
                    graph_value = direct_forbidden_counts(
                        completed_adjacency(core, assignment), 3
                    ) == (0, 0)
                    self.assertEqual(
                        cnf_value,
                        graph_value,
                        (core_count, core_mask, assignment),
                    )
                    checked_assignments += 1
        self.assertEqual(checked_cores, 10)
        self.assertEqual(checked_assignments, 25_672)

    def test_three_new_plus_core_pair_target_five(self) -> None:
        for core_mask in (0, 1):
            core = graph_from_mask(2, core_mask)
            instance = build_core_completion_k2_instance(core, 5)
            self.assertEqual(instance.variable_count, 9)
            self.assertEqual(len(instance.clauses), 1)
            self.assertEqual(len(instance.clauses[0]), 9)
            for assignment in itertools.product((False, True), repeat=9):
                self.assertEqual(
                    formula_is_satisfied(instance.clauses, assignment),
                    direct_forbidden_counts(
                        completed_adjacency(core, assignment), 5
                    )
                    == (0, 0),
                )

    def test_two_vertex_deletion_and_deterministic_dimacs(self) -> None:
        graph = graph_from_mask(6, 0b101101001101011)
        core, originals = induced_core(graph, (4, 1))
        self.assertEqual(originals, (0, 2, 3, 5))
        instance = build_core_completion_k2_instance(core, 4)
        keywords = {
            "base_graph6": encode_graph6(graph),
            "base_file_sha256": "3" * 64,
            "deleted_original_vertices": (1, 4),
            "core_original_vertices": originals,
        }
        first = render_dimacs(instance, **keywords)
        second = render_dimacs(instance, **keywords)
        self.assertEqual(first.encode("ascii"), second.encode("ascii"))


if __name__ == "__main__":
    unittest.main()
