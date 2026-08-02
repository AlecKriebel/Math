#!/usr/bin/env python3
"""Exact certificates for higher-threshold construction primitives."""

from __future__ import annotations

import sympy as sp


r = sp.symbols("r", positive=True)


def triangle_fixation(weights: sp.Matrix, rule: str):
    size = weights.rows
    full = (1 << size) - 1
    states = list(range(1, full))
    index = {mask: i for i, mask in enumerate(states)}
    degree = [sum(weights[i, j] for j in range(size)) for i in range(size)]
    matrix = sp.zeros(len(states))
    rhs = sp.zeros(len(states), 1)
    for mask, row in index.items():
        mutant = [bool(mask >> v & 1) for v in range(size)]
        changes = []
        if rule == "Bd":
            total_fitness = size + (r - 1) * sum(mutant)
            for parent in range(size):
                for target in range(size):
                    if not weights[parent, target] or mutant[parent] == mutant[target]:
                        continue
                    rate = (
                        (r if mutant[parent] else 1)
                        * weights[parent, target]
                        / (total_fitness * degree[parent])
                    )
                    target_mask = mask | (1 << target) if mutant[parent] else mask & ~(1 << target)
                    changes.append((target_mask, rate))
        elif rule == "dB":
            for target in range(size):
                denominator = sum(
                    (r if mutant[parent] else 1) * weights[parent, target]
                    for parent in range(size)
                )
                for parent in range(size):
                    if not weights[parent, target] or mutant[parent] == mutant[target]:
                        continue
                    rate = (
                        (r if mutant[parent] else 1)
                        * weights[parent, target]
                        / (size * denominator)
                    )
                    target_mask = mask | (1 << target) if mutant[parent] else mask & ~(1 << target)
                    changes.append((target_mask, rate))
        else:
            raise ValueError(rule)
        matrix[row, row] = sum(rate for _, rate in changes)
        for target_mask, rate in changes:
            if target_mask == full:
                rhs[row] += rate
            elif target_mask:
                matrix[row, index[target_mask]] -= rate
    values = matrix.inv() * rhs
    return tuple(sp.factor(values[index[1 << v]]) for v in range(size))


def check_two_edge_module():
    p = (r - 1) / r
    alpha_bd = r**3 / ((r + 1) * (r**2 + 1))
    alpha_db = r**2 / (2 * (r**2 + 1))
    beta_bd = 1 / ((r + 1) * (r**2 + 1))
    beta_db = 1 / (2 * (r**2 + 1))
    establishment_polynomial = r**3 - 2 * r**2 + 2 * r - 2

    assert sp.cancel(
        alpha_bd - p - 1 / (r * (r + 1) * (r**2 + 1))
    ) == 0
    assert sp.cancel(
        alpha_db - p + establishment_polynomial / (2 * r * (r**2 + 1))
    ) == 0
    assert sp.factor(sp.diff(establishment_polynomial, r)) == 3 * r**2 - 4 * r + 2
    assert establishment_polynomial.subs(r, sp.Rational(3, 2)) == -sp.Rational(1, 8)
    assert establishment_polynomial.subs(r, sp.Rational(31, 20)) > 0

    threshold_bd = sp.factor(p / (alpha_bd - p))
    threshold_db = sp.factor(p / (alpha_db - p))
    odds_bd_per_z = sp.factor((r - 1) / beta_bd)
    odds_db_times_z = sp.factor(r**2 * p / beta_db)
    lower_z = sp.factor(threshold_bd / odds_bd_per_z)
    upper_z = sp.factor(odds_db_times_z / threshold_db)
    assert lower_z == 1
    assert upper_z == -r * establishment_polynomial
    assert sp.factor(upper_z - lower_z) == -(r - 1) ** 2 * (r**2 + 1)
    print("PASS two-edge module establishment and no-window identities")


def check_rooted_portal():
    # Root 1 is incident to the two weight-3 edges; the base edge has weight 2.
    weights = sp.Matrix(((0, 3, 2), (3, 0, 3), (2, 3, 0)))
    bd = triangle_fixation(weights, "Bd")[1]
    db = triangle_fixation(weights, "dB")[1]
    expected_bd = 5 * r**2 * (12 * r**2 + 20 * r + 9) / (
        60 * r**4 + 172 * r**3 + 233 * r**2 + 172 * r + 60
    )
    expected_db = 3 * r * (2 * r**2 + 8 * r + 3) / (
        (r + 1) * (9 * r**2 + 34 * r + 9)
    )
    assert sp.cancel(bd - expected_bd) == 0
    assert sp.cancel(db - expected_db) == 0
    rv = sp.Rational(31, 20)
    p = (rv - 1) / rv
    assert sp.factor(bd.subs(r, rv) - p) == sp.Rational(40209028, 464555925)
    assert sp.factor(db.subs(r, rv) - p) == sp.Rational(1534279, 17564383)
    print("PASS exact rooted rational portal at r=31/20")


if __name__ == "__main__":
    check_two_edge_module()
    check_rooted_portal()
