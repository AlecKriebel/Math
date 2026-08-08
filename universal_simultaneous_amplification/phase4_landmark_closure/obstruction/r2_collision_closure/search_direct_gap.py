#!/usr/bin/env python3
"""Hostile numerical search for the actual direct gap L-V near the n=6 seed.

The exact n=6 graph refutes only the auxiliary inequality L<=S.  This
program optimizes the quantity that matters, L-V, on its full support and on
nearby sparse supports.  It is a discovery tool; every positive candidate
must be replayed by ``verify_fisher_route.py`` over exact rationals.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np
from scipy.optimize import minimize

from search_symmetric_split import quantities_from_weights


N = 6
EDGES = list(combinations(range(N), 2))
SEED = np.array([3, 300, 2, 5, 1, 3, 3, 1, 300, 1, 1, 1, 20, 1, 1], dtype=float)


def matrix_from_support(values: np.ndarray, support: tuple[int, ...]) -> np.ndarray:
    weights = np.zeros((N, N))
    positive = np.exp(values - np.mean(values))
    for value, edge_index in zip(positive, support):
        u, v = EDGES[edge_index]
        weights[u, v] = weights[v, u] = value
    return weights


def is_connected(support: tuple[int, ...]) -> bool:
    adjacency = [set() for _ in range(N)]
    for edge_index in support:
        u, v = EDGES[edge_index]
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    return len(seen) == N


def optimize_support(support: tuple[int, ...], label: str) -> dict[str, object]:
    initial = np.log(SEED[list(support)])
    initial -= np.mean(initial)

    def objective(values):
        try:
            L, _, V = quantities_from_weights(matrix_from_support(values, support))
            return V - L
        except np.linalg.LinAlgError:
            return 1e3

    initial_gap = -objective(initial)
    result = minimize(
        objective,
        initial,
        method="Powell",
        bounds=[(-12.0, 12.0)] * len(support),
        options={"maxiter": 220, "xtol": 1e-9, "ftol": 1e-11},
    )
    L, S, V = quantities_from_weights(matrix_from_support(result.x, support))
    output = {
        "label": label,
        "support": support,
        "initial_gap": initial_gap,
        "optimized_gap": L - V,
        "L": L,
        "S": S,
        "V": V,
        "success": result.success,
        "log_weights": result.x.tolist(),
    }
    print(output, flush=True)
    return output


def supports_to_test() -> list[tuple[str, tuple[int, ...]]]:
    full = tuple(range(len(EDGES)))
    weak = tuple(index for index, value in enumerate(SEED) if value == 1)
    tests: list[tuple[str, tuple[int, ...]]] = [("full", full)]
    for index in weak:
        support = tuple(edge for edge in full if edge != index)
        if is_connected(support):
            tests.append((f"drop-{EDGES[index]}", support))
    for threshold in (2, 3, 5, 20):
        support = tuple(index for index, value in enumerate(SEED) if value >= threshold)
        if is_connected(support):
            tests.append((f"threshold-{threshold}", support))
    # Deterministic mixed weak-edge deletions.
    rng = np.random.default_rng(260808)
    for sample in range(8):
        removed = set(rng.choice(weak, size=rng.integers(2, len(weak) + 1), replace=False))
        support = tuple(index for index in full if index not in removed)
        if is_connected(support):
            tests.append((f"weak-subset-{sample}", support))
    # Remove duplicates while retaining labels/order.
    unique = []
    seen = set()
    for label, support in tests:
        if support not in seen:
            seen.add(support)
            unique.append((label, support))
    return unique


def main() -> None:
    results = [optimize_support(support, label) for label, support in supports_to_test()]
    best = max(results, key=lambda result: result["optimized_gap"])
    print("BEST", best)
    if best["optimized_gap"] > 1e-8:
        print("CANDIDATE: reconstruct and replay exactly before drawing a conclusion")
    else:
        print("NO POSITIVE DIRECT GAP FOUND; numerical evidence only")


if __name__ == "__main__":
    main()
