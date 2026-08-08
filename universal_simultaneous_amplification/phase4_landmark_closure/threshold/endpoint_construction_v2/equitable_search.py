#!/usr/bin/env python3
"""Floating endpoint search over equitable weighted vertex classes.

Discovery only.  A graph is specified by class sizes ``sizes[a]`` and a
symmetric matrix ``weights[a,b]``.  Distinct vertices in classes ``a,b``
are joined with that weight; diagonal matrix entries are within-class edge
weights (there are no graph loops).

The mutant count vector is a strong lumping: all vertices with the same
class label have identical weighted neighbourhoods, and every type-changing
rate depends only on the mutant counts.  The transient harmonic equations
are solved with a sparse direct solver.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def complete_baseline(n: int, r: float, rule: str) -> float:
    if rule == "Bd":
        return (1.0 - 1.0 / r) / (1.0 - r ** (-n))
    # From the one-dimensional complete-graph chain.  The singleton step
    # has a distinct boundary ratio; after it, every interior down/up ratio
    # is 1/r.  This is algebraically the formula used throughout the project.
    return (n - 1.0) / n * (1.0 - 1.0 / r) / (
        1.0 - r ** (-(n - 1))
    )


def state_space(sizes: tuple[int, ...]):
    states = list(itertools.product(*(range(size + 1) for size in sizes)))
    empty = tuple(0 for _ in sizes)
    full = sizes
    transient = [state for state in states if state not in (empty, full)]
    return transient, {state: index for index, state in enumerate(transient)}


def flip_rates(
    state: tuple[int, ...],
    sizes: tuple[int, ...],
    weights: np.ndarray,
    r: float,
    rule: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Return aggregate increase/decrease rates for each target class."""
    mutant = np.asarray(state, dtype=float)
    resident = np.asarray(sizes, dtype=float) - mutant
    classes = len(sizes)
    degree = np.empty(classes)
    for a in range(classes):
        degree[a] = sum(
            weights[a, b] * (sizes[b] - (1 if a == b else 0))
            for b in range(classes)
        )
    if np.any(degree <= 0):
        raise FloatingPointError("isolated class")

    increase = np.zeros(classes)
    decrease = np.zeros(classes)
    if rule == "Bd":
        # The common total-fitness denominator cancels after deleting
        # no-change events.  For target class b, sum over reproducer class a.
        for b in range(classes):
            incoming_mutant = sum(
                mutant[a] * weights[a, b] / degree[a]
                for a in range(classes)
            )
            incoming_resident = sum(
                resident[a] * weights[a, b] / degree[a]
                for a in range(classes)
            )
            increase[b] = r * resident[b] * incoming_mutant
            decrease[b] = mutant[b] * incoming_resident
    elif rule == "dB":
        # Each possible death vertex has the same 1/n factor, also common to
        # all type-changing rates.  Parent totals exclude the dead vertex.
        for b in range(classes):
            if resident[b] > 0:
                mutant_mass = sum(weights[a, b] * mutant[a] for a in range(classes))
                resident_mass = sum(weights[a, b] * resident[a] for a in range(classes)) - weights[b, b]
                denominator = r * mutant_mass + resident_mass
                if denominator > 0:
                    increase[b] = resident[b] * r * mutant_mass / denominator
            if mutant[b] > 0:
                mutant_mass = sum(weights[a, b] * mutant[a] for a in range(classes)) - weights[b, b]
                resident_mass = sum(weights[a, b] * resident[a] for a in range(classes))
                denominator = r * mutant_mass + resident_mass
                if denominator > 0:
                    decrease[b] = mutant[b] * resident_mass / denominator
    else:
        raise ValueError(rule)
    return increase, decrease


def fixation(
    sizes: tuple[int, ...], weights: np.ndarray, r: float, rule: str
) -> float:
    transient, index = state_space(sizes)
    full = sizes
    rows: list[int] = []
    columns: list[int] = []
    data: list[float] = []
    rhs = np.zeros(len(transient))

    for row, state in enumerate(transient):
        increase, decrease = flip_rates(state, sizes, weights, r, rule)
        total = float(increase.sum() + decrease.sum())
        if not total > 1e-290:
            raise FloatingPointError(f"unresolved state {state}")
        rows.append(row)
        columns.append(row)
        data.append(1.0)
        for b in range(len(sizes)):
            for direction, rate in ((1, increase[b]), (-1, decrease[b])):
                if not rate:
                    continue
                target = list(state)
                target[b] += direction
                target_tuple = tuple(target)
                probability = float(rate / total)
                if target_tuple == full:
                    rhs[row] += probability
                elif any(target_tuple):
                    rows.append(row)
                    columns.append(index[target_tuple])
                    data.append(-probability)

    matrix = coo_matrix((data, (rows, columns)), shape=(len(transient),) * 2).tocsr()
    harmonic = spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ harmonic - rhs)))
    if not np.all(np.isfinite(harmonic)) or residual > 5e-8:
        raise FloatingPointError(f"bad solve residual={residual}")
    if float(harmonic.min()) < -5e-7 or float(harmonic.max()) > 1 + 5e-7:
        raise FloatingPointError("harmonic range failure")
    n = sum(sizes)
    answer = 0.0
    for b, size in enumerate(sizes):
        singleton = tuple(1 if a == b else 0 for a in range(len(sizes)))
        answer += size * harmonic[index[singleton]] / n
    return float(answer)


