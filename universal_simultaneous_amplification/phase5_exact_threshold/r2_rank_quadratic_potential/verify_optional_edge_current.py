#!/usr/bin/env python3
"""Exact check of the optional Farkas edge-current factorization.

The verifier constructs the symmetric complete-kernel obstruction at the
equality boundary.  It checks the edge grouping, all rank-quadratic moment
balances, the sharp endpoint ratio, and the conductance cut recurrence.
"""

from fractions import Fraction as F
from itertools import combinations
from math import comb


N = 6
FULL = (1 << N) - 1


def members(state: int) -> list[int]:
    return [i for i in range(N) if state >> i & 1]


def x_value(state: int, vertex: int) -> F:
    return F(sum(1 for i in members(state) if i != vertex), N - 1)


def g_rate(state: int, vertex: int) -> F:
    x = x_value(state, vertex)
    return 2 * x / (1 + x)


def l_rate(state: int, vertex: int) -> F:
    x = x_value(state, vertex)
    return (1 - x) / (1 + x)


def build_rank_weights() -> list[F]:
    # Normalize eta_(n-1)=1 per state.  Prescribe the geometrically
    # transported total currents, then solve each edge-current equation
    # backwards for eta_k.
    eta = [F(0) for _ in range(N + 1)]
    eta[N - 1] = F(1)
    for k in range(N - 2, 0, -1):
        total_current = F((1 << (N - 1 - k)) * N)
        edge_count = comb(N, k) * (N - k)
        per_edge = total_current / edge_count
        eta[k] = (
            F(N + k - 1, 2) * per_edge + (N - 1 - k) * eta[k + 1]
        ) / k
    assert all(value > 0 for value in eta[1:N])
    return eta


ETA_RANK = build_rank_weights()


def eta(state: int) -> F:
    return ETA_RANK[len(members(state))] if 0 < state < FULL else F(0)


def edge_current(state: int, vertex: int) -> F:
    target = state | (1 << vertex)
    return eta(state) * g_rate(state, vertex) - 2 * eta(target) * l_rate(target, vertex)


def storage(state: int) -> F:
    occupied = members(state)
    mass = F(len(occupied), N)
    internal = F(comb(len(occupied), 2), N * (N - 1))
    return mass + internal


def cut(state: int) -> F:
    k = len(members(state))
    return F(k * (N - k), N * (N - 1))


def correction(state: int) -> F:
    """A deterministic rank-quadratic correction with zero boundary."""

    if state == 0 or state == FULL:
        return F(0)
    occupied = members(state)
    k = len(occupied)
    value = F(3 * k - 7, 11)
    value += sum(F((k + 2) * (i + 1), 17) for i in occupied)
    value += sum(F((k + 1) * (i + j + 1), 23) for i, j in combinations(occupied, 2))
    if k == 1:
        # Subtract the uniform singleton average without changing degree.
        average = sum(F(3 - 7, 11) + F(3 * (i + 1), 17) for i in range(N)) / N
        value -= average
    return value


def optional_drift(state: int) -> F:
    value = F(0)
    for v in range(N):
        if state >> v & 1:
            value += l_rate(state, v) * (4 * correction(state ^ (1 << v)) - 2 * correction(state))
        else:
            value += g_rate(state, v) * (correction(state | (1 << v)) - 2 * correction(state))
    return value


def main() -> None:
    # Direct edge grouping of the optional drift.
    left = sum(eta(state) * optional_drift(state) for state in range(1, FULL))
    right = sum(
        edge_current(state, v) * (correction(state | (1 << v)) - 2 * correction(state))
        for state in range(FULL)
        for v in range(N)
        if not (state >> v & 1)
    )
    assert left == right == 0

    currents = [
        sum(
            edge_current(state, v)
            for state in range(FULL + 1)
            if len(members(state)) == k
            for v in range(N)
            if not (state >> v & 1)
        )
        for k in range(N)
    ]
    r1 = N * ETA_RANK[1]
    atop = N * ETA_RANK[N - 1]
    assert currents[0] == -2 * r1
    assert currents[N - 1] == atop
    for k in range(2, N):
        assert currents[k - 1] == 2 * currents[k]
    assert atop / r1 == F(2 * (N - 1), (N + 1) * 2 ** (N - 1) - 2 * N)

    # Base drift is zero on the complete equality ray.
    base_sum = F(0)
    for state in range(1, FULL):
        k = len(members(state))
        u = sum(g_rate(state, v) for v in range(N) if not (state >> v & 1))
        d = sum(l_rate(state, v) for v in range(N) if state >> v & 1)
        base = -F(N + k - 1, N) * u + F(2 * (N + k - 2), N) * d
        base_sum += eta(state) * base
    assert base_sum == 0

    # Boundary-aware conductance-production recurrence.
    h = [F(0) for _ in range(N)]
    c = [F(0) for _ in range(N)]
    for k in range(1, N):
        c[k] = sum(
            eta(state) * cut(state)
            for state in range(1, FULL)
            if len(members(state)) == k
        )
        h[k] = sum(
            storage(state)
            * sum(edge_current(state, v) for v in range(N) if not (state >> v & 1))
            for state in range(1, FULL)
            if len(members(state)) == k
        )
    for k in range(1, N - 1):
        assert 2 * h[k + 1] == h[k] + 2 * (c[k] - c[k + 1])
    theta = (currents[0] - 2 * currents[1]) / N
    assert h[1] == -c[1] - theta / 2
    assert h[N - 1] + 2 * c[N - 1] == F(3, 2) * atop

    rhs = (c[1] + (r1 + currents[1]) / N) / 2 ** (N - 2)
    rhs += sum(c[k] / 2 ** (N - 1 - k) for k in range(2, N))
    assert rhs == F(3, 2) * atop
    print("all exact optional edge-current checks passed")


if __name__ == "__main__":
    main()
