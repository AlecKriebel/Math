#!/usr/bin/env python3
"""Rare-coupling search over two arbitrary fixed modules (discovery only).

Two connected weighted modules A and B are joined by an epsilon-weight
complete bipartite bundle and epsilon tends to zero after the modules are
fixed.  The four monomorphic macro states have only two transient states,
so their fixation probabilities follow directly from the first successful
cross-module invasion rates.  An internal scale ratio z=t_A/t_B is free.

This script generates arbitrary small weighted modules, solves their labelled
subset chains directly, and optimizes the simultaneous endpoint fixation of
the two-module trace.  It is a falsification/construction screen, not a proof
for a growing graph family.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from itertools import product
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


R = 1.5


def singleton_fixation(weights: np.ndarray, fitness: float, rule: str) -> np.ndarray:
    n = len(weights)
    degree = weights.sum(axis=1)
    if np.any(degree <= 0):
        raise FloatingPointError("isolated vertex")
    full = (1 << n) - 1
    matrix = np.zeros((full - 1, full - 1))
    rhs = np.zeros(full - 1)
    for state in range(1, full):
        row = state - 1
        rates = []
        total = 0.0
        for target in range(n):
            target_mutant = bool(state & (1 << target))
            if rule == "Bd":
                incoming = sum(
                    weights[parent, target] / degree[parent]
                    for parent in range(n)
                    if bool(state & (1 << parent)) != target_mutant
                )
                rate = incoming if target_mutant else fitness * incoming
            elif rule == "dB":
                mutant_mass = sum(
                    weights[parent, target]
                    for parent in range(n)
                    if state & (1 << parent)
                )
                resident_mass = degree[target] - mutant_mass
                denominator = fitness * mutant_mass + resident_mass
                rate = (
                    resident_mass / denominator
                    if target_mutant
                    else fitness * mutant_mass / denominator
                )
            else:
                raise ValueError(rule)
            if rate:
                rates.append((state ^ (1 << target), rate))
                total += rate
        matrix[row, row] = 1.0
        for next_state, rate in rates:
            probability = rate / total
            if next_state == full:
                rhs[row] += probability
            elif next_state:
                matrix[row, next_state - 1] -= probability
    harmonic = np.linalg.solve(matrix, rhs)
    return np.asarray([harmonic[(1 << vertex) - 1] for vertex in range(n)])


@dataclass
class Module:
    weights: np.ndarray
    label: str
    n: int
    inverse_degree_sum: float
    bd_forward_mean: float
    bd_reverse_mean: float
    db_forward_mean: float
    db_forward_inverse: float
    db_reverse_inverse: float


def module_data(weights: np.ndarray, label: str) -> Module:
    degree = weights.sum(axis=1)
    n = len(weights)
    bd_f = singleton_fixation(weights, R, "Bd")
    bd_b = singleton_fixation(weights, 1.0 / R, "Bd")
    db_f = singleton_fixation(weights, R, "dB")
    db_b = singleton_fixation(weights, 1.0 / R, "dB")
    return Module(
        weights,
        label,
        n,
        float(np.sum(1.0 / degree)),
        float(np.mean(bd_f)),
        float(np.mean(bd_b)),
        float(np.mean(db_f)),
        float(np.sum(db_f / degree)),
        float(np.sum(db_b / degree)),
    )


def two_module_fixation(a: Module, b: Module, z: float) -> tuple[float, float]:
    """Trace fixation when module A's internal weights are scaled by z."""
    # Bd: replacement pressure is source-inverse-degree weighted, while the
    # newly invaded target vertex is uniform.
    up_a = R * b.n * (a.inverse_degree_sum / z) * b.bd_forward_mean
    down_a = a.n * b.inverse_degree_sum * a.bd_reverse_mean
    p_a_bd = up_a / (up_a + down_a)
    up_b = R * a.n * b.inverse_degree_sum * a.bd_forward_mean
    down_b = b.n * (a.inverse_degree_sum / z) * b.bd_reverse_mean
    p_b_bd = up_b / (up_b + down_b)
    rho_bd = (
        a.n * a.bd_forward_mean * p_a_bd
        + b.n * b.bd_forward_mean * p_b_bd
    ) / (a.n + b.n)

    # dB: the inverse-degree weighting belongs to the target.  Resident
    # invasion of a mutant module carries the relative-fitness factor 1/R.
    up_a = R * a.n * b.db_forward_inverse
    down_a = b.n / R * (a.db_reverse_inverse / z)
    p_a_db = up_a / (up_a + down_a)
    up_b = R * b.n * (a.db_forward_inverse / z)
    down_b = a.n / R * b.db_reverse_inverse
    p_b_db = up_b / (up_b + down_b)
    rho_db = (
        a.n * a.db_forward_mean * p_a_db
        + b.n * b.db_forward_mean * p_b_db
    ) / (a.n + b.n)
    return rho_bd, rho_db


