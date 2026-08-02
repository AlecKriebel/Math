#!/usr/bin/env python3
"""Unrestricted numerical search for dB fixation above the complete graph.

All transition equations are built directly from death--birth updating.  The
floating-point optimizer is reconnaissance only.  Apparent positive excesses
must be rationalized and checked by the independent exact solver.
"""

from __future__ import annotations

import argparse
import itertools

import networkx as nx
import numpy as np
import scipy.linalg
from scipy.optimize import differential_evolution, minimize


def baseline(size: int, fitness: float) -> float:
    """Complete-graph dB baseline."""
    return (size - 1) / size * (1 - 1 / fitness) / (
        1 - fitness ** (-(size - 1))
    )


def baseline_bd(size: int, fitness: float) -> float:
    return (1 - 1 / fitness) / (1 - fitness ** (-size))


def _solve_from_raw_rates(
    states: np.ndarray,
    mutant: np.ndarray,
    raw_rates: np.ndarray,
    next_masks: np.ndarray,
):
    size = mutant.shape[1]
    full = (1 << size) - 1
    index = np.full(full + 1, -1, dtype=np.int64)
    index[states] = np.arange(len(states), dtype=np.int64)
    changing_mass = raw_rates.sum(axis=1)
    if np.any(changing_mass <= 0):
        raise AssertionError(states[changing_mass <= 0])
    rates = raw_rates / changing_mass[:, None]
    matrix = np.eye(len(states))
    rhs = np.zeros(len(states))
    rows = np.arange(len(states))
    for target in range(size):
        targets = next_masks[:, target]
        probabilities = rates[:, target]
        fixation_rows = targets == full
        rhs[fixation_rows] += probabilities[fixation_rows]
        transient_rows = (targets > 0) & (targets < full) & (probabilities > 0)
        matrix[rows[transient_rows], index[targets[transient_rows]]] -= probabilities[
            transient_rows
        ]
    values = scipy.linalg.solve(
        matrix, rhs, assume_a="gen", check_finite=False, overwrite_a=True
    )
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    singletons = np.array([values[index[1 << vertex]] for vertex in range(size)])
    return float(singletons.mean()), residual, singletons


def fixation(weights: np.ndarray, fitness: float) -> tuple[float, float, np.ndarray]:
    """Return uniform-singleton dB fixation, residual, and singleton vector."""
    weights = np.asarray(weights, dtype=float)
    size = len(weights)
    full = (1 << size) - 1
    states = np.arange(1, full, dtype=np.int64)
    mutant = ((states[:, None] >> np.arange(size)) & 1).astype(bool)
    degrees = weights.sum(axis=1)
    if np.any(degrees <= 0):
        raise ValueError("isolated vertex")
    raw_rates = np.zeros((len(states), size), dtype=float)
    next_masks = np.zeros((len(states), size), dtype=np.int64)
    for target in range(size):
        # Matrix products only add nonnegative terms, so even extremely rare
        # bridge weights are retained without subtractive cancellation.
        mutant_mass = mutant.astype(float) @ weights[:, target]
        resident_mass = (~mutant).astype(float) @ weights[:, target]
        denominator = fitness * mutant_mass + resident_mass
        target_is_mutant = mutant[:, target]
        raw_rates[:, target] = np.where(
            target_is_mutant,
            resident_mass / (size * denominator),
            fitness * mutant_mass / (size * denominator),
        )
        next_masks[:, target] = np.where(
            target_is_mutant,
            states & ~(1 << target),
            states | (1 << target),
        )
    return _solve_from_raw_rates(states, mutant, raw_rates, next_masks)


def fixation_bd(weights: np.ndarray, fitness: float):
    """Cancellation-safe exact-state Bd fixation in floating arithmetic."""
    weights = np.asarray(weights, dtype=float)
    size = len(weights)
    full = (1 << size) - 1
    states = np.arange(1, full, dtype=np.int64)
    mutant = ((states[:, None] >> np.arange(size)) & 1).astype(bool)
    degrees = weights.sum(axis=1)
    if np.any(degrees <= 0):
        raise ValueError("isolated vertex")
    transition = weights / degrees[:, None]
    raw_rates = np.zeros((len(states), size), dtype=float)
    next_masks = np.zeros((len(states), size), dtype=np.int64)
    for target in range(size):
        mutant_source_mass = mutant.astype(float) @ transition[:, target]
        resident_source_mass = (~mutant).astype(float) @ transition[:, target]
        target_is_mutant = mutant[:, target]
        raw_rates[:, target] = np.where(
            target_is_mutant,
            resident_source_mass,
            fitness * mutant_source_mass,
        )
        next_masks[:, target] = np.where(
            target_is_mutant,
            states & ~(1 << target),
            states | (1 << target),
        )
    return _solve_from_raw_rates(states, mutant, raw_rates, next_masks)


def edge_list_from_support(support: np.ndarray):
    return [
        (i, j)
        for i in range(len(support))
        for j in range(i + 1, len(support))
        if support[i, j]
    ]


def weights_from_logs(support: np.ndarray, logs: np.ndarray):
    edges = edge_list_from_support(support)
    logs = np.asarray(logs, dtype=float)
    logs = logs - logs.mean()
    weights = np.zeros_like(support, dtype=float)
    for (i, j), value in zip(edges, np.exp(logs)):
        weights[i, j] = weights[j, i] = value
    return weights


