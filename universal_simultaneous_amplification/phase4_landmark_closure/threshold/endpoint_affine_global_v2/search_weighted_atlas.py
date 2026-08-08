#!/usr/bin/env python3
"""Random-weight discovery scan on every connected graph-atlas support."""

from __future__ import annotations

import argparse
import heapq

import networkx as nx
import numpy as np

from search_graph_atlas import baseline, fixation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=7)
    parser.add_argument("--samples", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20260808)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    scales = (0.35, 1.0, 2.5, 5.0)
    best = []
    count = 0
    for atlas_index, graph in enumerate(nx.graph_atlas_g()):
        n = len(graph)
        if n < 3 or n > args.max_n or not nx.is_connected(graph):
            continue
        edges = tuple(graph.edges())
        for scale in scales:
            for sample in range(args.samples):
                logs = rng.normal(0.0, scale, len(edges))
                logs -= logs.mean()
                weights = np.zeros((n, n))
                for (a, b), value in zip(edges, np.exp(logs)):
                    weights[a, b] = weights[b, a] = value
                bd, rb = fixation(weights, "Bd")
                db, rd = fixation(weights, "dB")
                if max(rb, rd) > 1e-7:
                    continue
                x = bd / baseline(n, "Bd")
                y = db / baseline(n, "dB")
                score = (x + 2 * y) / 3
                record = (score, x, y, atlas_index, scale, sample, tuple(logs))
                if len(best) < 30:
                    heapq.heappush(best, record)
                elif score > best[0][0]:
                    heapq.heapreplace(best, record)
                if score > 1.0000001:
                    print("VIOLATION", record, flush=True)
                count += 1
        if atlas_index % 100 == 0:
            print(f"PROGRESS atlas={atlas_index} cases={count} best={max(best)[0]:.12g}", flush=True)
    for record in sorted(best, reverse=True):
        print("TOP", record, flush=True)
    print(f"SCANNED {count}", flush=True)


if __name__ == "__main__":
    main()