def connected(weights: np.ndarray) -> bool:
    n = len(weights)
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in np.flatnonzero(weights[vertex] > 0):
            if int(other) not in reached:
                reached.add(int(other))
                stack.append(int(other))
    return len(reached) == n


def random_module(n: int, rng: np.random.Generator, label: str) -> np.ndarray:
    while True:
        weights = np.zeros((n, n))
        density = rng.uniform(0.3, 1.0)
        for i, j in itertools.combinations(range(n), 2):
            if rng.random() < density:
                weights[i, j] = weights[j, i] = math.exp(rng.uniform(-9.0, 9.0))
        if connected(weights):
            return weights


def star(n: int) -> np.ndarray:
    weights = np.zeros((n, n))
    for vertex in range(1, n):
        weights[0, vertex] = weights[vertex, 0] = 1.0
    return weights


def star_singletons(n: int, fitness: float, rule: str) -> tuple[float, float]:
    """Center and per-leaf singleton values for the unit star."""
    leaves = n - 1
    empty = (0, 0)
    full = (1, leaves)
    states = [
        (center, count)
        for center in (0, 1)
        for count in range(leaves + 1)
        if (center, count) not in (empty, full)
    ]
    index = {state: row for row, state in enumerate(states)}
    rows: list[int] = []
    columns: list[int] = []
    entries: list[float] = []
    rhs = np.zeros(len(states))
    for state, row in index.items():
        center, count = state
        resident_leaves = leaves - count
        changes = []
        if rule == "Bd":
            if center == 0 and count:
                changes.append(((1, count), fitness * count))
            if center == 1 and resident_leaves:
                changes.append(((0, count), resident_leaves))
            if center == 1 and resident_leaves:
                changes.append(((center, count + 1), fitness * resident_leaves / leaves))
            if center == 0 and count:
                changes.append(((center, count - 1), count / leaves))
        elif rule == "dB":
            if center == 0 and count:
                changes.append(((1, count), fitness * count / (fitness * count + resident_leaves)))
            if center == 1 and resident_leaves:
                changes.append(((0, count), resident_leaves / (fitness * count + resident_leaves)))
            # A leaf has only the center as a possible parent.
            if center == 1 and resident_leaves:
                changes.append(((center, count + 1), resident_leaves))
            if center == 0 and count:
                changes.append(((center, count - 1), count))
        else:
            raise ValueError(rule)
        total = sum(rate for _, rate in changes)
        rows.append(row); columns.append(row); entries.append(1.0)
        for target, rate in changes:
            probability = rate / total
            if target == full:
                rhs[row] += probability
            elif target != empty:
                rows.append(row); columns.append(index[target]); entries.append(-probability)
    matrix = coo_matrix(
        (entries, (rows, columns)), shape=(len(states), len(states))
    ).tocsr()
    harmonic = spsolve(matrix, rhs)
    return float(harmonic[index[(1, 0)]]), float(harmonic[index[(0, 1)]])


def star_module_data(n: int) -> Module:
    weights = star(n)
    leaves = n - 1
    bd_fc, bd_fl = star_singletons(n, R, "Bd")
    bd_bc, bd_bl = star_singletons(n, 1.0 / R, "Bd")
    db_fc, db_fl = star_singletons(n, R, "dB")
    db_bc, db_bl = star_singletons(n, 1.0 / R, "dB")
    return Module(
        weights,
        f"star-{n}",
        n,
        1.0 / leaves + leaves,
        (bd_fc + leaves * bd_fl) / n,
        (bd_bc + leaves * bd_bl) / n,
        (db_fc + leaves * db_fl) / n,
        db_fc / leaves + leaves * db_fl,
        db_bc / leaves + leaves * db_bl,
    )


def clique(n: int) -> np.ndarray:
    return np.ones((n, n)) - np.eye(n)


