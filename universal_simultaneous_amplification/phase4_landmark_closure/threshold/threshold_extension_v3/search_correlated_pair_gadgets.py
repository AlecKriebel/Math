#!/usr/bin/env python3
"""Search weakly correlated strong-pair satellite gadgets.

Each fast module is a strong K2.  Weak pair--core bundles and weak edges
between pair modules occur on the same time scale.  The resulting exact
trace before center establishment is a contact process on subsets of pair
modules with an additional successful-center cemetery state.  This regime
is not the fully absorbed bounded-gadget regime because the inter-pair edges
vanish at the same rate as the core cut.

Floating optimization is discovery only.  All displayed trace rates are
derived directly from Bd/dB replacement events and isolated K2 fixation.
"""

from __future__ import annotations

import argparse
import itertools
import math

import numpy as np
from scipy.optimize import differential_evolution


def trace_rates(
    fitness: float,
    rule: str,
    sigmas: np.ndarray,
    core_loads: np.ndarray,
    pair_loads: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return center-hit, core-recovery, infection, and recovery rates."""
    r = fitness
    k = len(sigmas)
    hit = np.zeros(k)
    loss = np.zeros(k)
    infection = np.zeros((k, k))
    recovery = np.zeros((k, k))
    if rule == "Bd":
        hit = 2.0 * sigmas * (r - 1.0) * core_loads
        loss = 2.0 / (r + 1.0) * core_loads
        for left in range(k):
            for right in range(k):
                if left == right:
                    continue
                y = pair_loads[left, right]
                # Mutant left introduces into resident right; the source
                # degree supplies sigma_left.  The introduced mutant fixes
                # in K2 with probability r/(r+1).
                infection[left, right] = 4.0 * r * r * sigmas[left] * y / (r + 1.0)
                # Resident right introduces into mutant left and fixes at
                # reciprocal fitness with probability 1/(r+1).
                recovery[right, left] = 4.0 * sigmas[right] * y / (r + 1.0)
    elif rule == "dB":
        hit = 2.0 * (r - 1.0) * core_loads
        loss = sigmas / r * core_loads
        for left in range(k):
            for right in range(k):
                if left == right:
                    continue
                y = pair_loads[left, right]
                # Target degree supplies sigma_right.  K2 dB fixation from
                # a mixed state is 1/2 for either relative fitness.
                infection[left, right] = 2.0 * r * sigmas[right] * y
                recovery[right, left] = 2.0 * sigmas[left] * y / r
    else:
        raise ValueError(rule)
    return hit, loss, infection, recovery


def hit_probabilities(
    fitness: float,
    rule: str,
    sigmas: np.ndarray,
    core_loads: np.ndarray,
    pair_loads: np.ndarray,
) -> np.ndarray:
    """Probability of mutant-center establishment from each mutant pair."""
    k = len(sigmas)
    full_mask = (1 << k) - 1
    states = list(range(1, full_mask + 1))
    index = {mask: row for row, mask in enumerate(states)}
    matrix = np.zeros((len(states), len(states)))
    rhs = np.zeros(len(states))
    hit, loss, infection, recovery = trace_rates(
        fitness, rule, sigmas, core_loads, pair_loads
    )
    for mask, row in index.items():
        transitions: dict[int, float] = {}
        success = 0.0
        for left in range(k):
            if not (mask & (1 << left)):
                continue
            success += hit[left]
            lost = mask ^ (1 << left)
            transitions[lost] = transitions.get(lost, 0.0) + loss[left]
            for right in range(k):
                if left == right or (mask & (1 << right)):
                    continue
                gained = mask | (1 << right)
                transitions[gained] = transitions.get(gained, 0.0) + infection[left, right]
                transitions[lost] = transitions.get(lost, 0.0) + recovery[right, left]
        total = success + sum(transitions.values())
        matrix[row, row] = 1.0
        rhs[row] = success / total
        for target, rate in transitions.items():
            if target:
                matrix[row, index[target]] -= rate / total
    harmonic = np.linalg.solve(matrix, rhs)
    return np.array([harmonic[index[1 << vertex]] for vertex in range(k)])


def corrections(
    fitness: float,
    sigmas: np.ndarray,
    core_loads: np.ndarray,
    pair_loads: np.ndarray,
) -> dict[str, object]:
    r = fitness
    p = 1.0 - 1.0 / r
    h_bd = hit_probabilities(r, "Bd", sigmas, core_loads, pair_loads)
    h_db = hit_probabilities(r, "dB", sigmas, core_loads, pair_loads)
    # The singleton first fixes its own fast K2, with the exact local values.
    contribution_bd = r / (r + 1.0) * float(h_bd.mean())
    contribution_db = 0.5 * float(h_db.mean())
    order = 2 * len(sigmas)
    f_bd = order * (contribution_bd / p - 1.0)
    f_db = order * (contribution_db / p - 1.0)
    separator = f_db + (r - 1.0) * f_bd
    leaf_ratio = max(0.0, (r - 1.0) * (f_db - f_bd) / r)
    balanced = min(f_bd + leaf_ratio / (r - 1.0), f_db - leaf_ratio)
    return {
        "balanced": balanced,
        "separator": separator,
        "Bd": f_bd,
        "dB": f_db,
        "lambda": leaf_ratio,
        "h_Bd": h_bd.tolist(),
        "h_dB": h_db.tolist(),
    }


def decode(order: int, parameters: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    edge_count = order * (order - 1) // 2
    sigma_logs = parameters[:order]
    core_logs = parameters[order : 2 * order]
    edge_logs = parameters[2 * order : 2 * order + edge_count]
    # A common multiplier on all weak rates cancels.  Center all weak-load
    # logs together, but leave the physical strong-pair scales independent.
    weak_logs = np.r_[core_logs, edge_logs]
    weak_logs -= weak_logs.mean()
    core_logs = weak_logs[:order]
    edge_logs = weak_logs[order:]
    sigmas = np.exp(sigma_logs)
    core_loads = np.exp(core_logs)
    pair_loads = np.zeros((order, order))
    for (left, right), value in zip(itertools.combinations(range(order), 2), np.exp(edge_logs)):
        pair_loads[left, right] = pair_loads[right, left] = value
    return sigmas, core_loads, pair_loads


def optimize(order: int, fitness: float, bound: float, maxiter: int, seed: int, objective: str) -> dict[str, object]:
    edge_count = order * (order - 1) // 2
    dimension = 2 * order + edge_count

    def target(parameters: np.ndarray) -> float:
        try:
            sigmas, core_loads, pair_loads = decode(order, parameters)
            return -float(corrections(fitness, sigmas, core_loads, pair_loads)[objective])
        except (np.linalg.LinAlgError, FloatingPointError, ZeroDivisionError):
            return 1e9

    result = differential_evolution(
        target,
        [(-bound, bound)] * dimension,
        seed=seed,
        maxiter=maxiter,
        popsize=12,
        polish=True,
        tol=1e-10,
        updating="immediate",
        workers=1,
    )
    sigmas, core_loads, pair_loads = decode(order, result.x)
    score = corrections(fitness, sigmas, core_loads, pair_loads)
    return {
        **score,
        "sigmas": sigmas.tolist(),
        "core_loads": core_loads.tolist(),
        "pair_loads": pair_loads.tolist(),
        "success": bool(result.success),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=2, help="number of fast K2 modules")
    parser.add_argument("--fitness", type=float, default=1.5028569127905696)
    parser.add_argument("--bound", type=float, default=8.0)
    parser.add_argument("--maxiter", type=int, default=300)
    parser.add_argument("--seed", type=int, default=20260808)
    parser.add_argument("--objective", choices=["balanced", "separator"], default="balanced")
    args = parser.parse_args()
    print(optimize(args.order, args.fitness, args.bound, args.maxiter, args.seed, args.objective))


if __name__ == "__main__":
    main()
