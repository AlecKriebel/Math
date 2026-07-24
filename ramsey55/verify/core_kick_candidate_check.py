#!/usr/bin/env python3
"""Independent structural and objective audit for core-kick candidates."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from incident_lns_candidate_check import (  # noqa: E402
    count_forbidden,
    decode_graph6,
    edge_present,
    expected_incident_edges,
    graph6_line,
    normalized_metadata_edges,
    parse_vertices,
    sha256_file,
)


VERIFIER_ID = "independent_core_kick_candidate_v1"


def run(args: argparse.Namespace) -> dict[str, object]:
    base_line = graph6_line(args.base)
    candidate_line = graph6_line(args.candidate)
    base = decode_graph6(base_line)
    candidate = decode_graph6(candidate_line)
    if len(base) != len(candidate):
        raise ValueError("base and candidate orders differ")
    order = len(base)
    incident_vertices = parse_vertices(args.incident_vertices, order)
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError("metadata root must be an object")
    metadata_edges = normalized_metadata_edges(metadata, order)
    expected_boundary = expected_incident_edges(order, incident_vertices)
    boundary_set = set(expected_boundary)
    metadata_checks = {
        "base_graph6": metadata.get("base_graph6") == base_line,
        "base_file_sha256": metadata.get("base_file_sha256")
        == sha256_file(args.base),
        "free_edges_exactly_incident_boundary": metadata_edges
        == expected_boundary,
        "variable_count": metadata.get("variable_count")
        == len(metadata_edges),
    }

    changed_boundary: list[tuple[int, int]] = []
    changed_core: list[tuple[int, int]] = []
    for left, right in itertools.combinations(range(order), 2):
        if edge_present(base, left, right) == edge_present(
            candidate, left, right
        ):
            continue
        if (left, right) in boundary_set:
            changed_boundary.append((left, right))
        else:
            changed_core.append((left, right))

    cliques, independent_sets = count_forbidden(candidate, args.k)
    degrees = sorted(row.bit_count() for row in candidate)
    edge_count = sum(degrees) // 2
    search = json.loads(args.search_json.read_text(encoding="utf-8"))
    if not isinstance(search, dict):
        raise ValueError("search JSON root must be an object")
    search_checks = {
        "mode": search.get("mode") == "search",
        "algorithm": search.get("algorithm")
        == "core_kick_dynamic_swap_lns_v1",
        "graph6": search.get("graph6") == candidate_line,
        "C5": search.get("C5") == cliques,
        "I5": search.get("I5") == independent_sets,
        "E": search.get("E") == cliques + independent_sets,
        "edge_count": search.get("edge_count") == edge_count,
        "degree_sequence": search.get("degree_sequence") == degrees,
        "changed_boundary_edges": search.get("changed_boundary_edges")
        == len(changed_boundary),
        "changed_core_edge_count": search.get("changed_core_edge_count")
        == len(changed_core),
        "changed_core_edges": search.get("changed_core_edges")
        == [list(pair) for pair in changed_core],
        "min_core_distance": search.get("min_core_distance")
        == args.min_core_distance,
        "max_core_distance": search.get("max_core_distance")
        == args.max_core_distance,
    }
    core_distance_valid = (
        args.min_core_distance
        <= len(changed_core)
        <= args.max_core_distance
    )
    structural_valid = (
        all(metadata_checks.values())
        and all(search_checks.values())
        and core_distance_valid
    )
    ramsey_valid = cliques == 0 and independent_sets == 0
    return {
        "verifier": VERIFIER_ID,
        "base": str(args.base),
        "base_sha256": sha256_file(args.base),
        "candidate": str(args.candidate),
        "candidate_sha256": sha256_file(args.candidate),
        "metadata": str(args.metadata),
        "metadata_sha256": sha256_file(args.metadata),
        "search_json": str(args.search_json),
        "search_json_sha256": sha256_file(args.search_json),
        "n": order,
        "k": args.k,
        "incident_vertices": list(incident_vertices),
        "boundary_edge_count": len(expected_boundary),
        "core_edge_count": order * (order - 1) // 2 - len(expected_boundary),
        "changed_boundary_edge_count": len(changed_boundary),
        "changed_core_edge_count": len(changed_core),
        "changed_core_edges": [list(pair) for pair in changed_core],
        "min_core_distance": args.min_core_distance,
        "max_core_distance": args.max_core_distance,
        "core_distance_valid": core_distance_valid,
        "metadata_checks": metadata_checks,
        "metadata_valid": all(metadata_checks.values()),
        "search_checks": search_checks,
        "search_output_valid": all(search_checks.values()),
        "structural_valid": structural_valid,
        "clique_count": cliques,
        "independent_count": independent_sets,
        "objective": cliques + independent_sets,
        "ramsey_valid": ramsey_valid,
        "accepted": structural_valid and ramsey_valid,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--search-json", type=Path, required=True)
    parser.add_argument("--incident-vertices", required=True)
    parser.add_argument("--min-core-distance", type=int, required=True)
    parser.add_argument("--max-core-distance", type=int, required=True)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = run(args)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        result = {
            "verifier": VERIFIER_ID,
            "structural_valid": False,
            "ramsey_valid": False,
            "accepted": False,
            "error": str(error),
        }
        status = 2
    else:
        status = 0 if result["accepted"] else 1
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
