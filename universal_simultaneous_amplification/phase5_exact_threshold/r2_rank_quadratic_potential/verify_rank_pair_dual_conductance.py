#!/usr/bin/env python3
"""Independent exact verifier for the rank-pair dual conductance laws.

This script deliberately does not import the floating discovery programs.
All transition rates, Green occupations, and identities are evaluated over
fractions.Fraction.
"""

from __future__ import annotations

from fractions import Fraction as F


WEIGHTS = (
    (0, 2, 0, 1),
    (2, 0, 3, 0),
    (0, 3, 0, 4),
    (1, 0, 4, 0),
)


def solve_linear(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Solve a nonsingular square rational system by Gauss-Jordan."""

    n = len(rhs)
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    a - scale * b
                    for a, b in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(n)]


def bit(state: int, vertex: int) -> bool:
    return bool(state >> vertex & 1)


def build_kernel():
    n = len(WEIGHTS)
    degree = [sum(row) for row in WEIGHTS]
    kernel = [
        [F(WEIGHTS[v][i], degree[v]) for i in range(n)] for v in range(n)
    ]
    total_degree = sum(degree)
    stationary = [F(value, total_degree) for value in degree]
    conductance = [
        [stationary[v] * kernel[v][i] for i in range(n)] for v in range(n)
    ]
    assert all(sum(row) == 1 for row in kernel)
    assert sum(stationary) == 1
    assert all(
        conductance[v][i] == conductance[i][v]
        for v in range(n)
        for i in range(n)
    )
    return kernel, stationary, conductance


P, PI, CONDUCTANCE = build_kernel()
N = len(P)
FULL = (1 << N) - 1


def x_value(state: int, vertex: int) -> F:
    return sum(P[vertex][i] for i in range(N) if bit(state, i))


def rates(state: int) -> list[tuple[int, F]]:
    result = []
    for vertex in range(N):
        x = x_value(state, vertex)
        if bit(state, vertex):
            rate = (1 - x) / (1 + x)
        else:
            rate = 2 * x / (1 + x)
        if rate:
            result.append((state ^ (1 << vertex), rate))
    return result


def mass(state: int) -> F:
    return sum(PI[i] for i in range(N) if bit(state, i))


def internal(state: int) -> F:
    return sum(
        CONDUCTANCE[i][j]
        for i in range(N)
        for j in range(i + 1, N)
        if bit(state, i) and bit(state, j)
    )


def storage(state: int) -> F:
    return mass(state) + internal(state)


def cut(state: int) -> F:
    return sum(
        CONDUCTANCE[i][j]
        for i in range(N)
        for j in range(N)
        if bit(state, i) and not bit(state, j)
    )


def generator(state: int, values: list[F]) -> F:
    return sum(rate * (values[target] - values[state]) for target, rate in rates(state))


def exact_green_occupation():
    transient = list(range(1, FULL))
    index = {state: j for j, state in enumerate(transient)}
    size = len(transient)
    q = [[F(0) for _ in transient] for _ in transient]
    for state in transient:
        row = index[state]
        outgoing = rates(state)
        q[row][row] -= sum(rate for _, rate in outgoing)
        for target, rate in outgoing:
            if target in index:
                q[row][index[target]] += rate

    initial = [F(1, N) if state.bit_count() == 1 else F(0) for state in transient]
    transpose = [[q[column][row] for column in range(size)] for row in range(size)]
    occupation = solve_linear(transpose, [-value for value in initial])

    # Independently solve the harmonic fixation equations.
    rhs = []
    harmonic_matrix = []
    for state in transient:
        row = [F(0) for _ in transient]
        outgoing = rates(state)
        row[index[state]] -= sum(rate for _, rate in outgoing)
        full_rate = F(0)
        for target, rate in outgoing:
            if target in index:
                row[index[target]] += rate
            elif target == FULL:
                full_rate += rate
        harmonic_matrix.append(row)
        rhs.append(-full_rate)
    fixation = solve_linear(harmonic_matrix, rhs)
    rho = sum(
        fixation[index[1 << vertex]] / N for vertex in range(N)
    )
    return transient, occupation, rho


def verify_storage_identities() -> None:
    h_values = [storage(state) for state in range(FULL + 1)]
    c_values = [cut(state) for state in range(FULL + 1)]
    assert storage(0) == 0
    assert storage(FULL) == F(3, 2)
    assert sum(storage(1 << i) for i in range(N)) / N == F(1, N)
    for state in range(1, FULL):
        for vertex in range(N):
            target = state ^ (1 << vertex)
            if bit(state, vertex):
                expected = -PI[vertex] * (1 + x_value(state, vertex))
            else:
                expected = PI[vertex] * (1 + x_value(state, vertex))
            assert h_values[target] - h_values[state] == expected
        assert generator(state, h_values) == c_values[state]

    # Check the full rank-weighted drift identity for a nontrivial sequence.
    q = [F((k + 2) * (k + 3), 2 * k + 3) for k in range(N + 1)]
    weighted = [q[state.bit_count()] * h_values[state] for state in range(FULL + 1)]
    for state in range(1, FULL):
        k = state.bit_count()
        u = sum(rate for target, rate in rates(state) if target.bit_count() == k + 1)
        d = sum(rate for target, rate in rates(state) if target.bit_count() == k - 1)
        right = h_values[state] * ((q[k + 1] - q[k]) * u + (q[k - 1] - q[k]) * d)
        right += c_values[state] * (2 * q[k + 1] - q[k - 1])
        assert generator(state, weighted) == right

    # In optional coordinates, the geometric rank profile turns the cut
    # reward into an exact drift on every (not necessarily complete) graph.
    geometric = [F(1, 2 ** (N - k)) for k in range(N + 1)]
    optional_values = [
        geometric[state.bit_count()] * h_values[state]
        for state in range(FULL + 1)
    ]
    for state in range(1, FULL):
        k = state.bit_count()
        optional_drift = F(0)
        for target, rate in rates(state):
            if target.bit_count() == k + 1:
                optional_drift += rate * (optional_values[target] - 2 * optional_values[state])
            else:
                optional_drift += rate * (4 * optional_values[target] - 2 * optional_values[state])
        assert optional_drift == 2 * geometric[k] * c_values[state]


def verify_dual_and_rank_recurrences() -> F:
    transient, occupation, rho = exact_green_occupation()
    y = {state: occupation[j] for j, state in enumerate(transient)}
    # The chosen sparse support has two transient configurations which are
    # not reached from a singleton, so nonnegativity (rather than strict
    # positivity) is the correct Green-law check.
    assert all(value >= 0 for value in occupation)

    # Full statewise dual conservation is stronger than rank-pair balance.
    for target in range(1, FULL + 1):
        residual = F(1, N) if target.bit_count() == 1 else F(0)
        for state in transient:
            outgoing = rates(state)
            residual -= y[state] * sum(rate for _, rate in outgoing) * (state == target)
            residual += y[state] * sum(
                rate for destination, rate in outgoing if destination == target
            )
        residual -= rho * (target == FULL)
        assert residual == 0

    a = [F(0) for _ in range(N + 1)]
    r = [F(0) for _ in range(N + 1)]
    xh = [F(0) for _ in range(N + 1)]
    yh = [F(0) for _ in range(N + 1)]
    cuts = [F(0) for _ in range(N + 1)]
    for state in transient:
        k = state.bit_count()
        up = sum(rate for target, rate in rates(state) if target.bit_count() == k + 1)
        down = sum(rate for target, rate in rates(state) if target.bit_count() == k - 1)
        a[k] += y[state] * up
        r[k] += y[state] * down
        xh[k] += y[state] * storage(state) * up
        yh[k] += y[state] * storage(state) * down
        cuts[k] += y[state] * cut(state)

    for k in range(1, N + 1):
        mass_residual = (k == 1) + a[k - 1]
        mass_residual += r[k + 1] if k < N else 0
        mass_residual -= a[k] + r[k] + rho * (k == N)
        assert mass_residual == 0

        storage_residual = F(1, N) * (k == 1)
        storage_residual += xh[k - 1] + 2 * cuts[k - 1]
        if k < N:
            storage_residual += yh[k + 1] - cuts[k + 1]
        storage_residual -= xh[k] + yh[k] + F(3, 2) * rho * (k == N)
        assert storage_residual == 0

    assert rho == a[N - 1] == 1 - r[1]
    assert F(1, N) + sum(cuts) == F(3, 2) * rho
    return rho


def main() -> None:
    verify_storage_identities()
    rho = verify_dual_and_rank_recurrences()
    print("all exact rank-pair/conductance checks passed")
    print("test-graph fixation numerator", rho.numerator)
    print("test-graph fixation denominator", rho.denominator)


if __name__ == "__main__":
    main()
