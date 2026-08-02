#!/usr/bin/env python3
"""dB search on windmills with asymmetric two-vertex blades.

Blade q has center weights ``left[q]`` and ``right[q]`` and internal weight
``internal[q]``.  Its state is a two-bit mask, so no unproved exchangeability
is used.  The exact reduced state space has ``2*4**blades`` states.

Numerical optimization is reconnaissance only.
"""

from __future__ import annotations

import argparse
from itertools import product

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import differential_evolution, minimize

from search_db import baseline


class OrientedWindmill:
    def __init__(self, blades: int):
        self.blades = blades
        self.order = 2 * blades + 1
        self.extinction = (0,) * (blades + 1)
        self.fixation_state = (1,) + (3,) * blades
        self.states = [
            state
            for state in product(range(2), *([range(4)] * blades))
            if state not in (self.extinction, self.fixation_state)
        ]
        self.index = {state: row for row, state in enumerate(self.states)}

    def fixation(self, left, right, internal, fitness):
        rows, columns, entries = [], [], []
        rhs = np.zeros(len(self.states))
        for state, row in self.index.items():
            center, *blade_states = state
            left_mutant = np.asarray([bool(value & 1) for value in blade_states])
            right_mutant = np.asarray([bool(value & 2) for value in blade_states])
            changes = []

            mutant_mass = float(left @ left_mutant + right @ right_mutant)
            resident_mass = float(
                left @ (~left_mutant) + right @ (~right_mutant)
            )
            denominator = fitness * mutant_mass + resident_mass
            if center == 0 and mutant_mass:
                changes.append(((1, *blade_states), fitness * mutant_mass / denominator))
            if center == 1 and resident_mass:
                changes.append(((0, *blade_states), resident_mass / denominator))

            for blade, value in enumerate(blade_states):
                for bit, partner_bit, outer in (
                    (1, 2, left[blade]),
                    (2, 1, right[blade]),
                ):
                    target_mutant = bool(value & bit)
                    partner_mutant = bool(value & partner_bit)
                    mutant_mass = internal[blade] * partner_mutant + outer * center
                    resident_mass = (
                        internal[blade] * (not partner_mutant) + outer * (1 - center)
                    )
                    denominator = fitness * mutant_mass + resident_mass
                    if target_mutant:
                        rate = resident_mass / denominator
                        target_value = value & ~bit
                    else:
                        rate = fitness * mutant_mass / denominator
                        target_value = value | bit
                    if rate:
                        updated = list(blade_states); updated[blade] = target_value
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
        answer = values[self.index[(1,) + (0,) * self.blades]]
        for blade in range(self.blades):
            answer += values[
                self.index[(0,) + tuple(1 if q == blade else 0 for q in range(self.blades))]
            ]
            answer += values[
                self.index[(0,) + tuple(2 if q == blade else 0 for q in range(self.blades))]
            ]
        return float(answer / self.order), residual


def weights_from_logs(logs, blades):
    logs = np.asarray(logs) - np.mean(logs)
    values = np.exp(logs)
    return values[:blades], values[blades:2 * blades], values[2 * blades:]


def optimize(model, fitness, bound, iterations, seed):
    target = baseline(model.order, fitness)
    dimension = 3 * model.blades

    def objective(logs):
        left, right, internal = weights_from_logs(logs, model.blades)
        try:
            value, residual = model.fixation(left, right, internal, fitness)
        except Exception:
            return 1.0
        if residual > 1e-7 or not np.isfinite(value) or not (-1e-8 <= value <= 1 + 1e-8):
            return 1.0
        return target - value

    result = differential_evolution(
        objective, [(-bound, bound)] * dimension,
        maxiter=iterations, popsize=7, polish=False, seed=seed, tol=1e-8,
    )
    symmetric = np.zeros(dimension)
    candidates = [result]
    for start in (result.x, symmetric):
        candidates.append(
            minimize(
                objective, start, method="L-BFGS-B",
                bounds=[(-bound, bound)] * dimension,
                options={"maxiter": 1000, "ftol": 1e-14},
            )
        )
    best = min(candidates, key=lambda item: item.fun)
    left, right, internal = weights_from_logs(best.x, model.blades)
    value, residual = model.fixation(left, right, internal, fitness)
    return dict(excess=value - target, value=value, residual=residual,
                left=left, right=right, internal=internal)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blades", type=int, required=True)
    parser.add_argument("--fitness", type=float, required=True)
    parser.add_argument("--bound", type=float, default=8)
    parser.add_argument("--iterations", type=int, default=250)
    parser.add_argument("--restarts", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260802)
    args = parser.parse_args()
    model = OrientedWindmill(args.blades)
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