@dataclass(frozen=True)
class Score:
    bd: float
    db: float
    x: float
    y: float

    @property
    def minimum(self) -> float:
        return min(self.x, self.y)


def score(sizes: tuple[int, ...], weights: np.ndarray, r: float = 1.5) -> Score:
    n = sum(sizes)
    bd = fixation(sizes, weights, r, "Bd")
    db = fixation(sizes, weights, r, "dB")
    return Score(
        bd,
        db,
        bd / complete_baseline(n, r, "Bd"),
        db / complete_baseline(n, r, "dB"),
    )


def support_pairs(classes: int, support: str):
    all_pairs = list(itertools.combinations_with_replacement(range(classes), 2))
    if support == "complete":
        return all_pairs
    if support == "portal":
        # Classes: bulk, portal, blade.  No direct bulk--blade edge.
        if classes != 3:
            raise ValueError("portal support requires three classes")
        return [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]
    if support == "portal-no-blade":
        if classes != 3:
            raise ValueError("portal support requires three classes")
        return [(0, 0), (0, 1), (1, 1), (1, 2)]
    if support == "chain":
        return [(a, a) for a in range(classes)] + [
            (a, a + 1) for a in range(classes - 1)
        ]
    raise ValueError(support)


def matrix_from_logs(classes: int, pairs, logs: np.ndarray) -> np.ndarray:
    centered = np.asarray(logs, dtype=float) - float(np.mean(logs))
    values = np.exp(np.clip(centered, -80.0, 80.0))
    weights = np.zeros((classes, classes))
    for (a, b), value in zip(pairs, values):
        weights[a, b] = weights[b, a] = value
    return weights


def optimize(
    sizes: tuple[int, ...],
    support: str,
    span: float,
    iterations: int,
    popsize: int,
    seed: int,
    r: float,
):
    pairs = support_pairs(len(sizes), support)
    cache: dict[tuple[float, ...], float] = {}

    def loss(logs):
        key = tuple(np.round(np.asarray(logs) - np.mean(logs), 10))
        if key in cache:
            return cache[key]
        try:
            candidate = score(sizes, matrix_from_logs(len(sizes), pairs, logs), r)
            # A smooth conservative surrogate is useful away from x=y; final
            # polishing uses the exact minimum below.
            temperature = 0.005
            center = min(candidate.x, candidate.y)
            smooth = center - temperature * math.log(
                math.exp(-(candidate.x - center) / temperature)
                + math.exp(-(candidate.y - center) / temperature)
            )
            value = -smooth
        except (FloatingPointError, ValueError, ArithmeticError):
            value = 1e6
        cache[key] = value
        return value

    bounds = [(-span, span)] * len(pairs)
    result = differential_evolution(
        loss,
        bounds,
        seed=seed,
        maxiter=iterations,
        popsize=popsize,
        polish=False,
        updating="immediate",
        workers=1,
        tol=1e-8,
        x0=np.zeros(len(pairs)),
    )

    def exact_min_loss(logs):
        try:
            candidate = score(sizes, matrix_from_logs(len(sizes), pairs, logs), r)
            return -candidate.minimum
        except (FloatingPointError, ValueError, ArithmeticError):
            return 1e6

    polished = minimize(
        exact_min_loss,
        result.x,
        method="Powell",
        bounds=bounds,
        options={"maxiter": 1200, "xtol": 1e-9, "ftol": 1e-12},
    )
    logs = polished.x if polished.fun <= exact_min_loss(result.x) else result.x
    weights = matrix_from_logs(len(sizes), pairs, logs)
    return score(sizes, weights, r), weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="12,2,6")
    parser.add_argument(
        "--support", choices=("complete", "portal", "portal-no-blade", "chain"), default="complete"
    )
    parser.add_argument("--r", type=float, default=1.5)
    parser.add_argument("--span", type=float, default=12.0)
    parser.add_argument("--iterations", type=int, default=60)
    parser.add_argument("--popsize", type=int, default=7)
    parser.add_argument("--seed", type=int, default=260808)
    args = parser.parse_args()
    sizes = tuple(int(value) for value in args.sizes.split(","))
    candidate, weights = optimize(
        sizes, args.support, args.span, args.iterations, args.popsize, args.seed, args.r
    )
    print(json.dumps({
        "sizes": sizes,
        "support": args.support,
        "r": args.r,
        "x": candidate.x,
        "y": candidate.y,
        "M": candidate.minimum,
        "bd": candidate.bd,
        "db": candidate.db,
        "weights": weights.tolist(),
    }, indent=2))


if __name__ == "__main__":
    main()
