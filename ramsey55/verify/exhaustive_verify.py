#!/usr/bin/env python3
"""Verifier 1: exhaustively inspect every k-subset and all of its pairs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import read_graph, validate_simple  # noqa: E402


def count_forbidden(adjacency: list[int], k: int = 5) -> tuple[int, int]:
    """Count k-cliques and independent k-sets by direct subset enumeration."""
    validate_simple(adjacency)
    clique_count = 0
    independent_count = 0
    for subset in itertools.combinations(range(len(adjacency)), k):
        all_edges = True
        no_edges = True
        for offset, left in enumerate(subset):
            for right in subset[offset + 1 :]:
                edge = (adjacency[left] >> right) & 1
                if edge:
                    no_edges = False
                else:
                    all_edges = False
        clique_count += int(all_edges)
        independent_count += int(no_edges)
    return clique_count, independent_count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("--line", type=int, default=1)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    adjacency = read_graph(args.graph, args.line)
    clique_count, independent_count = count_forbidden(adjacency, args.k)
    edge_count = sum(neighbors.bit_count() for neighbors in adjacency) // 2
    degrees = sorted(neighbors.bit_count() for neighbors in adjacency)
    result = {
        "verifier": "python_exhaustive_k_subset_pairs_v1",
        "input": str(args.graph),
        "input_sha256": hashlib.sha256(args.graph.read_bytes()).hexdigest(),
        "line": args.line,
        "n": len(adjacency),
        "k": args.k,
        "edge_count": edge_count,
        "degree_sequence": degrees,
        "clique_count": clique_count,
        "independent_count": independent_count,
        "objective": clique_count + independent_count,
        "valid": clique_count == 0 and independent_count == 0,
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
