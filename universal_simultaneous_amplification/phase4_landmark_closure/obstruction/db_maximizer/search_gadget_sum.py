#!/usr/bin/env python3
"""Search the separated star-of-gadgets limit for cross-rule sum excess."""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import minimize_scalar

from search_db import fixation, fixation_bd


def parameters(weights, fitness):
    size = len(weights)
    degree = weights.sum(axis=1)
    bd_a, _, _ = fixation_bd(weights, fitness)
    bd_b, _, _ = fixation_bd(weights, 1 / fitness)
    db_a, _, db_forward = fixation(weights, fitness)
    _, _, db_reverse = fixation(weights, 1 / fitness)
    inverse = 1 / degree
    db_invade = float(db_forward @ inverse / inverse.sum())
    db_reverse_invade = float(db_reverse @ inverse / inverse.sum())
    return bd_a, db_a, fitness * bd_a / bd_b, fitness**2 * db_invade / db_reverse_invade


def values(data, fitness, log_z):
    bd_a, db_a, q_bd, q_db = data
    z = math.exp(log_z)
    gamma_bd = (q_bd + z) / (q_bd * (q_bd * z + 1))
    gamma_db = (q_db * z + 1) / (q_db * (q_db + z))
    return bd_a * max(0, 1 - gamma_bd), db_a * max(0, 1 - gamma_db)


def sample_graph(rng, size):
    # Complete support covers sparse limits; keep the exponent range resolvable.
    scale = rng.choice((0.05, 0.2, 0.8, 2.0, 4.0))
    logs = np.clip(rng.normal(0, scale, (size, size)), -10, 10)
    logs = np.triu(logs, 1)
    logs += logs.T
    weights = np.exp(logs)
    np.fill_diagonal(weights, 0)
    return weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--fitness", type=float, required=True)
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    baseline_sum = 2 * (1 - 1 / args.fitness)
    best = (-np.inf, None)
    for sample in range(args.samples):
        weights = sample_graph(rng, args.size)
        data = parameters(weights, args.fitness)
        objective = lambda log_z: -(sum(values(data, args.fitness, log_z)) - baseline_sum)
        result = minimize_scalar(objective, bounds=(-20, 20), method="bounded")
        record = (-result.fun, math.exp(result.x), data, weights)
        if record[0] > best[0]:
            best = record
        if record[0] > 1e-8:
            print("APPARENT COUNTEREXAMPLE", sample, record[:3])
            print(repr(weights))
            return
    print("NO COUNTEREXAMPLE", args.size, args.fitness, args.samples)
    print("BEST", best[:3])
    print(repr(best[3]))


if __name__ == "__main__":
    main()
