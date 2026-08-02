#!/usr/bin/env python3
"""Optimize the exact first-order rare-satellite branching coefficients.

For ``mu=M/c -> 0``, the uniform early-survival probability has expansion

    p + mu*C_U + O(mu^2),   p=1-1/r.

Differentiating the center PGF at ``mu=0`` gives the coefficients implemented
below.  The satellite colony probabilities are exact seven-state killed-chain
solutions.  A positive result would be a branching candidate, not yet a
fixation theorem.
"""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import differential_evolution

from search_early_escape import local_success


def coefficients(fitness: float, delta: float, h: np.ndarray, center_degree: float):
    h = np.asarray(h, dtype=float)
    p = 1.0 - 1.0 / fitness
    internal_degree = np.array((1.0 + delta, 2.0 * delta, 1.0 + delta))
    values = {}
    for rule in ("Bd", "dB"):
        _, residual, local = local_success(
            fitness,
            delta,
            h,
            center_degree,
            rule,
            mark_probability=p,
        )
        if residual > 2e-7:
            raise FloatingPointError(residual)
        singleton = np.array([local[(1 << v) - 1] for v in range(3)])
        if rule == "Bd":
            center_derivative = (
                float((h / center_degree) @ singleton)
                - p * float(np.sum(h / (internal_degree + h)))
            ) / (fitness - 1.0)
        else:
            center_derivative = (
                float((h / (internal_degree + h)) @ singleton)
                - p * float(h.sum() / center_degree)
            ) / (fitness - 1.0)
        coefficient = center_derivative + float(singleton.sum()) - 3.0 * p
        values[rule] = (coefficient, center_derivative, singleton)
    return values


def decode(vector: np.ndarray):
    delta = math.exp(float(vector[0]))
    h = np.exp(np.asarray(vector[1:4], dtype=float))
    center_degree = math.exp(float(vector[4]))
    return delta, h, center_degree


def evaluate(fitness: float, vector: np.ndarray):
    delta, h, center_degree = decode(vector)
    result = coefficients(fitness, delta, h, center_degree)
    return min(result["Bd"][0], result["dB"][0]), result, delta, h, center_degree


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fitness", type=float, default=1.55)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=260)
    parser.add_argument("--popsize", type=int, default=18)
    args = parser.parse_args()

    def objective(vector):
        try:
            return -evaluate(args.fitness, vector)[0]
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            return 100.0

    result = differential_evolution(
        objective,
        [(-22.0, 10.0)] * 5,
        seed=args.seed,
        maxiter=args.iterations,
        popsize=args.popsize,
        polish=True,
        tol=1e-11,
        workers=1,
        updating="immediate",
        disp=True,
    )
    score, values, delta, h, center_degree = evaluate(args.fitness, result.x)
    print(f"RESULT r={args.fitness} score={score:+.12g}")
    for rule in ("Bd", "dB"):
        coefficient, center_derivative, singleton = values[rule]
        print(
            f"{rule} C={coefficient:+.12g} center'={center_derivative:+.12g} "
            + "sat=" + " ".join(f"{x:.12g}" for x in singleton)
        )
    print(f"delta={delta:.12g} D={center_degree:.12g}")
    print("h", " ".join(f"{x:.12g}" for x in h))


if __name__ == "__main__":
    main()
