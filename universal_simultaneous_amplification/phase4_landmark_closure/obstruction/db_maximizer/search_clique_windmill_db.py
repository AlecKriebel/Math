#!/usr/bin/env python3
"""dB reconnaissance on a center with heterogeneous clique blades.

Blade q is a clique of ``sizes[q]`` exchangeable vertices.  Its internal
edges have weight ``internal[q]`` and all its vertices attach to the common
center with weight ``outer[q]``.  The exact lumped state records the center
type and one mutant count per blade.

Floating-point optimization is discovery only.  A candidate is not a result
until a separate exact transition audit and rational absorbing solve pass.
"""

from __future__ import annotations

import argparse
from itertools import product

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import differential_evolution, minimize

from search_db import baseline


class CliqueWindmill:
    def __init__(self, sizes: tuple[int, ...]):
        if not sizes or min(sizes) < 1:
            raise ValueError(sizes)
        self.sizes = sizes
        self.blades = len(sizes)
        self.order = 1 + sum(sizes)
        self.extinction = (0,) * (self.blades + 1)
        self.fixation_state = (1,) + sizes
        self.states = [
            state
            for state in product(range(2), *(range(size + 1) for size in sizes))
            if state not in (self.extinction, self.fixation_state)
        ]
        self.index = {state: row for row, state in enumerate(self.states)}

    def fixation(self, outer: np.ndarray, internal: np.ndarray, fitness: float):
        rows, columns, entries = [], [], []
        rhs = np.zeros(len(self.states))
        for state, row in self.index.items():
            center, *counts = state
            changes: list[tuple[tuple[int, ...], float]] = []

            mutant_mass = float(np.dot(outer, counts))
            resident_mass = float(
                np.dot(outer, np.asarray(self.sizes) - np.asarray(counts))
            )
            denominator = fitness * mutant_mass + resident_mass
            if center == 0 and mutant_mass:
                changes.append(((1, *counts), fitness * mutant_mass / denominator))
            if center == 1 and resident_mass:
                changes.append(((0, *counts), resident_mass / denominator))

            for blade, (count, size, outer_weight, internal_weight) in enumerate(
                zip(counts, self.sizes, outer, internal)
            ):
                if count < size:
                    mutant_mass = internal_weight * count + outer_weight * center
                    resident_mass = (
                        internal_weight * (size - count - 1)
                        + outer_weight * (1 - center)
                    )
                    denominator = fitness * mutant_mass + resident_mass
                    rate = (size - count) * fitness * mutant_mass / denominator
                    if rate:
                        updated = list(counts); updated[blade] += 1
                        changes.append(((center, *updated), rate))
                if count > 0:
                    mutant_mass = (
                        internal_weight * (count - 1) + outer_weight * center
                    )
                    resident_mass = (
                        internal_weight * (size - count)
                        + outer_weight * (1 - center)
                    )
                    denominator = fitness * mutant_mass + resident_mass
                    rate = count * resident_mass / denominator
                    if rate:
                        updated = list(counts); updated[blade] -= 1
                        changes.append(((center, *updated), rate))

            changing = sum(rate for _, rate in changes)
            if not changing > 0:
                raise ArithmeticError((state, changes))
            rows.append(row); columns.append(row); entries.append(1.0)
            for target, rate in changes:
                probability = rate / changing
                if target == self.fixation_state:
                    rhs[row] += probability
                elif target != self.extinction:
                    rows.append(row); columns.append(self.index[target]); entries.append(-probability)

        matrix = sp.csr_matrix(
            (entries, (rows, columns)), shape=(len(self.states), len(self.states))
        )
        values = spla.spsolve(matrix, rhs)
        residual = float(np.max(np.abs(matrix @ values - rhs)))
        center_singleton = values[self.index[(1,) + (0,) * self.blades]]
        blade_singletons = [
            values[
                self.index[
                    (0,) + tuple(int(candidate == blade) for candidate in range(self.blades))
                ]
            ]
            for blade in range(self.blades)
        ]
        rho = (
            center_singleton
            + sum(size * value for size, value in zip(self.sizes, blade_singletons))
        ) / self.order
        return float(rho), residual


def weights_from_logs(logs: np.ndarray):
    logs = np.asarray(logs) - np.mean(logs)
    values = np.exp(logs)
    blades = len(values) // 2
    return values[:blades], values[blades:]


def optimize(model: CliqueWindmill, fitness: float, bound: float, iterations: int, seed: int):
    target = baseline(model.order, fitness)
    dimension = 2 * model.blades

    def objective(logs):
        outer, internal = weights_from_logs(logs)
        try:
            value, residual = model.fixation(outer, internal, fitness)
        except Exception:
            return 1.0
        if residual > 1e-7 or not np.isfinite(value) or not (-1e-8 <= value <= 1 + 1e-8):
            return 1.0
        return target - value

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
    value, residual = model.fixation(outer, internal, fitness)
    return dict(
        excess=value - target, value=value, residual=residual,
        outer=outer, internal=internal,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", required=True, help="comma-separated blade sizes")
    parser.add_argument("--fitness", type=float, required=True)
    parser.add_argument("--bound", type=float, default=9)
    parser.add_argument("--iterations", type=int, default=250)
    parser.add_argument("--restarts", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260802)
    args = parser.parse_args()
    model = CliqueWindmill(tuple(map(int, args.sizes.split(","))))
    records = []
    for restart in range(args.restarts):
        answer = optimize(
            model, args.fitness, args.bound, args.iterations,
            args.seed + 1009 * restart,
        )
        records.append(answer)
        print(restart, answer, flush=True)
    print("BEST", max(records, key=lambda item: item["excess"]))


if __name__ == "__main__":
    main()
