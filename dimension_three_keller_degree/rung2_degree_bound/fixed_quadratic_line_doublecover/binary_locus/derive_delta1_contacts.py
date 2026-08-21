#!/usr/bin/env python3
"""Exact contact minors for explicit k=1 Hilbert--Burch columns."""

from functools import reduce

import sympy as sp

p, q, r = sp.symbols("p q r")
a, b, c, d, eta = sp.symbols("a b c d eta")


def jac(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q)
                     - sp.diff(f, q) * sp.diff(g, p))


def jac3(f, g, h):
    return sp.expand(
        sp.Matrix(
            [
                [sp.diff(value, variable) for variable in (p, q, r)]
                for value in (f, g, h)
            ]
        ).det()
    )


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return sp.Matrix(
        [
            poly.coeff_monomial(p**i * q ** (degree - i))
            for i in range(degree, -1, -1)
        ]
    )


def audit(label, h, R, N):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    first, second, third = jac(Q, R), -jac(P, R), jac(P, Q)
    u, v, t = map(sp.expand, N)
    assert sp.expand(first * u + second * v + third * t) == 0
    curvature = sp.expand(
        jac3(P, r * v, r * t)
        + jac3(r * u, Q, r * t)
        + jac3(r * u, r * v, R)
    )
    assert sp.Poly(curvature, r).degree() <= 1
    assert sp.Poly(curvature, r).coeff_monomial(1) == 0
    K = sp.factor(sp.Poly(curvature, r).coeff_monomial(r))
    matrix = sp.Matrix.hstack(
        coefficients(first, 5), coefficients(second, 5), coefficients(K, 5)
    )
    minors = [
        sp.factor(matrix.extract(rows, range(3)).det())
        for rows in sp.utilities.iterables.combinations(range(6), 3)
    ]
    nonzero = [value for value in minors if value != 0]
    print("\nCASE", label)
    print("N =", tuple(sp.factor(value) for value in N))
    print("K =", K)
    print("minor gcd =", sp.factor(reduce(sp.gcd, nonzero)))
    for index, value in enumerate(minors):
        if value != 0:
            print(index, value)


audit(
    "pq_a0",
    p * q,
    b * p**2 * q + c * p * q**2 + d * q**3,
    (3 * p**2, q**2, 2 * b * p + c * q),
)

audit(
    "one_d0",
    p * (p + q),
    a * p**3 + b * p**2 * q + c * p * q**2,
    (p**2, q * (2 * p + 3 * q), b * p + 2 * c * q),
)

audit(
    "one_split",
    p * (p + q),
    a * p**3 + sp.Rational(3, 4) * a * p**2 * q
    + c * p * q**2 + d * q**3,
    (
        6 * p**2,
        -16 * p**2 - 20 * p * q + 2 * q**2,
        (3 * a - 16 * c) * p + 2 * (c - 12 * d) * q,
    ),
)

audit(
    "one_fixed_root",
    p * (p + q),
    a * p**3 + b * p**2 * q + (-a + b + d) * p * q**2 + d * q**3,
    (
        -3 * p**2,
        2 * p * q - q**2,
        (-3 * a + b) * p + (a - b + 2 * d) * q,
    ),
)

audit(
    "branch_square",
    p**2,
    a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3,
    (
        12 * d * p**2,
        -2 * c * p * q + 6 * d * q**2,
        (9 * d * a - c * b) * p + 2 * (3 * d * b - c**2) * q,
    ),
)

audit(
    "interior_left",
    p**2 + eta * p * q + q**2,
    a * p**3 + sp.Rational(3, 4) * a * eta * p**2 * q
    + c * p * q**2 + d * q**3,
    (
        2 * (3 * eta**2 - 8) * p**2 + 4 * eta * p * q,
        -16 * p**2 - 20 * eta * p * q
        + 2 * (eta**2 - 16) * q**2,
        (3 * eta**2 * a - 16 * c) * p
        + 2 * (eta * c - 12 * d) * q,
    ),
)

audit(
    "interior_square_eta2",
    (p + q) ** 2,
    a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3,
    (
        (6 * a - 8 * b + 10 * c - 12 * d) * p**2
        + (-2 * b + 4 * c - 6 * d) * p * q,
        (6 * a - 4 * b + 2 * c) * p * q
        + (12 * a - 10 * b + 8 * c - 6 * d) * q**2,
        ((6 * c - 9 * d) * a - 2 * b**2 + b * c) * p
        + (9 * d * a - (c + 6 * d) * b + 2 * c**2) * q,
    ),
)
