#!/usr/bin/env python3
"""Sparse numerical falsification search for the r=3/2 product conjecture.

This is discovery code only.  It deletes ineffective transitions exactly at
the rate level and solves the two transient subset systems with sparse LU.
Every apparent violation must be rationalized and checked independently.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


R = 1.5


def baseline(n, rule):
    if rule == "Bd":
        return (1 - 1 / R) / (1 - R ** (-n))
    return (n - 1) / n * (1 - 1 / R) / (1 - R ** (-(n - 1)))


def fixation(weights, rule):
    n = len(weights)
    degree = weights.sum(axis=1)
    if np.min(degree) <= 0:
        raise ValueError("isolated vertex")
    full = (1 << n) - 1
    size = full - 1
    rows, cols, data = [], [], []
    rhs = np.zeros(size)
    for state in range(1, full):
        row = state - 1
        flips = []
        total = 0.0
        mutant = np.array([(state >> i) & 1 for i in range(n)], dtype=bool)
        for target in range(n):
            if rule == "Bd":
                incoming = weights[:, target] / degree
                mutant_mass = incoming[mutant].sum()
                resident_mass = incoming[~mutant].sum()
                rate = resident_mass if mutant[target] else R * mutant_mass
            else:
                mutant_mass = weights[target, mutant].sum()
                resident_mass = degree[target] - mutant_mass
                denominator = R * mutant_mass + resident_mass
                rate = (
                    resident_mass / denominator
                    if mutant[target]
                    else R * mutant_mass / denominator
                )
            if rate > 0:
                flips.append((state ^ (1 << target), rate))
                total += rate
        if total <= 0:
            raise ValueError("disconnected")
        rows.append(row)
        cols.append(row)
        data.append(1.0)
        for target, rate in flips:
            probability = rate / total
            if target == full:
                rhs[row] += probability
            elif target:
                rows.append(row)
                cols.append(target - 1)
                data.append(-probability)
    matrix = coo_matrix((data, (rows, cols)), shape=(size, size)).tocsc()
    solution = spsolve(matrix, rhs)
    residual = np.max(np.abs(matrix @ solution - rhs))
    if residual > 1e-8:
        raise FloatingPointError(residual)
    return sum(solution[(1 << i) - 1] for i in range(n)) / n


def connected(weights):
    n = len(weights)
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for j in np.flatnonzero(weights[i] > 0):
            if int(j) not in seen:
                seen.add(int(j))
                stack.append(int(j))
    return len(seen) == n


def matrix_from_logs(n, edges, logs):
    weights = np.zeros((n, n))
    centered = logs - np.mean(logs)
    for (i, j), value in zip(edges, np.exp(centered)):
        weights[i, j] = weights[j, i] = value
    return weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--evaluations", type=int, default=500)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--span", type=float, default=8.0)
    parser.add_argument("--edge-probability", type=float, default=0.55)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    all_edges = list(itertools.combinations(range(args.n), 2))
    target = baseline(args.n, "Bd") * baseline(args.n, "dB")
    best = (-np.inf, None, None, None)
    for evaluation in range(args.evaluations):
        while True:
            active = [edge for edge in all_edges if rng.random() < args.edge_probability]
            if len(active) < args.n - 1:
                continue
            logs = rng.uniform(-args.span, args.span, len(active))
            weights = matrix_from_logs(args.n, active, logs)
            if connected(weights):
                break
        try:
            bd = fixation(weights, "Bd")
            db = fixation(weights, "dB")
        except (ValueError, FloatingPointError):
            continue
        excess = bd * db - target
        if excess > best[0]:
            best = (excess, weights.copy(), bd, db)
            print(
                evaluation,
                "best excess",
                f"{excess:.17g}",
                "Bd",
                f"{bd:.12g}",
                "dB",
                f"{db:.12g}",
                flush=True,
            )
        if excess > 1e-9:
            print("APPARENT VIOLATION")
            print(repr(weights.tolist()))
            return
    print("NO VIOLATION; best", best[0])
    print(repr(best[1].tolist()) if best[1] is not None else None)


if __name__ == "__main__":
    main()
