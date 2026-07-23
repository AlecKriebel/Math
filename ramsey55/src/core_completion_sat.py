#!/usr/bin/env python3
"""Deterministic CNF for a fixed core completed by exactly two new vertices.

The primary use is the k=1 replacement experiment: delete one vertex from a
verified 42-vertex (5,5)-graph, retain the induced 41-vertex core, and solve
for all 83 edges incident to two new vertices.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import (  # noqa: E402
    encode_graph6,
    read_graph,
    validate_simple,
    write_canonical_artifact,
)


GENERATOR_ID = "ramsey55_two_vertex_core_completion_cnf_v1"


@dataclass(frozen=True)
class CoreCompletionInstance:
    core_vertex_count: int
    forbidden_size: int
    clique_clauses: tuple[tuple[int, ...], ...]
    independent_clauses: tuple[tuple[int, ...], ...]
    one_new_clique_count: int
    one_new_independent_count: int
    two_new_clique_count: int
    two_new_independent_count: int

    @property
    def variable_count(self) -> int:
        return 2 * self.core_vertex_count + 1

    @property
    def clauses(self) -> tuple[tuple[int, ...], ...]:
        return self.clique_clauses + self.independent_clauses


def induced_core(
    adjacency: list[int], deleted_vertex: int
) -> tuple[list[int], tuple[int, ...]]:
    """Delete one original vertex and relabel the retained core increasingly."""
    validate_simple(adjacency)
    if not 0 <= deleted_vertex < len(adjacency):
        raise ValueError("deleted vertex is outside the base graph")
    original_vertices = tuple(
        vertex for vertex in range(len(adjacency)) if vertex != deleted_vertex
    )
    core = [0] * len(original_vertices)
    for new_left, old_left in enumerate(original_vertices):
        for new_right in range(new_left + 1, len(original_vertices)):
            old_right = original_vertices[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                core[new_left] |= 1 << new_right
                core[new_right] |= 1 << new_left
    validate_simple(core)
    return core, original_vertices


def variable_for_unknown_edge(
    core_vertex_count: int, left: int, right: int
) -> int:
    """Return the one-based variable for an edge involving a new vertex."""
    if left > right:
        left, right = right, left
    new_a = core_vertex_count
    new_b = core_vertex_count + 1
    if 0 <= left < core_vertex_count and right == new_a:
        return left + 1
    if 0 <= left < core_vertex_count and right == new_b:
        return core_vertex_count + left + 1
    if left == new_a and right == new_b:
        return 2 * core_vertex_count + 1
    raise ValueError(f"edge ({left},{right}) is fixed or outside the completion")


def _unknown_variables_on_subset(
    core_vertex_count: int, vertices: Sequence[int]
) -> tuple[int, ...]:
    result = []
    for left, right in itertools.combinations(vertices, 2):
        if right >= core_vertex_count:
            result.append(
                variable_for_unknown_edge(core_vertex_count, left, right)
            )
    return tuple(result)


def _fixed_core_pair_flags(
    core: Sequence[int], core_vertices: Sequence[int]
) -> tuple[bool, bool]:
    """Return whether all fixed pairs are edges and whether all are nonedges."""
    all_edges = True
    all_nonedges = True
    for left, right in itertools.combinations(core_vertices, 2):
        if (core[left] >> right) & 1:
            all_nonedges = False
        else:
            all_edges = False
    return all_edges, all_nonedges


def count_forbidden_sets(
    adjacency: Sequence[int], forbidden_size: int
) -> tuple[int, int]:
    cliques = 0
    independent_sets = 0
    pair_count = forbidden_size * (forbidden_size - 1) // 2
    for vertices in itertools.combinations(range(len(adjacency)), forbidden_size):
        edges = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        cliques += int(edges == pair_count)
        independent_sets += int(edges == 0)
    return cliques, independent_sets


def build_core_completion_instance(
    core: list[int], forbidden_size: int = 5
) -> CoreCompletionInstance:
    """Encode all forbidden sets containing at least one of two new vertices."""
    validate_simple(core)
    if forbidden_size < 3:
        raise ValueError("forbidden_size must be at least 3")
    core_count = len(core)
    new_vertices = (core_count, core_count + 1)
    clique_by_new_count: list[list[tuple[int, ...]]] = [[], [], []]
    independent_by_new_count: list[list[tuple[int, ...]]] = [[], [], []]

    for new_count in (1, 2):
        core_subset_size = forbidden_size - new_count
        if core_subset_size < 0 or core_subset_size > core_count:
            continue
        for selected_new in itertools.combinations(new_vertices, new_count):
            for selected_core in itertools.combinations(
                range(core_count), core_subset_size
            ):
                all_edges, all_nonedges = _fixed_core_pair_flags(
                    core, selected_core
                )
                selected = tuple(selected_core) + tuple(selected_new)
                variables = _unknown_variables_on_subset(core_count, selected)
                if all_edges:
                    clique_by_new_count[new_count].append(
                        tuple(-variable for variable in variables)
                    )
                if all_nonedges:
                    independent_by_new_count[new_count].append(variables)

    clique_clauses = tuple(
        clique_by_new_count[1] + clique_by_new_count[2]
    )
    independent_clauses = tuple(
        independent_by_new_count[1] + independent_by_new_count[2]
    )
    return CoreCompletionInstance(
        core_vertex_count=core_count,
        forbidden_size=forbidden_size,
        clique_clauses=clique_clauses,
        independent_clauses=independent_clauses,
        one_new_clique_count=len(clique_by_new_count[1]),
        one_new_independent_count=len(independent_by_new_count[1]),
        two_new_clique_count=len(clique_by_new_count[2]),
        two_new_independent_count=len(independent_by_new_count[2]),
    )


def clause_is_satisfied(clause: Sequence[int], assignment: Sequence[bool]) -> bool:
    return any(
        assignment[abs(literal) - 1] == (literal > 0) for literal in clause
    )


def formula_is_satisfied(
    clauses: Iterable[Sequence[int]], assignment: Sequence[bool]
) -> bool:
    return all(clause_is_satisfied(clause, assignment) for clause in clauses)


def completed_adjacency(
    core: list[int], assignment: Sequence[bool]
) -> list[int]:
    """Build the full core,new-A,new-B graph from a complete assignment."""
    validate_simple(core)
    core_count = len(core)
    expected = 2 * core_count + 1
    if len(assignment) != expected:
        raise ValueError(f"expected {expected} assignment values")
    result = core.copy() + [0, 0]
    for core_vertex in range(core_count):
        for new_vertex in (core_count, core_count + 1):
            variable = variable_for_unknown_edge(
                core_count, core_vertex, new_vertex
            )
            if assignment[variable - 1]:
                result[core_vertex] |= 1 << new_vertex
                result[new_vertex] |= 1 << core_vertex
    between_variable = variable_for_unknown_edge(
        core_count, core_count, core_count + 1
    )
    if assignment[between_variable - 1]:
        result[core_count] |= 1 << (core_count + 1)
        result[core_count + 1] |= 1 << core_count
    validate_simple(result)
    return result


def render_dimacs(
    instance: CoreCompletionInstance,
    *,
    base_graph6: str,
    base_file_sha256: str,
    deleted_original_vertex: int,
    core_original_vertices: Sequence[int],
) -> str:
    clauses = instance.clauses
    core_count = instance.core_vertex_count
    lines = [
        f"c generator {GENERATOR_ID}",
        f"c base_file_sha256 {base_file_sha256}",
        f"c base_graph6 {base_graph6}",
        f"c deleted_original_vertex {deleted_original_vertex}",
        "c core_original_vertices " + " ".join(map(str, core_original_vertices)),
        "c final vertex order: retained core positions, new_A, new_B",
        (
            "c clause order: one-new then two-new clique clauses; "
            "one-new then two-new independent clauses"
        ),
        (
            f"c forbidden_size {instance.forbidden_size} "
            f"one_new_clique {instance.one_new_clique_count} "
            f"two_new_clique {instance.two_new_clique_count} "
            f"one_new_independent {instance.one_new_independent_count} "
            f"two_new_independent {instance.two_new_independent_count}"
        ),
    ]
    for core_position, original_vertex in enumerate(core_original_vertices):
        lines.append(
            f"c var {core_position + 1} edge new_A "
            f"core_position {core_position} original_vertex {original_vertex}"
        )
    for core_position, original_vertex in enumerate(core_original_vertices):
        lines.append(
            f"c var {core_count + core_position + 1} edge new_B "
            f"core_position {core_position} original_vertex {original_vertex}"
        )
    lines.append(f"c var {2 * core_count + 1} edge new_A new_B")
    lines.append(f"p cnf {instance.variable_count} {len(clauses)}")
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return "\n".join(lines) + "\n"


def _parse_true_variables(text: str, variable_count: int) -> list[bool]:
    assignment = [False] * variable_count
    if not text.strip():
        return assignment
    for field in text.split(","):
        variable = int(field)
        if not 1 <= variable <= variable_count:
            raise ValueError(f"true variable {variable} is outside 1..{variable_count}")
        assignment[variable - 1] = True
    return assignment


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_graph", type=Path)
    parser.add_argument("--line", type=int, default=1)
    parser.add_argument("--delete-vertex", type=int, required=True)
    parser.add_argument("--forbidden-size", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument(
        "--true-variables",
        help="comma-separated SAT model; optionally export the completed graph",
    )
    parser.add_argument("--model-graph6", type=Path)
    parser.add_argument("--model-canonical-json", type=Path)
    args = parser.parse_args()

    base = read_graph(args.base_graph, args.line)
    validate_simple(base)
    base_conflicts = count_forbidden_sets(base, args.forbidden_size)
    if base_conflicts != (0, 0):
        raise SystemExit(
            "base graph is invalid: "
            f"cliques={base_conflicts[0]} independent_sets={base_conflicts[1]}"
        )
    core, original_vertices = induced_core(base, args.delete_vertex)
    core_conflicts = count_forbidden_sets(core, args.forbidden_size)
    if core_conflicts != (0, 0):
        raise AssertionError("an induced subgraph of a valid base became invalid")

    instance = build_core_completion_instance(core, args.forbidden_size)
    base_sha256 = hashlib.sha256(args.base_graph.read_bytes()).hexdigest()
    dimacs = render_dimacs(
        instance,
        base_graph6=encode_graph6(base),
        base_file_sha256=base_sha256,
        deleted_original_vertex=args.delete_vertex,
        core_original_vertices=original_vertices,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(dimacs, encoding="ascii")
    cnf_sha256 = hashlib.sha256(dimacs.encode("ascii")).hexdigest()

    result: dict[str, object] = {
        "generator": GENERATOR_ID,
        "base_file_sha256": base_sha256,
        "base_graph6": encode_graph6(base),
        "base_vertex_count": len(base),
        "deleted_original_vertex": args.delete_vertex,
        "core_vertex_count": len(core),
        "core_original_vertices": list(original_vertices),
        "core_graph6": encode_graph6(core),
        "forbidden_size": args.forbidden_size,
        "variable_count": instance.variable_count,
        "one_new_clique_clause_count": instance.one_new_clique_count,
        "two_new_clique_clause_count": instance.two_new_clique_count,
        "one_new_independent_clause_count": instance.one_new_independent_count,
        "two_new_independent_clause_count": instance.two_new_independent_count,
        "clique_clause_count": len(instance.clique_clauses),
        "independent_clause_count": len(instance.independent_clauses),
        "clause_count": len(instance.clauses),
        "cnf_sha256": cnf_sha256,
    }

    if args.true_variables is not None:
        assignment = _parse_true_variables(
            args.true_variables, instance.variable_count
        )
        if not formula_is_satisfied(instance.clauses, assignment):
            raise SystemExit("provided assignment does not satisfy the CNF")
        completed = completed_adjacency(core, assignment)
        completed_conflicts = count_forbidden_sets(
            completed, args.forbidden_size
        )
        if completed_conflicts != (0, 0):
            raise AssertionError("satisfying CNF model produced an invalid graph")
        if args.model_graph6:
            args.model_graph6.parent.mkdir(parents=True, exist_ok=True)
            args.model_graph6.write_text(
                encode_graph6(completed) + "\n", encoding="ascii"
            )
        if args.model_canonical_json:
            artifact_sha256 = write_canonical_artifact(
                completed,
                args.model_canonical_json,
                provenance={
                    "source": GENERATOR_ID,
                    "base_file_sha256": base_sha256,
                    "deleted_original_vertex": args.delete_vertex,
                    "true_variables": [
                        index + 1
                        for index, value in enumerate(assignment)
                        if value
                    ],
                },
            )
            result["model_canonical_sha256"] = artifact_sha256
        result["model_graph6"] = encode_graph6(completed)
        result["model_edge_count"] = (
            sum(neighbors.bit_count() for neighbors in completed) // 2
        )

    if args.metadata:
        args.metadata.parent.mkdir(parents=True, exist_ok=True)
        args.metadata.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
