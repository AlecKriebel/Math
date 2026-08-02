#!/usr/bin/env python3
"""Numerical search for a cross-sum violation at r=3/2.

This is discovery code, not a proof.  It directly solves both absorbing
subset chains, deletes state-dependent self-loops for numerical stability,
and optimizes logarithms of all edge weights.  Every apparent positive
excess must be converted to rational weights and checked exactly.
"""

from __future__ import annotations

import argparse
import itertools
import pathlib
import sys

import numpy as np
from scipy.optimize import differential_evolution, minimize


PARENT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PARENT))
from search_random import baseline, fixation  # noqa: E402


FITNESS = 1.5


def weights_from_logs(order: int, logs: np.ndarray) -> np.ndarray:
    weights = np.zeros((order, order))
    edges = list(itertools.combinations(range(order), 2))
    centered = logs - logs.mean()
    for edge, value in zip(edges, np.exp(centered)):
        i, j = edge
        weights[i, j] = weights[j, i] = value
    return weights


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--span", type=float, default=18.0)
    parser.add_argument("--popsize", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=120)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    edge_count = args.n * (args.n - 1) // 2
    target = baseline(args.n, FITNESS, "Bd") + baseline(args.n, FITNESS, "dB")
    evaluations = 0
    best = [float("inf"), None]

    def objective(logs: np.ndarray) -> float:
        nonlocal evaluations
        weights = weights_from_logs(args.n, logs)
        try:
            total = fixation(weights, FITNESS, "Bd") + fixation(
                weights, FITNESS, "dB"
            )
            value = target - total
        except (FloatingPointError, np.linalg.LinAlgError):
            value = 10.0
        evaluations += 1
        if value < best[0]:
            best[:] = value, logs.copy()
            if value < -1e-9:
                print("APPARENT VIOLATION", value, "evaluation", evaluations, flush=True)
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
    bd = fixation(weights, FITNESS, "Bd")
    db = fixation(weights, FITNESS, "dB")
    print("gap", target - bd - db)
    print("Bd_delta", bd - baseline(args.n, FITNESS, "Bd"))
    print("dB_delta", db - baseline(args.n, FITNESS, "dB"))
    print("weights", repr(weights.tolist()))


if __name__ == "__main__":
    main()
