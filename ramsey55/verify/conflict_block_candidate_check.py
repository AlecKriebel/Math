#!/usr/bin/env python3
"""Independent search-record and objective audit for conflict-block output."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import read_graph  # noqa: E402


VERIFIER_ID = "independent_conflict_block_candidate_v1"
ALGORITHM_ID = "conflict_hypergraph_probsat_blocks_v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph6_line(path: Path) -> str:
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            return line.removeprefix(">>graph6<<")
    raise ValueError("graph has no data line")


def count_forbidden(adjacency: list[int], size: int = 5) -> tuple[int, int]:
    cliques = 0
    independent = 0
    target = size * (size - 1) // 2
    for vertices in itertools.combinations(range(len(adjacency)), size):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        cliques += edge_count == target
        independent += edge_count == 0
    return cliques, independent


def degree_penalty(adjacency: list[int]) -> int:
    result = 0
    for neighbors in adjacency:
        degree = neighbors.bit_count()
        if degree < 18:
            result += (18 - degree) ** 2
        if degree > 24:
            result += (degree - 24) ** 2
    return result


def edge_hamming(left: list[int], right: list[int]) -> int:
    return sum(
        ((left[a] >> b) & 1) != ((right[a] >> b) & 1)
        for a, b in itertools.combinations(range(len(left)), 2)
    )


def run(args: argparse.Namespace) -> dict[str, object]:
    base = read_graph(args.base)
    candidate = read_graph(args.candidate)
    if len(base) != len(candidate):
        raise ValueError("base and candidate orders differ")
    search = json.loads(args.search_json.read_text(encoding="utf-8"))
    if not isinstance(search, dict):
        raise ValueError("search JSON root is not an object")

    base_cliques, base_independent = count_forbidden(base, args.k)
    cliques, independent = count_forbidden(candidate, args.k)
    degrees = sorted(neighbors.bit_count() for neighbors in candidate)
    edge_count = sum(degrees) // 2
    penalty = degree_penalty(candidate)
    hamming = edge_hamming(base, candidate)
    candidate_line = graph6_line(args.candidate)

    improvements = search.get("improvements")
    if not isinstance(improvements, list):
        raise ValueError("improvements is not an array")
    trace_checks: list[bool] = []
    previous = base_cliques + base_independent
    for expected_ordinal, item in enumerate(improvements, start=1):
        valid = (
            isinstance(item, dict)
            and item.get("ordinal") == expected_ordinal
            and isinstance(item.get("E"), int)
            and item["E"] < previous
            and item.get("C5", -1) + item.get("I5", -1) == item["E"]
            and isinstance(item.get("cause"), str)
            and item.get("degree_penalty", -1) >= 0
            and item.get("edge_hamming_distance", -1) >= 0
        )
        trace_checks.append(valid)
        if valid:
            previous = item["E"]
    expected_best = previous

    search_checks = {
        "mode": search.get("mode") == "search",
        "algorithm": search.get("algorithm") == ALGORITHM_ID,
        "seed_graph": search.get("seed_graph") == str(args.base),
        "output": Path(str(search.get("output"))) == args.candidate,
        "graph6": search.get("graph6") == candidate_line,
        "initial_C5": search.get("initial_C5") == base_cliques,
        "initial_I5": search.get("initial_I5") == base_independent,
        "initial_E": search.get("initial_E")
        == base_cliques + base_independent,
        "C5": search.get("C5") == cliques,
        "I5": search.get("I5") == independent,
        "E": search.get("E") == cliques + independent,
        "best_matches_trace": search.get("E") == expected_best,
        "strict_improvement_count": search.get("strict_improvements")
        == len(improvements),
        "degree_penalty": search.get("degree_penalty") == penalty,
        "edge_count": search.get("edge_count") == edge_count,
        "edge_hamming_distance": search.get("edge_hamming_distance")
        == hamming,
        "degree_sequence": search.get("degree_sequence") == degrees,
        "stopped_on_E0": search.get("stopped_on_E0")
        == (cliques + independent == 0),
        "step_budget": search.get("steps_executed", -1)
        <= search.get("steps_requested_per_restart", -1)
        * search.get("restarts", -1),
        "trace_records": all(trace_checks),
    }
    accepted = len(base) == 43 and all(search_checks.values())
    return {
        "verifier": VERIFIER_ID,
        "algorithm": ALGORITHM_ID,
        "base": str(args.base),
        "base_sha256": sha256(args.base),
        "candidate": str(args.candidate),
        "candidate_sha256": sha256(args.candidate),
        "search_json": str(args.search_json),
        "search_json_sha256": sha256(args.search_json),
        "n": len(candidate),
        "k": args.k,
        "base_clique_count": base_cliques,
        "base_independent_count": base_independent,
        "base_objective": base_cliques + base_independent,
        "clique_count": cliques,
        "independent_count": independent,
        "objective": cliques + independent,
        "edge_count": edge_count,
        "degree_sequence": degrees,
        "degree_penalty": penalty,
        "edge_hamming_distance": hamming,
        "improvement_trace_length": len(improvements),
        "search_checks": search_checks,
        "accepted": accepted,
        "ramsey_valid": cliques == 0 and independent == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--search-json", type=Path, required=True)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = run(args)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        result = {
            "verifier": VERIFIER_ID,
            "accepted": False,
            "ramsey_valid": False,
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
