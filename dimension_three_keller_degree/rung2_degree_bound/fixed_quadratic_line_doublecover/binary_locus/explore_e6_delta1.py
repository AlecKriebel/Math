#!/usr/bin/env python3
"""Symbolic E6 contact obstruction on selected delta=1 components."""

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


def coefficient_vector(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return sp.Matrix(
        [
            poly.coeff_monomial(p**i * q ** (degree - i))
            for i in range(degree, -1, -1)
        ]
    )


def m0_and_triple(h, R):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    first, second, third = jac(Q, R), -jac(P, R), jac(P, Q)
    columns = (
        [first * p**2, first * p * q, first * q**2]
        + [second * p**2, second * p * q, second * q**2]
        + [third * p, third * q]
    )
    matrix = sp.Matrix.hstack(
        *(coefficient_vector(column, 7) for column in columns)
    )
    return P, Q, first, second, third, matrix


def cleared(vector):
    denominator = sp.lcm(
        [sp.together(entry).as_numer_denom()[1] for entry in vector]
    )
    output = sp.Matrix([sp.factor(denominator * entry) for entry in vector])
    common = reduce(sp.gcd, [entry for entry in output if entry != 0])
    return sp.Matrix([sp.factor(entry / common) for entry in output])


def forms(vector):
    return (
        sp.expand(vector[0] * p**2 + vector[1] * p * q + vector[2] * q**2),
        sp.expand(vector[3] * p**2 + vector[4] * p * q + vector[5] * q**2),
        sp.expand(vector[6] * p + vector[7] * q),
    )


def contact_obstruction(label, h, R):
    P, Q, first, second, third, matrix = m0_and_triple(h, R)
    kernel = matrix.nullspace()
    print("\nCASE", label, "rank", matrix.rank(), "nullity", len(kernel))
    if len(kernel) != 1:
        return
    vector = cleared(kernel[0])
    u, v, t = forms(vector)
    print("N =", tuple(sp.factor(value) for value in (u, v, t)))
    U, V, T = r * u, r * v, r * t
    curvature = sp.expand(
        jac3(P, V, T) + jac3(U, Q, T) + jac3(U, V, R)
    )
    K = sp.factor(sp.Poly(curvature, r).coeff_monomial(r))
    constant = sp.factor(sp.Poly(curvature, r).coeff_monomial(1))
    print("K =", K)
    print("constant curvature =", constant)
    columns = sp.Matrix.hstack(
        coefficient_vector(first, 5),
        coefficient_vector(second, 5),
        coefficient_vector(K, 5),
    )
    minors = [
        sp.factor(columns.extract(rows, range(3)).det())
        for rows in sp.utilities.iterables.combinations(range(6), 3)
    ]
    nonzero = [value for value in minors if value != 0]
    obstruction = sp.factor(reduce(sp.gcd, nonzero)) if nonzero else 0
    print("contact minor gcd =", obstruction)
    print("nonzero minors =", len(nonzero))
    print("sample minors =", nonzero[:8])


contact_obstruction(
    "h=pq, a=0",
    p * q,
    b * p**2 * q + c * p * q**2 + d * q**3,
)
contact_obstruction(
    "h=p(p+q), d=0",
    p * (p + q),
    a * p**3 + b * p**2 * q + c * p * q**2,
)
contact_obstruction(
    "h=p(p+q), 3a=4b",
    p * (p + q),
    a * p**3 + sp.Rational(3, 4) * a * p**2 * q
    + c * p * q**2 + d * q**3,
)
contact_obstruction(
    "h=p^2 generic",
    p**2,
    a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3,
)
