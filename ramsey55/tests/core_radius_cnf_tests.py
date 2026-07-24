#!/usr/bin/env python3
"""Focused tests for aggregate fixed-core Hamming-radius CNFs."""

from __future__ import annotations

import itertools
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_radius_cnf import (  # noqa: E402
    build_core_radius_instance,
    validated_boundary_free_edges,
)
from direct_ramsey_cnf import (  # noqa: E402
    canonical_counter_extension,
    clause_is_satisfied,
    variable_for_edge,
)
from graph_io import read_graph  # noqa: E402


class CoreRadiusCnfTests(unittest.TestCase):
    def test_signed_difference_literals(self) -> None:
        graph = [0] * 5
        for left, right in ((0, 1), (1, 3)):
            graph[left] |= 1 << right
            graph[right] |= 1 << left
        free = {(0, 2), (3, 4)}
        instance = build_core_radius_instance(graph, free, radius=2)
        expected = []
        for left, right in itertools.combinations(range(5), 2):
            if (left, right) in free:
                continue
            variable = variable_for_edge(5, left, right)
            expected.append(
                -variable if (graph[left] >> right) & 1 else variable
            )
        self.assertEqual(instance.difference_literals, tuple(expected))

    def test_counter_accepts_exactly_assignments_in_radius(self) -> None:
        graph = [0] * 5
        graph[0] |= 1 << 1
        graph[1] |= 1 << 0
        instance = build_core_radius_instance(
            graph,
            set(itertools.combinations(range(5), 2)) - {(0, 1), (2, 3), (3, 4)},
            radius=1,
        )
        counter_clauses = tuple(instance.counter.clauses())
        for bits in itertools.product((False, True), repeat=3):
            assignment = {}
            for edge, value in zip(instance.core_edges, bits):
                assignment[variable_for_edge(5, *edge)] = value
            distance = sum(
                assignment[abs(literal)] == (literal > 0)
                for literal in instance.difference_literals
            )
            full = dict(assignment)
            full.update(
                canonical_counter_extension(instance.counter, assignment)
            )
            satisfied = all(
                clause_is_satisfied(clause, full)
                for clause in counter_clauses
            )
            self.assertEqual(satisfied, distance <= 1)

    def test_production_radius_six_counts(self) -> None:
        graph_path = (
            ROOT / "results" / "best_candidates" / "exoo_seed_20260724.g6"
        )
        graph = read_graph(graph_path)
        residual = {3, 4, 7, 38, 41, 42}
        free = {
            (left, right)
            for left, right in itertools.combinations(range(43), 2)
            if left in residual or right in residual
        }
        instance = build_core_radius_instance(graph, free, radius=6)
        self.assertEqual(len(free), 237)
        self.assertEqual(len(instance.core_edges), 666)
        self.assertEqual(instance.primary_variable_count, 903)
        self.assertEqual(instance.counter.auxiliary_count, 4_641)
        self.assertEqual(instance.counter.clause_count, 9_276)
        self.assertEqual(instance.variable_count, 5_544)
        self.assertEqual(instance.ramsey_clause_count, 1_925_196)
        self.assertEqual(instance.clause_count, 1_934_472)

    def test_empty_boundary_counts_every_graph_edge(self) -> None:
        graph_path = (
            ROOT / "results" / "best_candidates" / "core_kick_seed_20260731.g6"
        )
        graph = read_graph(graph_path)
        instance = build_core_radius_instance(graph, set(), radius=6)
        self.assertEqual(len(instance.core_edges), 903)
        self.assertEqual(len(instance.difference_literals), 903)
        self.assertEqual(instance.primary_variable_count, 903)
        self.assertEqual(instance.counter.auxiliary_count, 6_300)
        self.assertEqual(instance.counter.clause_count, 12_594)
        self.assertEqual(instance.variable_count, 7_203)
        self.assertEqual(instance.clause_count, 1_937_790)

    def test_production_boundary_metadata_fails_closed(self) -> None:
        graph_path = (
            ROOT / "results" / "best_candidates" / "exoo_seed_20260724.g6"
        )
        graph = read_graph(graph_path)
        graph_bytes = graph_path.read_bytes()
        metadata = json.loads(
            (
                ROOT
                / "certificates"
                / "residual_lns_incident_six.metadata.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            len(validated_boundary_free_edges(metadata, graph, graph_bytes)),
            237,
        )

        wrong_hash = copy.deepcopy(metadata)
        wrong_hash["base_file_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash"):
            validated_boundary_free_edges(wrong_hash, graph, graph_bytes)

        duplicate = copy.deepcopy(metadata)
        duplicate["free_edges"].append(duplicate["free_edges"][0])
        duplicate["variable_count"] += 1
        with self.assertRaisesRegex(ValueError, "duplicated|unsorted"):
            validated_boundary_free_edges(duplicate, graph, graph_bytes)

        missing = copy.deepcopy(metadata)
        missing["free_edges"].pop()
        missing["variable_count"] -= 1
        with self.assertRaisesRegex(ValueError, "exact incident"):
            validated_boundary_free_edges(missing, graph, graph_bytes)


if __name__ == "__main__":
    unittest.main()
