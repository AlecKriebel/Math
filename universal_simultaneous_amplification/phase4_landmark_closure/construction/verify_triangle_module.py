#!/usr/bin/env python3
"""Exact symbolic certificate for the weak triangle satellite module.

Vertices 0 and 2 have an edge of weight one; the two edges incident to
vertex 1 have weight delta.  The script builds both six-state absorbing
chains directly, solves them over Q(r,delta), and checks all module quantities
used by the separated center/module calculation.
"""

from __future__ import annotations

import sympy as sp


r, delta = sp.symbols("r delta", positive=True)
weights = sp.Matrix(((0, delta, 1), (delta, 0, delta), (1, delta, 0)))


def fixation_vector(rule: str):
    size = 3
    full = (1 << size) - 1
    states = list(range(1, full))
    index = {mask: position for position, mask in enumerate(states)}
    degrees = [sum(weights[i, j] for j in range(size)) for i in range(size)]
    matrix = sp.zeros(len(states))
    rhs = sp.zeros(len(states), 1)
    for mask, row in index.items():
        mutant = [bool((mask >> vertex) & 1) for vertex in range(size)]
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
                        / (total_fitness * degrees[parent])
                    )
                    target_mask = (
                        mask | (1 << target)
                        if mutant[parent]
                        else mask & ~(1 << target)
                    )
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
                    target_mask = (
                        mask | (1 << target)
                        if mutant[parent]
                        else mask & ~(1 << target)
                    )
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
    return tuple(sp.factor(values[index[1 << vertex]]) for vertex in range(size))


