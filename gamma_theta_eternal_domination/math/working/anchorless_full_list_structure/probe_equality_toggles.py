#!/usr/bin/env python3
"""Exploratory edge-addition probe around the equality control."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_a.core import (  # noqa: E402
    BitGraph,
    alpha,
    domination_number,
    eternal_fixed_point,
    theta,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repair-radius", type=int, default=0)
    parser.add_argument("--stop-after", type=int, default=20)
    arguments = parser.parse_args()

    base = BitGraph.from_graph6("Ksv`f\\knJVis")
    root = (1, 2, 3)
    target = 0
    root_mask = sum(1 << vertex for vertex in root)
    physical = base.complement().adj[target]
    missing_root_edges = [
        (anchor, vertex)
        for anchor in root
        for vertex in range(base.n)
        if physical >> vertex & 1 and not (base.adj[anchor] >> vertex & 1)
    ]

    all_pairs = list(itertools.combinations(range(base.n), 2))
    records = []
    tested = 0
    for additions in ((edge,) for edge in missing_root_edges):
        repair_pairs = [pair for pair in all_pairs if pair not in additions]
        for repair_count in range(arguments.repair_radius + 1):
            for repairs in itertools.combinations(repair_pairs, repair_count):
                tested += 1
                edits = tuple(additions) + tuple(repairs)
                adjacency = list(base.adj)
                for position, (u, v) in enumerate(edits):
                    if position < len(additions):
                        adjacency[u] |= 1 << v
                        adjacency[v] |= 1 << u
                    else:
                        adjacency[u] ^= 1 << v
                        adjacency[v] ^= 1 << u
                graph = BitGraph(base.n, tuple(adjacency))
                if alpha(graph) != 3 or domination_number(graph) != 3:
                    continue
                family = set(eternal_fixed_point(graph, 3).family)
                target_bit = 1 << target
                if not family or not all(
                    root_mask ^ (1 << anchor) ^ target_bit in family
                    for anchor in root
                ):
                    continue
                complement = graph.complement()
                spokes = [
                    complement.adj[target] & complement.adj[anchor]
                    for anchor in root
                ]
                anchorless = complement.adj[target]
                for spoke in spokes:
                    anchorless &= ~spoke
                if not anchorless:
                    continue
                records.append(
                    {
                        "graph6": graph.to_graph6(),
                        "additions": [list(edge) for edge in additions],
                        "repairs": [list(edge) for edge in repairs],
                        "family_size": len(family),
                        "theta": theta(graph),
                        "anchorless": [
                            vertex
                            for vertex in range(graph.n)
                            if anchorless >> vertex & 1
                        ],
                    }
                )
                if len(records) >= arguments.stop_after:
                    break
            if len(records) >= arguments.stop_after:
                break
        if len(records) >= arguments.stop_after:
            break

    print(
        json.dumps(
            {
                "base": base.to_graph6(),
                "missing_root_edges": missing_root_edges,
                "tested": tested,
                "records": records,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
