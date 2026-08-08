#!/usr/bin/env python3
"""Hostile search for the endpoint one-third affine separator.

The graph has one centre and ``q`` disjoint two-vertex blades.  Each blade
has independent left-centre, right-centre, and internal weights.  Its exact
configuration is a centre bit and one two-bit mask per blade, so this code
does not assume an exchangeability which asymmetric weights do not possess.

This file is discovery code.  Every apparent score above one must be rebuilt
over exact rational arithmetic before it is used as a mathematical claim.
"""

from __future__ import annotations

import argparse
from itertools import product

import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve


R = 1.5


def baseline(order: int, rule: str) -> float:
    if rule == "Bd":
        return 3.0 ** (order - 1) / (3.0**order - 2.0**order)
    return (order - 1.0) * 3.0 ** (order - 2) / (
        order * (3.0 ** (order - 1) - 2.0 ** (order - 1))
    )


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

    def fixation(self, left, right, internal, rule: str):
        centre_degree = float(np.sum(left + right))
        left_degree = left + internal
        right_degree = right + internal
        rows, columns, entries = [], [], []
        rhs = np.zeros(len(self.states))

        for state, row in self.index.items():
            centre, *blade_states = state
            left_mutant = np.asarray([bool(value & 1) for value in blade_states])
            right_mutant = np.asarray([bool(value & 2) for value in blade_states])
            changes = []

            if rule == "Bd":
                mutant_mass = float(
                    np.sum(left * left_mutant / left_degree)
                    + np.sum(right * right_mutant / right_degree)
                )
                resident_mass = float(
                    np.sum(left * (~left_mutant) / left_degree)
                    + np.sum(right * (~right_mutant) / right_degree)
                )
                if not centre and mutant_mass:
                    changes.append(((1, *blade_states), R * mutant_mass))
                if centre and resident_mass:
                    changes.append(((0, *blade_states), resident_mass))

                for blade, value in enumerate(blade_states):
                    for bit, partner_bit, outer, partner_degree in (
                        (1, 2, left[blade], right_degree[blade]),
                        (2, 1, right[blade], left_degree[blade]),
                    ):
                        target_mutant = bool(value & bit)
                        partner_mutant = bool(value & partner_bit)
                        mutant_mass = (
                            outer * centre / centre_degree
                            + internal[blade] * partner_mutant / partner_degree
                        )
                        resident_mass = (
                            outer * (1 - centre) / centre_degree
                            + internal[blade]
                            * (not partner_mutant)
                            / partner_degree
                        )
                        rate = resident_mass if target_mutant else R * mutant_mass
                        if rate:
                            updated = list(blade_states)
                            updated[blade] = value & ~bit if target_mutant else value | bit
                            changes.append(((centre, *updated), rate))
            elif rule == "dB":
                mutant_mass = float(left @ left_mutant + right @ right_mutant)
                resident_mass = float(left @ (~left_mutant) + right @ (~right_mutant))
                denominator = R * mutant_mass + resident_mass
                if not centre and mutant_mass:
                    changes.append(((1, *blade_states), R * mutant_mass / denominator))
                if centre and resident_mass:
                    changes.append(((0, *blade_states), resident_mass / denominator))

                for blade, value in enumerate(blade_states):
                    for bit, partner_bit, outer in (
                        (1, 2, left[blade]),
                        (2, 1, right[blade]),
                    ):
                        target_mutant = bool(value & bit)
                        partner_mutant = bool(value & partner_bit)
                        mutant_mass = internal[blade] * partner_mutant + outer * centre
                        resident_mass = (
                            internal[blade] * (not partner_mutant)
                            + outer * (1 - centre)
                        )
                        denominator = R * mutant_mass + resident_mass
                        rate = (
                            resident_mass / denominator
                            if target_mutant
                            else R * mutant_mass / denominator
                        )
                        if rate:
                            updated = list(blade_states)
                            updated[blade] = value & ~bit if target_mutant else value | bit
                            changes.append(((centre, *updated), rate))
            else:
                raise ValueError(rule)

            changing = sum(rate for _, rate in changes)
            if not changing > 0:
                raise ArithmeticError((state, changes))
            rows.append(row)
            columns.append(row)
            entries.append(changing)
            for target, rate in changes:
                if target == self.fixation_state:
                    rhs[row] += rate
                elif target != self.extinction:
                    rows.append(row)
                    columns.append(self.index[target])
                    entries.append(-rate)

        matrix = csr_matrix(
            (entries, (rows, columns)), shape=(len(self.states), len(self.states))
        )
        values = spsolve(matrix, rhs)
        residual = float(np.max(np.abs(matrix @ values - rhs)))
        singleton_sum = values[self.index[(1,) + (0,) * self.blades]]
        for blade in range(self.blades):
            for bit in (1, 2):
                singleton_sum += values[
                    self.index[
                        (0,)
                        + tuple(bit if candidate == blade else 0 for candidate in range(self.blades))
                    ]
                ]
        return float(singleton_sum / self.order), residual


def weights_from_logs(logs, blades):
    logs = np.asarray(logs, dtype=float)
    logs -= np.mean(logs)
    values = np.exp(logs)
    return values[:blades], values[blades : 2 * blades], values[2 * blades :]


def score(model, logs):
    left, right, internal = weights_from_logs(logs, model.blades)
    bd, residual_b = model.fixation(left, right, internal, "Bd")
    db, residual_d = model.fixation(left, right, internal, "dB")
    x = bd / baseline(model.order, "Bd")
    y = db / baseline(model.order, "dB")
    return (x + 2 * y) / 3, x, y, max(residual_b, residual_d)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blades", type=int, default=3)
    parser.add_argument("--bound", type=float, default=10)
    parser.add_argument("--iterations", type=int, default=180)
    parser.add_argument("--popsize", type=int, default=8)
    parser.add_argument("--restarts", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260808)
    args = parser.parse_args()
    model = OrientedWindmill(args.blades)
    dimension = 3 * args.blades
    best = None

    for restart in range(args.restarts):
        def loss(logs):
            try:
                value, _, _, residual = score(model, logs)
            except Exception:
                return 10.0
            if residual > 1e-7 or not np.isfinite(value):
                return 10.0
            return -value

        result = differential_evolution(
            loss,
            [(-args.bound, args.bound)] * dimension,
            maxiter=args.iterations,
            popsize=args.popsize,
            polish=False,
            seed=args.seed + 1009 * restart,
            tol=1e-9,
            updating="immediate",
        )
        candidates = [result]
        for start in (result.x, np.zeros(dimension)):
            candidates.append(
                minimize(
                    loss,
                    start,
                    method="Powell",
                    bounds=[(-args.bound, args.bound)] * dimension,
                    options={"maxiter": 2000, "ftol": 1e-13, "xtol": 1e-10},
                )
            )
        winner = min(candidates, key=lambda item: item.fun)
        record = (*score(model, winner.x), winner.x - np.mean(winner.x))
        if best is None or record[0] > best[0]:
            best = record
        print("restart", restart, "score,x,y,residual,logs", record, flush=True)

    print("BEST", best, flush=True)


if __name__ == "__main__":
    main()
