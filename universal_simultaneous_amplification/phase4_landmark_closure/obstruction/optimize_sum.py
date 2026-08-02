#!/usr/bin/env python3
"""Numerically stress-test the conjectured Bd+dB fixation sum inequality.

This is a discovery aid, not part of the exact certificate package.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import differential_evolution, minimize

from search_random import baseline, fixation


def weights_from_logs(order: int, logs: np.ndarray) -> np.ndarray:
    weights = np.zeros((order, order))
    edges = list(itertools.combinations(range(order), 2))
    # Remove the irrelevant global scale.
    centered = logs - logs.mean()
    for (i, j), value in zip(edges, np.exp(centered), strict=True):
        weights[i, j] = weights[j, i] = value
    return weights


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--r", type=float, default=1.5)
    parser.add_argument("--span", type=float, default=12.0)
    parser.add_argument("--popsize", type=int, default=10)
    parser.add_argument("--iterations", type=int, default=80)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    edge_count = args.n * (args.n - 1) // 2
    benchmark = baseline(args.n, args.r, "Bd") + baseline(args.n, args.r, "dB")
    evaluations = 0
    best = (float("inf"), None)

    def objective(logs: np.ndarray) -> float:
        nonlocal evaluations, best
        weights = weights_from_logs(args.n, logs)
        value = benchmark - (
            fixation(weights, args.r, "Bd") + fixation(weights, args.r, "dB")
        )
        evaluations += 1
        if value < best[0]:
            best = (value, logs.copy())
            print("best gap", value, "evaluation", evaluations, flush=True)
        return value

    result = differential_evolution(
        objective,
        [(-args.span, args.span)] * edge_count,
        seed=args.seed,
        popsize=args.popsize,
        maxiter=args.iterations,
        polish=False,
        updating="immediate",
        workers=1,
    )
    polished = minimize(objective, result.x, method="Nelder-Mead")
    logs = polished.x if polished.fun <= result.fun else result.x
    weights = weights_from_logs(args.n, logs)
    bd = fixation(weights, args.r, "Bd")
    db = fixation(weights, args.r, "dB")
    print("result gap", benchmark - bd - db)
    print("Bd", bd, "delta", bd - baseline(args.n, args.r, "Bd"))
    print("dB", db, "delta", db - baseline(args.n, args.r, "dB"))
    print("weights", weights.tolist())


if __name__ == "__main__":
    main()
