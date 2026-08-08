#!/usr/bin/env python3
"""Discovery scan of every connected unweighted graph in the graph atlas.

The score is computed from the full labelled subset chains.  Floating-point
results are discovery evidence only; a positive score must be rebuilt by an
independent exact verifier.
"""

from __future__ import annotations

import argparse

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve


R = 1.5


def baseline(n: int, rule: str) -> float:
    if rule == "Bd":
        return 3.0 ** (n - 1) / (3.0**n - 2.0**n)
    return (n - 1.0) * 3.0 ** (n - 2) / (
        n * (3.0 ** (n - 1) - 2.0 ** (n - 1))
    )


def fixation(weights: np.ndarray, rule: str) -> tuple[float, float]:
    n = len(weights)
    degree = weights.sum(axis=1)
    kernel = weights / degree[:, None]
    full = (1 << n) - 1
    rows: list[int] = []
    columns: list[int] = []
    entries: list[float] = []
    rhs = np.zeros(full - 1)

    for state in range(1, full):
        row = state - 1
        changing = 0.0
        for target in range(n):
            target_mutant = bool(state & (1 << target))
            if rule == "Bd":
                rate = sum(
                    kernel[parent, target]
                    for parent in range(n)
                    if bool(state & (1 << parent)) != target_mutant
                )
                if not target_mutant:
                    rate *= R
            else:
                mutant = sum(
                    weights[parent, target]
                    for parent in range(n)
                    if state & (1 << parent)
                )
                resident = degree[target] - mutant
                denominator = R * mutant + resident
                rate = resident / denominator if target_mutant else R * mutant / denominator
            if not rate:
                continue
            changing += rate
            next_state = state ^ (1 << target)
            if next_state == full:
                rhs[row] += rate
            elif next_state:
                rows.append(row)
                columns.append(next_state - 1)
                entries.append(-rate)
        rows.append(row)
        columns.append(row)
        entries.append(changing)

    matrix = csr_matrix((entries, (rows, columns)), shape=(full - 1, full - 1))
    values = spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    rho = sum(values[(1 << vertex) - 1] for vertex in range(n)) / n
    return float(rho), residual


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=7)
    parser.add_argument("--top", type=int, default=30)
    args = parser.parse_args()
    records = []
    count = 0
    for atlas_index, graph in enumerate(nx.graph_atlas_g()):
        n = len(graph)
        if n < 2 or n > args.max_n or not nx.is_connected(graph):
            continue
        weights = nx.to_numpy_array(graph, dtype=float)
        bd, rb = fixation(weights, "Bd")
        db, rd = fixation(weights, "dB")
        x = bd / baseline(n, "Bd")
        y = db / baseline(n, "dB")
        score = (x + 2.0 * y) / 3.0
        records.append((score, x, y, atlas_index, n, graph.number_of_edges(), rb, rd))
        count += 1
    records.sort(reverse=True)
    for record in records[: args.top]:
        print("score={:.15g} x={:.15g} y={:.15g} atlas={} n={} m={} residuals={:.2g},{:.2g}".format(*record), flush=True)
    print(f"SCANNED {count}", flush=True)


if __name__ == "__main__":
    main()
