#!/usr/bin/env python3
"""Generate the exact fixed-core one-vertex extension formula with E <= 2."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from catalog42_optimal_extension_certificate import (
    GENERATOR_ID as ENUMERATION_GENERATOR_ID,
    catalog_lines,
    extension_constraints,
    write_cnf,
)
from direct_ramsey_cnf import COUNTER_ID, allocate_sequential_counter
from graph_io import decode_graph6


GENERATOR_ID = "ramsey55_catalog42_e2_extension_cnf_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def build_formula(
    core: list[int],
) -> tuple[int, list[tuple[int, ...]], dict[str, int]]:
    constraints = extension_constraints(core)
    next_variable = 43
    relaxation_variables: list[int] = []
    definition_clauses: list[tuple[int, ...]] = []
    for _, _, clause in constraints:
        relaxation = next_variable
        next_variable += 1
        relaxation_variables.append(relaxation)
        definition_clauses.append(clause + (relaxation,))
        definition_clauses.extend(
            (-relaxation, -literal) for literal in clause
        )
    counter, next_variable = allocate_sequential_counter(
        relaxation_variables,
        2,
        next_variable,
        "extension_conflicts_at_most_2",
    )
    counter_clauses = list(counter.clauses())
    clauses = definition_clauses + counter_clauses
    counts = {
        "primary_variable_count": 42,
        "constraint_count": len(constraints),
        "clique_constraint_count": sum(
            kind == "clique" for kind, _, _ in constraints
        ),
        "independent_constraint_count": sum(
            kind == "independent" for kind, _, _ in constraints
        ),
        "relaxation_variable_count": len(relaxation_variables),
        "definition_clause_count": len(definition_clauses),
        "counter_auxiliary_variable_count": counter.auxiliary_count,
        "counter_clause_count": len(counter_clauses),
        "variable_count": next_variable - 1,
        "clause_count": len(clauses),
    }
    return next_variable - 1, clauses, counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--line", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    lines = catalog_lines(args.catalog)
    if not 1 <= args.line <= len(lines):
        raise ValueError("catalog line is out of range")
    core = decode_graph6(lines[args.line - 1])
    if len(core) != 42:
        raise ValueError("expected an order-42 core")
    variable_count, clauses, counts = build_formula(core)
    catalog_sha256 = sha256_file(args.catalog)
    comments = [
        f"generator {GENERATOR_ID}",
        f"catalog_sha256 {catalog_sha256}",
        f"catalog_line {args.line}",
        f"core_graph6 {lines[args.line - 1]}",
        "variables 1..42 are new-vertex adjacency bits",
        "one definitional conflict variable follows per core K4 or I4",
        f"counter_encoding {COUNTER_ID}",
        "the formula is satisfiable exactly for extensions with E <= 2",
        f"shared_definition_source {ENUMERATION_GENERATOR_ID}",
    ]
    written = write_cnf(args.output, clauses, variable_count, comments)
    metadata = {
        "generator": GENERATOR_ID,
        "catalog_path": str(args.catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "catalog_line": args.line,
        "core_graph6": lines[args.line - 1],
        "core_edge_count": sum(row.bit_count() for row in core) // 2,
        "counter_encoding": COUNTER_ID,
        "conflict_bound": 2,
        "semantics": (
            "The formula is satisfiable iff the fixed order-42 core has a "
            "one-vertex extension with at most two forbidden five-sets."
        ),
        "cnf_path": str(args.output.resolve()),
        **counts,
        **written,
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(metadata, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
