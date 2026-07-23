#!/usr/bin/env python3
"""Exact CNF for a bounded free-edge neighborhood of a fixed graph.

Every edge outside ``free_edges`` remains equal to the input graph.  One
Boolean variable is assigned to each free edge, with true meaning edge
present.  For every 5-subset whose fixed pairs do not already prevent a
clique (respectively independent set), the formula contains the exact clause
that prevents all of its free pairs becoming edges (respectively nonedges).
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import encode_graph6, read_graph, validate_simple  # noqa: E402


GENERATOR_ID = "ramsey55_fixed_boundary_free_edge_cnf_v1"


@dataclass(frozen=True)
class ResidualLnsInstance:
    order: int
    forbidden_size: int
    free_edges: tuple[tuple[int, int], ...]
    clique_clauses: tuple[tuple[int, ...], ...]
    independent_clauses: tuple[tuple[int, ...], ...]

    @property
    def variable_count(self) -> int:
        return len(self.free_edges)

    @property
    def clauses(self) -> tuple[tuple[int, ...], ...]:
        return self.clique_clauses + self.independent_clauses


def normalize_edges(
    order: int, edges: Iterable[tuple[int, int]]
) -> tuple[tuple[int, int], ...]:
    normalized: set[tuple[int, int]] = set()
    for raw_left, raw_right in edges:
        left, right = sorted((raw_left, raw_right))
        if not 0 <= left < right < order:
            raise ValueError(
                f"free edge ({raw_left},{raw_right}) is invalid for order {order}"
            )
        normalized.add((left, right))
    if not normalized:
        raise ValueError("at least one free edge is required")
    return tuple(sorted(normalized))


def neighborhood_edges(
    order: int,
    free_vertices: Sequence[int],
    extra_edges: Iterable[tuple[int, int]],
    incident_vertices: Sequence[int] = (),
) -> tuple[tuple[int, int], ...]:
    vertices = tuple(sorted(set(free_vertices)))
    incident = tuple(sorted(set(incident_vertices)))
    if any(
        vertex < 0 or vertex >= order
        for vertex in itertools.chain(vertices, incident)
    ):
        raise ValueError("a free vertex is outside the graph")
    incident_set = set(incident)
    return normalize_edges(
        order,
        itertools.chain(
            itertools.combinations(vertices, 2),
            (
                (left, right)
                for left, right in itertools.combinations(range(order), 2)
                if left in incident_set or right in incident_set
            ),
            extra_edges,
        ),
    )


def build_residual_lns_instance(
    adjacency: list[int],
    free_edges: Iterable[tuple[int, int]],
    forbidden_size: int = 5,
) -> ResidualLnsInstance:
    validate_simple(adjacency)
    if forbidden_size < 3:
        raise ValueError("forbidden_size must be at least 3")
    if forbidden_size > len(adjacency):
        raise ValueError("forbidden_size exceeds graph order")
    edges = normalize_edges(len(adjacency), free_edges)
    variable_by_edge = {
        edge: variable for variable, edge in enumerate(edges, 1)
    }
    clique_clauses: list[tuple[int, ...]] = []
    independent_clauses: list[tuple[int, ...]] = []

    for vertices in itertools.combinations(range(len(adjacency)), forbidden_size):
        free_variables: list[int] = []
        fixed_values: list[bool] = []
        for left, right in itertools.combinations(vertices, 2):
            variable = variable_by_edge.get((left, right))
            if variable is None:
                fixed_values.append(bool((adjacency[left] >> right) & 1))
            else:
                free_variables.append(variable)
        if all(fixed_values):
            clique_clauses.append(
                tuple(-variable for variable in free_variables)
            )
        if not any(fixed_values):
            independent_clauses.append(tuple(free_variables))

    return ResidualLnsInstance(
        order=len(adjacency),
        forbidden_size=forbidden_size,
        free_edges=edges,
        clique_clauses=tuple(clique_clauses),
        independent_clauses=tuple(independent_clauses),
    )


def assignment_from_graph(
    adjacency: Sequence[int], free_edges: Sequence[tuple[int, int]]
) -> tuple[bool, ...]:
    return tuple(bool((adjacency[left] >> right) & 1) for left, right in free_edges)


def apply_assignment(
    adjacency: list[int],
    free_edges: Sequence[tuple[int, int]],
    assignment: Sequence[bool],
) -> list[int]:
    if len(free_edges) != len(assignment):
        raise ValueError("assignment length does not match free-edge count")
    result = adjacency.copy()
    for (left, right), edge_present in zip(free_edges, assignment, strict=True):
        if edge_present:
            result[left] |= 1 << right
            result[right] |= 1 << left
        else:
            result[left] &= ~(1 << right)
            result[right] &= ~(1 << left)
    validate_simple(result)
    return result


def formula_is_satisfied(
    clauses: Iterable[Sequence[int]], assignment: Sequence[bool]
) -> bool:
    return all(
        any(
            assignment[abs(literal) - 1] == (literal > 0)
            for literal in clause
        )
        for clause in clauses
    )


def count_forbidden_sets(
    adjacency: Sequence[int], forbidden_size: int = 5
) -> tuple[int, int]:
    cliques = 0
    independent_sets = 0
    pair_count = forbidden_size * (forbidden_size - 1) // 2
    for vertices in itertools.combinations(range(len(adjacency)), forbidden_size):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        cliques += int(edge_count == pair_count)
        independent_sets += int(edge_count == 0)
    return cliques, independent_sets


def render_dimacs(
    instance: ResidualLnsInstance,
    *,
    base_graph6: str,
    base_file_sha256: str,
) -> str:
    lines = [
        f"c generator {GENERATOR_ID}",
        f"c base_file_sha256 {base_file_sha256}",
        f"c base_graph6 {base_graph6}",
        "c fixed_boundary all unlisted edges equal the base graph",
        "c variable true means the named free edge is present",
        (
            "c clause order: lexicographic 5-subset clique-prevention clauses, "
            "then lexicographic 5-subset independent-prevention clauses"
        ),
        (
            f"c forbidden_size {instance.forbidden_size} "
            f"clique_clauses {len(instance.clique_clauses)} "
            f"independent_clauses {len(instance.independent_clauses)}"
        ),
    ]
    for variable, (left, right) in enumerate(instance.free_edges, 1):
        lines.append(f"c var {variable} edge {left} {right}")
    lines.append(
        f"p cnf {instance.variable_count} {len(instance.clauses)}"
    )
    lines.extend(
        " ".join(map(str, clause)) + (" " if clause else "") + "0"
        for clause in instance.clauses
    )
    return "\n".join(lines) + "\n"


def parse_vertex_list(text: str) -> tuple[int, ...]:
    if not text:
        return ()
    return tuple(int(field) for field in text.split(","))


def parse_edge(text: str) -> tuple[int, int]:
    fields = text.split(",")
    if len(fields) != 2:
        raise argparse.ArgumentTypeError("edge must have form LEFT,RIGHT")
    return int(fields[0]), int(fields[1])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_graph", type=Path)
    parser.add_argument("--line", type=int, default=1)
    parser.add_argument("--forbidden-size", type=int, default=5)
    parser.add_argument("--free-vertices", type=parse_vertex_list, default=())
    parser.add_argument(
        "--free-incident-vertices",
        type=parse_vertex_list,
        default=(),
        help="free every edge having at least one endpoint in this list",
    )
    parser.add_argument(
        "--free-edge", type=parse_edge, action="append", default=[]
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()

    adjacency = read_graph(args.base_graph, args.line)
    validate_simple(adjacency)
    free_edges = neighborhood_edges(
        len(adjacency),
        args.free_vertices,
        args.free_edge,
        args.free_incident_vertices,
    )
    instance = build_residual_lns_instance(
        adjacency, free_edges, args.forbidden_size
    )
    base_bytes = args.base_graph.read_bytes()
    base_sha256 = hashlib.sha256(base_bytes).hexdigest()
    base_graph6 = encode_graph6(adjacency)
    dimacs = render_dimacs(
        instance,
        base_graph6=base_graph6,
        base_file_sha256=base_sha256,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(dimacs, encoding="ascii", newline="\n")
    cnf_sha256 = hashlib.sha256(dimacs.encode("ascii")).hexdigest()
    base_assignment = assignment_from_graph(adjacency, instance.free_edges)
    base_forbidden = count_forbidden_sets(adjacency, args.forbidden_size)

    result = {
        "generator": GENERATOR_ID,
        "base_file_sha256": base_sha256,
        "base_graph6": base_graph6,
        "order": len(adjacency),
        "forbidden_size": args.forbidden_size,
        "induced_free_vertices": sorted(set(args.free_vertices)),
        "incident_free_vertices": sorted(set(args.free_incident_vertices)),
        "free_edges": [list(edge) for edge in instance.free_edges],
        "variable_count": instance.variable_count,
        "clique_clause_count": len(instance.clique_clauses),
        "independent_clause_count": len(instance.independent_clauses),
        "clause_count": len(instance.clauses),
        "base_true_variables": [
            variable
            for variable, present in enumerate(base_assignment, 1)
            if present
        ],
        "base_forbidden_cliques": base_forbidden[0],
        "base_forbidden_independent_sets": base_forbidden[1],
        "base_assignment_satisfies_cnf": formula_is_satisfied(
            instance.clauses, base_assignment
        ),
        "cnf_sha256": cnf_sha256,
    }
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
