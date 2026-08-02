#!/usr/bin/env python3
"""Local early-migration search for a triangle next to a large clique.

Unlike the separated trace construction, center-seeding and center-to-module
replacement are allowed on the same scale as absorption inside the active
triangle.  The seven nonempty triangle masks form an exact limiting killed
chain when the center size diverges, its total internal weighted degree is
``Z``, each triangle vertex has total outer degree ``h``, and all other outer
mass is negligible relative to ``Z``.  A successful center introduction is
marked by the large-clique fixation limit ``p=1-1/r``.

This is a discovery model.  A positive local score would still require a
global scaling and center-sweep proof.
"""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import differential_evolution


def local_success(
    fitness: float,
    delta: float,
    outer_degree: np.ndarray,
    z: float,
    rule: str,
    mark_probability: float | None = None,
):
    weights = np.array(((0.0, delta, 1.0), (delta, 0.0, delta), (1.0, delta, 0.0)))
    degrees = weights.sum(axis=1)
    full = 7
    masks = list(range(1, 8))
    index = {mask: i for i, mask in enumerate(masks)}
    matrix = np.zeros((7, 7))
    rhs = np.zeros(7)
    p = (
        1.0 - 1.0 / fitness
        if mark_probability is None
        else float(mark_probability)
    )
    outer_degree = np.asarray(outer_degree, dtype=float)
    x = outer_degree / z
    for mask, row in index.items():
        mutant = np.array([(mask >> v) & 1 for v in range(3)], dtype=float)
        changes: dict[int, float] = {}
        success = 0.0
        if rule == "Bd":
            augmented = degrees + outer_degree
            for parent in range(3):
                parent_mutant = bool(mutant[parent])
                parent_fitness = fitness if parent_mutant else 1.0
                for target in range(3):
                    if not weights[parent, target] or parent_mutant == bool(mutant[target]):
                        continue
                    target_mask = mask | (1 << target) if parent_mutant else mask & ~(1 << target)
                    rate = parent_fitness * weights[parent, target] / augmented[parent]
                    changes[target_mask] = changes.get(target_mask, 0.0) + rate
                if parent_mutant:
                    success += fitness * outer_degree[parent] / augmented[parent] * p
            # The resident center collectively replaces each mutant target
            # at limiting rate h/Z.
            for target in range(3):
                if mutant[target]:
                    target_mask = mask & ~(1 << target)
                    changes[target_mask] = changes.get(target_mask, 0.0) + x[target]
        elif rule == "dB":
            for target in range(3):
                internal_mutant = float(weights[:, target] @ mutant)
                internal_resident = degrees[target] - internal_mutant
                denominator = (
                    fitness * internal_mutant
                    + internal_resident
                    + outer_degree[target]
                )
                if mutant[target]:
                    rate = (internal_resident + outer_degree[target]) / denominator
                    target_mask = mask & ~(1 << target)
                else:
                    rate = fitness * internal_mutant / denominator
                    target_mask = mask | (1 << target)
                if rate:
                    changes[target_mask] = changes.get(target_mask, 0.0) + rate
            # Across all center deaths, mutant triangle parents create marked
            # successful introductions at the first-order limiting rate.
            success = fitness * float(x @ mutant) * p
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
    return float(sum(values[index[1 << v]] for v in range(3)) / 3), residual, values


def evaluate(fitness: float, vector: np.ndarray):
    delta = math.exp(float(vector[0]))
    outer_degree = np.exp(np.asarray(vector[1:4], dtype=float))
    z = math.exp(float(vector[4]))
    bd, rb, _ = local_success(fitness, delta, outer_degree, z, "Bd")
    db, rd, _ = local_success(fitness, delta, outer_degree, z, "dB")
    if max(rb, rd) > 1e-6:
        raise FloatingPointError((rb, rd))
    baseline = 1.0 - 1.0 / fitness
    return min(bd - baseline, db - baseline), bd, db, delta, outer_degree, z


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fitness", type=float, default=1.55)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=240)
    parser.add_argument("--popsize", type=int, default=16)
    parser.add_argument(
        "--max-load",
        type=float,
        default=float("inf"),
        help="upper bound on mean(h_v/Z), the center load per triangle ratio",
    )
    args = parser.parse_args()

    def objective(vector):
        try:
            evaluated = evaluate(args.fitness, vector)
            load = float(np.mean(evaluated[4] / evaluated[5]))
            if load > args.max_load:
                return 10.0 + load - args.max_load
            return -evaluated[0]
        except (np.linalg.LinAlgError, FloatingPointError):
            return 100.0

    result = differential_evolution(
        objective,
        [(-14.0, 6.0)] * 5,
        seed=args.seed,
        maxiter=args.iterations,
        popsize=args.popsize,
        polish=True,
        tol=1e-11,
        workers=1,
        updating="immediate",
        disp=True,
    )
    score, bd, db, delta, outer_degree, z = evaluate(args.fitness, result.x)
    print(f"RESULT r={args.fitness} score={score:+.12g}")
    print(f"success=({bd:.12g},{db:.12g}) baseline={1-1/args.fitness:.12g}")
    print(f"delta={delta:.12g} Z={z:.12g}")
    print("h", " ".join(f"{value:.12g}" for value in outer_degree))
    print("h/Z", " ".join(f"{value/z:.12g}" for value in outer_degree))


if __name__ == "__main__":
    main()
