#!/usr/bin/env python3
"""Explore the sole endpoint branch surviving E5: RO-smooth/H, A=0,T!=0."""

from __future__ import annotations

import sympy as sp

x, y, z, weight = sp.symbols("x y z weight")
B, T = sp.symbols("B T", nonzero=True)
xyz = (x, y, z)
mon2 = tuple(
    x**i * y**j * z ** (2 - i - j)
    for i in range(2, -1, -1)
    for j in range(2 - i, -1, -1)
)


def exponents(degree):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def coefficients(value, degree):
    polynomial = sp.Poly(sp.expand(value), *xyz)
    return [
        polynomial.coeff_monomial(x**i * y**j * z**ell)
        for i, j, ell in exponents(degree)
    ]


def left_values(matrix, rhs):
    output = []
    for vector in matrix.T.nullspace():
        denominators = [
            sp.together(entry).as_numer_denom()[1]
            for entry in vector
            if entry != 0
        ]
        denominator = sp.factor(sp.lcm(denominators)) if denominators else 1
        vector = vector.applyfunc(lambda entry: sp.cancel(denominator * entry))
        value = sp.factor((vector.T * rhs)[0])
        if value != 0:
            output.append(value)
    return output


h = y**2 + x * z
P, Q, R = h**2, h * x**2, x * h
U = 2 * T * z * h
V = B * x**3 + T * x**2 * z
W = T * x * z

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
            + weight * H2.jacobian(xyz)
            + weight**2 * sp.Matrix([U, V, R]).jacobian(xyz)
            + weight**3 * sp.Matrix([P, Q, 0]).jacobian(xyz)
        ).det()
    ),
    weight,
)

unknowns = a + b + ell
substitutions = {}
for degree in (6, 5):
    identity = sp.expand(weighted.coeff_monomial(weight**degree).subs(substitutions))
    remaining = tuple(variable for variable in unknowns if variable in identity.free_symbols)
    matrix, rhs = sp.linear_eq_to_matrix(coefficients(identity, degree), remaining)
    print(f"E{degree} remaining/shape/rank:", remaining, matrix.shape, matrix.rank())
    print(f"E{degree} compat:", left_values(matrix, rhs))
    solution = next(iter(sp.linsolve((matrix, rhs), remaining)))
    substitutions.update(dict(zip(remaining, solution)))
    print(f"E{degree} changed:")
    for variable, value in zip(remaining, solution):
        if sp.expand(variable - value) != 0:
            print(" ", variable, "=", sp.factor(value))

print("detL through E5:", sp.factor(L.det().subs(substitutions)))
E4 = sp.factor(sp.expand(weighted.coeff_monomial(weight**4).subs(substitutions)))
print("E4 nonzero coefficients:")
for exponent, value in zip(exponents(4), coefficients(E4, 4)):
    if value != 0:
        print(" ", exponent, sp.factor(value))

remaining4 = tuple(variable for variable in unknowns if variable in E4.free_symbols)
print("E4 remaining:", remaining4)
try:
    matrix4, rhs4 = sp.linear_eq_to_matrix(coefficients(E4, 4), remaining4)
except sp.NonlinearError as error:
    print("E4 nonlinear:", error)
else:
    print("E4 shape/rank:", matrix4.shape, matrix4.rank())
    print("E4 compat:", left_values(matrix4, rhs4))
    solution4 = next(iter(sp.linsolve((matrix4, rhs4), remaining4)))
    substitutions4 = dict(zip(remaining4, solution4))
    print("detL through E4:", sp.factor(L.det().subs(substitutions).subs(substitutions4)))
