#!/usr/bin/env python3
"""Deterministic CNF for a fixed core completed by exactly three new vertices.

The production k=2 experiment deletes two vertices from a verified
42-vertex (5,5)-graph, preserves the induced 40-vertex core, and solves for
the 123 edges having at least one endpoint among three new vertices.
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


GENERATOR_ID = "ramsey55_three_vertex_core_completion_cnf_v1"
NEW_VERTEX_COUNT = 3


@dataclass(frozen=True)
class CoreCompletionK2Instance:
    core_vertex_count: int
    forbidden_size: int
    new_vertex_count: int
    clique_clauses: tuple[tuple[int, ...], ...]
    independent_clauses: tuple[tuple[int, ...], ...]
    clique_counts_by_new_count: tuple[int, ...]
    independent_counts_by_new_count: tuple[int, ...]

    @property
    def variable_count(self) -> int:
        return (
            self.new_vertex_count * self.core_vertex_count
            + self.new_vertex_count * (self.new_vertex_count - 1) // 2
        )

    @property
    def clauses(self) -> tuple[tuple[int, ...], ...]:
        return self.clique_clauses + self.independent_clauses


def induced_core(
    adjacency: list[int], deleted_vertices: Sequence[int]
) -> tuple[list[int], tuple[int, ...]]:
    validate_simple(adjacency)
    deleted = tuple(sorted(deleted_vertices))
    if len(deleted) != len(set(deleted)):
        raise ValueError("deleted vertices must be distinct")
    if any(vertex < 0 or vertex >= len(adjacency) for vertex in deleted):
        raise ValueError("a deleted vertex is outside the base graph")
    deleted_set = set(deleted)
    originals = tuple(
        vertex for vertex in range(len(adjacency)) if vertex not in deleted_set
    )
    core = [0] * len(originals)
    for new_left, old_left in enumerate(originals):
        for new_right in range(new_left + 1, len(originals)):
            old_right = originals[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                core[new_left] |= 1 << new_right
                core[new_right] |= 1 << new_left
    validate_simple(core)
    return core, originals


def variable_for_unknown_edge(
    core_count: int,
    new_count: int,
    left: int,
    right: int,
) -> int:
    """Map a final-graph edge involving a new vertex to a one-based variable."""
    if left > right:
        left, right = right, left
    final_order = core_count + new_count
    if not (0 <= left < right < final_order) or right < core_count:
        raise ValueError(f"edge ({left},{right}) is fixed or out of range")
    if left < core_count:
        new_index = right - core_count
        return new_index * core_count + left + 1
    new_left = left - core_count
    new_right = right - core_count
    for pair_index, pair in enumerate(
        itertools.combinations(range(new_count), 2)
    ):
        if pair == (new_left, new_right):
            return new_count * core_count + pair_index + 1
    raise AssertionError("new-new edge was not found in the variable order")


def _fixed_pair_flags(
    core: Sequence[int], core_vertices: Sequence[int]
) -> tuple[bool, bool]:
    all_edges = True
    all_nonedges = True
    for left, right in itertools.combinations(core_vertices, 2):
        if (core[left] >> right) & 1:
            all_nonedges = False
        else:
            all_edges = False
    return all_edges, all_nonedges


def _unknown_variables(
    core_count: int,
    new_count: int,
    vertices: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        variable_for_unknown_edge(core_count, new_count, left, right)
        for left, right in itertools.combinations(vertices, 2)
        if right >= core_count
    )


def count_forbidden_sets(
    adjacency: Sequence[int], forbidden_size: int
) -> tuple[int, int]:
    cliques = 0
    independent_sets = 0
    total_pairs = forbidden_size * (forbidden_size - 1) // 2
    for vertices in itertools.combinations(range(len(adjacency)), forbidden_size):
        edges = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        cliques += int(edges == total_pairs)
        independent_sets += int(edges == 0)
    return cliques, independent_sets


def build_core_completion_k2_instance(
    core: list[int],
    forbidden_size: int = 5,
    new_vertex_count: int = NEW_VERTEX_COUNT,
) -> CoreCompletionK2Instance:
    validate_simple(core)
    if forbidden_size < 3:
        raise ValueError("forbidden_size must be at least 3")
    if new_vertex_count < 1:
        raise ValueError("new_vertex_count must be positive")
    core_count = len(core)
    new_vertices = tuple(range(core_count, core_count + new_vertex_count))
    clique_families = [[] for _ in range(new_vertex_count + 1)]
    independent_families = [[] for _ in range(new_vertex_count + 1)]

    for selected_new_count in range(
        1, min(new_vertex_count, forbidden_size) + 1
    ):
        core_subset_size = forbidden_size - selected_new_count
        if core_subset_size > core_count:
            continue
        for selected_new in itertools.combinations(
            new_vertices, selected_new_count
        ):
            for selected_core in itertools.combinations(
                range(core_count), core_subset_size
            ):
                all_edges, all_nonedges = _fixed_pair_flags(
                    core, selected_core
                )
                variables = _unknown_variables(
                    core_count,
                    new_vertex_count,
                    tuple(selected_core) + tuple(selected_new),
                )
                if all_edges:
                    clique_families[selected_new_count].append(
                        tuple(-variable for variable in variables)
                    )
                if all_nonedges:
                    independent_families[selected_new_count].append(variables)

    clique_clauses = tuple(
        clause
        for family in clique_families[1:]
        for clause in family
    )
    independent_clauses = tuple(
        clause
        for family in independent_families[1:]
        for clause in family
    )
    return CoreCompletionK2Instance(
        core_vertex_count=core_count,
        forbidden_size=forbidden_size,
        new_vertex_count=new_vertex_count,
        clique_clauses=clique_clauses,
        independent_clauses=independent_clauses,
        clique_counts_by_new_count=tuple(map(len, clique_families)),
        independent_counts_by_new_count=tuple(
            map(len, independent_families)
        ),
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
    core: list[int],
    assignment: Sequence[bool],
    new_vertex_count: int = NEW_VERTEX_COUNT,
) -> list[int]:
    validate_simple(core)
    core_count = len(core)
    expected = (
        new_vertex_count * core_count
        + new_vertex_count * (new_vertex_count - 1) // 2
    )
    if len(assignment) != expected:
        raise ValueError(f"expected {expected} assignment values")
    result = core.copy() + [0] * new_vertex_count
    for left, right in itertools.combinations(
        range(core_count + new_vertex_count), 2
    ):
        if right < core_count:
            continue
        variable = variable_for_unknown_edge(
            core_count, new_vertex_count, left, right
        )
        if assignment[variable - 1]:
            result[left] |= 1 << right
            result[right] |= 1 << left
    validate_simple(result)
    return result


def render_dimacs(
    instance: CoreCompletionK2Instance,
    *,
    base_graph6: str,
    base_file_sha256: str,
    deleted_original_vertices: Sequence[int],
    core_original_vertices: Sequence[int],
) -> str:
    core_count = instance.core_vertex_count
    new_count = instance.new_vertex_count
    lines = [
        f"c generator {GENERATOR_ID}",
        f"c base_file_sha256 {base_file_sha256}",
        f"c base_graph6 {base_graph6}",
        "c deleted_original_vertices "
        + " ".join(map(str, deleted_original_vertices)),
        "c core_original_vertices " + " ".join(map(str, core_original_vertices)),
        "c final vertex order: retained core positions, new_0, new_1, new_2",
        (
            "c clause order: clique families by number of new vertices, "
            "then independent families by number of new vertices"
        ),
        (
            "c clique_counts_by_new_count "
            + " ".join(map(str, instance.clique_counts_by_new_count))
        ),
        (
            "c independent_counts_by_new_count "
            + " ".join(map(str, instance.independent_counts_by_new_count))
        ),
    ]
    for new_index in range(new_count):
        for core_position, original_vertex in enumerate(core_original_vertices):
            variable = variable_for_unknown_edge(
                core_count,
                new_count,
                core_position,
                core_count + new_index,
            )
            lines.append(
                f"c var {variable} edge new_{new_index} "
                f"core_position {core_position} original_vertex {original_vertex}"
            )
    for left, right in itertools.combinations(range(new_count), 2):
        variable = variable_for_unknown_edge(
            core_count,
            new_count,
            core_count + left,
            core_count + right,
        )
        lines.append(f"c var {variable} edge new_{left} new_{right}")
    lines.append(f"p cnf {instance.variable_count} {len(instance.clauses)}")
    lines.extend(
        " ".join(map(str, clause)) + " 0" for clause in instance.clauses
    )
    return "\n".join(lines) + "\n"


def _parse_deleted_vertices(text: str) -> tuple[int, ...]:
    result = tuple(sorted(int(field) for field in text.split(",")))
    if len(result) != 2 or len(set(result)) != 2:
        raise ValueError("k=2 requires exactly two distinct deleted vertices")
    return result


def _parse_true_variables(text: str, variable_count: int) -> list[bool]:
    assignment = [False] * variable_count
    if not text.strip():
        return assignment
    for field in text.split(","):
        variable = int(field)
        if not 1 <= variable <= variable_count:
            raise ValueError(f"true variable {variable} outside the formula")
        assignment[variable - 1] = True
    return assignment


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_graph", type=Path)
    parser.add_argument("--line", type=int, default=1)
    parser.add_argument("--delete-vertices", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--true-variables")
    parser.add_argument("--model-graph6", type=Path)
    parser.add_argument("--model-canonical-json", type=Path)
    args = parser.parse_args()

    deleted = _parse_deleted_vertices(args.delete_vertices)
    base = read_graph(args.base_graph, args.line)
    validate_simple(base)
    base_conflicts = count_forbidden_sets(base, 5)
    if base_conflicts != (0, 0):
        raise SystemExit(f"base graph is invalid: conflicts={base_conflicts}")
    core, originals = induced_core(base, deleted)
    if count_forbidden_sets(core, 5) != (0, 0):
        raise AssertionError("induced core is unexpectedly invalid")
    instance = build_core_completion_k2_instance(core)

    base_sha256 = hashlib.sha256(args.base_graph.read_bytes()).hexdigest()
    dimacs = render_dimacs(
        instance,
        base_graph6=encode_graph6(base),
        base_file_sha256=base_sha256,
        deleted_original_vertices=deleted,
        core_original_vertices=originals,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(dimacs, encoding="ascii")
    cnf_sha256 = hashlib.sha256(dimacs.encode("ascii")).hexdigest()
    result: dict[str, object] = {
        "generator": GENERATOR_ID,
        "base_file_sha256": base_sha256,
        "base_graph6": encode_graph6(base),
        "deleted_original_vertices": list(deleted),
        "core_original_vertices": list(originals),
        "core_vertex_count": len(core),
        "core_graph6": encode_graph6(core),
        "new_vertex_count": instance.new_vertex_count,
        "variable_count": instance.variable_count,
        "clique_counts_by_new_count": list(
            instance.clique_counts_by_new_count
        ),
        "independent_counts_by_new_count": list(
            instance.independent_counts_by_new_count
        ),
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
        if count_forbidden_sets(completed, 5) != (0, 0):
            raise AssertionError("satisfying model produced an invalid graph")
        graph6 = encode_graph6(completed)
        result["model_graph6"] = graph6
        result["model_edge_count"] = (
            sum(neighbors.bit_count() for neighbors in completed) // 2
        )
        if args.model_graph6:
            args.model_graph6.parent.mkdir(parents=True, exist_ok=True)
            args.model_graph6.write_text(graph6 + "\n", encoding="ascii")
        if args.model_canonical_json:
            result["model_canonical_sha256"] = write_canonical_artifact(
                completed,
                args.model_canonical_json,
                provenance={
                    "source": GENERATOR_ID,
                    "base_file_sha256": base_sha256,
                    "deleted_original_vertices": list(deleted),
                    "true_variables": [
                        index + 1
                        for index, value in enumerate(assignment)
                        if value
                    ],
                },
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
