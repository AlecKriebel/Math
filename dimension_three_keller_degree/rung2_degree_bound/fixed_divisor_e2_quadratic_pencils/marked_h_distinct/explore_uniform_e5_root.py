#!/usr/bin/env python3
"""Exploratory exact E5 calculation for the finite CTAU chart.

This is deliberately not a verifier.  It keeps the cross-ratio parameter
symbolic, solves E6 without choosing parameter-dependent pivots by hand, and
prints the first E5 compatibility data for later certification.
"""

from __future__ import annotations

import sympy as sp

x, y, z, scale, k = sp.symbols("x y z scale k")
A, B, T = sp.symbols("A B T")
variables = (x, y, z)


def exponents(degree):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), *variables)
    return [
        poly.coeff_monomial(x**i * y**j * z**ell)
        for i, j, ell in exponents(degree)
    ]


def left_compatibilities(matrix, rhs):
    pairs = []
    for vector in matrix.T.nullspace():
        value = sp.factor((vector.T * rhs)[0])
        if value != 0:
            pairs.append((vector, value))
    return pairs


mon2 = tuple(
    x**i * y**j * z ** (2 - i - j)
    for i in range(2, -1, -1)
    for j in range(2 - i, -1, -1)
)

h = x**2 + y * z
s = x**2
P, Q = h**2, h * s
R = x * (h + k * s)
U, V, W = A * x**3, B * x**3, T * x**2

a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("l0:9")
H2 = sp.Matrix(
    [
        sum(c * monomial for c, monomial in zip(a, mon2)),
        sum(c * monomial for c, monomial in zip(b, mon2)),
        W,
    ]
)
L = sp.Matrix(3, 3, ell)
weighted = sp.Poly(
    sp.expand(
        (
            L
            + scale * H2.jacobian(variables)
            + scale**2 * sp.Matrix([U, V, R]).jacobian(variables)
            + scale**3 * sp.Matrix([P, Q, 0]).jacobian(variables)
        ).det()
    ),
    scale,
)

unknowns = a + b + ell
E6 = sp.expand(weighted.coeff_monomial(scale**6))
print("E6 nonzero coefficient rows:")
for exponent, value in zip(exponents(6), coefficients(E6, 6)):
    if value != 0:
        print(" ", exponent, sp.factor(value))
matrix6, rhs6 = sp.linear_eq_to_matrix(coefficients(E6, 6), unknowns)
print("E6 shape/rank:", matrix6.shape, matrix6.rank())
solution6 = next(iter(sp.linsolve((matrix6, rhs6), unknowns)))
substitutions6 = dict(zip(unknowns, solution6))
print("E6 changed:")
for variable, value in zip(unknowns, solution6):
    if sp.expand(variable - value) != 0:
        print(" ", variable, "=", sp.factor(value))

E5 = sp.expand(weighted.coeff_monomial(scale**5).subs(substitutions6))
print("E5 nonzero coefficient rows:")
for exponent, value in zip(exponents(5), coefficients(E5, 5)):
    if value != 0:
        print(" ", exponent, sp.factor(value))
remaining = tuple(variable for variable in unknowns if variable in E5.free_symbols)
print("E5 remaining:", remaining)
try:
    matrix5, rhs5 = sp.linear_eq_to_matrix(coefficients(E5, 5), remaining)
except sp.NonlinearError as exc:
    print("E5 nonlinear:", exc)
    print("nonzero coefficients:")
    for exponent, value in zip(exponents(5), coefficients(E5, 5)):
        if value != 0:
            print(" ", exponent, sp.factor(value))
    raise

print("E5 shape/rank:", matrix5.shape, matrix5.rank())
pivot_rows = matrix5.T.rref()[1]
pivot_columns = matrix5.rref()[1]
print("E5 pivot rows:", pivot_rows)
print("E5 pivot columns:", pivot_columns)
if pivot_rows and pivot_columns:
    print(
        "E5 pivot determinant:",
        sp.factor(matrix5.extract(pivot_rows, pivot_columns).det()),
    )
minor_gcd = sp.Integer(0)
minor_certificates = []
for rows in __import__("itertools").combinations(range(matrix5.rows), 4):
    determinant = sp.factor(matrix5.extract(rows, range(4)).det())
    if determinant == 0:
        continue
    new_gcd = sp.factor(sp.gcd(minor_gcd, determinant))
    if new_gcd != minor_gcd:
        minor_certificates.append((rows, determinant, new_gcd))
        minor_gcd = new_gcd
        if minor_gcd in (1, -1):
            break
print("E5 rank-cover minors:")
for certificate in minor_certificates:
    print(" ", certificate)
print("E5 maximal-minor gcd:", minor_gcd)
print("E5 compatibilities:")
for vector, value in left_compatibilities(matrix5, rhs5):
    denominators = [
        sp.factor(sp.together(entry).as_numer_denom()[1])
        for entry in vector
        if entry != 0
    ]
    print(
        " ",
        value,
        "den=",
        sp.factor(sp.lcm(denominators)) if denominators else 1,
    )
solution5 = next(iter(sp.linsolve((matrix5, rhs5), remaining)))
substitutions5 = dict(zip(remaining, solution5))
print("E5 changed:")
for variable, value in zip(remaining, solution5):
    if sp.expand(variable - value) != 0:
        print(" ", variable, "=", sp.factor(value))
print(
    "det(L) through E5:",
    sp.factor(L.det().subs(substitutions6).subs(substitutions5)),
)

for special in (sp.Integer(0), sp.Integer(-1), sp.Rational(1, 3)):
    specialized5 = sp.expand(E5.subs(k, special))
    specialized_remaining = tuple(
        variable for variable in unknowns if variable in specialized5.free_symbols
    )
    specialized_matrix, specialized_rhs = sp.linear_eq_to_matrix(
        coefficients(specialized5, 5), specialized_remaining
    )
    print(
        f"k={special}: E5 remaining/shape/rank",
        specialized_remaining,
        specialized_matrix.shape,
        specialized_matrix.rank(),
    )
    print(
        f"k={special}: compatibilities",
        [
            sp.factor(value)
            for _, value in left_compatibilities(
                specialized_matrix, specialized_rhs
            )
        ],
    )
