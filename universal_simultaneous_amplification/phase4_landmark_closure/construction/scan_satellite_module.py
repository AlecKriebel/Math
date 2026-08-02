#!/usr/bin/env python3
"""Reconnaissance for weakly coupled repeated satellite modules.

Consider a growing complete center with internal weighted degree ``z`` and
many identical copies of a fixed connected weighted module ``H``.  Vertex
``v`` of every module is joined to every center vertex with weight
``epsilon*h[v]``.  In the successive limit epsilon->0, center size->infinity,
and module count/center size->infinity, a uniform singleton begins in a
satellite with probability tending to one.

This file computes the exact finite-module fixation vectors from the defining
chains and evaluates the resulting two-clock overlap criterion.  The scan is
numerical discovery only; it is not a timescale-separation proof.
"""

from __future__ import annotations

import argparse
import itertools

import networkx as nx
import numpy as np
from scipy.optimize import differential_evolution


def fixation_vector(weights: np.ndarray, fitness: float, rule: str) -> tuple[np.ndarray, float]:
    weights = np.asarray(weights, dtype=float)
    size = len(weights)
    full = (1 << size) - 1
    transient = list(range(1, full))
    index = {mask: position for position, mask in enumerate(transient)}
    matrix = np.zeros((len(transient), len(transient)))
    rhs = np.zeros(len(transient))
    degrees = weights.sum(axis=1)
    for mask, row in index.items():
        mutant = np.array([(mask >> v) & 1 for v in range(size)], dtype=float)
        changes = []
        if rule == "Bd":
            total_fitness = size + (fitness - 1) * mutant.sum()
            for target in range(size):
                if mutant[target]:
                    rate = weights[:, target] @ ((1 - mutant) / degrees) / total_fitness
                    target_mask = mask & ~(1 << target)
                else:
                    rate = fitness * weights[:, target] @ (mutant / degrees) / total_fitness
                    target_mask = mask | (1 << target)
                if rate:
                    changes.append((target_mask, float(rate)))
        elif rule == "dB":
            for target in range(size):
                mutant_mass = weights[:, target] @ mutant
                resident_mass = degrees[target] - mutant_mass
                denominator = fitness * mutant_mass + resident_mass
                if mutant[target]:
                    rate = resident_mass / (size * denominator)
                    target_mask = mask & ~(1 << target)
                else:
                    rate = fitness * mutant_mass / (size * denominator)
                    target_mask = mask | (1 << target)
                if rate:
                    changes.append((target_mask, float(rate)))
        else:
            raise ValueError(rule)
        changing_mass = sum(rate for _, rate in changes)
        if not changing_mass > 0:
            raise AssertionError((mask, rule))
        matrix[row, row] = changing_mass
        for target_mask, rate in changes:
            if target_mask == full:
                rhs[row] += rate
            elif target_mask:
                matrix[row, index[target_mask]] -= rate
    values = np.linalg.solve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    singletons = np.array([values[index[1 << v]] for v in range(size)])
    return singletons, residual


def module_data(weights: np.ndarray, fitness: float):
    result = {}
    for rule in ("Bd", "dB"):
        forward, residual_forward = fixation_vector(weights, fitness, rule)
        reverse, residual_reverse = fixation_vector(weights, 1 / fitness, rule)
        if max(residual_forward, residual_reverse) > 2e-9:
            raise AssertionError((rule, residual_forward, residual_reverse))
        result[rule] = (forward, reverse)
    return result


def z_interval(weights: np.ndarray, fitness: float, attachment: np.ndarray):
    """Return the separated-limit open interval (z_B, z_D), if meaningful."""
    degrees = weights.sum(axis=1)
    attachment = np.asarray(attachment, dtype=float)
    if np.any(attachment < 0) or not attachment.sum() > 0:
        raise ValueError("attachment vector must be nonnegative and nonzero")
    data = module_data(weights, fitness)
    q = 1 - 1 / fitness
    alpha_bd = float(data["Bd"][0].mean())
    alpha_db = float(data["dB"][0].mean())
    if alpha_bd <= q or alpha_db <= q:
        return None, (alpha_bd, alpha_db), data
    beta_bd = data["Bd"][1]
    beta_db = data["dB"][1]
    x = float(np.sum(attachment / degrees))
    total = float(np.sum(attachment))
    y_bd = float(attachment @ beta_bd)
    y_db = float((attachment / degrees) @ beta_db)
    lower = q * y_bd / ((fitness - 1) * x * (alpha_bd - q))
    upper = fitness * (fitness - 1) * total * (alpha_db - q) / (q * y_db)
    return (lower, upper), (alpha_bd, alpha_db), data


