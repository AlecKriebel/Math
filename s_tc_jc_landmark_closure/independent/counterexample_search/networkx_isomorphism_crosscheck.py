#!/usr/bin/env python3
"""Independent labelled mixed-graph isomorphism cross-check.

Arrowheads are encoded by a coloured incidence gadget, so this implementation
does not call the clean-room brute-force canonicalizer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import networkx as nx

from audit_io import load_json


def incidence_graph(record: dict) -> nx.Graph:
    graph = nx.Graph()
    n = record["n"]
    retics = set(record["reticulations"])
    for v in range(n + record["m"]):
        if v < n:
            color = f"leaf:{v}"
        elif v in retics:
            color = "reticulation"
        else:
            color = "tree"
        graph.add_node(("v", v), color=color)
    for index, item in enumerate(sorted(record["edges"], key=lambda e: (min(e["u"], e["v"]), max(e["u"], e["v"])))):
        center = ("e", index)
        graph.add_node(center, color="edge")
        heads = set(item["arrowheads"])
        for side, endpoint in enumerate((item["u"], item["v"])):
            incidence = ("i", index, side)
            graph.add_node(incidence, color="arrowhead" if endpoint in heads else "plain")
            graph.add_edge(("v", endpoint), incidence)
            graph.add_edge(incidence, center)
    return graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--max-n", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = load_json(args.census)
    records = [t for t in data["topologies"] if t["n"] <= args.max_n]
    buckets = defaultdict(list)
    for index, record in enumerate(records):
        graph = incidence_graph(record)
        digest = nx.weisfeiler_lehman_graph_hash(graph, node_attr="color", iterations=6)
        buckets[(record["n"], len(record["reticulations"]), digest)].append((index, graph))

    comparisons = 0
    duplicates = []
    node_match = nx.algorithms.isomorphism.categorical_node_match("color", None)
    for bucket in buckets.values():
        for i in range(len(bucket)):
            for j in range(i + 1, len(bucket)):
                comparisons += 1
                if nx.is_isomorphic(bucket[i][1], bucket[j][1], node_match=node_match):
                    duplicates.append([bucket[i][0], bucket[j][0]])
    assert not duplicates, duplicates[:5]
    payload = {
        "schema": 1,
        "status": "EXACTLY_COMPUTED_INDEPENDENT_CROSSCHECK",
        "records_checked": len(records),
        "WL_buckets": len(buckets),
        "exact_GraphMatcher_comparisons_within_buckets": comparisons,
        "isomorphic_duplicate_pairs": duplicates,
        "conclusion": "No two released bounded topology records are isomorphic as leaf-labelled arrowhead-preserving mixed graphs.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", hashlib.sha256(args.output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
