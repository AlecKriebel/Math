#!/usr/bin/env python
"""Numerical discovery tests for reflected dB-dual level inequalities.

This is deliberately a floating-point exploration script, not a proof
certificate.  It constructs the geometric-union dual directly and solves
for its stationary law.  The exact claims discovered here must be checked
separately over the rationals.
"""

from __future__ import annotations

import argparse
from itertools import combinations

import numpy as np
from scipy.linalg import solve


def popcount(mask: int) -> int:
    return bin(int(mask)).count("1")


def union_laws(transition: np.ndarray, fitness: float):
    laws = []
    for row in transition:
        support = np.flatnonzero(row > 1e-15).tolist()
        support_size = len(support)
        probabilities = np.zeros(1 << support_size)
        for mask in range(1, 1 << support_size):
            mass = sum(
                row[support[j]]
                for j in range(support_size)
                if (mask >> j) & 1
            )
            probabilities[mask] = mass / (
                fitness - (fitness - 1) * mass
            )
        # Boolean-lattice Mobius inversion turns probabilities of containment
        # into probabilities of an exact sampled union.
        for j in range(support_size):
            for mask in range(1 << support_size):
                if (mask >> j) & 1:
                    probabilities[mask] -= probabilities[mask ^ (1 << j)]
        law = []
        for mask in range(1, 1 << support_size):
            probability = probabilities[mask]
            if probability > 1e-13:
                vertex_mask = sum(
                    1 << support[j]
                    for j in range(support_size)
                    if (mask >> j) & 1
                )
                law.append((vertex_mask, probability))
        assert abs(sum(value for _, value in law) - 1) < 1e-8
        laws.append(law)
    return laws


def dual_generator(weights: np.ndarray, fitness: float) -> np.ndarray:
    order = len(weights)
    transition = weights / weights.sum(axis=1)[:, None]
    state_count = (1 << order) - 1
    generator = np.zeros((state_count, state_count))
    laws = union_laws(transition, fitness)
    for state in range(1, state_count + 1):
        row = state - 1
        for target in range(order):
            if not ((state >> target) & 1):
                continue
            without_target = state & ~(1 << target)
            for sampled_set, probability in laws[target]:
                new_state = without_target | sampled_set
                if new_state != state:
                    generator[row, new_state - 1] += probability
        generator[row, row] = -sum(generator[row])
    return generator


def stationary_distribution(weights: np.ndarray, fitness: float) -> np.ndarray:
    generator = dual_generator(weights, fitness)
    state_count = len(generator)
    system = generator.T.copy()
    rhs = np.zeros(state_count)
    system[-1] = 1
    rhs[-1] = 1
    invariant = solve(system, rhs)
    residual = np.linalg.norm(generator.T @ invariant, ord=np.inf)
    assert residual < 1e-8
    return invariant


def stationary_levels(weights: np.ndarray, fitness: float) -> np.ndarray:
    order = len(weights)
    invariant = stationary_distribution(weights, fitness)
    state_count = len(invariant)
    levels = np.zeros(order + 1)
    for state, probability in enumerate(invariant, 1):
        levels[popcount(state)] += probability
    return levels


def connected(weights: np.ndarray) -> bool:
    order = len(weights)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in np.flatnonzero(weights[vertex] > 0):
            neighbor = int(neighbor)
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == order


def weights_from_support(order: int, support_mask: int) -> np.ndarray:
    weights = np.zeros((order, order))
    for edge_index, (i, j) in enumerate(combinations(range(order), 2)):
        if (support_mask >> edge_index) & 1:
            weights[i, j] = weights[j, i] = 1
    return weights


def diagnostics(levels: np.ndarray, fitness: float):
    order = len(levels) - 1
    theta = fitness - 1
    reflection = []
    for size in range(order // 2 + 1, order):
        reflection.append(
            (
                (order - size)
                * theta ** (2 * size - order)
                * levels[order - size]
                - size * levels[size],
                size,
            )
        )

    # At r=2 the complete graph has level weights proportional to
    # C(n-1,k).  Test ordinary and ultra-log-concavity after this division.
    scaled = np.zeros(order + 1)
    from math import comb

    for size in range(1, order):
        scaled[size] = levels[size] / comb(order - 1, size)
    log_concavity = []
    for size in range(2, order - 1):
        log_concavity.append(
            (scaled[size] ** 2 - scaled[size - 1] * scaled[size + 1], size)
        )

    # Reflected cumulative first-moment surplus.  Nonnegativity for every
    # lower cutoff would strengthen the single-pair conjecture.
    cumulative = []
    for cutoff in range(order // 2 + 1, order):
        value = sum(
            (order - size)
            * theta ** (2 * size - order)
            * levels[order - size]
            - size * levels[size]
            for size in range(cutoff, order)
        )
        cumulative.append((value, cutoff))

    # Complete-graph level law: Bin(n-1,p), conditioned to be nonempty,
    # where p=(r-1)/r.  Positive upper-tail margins mean first-order
    # stochastic domination by the complete graph.
    complete = np.zeros(order + 1)
    normalization = fitness ** (order - 1) - 1
    for size in range(1, order):
        complete[size] = (
            comb(order - 1, size)
            * theta**size
            / normalization
        )
    complete_tail = []
    for cutoff in range(1, order):
        complete_tail.append(
            (sum(complete[cutoff:]) - sum(levels[cutoff:]), cutoff)
        )
    mean_margin = sum(
        size * (complete[size] - levels[size])
        for size in range(1, order)
    )
    return (
        reflection,
        log_concavity,
        cumulative,
        complete_tail,
        [(mean_margin, 0)],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--r", type=float, default=2.0)
    parser.add_argument("--random", type=int, default=100)
    parser.add_argument("--enumerate", action="store_true")
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    worst = {"reflection": (float("inf"), None),
             "log_concavity": (float("inf"), None),
             "cumulative": (float("inf"), None),
             "complete_tail": (float("inf"), None),
             "complete_mean": (float("inf"), None)}

    graphs = []
    edge_count = args.n * (args.n - 1) // 2
    if args.enumerate:
        for support in range(1, 1 << edge_count):
            weights = weights_from_support(args.n, support)
            if connected(weights):
                graphs.append(weights)
    for _ in range(args.random):
        raw = np.exp(rng.uniform(-10, 10, size=(args.n, args.n)))
        weights = np.triu(raw, 1)
        weights += weights.T
        graphs.append(weights)

    for index, weights in enumerate(graphs):
        levels = stationary_levels(weights, args.r)
        values_by_name = diagnostics(levels, args.r)
        for name, values in zip(worst, values_by_name):
            if values:
                value = min(values)
                if value[0] < worst[name][0]:
                    worst[name] = (value[0], (index, value[1], levels, weights))
    print("tested", len(graphs))
    for name, record in worst.items():
        print(name, record[0])
        if record[1] is not None:
            index, size, levels, weights = record[1]
            print(" index", index, "size", size)
            print(" levels", levels.tolist())
            print(" weights", weights.tolist())


if __name__ == "__main__":
    main()
