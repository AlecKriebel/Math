#!/usr/bin/env python3
"""Relabel/complement/parser audit for a candidate graph."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from graph_io import complement, encode_graph6, read_graph, validate_simple  # noqa: E402

from exhaustive_verify import count_forbidden  # noqa: E402


def relabel(adjacency: list[int], permutation: list[int]) -> list[int]:
    """permutation[old] is the new label."""
    n = len(adjacency)
    result = [0] * n
    for old_left in range(n):
        for old_right in range(old_left + 1, n):
            if (adjacency[old_left] >> old_right) & 1:
                new_left = permutation[old_left]
                new_right = permutation[old_right]
                result[new_left] |= 1 << new_right
                result[new_right] |= 1 << new_left
    return result


def cpp_result(binary: Path, graph: Path) -> dict:
    run = subprocess.run(
        [str(binary), str(graph), "--k", "5"],
        text=True,
        capture_output=True,
        check=False,
    )
    if run.returncode not in (0, 1):
        raise RuntimeError(run.stderr)
    return json.loads(run.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("--json-copy", type=Path)
    parser.add_argument("--seed", type=int, default=730055)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--cpp", type=Path, default=ROOT / "build" / "bitset_verify"
    )
    args = parser.parse_args()

    adjacency = read_graph(args.graph)
    validate_simple(adjacency)
    parser_match = None
    if args.json_copy is not None:
        parser_match = adjacency == read_graph(args.json_copy)
        if not parser_match:
            raise AssertionError("graph6 and JSON parser paths disagree")

    rng = random.Random(args.seed)
    permutation = list(range(len(adjacency)))
    rng.shuffle(permutation)
    transformed = {
        "original": adjacency,
        "complement": complement(adjacency),
        "relabel": relabel(adjacency, permutation),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    reports = {}
    for name, graph in transformed.items():
        path = args.output_dir / f"{name}.g6"
        path.write_text(encode_graph6(graph) + "\n", encoding="ascii")
        clique_count, independent_count = count_forbidden(graph, 5)
        cpp = cpp_result(args.cpp, path)
        if cpp["clique_k_found"] != (clique_count > 0):
            raise AssertionError(f"C++ clique disagreement for {name}")
        if cpp["independent_k_found"] != (independent_count > 0):
            raise AssertionError(f"C++ independent disagreement for {name}")
        reports[name] = {
            "path": str(path),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "C5": clique_count,
            "I5": independent_count,
            "E": clique_count + independent_count,
            "edge_count": sum(row.bit_count() for row in graph) // 2,
            "cpp_verifier": cpp,
        }
    original = reports["original"]
    if (reports["relabel"]["C5"], reports["relabel"]["I5"]) != (
        original["C5"],
        original["I5"],
    ):
        raise AssertionError("relabeling changed forbidden-set counts")
    if (reports["complement"]["C5"], reports["complement"]["I5"]) != (
        original["I5"],
        original["C5"],
    ):
        raise AssertionError("complement did not swap forbidden-set counts")
    print(
        json.dumps(
            {
                "audit": "adversarial_relabel_complement_parser_v1",
                "seed": args.seed,
                "permutation_old_to_new": permutation,
                "json_graph6_parser_match": parser_match,
                "reports": reports,
                "status": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
