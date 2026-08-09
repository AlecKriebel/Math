#!/usr/bin/env python3
"""Exact rational check of the row-stochastic tangent/SOS identity."""

from fractions import Fraction as F


# A genuinely directed, loopless row-stochastic kernel.
ROW_WEIGHTS = (
    (0, 2, 1, 4, 3),
    (5, 0, 2, 1, 2),
    (1, 7, 0, 1, 1),
    (3, 1, 5, 0, 1),
    (2, 1, 1, 6, 0),
)

N = len(ROW_WEIGHTS)
P = tuple(
    tuple(F(value, sum(row)) for value in row) for row in ROW_WEIGHTS
)
TAU = tuple(sum(P[v][i] for v in range(N)) for i in range(N))


def occupied(state: int) -> list[int]:
    return [i for i in range(N) if state >> i & 1]


def x_value(state: int, vertex: int) -> F:
    return sum(P[vertex][i] for i in occupied(state))


def verify_state(state: int) -> None:
    members = occupied(state)
    k = len(members)
    outside = [v for v in range(N) if v not in members]
    x = [x_value(state, v) for v in range(N)]
    u = sum(2 * x[v] / (1 + x[v]) for v in outside)
    d = sum((1 - x[v]) / (1 + x[v]) for v in members)
    base = -F(N + k - 1, N) * u + F(2 * (N + k - 2), N) * d

    temperature = sum(TAU[i] for i in members)
    internal = sum(P[v][i] for v in members for i in members)
    z = F(k * (k - 1), N - 1) - internal

    alpha = F(2 * (N - 1) ** 2, N * (N + k - 1))
    beta = F(4 * (N - 1) ** 2, N * (N + k - 2))
    gamma = beta - alpha
    rhs = -alpha * (temperature - k) + gamma * z
    rhs += alpha * sum(
        (x[v] - F(k, N - 1)) ** 2 / (1 + x[v]) for v in outside
    )
    rhs += beta * sum(
        (x[v] - F(k - 1, N - 1)) ** 2 / (1 + x[v]) for v in members
    )
    assert base == rhs

    # Independently check the two aggregate first-moment identities.
    assert sum(x[v] - F(k - 1, N - 1) for v in members) == -z
    assert sum(x[v] - F(k, N - 1) for v in outside) == temperature - k + z


def main() -> None:
    assert all(P[i][i] == 0 and sum(P[i]) == 1 for i in range(N))
    assert any(P[i][j] != P[j][i] for i in range(N) for j in range(N))
    for state in range(1, (1 << N) - 1):
        verify_state(state)
    print("all exact directed tangent/SOS checks passed")


if __name__ == "__main__":
    main()
