#!/usr/bin/env python3
"""Exact count-lumped hostile search for three equitable weighted classes."""

from __future__ import annotations

import argparse
from itertools import product

import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

from search_graph_atlas import baseline


R = 1.5
PAIRS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))


def matrix_from_logs(logs):
    logs = np.asarray(logs, dtype=float)
    logs -= logs.mean()
    values = np.exp(np.clip(logs, -20, 20))
    weights = np.zeros((3, 3))
    for (a, b), value in zip(PAIRS, values):
        weights[a, b] = weights[b, a] = value
    return weights


def fixation(sizes, logs, rule):
    weights = matrix_from_logs(logs)
    degrees = np.array([
        sum((sizes[t] - int(s == t)) * weights[s, t] for t in range(3))
        for s in range(3)
    ])
    extinct = (0, 0, 0)
    fixed = tuple(sizes)
    states = [state for state in product(*(range(size + 1) for size in sizes)) if state not in (extinct, fixed)]
    index = {state: row for row, state in enumerate(states)}
    rows, columns, entries = [], [], []
    rhs = np.zeros(len(states))
    for state, row in index.items():
        changes = []
        for target_class in range(3):
            count = state[target_class]
            if count < sizes[target_class]:
                if rule == "Bd":
                    incoming = sum(
                        state[source] * weights[source, target_class] / degrees[source]
                        for source in range(3)
                    )
                    rate = R * (sizes[target_class] - count) * incoming
                else:
                    mutant = sum(state[source] * weights[target_class, source] for source in range(3))
                    resident = degrees[target_class] - mutant
                    rate = (sizes[target_class] - count) * R * mutant / (R * mutant + resident)
                updated = list(state); updated[target_class] += 1
                changes.append((tuple(updated), rate))
            if count:
                if rule == "Bd":
                    incoming = sum(
                        (sizes[source] - state[source]) * weights[source, target_class] / degrees[source]
                        for source in range(3)
                    )
                    rate = count * incoming
                else:
                    mutant = sum(state[source] * weights[target_class, source] for source in range(3)) - weights[target_class, target_class]
                    resident = degrees[target_class] - mutant
                    rate = count * resident / (R * mutant + resident)
                updated = list(state); updated[target_class] -= 1
                changes.append((tuple(updated), rate))
        changing = sum(rate for _, rate in changes if rate)
        rows.append(row); columns.append(row); entries.append(changing)
        for target, rate in changes:
            if not rate:
                continue
            if target == fixed:
                rhs[row] += rate
            elif target != extinct:
                rows.append(row); columns.append(index[target]); entries.append(-rate)
    matrix = csr_matrix((entries, (rows, columns)), shape=(len(states), len(states)))
    h = spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ h - rhs)))
    n = sum(sizes)
    rho = 0.0
    for cls, size in enumerate(sizes):
        singleton = tuple(int(candidate == cls) for candidate in range(3))
        rho += size * h[index[singleton]] / n
    return float(rho), residual


def score(sizes, logs):
    bd, rb = fixation(sizes, logs, "Bd")
    db, rd = fixation(sizes, logs, "dB")
    n = sum(sizes)
    x = bd / baseline(n, "Bd")
    y = db / baseline(n, "dB")
    return (x + 2 * y) / 3, x, y, max(rb, rd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sizes", nargs=3, type=int)
    parser.add_argument("--iterations", type=int, default=200)
    parser.add_argument("--restarts", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260808)
    args = parser.parse_args()
    sizes = tuple(args.sizes)
    best = None
    for restart in range(args.restarts):
        def loss(logs):
            value, _, _, residual = score(sizes, logs)
            return -value if residual < 1e-7 and np.isfinite(value) else 10.0
        result = differential_evolution(
            loss, [(-12, 12)] * 6, maxiter=args.iterations, popsize=8,
            seed=args.seed + 1009 * restart, polish=False, tol=1e-9,
        )
        polished = minimize(loss, result.x, method="Powell", bounds=[(-12, 12)] * 6,
                            options={"maxiter": 2000, "ftol": 1e-13, "xtol": 1e-10})
        record = (*score(sizes, polished.x), polished.x - np.mean(polished.x))
        if best is None or record[0] > best[0]:
            best = record
        print("RESULT", restart, record, flush=True)
    print("BEST", sizes, best)


if __name__ == "__main__":
    main()
