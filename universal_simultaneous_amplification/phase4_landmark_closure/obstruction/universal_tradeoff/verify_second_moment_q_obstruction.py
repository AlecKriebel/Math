#!/usr/bin/env python3
"""Exact checks for SECOND_MOMENT_Q_OBSTRUCTION.md.

This script proves two deliberately distinct facts:

1. a positive four-vertex pseudo-law annihilates every singleton drift and
   the drift of Q, but has a positive second-moment target;
2. the true invariant law on that graph has a strictly negative target.

The first fact rules out the singleton-plus-Q proof architecture.  The
second prevents misreading the pseudo-law as an actual graph counterexample.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations


def popcount(state: int) -> int:
    return bin(state).count("1")


def h(value: F) -> F:
    return 2 * value / (1 + value)


def transition(weights: list[list[int]]) -> list[list[F]]:
    return [[F(value, sum(row)) for value in row] for row in weights]


def exact_union_law(row: list[F]) -> dict[int, F]:
    """Law of the distinct sites in a geometric(1/2) sequence of draws."""

    support = [i for i, value in enumerate(row) if value]
    size = len(support)
    exact = [F(0) for _ in range(1 << size)]

    # For nonempty L, this is P(U subseteq L and U nonempty) in the
    # containment convention needed by Boolean Mobius inversion.
    for mask in range(1, 1 << size):
        mass = sum(
            row[support[j]] for j in range(size) if (mask >> j) & 1
        )
        exact[mask] = mass / (2 - mass)

    for j in range(size):
        for mask in range(1 << size):
            if (mask >> j) & 1:
                exact[mask] -= exact[mask ^ (1 << j)]

    answer: dict[int, F] = {}
    for mask in range(1, 1 << size):
        if exact[mask]:
            actual = sum(
                1 << support[j]
                for j in range(size)
                if (mask >> j) & 1
            )
            answer[actual] = exact[mask]

    assert all(value > 0 for value in answer.values())
    assert sum(answer.values()) == 1
    return answer


def q_value(P: list[list[F]], state: int) -> F:
    n = len(P)
    return sum(
        P[i][j]
        for i in range(n)
        for j in range(n)
        if (state >> i) & 1 and (state >> j) & 1
    )


def direct_drift(
    P: list[list[F]], laws: list[dict[int, F]], state: int
) -> tuple[list[F], F]:
    """Enumerate the exact geometric-union transition from one state."""

    n = len(P)
    dx = [F(0) for _ in range(n)]
    dq = F(0)
    old_q = q_value(P, state)
    for v in range(n):
        if not (state >> v) & 1:
            continue
        for union, probability in laws[v].items():
            new_state = (state & ~(1 << v)) | union
            for i in range(n):
                dx[i] += probability * (
                    ((new_state >> i) & 1) - ((state >> i) & 1)
                )
            dq += probability * (q_value(P, new_state) - old_q)
    return dx, dq


def formula_drift(P: list[list[F]], state: int) -> tuple[list[F], F]:
    """Singleton drift and formula (10) of the note."""

    n = len(P)
    H = [[h(P[v][i]) for i in range(n)] for v in range(n)]
    s = [[P[i][j] + P[j][i] for j in range(n)] for i in range(n)]
    occupied = [i for i in range(n) if (state >> i) & 1]
    holes = [i for i in range(n) if not (state >> i) & 1]

    dx = [
        (-1 if i in occupied else 0)
        + (sum(H[v][i] for v in occupied) if i in holes else 0)
        for i in range(n)
    ]

    dq = F(0)
    for v in occupied:
        dq -= sum(s[v][j] for j in occupied if j != v)
        dq += sum(
            H[v][i] * sum(s[i][j] for j in occupied if j != v)
            for i in holes
        )
        dq += sum(
            (H[v][i] + H[v][j] - h(P[v][i] + P[v][j])) * s[i][j]
            for i, j in combinations(holes, 2)
        )
    return dx, dq


def full_generator(
    P: list[list[F]], laws: list[dict[int, F]]
) -> tuple[list[int], list[list[F]]]:
    n = len(P)
    states = list(range(1, 1 << n))
    index = {state: position for position, state in enumerate(states)}
    generator = [[F(0) for _ in states] for _ in states]
    for state in states:
        row = index[state]
        for v in range(n):
            if not (state >> v) & 1:
                continue
            for union, probability in laws[v].items():
                new_state = (state & ~(1 << v)) | union
                if new_state != state:
                    generator[row][index[new_state]] += probability
        generator[row][row] = -sum(generator[row])
    return states, generator


def exact_stationary(generator: list[list[F]]) -> list[F]:
    size = len(generator)
    matrix = [
        [generator[j][i] for j in range(size)]
        for i in range(size)
    ]
    matrix[size - 1] = [F(1) for _ in range(size)]
    rhs = [F(0) for _ in range(size)]
    rhs[size - 1] = 1

    # Exact Gauss--Jordan elimination on the augmented system.
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if augmented[row][column]
        )
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    left - scale * right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    pi = [augmented[row][-1] for row in range(size)]

    assert sum(pi) == 1
    assert all(value >= 0 for value in pi)
    for column in range(size):
        assert sum(pi[row] * generator[row][column] for row in range(size)) == 0
    return pi


def main() -> None:
    weights = [
        [0, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 2],
        [1, 1, 2, 0],
    ]
    P = transition(weights)
    assert P == [
        [F(0), F(1, 3), F(1, 3), F(1, 3)],
        [F(1, 3), F(0), F(1, 3), F(1, 3)],
        [F(1, 4), F(1, 4), F(0), F(1, 2)],
        [F(1, 4), F(1, 4), F(1, 2), F(0)],
    ]
    laws = [exact_union_law(row) for row in P]

    # Verify the declared DQ formula against the full burst law on every
    # proper state.  The full state is transient and irrelevant to the
    # Farkas certificate, but the formula also holds there.
    formula_checks = 0
    size_identity_checks = 0
    for state in range(1, 1 << 4):
        direct_dx, direct_dq = direct_drift(P, laws, state)
        formula_dx, formula_dq = formula_drift(P, state)
        assert direct_dx == formula_dx
        assert direct_dq == formula_dq
        formula_checks += 1

        size = popcount(state)
        size_drift = sum(direct_dx)
        C = q_value(P, state)
        R2 = sum(
            P[v][i] ** 2 / (1 + P[v][i])
            for v in range(4)
            for i in range(4)
            if (state >> v) & 1 and not (state >> i) & 1
        )
        assert C + R2 == F(size - size_drift, 2)
        size_identity_checks += 1

    pseudo = {
        0b0010: F(149, 7043),
        0b0100: F(40917, 70430),
        0b1000: F(384, 35215),
        0b1001: F(12071, 133817),
        0b1010: F(9836, 133817),
        0b1011: F(3145, 14086),
    }
    assert all(value > 0 for value in pseudo.values())
    assert sum(pseudo.values()) == 1

    expected_dx = [F(0) for _ in range(4)]
    expected_dq = F(0)
    expected_target = F(0)
    for state, mass in pseudo.items():
        dx, dq = formula_drift(P, state)
        for i in range(4):
            expected_dx[i] += mass * dx[i]
        expected_dq += mass * dq
        size = popcount(state)
        expected_target += mass * (F(size * size, 4) - F(size, 2))

    assert expected_dx == [F(0), F(0), F(0), F(0)]
    assert expected_dq == 0
    assert expected_target == F(100, 7043) > 0

    states, generator = full_generator(P, laws)
    pi = exact_stationary(generator)
    mean = sum(mass * popcount(state) for state, mass in zip(states, pi))
    second = sum(
        mass * popcount(state) ** 2 for state, mass in zip(states, pi)
    )
    true_margin = mean / 2 - second / 4
    assert mean == F(28299, 16711)
    assert second == F(55968, 16711)
    assert true_margin == F(315, 33422) > 0

    print(f"PASS: {formula_checks} exact Q-drift checks")
    print(f"PASS: {size_identity_checks} exact C+R2 identity checks")
    print("PASS: exact singleton-plus-Q Farkas obstruction")
    print(f"pseudo-law target = {expected_target}")
    print("PASS: exact full-chain stationary separation")
    print(f"true stationary margin = {true_margin}")
    print("OPEN: universal second-moment inequality")


if __name__ == "__main__":
    main()
