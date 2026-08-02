#!/usr/bin/env python3
"""Numerical adversarial search for failures of two stationary-mixture splits.

This is a discovery script, not a proof certificate.  Every candidate it
prints must be reconstructed with exact rational arithmetic before it can be
used mathematically.
"""

from __future__ import annotations

import argparse
import math
import random

import numpy as np


def geometric_union_law(row: np.ndarray) -> list[tuple[int, float]]:
    n = len(row)
    values = np.zeros(1 << n)
    for mask in range(1 << n):
        mass = sum(row[j] for j in range(n) if mask >> j & 1)
        values[mask] = mass / (2.0 - mass)
    for j in range(n):
        for mask in range(1 << n):
            if mask >> j & 1:
                values[mask] -= values[mask ^ (1 << j)]
    return [(mask, values[mask]) for mask in range(1, 1 << n) if values[mask] > 1e-15]


def stationary(generator: np.ndarray) -> np.ndarray:
    matrix = generator.T.copy()
    rhs = np.zeros(len(matrix))
    matrix[-1] = 1.0
    rhs[-1] = 1.0
    return np.linalg.solve(matrix, rhs)


def batched_generator(P: np.ndarray) -> tuple[np.ndarray, list[list[tuple[int, float]]]]:
    n = len(P)
    size = (1 << n) - 1
    laws = [geometric_union_law(row) for row in P]
    generator = np.zeros((size, size))
    for state in range(1, 1 << n):
        for v in range(n):
            if not (state >> v & 1):
                continue
            for offspring, probability in laws[v]:
                new_state = (state & ~(1 << v)) | offspring
                if new_state != state:
                    generator[state - 1, new_state - 1] += probability
        generator[state - 1, state - 1] = -generator[state - 1].sum()
    return generator, laws


def stopped_systems(
    P: np.ndarray, laws: list[list[tuple[int, float]]], target: int
) -> tuple[np.ndarray, np.ndarray, list[int], np.ndarray]:
    n = len(P)
    outside = [vertex for vertex in range(n) if vertex != target]
    local = {vertex: position for position, vertex in enumerate(outside)}
    size = 1 << (n - 1)
    generator = np.zeros((size, size))
    zero_hit = np.eye(size)
    reward = np.zeros(size)
    for state in range(size):
        active = [outside[k] for k in range(n - 1) if state >> k & 1]
        zero_hit[state, state] += len(active)
        for v in active:
            reward[state] += 2.0 * P[v, target]
            marginal: dict[int, float] = {}
            for offspring, probability in laws[v]:
                outside_offspring = sum(
                    1 << local[j] for j in outside if offspring >> j & 1
                )
                new_state = (state & ~(1 << local[v])) | outside_offspring
                marginal[new_state] = marginal.get(new_state, 0.0) + probability
                if not (offspring >> target & 1):
                    zero_hit[state, new_state] -= probability
            for new_state, probability in marginal.items():
                if new_state != state:
                    generator[state, new_state] += probability
        generator[state, state] = -generator[state].sum()
    zero_resolvent = np.linalg.inv(zero_hit)
    u = zero_resolvent @ np.ones(size)
    g = np.linalg.solve(np.eye(size) - generator, reward)
    return u, g, outside, zero_resolvent


def post_target_law(
    pi: np.ndarray,
    laws: list[list[tuple[int, float]]],
    target: int,
    n: int,
) -> np.ndarray:
    outside = [vertex for vertex in range(n) if vertex != target]
    local = {vertex: position for position, vertex in enumerate(outside)}
    eta = np.zeros(1 << (n - 1))
    for state in range(1, 1 << n):
        outputs = [(state, 1.0)] if not (state >> target & 1) else [
            ((state & ~(1 << target)) | offspring, probability)
            for offspring, probability in laws[target]
        ]
        for output, probability in outputs:
            local_state = sum(1 << local[j] for j in outside if output >> j & 1)
            eta[local_state] += pi[state - 1] * probability
    return eta


