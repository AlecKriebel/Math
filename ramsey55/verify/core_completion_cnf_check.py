#!/usr/bin/env python3
"""Independently reconstruct and compare k=1 core-completion CNF clauses."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from core_completion_proof_check import (  # noqa: E402
    VARIABLE_COUNT,
    build_formula,
    decode_short_graph6,
    delete_vertex,
)
from extension_sat_check import read_cnf  # noqa: E402


CHECKER_ID = "core_completion_independent_cnf_set_checker_v1"


def semantic_clause_set(
    deleted_vertex: int, adjacency: list[int]
) -> set[frozenset[int]]:
    formula = build_formula(delete_vertex(adjacency, deleted_vertex))
    return {
        frozenset(
            (variable + 1 if positive else -(variable + 1))
            for variable in range(VARIABLE_COUNT)
            if (mask >> variable) & 1
        )
        for mask, positive in formula.clauses
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--cnf-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--expect-all-42",
        action="store_true",
        help="require exactly deletion labels 0 through 41",
    )
    args = parser.parse_args()
    started = time.monotonic()

    graph_bytes = args.graph.read_bytes()
    adjacency = decode_short_graph6(graph_bytes)
    paths = sorted(args.cnf_dir.glob("core_completion_delete_*.cnf"))
    if not paths:
        raise SystemExit("no core-completion CNFs found")
    deletion_labels = [int(path.stem.rsplit("_", 1)[1]) for path in paths]
    expected_labels = list(range(42)) if args.expect_all_42 else deletion_labels
    if (
        len(deletion_labels) != len(set(deletion_labels))
        or deletion_labels != expected_labels
    ):
        raise SystemExit(
            "deletion-label coverage mismatch: "
            f"found={deletion_labels}, expected={expected_labels}"
        )

    results: list[dict[str, object]] = []
    for path in paths:
        deleted_vertex = int(path.stem.rsplit("_", 1)[1])
        variable_count, clauses = read_cnf(path)
        actual = {frozenset(clause) for clause in clauses}
        expected = semantic_clause_set(deleted_vertex, adjacency)
        result = {
            "deleted_original_vertex": deleted_vertex,
            "cnf": path.name,
            "cnf_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "variable_count": variable_count,
            "clause_count": len(clauses),
            "unique_clause_count": len(actual),
            "independently_reconstructed_clause_count": len(expected),
            "missing_clause_count": len(expected - actual),
            "extra_clause_count": len(actual - expected),
            "exact_clause_set_match": (
                variable_count == VARIABLE_COUNT
                and len(clauses) == len(actual)
                and actual == expected
            ),
        }
        results.append(result)
        print(json.dumps(result, sort_keys=True), flush=True)

    valid = all(bool(item["exact_clause_set_match"]) for item in results)
    summary = {
        "checker": CHECKER_ID,
        "valid": valid,
        "graph_sha256": hashlib.sha256(graph_bytes).hexdigest(),
        "deletion_labels": deletion_labels,
        "expected_all_42": args.expect_all_42,
        "instance_count": len(results),
        "total_clause_count": sum(
            int(item["clause_count"]) for item in results
        ),
        "total_missing_clause_count": sum(
            int(item["missing_clause_count"]) for item in results
        ),
        "total_extra_clause_count": sum(
            int(item["extra_clause_count"]) for item in results
        ),
        "runtime_seconds": time.monotonic() - started,
        "instances": results,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(summary, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(
        json.dumps(
            {key: value for key, value in summary.items() if key != "instances"},
            sort_keys=True,
        )
    )
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
