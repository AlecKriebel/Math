#!/usr/bin/env python3
"""Adjoint-gradient hostile endpoint search (discovery only).

The full transient subset systems are differentiated analytically with
respect to logarithmic edge weights.  This is substantially cheaper than
finite-difference optimization at orders seven and eight.  Any candidate
still requires the independent rational verifier in this directory.
"""

from __future__ import annotations

import argparse
from itertools import combinations

import numpy as np
from scipy.optimize import minimize


R = 1.5


def baseline(n: int, rule: str) -> float:
    if rule == "Bd":
        return 3.0 ** (n - 1) / (3.0**n - 2.0**n)
    return (n - 1.0) * 3.0 ** (n - 2) / (
        n * (3.0 ** (n - 1) - 2.0 ** (n - 1))
    )


def fixation_gradient(logs: np.ndarray, n: int, rule: str):
    """Return uniform-singleton fixation and its log-edge gradient."""
    edges = list(combinations(range(n), 2))
    logs = np.asarray(logs, dtype=float)
    logs = logs - logs.mean()
    values = np.exp(np.clip(logs, -30.0, 30.0))
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
                    0.0
                    if not next_state
                    else 1.0
                    if next_state == full
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
                    derivative_mutant = (
                        derivative_weight if state & (1 << other) else 0.0
                    )
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
                gradient[edge_index] += (
                    adjoint[state - 1]
                    * derivative_rate
                    * (next_value - state_value)
                )

    return float(initial @ harmonic), gradient


def optimize(n: int, objective: str, starts: int, seed: int, iterations: int):
    dimension = n * (n - 1) // 2
    best = None
    for start in range(starts):
        rng = np.random.default_rng(seed + start)
        initial = rng.normal(0.0, 3.5, dimension)

        def loss(logs):
            bd, bd_gradient = fixation_gradient(logs, n, "Bd")
            db, db_gradient = fixation_gradient(logs, n, "dB")
            x = bd / baseline(n, "Bd")
            y = db / baseline(n, "dB")
            if objective == "product":
                value = np.log(x) + np.log(y)
                gradient = bd_gradient / bd + db_gradient / db
            elif objective == "arithmetic":
                value = (x + y) / 2.0
                gradient = (
                    bd_gradient / baseline(n, "Bd")
                    + db_gradient / baseline(n, "dB")
                ) / 2.0
            else:
                temperature = 0.02
                first = np.exp(-x / temperature)
                second = np.exp(-y / temperature)
                value = -temperature * np.log(first + second)
                gradient = (
                    first * bd_gradient / baseline(n, "Bd")
                    + second * db_gradient / baseline(n, "dB")
                ) / (first + second)
            return -value, -gradient

        result = minimize(
            loss,
            initial,
            jac=True,
            method="L-BFGS-B",
            bounds=[(-14.0, 14.0)] * dimension,
            options={"maxiter": iterations, "ftol": 1e-13, "gtol": 1e-8},
        )
        bd, _ = fixation_gradient(result.x, n, "Bd")
        db, _ = fixation_gradient(result.x, n, "dB")
        x = bd / baseline(n, "Bd")
        y = db / baseline(n, "dB")
        score = {"product": x * y, "arithmetic": (x + y) / 2.0}.get(
            objective, min(x, y)
        )
        print(
            f"{objective} start={start} success={result.success} "
            f"iterations={result.nit} score={score:.15g} x={x:.15g} y={y:.15g}",
            flush=True,
        )
        if best is None or score > best[0]:
            best = score, x, y, result.x - result.x.mean()
    print("BEST", objective, best, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument(
        "--objective", choices=("product", "arithmetic", "softmin"), default="product"
    )
    parser.add_argument("--starts", type=int, default=4)
    parser.add_argument("--seed", type=int, default=260808)
    parser.add_argument("--iterations", type=int, default=100)
    args = parser.parse_args()
    optimize(args.n, args.objective, args.starts, args.seed, args.iterations)


if __name__ == "__main__":
    main()
