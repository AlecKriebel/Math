#!/usr/bin/env python3
"""Exact-count reconnaissance for dB on heterogeneous two-vertex windmills.

Blade q has two exchangeable vertices.  Their common edge to the center has
weight ``outer[q]`` and their internal edge has weight ``internal[q]``.  The
state ``(c,k_1,...,k_m)`` records the center type and each blade mutant count,
so the lumped chain has ``2*3**m`` states.  The formulas are derived directly
from dB updating and are strongly lumpable because the two vertices within
each blade are exchangeable.

Floating-point optimization is for discovery only.  Any positive candidate
must be rationalized and passed to an exact version of the same chain.
"""

from __future__ import annotations

import argparse
from itertools import product

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import differential_evolution, minimize

from search_db import baseline


def fixation(outer: np.ndarray, internal: np.ndarray, fitness: float):
    blades = len(outer)
    size = 2 * blades + 1
    extinction = (0,) * (blades + 1)
    fixation_state = (1,) + (2,) * blades
    states = [
        state
        for state in product(range(2), *([range(3)] * blades))
        if state not in (extinction, fixation_state)
    ]
    index = {state: row for row, state in enumerate(states)}
    rows, cols, data = [], [], []
    rhs = np.zeros(len(states))

    for state, row in index.items():
        center, *counts = state
        changes: list[tuple[tuple[int, ...], float]] = []

        mutant_mass = float(np.dot(outer, counts))
        resident_mass = float(np.dot(outer, 2 - np.asarray(counts)))
        denominator = fitness * mutant_mass + resident_mass
        if center == 0 and mutant_mass:
            changes.append(((1, *counts), fitness * mutant_mass / denominator))
        if center == 1 and resident_mass:
            changes.append(((0, *counts), resident_mass / denominator))

        for blade, (count, outer_weight, internal_weight) in enumerate(
            zip(counts, outer, internal)
        ):
            if count < 2:
                mutant_mass = internal_weight * (count == 1) + outer_weight * center
                resident_mass = internal_weight * (count == 0) + outer_weight * (1 - center)
                denominator = fitness * mutant_mass + resident_mass
                rate = (2 - count) * fitness * mutant_mass / denominator
                if rate:
                    updated = list(counts); updated[blade] += 1
                    changes.append(((center, *updated), rate))
            if count > 0:
                mutant_mass = internal_weight * (count == 2) + outer_weight * center
                resident_mass = internal_weight * (count == 1) + outer_weight * (1 - center)
                denominator = fitness * mutant_mass + resident_mass
                rate = count * resident_mass / denominator
                if rate:
                    updated = list(counts); updated[blade] -= 1
                    changes.append(((center, *updated), rate))

        changing = sum(rate for _, rate in changes)
        if not changing > 0:
            raise ArithmeticError((state, changes))
        rows.append(row); cols.append(row); data.append(1.0)
        for target, rate in changes:
            probability = rate / changing
            if target == fixation_state:
                rhs[row] += probability
            elif target != extinction:
                rows.append(row); cols.append(index[target]); data.append(-probability)

    matrix = sp.csr_matrix((data, (rows, cols)), shape=(len(states), len(states)))
    values = spla.spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    center_singleton = values[index[(1,) + (0,) * blades]]
    blade_singletons = [
        values[index[(0,) + tuple(int(q == blade) for q in range(blades))]]
        for blade in range(blades)
    ]
    rho = (center_singleton + 2 * sum(blade_singletons)) / size
    return float(rho), residual


