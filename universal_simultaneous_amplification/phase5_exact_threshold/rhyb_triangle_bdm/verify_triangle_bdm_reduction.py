#!/usr/bin/env python3
"""Exact hostile audit of the weighted-triangle BDM reduction.

This replay proves identities only.  In particular, it does not assert the
six open portal-matrix signs from the companion note.
"""

from __future__ import annotations

from collections import defaultdict
from math import comb

import sympy as sp


r = sp.symbols("r", positive=True)
A, B, C = sp.symbols("A B C", positive=True)
z = sp.symbols("z", nonnegative=True)
WEIGHTS = ((0, A, B), (A, 0, C), (B, C, 0))
DEGREES = tuple(sum(row) for row in WEIGHTS)
SINGLETON_MASKS = (1, 2, 4)
ROOT_LO = sp.Rational(1502856912, 10**9)
ROOT_HI = sp.Rational(1502856913, 10**9)
HYBRID = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1


def labelled_chain(
    rule: str,
    fitness: sp.Expr,
    weights: tuple[tuple[sp.Expr, ...], ...] = WEIGHTS,
) -> tuple[sp.Expr, ...]:
    """Independently solve all six labelled transient subset equations."""

    degrees = tuple(sum(row) for row in weights)
    states = list(range(1, 7))
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.eye(6)
    rhs = sp.zeros(6, 1)

    for state in states:
        mutant = [(state >> vertex) & 1 for vertex in range(3)]
        transition: dict[int, sp.Expr] = defaultdict(lambda: sp.Integer(0))
        if rule == "Bd":
            total_fitness = 3 + (fitness - 1) * sum(mutant)
            for parent in range(3):
                for target in range(3):
                    if parent == target:
                        continue
                    probability = (
                        (fitness if mutant[parent] else 1)
                        * weights[parent][target]
                        / (total_fitness * degrees[parent])
                    )
                    new_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transition[new_state] += probability
        elif rule == "dB":
            for target in range(3):
                denominator = sum(
                    weights[parent][target]
                    * (fitness if mutant[parent] else 1)
                    for parent in range(3)
                )
                for parent in range(3):
                    if parent == target:
                        continue
                    probability = (
                        weights[parent][target]
                        * (fitness if mutant[parent] else 1)
                        / (3 * denominator)
                    )
                    new_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transition[new_state] += probability
        else:
            raise ValueError(rule)

        row = index[state]
        for target, probability in transition.items():
            if target == 7:
                rhs[row] += probability
            elif target:
                matrix[row, index[target]] -= probability

    solution = next(iter(sp.linsolve((matrix, rhs))))
    return tuple(sp.cancel(value) for value in solution)


def schur_recurrence_audit(rule: str) -> None:
    """Check equations (4)--(7) against the independent labelled chain."""

    fitness = 1 / r
    # A fully nonregular rational triangle keeps every orientation and degree
    # factor visible while making the independent symbolic-r solve quick.
    zero, two, three, five = map(sp.Integer, (0, 2, 3, 5))
    weights = ((zero, two, three), (two, zero, five), (three, five, zero))
    degrees = tuple(sum(row) for row in weights)
    values = labelled_chain(rule, fitness, weights)
    singleton = tuple(values[mask - 1] for mask in SINGLETON_MASKS)

    for k in range(3):
        i, j = [vertex for vertex in range(3) if vertex != k]
        doubleton = values[((1 << i) | (1 << j)) - 1]

        if rule == "Bd":
            t_k = weights[i][k] / degrees[i] + weights[j][k] / degrees[j]
            recurrence = (
                fitness * t_k
                + weights[k][i] / degrees[k] * singleton[j]
                + weights[k][j] / degrees[k] * singleton[i]
            ) / (fitness * t_k + 1)
        else:
            h_ki = weights[k][i] / (
                weights[k][i] + fitness * weights[j][i]
            )
            h_kj = weights[k][j] / (
                weights[k][j] + fitness * weights[i][j]
            )
            recurrence = (
                1 + h_ki * singleton[j] + h_kj * singleton[i]
            ) / (1 + h_ki + h_kj)
        assert sp.cancel(doubleton - recurrence) == 0

    for i in range(3):
        others = [vertex for vertex in range(3) if vertex != i]
        if rule == "Bd":
            numerator = 0
            for j in others:
                doubleton = values[((1 << i) | (1 << j)) - 1]
                numerator += weights[i][j] / degrees[i] * doubleton
            denominator = fitness + sum(
                weights[j][i] / degrees[j] for j in others
            )
            recurrence = fitness * numerator / denominator
        else:
            numerator = 0
            denominator = 1
            for j in others:
                k = next(vertex for vertex in range(3) if vertex not in (i, j))
                h_ij = fitness * weights[i][j] / (
                    fitness * weights[i][j] + weights[k][j]
                )
                doubleton = values[((1 << i) | (1 << j)) - 1]
                numerator += h_ij * doubleton
                denominator += h_ij
            recurrence = numerator / denominator
        assert sp.cancel(singleton[i] - recurrence) == 0