def optimize_support(
    support: np.ndarray,
    fitness: float,
    iterations: int,
    seed: int,
    log_bound: float,
    rule: str = "dB",
):
    edges = edge_list_from_support(support)
    dimension = len(edges)
    if rule == "dB":
        target = baseline(len(support), fitness)
    elif rule == "Bd":
        target = baseline_bd(len(support), fitness)
    elif rule == "sum":
        target = baseline(len(support), fitness) + baseline_bd(len(support), fitness)
    else:
        raise ValueError(rule)

    def evaluate(weights):
        if rule == "dB":
            return fixation(weights, fitness)
        if rule == "Bd":
            return fixation_bd(weights, fitness)
        db_value, db_residual, db_singletons = fixation(weights, fitness)
        bd_value, bd_residual, bd_singletons = fixation_bd(weights, fitness)
        return (
            db_value + bd_value,
            max(db_residual, bd_residual),
            db_singletons + bd_singletons,
        )

    def objective(logs):
        weights = weights_from_logs(support, logs)
        try:
            value, residual, _ = evaluate(weights)
        except (ValueError, np.linalg.LinAlgError):
            return 1.0
        upper_value = 2.0 if rule == "sum" else 1.0
        if (
            residual > 2e-7
            or not np.isfinite(value)
            or value < -1e-9
            or value > upper_value + 1e-9
        ):
            return 1.0
        return target - value

    result = differential_evolution(
        objective,
        [(-log_bound, log_bound)] * dimension,
        maxiter=iterations,
        popsize=7,
        polish=False,
        seed=seed,
        workers=1,
        updating="immediate",
        disp=False,
    )
    rng = np.random.default_rng(seed + 17)
    starts = [result.x, np.zeros(dimension)]
    for scale in (0.05, 0.2, 0.8, 2.0, 5.0):
        starts.extend(rng.normal(0, scale, size=(2, dimension)))
    candidates = [(objective(start), start) for start in starts]
    for start in starts:
        polished = minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=[(-log_bound, log_bound)] * dimension,
            options={"maxiter": max(500, 50 * dimension), "ftol": 1e-15, "gtol": 1e-9},
        )
        candidates.append((float(polished.fun), polished.x))
    _, logs = min(candidates, key=lambda item: item[0])
    weights = weights_from_logs(support, logs)
    value, residual, singletons = evaluate(weights)
    return {
        "excess": value - target,
        "value": value,
        "residual": residual,
        "weights": weights,
        "logs": logs - logs.mean(),
        "singletons": singletons,
        "edges": edges,
    }


def complete_support(size: int):
    return np.ones((size, size), dtype=float) - np.eye(size)


def connected_atlas_supports(size: int):
    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        if len(graph) == size and nx.is_connected(graph):
            yield atlas_id, nx.to_numpy_array(graph, dtype=float)


def print_result(label: str, result, compact: bool = False):
    print(
        f"{label} excess={result['excess']:+.12g} value={result['value']:.12g} "
        f"residual={result['residual']:.2e}"
    )
    if compact:
        return
    np.set_printoptions(precision=10, suppress=True, linewidth=220)
    print("singletons", result["singletons"])
    print("logs", result["logs"])
    print("weights")
    print(result["weights"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--fitness", type=float, required=True)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--restarts", type=int, default=4)
    parser.add_argument("--seed-offset", type=int, default=0)
    parser.add_argument("--log-bound", type=float, default=12.0)
    parser.add_argument("--rule", choices=("dB", "Bd", "sum"), default="dB")
    parser.add_argument("--atlas", action="store_true")
    parser.add_argument("--atlas-start", type=int, default=0)
    parser.add_argument("--atlas-limit", type=int, default=0)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    if args.atlas:
        records = []
        for ordinal, (atlas_id, support) in enumerate(connected_atlas_supports(args.size)):
            if ordinal < args.atlas_start:
                continue
            if args.atlas_limit and ordinal >= args.atlas_start + args.atlas_limit:
                break
            result = optimize_support(
                support,
                args.fitness,
                args.iterations,
                seed=100003 * atlas_id + 97 + args.seed_offset,
                log_bound=args.log_bound,
                rule=args.rule,
            )
            records.append((result["excess"], atlas_id, result))
            if result["excess"] > 1e-8:
                print_result(f"COUNTEREXAMPLE atlas={atlas_id}", result, args.compact)
        print(f"searched {len(records)} connected atlas supports")
        for _, atlas_id, result in sorted(records, reverse=True, key=lambda item: item[0])[:10]:
            print_result(f"TOP atlas={atlas_id}", result, args.compact)
    else:
        support = complete_support(args.size)
        records = []
        for restart in range(args.restarts):
            result = optimize_support(
                support,
                args.fitness,
                args.iterations,
                seed=(1009 * args.size + 7919 * restart
                      + round(1000 * args.fitness) + args.seed_offset),
                log_bound=args.log_bound,
                rule=args.rule,
            )
            records.append(result)
            print_result(f"restart={restart}", result, args.compact)
        print_result("BEST", max(records, key=lambda result: result["excess"]), args.compact)


if __name__ == "__main__":
    main()
