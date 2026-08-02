#!/usr/bin/env python3
"""Rare-satellite branching derivative for an arbitrary finite module.

The module subset chain is built directly from Bd/dB updating with simultaneous
center migration.  Differentiating the dense-center PGF at satellite ratio
``mu=0`` gives an exact finite-state coefficient.  The numerical optimizer is
reconnaissance; positive output would require symbolic certification and a
post-establishment argument.
"""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import differential_evolution


def colony_survival(
    weights: np.ndarray,
    outer: np.ndarray,
    center_degree: float,
    fitness: float,
    rule: str,
    mark: float,
):
    size = len(weights)
    degree = weights.sum(axis=1)
    full = (1 << size) - 1
    masks = list(range(1, full + 1))
    index = {mask: i for i, mask in enumerate(masks)}
    matrix = np.zeros((full, full))
    rhs = np.zeros(full)
    for mask, row in index.items():
        mutant = np.array([(mask >> v) & 1 for v in range(size)], dtype=float)
        changes: dict[int, float] = {}
        success = 0.0
        if rule == "Bd":
            augmented = degree + outer
            for parent in range(size):
                parent_mutant = bool(mutant[parent])
                parent_fitness = fitness if parent_mutant else 1.0
                for target in range(size):
                    if not weights[parent, target] or parent_mutant == bool(mutant[target]):
                        continue
                    target_mask = mask | (1 << target) if parent_mutant else mask & ~(1 << target)
                    rate = parent_fitness * weights[parent, target] / augmented[parent]
                    changes[target_mask] = changes.get(target_mask, 0.0) + rate
                if parent_mutant:
                    success += fitness * outer[parent] / augmented[parent] * mark
            for target in range(size):
                if mutant[target]:
                    target_mask = mask & ~(1 << target)
                    changes[target_mask] = changes.get(target_mask, 0.0) + outer[target] / center_degree
        elif rule == "dB":
            for target in range(size):
                internal_mutant = float(weights[:, target] @ mutant)
                internal_resident = degree[target] - internal_mutant
                denominator = fitness * internal_mutant + internal_resident + outer[target]
                if mutant[target]:
                    rate = (internal_resident + outer[target]) / denominator
                    target_mask = mask & ~(1 << target)
                else:
                    rate = fitness * internal_mutant / denominator
                    target_mask = mask | (1 << target)
                if rate:
                    changes[target_mask] = changes.get(target_mask, 0.0) + rate
            success = fitness * float((outer / center_degree) @ mutant) * mark
        else:
            raise ValueError(rule)
        total = success + sum(changes.values())
        matrix[row, row] = total
        rhs[row] = success
        for target_mask, rate in changes.items():
            if target_mask:
                matrix[row, index[target_mask]] -= rate
    values = np.linalg.solve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    singleton = np.array([values[index[1 << v]] for v in range(size)])
    return singleton, residual


def coefficients(weights, outer, center_degree, fitness):
    degree = weights.sum(axis=1)
    p = 1.0 - 1.0 / fitness
    result = {}
    for rule in ("Bd", "dB"):
        singleton, residual = colony_survival(
            weights, outer, center_degree, fitness, rule, p
        )
        if residual > 1e-6:
            raise FloatingPointError(residual)
        if rule == "Bd":
            center_derivative = (
                float((outer / center_degree) @ singleton)
                - p * float(np.sum(outer / (degree + outer)))
            ) / (fitness - 1.0)
        else:
            center_derivative = (
                float((outer / (degree + outer)) @ singleton)
                - p * float(outer.sum() / center_degree)
            ) / (fitness - 1.0)
        coefficient = center_derivative + float(singleton.sum()) - len(weights) * p
        result[rule] = (coefficient, center_derivative, singleton)
    return result


def decode(size: int, vector: np.ndarray):
    edge_count = size * (size - 1) // 2
    edge_logs = np.asarray(vector[:edge_count])
    edge_logs = edge_logs - np.max(edge_logs)
    weights = np.zeros((size, size))
    cursor = 0
    for i in range(size):
        for j in range(i + 1, size):
            weights[i, j] = weights[j, i] = math.exp(float(edge_logs[cursor]))
            cursor += 1
    outer = np.exp(np.asarray(vector[edge_count : edge_count + size]))
    center_degree = math.exp(float(vector[-1]))
    return weights, outer, center_degree


def evaluate(size: int, fitness: float, vector: np.ndarray):
    weights, outer, center_degree = decode(size, vector)
    result = coefficients(weights, outer, center_degree, fitness)
    return min(result["Bd"][0], result["dB"][0]), result, weights, outer, center_degree


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=4)
    parser.add_argument("--fitness", type=float, default=1.55)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=260)
    parser.add_argument("--popsize", type=int, default=16)
    args = parser.parse_args()
    dimension = args.size * (args.size - 1) // 2 + args.size + 1

    def objective(vector):
        try:
            return -evaluate(args.size, args.fitness, vector)[0]
        except (np.linalg.LinAlgError, FloatingPointError, ValueError):
            return 100.0

    result = differential_evolution(
        objective,
        [(-20.0, 8.0)] * dimension,
        seed=args.seed,
        maxiter=args.iterations,
        popsize=args.popsize,
        polish=True,
        tol=1e-10,
        workers=1,
        updating="immediate",
        disp=True,
    )
    score, values, weights, outer, center_degree = evaluate(
        args.size, args.fitness, result.x
    )
    print(f"RESULT n={args.size} r={args.fitness} score={score:+.12g}")
    for rule in ("Bd", "dB"):
        coefficient, center_derivative, singleton = values[rule]
        print(
            f"{rule} C={coefficient:+.12g} center'={center_derivative:+.12g} "
            + "sat=" + " ".join(f"{x:.12g}" for x in singleton)
        )
    print(f"D={center_degree:.12g}")
    print("h", " ".join(f"{x:.12g}" for x in outer))
    for row in weights:
        print(" ".join(f"{x:.12g}" for x in row))


if __name__ == "__main__":
    main()
