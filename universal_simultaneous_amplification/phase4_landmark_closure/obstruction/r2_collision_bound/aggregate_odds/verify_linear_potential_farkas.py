#!/usr/bin/env python3
"""Exact verifier for the nonnegative linear-potential Farkas obstruction."""

from __future__ import annotations

from fractions import Fraction as F


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    n = len(matrix)
    augmented = [matrix[row][:] + [rhs[row]] for row in range(n)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    left - scale * right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(n)]


def h(value: F) -> F:
    return 2 * value / (1 + value)


def geometric_union_law(row: list[F]) -> dict[int, F]:
    """Law of the distinct sites in K geometric(1/2) row samples."""

    n = len(row)
    values = [F(0) for _ in range(1 << n)]
    for mask in range(1 << n):
        mass = sum((row[j] for j in range(n) if mask >> j & 1), F(0))
        values[mask] = mass / (2 - mass)
    for j in range(n):
        for mask in range(1 << n):
            if mask >> j & 1:
                values[mask] -= values[mask ^ (1 << j)]
    law = {mask: values[mask] for mask in range(1, 1 << n) if values[mask]}
    assert sum(law.values()) == 1
    assert all(probability > 0 for probability in law.values())
    return law


def dual_generator(P: list[list[F]]) -> list[list[F]]:
    n = len(P)
    size = (1 << n) - 1
    laws = [geometric_union_law(row) for row in P]
    generator = [[F(0) for _ in range(size)] for _ in range(size)]
    for state in range(1, 1 << n):
        row = state - 1
        for vertex in range(n):
            if not (state >> vertex & 1):
                continue
            for offspring, probability in laws[vertex].items():
                new_state = (state & ~(1 << vertex)) | offspring
                if new_state != state:
                    generator[row][new_state - 1] += probability
        generator[row][row] = -sum(generator[row])
    return generator


def stationary(generator: list[list[F]]) -> list[F]:
    size = len(generator)
    matrix = [
        [generator[column][row] for column in range(size)]
        for row in range(size)
    ]
    rhs = [F(0) for _ in range(size)]
    matrix[-1] = [F(1) for _ in range(size)]
    rhs[-1] = F(1)
    law = solve(matrix, rhs)
    assert sum(law) == 1
    # Every nonempty proper state is in the closed irreducible class.  The
    # full set is transient: every burst removes its ringing source.
    assert all(mass > 0 for mass in law[:-1])
    assert law[-1] == 0
    for column in range(size):
        assert sum(law[row] * generator[row][column] for row in range(size)) == 0
    return law


def main() -> None:
    n = 5
    edge_order = [(i, j) for i in range(n) for j in range(i + 1, n)]
    edge_weights = (1, 2, 5, 2, 200, 1, 5, 1, 1, 1)
    weights = [[0 for _ in range(n)] for _ in range(n)]
    for value, (i, j) in zip(edge_weights, edge_order):
        weights[i][j] = weights[j][i] = value
    assert all(weights[i][j] > 0 for i in range(n) for j in range(i + 1, n))

    degrees = [sum(row) for row in weights]
    assert degrees == [10, 207, 204, 8, 9]
    P = [[F(value, degrees[i]) for value in row] for i, row in enumerate(weights)]
    H = [[h(value) for value in row] for row in P]

    generator = dual_generator(P)
    pi = stationary(generator)
    p = [
        sum(pi[state - 1] for state in range(1, 1 << n) if state >> i & 1)
        for i in range(n)
    ]
    q = [1 - value for value in p]
    r = [1 / value - 2 for value in q]

    # These two exact marginal bounds imply r_1>17/500 and r_2>1/1000.
    assert p[1] > F(517, 1017)
    assert p[2] > F(1001, 2001)
    assert r[1] > F(17, 500)
    assert r[2] > F(1, 1000)
    assert r[4] > -1

    y = [F(0), F(1), F(1977, 2000), F(0), F(3, 100)]
    dual_slacks = [
        sum(H[i][j] * y[i] for i in range(n)) - y[j]
        for j in range(n)
    ]
    assert dual_slacks == [
        F(73127, 1841125),
        F(1, 7070),
        F(49, 162800),
        F(16829, 666250),
        F(291331, 10865000),
    ]
    assert all(value > 0 for value in dual_slacks)

    farkas_dot = sum(y[i] * r[i] for i in range(n))
    transparent_lower_bound = F(9977, 2_000_000)
    assert farkas_dot > transparent_lower_bound > 0

    # The graph itself strictly satisfies every component-odds inequality.
    component_slacks = [
        2 * sum(P[v][i] * p[v] for v in range(n)) - p[i] / q[i]
        for i in range(n)
    ]
    rational_lower_bounds = [F(1, 25), F(1, 20), F(1, 25), F(3, 100), F(1, 100)]
    assert all(
        slack > lower
        for slack, lower in zip(component_slacks, rational_lower_bounds)
    )
    aggregate_slack = sum(component_slacks)
    assert aggregate_slack > 0

    # Check the stationary integrand identity E b = -aggregate_slack.
    expected_b = F(0)
    for state in range(1, 1 << n):
        occupied = [i for i in range(n) if state >> i & 1]
        holes = [i for i in range(n) if not (state >> i & 1)]
        b_state = sum(
            H[v][u] / q[u] for v in occupied for u in holes
        ) - 2 * len(occupied)
        expected_b += pi[state - 1] * b_state
    assert expected_b == -aggregate_slack

    print("PASS: exact five-vertex Farkas obstruction")
    print("degrees:", degrees)
    print("H^T y-y:", dual_slacks)
    print("y^T r lower bound:", transparent_lower_bound)
    print("exact y^T r:", farkas_dot)
    print("component slacks (decimal summaries):", [float(x) for x in component_slacks])
    print("aggregate slack (decimal summary):", float(aggregate_slack))


if __name__ == "__main__":
    main()
