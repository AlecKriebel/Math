#!/usr/bin/env python3
"""Semantic and adversarial tests for fixed-boundary residual CNFs."""

from __future__ import annotations

import itertools
import random
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from graph_io import read_graph  # noqa: E402
from residual_lns_sat import (  # noqa: E402
    apply_assignment,
    assignment_from_graph,
    build_residual_lns_instance,
    count_forbidden_sets,
    formula_is_satisfied,
    neighborhood_edges,
    normalize_edges,
)
from residual_lns_cnf_check import (  # noqa: E402
    free_edge_order as independent_free_edge_order,
)


class ResidualLnsTests(unittest.TestCase):
    def test_edge_normalization_and_variable_order(self) -> None:
        self.assertEqual(
            normalize_edges(6, [(4, 1), (0, 2), (1, 4)]),
            ((0, 2), (1, 4)),
        )
        with self.assertRaisesRegex(ValueError, "invalid"):
            normalize_edges(6, [(2, 2)])

    def test_exhaustive_small_semantics(self) -> None:
        # Six-cycle, with every edge among vertices 0..3 free.
        adjacency = [0] * 6
        for left, right in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)):
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
        free_edges = neighborhood_edges(6, (0, 1, 2, 3), ())
        instance = build_residual_lns_instance(
            adjacency, free_edges, forbidden_size=3
        )
        for bits in itertools.product((False, True), repeat=len(free_edges)):
            completed = apply_assignment(adjacency, free_edges, bits)
            graph_valid = count_forbidden_sets(completed, 3) == (0, 0)
            self.assertEqual(
                formula_is_satisfied(instance.clauses, bits), graph_valid
            )

    def test_exhaustive_incident_vertex_semantics(self) -> None:
        adjacency = [0] * 6
        for left, right in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)):
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
        free_edges = neighborhood_edges(
            6, (), (), incident_vertices=(0, 2)
        )
        self.assertEqual(len(free_edges), 9)
        instance = build_residual_lns_instance(
            adjacency, free_edges, forbidden_size=3
        )
        for bits in itertools.product((False, True), repeat=len(free_edges)):
            completed = apply_assignment(adjacency, free_edges, bits)
            graph_valid = count_forbidden_sets(completed, 3) == (0, 0)
            self.assertEqual(
                formula_is_satisfied(instance.clauses, bits), graph_valid
            )

    def test_incident_edge_set_and_adversarial_boundaries(self) -> None:
        edges = neighborhood_edges(
            6, (0, 5), ((2, 3),), incident_vertices=(1, 4, 1)
        )
        expected = {
            (left, right)
            for left, right in itertools.combinations(range(6), 2)
            if left in {1, 4} or right in {1, 4}
        }
        expected.update({(0, 5), (2, 3)})
        self.assertEqual(set(edges), expected)
        self.assertEqual(len(edges), 11)
        self.assertEqual(
            independent_free_edge_order(
                6, (0, 5), [(2, 3)], incident_vertices=(1, 4, 1)
            ),
            edges,
        )
        with self.assertRaisesRegex(ValueError, "outside"):
            neighborhood_edges(6, (), (), incident_vertices=(6,))
        with self.assertRaisesRegex(ValueError, "outside"):
            independent_free_edge_order(
                6, (0,), [], incident_vertices=(6,)
            )

    def test_randomized_small_semantics(self) -> None:
        rng = random.Random(20260723)
        checked = 0
        for _ in range(12):
            order = 7
            adjacency = [0] * order
            for left, right in itertools.combinations(range(order), 2):
                if rng.getrandbits(1):
                    adjacency[left] |= 1 << right
                    adjacency[right] |= 1 << left
            free_edges = normalize_edges(
                order, rng.sample(list(itertools.combinations(range(order), 2)), 7)
            )
            instance = build_residual_lns_instance(
                adjacency, free_edges, forbidden_size=4
            )
            for _ in range(64):
                assignment = tuple(
                    bool(rng.getrandbits(1)) for _ in free_edges
                )
                completed = apply_assignment(
                    adjacency, free_edges, assignment
                )
                graph_valid = count_forbidden_sets(completed, 4) == (0, 0)
                self.assertEqual(
                    formula_is_satisfied(instance.clauses, assignment),
                    graph_valid,
                )
                checked += 1
        self.assertEqual(checked, 768)

    def test_production_neighborhood_and_base_assignment(self) -> None:
        adjacency = read_graph(
            ROOT / "results" / "best_candidates" / "exoo_seed_20260724.g6"
        )
        free_edges = neighborhood_edges(
            43,
            (3, 4, 7, 38, 41, 42),
            ((10, 31), (21, 22), (30, 31), (31, 32)),
        )
        self.assertEqual(len(free_edges), 19)
        instance = build_residual_lns_instance(adjacency, free_edges)
        assignment = assignment_from_graph(adjacency, free_edges)
        self.assertFalse(formula_is_satisfied(instance.clauses, assignment))
        self.assertEqual(count_forbidden_sets(adjacency), (0, 2))

    def test_production_incident_neighborhood(self) -> None:
        residual = {3, 4, 7, 38, 41, 42}
        free_edges = neighborhood_edges(
            43, (), (), incident_vertices=tuple(residual)
        )
        self.assertEqual(len(free_edges), 237)
        self.assertTrue(
            all(
                (
                    (left in residual or right in residual)
                    == ((left, right) in free_edges)
                )
                for left, right in itertools.combinations(range(43), 2)
            )
        )


if __name__ == "__main__":
    unittest.main()
