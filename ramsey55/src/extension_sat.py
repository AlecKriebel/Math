#!/usr/bin/env python3
"""Deterministic CNF generator for extending a fixed Ramsey graph by one vertex.

For a base (k,k;n)-graph H, variable i+1 is true exactly when the new vertex
is adjacent to base vertex i.  Every (k-1)-clique gives a negative clause and
every independent (k-1)-set gives a positive clause.
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

from graph_io import encode_graph6, read_graph, validate_simple  # noqa: E402


GENERATOR_ID = "ramsey55_one_vertex_extension_cnf_v1"


@dataclass(frozen=True)
class ExtensionInstance:
    """An extension formula and the two semantic clause counts."""

    variable_count: int
    forbidden_size: int
    clique_clauses: tuple[tuple[int, ...], ...]
    independent_clauses: tuple[tuple[int, ...], ...]

    @property
    def clauses(self) -> tuple[tuple[int, ...], ...]:
        return self.clique_clauses + self.independent_clauses


def _edge(adjacency: Sequence[int], left: int, right: int) -> bool:
    return bool((adjacency[left] >> right) & 1)


def _homogeneous_type(
    adjacency: Sequence[int], vertices: Sequence[int]
) -> int:
    """Return 1 for a clique, 0 for an independent set, and -1 otherwise."""
    saw_edge = False
    saw_nonedge = False
    for offset, left in enumerate(vertices):
        for right in vertices[offset + 1 :]:
            if _edge(adjacency, left, right):
                saw_edge = True
            else:
                saw_nonedge = True
            if saw_edge and saw_nonedge:
                return -1
    if saw_edge:
        return 1
    return 0


def count_forbidden_base_sets(
    adjacency: Sequence[int], forbidden_size: int = 5
) -> tuple[int, int]:
    """Count forbidden subsets already wholly contained in the base graph."""
    clique_count = 0
    independent_count = 0
    for vertices in itertools.combinations(range(len(adjacency)), forbidden_size):
        kind = _homogeneous_type(adjacency, vertices)
        clique_count += int(kind == 1)
        independent_count += int(kind == 0)
    return clique_count, independent_count


def build_extension_instance(
    adjacency: list[int], forbidden_size: int = 5
) -> ExtensionInstance:
    """Construct the exact one-new-vertex extension formula."""
    validate_simple(adjacency)
    if forbidden_size < 3:
        raise ValueError("forbidden_size must be at least 3")
    if len(adjacency) < forbidden_size - 1:
        raise ValueError("base graph is too small for extension clauses")

    clique_clauses: list[tuple[int, ...]] = []
    independent_clauses: list[tuple[int, ...]] = []
    for vertices in itertools.combinations(
        range(len(adjacency)), forbidden_size - 1
    ):
        kind = _homogeneous_type(adjacency, vertices)
        if kind == 1:
            clique_clauses.append(tuple(-(vertex + 1) for vertex in vertices))
        elif kind == 0:
            independent_clauses.append(
                tuple(vertex + 1 for vertex in vertices)
            )

    return ExtensionInstance(
        variable_count=len(adjacency),
        forbidden_size=forbidden_size,
        clique_clauses=tuple(clique_clauses),
        independent_clauses=tuple(independent_clauses),
    )


def clause_is_satisfied(clause: Sequence[int], assignment: Sequence[bool]) -> bool:
    """Evaluate one DIMACS clause under a complete zero-based assignment."""
    return any(
        assignment[abs(literal) - 1] == (literal > 0) for literal in clause
    )


def formula_is_satisfied(
    clauses: Iterable[Sequence[int]], assignment: Sequence[bool]
) -> bool:
    return all(clause_is_satisfied(clause, assignment) for clause in clauses)


def render_dimacs(
    instance: ExtensionInstance,
    *,
    base_graph6: str,
    base_file_sha256: str,
) -> str:
    """Render stable DIMACS bytes; paths and timestamps are deliberately absent."""
    clauses = instance.clauses
    lines = [
        f"c generator {GENERATOR_ID}",
        f"c base_file_sha256 {base_file_sha256}",
        f"c base_graph6 {base_graph6}",
        "c variable i means: new vertex is adjacent to base vertex i-1",
        (
            "c clause order: lexicographic (k-1)-cliques first, "
            "then lexicographic independent (k-1)-sets"
        ),
        (
            f"c forbidden_size {instance.forbidden_size} "
            f"clique_clauses {len(instance.clique_clauses)} "
            f"independent_clauses {len(instance.independent_clauses)}"
        ),
        f"p cnf {instance.variable_count} {len(clauses)}",
    ]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_graph", type=Path)
    parser.add_argument("--line", type=int, default=1)
    parser.add_argument("--forbidden-size", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument(
        "--allow-invalid-base",
        action="store_true",
        help="generate even if the base already contains a forbidden set",
    )
    args = parser.parse_args()

    adjacency = read_graph(args.base_graph, args.line)
    validate_simple(adjacency)
    base_conflicts = count_forbidden_base_sets(
        adjacency, args.forbidden_size
    )
    if base_conflicts != (0, 0) and not args.allow_invalid_base:
        raise SystemExit(
            "base graph is not valid for the requested forbidden size: "
            f"cliques={base_conflicts[0]} independent_sets={base_conflicts[1]}"
        )

    instance = build_extension_instance(adjacency, args.forbidden_size)
    base_bytes = args.base_graph.read_bytes()
    base_sha256 = hashlib.sha256(base_bytes).hexdigest()
    graph6 = encode_graph6(adjacency)
    dimacs = render_dimacs(
        instance,
        base_graph6=graph6,
        base_file_sha256=base_sha256,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(dimacs, encoding="ascii")
    cnf_sha256 = hashlib.sha256(dimacs.encode("ascii")).hexdigest()

    result = {
        "generator": GENERATOR_ID,
        "base_file_sha256": base_sha256,
        "base_graph6": graph6,
        "base_vertex_count": len(adjacency),
        "base_forbidden_cliques": base_conflicts[0],
        "base_forbidden_independent_sets": base_conflicts[1],
        "forbidden_size": args.forbidden_size,
        "variable_count": instance.variable_count,
        "clique_clause_count": len(instance.clique_clauses),
        "independent_clause_count": len(instance.independent_clauses),
        "clause_count": len(instance.clauses),
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
