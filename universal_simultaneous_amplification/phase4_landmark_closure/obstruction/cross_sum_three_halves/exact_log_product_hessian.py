#!/usr/bin/env python3
"""Exact second variations of the log fixation product at K_n.

Permutation symmetry splits zero-sum edge perturbations into a vertex-degree
mode and a zero-row-sum cycle mode.  This verifier differentiates the full
labelled absorbing systems exactly (no finite differences) for n=4,5,6.
It is a local certificate, not a global concavity theorem.
"""

from __future__ import annotations

from functools import lru_cache

import sympy as sp


R = sp.Rational(3, 2)
E = sp.symbols("e")


def directions(n: int):
    degree_vertex = [sp.Integer(1)] + [sp.Rational(-1, n - 1)] * (n - 1)
    degree = [[sp.Integer(0) for _ in range(n)] for _ in range(n)]
    cycle = [[sp.Integer(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            degree[i][j] = degree[j][i] = degree_vertex[i] + degree_vertex[j]
    for i, j, value in ((0, 1, 1), (2, 3, 1), (0, 2, -1), (1, 3, -1)):
        cycle[i][j] = cycle[j][i] = sp.Integer(value)
    assert all(sum(row) == 0 for row in cycle)
    return degree, cycle


@lru_cache(maxsize=None)
def derivatives(expression: sp.Expr):
    return tuple(sp.cancel(sp.diff(expression, E, order).subs(E, 0)) for order in range(3))


def systems(n: int, direction, rule: str):
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    weights = [
        [sp.Integer(0) if i == j else 1 + E * direction[i][j] for j in range(n)]
        for i in range(n)
    ]
    degree = [sum(row) for row in weights]
    matrices = [sp.zeros(len(states)) for _ in range(3)]
    vectors = [sp.zeros(len(states), 1) for _ in range(3)]
    for state in states:
        row = index[state]
        mutant = [bool(state & (1 << i)) for i in range(n)]
        for target in range(n):
            if rule == "Bd":
                mutant_mass = sum(
                    weights[parent][target] / degree[parent]
                    for parent in range(n)
                    if mutant[parent]
                )
                resident_mass = sum(
                    weights[parent][target] / degree[parent]
                    for parent in range(n)
                    if not mutant[parent]
                )
                rate = resident_mass if mutant[target] else R * mutant_mass
            elif rule == "dB":
                mutant_mass = sum(
                    weights[parent][target]
                    for parent in range(n)
                    if mutant[parent]
                )
                resident_mass = degree[target] - mutant_mass
                denominator = R * mutant_mass + resident_mass
                rate = (
                    resident_mass / denominator
                    if mutant[target]
                    else R * mutant_mass / denominator
                )
            else:
                raise ValueError(rule)
            if rate == 0:
                continue
            target_state = state ^ (1 << target)
            for order, value in enumerate(derivatives(rate)):
                matrices[order][row, row] += value
                if target_state == full:
                    vectors[order][row] += value
                elif target_state:
                    matrices[order][row, index[target_state]] -= value
    return matrices, vectors


def second_variation(n: int, direction, rule: str):
    matrices, vectors = systems(n, direction, rule)
    a0, a1, a2 = matrices
    b0, b1, b2 = vectors
    inverse = a0.inv()
    u0 = inverse * b0
    u1 = inverse * (b1 - a1 * u0)
    u2 = inverse * (b2 - a2 * u0 - 2 * a1 * u1)
    singleton = [((1 << i) - 1) for i in range(n)]
    rho0 = sp.cancel(sum(u0[row] for row in singleton) / n)
    rho1 = sp.cancel(sum(u1[row] for row in singleton) / n)
    rho2 = sp.cancel(sum(u2[row] for row in singleton) / n)
    assert rho1 == 0
    return rho0, rho2


def main():
    for n in (4, 5, 6, 7):
        degree, cycle = directions(n)
        records = []
        for label, direction in (("degree", degree), ("cycle", cycle)):
            bd0, bd2 = second_variation(n, direction, "Bd")
            db0, db2 = second_variation(n, direction, "dB")
            log_product = sp.cancel(bd2 / bd0 + db2 / db0)
            assert log_product < 0
            if label == "cycle":
                assert bd2 == 0
            records.append((label, bd2, db2, log_product))
        print("n", n)
        for record in records:
            print(*record)
    print("PASS: exact log-product Hessian is negative on both irreducible modes")


if __name__ == "__main__":
    main()