def known_windmill() -> np.ndarray:
    weights = np.zeros((7, 7))
    for (left, right), outer, internal in zip(
        ((1, 2), (3, 4), (5, 6)), (100.0, 10.0, 1.0), (600.0, 1200.0, 1800.0)
    ):
        weights[0, left] = weights[left, 0] = outer
        weights[0, right] = weights[right, 0] = outer
        weights[left, right] = weights[right, left] = internal
    return weights


def windmill_singletons(
    outer: np.ndarray, internal: np.ndarray, fitness: float, rule: str
) -> tuple[float, list[float]]:
    """Center and per-vertex blade singleton values from the orbit chain."""
    blades = len(outer)
    empty = (0,) * (blades + 1)
    full = (1,) + (2,) * blades
    states = [
        state
        for state in product(range(2), *([range(3)] * blades))
        if state not in (empty, full)
    ]
    index = {state: row for row, state in enumerate(states)}
    rows: list[int] = []
    columns: list[int] = []
    entries: list[float] = []
    rhs = np.zeros(len(states))
    center_degree = 2.0 * float(np.sum(outer))
    blade_degree = outer + internal
    for state, row in index.items():
        center, *counts_tuple = state
        counts = np.asarray(counts_tuple)
        changes = []
        if rule == "dB":
            mutant_mass = float(outer @ counts)
            resident_mass = float(outer @ (2 - counts))
            denominator = fitness * mutant_mass + resident_mass
            if center == 0 and mutant_mass:
                changes.append(((1, *counts_tuple), fitness * mutant_mass / denominator))
            if center == 1 and resident_mass:
                changes.append(((0, *counts_tuple), resident_mass / denominator))
            for blade, (count, spoke, inside) in enumerate(
                zip(counts_tuple, outer, internal)
            ):
                if count < 2:
                    mm = inside * (count == 1) + spoke * center
                    rm = inside * (count == 0) + spoke * (1 - center)
                    rate = (2 - count) * fitness * mm / (fitness * mm + rm)
                    if rate:
                        target = list(counts_tuple); target[blade] += 1
                        changes.append(((center, *target), rate))
                if count > 0:
                    mm = inside * (count == 2) + spoke * center
                    rm = inside * (count == 1) + spoke * (1 - center)
                    rate = count * rm / (fitness * mm + rm)
                    if rate:
                        target = list(counts_tuple); target[blade] -= 1
                        changes.append(((center, *target), rate))
        elif rule == "Bd":
            center_up = fitness * sum(
                count * spoke / degree
                for count, spoke, degree in zip(counts_tuple, outer, blade_degree)
            )
            center_down = sum(
                (2 - count) * spoke / degree
                for count, spoke, degree in zip(counts_tuple, outer, blade_degree)
            )
            if center == 0 and center_up:
                changes.append(((1, *counts_tuple), center_up))
            if center == 1 and center_down:
                changes.append(((0, *counts_tuple), center_down))
            for blade, (count, spoke, inside, degree) in enumerate(
                zip(counts_tuple, outer, internal, blade_degree)
            ):
                if count < 2:
                    rate = fitness * (
                        (2 - count) * center * spoke / center_degree
                        + int(count == 1) * inside / degree
                    )
                    if rate:
                        target = list(counts_tuple); target[blade] += 1
                        changes.append(((center, *target), rate))
                if count > 0:
                    rate = (
                        count * (1 - center) * spoke / center_degree
                        + int(count == 1) * inside / degree
                    )
                    if rate:
                        target = list(counts_tuple); target[blade] -= 1
                        changes.append(((center, *target), rate))
        else:
            raise ValueError(rule)
        total = sum(rate for _, rate in changes)
        rows.append(row); columns.append(row); entries.append(1.0)
        for target, rate in changes:
            probability = rate / total
            if target == full:
                rhs[row] += probability
            elif target != empty:
                rows.append(row); columns.append(index[target]); entries.append(-probability)
    matrix = coo_matrix(
        (entries, (rows, columns)), shape=(len(states), len(states))
    ).tocsr()
    values = spsolve(matrix, rhs)
    center_value = float(values[index[(1,) + (0,) * blades]])
    blade_values = []
    for blade in range(blades):
        singleton = (0,) + tuple(int(q == blade) for q in range(blades))
        blade_values.append(float(values[index[singleton]]))
    return center_value, blade_values