def bernstein_coefficients(poly: sp.Expr, variable: sp.Symbol) -> list[sp.Expr]:
    polynomial = sp.Poly(sp.expand(poly), variable)
    degree = polynomial.degree()
    power = [
        polynomial.coeff_monomial(variable**i) for i in range(degree + 1)
    ]
    return [
        sp.factor(
            sum(
                power[i] * sp.Rational(comb(k, i), comb(degree, i))
                for i in range(k + 1)
            )
        )
        for k in range(degree + 1)
    ]


def type_complement_audit() -> None:
    """Check reciprocal singletons against forward complementary pairs."""

    zero, two, three, five = map(sp.Integer, (0, 2, 3, 5))
    weights = ((zero, two, three), (two, zero, five), (three, five, zero))
    for rule in ("Bd", "dB"):
        forward = labelled_chain(rule, r, weights)
        reciprocal = labelled_chain(rule, 1 / r, weights)
        for vertex in range(3):
            singleton = 1 << vertex
            complement = 7 ^ singleton
            assert sp.cancel(
                reciprocal[singleton - 1] + forward[complement - 1] - 1
            ) == 0


def complete_anchor_audit() -> None:
    """Check (8)--(10), the root isolation, and the positive anchor sign."""

    complete_weights = ((0, 1, 1), (1, 0, 1), (1, 1, 0))
    bd_forward = labelled_chain("Bd", r, complete_weights)
    db_forward = labelled_chain("dB", r, complete_weights)
    bd_reverse = labelled_chain("Bd", 1 / r, complete_weights)
    db_reverse = labelled_chain("dB", 1 / r, complete_weights)

    b = sp.factor(
        sum(bd_forward[mask - 1] for mask in SINGLETON_MASKS) / 3
    )
    a = sp.factor(
        sum(db_forward[mask - 1] for mask in SINGLETON_MASKS)
        / (3 * (r - 1))
    )
    u = sp.factor(bd_reverse[0])
    v = sp.factor(db_reverse[0])
    assert sp.factor(a - 2 * r / (3 * (r - 1) * (r + 1))) == 0
    assert sp.factor(b - r**2 / (r**2 + r + 1)) == 0
    assert sp.factor(u - 1 / (r**2 + r + 1)) == 0
    assert sp.factor(v - 2 / (3 * (r + 1))) == 0

    constant = r * (r - 1) ** 2
    product_ab = sp.factor(a * b)
    product_complement = sp.factor((1 - a) * (1 - b))
    atom = sp.factor(u * v)

    # Rationalize atom >= C(U+V-2 sqrt(UV)).  Since the left side after
    # moving the nonsquare terms is positive on the isolating interval, the
    # sign is the sign of this difference of squares.
    anchor = sp.factor(
        (atom + constant * (product_ab + product_complement)) ** 2
        - 4 * constant**2 * product_ab * product_complement
    )
    expected_numerator = (
        r**10
        - 12 * r**8
        + 4 * r**7
        + 42 * r**6
        - 4 * r**5
        - 48 * r**4
        - 12 * r**3
        + 17 * r**2
        + 12 * r
        + 4
    )
    expected_anchor = expected_numerator / (
        9 * (r + 1) ** 2 * (r**2 + r + 1) ** 2
    )
    assert sp.factor(anchor - expected_anchor) == 0

    expected_remainder = (
        1658 * r**5
        - 6161 * r**4
        + 9652 * r**3
        - 7510 * r**2
        + 2224 * r
        - 381
    )
    assert sp.rem(expected_numerator, HYBRID, r) == expected_remainder

    assert sp.Poly(HYBRID, r).count_roots(ROOT_LO, ROOT_HI) == 1
    assert HYBRID.subs(r, ROOT_LO) > 0
    assert HYBRID.subs(r, ROOT_HI) < 0

    mapped = expected_remainder.subs(r, ROOT_LO + (ROOT_HI - ROOT_LO) * z)
    coefficients = bernstein_coefficients(mapped, z)
    assert len(coefficients) == 6
    assert all(coefficient > 0 for coefficient in coefficients)

    # Audit the unsquared orientation at both rational endpoints.
    nonsquare_side = sp.factor(
        atom + constant * (product_ab + product_complement)
    )
    assert nonsquare_side.subs(r, ROOT_LO) > 0
    assert nonsquare_side.subs(r, ROOT_HI) > 0


def main() -> None:
    schur_recurrence_audit("Bd")
    schur_recurrence_audit("dB")
    type_complement_audit()
    complete_anchor_audit()
    print("PASS independent labelled chains satisfy Bd recurrences (4)--(5)")
    print("PASS independent labelled chains satisfy dB recurrences (6)--(7)")
    print("PASS reciprocal singleton/forward complement identity (8)")
    print("PASS complete-triangle formulas and rationalized anchor (8)--(10)")
    print("PASS hybrid sextic has one root in the stated rational interval")
    print("OPEN six stronger BDM portal-matrix entry signs")


if __name__ == "__main__":
    main()
