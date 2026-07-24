#!/usr/bin/env python3
"""Generate the symmetry-broken certificate CNF for cycle type 13^2 1^17."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import automorphism13_two_cycle_search as search


GENERATOR_ID = "ramsey55_order13_two_cycle_symmetry_cnf_generator_v1"


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def symmetry_breaking_clauses(
    edge_variable: dict[tuple[int, int], int],
) -> tuple[tuple[int, ...], ...]:
    """Encode the rigorously justified one-hot/sorted group normalization."""
    result: list[tuple[int, ...]] = []
    first_cycle_variables: list[int] = []
    for fixed_vertex in search.FIXED_VERTICES:
        first = edge_variable[(0, fixed_vertex)]
        second = edge_variable[(13, fixed_vertex)]
        first_cycle_variables.append(first)
        result.extend(((first, second), (-first, -second)))
    # Fixed vertices may be relabeled, so first-cycle incidences form a prefix.
    result.extend(
        (left, -right)
        for left, right in zip(
            first_cycle_variables, first_cycle_variables[1:]
        )
    )
    # Exchanging the two moved cycles selects the prefix of size at most eight.
    result.append((-first_cycle_variables[8],))
    if len(result) != 51:
        raise AssertionError("unexpected symmetry-breaking clause count")
    return tuple(result)


def write_dimacs(
    path: Path, variable_count: int, clauses: list[tuple[int, ...]]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()

    _, edge_variable, orbits, signatures = search.formula()
    base_clauses = search.clauses(signatures)
    extra_clauses = symmetry_breaking_clauses(edge_variable)
    complete_clauses = [*base_clauses, *extra_clauses]
    write_dimacs(args.cnf, len(orbits), complete_clauses)
    source = Path(__file__).resolve()
    search_source = Path(search.__file__).resolve()
    first_cycle_variables = [
        edge_variable[(0, fixed_vertex)]
        for fixed_vertex in search.FIXED_VERTICES
    ]
    second_cycle_variables = [
        edge_variable[(13, fixed_vertex)]
        for fixed_vertex in search.FIXED_VERTICES
    ]
    metadata = {
        "generator": GENERATOR_ID,
        "claim_scope": (
            "Order-43 Ramsey(5,5) graphs admitting an automorphism with "
            "cycle type 13^2 1^17 only; this does not cover 13^1 1^30."
        ),
        "order": 43,
        "clique_size": 5,
        "automorphism_order": 13,
        "cycle_count": 2,
        "fixed_point_count": 17,
        "cycle_type": "13^2 1^17",
        "variable_count": len(orbits),
        "base_clause_count": len(base_clauses),
        "symmetry_breaking_clause_count": len(extra_clauses),
        "clause_count": len(complete_clauses),
        "unique_orbit_signature_count": len(signatures),
        "degree_theorem": {
            "global_degree_bound": [18, 24],
            "degree_expression": "13*m + d_F",
            "moved_cycle_neighbors_per_fixed_vertex": 1,
            "fixed_subgraph_degree_bound": [5, 11],
        },
        "symmetry_cover": {
            "fixed_vertex_relabeling": (
                "Sort first-cycle incidence bits into a true prefix."
            ),
            "moved_cycle_exchange": (
                "Choose the prefix size at most floor(17/2)=8."
            ),
            "normalized_group_sizes": list(range(9)),
            "complete_group_split_count": 9,
            "first_cycle_variables": first_cycle_variables,
            "second_cycle_variables": second_cycle_variables,
            "added_clause_order": (
                "34 alternating one-hot clauses, 16 prefix-order clauses, "
                "then the unit clause negating the ninth prefix bit."
            ),
        },
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256_file(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "generator_path": str(source),
        "generator_sha256": sha256_file(source),
        "formula_source_path": str(search_source),
        "formula_source_sha256": sha256_file(search_source),
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
