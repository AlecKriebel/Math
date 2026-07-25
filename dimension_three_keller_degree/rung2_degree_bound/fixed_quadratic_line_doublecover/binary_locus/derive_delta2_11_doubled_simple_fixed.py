#!/usr/bin/env python3
"""Explore h=(p+q)^2 with one simple fixed-root contribution."""

from __future__ import annotations

import itertools

import sympy as sp
from sympy.polys.matrices import DomainMatrix


p, q, r, z = sp.symbols("p q r z")
A, B, C = sp.symbols("A B C")
s, t, x5, y5 = sp.symbols("s t x5 y5")
X, Y, Z = sp.symbols("X Y Z")
variables = (p, q, r)


def jac(first, second):
    return sp.expand(
        sp.diff(first, p) * sp.diff(second, q)
        - sp.diff(first, q) * sp.diff(second, p)
    )


def coefficients(value, degree):
    polynomial = sp.Poly(sp.expand(value), p, q)
    return [
        polynomial.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand((p + q) * (A * p**2 + B * p * q + C * q**2))
alpha = jac(Q, R)
beta = -jac(P, R)
gamma = jac(P, Q)
print("gcd", sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)))

monomials = (p**2, p * q, q**2, p**2, p * q, q**2, p, q)
columns = tuple(
    alpha * monomials[index]
    if index < 3
    else beta * monomials[index]
    if index < 6
    else gamma * monomials[index]
    for index in range(8)
)
M7 = sp.Matrix(
    [
        [
            sp.Poly(column, p, q).coeff_monomial(
                p ** (7 - row) * q**row
            )
            for column in columns
        ]
        for row in range(8)
    ]
)
rref7, pivots7 = DomainMatrix.from_Matrix(M7).to_field().rref()
print("E7 pivots", pivots7)
rref_matrix = rref7.to_Matrix()
free_columns = tuple(
    index for index in range(8) if index not in pivots7
)
basis = []
for free_column in free_columns:
    vector = [sp.Integer(0) for _index in range(8)]
    vector[free_column] = 1
    for row, pivot in enumerate(pivots7):
        vector[pivot] = -rref_matrix[row, free_column]
    basis.append(vector)

for index, vector in enumerate(basis):
    common_denominator = sp.factor(
        sp.lcm([sp.denom(sp.cancel(value)) for value in vector])
    )
    print("basis", index, "denominator", common_denominator)
    print(
        "basis",
        index,
        [sp.factor(sp.cancel(value * common_denominator)) for value in vector],
    )


def tangent(vector):
    return (
        vector[0] * p**2 + vector[1] * p * q + vector[2] * q**2,
        vector[3] * p**2 + vector[4] * p * q + vector[5] * q**2,
        vector[6] * p + vector[7] * q,
    )


denominator = sp.lcm(
    [
        sp.denom(sp.cancel(value))
        for vector in basis
        for value in vector
    ]
)
N1, N2 = tuple(
    tangent([sp.cancel(denominator * value) for value in vector])
    for vector in basis
)
N = tuple(
    sp.expand(s * N1[index] + t * N2[index]) for index in range(3)
)
H4 = sp.Matrix([P, Q, 0])
H3 = sp.Matrix([r * N[0], r * N[1], R])
H2 = sp.Matrix([x5 * r**2, y5 * r**2, r * N[2]])
weighted = sp.Poly(
    sp.expand(
        (
            z * H2.jacobian(variables)
            + z**2 * H3.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
assert sp.expand(weighted.coeff_monomial(z**7)) == 0
E6r = sp.Poly(
    sp.expand(weighted.coeff_monomial(z**6)), r
).coeff_monomial(r)
lifted = []
for equation in coefficients(E6r, 5):
    polynomial = sp.Poly(equation, s, t)
    lifted.append(
        sp.expand(
            polynomial.coeff_monomial(s**2) * X
            + polynomial.coeff_monomial(s * t) * Y
            + polynomial.coeff_monomial(t**2) * Z
            + polynomial.coeff_monomial(1)
        )
    )
contact = sp.Matrix(
    [
        [
            equation.coeff(variable)
            for variable in (X, Y, Z, x5, y5)
        ]
        for equation in lifted
    ]
)
print("contact generic rank", contact.rank())
maximal_minors = []
for omitted in range(6):
    rows = [row for row in range(6) if row != omitted]
    maximal_minors.append(
        sp.factor(contact.extract(rows, range(5)).det())
    )
    print("contact omit", omitted, maximal_minors[-1])
print("contact maximal gcd", sp.factor(sp.gcd_list(maximal_minors)))

# The generic basis is singular on Delta=0.  This divisor remains on
# the exact open, so compute a fresh E7 basis there.
Delta = 4 * A * C - B**2
A_delta = B**2 / (4 * C)
R_delta = sp.expand(R.subs(A, A_delta))
M7_delta = M7.applyfunc(lambda value: sp.cancel(value.subs(A, A_delta)))
rref_delta, pivots_delta = DomainMatrix.from_Matrix(
    M7_delta
).to_field().rref()
print("Delta=0 E7 pivots", pivots_delta)
rref_delta_matrix = rref_delta.to_Matrix()
free_delta = tuple(
    index for index in range(8) if index not in pivots_delta
)
basis_delta = []
for free_column in free_delta:
    vector = [sp.Integer(0) for _index in range(8)]
    vector[free_column] = 1
    for row, pivot in enumerate(pivots_delta):
        vector[pivot] = -rref_delta_matrix[row, free_column]
    common_denominator = sp.factor(
        sp.lcm([sp.denom(sp.cancel(value)) for value in vector])
    )
    vector = [
        sp.factor(sp.cancel(common_denominator * value))
        for value in vector
    ]
    basis_delta.append(vector)
    print("Delta=0 basis", vector)

N1_delta, N2_delta = tuple(tangent(vector) for vector in basis_delta)
N_delta = tuple(
    sp.expand(s * N1_delta[index] + t * N2_delta[index])
    for index in range(3)
)
H3_delta = sp.Matrix([r * N_delta[0], r * N_delta[1], R_delta])
H2_delta = sp.Matrix([x5 * r**2, y5 * r**2, r * N_delta[2]])
weighted_delta = sp.Poly(
    sp.expand(
        (
            z * H2_delta.jacobian(variables)
            + z**2 * H3_delta.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
assert sp.expand(weighted_delta.coeff_monomial(z**7)) == 0
E6r_delta = sp.Poly(
    sp.expand(weighted_delta.coeff_monomial(z**6)), r
).coeff_monomial(r)
lifted_delta = []
for equation in coefficients(E6r_delta, 5):
    polynomial = sp.Poly(equation, s, t)
    lifted_delta.append(
        sp.expand(
            polynomial.coeff_monomial(s**2) * X
            + polynomial.coeff_monomial(s * t) * Y
            + polynomial.coeff_monomial(t**2) * Z
            + polynomial.coeff_monomial(1)
        )
    )
contact_delta = sp.Matrix(
    [
        [
            equation.coeff(variable)
            for variable in (X, Y, Z, x5, y5)
        ]
        for equation in lifted_delta
    ]
)
print("Delta=0 contact rank", contact_delta.rank())
for omitted in range(6):
    rows = [row for row in range(6) if row != omitted]
    print(
        "Delta=0 contact omit",
        omitted,
        sp.factor(contact_delta.extract(rows, range(5)).det()),
    )
