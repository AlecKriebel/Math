#!/usr/bin/env python3
"""Independent audit of an aligned path-relinking search result."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import complement, encode_graph6, read_graph  # noqa: E402


ALGORITHM = "aligned_path_relink_minconflicts_v1"
VERIFIER = "independent_aligned_path_relink_candidate_v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph6_line(path: Path) -> str:
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            return line.removeprefix(">>graph6<<")
    raise ValueError("graph has no data line")


def count_forbidden(adjacency: list[int]) -> tuple[int, int]:
    cliques = 0
    independent = 0
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edges = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        cliques += edges == 10
        independent += edges == 0
    return cliques, independent


def conflict_topology(adjacency: list[int]) -> dict[str, object]:
    records: list[tuple[str, tuple[int, ...]]] = []
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edges = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        if edges == 10:
            records.append(("C5", vertices))
        elif edges == 0:
            records.append(("I5", vertices))
    result: dict[str, object] = {
        "conflict_count": len(records),
        "colors": [color for color, _ in records],
        "vertex_sets": [list(vertices) for _, vertices in records],
    }
    if len(records) == 2:
        result["pair_overlap"] = len(
            set(records[0][1]).intersection(records[1][1])
        )
        result["mixed_colors"] = records[0][0] != records[1][0]
    else:
        result["pair_overlap"] = None
        result["mixed_colors"] = None
    return result


def align(adjacency: list[int], mapping: list[int]) -> list[int]:
    result = [0] * len(adjacency)
    for left in range(len(adjacency)):
        for right in range(left + 1, len(adjacency)):
            if (adjacency[mapping[left]] >> mapping[right]) & 1:
                result[left] |= 1 << right
                result[right] |= 1 << left
    return result


def edge_hamming(left: list[int], right: list[int]) -> int:
    return sum(
        ((left[a] >> b) & 1) != ((right[a] >> b) & 1)
        for a, b in itertools.combinations(range(len(left)), 2)
    )


def agreement_breaks(
    values: list[int], parent_a: list[int], parent_b: list[int]
) -> int:
    return sum(
        ((parent_a[a] >> b) & 1) == ((parent_b[a] >> b) & 1)
        and ((values[a] >> b) & 1) != ((parent_a[a] >> b) & 1)
        for a, b in itertools.combinations(range(len(values)), 2)
    )


def degree_sequence(adjacency: list[int]) -> list[int]:
    return sorted(neighbors.bit_count() for neighbors in adjacency)


def run(args: argparse.Namespace) -> dict[str, object]:
    search = json.loads(args.search_json.read_text(encoding="utf-8"))
    if not isinstance(search, dict):
        raise ValueError("search JSON root is not an object")
    raw_a = read_graph(args.parent_a)
    raw_b = read_graph(args.parent_b)
    child = read_graph(args.child)
    candidate = read_graph(args.candidate)
    if {len(raw_a), len(raw_b), len(child), len(candidate)} != {43}:
        raise ValueError("all graphs must have order 43")

    mapping = search.get("mapping")
    if (
        not isinstance(mapping, list)
        or sorted(mapping) != list(range(43))
    ):
        raise ValueError("search mapping is not a 43-vertex permutation")
    parent_a = complement(raw_a) if search.get("complement_a") else raw_a
    oriented_b = complement(raw_b) if search.get("complement_b") else raw_b
    parent_b = align(oriented_b, mapping)
    direction = search.get("direction")
    if direction == "a_to_b":
        source, target = parent_a, parent_b
    elif direction == "b_to_a":
        source, target = parent_b, parent_a
    else:
        raise ValueError("search direction is invalid")

    a_cliques, a_independent = count_forbidden(parent_a)
    b_cliques, b_independent = count_forbidden(parent_b)
    child_cliques, child_independent = count_forbidden(child)
    cliques, independent = count_forbidden(candidate)
    disagreement = edge_hamming(parent_a, parent_b)
    child_source = edge_hamming(child, source)
    child_target = edge_hamming(child, target)
    child_breaks = agreement_breaks(child, parent_a, parent_b)
    distance_a = edge_hamming(candidate, parent_a)
    distance_b = edge_hamming(candidate, parent_b)
    final_breaks = agreement_breaks(candidate, parent_a, parent_b)
    degrees = degree_sequence(candidate)
    topology = conflict_topology(candidate)

    improvements = search.get("improvements")
    if not isinstance(improvements, list):
        raise ValueError("search improvements is not an array")
    previous = child_cliques + child_independent
    trace_checks: list[bool] = []
    for ordinal, item in enumerate(improvements, start=1):
        valid = (
            isinstance(item, dict)
            and item.get("ordinal") == ordinal
            and isinstance(item.get("E"), int)
            and item["E"] < previous
            and item.get("C5", -1) + item.get("I5", -1) == item["E"]
            and item.get("distance_a", -1) >= 0
            and item.get("distance_b", -1) >= 0
            and item.get("agreement_breaks", -1) >= 0
            and 0 < item.get("step", 0) <= search.get("steps_executed", -1)
        )
        trace_checks.append(valid)
        if valid:
            previous = item["E"]

    path_flips = min(
        int(search.get("path_flips_requested", -1)), disagreement // 2
    )
    edge_count = sum(degrees) // 2
    checks = {
        "mode": search.get("mode") == "search",
        "algorithm": search.get("algorithm") == ALGORITHM,
        "parent_a_path": Path(str(search.get("parent_a"))) == args.parent_a,
        "parent_b_path": Path(str(search.get("parent_b"))) == args.parent_b,
        "child_path": Path(str(search.get("child_output"))) == args.child,
        "candidate_path": Path(str(search.get("output"))) == args.candidate,
        "parent_a_C5_only_E2": (a_cliques, a_independent) == (2, 0),
        "parent_b_C5_only_E2": (b_cliques, b_independent) == (2, 0),
        "parent_a_counts": (
            search.get("parent_a_C5"),
            search.get("parent_a_I5"),
            search.get("parent_a_E"),
        )
        == (a_cliques, a_independent, a_cliques + a_independent),
        "parent_b_counts": (
            search.get("parent_b_C5"),
            search.get("parent_b_I5"),
            search.get("parent_b_E"),
        )
        == (b_cliques, b_independent, b_cliques + b_independent),
        "parent_disagreement": search.get("parent_disagreement")
        == disagreement,
        "child_graph6": search.get("child_graph6") == graph6_line(args.child),
        "child_counts": (
            search.get("child_C5"),
            search.get("child_I5"),
            search.get("child_E"),
        )
        == (
            child_cliques,
            child_independent,
            child_cliques + child_independent,
        ),
        "child_source_distance": (
            search.get("child_distance_a")
            if direction == "a_to_b"
            else search.get("child_distance_b")
        )
        == child_source,
        "child_distance_a": search.get("child_distance_a")
        == edge_hamming(child, parent_a),
        "child_distance_b": search.get("child_distance_b")
        == edge_hamming(child, parent_b),
        "child_path_depth": child_source == path_flips,
        "child_path_partition": child_source + child_target == disagreement,
        "child_parent_agreements_preserved": child_breaks == 0
        and search.get("child_agreement_breaks") == 0,
        "candidate_graph6": search.get("graph6")
        == graph6_line(args.candidate),
        "candidate_counts": (
            search.get("C5"),
            search.get("I5"),
            search.get("E"),
        )
        == (cliques, independent, cliques + independent),
        "candidate_distance_a": search.get("distance_a") == distance_a,
        "candidate_distance_b": search.get("distance_b") == distance_b,
        "candidate_agreement_breaks": search.get("agreement_breaks")
        == final_breaks,
        "candidate_edge_count": search.get("edge_count") == edge_count,
        "candidate_degree_sequence": search.get("degree_sequence") == degrees,
        "strict_trace": all(trace_checks),
        "strict_trace_count": search.get("strict_improvements")
        == len(improvements),
        "best_matches_trace": search.get("E") == previous,
        "step_budget": 0
        <= search.get("steps_executed", -1)
        <= search.get("steps_requested", -1),
        "stopped_on_E0": search.get("stopped_on_E0")
        == (cliques + independent == 0),
    }
    accepted = all(checks.values())
    return {
        "verifier": VERIFIER,
        "algorithm": ALGORITHM,
        "parent_a": str(args.parent_a),
        "parent_a_sha256": sha256(args.parent_a),
        "parent_b": str(args.parent_b),
        "parent_b_sha256": sha256(args.parent_b),
        "child": str(args.child),
        "child_sha256": sha256(args.child),
        "candidate": str(args.candidate),
        "candidate_sha256": sha256(args.candidate),
        "search_json": str(args.search_json),
        "search_json_sha256": sha256(args.search_json),
        "parent_disagreement": disagreement,
        "child_C5": child_cliques,
        "child_I5": child_independent,
        "child_E": child_cliques + child_independent,
        "child_source_distance": child_source,
        "child_target_distance": child_target,
        "child_agreement_breaks": child_breaks,
        "C5": cliques,
        "I5": independent,
        "E": cliques + independent,
        "distance_a": distance_a,
        "distance_b": distance_b,
        "agreement_breaks": final_breaks,
        "conflict_topology": topology,
        "checks": checks,
        "accepted": accepted,
        "ramsey_valid": cliques == 0 and independent == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--child", type=Path, required=True)
    parser.add_argument("--parent-a", type=Path, required=True)
    parser.add_argument("--parent-b", type=Path, required=True)
    parser.add_argument("--search-json", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = run(args)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        result = {
            "verifier": VERIFIER,
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
