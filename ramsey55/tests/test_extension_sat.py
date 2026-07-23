#!/usr/bin/env python3
"""Brute-force semantic tests for the one-vertex-extension encoding."""

from __future__ import annotations

import itertools
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from extension_sat import (  # noqa: E402
    build_extension_instance,
    count_forbidden_base_sets,
    formula_is_satisfied,
    render_dimacs,
)
from graph_io import encode_graph6  # noqa: E402
from extension_sat_check import CheckError, TreeChecker, read_cnf, read_proof  # noqa: E402
from extension_sat_solver import DpllSolver, parse_dimacs, write_proof  # noqa: E402


def adjacency_from_edge_mask(vertex_count: int, edge_mask: int) -> list[int]:
    adjacency = [0] * vertex_count
    bit = 0
    for right in range(1, vertex_count):
        for left in range(right):
            if (edge_mask >> bit) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit += 1
    return adjacency


def independently_count_forbidden(
    adjacency: list[int], forbidden_size: int
) -> tuple[int, int]:
    cliques = 0
    independent_sets = 0
    for vertices in itertools.combinations(range(len(adjacency)), forbidden_size):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for offset, left in enumerate(vertices)
            for right in vertices[offset + 1 :]
        )
        pair_count = forbidden_size * (forbidden_size - 1) // 2
        cliques += int(edge_count == pair_count)
        independent_sets += int(edge_count == 0)
    return cliques, independent_sets


def add_vertex(adjacency: list[int], assignment: tuple[bool, ...]) -> list[int]:
    result = adjacency.copy() + [0]
    new_vertex = len(adjacency)
    for vertex, adjacent in enumerate(assignment):
        if adjacent:
            result[vertex] |= 1 << new_vertex
            result[new_vertex] |= 1 << vertex
    return result


class ExtensionEncodingTests(unittest.TestCase):
    def test_exhaustive_semantics_on_all_valid_graphs_through_five_vertices(self) -> None:
        # R(3,3)=6 makes target 3 a useful complete small-cell test.  This
        # checks every labeled valid base graph on 2..5 vertices and every
        # possible neighborhood of the added vertex.
        checked_graphs = 0
        checked_assignments = 0
        for vertex_count in range(2, 6):
            edge_count = vertex_count * (vertex_count - 1) // 2
            for edge_mask in range(1 << edge_count):
                adjacency = adjacency_from_edge_mask(vertex_count, edge_mask)
                if independently_count_forbidden(adjacency, 3) != (0, 0):
                    continue
                instance = build_extension_instance(adjacency, 3)
                checked_graphs += 1
                for assignment in itertools.product(
                    (False, True), repeat=vertex_count
                ):
                    formula_value = formula_is_satisfied(
                        instance.clauses, assignment
                    )
                    extended = add_vertex(adjacency, assignment)
                    graph_value = independently_count_forbidden(
                        extended, 3
                    ) == (0, 0)
                    self.assertEqual(
                        formula_value,
                        graph_value,
                        (vertex_count, edge_mask, assignment),
                    )
                    checked_assignments += 1
        self.assertEqual(checked_graphs, 38)
        self.assertEqual(checked_assignments, 728)

    def test_c5_extension_formula_is_unsatisfiable(self) -> None:
        adjacency = [0] * 5
        for left, right in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0)):
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
        self.assertEqual(count_forbidden_base_sets(adjacency, 3), (0, 0))
        instance = build_extension_instance(adjacency, 3)
        self.assertEqual(len(instance.clique_clauses), 5)
        self.assertEqual(len(instance.independent_clauses), 5)
        self.assertFalse(
            any(
                formula_is_satisfied(instance.clauses, assignment)
                for assignment in itertools.product((False, True), repeat=5)
            )
        )

    def test_small_unsat_tree_proof_and_tamper_rejection(self) -> None:
        adjacency = [0] * 5
        for left, right in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0)):
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
        instance = build_extension_instance(adjacency, 3)
        dimacs = render_dimacs(
            instance,
            base_graph6=encode_graph6(adjacency),
            base_file_sha256="1" * 64,
        )
        import hashlib

        cnf_hash = hashlib.sha256(dimacs.encode("ascii")).hexdigest()
        with tempfile.TemporaryDirectory() as temporary:
            cnf_path = Path(temporary) / "c5.cnf"
            proof_path = Path(temporary) / "c5.tree"
            cnf_path.write_text(dimacs, encoding="ascii")
            variables, solver_clauses = parse_dimacs(cnf_path)
            solver = DpllSolver(
                variables,
                solver_clauses,
                deadline=time.monotonic() + 1.0,
            )
            self.assertIsNone(solver.solve())
            with proof_path.open("w", encoding="ascii", newline="\n") as stream:
                write_proof(
                    stream,
                    variables,
                    cnf_hash,
                    solver.proof_records,
                )

            checked_variables, checker_clauses = read_cnf(cnf_path)
            records = read_proof(proof_path, checked_variables, cnf_hash)
            stats = TreeChecker(
                checked_variables, checker_clauses, records
            ).check()
            self.assertGreater(stats.conflict_records, 0)

            tampered = records.copy()
            unit_index = next(
                index
                for index, record in enumerate(tampered)
                if record[0] == "u"
            )
            kind, literal, reason = tampered[unit_index]
            tampered[unit_index] = (kind, -literal, reason)
            with self.assertRaises(CheckError):
                TreeChecker(
                    checked_variables, checker_clauses, tampered
                ).check()

    def test_dimacs_render_is_byte_deterministic(self) -> None:
        adjacency = adjacency_from_edge_mask(4, 0b101101)
        instance = build_extension_instance(adjacency, 3)
        keywords = {
            "base_graph6": encode_graph6(adjacency),
            "base_file_sha256": "0" * 64,
        }
        first = render_dimacs(instance, **keywords)
        second = render_dimacs(instance, **keywords)
        self.assertEqual(first.encode("ascii"), second.encode("ascii"))
        problem = next(line for line in first.splitlines() if line.startswith("p "))
        self.assertEqual(
            problem,
            f"p cnf 4 {len(instance.clauses)}",
        )


if __name__ == "__main__":
    unittest.main()
