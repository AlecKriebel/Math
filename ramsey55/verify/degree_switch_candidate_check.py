#!/usr/bin/env python3
"""Independent structural audit for retained degree-switch candidates."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


VERIFIER_ID = "independent_degree_switch_candidate_v1"
ALGORITHM_ID = "degree_preserving_2switch_compound_lns_v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph6_line(path: Path) -> str:
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            return line.removeprefix(">>graph6<<")
    raise ValueError("graph has no data line")


def decode_graph6(line: str) -> list[int]:
    if not line:
        raise ValueError("empty graph6 value")
    order = ord(line[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("only one-byte graph6 orders are supported")
    adjacency = [0] * order
    bit_index = 0
    for right in range(1, order):
        for left in range(right):
            byte_index = 1 + bit_index // 6
            if byte_index >= len(line):
                raise ValueError("truncated graph6 value")
            value = ord(line[byte_index]) - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 byte")
            if (value >> (5 - bit_index % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit_index += 1
    return adjacency


def count_forbidden(adjacency: list[int], size: int) -> tuple[int, int]:
    cliques = 0
    independent = 0
    for vertices in itertools.combinations(range(len(adjacency)), size):
        edge_count = 0
        for left, right in itertools.combinations(vertices, 2):
            edge_count += (adjacency[left] >> right) & 1
        cliques += edge_count == size * (size - 1) // 2
        independent += edge_count == 0
    return cliques, independent


def run(args: argparse.Namespace) -> dict[str, object]:
    base_line = graph6_line(args.base)
    candidate_line = graph6_line(args.candidate)
    base = decode_graph6(base_line)
    candidate = decode_graph6(candidate_line)
    if len(base) != len(candidate):
        raise ValueError("base and candidate orders differ")
    order = len(base)
    base_degrees = [neighbors.bit_count() for neighbors in base]
    candidate_degrees = [neighbors.bit_count() for neighbors in candidate]
    base_edges = sum(base_degrees) // 2
    candidate_edges = sum(candidate_degrees) // 2

    changed_edges: list[tuple[int, int]] = []
    added_incidence = [0] * order
    removed_incidence = [0] * order
    for left, right in itertools.combinations(range(order), 2):
        old = (base[left] >> right) & 1
        new = (candidate[left] >> right) & 1
        if old == new:
            continue
        changed_edges.append((left, right))
        target = added_incidence if new else removed_incidence
        target[left] += 1
        target[right] += 1

    cliques, independent = count_forbidden(candidate, args.k)
    base_cliques, base_independent = count_forbidden(base, args.k)
    search = json.loads(args.search_json.read_text(encoding="utf-8"))
    if not isinstance(search, dict):
        raise ValueError("search JSON root is not an object")

    if args.improvement_ordinal is None:
        expected = {
            "graph6": search.get("graph6"),
            "E": search.get("E"),
            "C5": search.get("C5"),
            "I5": search.get("I5"),
            "edge_hamming_distance": search.get("edge_hamming_distance"),
            "path": search.get("output"),
        }
        record_kind = "final"
    else:
        matches = [
            item
            for item in search.get("improvements", [])
            if isinstance(item, dict)
            and item.get("ordinal") == args.improvement_ordinal
        ]
        if len(matches) != 1:
            raise ValueError("improvement ordinal is not unique")
        expected = matches[0]
        record_kind = "strict_improvement"

    expected_path = Path(str(expected.get("path")))
    search_checks = {
        "mode": search.get("mode") == "search",
        "algorithm": search.get("algorithm") == ALGORITHM_ID,
        "seed_graph": search.get("seed_graph") == str(args.base),
        "record_graph6": expected.get("graph6") == candidate_line,
        "record_path": expected_path == args.candidate,
        "record_C5": expected.get("C5") == cliques,
        "record_I5": expected.get("I5") == independent,
        "record_E": expected.get("E") == cliques + independent,
        "record_hamming": expected.get("edge_hamming_distance")
        == len(changed_edges),
    }
    if args.improvement_ordinal is None:
        search_checks.update(
            {
                "edge_count": search.get("edge_count") == candidate_edges,
                "degree_vector": search.get("degree_vector")
                == candidate_degrees,
                "degree_sequence": search.get("degree_sequence")
                == sorted(candidate_degrees),
                "degree_vector_preserved": search.get(
                    "degree_vector_preserved"
                )
                is True,
            }
        )

    structural_checks = {
        "order_43": order == 43,
        "base_objective_2": base_cliques + base_independent == 2,
        "labeled_degree_vector_exact": candidate_degrees == base_degrees,
        "edge_count_exact": candidate_edges == base_edges,
        "balanced_changed_incidence": added_incidence == removed_incidence,
        "even_edge_hamming_distance": len(changed_edges) % 2 == 0,
    }
    accepted = all(structural_checks.values()) and all(search_checks.values())
    return {
        "verifier": VERIFIER_ID,
        "algorithm": ALGORITHM_ID,
        "record_kind": record_kind,
        "improvement_ordinal": args.improvement_ordinal,
        "base": str(args.base),
        "base_sha256": sha256(args.base),
        "candidate": str(args.candidate),
        "candidate_sha256": sha256(args.candidate),
        "search_json": str(args.search_json),
        "search_json_sha256": sha256(args.search_json),
        "n": order,
        "k": args.k,
        "base_clique_count": base_cliques,
        "base_independent_count": base_independent,
        "base_objective": base_cliques + base_independent,
        "clique_count": cliques,
        "independent_count": independent,
        "objective": cliques + independent,
        "base_edge_count": base_edges,
        "candidate_edge_count": candidate_edges,
        "edge_hamming_distance": len(changed_edges),
        "base_degree_vector": base_degrees,
        "candidate_degree_vector": candidate_degrees,
        "added_incidence": added_incidence,
        "removed_incidence": removed_incidence,
        "structural_checks": structural_checks,
        "search_checks": search_checks,
        "structural_valid": all(structural_checks.values()),
        "search_record_valid": all(search_checks.values()),
        "accepted": accepted,
        "ramsey_valid": cliques == 0 and independent == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--search-json", type=Path, required=True)
    parser.add_argument("--improvement-ordinal", type=int)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = run(args)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        result = {
            "verifier": VERIFIER_ID,
            "structural_valid": False,
            "search_record_valid": False,
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
