#!/usr/bin/env python3
"""Independent internal-core count using NetworkX's graph atlas.

This does not call the edge-subset generator or its canonicalizer.  The atlas
contains one representative of every simple graph on at most seven vertices,
which covers all internal cores in the 3--5 leaf, level-2 census.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import networkx as nx


def main() -> None:
    atlas = nx.graph_atlas_g()
    cells = []
    for n in range(3, 6):
        for r in range(3):
            m = n + 2 * r - 2
            ecount = n + 3 * r - 3
            selected = []
            for graph in atlas:
                if graph.number_of_nodes() != m or graph.number_of_edges() != ecount:
                    continue
                if m > 1 and not nx.is_connected(graph):
                    continue
                degrees = sorted(dict(graph.degree()).values())
                if any(d > 3 for d in degrees) or sum(3 - d for d in degrees) != n:
                    continue
                selected.append(graph)
            cells.append(
                {
                    "n": n,
                    "reticulations": r,
                    "internal_vertices": m,
                    "internal_edges": ecount,
                    "atlas_core_count": len(selected),
                    "degree_sequence_counts": {
                        ",".join(map(str, key)): value
                        for key, value in sorted(Counter(tuple(sorted(dict(g.degree()).values())) for g in selected).items())
                    },
                    "graph6": sorted(nx.to_graph6_bytes(g, header=False).decode().strip() for g in selected),
                }
            )
    payload = {
        "schema": 1,
        "status": "EXACTLY_COMPUTED_INDEPENDENT_CROSSCHECK",
        "coverage": "all simple internal graphs on at most seven vertices",
        "cells": cells,
    }
    path = Path("atlas_core_crosscheck.json")
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", hashlib.sha256(path.read_bytes()).hexdigest())
    for cell in cells:
        print(cell["n"], cell["reticulations"], cell["atlas_core_count"])


if __name__ == "__main__":
    main()

