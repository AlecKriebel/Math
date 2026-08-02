#!/usr/bin/env python3
"""Cancellation-safe Monte Carlo search for a cross-rule-sum violation.

This is discovery code only.  It samples complete and sparse connected
supports over many logarithmic weight scales and evaluates both exact subset
chains in double precision.  Any positive excess must be rerun with rational
weights in an exact solver.
"""

from __future__ import annotations

import argparse
import warnings

import networkx as nx
import numpy as np

from search_db import baseline, baseline_bd, fixation, fixation_bd


def sample_weights(rng, size, sparse):
    if sparse:
        while True:
            probability = rng.uniform(0.18, 0.82)
            support = rng.random((size, size)) < probability
            support = np.triu(support, 1)
            support |= support.T
            if nx.is_connected(nx.from_numpy_array(support.astype(float))):
                break
    else:
        support = np.ones((size, size), dtype=bool)
        np.fill_diagonal(support, False)
    scale = rng.choice((0.02, 0.1, 0.4, 1.5, 3.0, 5.0))
    logs = np.clip(rng.normal(0, scale, (size, size)), -12, 12)
    logs = np.triu(logs, 1)
    logs += logs.T
    weights = support * np.exp(logs)
    return weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--fitness", type=float, required=True)
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    target = baseline(args.size, args.fitness) + baseline_bd(args.size, args.fitness)
    best = (-np.inf, None, None)
    best_nontrivial = (-np.inf, None, None)
    warnings.filterwarnings("ignore")
    for sample in range(args.samples):
        weights = sample_weights(rng, args.size, sparse=bool(sample & 1))
        try:
            db, db_residual, _ = fixation(weights, args.fitness)
            bd, bd_residual, _ = fixation_bd(weights, args.fitness)
        except (ValueError, np.linalg.LinAlgError):
            continue
        residual = max(db_residual, bd_residual)
        excess = db + bd - target
        valid = (
            residual < 1e-8
            and -1e-9 <= db <= 1 + 1e-9
            and -1e-9 <= bd <= 1 + 1e-9
        )
        if valid and excess > best[0]:
            best = (excess, (bd, db, residual), weights.copy())
        edge_values = weights[np.triu_indices(args.size, 1)]
        positive = edge_values[edge_values > 0]
        if (
            valid
            and positive.size
            and np.std(np.log(positive)) > 0.05
            and excess > best_nontrivial[0]
        ):
            best_nontrivial = (excess, (bd, db, residual), weights.copy())
        if excess > 1e-7 and valid:
            print("APPARENT COUNTEREXAMPLE", sample, excess, bd, db, residual)
            print(repr(weights))
            return
    print("NO COUNTEREXAMPLE", args.size, args.fitness, args.samples)
    print("best", best[0], best[1])
    print("best_nontrivial", best_nontrivial[0], best_nontrivial[1])
    print(repr(best_nontrivial[2]))


if __name__ == "__main__":
    main()
