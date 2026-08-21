#!/usr/bin/env python3
"""Factor exact E7 block determinants for the four h-orbit charts."""

from functools import reduce

import sympy as sp

p, q = sp.symbols("p q")
a, b, c, d, eta = sp.symbols("a b c d eta")
R = a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3


def jac(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q)
                     - sp.diff(f, q) * sp.diff(g, p))


def block_matrix(h, level):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    first, second, third = jac(Q, R), -jac(P, R), jac(P, Q)
    if level == 2:
        multipliers = ((1,), (1,), ())
    elif level == 1:
        multipliers = ((p, q), (p, q), (1,))
    elif level == 0:
        multipliers = ((p**2, p * q, q**2),
                       (p**2, p * q, q**2), (p, q))
    else:
        raise ValueError(level)
    columns = (
        tuple(first * value for value in multipliers[0])
        + tuple(second * value for value in multipliers[1])
        + tuple(third * value for value in multipliers[2])
    )
    degree = 5 + (2 - level)
    return sp.Matrix(
        [
            [
                sp.Poly(sp.expand(column), p, q).coeff_monomial(
                    p**i * q ** (degree - i)
                )
                for column in columns
            ]
            for i in range(degree, -1, -1)
        ]
    )


def primitive_gcd(values):
    nonzero = [sp.factor(value) for value in values if value != 0]
    if not nonzero:
        return sp.Integer(0)
    return sp.factor(reduce(sp.gcd, nonzero))


charts = (
    ("branch_square", p**2),
    ("two_branch", p * q),
    ("one_branch", p * (p + q)),
    ("interior", p**2 + eta * p * q + q**2),
)
for name, h in charts:
    print("CHART", name)
    matrices = {level: block_matrix(h, level) for level in (2, 1, 0)}
    M0 = matrices[0]
    determinant = sp.factor(M0.det())
    print("det0 =", determinant)
    M1 = matrices[1]
    minors1 = [
        sp.factor(M1.extract(rows, range(5)).det())
        for rows in sp.utilities.iterables.combinations(range(7), 5)
    ]
    print("gcd5(M1) =", primitive_gcd(minors1))
    print("nonzero M1 max minors =", sum(value != 0 for value in minors1))
    M2 = matrices[2]
    minors2 = [
        sp.factor(M2.extract(rows, range(2)).det())
        for rows in sp.utilities.iterables.combinations(range(6), 2)
    ]
    print("gcd2(M2) =", primitive_gcd(minors2))
    print("nonzero M2 max minors =", sum(value != 0 for value in minors2))
    print()
