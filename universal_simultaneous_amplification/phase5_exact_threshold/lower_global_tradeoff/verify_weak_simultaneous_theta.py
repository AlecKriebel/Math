#!/usr/bin/env python3
"""Exact QQ replay for the 23-vertex simultaneous weak theta amplifier."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from itertools import permutations

from flint import fmpq as Q
from flint import fmpq_mat
import sympy as sp


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


def canonical_pair(pair):
    """Orbit label under arm permutations and global reflection."""

    candidates = []
    for reflect in (False, True):
        reflected = []
        for vertex in pair:
            if vertex[0] == "h":
                reflected.append(("h", 1 - vertex[1]) if reflect else vertex)
            else:
                reflected.append(
                    ("i", vertex[1], 2 - vertex[2]) if reflect else vertex
                )
        arms = sorted({vertex[1] for vertex in reflected if vertex[0] == "i"})
        for targets in permutations(range(len(arms))):
            relabel = dict(zip(arms, targets))
            labelled = [
                vertex
                if vertex[0] == "h"
                else ("i", relabel[vertex[1]], vertex[2])
                for vertex in reflected
            ]
            candidates.append(tuple(sorted(labelled)))
    return min(candidates)


def symbolic_orbit_excesses():
    """Solve the ten pair orbits over Q(x), independently of the QQ solve."""

    arms = 7
    x = sp.symbols("x", positive=True)
    vertices = [("h", 0), ("h", 1)] + [
        ("i", arm, position)
        for arm in range(arms)
        for position in range(3)
    ]
    pair_orbits = defaultdict(list)
    for pair in combinations(vertices, 2):
        pair_orbits[canonical_pair(pair)].append(pair)
    orbit_labels = sorted(pair_orbits)
    orbit_index = {label: k for k, label in enumerate(orbit_labels)}
    assert len(orbit_labels) == 10

    def weight(left, right):
        if left[0] == "i" and right[0] == "h":
            left, right = right, left
        if left[0] == "h" and right[0] == "i":
            return x if (
                (left[1] == 0 and right[2] == 0)
                or (left[1] == 1 and right[2] == 2)
            ) else sp.Integer(0)
        if (
            left[0] == right[0] == "i"
            and left[1] == right[1]
            and abs(left[2] - right[2]) == 1
        ):
            return sp.Integer(1)
        return sp.Integer(0)

    def degree(vertex):
        if vertex[0] == "h":
            return arms * x
        return x + 1 if vertex[2] in (0, 2) else sp.Integer(2)

    order = len(vertices)
    total_degree = sum(degree(vertex) for vertex in vertices)
    C = 1 / sum(1 / degree(vertex) for vertex in vertices)
    excesses = {}
    for rule in ("Bd", "dB"):
        system = sp.zeros(len(orbit_labels))
        for label, row in orbit_index.items():
            i, j = pair_orbits[label][0]
            for current, other in ((i, j), (j, i)):
                for target in vertices:
                    edge_weight = weight(current, target)
                    if not edge_weight:
                        continue
                    denominator = degree(target) if rule == "Bd" else degree(current)
                    rate = edge_weight / denominator
                    system[row, row] += rate
                    if target != other:
                        column = orbit_index[canonical_pair((target, other))]
                        system[row, column] -= rate
        meeting = system.inv() * sp.ones(len(orbit_labels), 1)

        coefficient = 0
        for label, row in orbit_index.items():
            load = 0
            for i, j in pair_orbits[label]:
                if rule == "Bd":
                    load += (
                        2 * C * weight(i, j) / (order * degree(i) * degree(j))
                    )
                else:
                    wedge = sum(
                        weight(vertex, i) * weight(vertex, j) / degree(vertex)
                        for vertex in vertices
                    )
                    load += 2 * wedge / (order * total_degree)
            coefficient += load * meeting[row]
        baseline = sp.Rational(11, 23) if rule == "Bd" else sp.Rational(21, 46)
        excesses[rule] = sp.factor(coefficient - baseline)
    return x, excesses


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

    x, excesses = symbolic_orbit_excesses()
    P_B = (
        180018405 * x**7
        + 2975072149 * x**6
        + 13161584556 * x**5
        + 17094630950 * x**4
        + 2810292145 * x**3
        - 858773619 * x**2
        - 105248866 * x
        - 1878120
    )
    Q_B = (
        1786365 * x**5
        + 15512608 * x**4
        + 34819480 * x**3
        + 14633270 * x**2
        + 1659563 * x
        + 52170
    )
    expected_bd_excess = P_B / (
        23 * (49 * x**2 + 249 * x + 4) * Q_B
    )
    dB_quadratic = 9576 * x**2 + 2473 * x - 924
    expected_db_excess = -dB_quadratic / (
        46 * (672 * x**2 + 743 * x + 252)
    )
    assert sp.factor(excesses["Bd"] - expected_bd_excess) == 0
    assert sp.factor(excesses["dB"] - expected_db_excess) == 0
    # Descartes: coefficients in increasing order are ---+++++, so exactly
    # one positive root (existence follows from the endpoint signs).
    assert sp.gcd(sp.Poly(P_B, x), sp.Poly(sp.diff(P_B, x), x)) == 1
    assert sp.Poly(P_B, x).count_roots(0, sp.oo) == 1
    assert sp.Poly(dB_quadratic, x).count_roots(0, sp.oo) == 1
    witness = sp.Rational(103, 500)
    assert P_B.subs(x, witness) > 0
    assert dB_quadratic.subs(x, witness) < 0

    print(f"Bd coefficient={bd}")
    print(f"Bd excess={bd_excess} (~{float(bd_excess):.15g})")
    print(f"dB coefficient={db}")
    print(f"dB excess={db_excess} (~{float(db_excess):.15g})")
    print(f"N(-1)+N(1)-46={midpoint_excess}")
    print("PASS exact ten-orbit formulas and complete x-interval classification")
    print("PASS exact finite simultaneous weak amplification")
    print("PASS exact power-midpoint refutation")


if __name__ == "__main__":
    main()
