#!/usr/bin/env python3
"""Numerical falsification search for the geometric-batching ratio.

This is a discovery aid, never a proof.  It evaluates dB fixation and the
reversed-arrow biased-link fixation, whose quotient equals m_D/m_C.
"""

from __future__ import annotations

import argparse
import pathlib
import random
import sys

import numpy as np
from scipy.optimize import differential_evolution


HERE = pathlib.Path(__file__).resolve()
SIGNED = HERE.parents[1] / "signed_cut_capacity"
OBSTRUCTION = HERE.parents[1]
sys.path.insert(0, str(SIGNED))
sys.path.insert(0, str(OBSTRUCTION))
from search_adjoint_split import link_fixation  # noqa: E402
from search_random import fixation  # noqa: E402


R = 1.5


def complete_ratio(n: int) -> float:
    a = 2.0 / 3.0
    return (n - 1) / n * (1 - a**n) / (1 - a ** (n - 1))


def random_connected_weights(
    n: int, rng: random.Random, span: float, edge_probability: float
) -> np.ndarray:
    weights = np.zeros((n, n))
    order = list(range(n))
    rng.shuffle(order)
    edges: set[tuple[int, int]] = set()
    for index in range(1, n):
        child = order[index]
        parent = order[rng.randrange(index)]
        edges.add(tuple(sorted((child, parent))))
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < edge_probability:
                edges.add((i, j))
    for i, j in edges:
        value = np.exp(rng.uniform(-span, span))
        weights[i, j] = weights[j, i] = value
    return weights


def ratio_excess(weights: np.ndarray) -> tuple[float, float, float]:
    p = weights / weights.sum(axis=1)[:, None]
    rho_c = link_fixation(p.T)
    rho_d = fixation(weights, R, "dB")
    ratio = rho_d / rho_c
    return ratio / complete_ratio(len(weights)) - 1, rho_c, rho_d


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--span", type=float, default=18.0)
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument("--optimize", action="store_true")
    parser.add_argument("--iterations", type=int, default=80)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    if args.optimize:
        pairs = [(i, j) for i in range(args.n) for j in range(i + 1, args.n)]
        best_opt: list[object] = [-np.inf, None, None]

        def objective(logs: np.ndarray) -> float:
            weights = np.zeros((args.n, args.n))
            logs = logs - logs.mean()
            for (i, j), value in zip(pairs, np.exp(logs)):
                weights[i, j] = weights[j, i] = value
            try:
                values = ratio_excess(weights)
            except (FloatingPointError, np.linalg.LinAlgError):
                return 1e3
            if values[0] > best_opt[0]:
                best_opt[:] = [values[0], weights.copy(), values[1:]]
            return -values[0]

        differential_evolution(
            objective,
            [(-args.span, args.span)] * len(pairs),
            seed=args.seed,
            popsize=10,
            maxiter=args.iterations,
            polish=True,
        )
        print("optimized relative excess", best_opt[0], "rho_C,rho_D", best_opt[2])
        print("weights", best_opt[1].tolist() if best_opt[1] is not None else None)
        return
    best = (-np.inf, None, None)
    for trial in range(args.trials):
        # Mix trees, sparse graphs, and dense graphs.
        probability = (0.0, 0.2, 0.5, 1.0)[trial % 4]
        weights = random_connected_weights(args.n, rng, args.span, probability)
        try:
            values = ratio_excess(weights)
        except np.linalg.LinAlgError:
            continue
        if not all(np.isfinite(value) for value in values):
            continue
        if values[0] > best[0]:
            best = values[0], weights.copy(), values[1:]
        if values[0] > 1e-7:
            print("APPARENT COUNTEREXAMPLE", trial, values)
            print(weights.tolist())
            return
    print("best relative excess", best[0], "rho_C,rho_D", best[2])
    print("weights", best[1].tolist() if best[1] is not None else None)


if __name__ == "__main__":
    main()
