#!/usr/bin/env python3
"""Exact QQ replay for the 23-vertex simultaneous weak theta amplifier."""

from __future__ import annotations

from itertools import combinations

from flint import fmpq as Q
from flint import fmpq_mat


def theta_graph(arms: int = 7, endpoint_weight: Q = Q(103, 500)):
    order = 2 + 3 * arms
    weights = [[Q(0) for _ in range(order)] for _ in range(order)]

    def add_edge(i: int, j: int, value: Q) -> None:
        weights[i][j] = weights[j][i] = value

    for arm in range(arms):
        left = 2 + 3 * arm
        middle = left + 1
        right = left + 2
        add_edge(0, left, endpoint_weight)
        add_edge(left, middle, Q(1))
        add_edge(middle, right, Q(1))
        add_edge(right, 1, endpoint_weight)
    return weights


def weak_coefficient(weights, rule: str) -> Q:
    order = len(weights)
    degree = [sum(row, Q(0)) for row in weights]
    total_degree = sum(degree, Q(0))
    harmonic_degree = sum((Q(1) / value for value in degree), Q(0))
    C = Q(1) / harmonic_degree

    rate = [[Q(0) for _ in range(order)] for _ in range(order)]
    for i in range(order):
        for j in range(order):
            denominator = degree[j] if rule == "Bd" else degree[i]
            rate[i][j] = weights[i][j] / denominator
    leave = [sum(row, Q(0)) for row in rate]

    pairs = list(combinations(range(order), 2))
    index = {pair: k for k, pair in enumerate(pairs)}
    system = fmpq_mat(len(pairs), len(pairs))
    source = fmpq_mat(len(pairs), 1)
    for row, (i, j) in enumerate(pairs):
        source[row, 0] = 1
        system[row, row] = leave[i] + leave[j]
        for k in range(order):
            if k != j and rate[i][k]:
                system[row, index[tuple(sorted((k, j)))]] -= rate[i][k]
            if k != i and rate[j][k]:
                system[row, index[tuple(sorted((i, k)))]] -= rate[j][k]

    meeting = system.solve(source)
    assert system * meeting == source

    coefficient = Q(0)
    if rule == "Bd":
        for row, (i, j) in enumerate(pairs):
            coefficient += (
                weights[i][j] * meeting[row, 0] / (degree[i] * degree[j])
            )
        coefficient *= 2 * C / order
    elif rule == "dB":
        for row, (i, j) in enumerate(pairs):
            wedge = sum(
                (
                    weights[v][i] * weights[v][j] / degree[v]
                    for v in range(order)
                ),
                Q(0),
            )
            coefficient += 2 * wedge * meeting[row, 0] / (order * total_degree)
    else:
        raise ValueError(rule)
    return coefficient


def main() -> None:
    weights = theta_graph()
    order = len(weights)
    degree = [sum(row, Q(0)) for row in weights]
    assert order == 23
    assert sorted(degree) == sorted(
        [Q(721, 500)] * 2 + [Q(603, 500)] * 14 + [Q(2)] * 7
    )

    bd = weak_coefficient(weights, "Bd")
    db = weak_coefficient(weights, "dB")
    expected_bd = Q(
        443330487524299675208486212,
        926460931665398277422905559,
    )
    expected_db = Q(284789678, 623264051)
    assert bd == expected_bd
    assert db == expected_db

    bd_baseline = Q(11, 23)
    db_baseline = Q(21, 46)
    bd_excess = bd - bd_baseline
    db_excess = db - db_baseline
    assert bd_excess == Q(
        240476727804846875792249,
        926460931665398277422905559,
    )
    assert db_excess == Q(512179, 1246528102)
    assert bd_excess > 0 and db_excess > 0

    midpoint_excess = 2 * order * (bd_excess + db_excess)
    assert midpoint_excess == Q(
        33664123156747757687570792981933,
        1091549703899830447854483854239621,
    )
    assert midpoint_excess > 0

    print(f"Bd coefficient={bd}")
    print(f"Bd excess={bd_excess} (~{float(bd_excess):.15g})")
    print(f"dB coefficient={db}")
    print(f"dB excess={db_excess} (~{float(db_excess):.15g})")
    print(f"N(-1)+N(1)-46={midpoint_excess}")
    print("PASS exact finite simultaneous weak amplification")
    print("PASS exact power-midpoint refutation")


if __name__ == "__main__":
    main()
