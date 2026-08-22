#!/usr/bin/env python3
"""Deterministic exact hostile screen for the direct sign ``L <= V``.

This is finite implementation validation, not a universal proof.  It uses
only rational arithmetic and reconstructs the complete subset chain for
every tested graph.  The screen deliberately includes zero edges, highly
unequal integer weights, and the frozen six-vertex counterexample to the
discarded symmetric split.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, product
from random import Random

from verify_fisher_route import (
    green_data,
    proper_generator,
    stationary,
    transition,
)


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate check fails."""


def require(condition, detail="certificate check failed"):
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(str(detail))


def matrix_from_edges(n: int, values) -> list[list[int]]:
    weights = [[0 for _ in range(n)] for _ in range(n)]
    for value, (u, v) in zip(values, combinations(range(n), 2)):
        weights[u][v] = weights[v][u] = value
    return weights


def connected(weights) -> bool:
    n = len(weights)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor, value in enumerate(weights[vertex]):
            if value and neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == n


def exact_gap(weights) -> F:
    n = len(weights)
    P = transition(weights)
    states, QP = proper_generator(P)
    pi = stationary(QP)
    complete_P = [
        [F(0) if u == v else F(1, n - 1) for u in range(n)]
        for v in range(n)
    ]
    complete_states, QK = proper_generator(complete_P)
    require(states == complete_states)
    L, V, _, _, _ = green_data(weights, P, states, QK, pi)
    return V - L


def screen(label: str, graphs) -> tuple[int, F]:
    tested = 0
    smallest = None
    for weights in graphs:
        if not connected(weights):
            continue
        gap = exact_gap(weights)
        require(gap >= 0, (label, weights, gap))
        if smallest is None or gap < smallest:
            smallest = gap
        tested += 1
    require(tested and smallest is not None)
    minimum_text = "0" if smallest == 0 else f">0 (~{float(smallest):.12g})"
    print(
        f"PASS: {label}: {tested} connected exact graphs; "
        f"min(V-L)={minimum_text}"
    )
    return tested, smallest


def exhaustive_graphs(n: int, alphabet):
    edge_count = n * (n - 1) // 2
    for values in product(alphabet, repeat=edge_count):
        yield matrix_from_edges(n, values)


def deterministic_graphs(n: int, count: int, seed: int):
    rng = Random(seed)
    edge_count = n * (n - 1) // 2
    alphabet = (0, 0, 1, 2, 7, 100, 1000)
    produced = 0
    while produced < count:
        values = [rng.choice(alphabet) for _ in range(edge_count)]
        weights = matrix_from_edges(n, values)
        if connected(weights):
            yield weights
            produced += 1


def main() -> None:
    # Exhaustive support/weight screens.  Common rescalings appear more than
    # once intentionally; they also audit scale invariance of the formulas.
    screen("n=3, weights in {0,1,2,5}", exhaustive_graphs(3, (0, 1, 2, 5)))
    screen("n=4, weights in {0,1,2}", exhaustive_graphs(4, (0, 1, 2)))
    screen("n=5 deterministic sparse/extreme", deterministic_graphs(5, 48, 26080805))

    # Complete-support n=6 graph which exactly refutes L<=S but not L<=V.
    split_witness = matrix_from_edges(
        6,
        (3, 300, 2, 5, 1, 3, 3, 1, 300, 1, 1, 1, 20, 1, 1),
    )
    gap = exact_gap(split_witness)
    require(gap > 0)
    print(f"PASS: frozen n=6 split witness has exact V-L>0 (~{float(gap):.10g})")
    print("PASS: direct L-V exact hostile screen (finite validation only)")


if __name__ == "__main__":
    main()
