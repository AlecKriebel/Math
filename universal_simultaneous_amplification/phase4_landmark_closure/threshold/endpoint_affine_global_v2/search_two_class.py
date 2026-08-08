#!/usr/bin/env python3
"""Full lumped-chain search for two equitable weighted vertex classes.

Class A and B have unit-complete internal supports with weights ``u,v`` and
complete cross support with weight ``w``.  The automorphism orbits are the
two mutant counts, so the chain below is exact.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

from search_graph_atlas import baseline


R = 1.5


def fixation(a: int, b: int, logs, rule: str) -> tuple[float, float]:
    values = np.exp(np.asarray((logs[0], logs[1], 0.0)) - np.mean((logs[0], logs[1], 0.0)))
    u, v, w = map(float, values)
    d_a = (a - 1) * u + b * w
    d_b = (b - 1) * v + a * w
    states = [(i, j) for i in range(a + 1) for j in range(b + 1) if (i, j) not in ((0, 0), (a, b))]
    index = {state: row for row, state in enumerate(states)}
    rows, columns, entries = [], [], []
    rhs = np.zeros(len(states))

    for state, row in index.items():
        i, j = state
        changes = []
        if rule == "Bd":
            if i < a:
                changes.append(((i + 1, j), R * (a - i) * (i * u / d_a + j * w / d_b)))
            if i:
                changes.append(((i - 1, j), i * ((a - i) * u / d_a + (b - j) * w / d_b)))
            if j < b:
                changes.append(((i, j + 1), R * (b - j) * (j * v / d_b + i * w / d_a)))
            if j:
                changes.append(((i, j - 1), j * ((b - j) * v / d_b + (a - i) * w / d_a)))
        else:
            if i < a:
                mutant = i * u + j * w
                resident = (a - i - 1) * u + (b - j) * w
                changes.append(((i + 1, j), (a - i) * R * mutant / (R * mutant + resident)))
            if i:
                mutant = (i - 1) * u + j * w
                resident = (a - i) * u + (b - j) * w
                changes.append(((i - 1, j), i * resident / (R * mutant + resident)))
            if j < b:
                mutant = j * v + i * w
                resident = (b - j - 1) * v + (a - i) * w
                changes.append(((i, j + 1), (b - j) * R * mutant / (R * mutant + resident)))
            if j:
                mutant = (j - 1) * v + i * w
                resident = (b - j) * v + (a - i) * w
                changes.append(((i, j - 1), j * resident / (R * mutant + resident)))

        changing = sum(rate for _, rate in changes if rate)
        rows.append(row); columns.append(row); entries.append(changing)
        for target, rate in changes:
            if not rate:
                continue
            if target == (a, b):
                rhs[row] += rate
            elif target != (0, 0):
                rows.append(row); columns.append(index[target]); entries.append(-rate)
    matrix = csr_matrix((entries, (rows, columns)), shape=(len(states), len(states)))
    h = spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ h - rhs)))
    rho = (a * h[index[(1, 0)]] + b * h[index[(0, 1)]]) / (a + b)
    return float(rho), residual


def score(a: int, b: int, logs):
    bd, rb = fixation(a, b, logs, "Bd")
    db, rd = fixation(a, b, logs, "dB")
    n = a + b
    x = bd / baseline(n, "Bd")
    y = db / baseline(n, "dB")
    return (x + 2 * y) / 3, x, y, max(rb, rd)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=60)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260808)
    args = parser.parse_args()
    best = None
    for n in range(4, args.max_n + 1):
        for a in range(1, n // 2 + 1):
            b = n - a

            def loss(logs):
                value, _, _, residual = score(a, b, logs)
                return -value if residual < 1e-7 and np.isfinite(value) else 10.0

            result = differential_evolution(
                loss, [(-12, 12), (-12, 12)], maxiter=args.iterations,
                popsize=6, polish=False, seed=args.seed + 101 * n + a, tol=1e-8,
            )
            polished = minimize(loss, result.x, method="Nelder-Mead", options={"maxiter": 800, "xatol": 1e-10, "fatol": 1e-12})
            record = (*score(a, b, polished.x), n, a, b, tuple(polished.x))
            if best is None or record[0] > best[0]:
                best = record
                print("BEST", best, flush=True)
            if record[0] > 1.0000001:
                print("VIOLATION", record, flush=True)
        if n % 5 == 0:
            print(f"PROGRESS n={n} best={best[0]:.14g}", flush=True)


if __name__ == "__main__":
    main()
