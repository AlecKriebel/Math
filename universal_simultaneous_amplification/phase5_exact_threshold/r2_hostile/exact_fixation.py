#!/usr/bin/env python3
"""Exact Bd and dB fixation at fitness two for small rational graphs.

The absorbing equations are reconstructed directly from the two update
rules.  State-dependent self loops are deleted and the remaining flip rates
are normalized; this leaves hitting probabilities unchanged and avoids the
conditioning problems caused by weak bridges.  The linear systems are solved
over QQ by FLINT.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import Iterable

from flint import fmpq, fmpq_mat


Q = fmpq


def _q(value) -> Q:
    if isinstance(value, Q):
        return value
    if isinstance(value, Fraction):
        return Q(value.numerator, value.denominator)
    if isinstance(value, int):
        return Q(value)
    raise TypeError(f"weight must be rational, not {type(value)!r}")


def as_float(value: Q) -> float:
    return int(value.p) / int(value.q)


def baseline(n: int, rule: str) -> Q:
    """Same-order complete-graph fixation at r=2."""
    if rule == "Bd":
        return Q(2 ** (n - 1), 2**n - 1)
    if rule == "dB":
        return Q((n - 1) * 2 ** (n - 2), n * (2 ** (n - 1) - 1))
    raise ValueError(rule)


def matrix_from_edges(n: int, values: Iterable) -> list[list[Q]]:
    weights = [[Q(0) for _ in range(n)] for _ in range(n)]
    for (u, v), value in zip(combinations(range(n), 2), values):
        weight = _q(value)
        if weight < 0:
            raise ValueError("negative edge weight")
        weights[u][v] = weights[v][u] = weight
    return weights


def connected(weights: list[list[Q]]) -> bool:
    n = len(weights)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v, weight in enumerate(weights[u]):
            if weight and v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def fixation(weights, rule: str) -> Q:
    """Uniform-singleton fixation at r=2, exactly over QQ."""
    weights = [[_q(value) for value in row] for row in weights]
    n = len(weights)
    if any(len(row) != n for row in weights):
        raise ValueError("weights must be square")
    if any(weights[u][u] for u in range(n)):
        raise ValueError("loops are not allowed")
    if any(weights[u][v] != weights[v][u] for u in range(n) for v in range(n)):
        raise ValueError("weights must be symmetric")
    degrees = [sum(row, Q(0)) for row in weights]
    if any(not degree for degree in degrees):
        raise ValueError("isolated vertex")

    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    size = len(states)
    matrix = fmpq_mat(size, size)
    rhs = fmpq_mat(size, 1)

    for state, row in index.items():
        raw: list[tuple[int, Q]] = []
        mutant_count = state.bit_count()
        for target in range(n):
            target_mutant = bool(state & (1 << target))
            if rule == "dB":
                mutant_mass = sum(
                    (weights[source][target]
                     for source in range(n) if state & (1 << source)),
                    Q(0),
                )
                resident_mass = degrees[target] - mutant_mass
                denominator = 2 * mutant_mass + resident_mass
                rate = (
                    resident_mass / denominator
                    if target_mutant
                    else 2 * mutant_mass / denominator
                )
            elif rule == "Bd":
                if target_mutant:
                    rate = sum(
                        (weights[source][target] / degrees[source]
                         for source in range(n) if not state & (1 << source)),
                        Q(0),
                    )
                else:
                    rate = 2 * sum(
                        (weights[source][target] / degrees[source]
                         for source in range(n) if state & (1 << source)),
                        Q(0),
                    )
                # The omitted common factor 1/(n+|S|) cancels below.
                assert mutant_count == state.bit_count()
            else:
                raise ValueError(rule)
            if rate:
                raw.append((state ^ (1 << target), rate))

        total = sum((rate for _, rate in raw), Q(0))
        if not total:
            raise ArithmeticError(f"no changing transition from {state}")
        matrix[row, row] = 1
        for target_state, rate in raw:
            probability = rate / total
            if target_state == full:
                rhs[row, 0] += probability
            elif target_state:
                matrix[row, index[target_state]] -= probability

    solution = matrix.solve(rhs)
    answer = sum((solution[index[1 << v], 0] for v in range(n)), Q(0)) / n
    assert 0 < answer < 1
    return answer


def normalized_scores(weights) -> tuple[Q, Q]:
    n = len(weights)
    return (
        fixation(weights, "Bd") / baseline(n, "Bd"),
        fixation(weights, "dB") / baseline(n, "dB"),
    )


def _self_test() -> None:
    for n in range(2, 8):
        complete = matrix_from_edges(n, [1] * (n * (n - 1) // 2))
        for rule in ("Bd", "dB"):
            assert fixation(complete, rule) == baseline(n, rule)
    path = matrix_from_edges(3, [1, 0, 1])
    assert connected(path)
    normalized_scores(path)
    print("PASS: exact FLINT Bd/dB solver and complete baselines through n=7")


if __name__ == "__main__":
    _self_test()
