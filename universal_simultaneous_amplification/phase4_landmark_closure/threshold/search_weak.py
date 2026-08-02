#!/usr/bin/env python3
"""First-principles reconnaissance for simultaneous weak amplification.

The program solves the two-lineage neutral meeting equations by iteration and
substitutes them into the independently derived weak-selection coefficients.
All calculations in this file are floating-point reconnaissance.  A printed
candidate is not a theorem.
"""

from __future__ import annotations

import argparse
import math
import random
from typing import Iterable, Sequence


Matrix = list[list[float]]


def solve_linear(matrix: Matrix, rhs: list[float]) -> list[float]:
    """Dense partial-pivoting elimination for small reconnaissance systems."""
    n = len(rhs)
    augmented = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda i: abs(augmented[i][column]))
        if abs(augmented[pivot][column]) < 1e-15:
            raise RuntimeError("singular meeting-time system")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        for j in range(column, n + 1):
            augmented[column][j] /= scale
        for i in range(column + 1, n):
            scale = augmented[i][column]
            if not scale:
                continue
            for j in range(column, n + 1):
                augmented[i][j] -= scale * augmented[column][j]
    solution = [0.0] * n
    for i in range(n - 1, -1, -1):
        solution[i] = augmented[i][n] - sum(
            augmented[i][j] * solution[j] for j in range(i + 1, n)
        )
    return solution


def meeting_times_direct(weights: Matrix, rule: str) -> Matrix:
    n = len(weights)
    degree = [sum(row) for row in weights]
    if min(degree) <= 0:
        raise ValueError("isolated vertex")
    if rule == "Bd":
        rate = [[weights[i][j] / degree[j] for j in range(n)] for i in range(n)]
    elif rule == "dB":
        rate = [[weights[i][j] / degree[i] for j in range(n)] for i in range(n)]
    else:
        raise ValueError(rule)
    leave = [sum(row) for row in rate]
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    index = {pair: k for k, pair in enumerate(pairs)}
    matrix = [[0.0] * len(pairs) for _ in pairs]
    for row, (i, j) in enumerate(pairs):
        matrix[row][row] = leave[i] + leave[j]
        for k in range(n):
            if k != j:
                pair = tuple(sorted((k, j)))
                matrix[row][index[pair]] -= rate[i][k]
            if k != i:
                pair = tuple(sorted((i, k)))
                matrix[row][index[pair]] -= rate[j][k]
    values = solve_linear(matrix, [1.0] * len(pairs))
    h = [[0.0] * n for _ in range(n)]
    for pair, value in zip(pairs, values):
        i, j = pair
        h[i][j] = h[j][i] = value
    return h


def meeting_times(weights: Matrix, rule: str, tolerance: float = 2e-12) -> Matrix:
    n = len(weights)
    degree = [sum(row) for row in weights]
    if min(degree) <= 0:
        raise ValueError("isolated vertex")
    if rule == "Bd":
        rate = [[weights[i][j] / degree[j] for j in range(n)] for i in range(n)]
    elif rule == "dB":
        rate = [[weights[i][j] / degree[i] for j in range(n)] for i in range(n)]
    else:
        raise ValueError(rule)
    leave = [sum(row) for row in rate]
    h = [[0.0] * n for _ in range(n)]
    for iteration in range(2_000_000):
        error = 0.0
        # Symmetric pair meeting times; alternate direction to reduce ordering bias.
        irange = range(n) if iteration % 2 == 0 else range(n - 1, -1, -1)
        for i in irange:
            jrange = range(i + 1, n) if iteration % 2 == 0 else range(n - 1, i, -1)
            for j in jrange:
                value = 1.0
                value += sum(rate[i][k] * h[min(k, j)][max(k, j)] for k in range(n) if k != j)
                value += sum(rate[j][k] * h[min(i, k)][max(i, k)] for k in range(n) if k != i)
                value /= leave[i] + leave[j]
                error = max(error, abs(value - h[i][j]))
                h[i][j] = h[j][i] = value
        if error < tolerance:
            return h
    raise RuntimeError("meeting-time iteration failed")


def weak_coefficients(weights: Matrix) -> tuple[float, float]:
    n = len(weights)
    degree = [sum(row) for row in weights]
    total_degree = sum(degree)
    harmonic = sum(1.0 / d for d in degree)
    c = 1.0 / harmonic
    h_bd = meeting_times_direct(weights, "Bd")
    h_db = meeting_times_direct(weights, "dB")
    # h is continuous-time meeting time; tau=n*h in the inherited formulas.
    c_bd = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            c_bd += weights[i][j] * h_bd[i][j] / (degree[i] * degree[j])
    c_bd *= 2.0 * c / n
    c_db = 0.0
    for v in range(n):
        for i in range(n):
            for j in range(n):
                c_db += weights[v][i] * weights[v][j] * h_db[i][j] / degree[v]
    c_db /= n * total_degree
    return c_bd, c_db


