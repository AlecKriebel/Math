#!/usr/bin/env python3
"""Targeted falsification search for the adjoint rank-MLR strengthening."""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import differential_evolution

from search_adjoint_split import weights_from_logs


A = 0.5


def dual_generator(p: np.ndarray, transpose_arrows: bool) -> np.ndarray:
    n = len(p)
    full = (1 << n) - 1
    q = np.zeros((full, full))
    for state in range(1, full + 1):
        row = state - 1
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            for source in range(n):
                rate = p[target, source] if transpose_arrows else p[source, target]
                if not rate:
                    continue
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                if neutral != state:
                    q[row, neutral - 1] += rate
                if selective != state:
                    q[row, selective - 1] += A * rate
        q[row, row] = -q[row].sum()
    return q


def stationary(q: np.ndarray) -> np.ndarray:
    matrix = q.T.copy()
    matrix[-1] = 1
    rhs = np.zeros(len(q))
    rhs[-1] = 1
    return np.linalg.solve(matrix, rhs)


def rank_likelihoods(weights: np.ndarray) -> np.ndarray:
    n = len(weights)
    p = weights / weights.sum(axis=1)[:, None]
    pi = stationary(dual_generator(p, False))
    sigma = stationary(dual_generator(p, True))
    z = (1 + A) ** n - 1
    result = []
    for k in range(1, n + 1):
        states = [state for state in range(1, 1 << n) if state.bit_count() == k]
        result.append(
            sum((pi[state - 1] + sigma[state - 1]) * z / A**k for state in states)
            / len(states)
        )
    return np.asarray(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--span", type=float, default=10)
    parser.add_argument("--iterations", type=int, default=80)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    edge_count = args.n * (args.n - 1) // 2
    for level in range(args.n - 1):
        best = [-np.inf, None, None]

        def objective(logs: np.ndarray) -> float:
            try:
                weights = weights_from_logs(args.n, logs)
                ranks = rank_likelihoods(weights)
                excess = ranks[level + 1] - ranks[level]
            except np.linalg.LinAlgError:
                return 1e3
            if excess > best[0]:
                best[:] = excess, logs.copy(), ranks
            return -excess

        differential_evolution(
            objective,
            [(-args.span, args.span)] * edge_count,
            seed=args.seed + level,
            popsize=10,
            maxiter=args.iterations,
            polish=True,
        )
        print("level", level + 1, "excess", best[0], "ranks", best[2])
        print("weights", weights_from_logs(args.n, best[1]).tolist())


if __name__ == "__main__":
    main()