def symmetric_transition(log_weights: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    weights = np.zeros((n, n))
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    values = np.exp(log_weights - np.mean(log_weights))
    for value, (i, j) in zip(values, edges):
        weights[i, j] = weights[j, i] = value
    return weights / weights.sum(axis=1)[:, None], weights


def directed_transition(log_weights: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    weights = np.zeros((n, n))
    arcs = [(i, j) for i in range(n) for j in range(n) if i != j]
    values = np.exp(log_weights)
    for value, (i, j) in zip(values, arcs):
        weights[i, j] = value
    return weights / weights.sum(axis=1)[:, None], weights


def evaluate(log_weights: np.ndarray, n: int, directed: bool) -> tuple[float, float, dict]:
    transition = directed_transition if directed else symmetric_transition
    P, weights = transition(log_weights, n)
    generator, laws = batched_generator(P)
    pi = stationary(generator)
    if pi.min() < -1e-8 or abs(pi.sum() - 1.0) > 1e-7:
        raise np.linalg.LinAlgError("invalid stationary solve")
    best_a = (math.inf, None)
    best_b = (-math.inf, None)
    all_data = []
    for target in range(n):
        u, g, _, zero_resolvent = stopped_systems(P, laws, target)
        eta = post_target_law(pi, laws, target, n)
        Eu = eta @ u
        Eg = eta @ g
        Eprod = eta @ (u * g)
        a_slack = eta @ (u * (1.0 + g)) - 1.0
        covariance = Eprod - Eu * Eg
        total = Eu * (1.0 + Eg) - 1.0
        bridge_left = eta @ (u * g - zero_resolvent @ g)
        bridge_right = eta @ (zero_resolvent @ g) - (1.0 - Eu)
        all_data.append(
            (target, a_slack, covariance, total, Eu, Eg, bridge_left, bridge_right)
        )
        best_a = min(best_a, (a_slack, target))
        best_b = max(best_b, (covariance, target))
    return best_a[0], best_b[0], {
        "A_target": best_a[1],
        "B_target": best_b[1],
        "weights": weights,
        "data": all_data,
    }


def objective(log_weights: np.ndarray, n: int, directed: bool, which: str) -> float:
    try:
        a_slack, covariance, data = evaluate(log_weights, n, directed)
        if which == "A":
            return a_slack
        if which == "B":
            return -covariance
        if which == "C":
            return min(row[3] for row in data["data"])
        if which == "D":
            return min(row[6] for row in data["data"])
        return min(row[7] for row in data["data"])
    except (np.linalg.LinAlgError, FloatingPointError, ZeroDivisionError):
        return 1e6


def evolve(n: int, directed: bool, which: str, seed: int, generations: int) -> None:
    rng = np.random.default_rng(seed)
    random.seed(seed)
    dimension = n * (n - 1) if directed else n * (n - 1) // 2
    population_size = max(30, 8 * dimension)
    bound = 6.0
    population = [rng.uniform(-bound, bound, dimension) for _ in range(population_size)]
    scores = [objective(x, n, directed, which) for x in population]
    for generation in range(generations):
        order = np.argsort(scores)
        elite_count = max(5, population_size // 5)
        elites = [population[k].copy() for k in order[:elite_count]]
        scale = max(0.03, 1.5 * (1.0 - generation / generations))
        new_population = elites[:]
        while len(new_population) < population_size:
            parent = elites[random.randrange(elite_count)].copy()
            if random.random() < 0.15:
                parent = rng.uniform(-bound, bound, dimension)
            else:
                mask = rng.random(dimension) < max(0.15, 2.0 / dimension)
                parent[mask] += rng.normal(0.0, scale, mask.sum())
                parent = np.clip(parent, -bound, bound)
            new_population.append(parent)
        population = new_population
        scores = [objective(x, n, directed, which) for x in population]
        if generation % 100 == 0 or generation + 1 == generations:
            best = int(np.argmin(scores))
            print(which, "generation", generation, "score", scores[best], flush=True)
    best = int(np.argmin(scores))
    a_slack, covariance, data = evaluate(population[best], n, directed)
    print("BEST", "directed" if directed else "symmetric", "n", n, "criterion", which)
    print("A_min", repr(a_slack), "B_max", repr(covariance))
    print("log_weights", repr(population[best].tolist()))
    print("weights")
    print(np.array2string(data["weights"], precision=12, suppress_small=False))
    print("targets", data["data"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--directed", action="store_true")
    parser.add_argument("--criterion", choices=("A", "B", "C", "D", "E"), default="A")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--generations", type=int, default=1000)
    args = parser.parse_args()
    evolve(args.n, args.directed, args.criterion, args.seed, args.generations)


if __name__ == "__main__":
    main()
