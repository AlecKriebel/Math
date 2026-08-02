#!/usr/bin/env python3
"""Discovery-only search for regular weighted dB amplifiers at r=2.

A regular undirected weighted graph can be scaled so that its weight matrix is
symmetric, has zero diagonal, and every row sums to one.  We parameterize this
polytope exactly at the linear-algebra level as

    w = (1/(n-1)) 1 + Z x,

where the columns of Z span the nullspace of the unsigned vertex-edge
incidence matrix.  Floating optimization is reconnaissance only; any positive
candidate must be converted to rational weights and independently certified.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np
import scipy.linalg
from scipy.optimize import LinearConstraint, minimize

HERE = Path(__file__).resolve()
DB_MAX = HERE.parents[1] / "db_maximizer"
sys.path.insert(0, str(DB_MAX))
from search_db import baseline, fixation  # noqa: E402


def regular_coordinates(size: int):
    edges = [(i, j) for i in range(size) for j in range(i + 1, size)]
    incidence = np.zeros((size, len(edges)))
    for edge, (i, j) in enumerate(edges):
        incidence[i, edge] = 1.0
        incidence[j, edge] = 1.0
    null = scipy.linalg.null_space(incidence)
    uniform = np.full(len(edges), 1.0 / (size - 1))
    assert np.max(np.abs(incidence @ uniform - 1.0)) < 1e-13
    assert np.max(np.abs(incidence @ null)) < 1e-13
    return edges, incidence, uniform, null


def matrix_from_edges(size: int, edges, edge_weights):
    weights = np.zeros((size, size))
    for (i, j), value in zip(edges, edge_weights):
        weights[i, j] = weights[j, i] = value
    return weights


def hit_and_run(uniform, null, rng, steps: int, floor: float = 1e-10):
    """Return an interior polytope point after exact-line hit-and-run steps."""
    x = np.zeros(null.shape[1])
    edge_weights = uniform.copy()
    for _ in range(steps):
        direction = rng.normal(size=null.shape[1])
        direction /= np.linalg.norm(direction)
        delta = null @ direction
        lower, upper = -np.inf, np.inf
        positive = delta > 1e-15
        negative = delta < -1e-15
        if np.any(positive):
            lower = max(lower, np.max((floor - edge_weights[positive]) / delta[positive]))
        if np.any(negative):
            upper = min(upper, np.min((floor - edge_weights[negative]) / delta[negative]))
        amount = rng.uniform(lower, upper)
        x += amount * direction
        edge_weights = uniform + null @ x
    return x


def search(size: int, starts: int, seed: int):
    edges, incidence, uniform, null = regular_coordinates(size)
    target = baseline(size, 2.0)
    constraint = LinearConstraint(null, -uniform + 1e-11, np.inf)
    rng = np.random.default_rng(seed)
    cache = {}

    def objective(x):
        key = np.asarray(x).tobytes()
        if key in cache:
            return cache[key]
        edge_weights = uniform + null @ x
        if np.min(edge_weights) <= 0:
            return 1.0
        weights = matrix_from_edges(size, edges, edge_weights)
        try:
            value, residual, _ = fixation(weights, 2.0)
        except (ValueError, np.linalg.LinAlgError):
            return 1.0
        if residual > 1e-7 or not (-1e-9 <= value <= 1 + 1e-9):
            return 1.0
        result = target - value
        cache[key] = result
        return result

    candidates = [(objective(np.zeros(null.shape[1])), np.zeros(null.shape[1]))]
    for start_number in range(starts):
        if start_number == 0:
            start = np.zeros(null.shape[1])
        else:
            start = hit_and_run(uniform, null, rng, 20 + 3 * size)
        candidates.append((objective(start), start.copy()))
        polished = minimize(
            objective,
            start,
            method="SLSQP",
            constraints=[constraint],
            options={"maxiter": 1500, "ftol": 1e-13, "disp": False},
        )
        candidates.append((float(polished.fun), polished.x.copy()))
        best_value, best_x = min(candidates, key=lambda item: item[0])
        print(
            f"n={size} start={start_number + 1}/{starts} "
            f"best_excess={-best_value:.16g} min_w={np.min(uniform + null @ best_x):.4g}",
            flush=True,
        )

    deficit, x = min(candidates, key=lambda item: item[0])
    edge_weights = uniform + null @ x
    weights = matrix_from_edges(size, edges, edge_weights)
    value, residual, singletons = fixation(weights, 2.0)
    return {
        "excess": value - target,
        "value": value,
        "target": target,
        "residual": residual,
        "weights": weights,
        "edge_weights": edge_weights,
        "singletons": singletons,
        "row_error": np.max(np.abs(weights.sum(axis=1) - 1.0)),
        "dimension": null.shape[1],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--starts", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20260802)
    args = parser.parse_args()
    result = search(args.n, args.starts, args.seed)
    for key in ("dimension", "target", "value", "excess", "residual", "row_error"):
        print(key, result[key])
    print("singletons", np.array2string(result["singletons"], precision=16))
    print("weights")
    print(np.array2string(result["weights"], precision=16, suppress_small=False))


if __name__ == "__main__":
    main()