def optimize_attachment(weights: np.ndarray, fitness: float, seed: int = 1):
    """Maximize log(z_D/z_B) over attachment weights, up to common scale."""
    data = module_data(weights, fitness)
    q = 1 - 1 / fitness
    alpha_bd = float(data["Bd"][0].mean())
    alpha_db = float(data["dB"][0].mean())
    if alpha_bd <= q or alpha_db <= q:
        return -np.inf, np.ones(len(weights)), None, (alpha_bd, alpha_db)
    degrees = weights.sum(axis=1)
    beta_bd = data["Bd"][1]
    beta_db = data["dB"][1]

    def score(log_attachment):
        attachment = np.exp(log_attachment - np.max(log_attachment))
        x = np.sum(attachment / degrees)
        total = np.sum(attachment)
        y_bd = attachment @ beta_bd
        y_db = (attachment / degrees) @ beta_db
        return float(
            np.log(x) + np.log(total) - np.log(y_bd) - np.log(y_db)
        )

    candidates = []
    for vertex in range(len(weights)):
        logs = np.full(len(weights), -20.0)
        logs[vertex] = 0.0
        candidates.append(logs)
    candidates.append(np.zeros(len(weights)))
    result = differential_evolution(
        lambda logs: -score(logs),
        [(-20, 0)] * len(weights),
        maxiter=50,
        popsize=6,
        polish=True,
        seed=seed,
        workers=1,
        updating="immediate",
    )
    candidates.append(result.x)
    best_logs = max(candidates, key=score)
    attachment = np.exp(best_logs - np.max(best_logs))
    interval, _, _ = z_interval(weights, fitness, attachment)
    if interval is None:
        return -np.inf, attachment, None, (alpha_bd, alpha_db)
    lower, upper = interval
    return float(np.log(upper / lower)), attachment, interval, (alpha_bd, alpha_db)


def atlas_scan(max_size: int, fitnesses: tuple[float, ...], top: int):
    records = []
    for graph_id, graph in enumerate(nx.graph_atlas_g()):
        size = len(graph)
        if size < 2 or size > max_size or not nx.is_connected(graph):
            continue
        weights = nx.to_numpy_array(graph, dtype=float)
        for fitness in fitnesses:
            score, attachment, interval, alphas = optimize_attachment(
                weights, fitness, seed=1009 * graph_id + round(100 * fitness)
            )
            records.append((score, graph_id, fitness, weights, attachment, interval, alphas))
    for score, graph_id, fitness, weights, attachment, interval, alphas in sorted(
        records, key=lambda item: item[0], reverse=True
    )[:top]:
        edges = [tuple(map(int, edge)) for edge in np.argwhere(np.triu(weights) > 0)]
        print(
            f"score={score:+.8g} atlas={graph_id} size={len(weights)} r={fitness:g} "
            f"alphas=({alphas[0]:.9g},{alphas[1]:.9g}) interval={interval}"
        )
        print(" edges", edges)
        print(" attach", np.array2string(attachment, precision=6, suppress_small=True))


def complete_graph_check(max_size: int, fitnesses: tuple[float, ...]):
    for size in range(2, max_size + 1):
        weights = np.ones((size, size)) - np.eye(size)
        for fitness in fitnesses:
            score, attachment, interval, alphas = optimize_attachment(weights, fitness)
            print(
                f"K{size} r={fitness:g} log-ratio={score:+.8g} "
                f"interval={interval} alphas={alphas}"
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-size", type=int, default=6)
    parser.add_argument("--fitness", type=float, nargs="+", default=(1.05, 1.1, 1.2, 1.3, 1.5))
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--complete-only", action="store_true")
    args = parser.parse_args()
    if args.complete_only:
        complete_graph_check(args.max_size, tuple(args.fitness))
    else:
        atlas_scan(args.max_size, tuple(args.fitness), args.top)


if __name__ == "__main__":
    main()
