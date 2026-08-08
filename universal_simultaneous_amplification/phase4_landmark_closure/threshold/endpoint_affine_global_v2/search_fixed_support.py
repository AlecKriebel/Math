#!/usr/bin/env python3
"""Adjoint-gradient search on one fixed connected support.

Only existing support edges are varied.  This avoids treating structural
zeros as ill-conditioned tiny positive edges.  Discovery results are not
certificates.
"""

from __future__ import annotations

import argparse

import networkx as nx
import numpy as np
from scipy.optimize import minimize


R = 1.5


def baseline(n: int, rule: str) -> float:
    if rule == "Bd":
        return 3.0 ** (n - 1) / (3.0**n - 2.0**n)
    return (n - 1.0) * 3.0 ** (n - 2) / (
        n * (3.0 ** (n - 1) - 2.0 ** (n - 1))
    )


def fixation_gradient(logs: np.ndarray, n: int, edges, rule: str):
    logs = np.asarray(logs, dtype=float)
    logs = logs - logs.mean()
    values = np.exp(np.clip(logs, -25.0, 25.0))
    weights = np.zeros((n, n))
    for (a, b), value in zip(edges, values):
        weights[a, b] = weights[b, a] = value
    degree = weights.sum(axis=1)
    kernel = weights / degree[:, None]
    full = (1 << n) - 1
    transient_count = full - 1
    matrix = np.zeros((transient_count, transient_count))
    rhs = np.zeros(transient_count)

    def rate(state: int, target: int) -> float:
        target_mutant = bool(state & (1 << target))
        if rule == "Bd":
            value = sum(
                kernel[parent, target]
                for parent in range(n)
                if bool(state & (1 << parent)) != target_mutant
            )
            return value if target_mutant else R * value
        mutant = sum(
            weights[parent, target]
            for parent in range(n)
            if state & (1 << parent)
        )
        resident = degree[target] - mutant
        denominator = R * mutant + resident
        return resident / denominator if target_mutant else R * mutant / denominator

    for state in range(1, full):
        row = state - 1
        for target in range(n):
            value = rate(state, target)
            if not value:
                continue
            next_state = state ^ (1 << target)
            matrix[row, row] += value
            if next_state == full:
                rhs[row] += value
            elif next_state:
                matrix[row, next_state - 1] -= value

    harmonic = np.linalg.solve(matrix, rhs)
    initial = np.zeros(transient_count)
    for vertex in range(n):
        initial[(1 << vertex) - 1] = 1.0 / n
    adjoint = np.linalg.solve(matrix.T, initial)
    gradient = np.zeros(len(edges))

    for edge_index, (a, b) in enumerate(edges):
        derivative_kernel = np.zeros((n, n))
        for parent, other in ((a, b), (b, a)):
            for child in range(n):
                derivative_kernel[parent, child] = kernel[parent, child] * (
                    float(child == other) - kernel[parent, other]
                )

        for state in range(1, full):
            state_value = harmonic[state - 1]
            for target in range(n):
                target_mutant = bool(state & (1 << target))
                next_state = state ^ (1 << target)
                next_value = (
                    0.0 if not next_state else 1.0 if next_state == full
                    else harmonic[next_state - 1]
                )
                if rule == "Bd":
                    derivative_rate = sum(
                        derivative_kernel[parent, target]
                        for parent in range(n)
                        if bool(state & (1 << parent)) != target_mutant
                    )
                    if not target_mutant:
                        derivative_rate *= R
                elif target not in (a, b):
                    derivative_rate = 0.0
                else:
                    mutant = sum(
                        weights[parent, target]
                        for parent in range(n)
                        if state & (1 << parent)
                    )
                    resident = degree[target] - mutant
                    denominator = R * mutant + resident
                    other = b if target == a else a
                    derivative_weight = weights[target, other]
                    derivative_mutant = derivative_weight if state & (1 << other) else 0.0
                    derivative_resident = derivative_weight - derivative_mutant
                    derivative_denominator = R * derivative_mutant + derivative_resident
                    if target_mutant:
                        derivative_rate = (
                            derivative_resident * denominator
                            - resident * derivative_denominator
                        ) / denominator**2
                    else:
                        derivative_rate = R * (
                            derivative_mutant * denominator
                            - mutant * derivative_denominator
                        ) / denominator**2
                gradient[edge_index] += adjoint[state - 1] * derivative_rate * (
                    next_value - state_value
                )
    return float(initial @ harmonic), gradient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--atlas", type=int, required=True)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--scale", type=float, default=4.0)
    parser.add_argument("--iterations", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260808)
    args = parser.parse_args()
    graph = nx.graph_atlas(args.atlas)
    if not nx.is_connected(graph):
        raise ValueError("support is not connected")
    n = len(graph)
    edges = tuple(sorted(tuple(sorted(edge)) for edge in graph.edges()))
    best = None
    for start in range(args.starts):
        rng = np.random.default_rng(args.seed + 1009 * start)
        initial = rng.normal(0.0, args.scale, len(edges))

        def loss(logs):
            bd, gb = fixation_gradient(logs, n, edges, "Bd")
            db, gd = fixation_gradient(logs, n, edges, "dB")
            x = bd / baseline(n, "Bd")
            y = db / baseline(n, "dB")
            return -(x + 2.0 * y) / 3.0, -(
                gb / baseline(n, "Bd") + 2.0 * gd / baseline(n, "dB")
            ) / 3.0

        result = minimize(
            loss,
            initial,
            jac=True,
            method="L-BFGS-B",
            bounds=[(-18.0, 18.0)] * len(edges),
            options={"maxiter": args.iterations, "ftol": 1e-14, "gtol": 1e-9},
        )
        bd, _ = fixation_gradient(result.x, n, edges, "Bd")
        db, _ = fixation_gradient(result.x, n, edges, "dB")
        x = bd / baseline(n, "Bd")
        y = db / baseline(n, "dB")
        score = (x + 2.0 * y) / 3.0
        centered = result.x - result.x.mean()
        record = (score, x, y, centered)
        if best is None or score > best[0]:
            best = record
        print(
            f"start={start} score={score:.16g} x={x:.16g} y={y:.16g} "
            f"nit={result.nit} success={result.success} spread={centered.max()-centered.min():.8g}",
            flush=True,
        )
    print("EDGES", edges)
    print("BEST", best)


if __name__ == "__main__":
    main()
