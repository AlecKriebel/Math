#!/usr/bin/env python3
"""Search the regular weighted polytope for a dB amplifier at r=3/2.

On a regular undirected weighted graph Bd ties the complete graph exactly, so
any dB amplifier found here is immediately a cross-sum counterexample.  This
script is numerical discovery only.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
import scipy.linalg
from scipy.optimize import LinearConstraint, minimize


DB_MAX = pathlib.Path(__file__).resolve().parents[1] / "db_maximizer"
sys.path.insert(0, str(DB_MAX))
from search_db import baseline, fixation  # noqa: E402


FITNESS = 1.5


def coordinates(n: int):
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    incidence = np.zeros((n, len(edges)))
    for e, (i, j) in enumerate(edges):
        incidence[i, e] = incidence[j, e] = 1
    uniform = np.full(len(edges), 1 / (n - 1))
    null = scipy.linalg.null_space(incidence)
    return edges, uniform, null


def matrix(n, edges, values):
    answer = np.zeros((n, n))
    for (i, j), value in zip(edges, values):
        answer[i, j] = answer[j, i] = value
    return answer


def hit_and_run(uniform, null, rng, steps):
    x = np.zeros(null.shape[1])
    values = uniform.copy()
    for _ in range(steps):
        direction = rng.normal(size=len(x))
        direction /= np.linalg.norm(direction)
        delta = null @ direction
        lower, upper = -np.inf, np.inf
        if np.any(delta > 1e-14):
            mask = delta > 1e-14
            lower = np.max((1e-10 - values[mask]) / delta[mask])
        if np.any(delta < -1e-14):
            mask = delta < -1e-14
            upper = np.min((1e-10 - values[mask]) / delta[mask])
        amount = rng.uniform(lower, upper)
        x += amount * direction
        values = uniform + null @ x
    return x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--starts", type=int, default=40)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    edges, uniform, null = coordinates(args.n)
    target = baseline(args.n, FITNESS)
    rng = np.random.default_rng(args.seed)
    constraint = LinearConstraint(null, -uniform + 1e-11, np.inf)

    def objective(x):
        values = uniform + null @ x
        if values.min() <= 0:
            return 1.0
        try:
            rho, residual, _ = fixation(matrix(args.n, edges, values), FITNESS)
        except (ValueError, np.linalg.LinAlgError):
            return 1.0
        if residual > 1e-8:
            return 1.0
        return target - rho

    candidates = [(objective(np.zeros(null.shape[1])), np.zeros(null.shape[1]))]
    for number in range(args.starts):
        start = (
            np.zeros(null.shape[1])
            if number == 0
            else hit_and_run(uniform, null, rng, 20 + 3 * args.n)
        )
        candidates.append((objective(start), start))
        result = minimize(
            objective,
            start,
            method="SLSQP",
            constraints=[constraint],
            options={"maxiter": 1000, "ftol": 1e-13},
        )
        candidates.append((float(result.fun), result.x))
        best = min(candidates, key=lambda item: item[0])
        print(number + 1, "best dB excess", -best[0], flush=True)
        if best[0] < -1e-9:
            break
    deficit, x = min(candidates, key=lambda item: item[0])
    weights = matrix(args.n, edges, uniform + null @ x)
    rho, residual, _ = fixation(weights, FITNESS)
    print("dB excess", rho - target, "residual", residual)
    print(repr(weights.tolist()))


if __name__ == "__main__":
    main()
