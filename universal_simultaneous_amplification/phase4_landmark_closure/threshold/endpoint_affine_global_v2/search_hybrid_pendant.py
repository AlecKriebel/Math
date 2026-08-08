#!/usr/bin/env python3
"""Discovery search combining the weak-module dB gain with hub pendants.

Classes are: a strong two-clique A, one hub H, the remaining B-clique core
C, and identical leaves L.  All A--B edges are weak, H+C form a unit clique,
and each leaf is adjacent only to H.  The four mutant counts are exact
automorphism orbits.
"""

from __future__ import annotations

import argparse
from itertools import product

import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

from search_graph_atlas import baseline


R = 1.5


def graph_data(core: int, leaves: int, logs):
    # v=1 fixes scale; variables are u, epsilon, pendant weight.
    u, epsilon, pendant = np.exp(np.clip(logs, -25, 25))
    sizes = (2, 1, core, leaves)
    weights = np.zeros((4, 4))
    weights[0, 0] = u
    weights[0, 1] = weights[1, 0] = epsilon
    weights[0, 2] = weights[2, 0] = epsilon
    weights[1, 2] = weights[2, 1] = 1.0
    weights[2, 2] = 1.0
    weights[1, 3] = weights[3, 1] = pendant
    return sizes, weights


def fixation(core, leaves, logs, rule):
    sizes, weights = graph_data(core, leaves, logs)
    classes = len(sizes)
    degrees = np.array([
        sum((sizes[t] - int(s == t)) * weights[s, t] for t in range(classes))
        for s in range(classes)
    ])
    extinct = (0,) * classes
    fixed = sizes
    states = [state for state in product(*(range(size + 1) for size in sizes)) if state not in (extinct, fixed)]
    index = {state: row for row, state in enumerate(states)}
    rows, columns, entries = [], [], []
    rhs = np.zeros(len(states))
    for state, row in index.items():
        changes = []
        for target_class in range(classes):
            count = state[target_class]
            if count < sizes[target_class]:
                if rule == "Bd":
                    mass = sum(state[source] * weights[source, target_class] / degrees[source] for source in range(classes))
                    rate = R * (sizes[target_class] - count) * mass
                else:
                    mutant = sum(state[source] * weights[target_class, source] for source in range(classes))
                    resident = degrees[target_class] - mutant
                    rate = (sizes[target_class] - count) * R * mutant / (R * mutant + resident)
                updated = list(state); updated[target_class] += 1
                changes.append((tuple(updated), rate))
            if count:
                if rule == "Bd":
                    mass = sum((sizes[source] - state[source]) * weights[source, target_class] / degrees[source] for source in range(classes))
                    rate = count * mass
                else:
                    mutant = sum(state[source] * weights[target_class, source] for source in range(classes)) - weights[target_class, target_class]
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
        if not size:
            continue
        singleton = tuple(int(candidate == cls) for candidate in range(classes))
        rho += size * h[index[singleton]] / n
    return float(rho), residual


def score(core, leaves, logs):
    bd, rb = fixation(core, leaves, logs, "Bd")
    db, rd = fixation(core, leaves, logs, "dB")
    n = core + leaves + 3
    x = bd / baseline(n, "Bd")
    y = db / baseline(n, "dB")
    return min(x, y), x, y, (x + 2 * y) / 3, max(rb, rd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=int, default=19)
    parser.add_argument("--leaves", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=80)
    parser.add_argument("--restarts", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260808)
    args = parser.parse_args()
    best = None
    for restart in range(args.restarts):
        def loss(logs):
            value, _, _, _, residual = score(args.core, args.leaves, logs)
            return -value if residual < 1e-7 and np.isfinite(value) else 10
        result = differential_evolution(
            loss, [(0, 10), (-14, 0), (-8, 8)], maxiter=args.iterations,
            popsize=6, seed=args.seed + 1009 * restart, polish=False, tol=1e-8,
        )
        polished = minimize(loss, result.x, method="Powell", bounds=[(0, 10), (-14, 0), (-8, 8)],
                            options={"maxiter": 1000, "ftol": 1e-12, "xtol": 1e-9})
        record = (*score(args.core, args.leaves, polished.x), polished.x)
        if best is None or record[0] > best[0]:
            best = record
        print("RESULT", restart, record, flush=True)
    print("BEST", best)


if __name__ == "__main__":
    main()
