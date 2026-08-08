#!/usr/bin/env python3
"""Hostile floating-point search for endpoint product/minimum violations.

Discovery only.  The effective subset chains are constructed directly after
deleting self-loops.  The scale-free edge variables are logarithms on a fixed
connected support.  An independent rational implementation lives in
``verify_endpoint_candidates.py``.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from dataclasses import dataclass

import numpy as np
from scipy.optimize import differential_evolution, minimize


R = 1.5


def baseline(n: int, rule: str) -> float:
    if rule == "Bd":
        return 3.0 ** (n - 1) / (3.0**n - 2.0**n)
    return (n - 1.0) * 3.0 ** (n - 2) / (
        n * (3.0 ** (n - 1) - 2.0 ** (n - 1))
    )


def fixation(weights: np.ndarray, rule: str) -> float:
    """Uniform-singleton fixation from the effective flip chain."""
    n = len(weights)
    full = (1 << n) - 1
    states = range(1, full)
    size = full - 1
    matrix = np.eye(size)
    rhs = np.zeros(size)
    degree = weights.sum(axis=1)
    if np.any(degree <= 0):
        raise FloatingPointError("isolated vertex")

    for state in states:
        row = state - 1
        rates: list[tuple[int, float]] = []
        total = 0.0
        for target in range(n):
            target_mutant = bool(state & (1 << target))
            if rule == "Bd":
                mutant = sum(
                    weights[parent, target] / degree[parent]
                    for parent in range(n)
                    if state & (1 << parent)
                )
                resident = sum(
                    weights[parent, target] / degree[parent]
                    for parent in range(n)
                    if not state & (1 << parent)
                )
                rate = resident if target_mutant else R * mutant
            else:
                mutant = sum(
                    weights[parent, target]
                    for parent in range(n)
                    if state & (1 << parent)
                )
                resident = degree[target] - mutant
                denominator = R * mutant + resident
                if denominator <= 0:
                    raise FloatingPointError("zero replacement mass")
                rate = resident / denominator if target_mutant else R * mutant / denominator
            if rate > 0:
                rates.append((state ^ (1 << target), rate))
                total += rate
        if not total > 1e-280:
            raise FloatingPointError("unresolved effective transition")
        for target, rate in rates:
            probability = rate / total
            if target == full:
                rhs[row] += probability
            elif target:
                matrix[row, target - 1] -= probability

    values = np.linalg.solve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    if residual > 2e-8 or np.min(values) < -2e-8 or np.max(values) > 1 + 2e-8:
        raise FloatingPointError(
            f"ill-conditioned absorption solve: residual={residual}, "
            f"range=({np.min(values)},{np.max(values)})"
        )
    result = sum(values[(1 << vertex) - 1] for vertex in range(n)) / n
    if not -2e-8 <= result <= 1 + 2e-8:
        raise FloatingPointError(f"fixation outside [0,1]: {result}")
    return result


def connected(n: int, edges: tuple[tuple[int, int], ...]) -> bool:
    adjacency = [set() for _ in range(n)]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    reached = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for j in adjacency[i] - reached:
            reached.add(j)
            stack.append(j)
    return len(reached) == n


def matrix_from_logs(
    n: int, edges: tuple[tuple[int, int], ...], logs: np.ndarray
) -> np.ndarray:
    centered = logs - np.mean(logs)
    values = np.exp(np.clip(centered, -350.0, 350.0))
    weights = np.zeros((n, n))
    for (i, j), value in zip(edges, values):
        weights[i, j] = weights[j, i] = value
    return weights


@dataclass(frozen=True)
class Score:
    bd: float
    db: float
    x: float
    y: float
    product: float
    minimum: float
    arithmetic: float


def score(weights: np.ndarray) -> Score:
    n = len(weights)
    bd = fixation(weights, "Bd")
    db = fixation(weights, "dB")
    x = bd / baseline(n, "Bd")
    y = db / baseline(n, "dB")
    return Score(bd, db, x, y, x * y, min(x, y), (x + y) / 2)


def support_from_mask(n: int, mask: int) -> tuple[tuple[int, int], ...]:
    all_edges = tuple(itertools.combinations(range(n), 2))
    return tuple(edge for bit, edge in enumerate(all_edges) if mask & (1 << bit))


def optimize_support(
    n: int,
    edges: tuple[tuple[int, int], ...],
    objective: str,
    span: float,
    seed: int,
    iterations: int,
    popsize: int,
    lam: float = 0.5,
) -> tuple[Score, np.ndarray]:
    dimensions = len(edges)
    cache: dict[tuple[float, ...], tuple[float, Score | None]] = {}

    def loss(logs: np.ndarray) -> float:
        key = tuple(np.round(logs - np.mean(logs), 12))
        if key in cache:
            return cache[key][0]
        try:
            candidate = score(matrix_from_logs(n, edges, logs))
            if objective == "product":
                value = -math.log(candidate.product)
            elif objective == "minimum":
                # Exact nonsmooth objective.  Powell polishing handles the
                # crossing of the two normalized ratios better than a softmin.
                value = -candidate.minimum
            elif objective == "arithmetic":
                value = -candidate.arithmetic
            elif objective == "pareto":
                value = -(lam * candidate.x + (1.0 - lam) * candidate.y)
            else:
                raise ValueError(objective)
        except (FloatingPointError, np.linalg.LinAlgError, ValueError):
            candidate = None
            value = 1e6
        cache[key] = value, candidate
        return value

    bounds = [(-span, span)] * dimensions
    result = differential_evolution(
        loss,
        bounds,
        seed=seed,
        popsize=popsize,
        maxiter=iterations,
        polish=False,
        updating="immediate",
        workers=1,
        tol=1e-9,
        x0=np.zeros(dimensions),
    )
    polished = minimize(
        loss,
        result.x,
        method="Powell",
        bounds=bounds,
        options={"maxiter": max(1000, 30 * dimensions), "xtol": 1e-10, "ftol": 1e-13},
    )
    logs = polished.x if polished.fun <= result.fun else result.x
    weights = matrix_from_logs(n, edges, logs)
    return score(weights), weights


def chosen_supports(n: int, count: int, seed: int):
    all_edges = tuple(itertools.combinations(range(n), 2))
    total = 1 << len(all_edges)
    if n <= 4:
        for mask in range(1, total):
            edges = support_from_mask(n, mask)
            if connected(n, edges):
                yield mask, edges
        return

    # Deliberately include trees, cycles, complete support, weakly completed
    # sparse supports, core-periphery supports, and random irregular supports.
    deterministic: list[tuple[tuple[int, int], ...]] = []
    deterministic.append(all_edges)
    deterministic.append(tuple((i, i + 1) for i in range(n - 1)))
    deterministic.append(tuple((0, i) for i in range(1, n)))
    deterministic.append(
        tuple(sorted(tuple(sorted((i, (i + 1) % n))) for i in range(n)))
    )
    for core in range(2, n):
        edges = list(itertools.combinations(range(core), 2))
        edges.extend((i % core, i) for i in range(core, n))
        deterministic.append(tuple(sorted(set(edges))))
    seen = set()
    for edges in deterministic:
        mask = sum(1 << all_edges.index(edge) for edge in edges)
        if mask not in seen and connected(n, edges):
            seen.add(mask)
            yield mask, edges

    rng = random.Random(seed)
    while len(seen) < count + len(deterministic):
        probability = rng.uniform(0.18, 0.9)
        mask = sum(1 << bit for bit in range(len(all_edges)) if rng.random() < probability)
        edges = support_from_mask(n, mask)
        if mask not in seen and connected(n, edges):
            seen.add(mask)
            yield mask, edges


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--objective", choices=("product", "minimum", "arithmetic", "pareto"), default="minimum")
    parser.add_argument("--lambda", dest="lam", type=float, default=0.5)
    parser.add_argument("--span", type=float, default=14.0)
    parser.add_argument("--iterations", type=int, default=80)
    parser.add_argument("--popsize", type=int, default=8)
    parser.add_argument("--supports", type=int, default=20)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    best: tuple[float, Score, np.ndarray, int] | None = None
    for number, (mask, edges) in enumerate(chosen_supports(args.n, args.supports, args.seed)):
        result, weights = optimize_support(
            args.n,
            edges,
            args.objective,
            args.span,
            args.seed + 104729 * number,
            args.iterations,
            args.popsize,
            args.lam,
        )
        value = {
            "product": result.product,
            "minimum": result.minimum,
            "arithmetic": result.arithmetic,
            "pareto": args.lam * result.x + (1 - args.lam) * result.y,
        }[args.objective]
        record = (value, result, weights, mask)
        if best is None or value > best[0]:
            best = record
            print(json.dumps({
                "support_index": number,
                "support_mask": mask,
                "edge_count": len(edges),
                "objective": args.objective,
                "value": value,
                "x": result.x,
                "y": result.y,
                "P": result.product,
                "M": result.minimum,
                "A": result.arithmetic,
                "weights": weights.tolist(),
            }), flush=True)

    assert best is not None
    value, result, weights, mask = best
    print("BEST", json.dumps({
        "support_mask": mask,
        "objective": args.objective,
        "value": value,
        "x": result.x,
        "y": result.y,
        "P": result.product,
        "M": result.minimum,
        "A": result.arithmetic,
        "weights": weights.tolist(),
    }))


if __name__ == "__main__":
    main()
