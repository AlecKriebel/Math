#!/usr/bin/env python3
"""Numerical hostile search for violations of L <= S <= V.

This is a discovery program only.  It uses floating-point linear algebra and
must not be used as a proof certificate.  Every apparent violation is printed
with its raw log-weights for subsequent rational reconstruction.
"""

from __future__ import annotations

from itertools import combinations
from math import comb

import numpy as np
from scipy.optimize import differential_evolution


def popcount(state: int) -> int:
    return state.bit_count()


def geometric_union_law(row: np.ndarray) -> dict[int, float]:
    support = np.flatnonzero(row > 0).tolist()
    law: dict[int, float] = {}
    for size in range(1, len(support) + 1):
        for chosen in combinations(support, size):
            probability = 0.0
            for subsize in range(size + 1):
                for subset in combinations(chosen, subsize):
                    mass = float(row[list(subset)].sum()) if subset else 0.0
                    probability += (-1) ** (size - subsize) * (
                        mass / (2.0 - mass) if mass else 0.0
                    )
            if probability > 1e-15:
                law[sum(1 << u for u in chosen)] = probability
    return law


def generator(P: np.ndarray) -> tuple[list[int], np.ndarray]:
    n = len(P)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    laws = [geometric_union_law(P[v]) for v in range(n)]
    Q = np.zeros((len(states), len(states)))
    for state in states:
        source = index[state]
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            without = state & ~(1 << target)
            for union, probability in laws[target].items():
                output = without | union
                if output != state:
                    Q[source, index[output]] += probability
                    Q[source, source] -= probability
    return states, Q


def stationary(Q: np.ndarray) -> np.ndarray:
    matrix = Q.T.copy()
    rhs = np.zeros(len(Q))
    matrix[-1, :] = 1.0
    rhs[-1] = 1.0
    # Extreme nearly disconnected kernels easily manufacture false signs in
    # double precision.  Reject rather than optimize through that regime;
    # any boundary candidate must be reconstructed in exact arithmetic.
    if np.linalg.cond(matrix) > 1e11:
        raise np.linalg.LinAlgError("ill-conditioned stationary system")
    return np.linalg.solve(matrix, rhs)


def complete_coefficients(n: int) -> np.ndarray:
    denominator = 1.0 - 2.0 ** (1 - n)
    mu = np.zeros(n + 1)
    for k in range(1, n):
        mu[k] = (
            (n + k) / (2 * n) - 2.0 ** (k - n)
        ) / (n * comb(n - 2, k - 1) * denominator)
    return mu[:-1] + mu[1:]


def quantities_from_weights(weights: np.ndarray) -> tuple[float, float, float]:
    """Evaluate a connected symmetric weight matrix, allowing zero edges."""
    n = len(weights)
    if np.any(weights.sum(axis=1) <= 0):
        raise np.linalg.LinAlgError("isolated vertex")
    P = weights / weights.sum(axis=1, keepdims=True)

    states, QP = generator(P)
    pi = stationary(QP)
    N = n - 1
    PK = (np.ones((n, n)) - np.eye(n)) / N
    complete_states, QK = generator(PK)
    assert states == complete_states
    piK = np.array(
        [
            (n - popcount(state)) / (n * (2 ** (n - 1) - 1))
            for state in states
        ]
    )
    g = pi / piK

    coefficients = complete_coefficients(n)
    U = np.zeros(n)
    for holes in range(1, n):
        U[holes] = sum(
            coefficients[k]
            * (2 * N * N) / (N + k) ** 2
            * comb(holes - 1, k - 1)
            for k in range(1, holes + 1)
        )

    forcing = np.zeros(len(states))
    conditional_V = np.zeros(len(states))
    for row, state in enumerate(states):
        occupied = [v for v in range(n) if (state >> v) & 1]
        holes = [u for u in range(n) if not ((state >> u) & 1)]
        cut = sum(P[v, u] for v in occupied for u in holes)
        forcing[row] = U[len(holes)] * (
            cut - len(occupied) * len(holes) / N
        )
        for k in range(1, len(holes) + 1):
            baseline = k / N
            factor = coefficients[k] * 2 / (1 + baseline) ** 2
            for v in occupied:
                for subset in combinations(holes, k):
                    mass = P[v, list(subset)].sum()
                    conditional_V[row] += (
                        factor * (mass - baseline) ** 2 / (1 + mass)
                    )

    matrix = QK.copy()
    rhs = forcing.copy()
    matrix[-1, :] = 0.0
    matrix[-1, 0] = 1.0
    rhs[-1] = 0.0
    psi = np.linalg.solve(matrix, rhs)

    L = float(pi @ forcing)
    V = float(pi @ conditional_V)
    flow = piK[:, None] * QK
    S = float(
        -0.5
        * np.sum(flow * (g[None, :] - g[:, None]) * (psi[None, :] - psi[:, None]))
    )
    return L, S, V


def quantities(log_weights: np.ndarray, n: int) -> tuple[float, float, float]:
    edges = list(combinations(range(n), 2))
    weights = np.zeros((n, n))
    # Removing the mean fixes the irrelevant common scale and avoids overflow.
    positive = np.exp(log_weights - np.mean(log_weights))
    for value, (u, v) in zip(positive, edges):
        weights[u, v] = weights[v, u] = value
    return quantities_from_weights(weights)


def search(n: int, objective: str, seed: int) -> None:
    dimension = n * (n - 1) // 2

    def score(log_weights):
        try:
            L, S, V = quantities(log_weights, n)
            return -(L - S if objective == "L-S" else S - V)
        except np.linalg.LinAlgError:
            return 1e6

    result = differential_evolution(
        score,
        [(-8.0, 8.0)] * dimension,
        seed=seed,
        popsize=10,
        maxiter=180,
        polish=True,
        updating="immediate",
        workers=1,
        tol=1e-10,
    )
    L, S, V = quantities(result.x, n)
    print(
        f"n={n} objective={objective} maximum={-result.fun:.17g} "
        f"L={L:.17g} S={S:.17g} V={V:.17g}"
    )
    print("log_weights=", repr(result.x.tolist()))


def main() -> None:
    for n in (4, 5):
        for objective in ("L-S", "S-V"):
            search(n, objective, seed=260807 + 10 * n + (objective == "S-V"))


if __name__ == "__main__":
    main()