def check():
    forward_bd = fixation_vector("Bd")
    forward_db = fixation_vector("dB")
    reverse_bd = tuple(sp.factor(value.subs(r, 1 / r)) for value in forward_bd)
    reverse_db = tuple(sp.factor(value.subs(r, 1 / r)) for value in forward_db)

    alpha_bd = sp.factor(sum(forward_bd) / 3)
    alpha_db = sp.factor(sum(forward_db) / 3)
    y_bd = sp.factor(sum(reverse_bd))
    degrees = (1 + delta, 2 * delta, 1 + delta)
    i_db = sp.factor(sum(reverse_db[v] / degrees[v] for v in range(3)))
    j_db = sp.factor(sum(forward_db[v] / degrees[v] for v in range(3)))
    x_bd = sp.factor(sum(1 / degree for degree in degrees))

    common_bd = (
        4 * delta**3 * r**4
        + 12 * delta**3 * r**3
        + 13 * delta**3 * r**2
        + 12 * delta**3 * r
        + 4 * delta**3
        + 16 * delta**2 * r**4
        + 52 * delta**2 * r**3
        + 83 * delta**2 * r**2
        + 52 * delta**2 * r
        + 16 * delta**2
        + 12 * delta * r**4
        + 24 * delta * r**3
        + 15 * delta * r**2
        + 24 * delta * r
        + 12 * delta
        + 9 * r**2
    )
    expected_alpha_bd = r**2 * (
        4 * delta**3 * r**2
        + 8 * delta**3 * r
        + 3 * delta**3
        + 16 * delta**2 * r**2
        + 36 * delta**2 * r
        + 21 * delta**2
        + 12 * delta * r**2
        + 12 * delta * r
        + 5 * delta
        + 3
    ) / common_bd
    expected_y_bd = 3 * (
        3 * delta**3 * r**2
        + 8 * delta**3 * r
        + 4 * delta**3
        + 21 * delta**2 * r**2
        + 36 * delta**2 * r
        + 16 * delta**2
        + 5 * delta * r**2
        + 12 * delta * r
        + 12 * delta
        + 3 * r**2
    ) / common_bd

    common_db = (r + 1) * (
        6 * delta**2 * r
        + 3 * delta * r**2
        + delta * r
        + 3 * delta
        + 2 * r
    )
    expected_alpha_db = 2 * r * (
        5 * delta**2 * r
        + delta**2
        + 3 * delta * r**2
        + 3 * delta * r
        + delta
        + r
        + 1
    ) / (3 * common_db)
    expected_i_db = (
        delta**2 * r**2
        + 8 * delta**2 * r
        + 3 * delta * r**2
        + 7 * delta * r
        + 5 * delta
        + 2 * r**2
        + 3 * r
        + 1
    ) / ((delta + 1) * common_db)

    identities = {
        "alpha_Bd": alpha_bd - expected_alpha_bd,
        "Y_Bd": y_bd - expected_y_bd,
        "alpha_dB": alpha_db - expected_alpha_db,
        "I_dB": i_db - expected_i_db,
        "X_Bd": x_bd - (2 / (1 + delta) + 1 / (2 * delta)),
    }
    for label, expression in identities.items():
        if sp.cancel(expression) != 0:
            raise AssertionError((label, sp.factor(expression)))
        print(f"PASS exact {label}")

    limits = {
        "alpha_Bd->1/3": sp.limit(alpha_bd, delta, 0) - sp.Rational(1, 3),
        "alpha_dB->1/3": sp.limit(alpha_db, delta, 0) - sp.Rational(1, 3),
        "Y_Bd->1": sp.limit(y_bd, delta, 0) - 1,
        "2delta X_Bd->1": sp.limit(2 * delta * x_bd, delta, 0) - 1,
        "I_dB->(2r+1)/(2r)": sp.limit(i_db, delta, 0) - (2 * r + 1) / (2 * r),
        "J_dB->(r+2)/2": sp.limit(j_db, delta, 0) - (r + 2) / 2,
    }
    for label, expression in limits.items():
        if sp.cancel(expression) != 0:
            raise AssertionError((label, sp.factor(expression)))
        print(f"PASS limit {label}")

    q = (r - 1) / r
    threshold_odds = sp.factor(q / (sp.Rational(1, 3) - q))
    if sp.cancel(threshold_odds - 3 * (r - 1) / (3 - 2 * r)) != 0:
        raise AssertionError("odds threshold")
    bd_lower = sp.factor(
        threshold_odds
        * sp.limit(y_bd, delta, 0)
        / ((r - 1) * sp.limit(delta * x_bd, delta, 0))
    )
    db_upper = sp.factor(
        3 * r * (r - 1)
        / (sp.limit(i_db, delta, 0) * threshold_odds)
    )
    if sp.cancel(bd_lower - 6 / (3 - 2 * r)) != 0:
        raise AssertionError("Bd threshold")
    if sp.cancel(db_upper - 2 * r**2 * (3 - 2 * r) / (2 * r + 1)) != 0:
        raise AssertionError("dB threshold")
    print("PASS macro thresholds")

    c = sp.symbols("c", integer=True, positive=True)
    q = (r - 1) / r
    center_bd = q / (1 - r ** (-c))
    reverse_bd = (r - 1) / (r**c - 1)
    if sp.cancel(reverse_bd / center_bd - r ** (1 - c)) != 0:
        raise AssertionError("Bd center reverse ratio")
    center_db = (c - 1) / c * q / (1 - r ** (-(c - 1)))
    reverse_db_center = (c - 1) / c * (r - 1) / (r ** (c - 1) - 1)
    if sp.cancel(reverse_db_center / center_db - r ** (2 - c)) != 0:
        raise AssertionError("dB center reverse ratio")
    print("PASS center reverse ratios")

    # Endpoint r=3/2.  Put t=1/N, delta=t^4 and
    # Z=(N-1)N^-3=t^2-t^3.  Exponentially small center terms are o(t^k)
    # for every fixed k and therefore do not enter these algebraic limits.
    t = sp.symbols("t", positive=True)
    rv = sp.Rational(3, 2)
    qv = sp.Rational(1, 3)
    substitutions = {r: rv, delta: t**4}
    z_total = t**2 - t**3
    odds_bd = sp.factor(
        z_total * (rv - 1) * x_bd.subs(substitutions) / y_bd.subs(substitutions)
    )
    odds_db = sp.factor(
        3 * rv * (rv - 1) / (z_total * i_db.subs(substitutions))
    )
    if sp.limit(t**2 * odds_bd, t, 0) != sp.Rational(1, 4):
        raise AssertionError("Bd endpoint odds")
    if sp.limit(t**2 * odds_db, t, 0) != sp.Rational(27, 16):
        raise AssertionError("dB endpoint odds")
    p_bd = sp.factor(alpha_bd.subs(substitutions) * odds_bd / (1 + odds_bd))
    p_db = sp.factor(alpha_db.subs(substitutions) * odds_db / (1 + odds_db))
    h = t / (3 + t)
    rho_bd = (1 - h) * p_bd + h * qv
    rho_db = (1 - h) * p_db + h * qv * (1 - t)
    baseline_bd = qv
    baseline_db = qv * (1 - t**2 / (3 + t))
    if sp.limit((rho_bd - baseline_bd) / t**2, t, 0) != -sp.Rational(4, 3):
        raise AssertionError("Bd endpoint comparison")
    if sp.limit((rho_db - baseline_db) / t**2, t, 0) != -sp.Rational(16, 81):
        raise AssertionError("dB endpoint comparison")
    print("PASS endpoint comparison coefficients")


if __name__ == "__main__":
    check()
