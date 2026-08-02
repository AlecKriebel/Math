#!/usr/bin/env python3
"""Enumerate all connected unweighted graphs of order at most seven.

Numerical discovery only.  NetworkX's graph atlas contains one representative
of every unlabeled graph through order seven.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import networkx as nx
import numpy as np


PARENT = pathlib.Path(__file__).resolve().parents[1]
DB_MAX = PARENT / "db_maximizer"
sys.path.insert(0, str(DB_MAX))
from search_db import baseline, baseline_bd, fixation, fixation_bd  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=7)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    r = 1.5
    target = baseline(args.n, r) + baseline_bd(args.n, r)
    all_graphs = [
        graph
        for graph in nx.graph_atlas_g()
        if len(graph) == args.n and nx.is_connected(graph)
    ]
    stop = None if not args.limit else args.start + args.limit
    graphs = all_graphs[args.start:stop]
    best = (-np.inf, None, None)
    simultaneous = []
    for number, graph in enumerate(graphs):
        weights = nx.to_numpy_array(graph)
        bd, _, _ = fixation_bd(weights, r)
        db, _, _ = fixation(weights, r)
        excess = bd + db - target
        if excess > best[0]:
            best = (excess, (bd, db), graph.copy())
        if bd > baseline_bd(args.n, r) + 1e-12 and db > baseline(args.n, r) + 1e-12:
            simultaneous.append((number, bd, db, graph.copy()))
    print("order", args.n, "chunk", args.start, args.start + len(graphs),
          "of", len(all_graphs))
    print("best excess", best[0], "Bd,dB", best[1])
    print("best edges", sorted(best[2].edges()))
    print("simultaneous count", len(simultaneous))


if __name__ == "__main__":
    main()