def fixation_bd(outer: np.ndarray, internal: np.ndarray, fitness: float):
    """Bd fixation on the same exact blade-count state space."""
    blades = len(outer)
    size = 2 * blades + 1
    center_degree = 2 * float(sum(outer))
    blade_degree = outer + internal
    extinction = (0,) * (blades + 1)
    fixation_state = (1,) + (2,) * blades
    states = [
        state
        for state in product(range(2), *([range(3)] * blades))
        if state not in (extinction, fixation_state)
    ]
    index = {state: row for row, state in enumerate(states)}
    rows, cols, data = [], [], []
    rhs = np.zeros(len(states))

    for state, row in index.items():
        center, *counts = state
        changes: list[tuple[tuple[int, ...], float]] = []
        center_up = fitness * sum(
            count * outer_weight / degree
            for count, outer_weight, degree in zip(counts, outer, blade_degree)
        )
        center_down = sum(
            (2 - count) * outer_weight / degree
            for count, outer_weight, degree in zip(counts, outer, blade_degree)
        )
        if center == 0 and center_up:
            changes.append(((1, *counts), center_up))
        if center == 1 and center_down:
            changes.append(((0, *counts), center_down))

        for blade, (count, outer_weight, internal_weight, degree) in enumerate(
            zip(counts, outer, internal, blade_degree)
        ):
            if count < 2:
                rate = fitness * (
                    (2 - count) * center * outer_weight / center_degree
                    + int(count == 1) * internal_weight / degree
                )
                if rate:
                    updated = list(counts); updated[blade] += 1
                    changes.append(((center, *updated), rate))
            if count > 0:
                rate = (
                    count * (1 - center) * outer_weight / center_degree
                    + int(count == 1) * internal_weight / degree
                )
                if rate:
                    updated = list(counts); updated[blade] -= 1
                    changes.append(((center, *updated), rate))

        changing = sum(rate for _, rate in changes)
        if not changing > 0:
            raise ArithmeticError((state, changes))
        rows.append(row); cols.append(row); data.append(1.0)
        for target, rate in changes:
            probability = rate / changing
            if target == fixation_state:
                rhs[row] += probability
            elif target != extinction:
                rows.append(row); cols.append(index[target]); data.append(-probability)

    matrix = sp.csr_matrix((data, (rows, cols)), shape=(len(states), len(states)))
    values = spla.spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    center_singleton = values[index[(1,) + (0,) * blades]]
    blade_singletons = [
        values[index[(0,) + tuple(int(q == blade) for q in range(blades))]]
        for blade in range(blades)
    ]
    rho = (center_singleton + 2 * sum(blade_singletons)) / size
    return float(rho), residual


def weights_from_logs(logs: np.ndarray):
    logs = np.asarray(logs) - np.mean(logs)
    values = np.exp(logs)
    blades = len(values) // 2
    return values[:blades], values[blades:]


def optimize(blades: int, fitness: float, bound: float, iterations: int, seed: int):
    target = baseline(2 * blades + 1, fitness)

    def objective(logs):
        outer, internal = weights_from_logs(logs)
        try:
            value, residual = fixation(outer, internal, fitness)
        except Exception:
            return 1.0
        if residual > 1e-7 or not np.isfinite(value) or not (-1e-8 <= value <= 1 + 1e-8):
            return 1.0
        return target - value

    dimension = 2 * blades
    result = differential_evolution(
        objective,
        [(-bound, bound)] * dimension,
        maxiter=iterations,
        popsize=8,
        polish=False,
        seed=seed,
        tol=1e-8,
    )
    candidates = [result]
    for start in (result.x, np.zeros(dimension)):
        candidates.append(
            minimize(
                objective, start, method="L-BFGS-B",
                bounds=[(-bound, bound)] * dimension,
                options={"maxiter": 1000, "ftol": 1e-14},
            )
        )
    best = min(candidates, key=lambda item: item.fun)
    outer, internal = weights_from_logs(best.x)
    value, residual = fixation(outer, internal, fitness)
    return dict(
        excess=value - target, value=value, residual=residual,
        outer=outer, internal=internal,
        logs=np.asarray(best.x) - np.mean(best.x),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blades", type=int, required=True)
    parser.add_argument("--fitness", type=float, required=True)
    parser.add_argument("--bound", type=float, default=9)
    parser.add_argument("--iterations", type=int, default=250)
    parser.add_argument("--restarts", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20260802)
    args = parser.parse_args()
    records = []
    for restart in range(args.restarts):
        answer = optimize(
            args.blades, args.fitness, args.bound, args.iterations,
            args.seed + 1009 * restart,
        )
        records.append(answer)
        print(restart, answer, flush=True)
    print("BEST", max(records, key=lambda item: item["excess"]))


if __name__ == "__main__":
    main()