def meeting_times_sparse(
    weights: Matrix, rule: str, tolerance: float = 2e-10, max_iterations: int = 500_000
) -> Matrix:
    """Sparse Gauss--Seidel meeting solve for larger bounded-degree graphs."""
    n = len(weights)
    degree = [sum(row) for row in weights]
    adjacency: list[list[tuple[int, float]]] = []
    for i in range(n):
        if rule == "Bd":
            adjacency.append(
                [(j, weights[i][j] / degree[j]) for j in range(n) if weights[i][j]]
            )
        elif rule == "dB":
            adjacency.append(
                [(j, weights[i][j] / degree[i]) for j in range(n) if weights[i][j]]
            )
        else:
            raise ValueError(rule)
    leave = [sum(value for _, value in row) for row in adjacency]
    h = [[0.0] * n for _ in range(n)]
    for iteration in range(max_iterations):
        error = 0.0
        forward = iteration % 2 == 0
        irange = range(n) if forward else range(n - 1, -1, -1)
        for i in irange:
            jrange = range(i + 1, n) if forward else range(n - 1, i, -1)
            for j in jrange:
                value = 1.0
                value += sum(rate * h[k][j] for k, rate in adjacency[i] if k != j)
                value += sum(rate * h[i][k] for k, rate in adjacency[j] if k != i)
                value /= leave[i] + leave[j]
                error = max(error, abs(value - h[i][j]))
                h[i][j] = h[j][i] = value
        if error < tolerance:
            return h
    raise RuntimeError((rule, error, max_iterations))


def weak_coefficients_sparse(weights: Matrix) -> tuple[float, float]:
    n = len(weights)
    degree = [sum(row) for row in weights]
    total_degree = sum(degree)
    c = 1.0 / sum(1.0 / d for d in degree)
    h_bd = meeting_times_sparse(weights, "Bd")
    h_db = meeting_times_sparse(weights, "dB")
    c_bd = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            if weights[i][j]:
                c_bd += weights[i][j] * h_bd[i][j] / (degree[i] * degree[j])
    c_bd *= 2.0 * c / n
    c_db = 0.0
    for v in range(n):
        neighbors = [i for i, value in enumerate(weights[v]) if value]
        for i in neighbors:
            for j in neighbors:
                c_db += weights[v][i] * weights[v][j] * h_db[i][j] / degree[v]
    c_db /= n * total_degree
    return c_bd, c_db


def excess(weights: Matrix) -> tuple[float, float]:
    n = len(weights)
    bd, db = weak_coefficients(weights)
    return bd - (n - 1) / (2 * n), db - (n - 2) / (2 * n)


def reflected_weights(n: int, orbit_values: Sequence[float]) -> Matrix:
    """Complete-support reflection-symmetric weights from edge-orbit values."""
    orbits: dict[tuple[tuple[int, int], ...], int] = {}
    edge_orbit: dict[tuple[int, int], int] = {}
    for i in range(n):
        for j in range(i + 1, n):
            reflected = tuple(sorted(((i, j), (n - 1 - j, n - 1 - i))))
            if reflected not in orbits:
                orbits[reflected] = len(orbits)
            edge_orbit[(i, j)] = orbits[reflected]
    if len(orbit_values) != len(orbits):
        raise ValueError((len(orbit_values), len(orbits)))
    weights = [[0.0] * n for _ in range(n)]
    for (i, j), orbit in edge_orbit.items():
        weights[i][j] = weights[j][i] = orbit_values[orbit]
    return weights


def orbit_count(n: int) -> int:
    return len({tuple(sorted(((i, j), (n - 1 - j, n - 1 - i)))) for i in range(n) for j in range(i + 1, n)})


def random_search(n: int, samples: int, seed: int) -> None:
    rng = random.Random(seed)
    dim = orbit_count(n)
    population: list[tuple[float, list[float], tuple[float, float]]] = []
    for sample in range(samples):
        if population and sample % 2:
            parent = population[rng.randrange(min(30, len(population)))][1]
            logs = [x + rng.gauss(0, 0.7) for x in parent]
        else:
            logs = [rng.uniform(-5.0, 5.0) for _ in range(dim)]
        # Global weight scaling is irrelevant.
        center = sum(logs) / dim
        logs = [x - center for x in logs]
        weights = reflected_weights(n, [math.exp(x) for x in logs])
        try:
            delta = excess(weights)
        except RuntimeError:
            continue
        score = min(delta)
        population.append((score, logs, delta))
        population.sort(reverse=True, key=lambda item: item[0])
        del population[100:]
        if sample % 100 == 0 or score > 0:
            best = population[0]
            print(
                f"sample={sample} score={best[0]:+.12g} "
                f"delta_Bd={best[2][0]:+.12g} delta_dB={best[2][1]:+.12g} "
                "weights=" + ",".join(f"{math.exp(x):.8g}" for x in best[1]),
                flush=True,
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--samples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    random_search(args.n, args.samples, args.seed)


if __name__ == "__main__":
    main()
