#!/usr/bin/env python3
"""Explore quadratic Poisson certificates for dB dual bounds at r=2.

This is a discovery script, not a proof certificate.  For a row-stochastic
kernel P it asks whether a Boolean quadratic g satisfies

    L g(A) >= |A| - b

on every nonempty state of the geometric-union dual.  The two relevant
choices are b=n/2 and b=n rho_dB(K_n,2).
"""

from __future__ import annotations

import argparse
import itertools

import networkx as nx
import numpy as np
from scipy.optimize import linprog


def union_distribution(probabilities: list[float]) -> list[tuple[int, float]]:
    """Distribution of the occupied support of K iid samples, Pr(K=k)=2^-k."""
    dimension = len(probabilities)
    result = []
    for union_mask in range(1, 1 << dimension):
        probability = 0.0
        subset_mask = union_mask
        while True:
            mass = sum(
                probabilities[i]
                for i in range(dimension)
                if subset_mask >> i & 1
            )
            generating_function = mass / (2.0 - mass) if mass else 0.0
            sign = -1.0 if (union_mask.bit_count() - subset_mask.bit_count()) % 2 else 1.0
            probability += sign * generating_function
            if subset_mask == 0:
                break
            subset_mask = (subset_mask - 1) & union_mask
        if probability > 1e-13:
            result.append((union_mask, probability))
    assert abs(sum(probability for _, probability in result) - 1.0) < 1e-8
    return result


def certificate(weight: np.ndarray, pair_mode: str, target: str):
    n = len(weight)
    transition = weight / weight.sum(axis=1)[:, None]
    pairs = [
        (i, j)
        for i in range(n)
        for j in range(i + 1, n)
        if pair_mode == "all" or weight[i, j] > 0
    ]
    replacements = []
    for vertex in range(n):
        neighbors = [u for u in range(n) if transition[vertex, u] > 1e-15]
        distribution = union_distribution([transition[vertex, u] for u in neighbors])
        replacements.append((neighbors, distribution))

    def features(state: set[int]) -> np.ndarray:
        return np.array(
            [len(state)] + [int(i in state and j in state) for i, j in pairs],
            dtype=float,
        )

    if target == "complete":
        bound = (n - 1) * 2 ** (n - 2) / (2 ** (n - 1) - 1)
    else:
        bound = n / 2
    rows = []
    right_sides = []
    for state_mask in range(1, 1 << n):
        state = {i for i in range(n) if state_mask >> i & 1}
        old_features = features(state)
        drift = np.zeros(1 + len(pairs))
        for vertex in state:
            neighbors, distribution = replacements[vertex]
            for union_mask, probability in distribution:
                replacement = {
                    neighbors[i]
                    for i in range(len(neighbors))
                    if union_mask >> i & 1
                }
                new_state = (state - {vertex}) | replacement
                drift += probability * (features(new_state) - old_features)
        rows.append(-drift)
        right_sides.append(-(len(state) - bound))
    return linprog(
        np.zeros(1 + len(pairs)),
        A_ub=np.asarray(rows),
        b_ub=np.asarray(right_sides),
        bounds=[(None, None)] * (1 + len(pairs)),
        method="highs",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=7)
    args = parser.parse_args()
    atlas = nx.graph_atlas_g()
    for target, pair_mode in itertools.product(("half", "complete"), ("edge", "all")):
        for n in range(2, args.max_n + 1):
            tested = failures = 0
            first = None
            for graph in atlas:
                if len(graph) != n or not nx.is_connected(graph):
                    continue
                result = certificate(nx.to_numpy_array(graph), pair_mode, target)
                tested += 1
                if not result.success:
                    failures += 1
                    if first is None:
                        first = sorted(graph.edges())
            print(target, pair_mode, n, tested, failures, first, flush=True)


if __name__ == "__main__":
    main()