def windmill_module_data(
    outer_values: list[float], internal_values: list[float], label: str
) -> Module:
    outer = np.asarray(outer_values, dtype=float)
    internal = np.asarray(internal_values, dtype=float)
    blades = len(outer)
    weights = np.zeros((2 * blades + 1, 2 * blades + 1))
    for blade, (spoke, inside) in enumerate(zip(outer, internal)):
        left, right = 2 * blade + 1, 2 * blade + 2
        weights[0, left] = weights[left, 0] = spoke
        weights[0, right] = weights[right, 0] = spoke
        weights[left, right] = weights[right, left] = inside
    center_degree = 2.0 * float(np.sum(outer))
    blade_degree = outer + internal
    inverse_degree_sum = 1.0 / center_degree + 2.0 * float(np.sum(1.0 / blade_degree))
    bd_f_center, bd_f_blades = windmill_singletons(outer, internal, R, "Bd")
    bd_b_center, bd_b_blades = windmill_singletons(outer, internal, 1.0 / R, "Bd")
    db_f_center, db_f_blades = windmill_singletons(outer, internal, R, "dB")
    db_b_center, db_b_blades = windmill_singletons(outer, internal, 1.0 / R, "dB")
    n = 2 * blades + 1
    return Module(
        weights,
        label,
        n,
        inverse_degree_sum,
        (bd_f_center + 2.0 * sum(bd_f_blades)) / n,
        (bd_b_center + 2.0 * sum(bd_b_blades)) / n,
        (db_f_center + 2.0 * sum(db_f_blades)) / n,
        db_f_center / center_degree
        + 2.0 * sum(value / degree for value, degree in zip(db_f_blades, blade_degree)),
        db_b_center / center_degree
        + 2.0 * sum(value / degree for value, degree in zip(db_b_blades, blade_degree)),
    )


def optimize_pair(a: Module, b: Module):
    def loss(log_z):
        bd, db = two_module_fixation(a, b, math.exp(float(log_z)))
        return -min(bd, db)

    grid = np.linspace(-24.0, 24.0, 193)
    values = [loss(value) for value in grid]
    best = int(np.argmin(values))
    left = grid[max(0, best - 1)]
    right = grid[min(len(grid) - 1, best + 1)]
    polished = minimize_scalar(loss, bounds=(left, right), method="bounded")
    log_z = float(polished.x)
    bd, db = two_module_fixation(a, b, math.exp(log_z))
    return min(bd, db), bd, db, math.exp(log_z)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=80)
    parser.add_argument("--max-n", type=int, default=6)
    parser.add_argument("--seed", type=int, default=260808)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    modules = []
    for n in range(2, args.max_n + 1):
        modules.append(module_data(star(n), f"star-{n}"))
        modules.append(module_data(clique(n), f"clique-{n}"))
    modules.append(module_data(known_windmill(), "windmill-7"))
    modules.append(windmill_module_data(
        [1, 40, 2400, 200000],
        [9000000, 3800000, 2000000, 920000],
        "windmill-9-high-r",
    ))
    modules.append(windmill_module_data(
        [1, 6, 120, 3500, 60000],
        [9000000, 2500000, 880000, 410000, 190000],
        "windmill-11-high-r",
    ))
    for sample in range(args.samples):
        n = int(rng.integers(3, args.max_n + 1))
        weights = random_module(n, rng, f"random-{sample}")
        modules.append(module_data(weights, f"random-{sample}-n{n}"))

    best = None
    for index, (a, b) in enumerate(itertools.combinations(modules, 2)):
        minimum, bd, db, z = optimize_pair(a, b)
        record = (minimum, bd, db, z, a, b)
        if best is None or minimum > best[0]:
            best = record
            print(
                f"pair={index} min={minimum:.12g} Bd={bd:.12g} dB={db:.12g} "
                f"z={z:.8g} A={a.label} B={b.label}",
                flush=True,
            )
    assert best is not None
    minimum, bd, db, z, a, b = best
    print(json.dumps({
        "minimum": minimum,
        "Bd": bd,
        "dB": db,
        "baseline_limit": 1.0 / 3.0,
        "z": z,
        "A": a.label,
        "B": b.label,
        "weights_A": a.weights.tolist(),
        "weights_B": b.weights.tolist(),
    }, indent=2))


if __name__ == "__main__":
    main()
