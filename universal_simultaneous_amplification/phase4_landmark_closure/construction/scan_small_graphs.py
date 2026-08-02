#!/usr/bin/env python3
"""Unrestricted small-graph reconnaissance from the defining Markov chain.

Weights are positive and parametrized logarithmically on complete support.
The optimizer is used only to suggest exact orbit patterns.  Every objective
evaluation solves both absorbing chains directly and checks the residual.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import differential_evolution


def baseline(n: int, fitness: float, rule: str) -> float:
    if rule == "Bd":
        return (1 - fitness**-1) / (1 - fitness**-n)
    return (n - 1) / n * (1 - fitness**-1) / (1 - fitness ** (-(n - 1)))


def matrix_from_logs(n: int, logs: np.ndarray) -> np.ndarray:
    edges = list(itertools.combinations(range(n), 2))
    if len(logs) != len(edges):
        raise ValueError((len(logs), len(edges)))
    logs = logs - np.mean(logs)
    weights = np.zeros((n, n))
    for (i, j), value in zip(edges, np.exp(logs)):
        weights[i, j] = weights[j, i] = value
    return weights


def fixation(weights: np.ndarray, fitness: float, rule: str) -> tuple[float, float]:
    n = len(weights)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {mask: position for position, mask in enumerate(states)}
    matrix = np.zeros((len(states), len(states)))
    rhs = np.zeros(len(states))
    degrees = weights.sum(axis=1)
    for mask, source in index.items():
        mutant = np.array([(mask >> i) & 1 for i in range(n)], dtype=float)
        changes: list[tuple[int, float]] = []
        if rule == "Bd":
            total_fitness = n + (fitness - 1) * mutant.sum()
            source_mass = weights.T @ ((1 + (fitness - 1) * mutant) / degrees)
            for target in range(n):
                if mutant[target]:
                    probability = float((weights[:, target] @ ((1 - mutant) / degrees)) / total_fitness)
                    if probability:
                        changes.append((mask & ~(1 << target), probability))
                else:
                    probability = float(fitness * (weights[:, target] @ (mutant / degrees)) / total_fitness)
                    if probability:
                        changes.append((mask | (1 << target), probability))
        elif rule == "dB":
            for target in range(n):
                mutant_mass = float(weights[:, target] @ mutant)
                resident_mass = degrees[target] - mutant_mass
                denominator = fitness * mutant_mass + resident_mass
                if mutant[target]:
                    probability = resident_mass / (n * denominator)
                    if probability:
                        changes.append((mask & ~(1 << target), probability))
                else:
                    probability = fitness * mutant_mass / (n * denominator)
                    if probability:
                        changes.append((mask | (1 << target), probability))
        else:
            raise ValueError(rule)
        matrix[source, source] = sum(probability for _, probability in changes)
        for target, probability in changes:
            if target == full:
                rhs[source] += probability
            elif target:
                matrix[source, index[target]] -= probability
    values = np.linalg.solve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    average = sum(values[index[1 << i]] for i in range(n)) / n
    return float(average), residual


def comparisons(n: int, logs: np.ndarray, fitnesses: tuple[float, ...]) -> np.ndarray:
    weights = matrix_from_logs(n, logs)
    result = []
    for fitness in fitnesses:
        for rule in ("Bd", "dB"):
            value, residual = fixation(weights, fitness, rule)
            if residual > 1e-8:
                raise AssertionError(residual)
            result.append(value - baseline(n, fitness, rule))
    return np.array(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--upper", type=float, default=1.2)
    parser.add_argument("--points", type=int, default=5)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    fitnesses = tuple(np.linspace(1.001, args.upper, args.points))
    dimension = args.n * (args.n - 1) // 2

    def objective(logs: np.ndarray) -> float:
        values = comparisons(args.n, logs, fitnesses)
        # Scale by baseline selection gain to avoid optimizing only the largest r.
        scales = np.repeat(np.array(fitnesses) - 1, 2)
        return -float(np.min(values / scales))

    result = differential_evolution(
        objective,
        [(-8.0, 8.0)] * dimension,
        maxiter=args.iterations,
        popsize=8,
        polish=True,
        seed=args.seed,
        workers=1,
        updating="immediate",
        disp=True,
    )
    logs = result.x - np.mean(result.x)
    weights = matrix_from_logs(args.n, logs)
    print("objective", result.fun)
    print("fitnesses", fitnesses)
    print("comparisons", comparisons(args.n, logs, fitnesses))
    np.set_printoptions(precision=7, suppress=True, linewidth=200)
    print("logs", logs)
    print("weights")
    print(weights)


if __name__ == "__main__":
    main()
