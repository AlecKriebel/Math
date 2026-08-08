#!/usr/bin/env python3
"""Exact r=2 audit of every connected unweighted graph through order seven.

This is a finite hostile screen, not a universal theorem.  It evaluates each
unlabelled connected support in NetworkX's graph atlas using the independent
FLINT absorbing-chain solver in ``exact_fixation.py``.
"""

from __future__ import annotations

import networkx as nx

from exact_fixation import Q, as_float, baseline, fixation


def weight_matrix(graph: nx.Graph):
    n = len(graph)
    return [
        [Q(int(u != v and graph.has_edge(u, v))) for v in range(n)]
        for u in range(n)
    ]


def edge_code(graph: nx.Graph) -> str:
    return ",".join(f"{u}-{v}" for u, v in sorted(graph.edges()))


def main() -> None:
    atlas = nx.graph_atlas_g()
    total = 0
    for n in range(2, 8):
        graphs = [
            (atlas_id, graph)
            for atlas_id, graph in enumerate(atlas)
            if len(graph) == n and nx.is_connected(graph)
        ]
        best_db = None
        best_sim = None
        db_violations = 0
        simultaneous = 0
        equality = 0
        for atlas_id, graph in graphs:
            weights = weight_matrix(graph)
            db_ratio = fixation(weights, "dB") / baseline(n, "dB")
            bd_ratio = fixation(weights, "Bd") / baseline(n, "Bd")
            minimum = min(db_ratio, bd_ratio)
            record = (db_ratio, bd_ratio, atlas_id, edge_code(graph))
            sim_record = (minimum, db_ratio, bd_ratio, atlas_id, edge_code(graph))
            if best_db is None or db_ratio > best_db[0]:
                best_db = record
            if best_sim is None or minimum > best_sim[0]:
                best_sim = sim_record
            db_violations += db_ratio > 1
            simultaneous += db_ratio > 1 and bd_ratio > 1
            equality += db_ratio == 1
        assert best_db is not None and best_sim is not None
        assert db_violations == 0
        assert simultaneous == 0
        # The complete support is present and attains equality.
        assert best_db[0] == 1
        assert best_sim[0] == 1
        total += len(graphs)
        print(
            f"n={n}: {len(graphs)} connected supports PASS; "
            f"dB equalities={equality}; max dB={as_float(best_db[0]):.17g}; "
            f"max simultaneous minimum={as_float(best_sim[0]):.17g}"
        )
        print(f"  dB maximizer atlas={best_db[2]} edges={best_db[3]}")
        print(f"  M maximizer atlas={best_sim[3]} edges={best_sim[4]}")
    assert total == 995
    print(f"EXACT FINITE ATLAS PASS: {total} connected unweighted graphs, 2<=n<=7")
    print("No dB or simultaneous r=2 violation; finite evidence only.")


if __name__ == "__main__":
    main()
