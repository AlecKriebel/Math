#!/usr/bin/env python3
"""Numerically stress-test the proposed all-graph dB stationary inequality."""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import differential_evolution

from optimize_sum import weights_from_logs


def singleton_values(weights: np.ndarray, fitness: float) -> np.ndarray:
    order = len(weights)
    full = (1 << order) - 1
    transient = list(range(1, full))
    index = {state: position for position, state in enumerate(transient)}
    matrix = np.eye(len(transient))
    rhs = np.zeros(len(transient))
    degree = weights.sum(axis=1)
    transition = weights / degree[:, None]
    for state in transient:
        row = index[state]
        mutant = np.array([(state >> i) & 1 for i in range(order)])
        changes: dict[int, float] = {}
        for target in range(order):
            x = float(transition[target] @ mutant)
            new_mutant = fitness * x / (1 + (fitness - 1) * x)
            if mutant[target]:
                new_state = state & ~(1 << target)
                probability = 1 - new_mutant
            else:
                new_state = state | (1 << target)
                probability = new_mutant
            changes[new_state] = changes.get(new_state, 0.0) + probability
        changes.pop(state, None)
        effective = sum(changes.values())
        if effective <= 1e-280:
            raise FloatingPointError
        for new_state, probability in changes.items():
            probability /= effective
            if new_state == full:
                rhs[row] += probability
            elif new_state:
                matrix[row, index[new_state]] -= probability
    condition = np.linalg.cond(matrix)
    if not np.isfinite(condition) or condition > 1e11:
        raise FloatingPointError
    solution = np.linalg.solve(matrix, rhs)
    residual = np.linalg.norm(matrix @ solution - rhs, ord=np.inf)
    values = np.array([solution[index[1 << i]] for i in range(order)])
    if residual > 1e-8 or values.min() < -1e-7 or values.max() > 1 + 1e-7:
        raise FloatingPointError
    return values


def margin(weights: np.ndarray, fitness: float) -> tuple[float, float, float]:
    degree = weights.sum(axis=1)
    forward = singleton_values(weights, fitness)
    reverse = singleton_values(weights, 1 / fitness)
    harmonic_degree = np.sum(1 / degree)
    average = forward.mean()
    weighted_singleton = np.sum(reverse / degree)
    normalized = weighted_singleton / (fitness**2 * harmonic_degree)
    return normalized - (average - (1 - 1 / fitness)), average, normalized


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--r", type=float, default=1.5)
    parser.add_argument("--span", type=float, default=18)
    parser.add_argument("--iterations", type=int, default=120)
    parser.add_argument("--popsize", type=int, default=15)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    edge_count = args.n * (args.n - 1) // 2
    best = (float("inf"), None)

    def objective(logs: np.ndarray) -> float:
        nonlocal best
        weights = weights_from_logs(args.n, logs)
        try:
            value = margin(weights, args.r)[0]
        except (FloatingPointError, np.linalg.LinAlgError):
            return 10
        if value < best[0]:
            best = (value, logs.copy())
            print("best margin", value, flush=True)
        return value

    result = differential_evolution(
        objective,
        [(-args.span, args.span)] * edge_count,
        seed=args.seed,
        popsize=args.popsize,
        maxiter=args.iterations,
        polish=True,
    )
    weights = weights_from_logs(args.n, result.x)
    print("result", margin(weights, args.r))
    print("weights", weights.tolist())


if __name__ == "__main__":
    main()
