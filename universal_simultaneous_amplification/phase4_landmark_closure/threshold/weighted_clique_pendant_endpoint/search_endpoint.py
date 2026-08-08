#!/usr/bin/env python3
"""Sparse endpoint search for weighted clique--pendant graphs."""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

from model import absorbing_states, complete_baseline, moves, states


R = 1.5


def fixation(rule: str, c: int, m: int, w: float) -> float:
    extinct, fixed = absorbing_states(c, m)
    transient = [s for s in states(c, m) if s not in (extinct, fixed)]
    index = {s: k for k, s in enumerate(transient)}
    rows, cols, data = [], [], []
    rhs = np.zeros(len(transient))
    for row, state in enumerate(transient):
        outgoing = moves(rule, state, c, m, R, w)
        rows.append(row)
        cols.append(row)
        data.append(sum(outgoing.values()))
        for target, probability in outgoing.items():
            if target == fixed:
                rhs[row] += probability
            elif target != extinct:
                rows.append(row)
                cols.append(index[target])
                data.append(-probability)
    matrix = coo_matrix((data, (rows, cols)), shape=(len(transient),) * 2).tocsr()
    answer = spsolve(matrix, rhs)
    n = c + m + 1
    rho = (
        answer[index[(1, 0, 0)]]
        + c * answer[index[(0, 1, 0)]]
        + m * answer[index[(0, 0, 1)]]
    ) / n
    return float(rho)


def ratios(c: int, m: int, w: float) -> tuple[float, float, float]:
    n = c + m + 1
    x = fixation("Bd", c, m, w) / complete_baseline("Bd", n, R)
    y = fixation("dB", c, m, w) / complete_baseline("dB", n, R)
    return x, y, min(x, y)


def optimize(c: int, m: int, lo: float, hi: float):
    # A coarse scan protects against multiple local maxima; polish every local
    # contender in log w.
    grid = np.linspace(lo, hi, 61)
    vals = np.array([ratios(c, m, math.exp(z))[2] for z in grid])
    candidates = []
    for k in range(1, len(grid) - 1):
        if vals[k] >= vals[k - 1] and vals[k] >= vals[k + 1]:
            ans = minimize_scalar(
                lambda z: -ratios(c, m, math.exp(z))[2],
                bounds=(grid[k - 1], grid[k + 1]),
                method="bounded",
                options={"xatol": 1e-9},
            )
            candidates.append((math.exp(ans.x),) + ratios(c, m, math.exp(ans.x)))
    candidates.extend(
        [
            (math.exp(lo),) + ratios(c, m, math.exp(lo)),
            (math.exp(hi),) + ratios(c, m, math.exp(hi)),
        ]
    )
    return max(candidates, key=lambda row: row[-1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=50)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--log-w-min", type=float, default=-9.21)
    parser.add_argument("--log-w-max", type=float, default=9.21)
    parser.add_argument("--top", type=int, default=30)
    args = parser.parse_args()
    results = []
    for n in range(args.min_n, args.max_n + 1):
        for m in range(1, n - 1):
            c = n - m - 1
            row = optimize(c, m, args.log_w_min, args.log_w_max)
            results.append((row[-1], c, m, *row[:-1]))
        best = max(results, key=lambda row: row[0])
        print(
            f"through n={n}: M={best[0]:.12f} c={best[1]} m={best[2]} "
            f"w={best[3]:.9g} Bd={best[4]:.12f} dB={best[5]:.12f}",
            flush=True,
        )
    print("\nTOP")
    for M, c, m, w, x, y in sorted(results, reverse=True)[: args.top]:
        print(f"M={M:.15f} c={c} m={m} w={w:.12g} Bd={x:.15f} dB={y:.15f}")


if __name__ == "__main__":
    main()
