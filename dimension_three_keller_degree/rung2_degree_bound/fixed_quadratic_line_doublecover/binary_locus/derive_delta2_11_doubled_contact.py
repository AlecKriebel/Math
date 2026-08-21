#!/usr/bin/env python3
"""Explore the final doubled-nonbranch plus ramification-contact leaf.

This is an exploratory exact-algebra script.  It reconstructs the E7
Hilbert--Burch matrix, extracts a generic polynomial tangent basis, and
forms the lifted E6 contact matrix.  Every factor in the output must be
split before it can be used in a proof.
"""

from __future__ import annotations

import itertools

import sympy as sp
from sympy.polys.matrices import DomainMatrix


p, q, r, z = sp.symbols("p q r z")
a, b, d = sp.symbols("a b d")
s, t, x5, y5 = sp.symbols("s t x5 y5")
X, Y, Z = sp.symbols("X Y Z")
variables = (p, q, r)


def jac(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, p) * sp.diff(second, q)
        - sp.diff(first, q) * sp.diff(second, p)
    )


def coefficients(value: sp.Expr, degree: int) -> list[sp.Expr]:
    polynomial = sp.Poly(sp.expand(value), p, q)
    return [
        polynomial.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


def polynomial_kernel_basis(matrix: sp.Matrix) -> tuple[list[sp.Expr], ...]:
    rref, pivots = DomainMatrix.from_Matrix(matrix).to_field().rref()
    reduced = rref.to_Matrix()
    free = tuple(index for index in range(matrix.cols) if index not in pivots)
    output: list[list[sp.Expr]] = []
    for free_column in free:
        vector = [sp.Integer(0) for _index in range(matrix.cols)]
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row, free_column]
        denominator = sp.factor(
            sp.lcm([sp.denom(sp.cancel(value)) for value in vector])
        )
        output.append(
            [
                sp.factor(sp.cancel(denominator * value))
                for value in vector
            ]
        )
    return tuple(output)


def tangent(vector: list[sp.Expr]) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    return (
        sp.expand(vector[0] * p**2 + vector[1] * p * q + vector[2] * q**2),
        sp.expand(vector[3] * p**2 + vector[4] * p * q + vector[5] * q**2),
        sp.expand(vector[6] * p + vector[7] * q),
    )


def contact_matrix(
    P_case: sp.Expr,
    Q_case: sp.Expr,
    R_case: sp.Expr,
    first: tuple[sp.Expr, sp.Expr, sp.Expr],
    second: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> sp.Matrix:
    moving = tuple(
        sp.expand(s * first[index] + t * second[index])
        for index in range(3)
    )
    H4 = sp.Matrix([P_case, Q_case, 0])
    H3 = sp.Matrix([r * moving[0], r * moving[1], R_case])
    H2 = sp.Matrix([x5 * r**2, y5 * r**2, r * moving[2]])
    determinant = sp.Poly(
        sp.expand(
            (
                z * H2.jacobian(variables)
                + z**2 * H3.jacobian(variables)
                + z**3 * H4.jacobian(variables)
            ).det()
        ),
        z,
    )
    assert sp.expand(determinant.coeff_monomial(z**7)) == 0
    e6r = sp.Poly(
        sp.expand(determinant.coeff_monomial(z**6)), r
    ).coeff_monomial(r)
    lifted: list[sp.Expr] = []
    for equation in coefficients(e6r, 5):
        polynomial = sp.Poly(equation, s, t)
        lifted.append(
            sp.expand(
                polynomial.coeff_monomial(s**2) * X
                + polynomial.coeff_monomial(s * t) * Y
                + polynomial.coeff_monomial(t**2) * Z
                + polynomial.coeff_monomial(1)
            )
        )
    return sp.Matrix(
        [
            [
                equation.coeff(variable)
                for variable in (X, Y, Z, x5, y5)
            ]
            for equation in lifted
        ]
    )


h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(
    a * p**3
    + b * p**2 * q
    + sp.Rational(3, 2) * d * p * q**2
    + d * q**3
)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
print("gcd", sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)))

e7_monomials = (p**2, p * q, q**2, p**2, p * q, q**2, p, q)
e7_columns = tuple(
    alpha * e7_monomials[index]
    if index < 3
    else beta * e7_monomials[index]
    if index < 6
    else gamma * e7_monomials[index]
    for index in range(8)
)
e7_matrix = sp.Matrix.hstack(
    *(sp.Matrix(coefficients(column, 7)) for column in e7_columns)
)
basis = polynomial_kernel_basis(e7_matrix)
print("generic kernel dimension", len(basis))
for index, vector in enumerate(basis):
    print("basis", index, tuple(vector))

first, second = (tangent(vector) for vector in basis)
contact = contact_matrix(P, Q, R, first, second)
minors = []
for rows in itertools.combinations(range(6), 5):
    value = sp.factor(contact.extract(rows, range(5)).det(method="domain-ge"))
    minors.append(value)
    print("contact rows", rows, value)
print("contact maximal gcd", sp.factor(sp.gcd_list(minors)))

