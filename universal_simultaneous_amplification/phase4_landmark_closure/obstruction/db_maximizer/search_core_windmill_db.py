#!/usr/bin/env python3
"""dB reconnaissance for an exchangeable clique core with clique blades.

The core has ``core_size`` vertices and common internal edge weight
``core_weight``.  Blade q is a clique of ``sizes[q]`` vertices, with internal
weight ``internal[q]``; every core--blade-q edge has weight ``outer[q]``.
The exact state consists only of mutant counts in the core and blades.

Numerical optimization is discovery only.
"""

from __future__ import annotations

import argparse
from itertools import product

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import differential_evolution, minimize

from search_db import baseline


class CoreWindmill:
    def __init__(self, core_size: int, sizes: tuple[int, ...]):
        self.core_size = core_size
        self.sizes = sizes
        self.blades = len(sizes)
        self.order = core_size + sum(sizes)
        self.extinction = (0,) * (self.blades + 1)
        self.fixation_state = (core_size,) + sizes
        self.states = [
            state
            for state in product(range(core_size + 1), *(range(size + 1) for size in sizes))
            if state not in (self.extinction, self.fixation_state)
        ]
        self.index = {state: row for row, state in enumerate(self.states)}

    def fixation(self, core_weight, outer, internal, fitness):
        rows, columns, entries = [], [], []
        rhs = np.zeros(len(self.states))
        for state, row in self.index.items():
            core_mutants, *counts = state
            changes = []

            if core_mutants < self.core_size:
                mutant_mass = (
                    core_weight * core_mutants
                    + float(np.dot(outer, counts))
                )
                resident_mass = (
                    core_weight * (self.core_size - core_mutants - 1)
                    + float(np.dot(outer, np.asarray(self.sizes) - counts))
                )
                denominator = fitness * mutant_mass + resident_mass
                rate = (self.core_size - core_mutants) * fitness * mutant_mass / denominator
                if rate:
                    changes.append(((core_mutants + 1, *counts), rate))
            if core_mutants > 0:
                mutant_mass = (
                    core_weight * (core_mutants - 1)
                    + float(np.dot(outer, counts))
                )
                resident_mass = (
                    core_weight * (self.core_size - core_mutants)
                    + float(np.dot(outer, np.asarray(self.sizes) - counts))
                )
                denominator = fitness * mutant_mass + resident_mass
                rate = core_mutants * resident_mass / denominator
                if rate:
                    changes.append(((core_mutants - 1, *counts), rate))

            for blade, (count, size, outer_weight, internal_weight) in enumerate(
                zip(counts, self.sizes, outer, internal)
            ):
                if count < size:
                    mutant_mass = (
                        internal_weight * count + outer_weight * core_mutants
                    )
                    resident_mass = (
                        internal_weight * (size - count - 1)
                        + outer_weight * (self.core_size - core_mutants)
                    )
                    denominator = fitness * mutant_mass + resident_mass
                    rate = (size - count) * fitness * mutant_mass / denominator
                    if rate:
                        updated = list(counts); updated[blade] += 1
                        changes.append(((core_mutants, *updated), rate))
                if count > 0:
                    mutant_mass = (
                        internal_weight * (count - 1) + outer_weight * core_mutants
                    )
                    resident_mass = (
                        internal_weight * (size - count)
                        + outer_weight * (self.core_size - core_mutants)
                    )
                    denominator = fitness * mutant_mass + resident_mass
                    rate = count * resident_mass / denominator
                    if rate:
                        updated = list(counts); updated[blade] -= 1
                        changes.append(((core_mutants, *updated), rate))

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
        core_singleton = values[self.index[(1,) + (0,) * self.blades]]
        blade_singletons = [
            values[
                self.index[
                    (0,) + tuple(int(candidate == blade) for candidate in range(self.blades))
                ]
            ]
            for blade in range(self.blades)
        ]
        rho = (
            self.core_size * core_singleton
            + sum(size * value for size, value in zip(self.sizes, blade_singletons))
        ) / self.order
        return float(rho), residual


def weights_from_logs(logs, blades):
    logs = np.asarray(logs) - np.mean(logs)
    values = np.exp(logs)
    return values[0], values[1:blades + 1], values[blades + 1:]


def optimize(model, fitness, bound, iterations, seed):
    target = baseline(model.order, fitness)
    dimension = 1 + 2 * model.blades

    def objective(logs):
        core, outer, internal = weights_from_logs(logs, model.blades)
        try:
            value, residual = model.fixation(core, outer, internal, fitness)
        except Exception:
            return 1.0
        if residual > 1e-7 or not np.isfinite(value) or not (-1e-8 <= value <= 1 + 1e-8):
            return 1.0
        return target - value

    result = differential_evolution(
        objective, [(-bound, bound)] * dimension,
        maxiter=iterations, popsize=8, polish=False, seed=seed, tol=1e-8,
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
    core, outer, internal = weights_from_logs(best.x, model.blades)
    value, residual = model.fixation(core, outer, internal, fitness)
    return dict(excess=value - target, value=value, residual=residual,
                core=core, outer=outer, internal=internal)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-size", type=int, required=True)
    parser.add_argument("--sizes", required=True)
    parser.add_argument("--fitness", type=float, required=True)
    parser.add_argument("--bound", type=float, default=8)
    parser.add_argument("--iterations", type=int, default=250)
    parser.add_argument("--restarts", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260802)
    args = parser.parse_args()
    model = CoreWindmill(args.core_size, tuple(map(int, args.sizes.split(","))))
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
