#!/usr/bin/env python3
"""Discovery screen for rank-resolved low-degree Green-flow relaxations.

For each update rule, an exact Green occupation ``z`` obeys

    <z,-L f> = <mu,f>

for every transient test function ``f``.  This script retains all test
functions whose restriction to each rank is a Boolean polynomial of degree
at most ``d`` and maximizes normalized fixation over nonnegative ``z``.
The result is a rigorous LP upper bound only up to floating-point solver
error; this file is for discovery.  The exact verifier is separate.
"""

from __future__ import annotations

import argparse
import itertools
import json

import numpy as np
import scipy.linalg as la
from scipy.optimize import differential_evolution, linprog


R = 1.5


def baseline(n: int, rule: str) -> float:
    if rule == "Bd":
        return 3.0 ** (n - 1) / (3.0**n - 2.0**n)
    return (n - 1.0) * 3.0 ** (n - 2) / (
        n * (3.0 ** (n - 1) - 2.0 ** (n - 1))
    )


def rank_polynomial_basis(n: int, degree: int):
    """Independent rank-labelled monomials, represented by state values."""
    full = (1 << n) - 1
    states = np.arange(1, full, dtype=int)
    answer = []
    labels = []
    for rank in range(1, n):
        candidates = []
        candidate_labels = []
        for order in range(degree + 1):
            for vertices in itertools.combinations(range(n), order):
                mask = sum(1 << vertex for vertex in vertices)
                candidates.append(
                    [
                        float(
                            int(state).bit_count() == rank
                            and (int(state) & mask) == mask
                        )
                        for state in states
                    ]
                )
                candidate_labels.append((rank, vertices))
        values = np.asarray(candidates)
        _, _, pivots = la.qr(values.T, pivoting=True, mode="economic")
        dimension = np.linalg.matrix_rank(values)
        for pivot in pivots[:dimension]:
            answer.append(values[pivot])
            labels.append(candidate_labels[pivot])
    return np.asarray(answer), states, tuple(labels)


def changing_generator(weights: np.ndarray, states, rule: str):
    n = len(weights)
    full = (1 << n) - 1
    degree = weights.sum(axis=1)
    if np.any(degree <= 0):
        raise ValueError("isolated vertex")
    size = full - 1
    generator = np.zeros((size, size))
    fixation_flux = np.zeros(size)
    for row, raw_state in enumerate(states):
        state = int(raw_state)
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
            elif rule == "dB":
                mutant_fraction = sum(
                    weights[target, parent]
                    for parent in range(n)
                    if state & (1 << parent)
                ) / degree[target]
                rate = (
                    (1.0 - mutant_fraction)
                    / (1.0 + (R - 1.0) * mutant_fraction)
                    if target_mutant
                    else R
                    * mutant_fraction
                    / (1.0 + (R - 1.0) * mutant_fraction)
                )
            else:
                raise ValueError(rule)
            if rate <= 0:
                continue
            changed = state ^ (1 << target)
            total += rate
            if changed == full:
                fixation_flux[row] += rate
            elif changed:
                generator[row, changed - 1] += rate
        generator[row, row] -= total
    return generator, fixation_flux


class Relaxation:
    def __init__(self, n: int, degree: int):
        self.n = n
        self.degree = degree
        self.basis, self.states, self.labels = rank_polynomial_basis(n, degree)
        source = np.asarray(
            [1.0 / n if int(state).bit_count() == 1 else 0.0 for state in self.states]
        )
        self.rhs = self.basis @ source

    def rule_bound(self, weights: np.ndarray, rule: str):
        generator, top_flux = changing_generator(weights, self.states, rule)
        constraints = -self.basis @ generator.T
        result = linprog(
            -top_flux / baseline(self.n, rule),
            A_eq=constraints,
            b_eq=self.rhs,
            bounds=(0.0, None),
            method="highs",
        )
        if not result.success:
            raise FloatingPointError(result.message)
        residual = np.max(np.abs(constraints @ result.x - self.rhs))
        if residual > 2e-7:
            raise FloatingPointError(f"LP residual {residual}")
        return -result.fun

    def balanced_bound(self, weights: np.ndarray):
        bd = self.rule_bound(weights, "Bd")
        db = self.rule_bound(weights, "dB")
        return (bd + db) / 2.0, bd, db


def support_edges(n: int, support: str):
    if support == "complete":
        return tuple(itertools.combinations(range(n), 2))
    if support == "star":
        return tuple((0, vertex) for vertex in range(1, n))
    if support == "path":
        return tuple((vertex, vertex + 1) for vertex in range(n - 1))
    if support == "three-blade":
        if n != 7:
            raise ValueError("three-blade support requires n=7")
        edges = []
        for left, right in ((1, 2), (3, 4), (5, 6)):
            edges.extend(((0, left), (0, right), (left, right)))
        return tuple(edges)
    raise ValueError(support)


def weights_from_logs(n: int, edges, logs):
    logs = np.asarray(logs) - np.mean(logs)
    values = np.exp(np.clip(logs, -40.0, 40.0))
    weights = np.zeros((n, n))
    for (left, right), value in zip(edges, values):
        weights[left, right] = weights[right, left] = value
    return weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument(
        "--support", choices=("complete", "star", "path", "three-blade"), default="complete"
    )
    parser.add_argument("--span", type=float, default=12.0)
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--popsize", type=int, default=6)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    edges = support_edges(args.n, args.support)
    relaxation = Relaxation(args.n, args.degree)
    best = [-np.inf]

    def objective(logs):
        try:
            weights = weights_from_logs(args.n, edges, logs)
            score, bd, db = relaxation.balanced_bound(weights)
        except (FloatingPointError, ValueError):
            return 1e4
        if score > best[0]:
            best[0] = score
            print(
                json.dumps(
                    {
                        "balanced_bound": score,
                        "Bd_bound": bd,
                        "dB_bound": db,
                        "log_span": float(np.ptp(logs)),
                        "weights": weights.tolist(),
                    }
                ),
                flush=True,
            )
        return -score

    result = differential_evolution(
        objective,
        [(-args.span, args.span)] * len(edges),
        seed=args.seed,
        popsize=args.popsize,
        maxiter=args.iterations,
        polish=False,
        updating="immediate",
        tol=1e-8,
    )
    weights = weights_from_logs(args.n, edges, result.x)
    score, bd, db = relaxation.balanced_bound(weights)
    print(
        "BEST",
        json.dumps(
            {
                "balanced_bound": score,
                "Bd_bound": bd,
                "dB_bound": db,
                "weights": weights.tolist(),
            }
        ),
    )


if __name__ == "__main__":
    main()
