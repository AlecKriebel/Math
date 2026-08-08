#!/usr/bin/env python3
"""Hostile numerical search for the full-start transient midpoint inequality.

Discovery code only.  An apparent negative value must be rationalized and
checked independently.  The state space has 2^n-1 states, so defaults are
deliberately modest.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.linalg import expm
from scipy.optimize import differential_evolution


R = 1.5
A = R - 1.0


def dual_generator(weights: np.ndarray, reversed_arrows: bool) -> np.ndarray:
    n = len(weights)
    full = (1 << n) - 1
    degree = weights.sum(axis=1)
    p = weights / degree[:, None]
    generator = np.zeros((full, full))
    for state in range(1, full + 1):
        row = state - 1
        for target in range(n):
            if not (state >> target) & 1:
                continue
            for source in range(n):
                rate = p[target, source] if reversed_arrows else p[source, target]
                if not rate:
                    continue
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                if neutral != state:
                    generator[row, neutral - 1] += rate
                if selective != state:
                    generator[row, selective - 1] += A * rate
        generator[row, row] = -generator[row].sum()
    return generator


def graph_from_logs(n: int, logs: np.ndarray) -> np.ndarray:
    weights = np.zeros((n, n))
    centered = logs - logs.mean()
    for (i, j), value in zip(itertools.combinations(range(n), 2), np.exp(centered)):
        weights[i, j] = weights[j, i] = value
    return weights


def gap(weights: np.ndarray, time: float) -> float:
    left = dual_generator(weights, False)
    reverse = dual_generator(weights, True)
    midpoint = (left + reverse) / 2
    n = len(weights)
    size = np.array([state.bit_count() for state in range(1, 1 << n)], float)
    start = np.zeros(len(size))
    start[-1] = 1.0
    return float(
        2 * start @ expm(time * midpoint) @ size
        - start @ expm(time * left) @ size
        - start @ expm(time * reverse) @ size
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--span", type=float, default=14.0)
    parser.add_argument("--iterations", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20260807)
    args = parser.parse_args()
    edge_count = args.n * (args.n - 1) // 2
    best: list[object] = [float("inf"), None, None]

    def objective(parameters: np.ndarray) -> float:
        logs = parameters[:-1]
        time = float(np.exp(parameters[-1]))
        weights = graph_from_logs(args.n, logs)
        value = gap(weights, time)
        if np.isfinite(value) and value < best[0]:
            best[:] = [value, weights.copy(), time]
        return value if np.isfinite(value) else 1e3

    bounds = [(-args.span, args.span)] * edge_count + [(-8.0, 8.0)]
    differential_evolution(
        objective,
        bounds,
        seed=args.seed,
        maxiter=args.iterations,
        popsize=8,
        polish=True,
        workers=1,
    )
    print("minimum transient midpoint gap", best[0])
    print("time", best[2])
    print("weights", best[1].tolist() if best[1] is not None else None)
    if best[0] < -1e-8:
        print("APPARENT COUNTEREXAMPLE -- exactification required")
    else:
        print("NO VIOLATION FOUND -- numerical evidence only")


if __name__ == "__main__":
    main()
