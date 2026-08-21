#!/usr/bin/env python3
"""Root exploration of the last doubled-nonbranch {1,1} contact leaf.

The polynomial tangent basis below is valid on the chart D0 != 0.
This script deliberately exposes every maximal contact minor after
projectivizing first to d=1 and then to the boundary d=0.
"""

from __future__ import annotations

import itertools

import sympy as sp


p, q, r, z = sp.symbols("p q r z")
a, b, d = sp.symbols("a b d")
s, t = sp.symbols("s t")
X, Y, Z, x5, y5 = sp.symbols("X Y Z x5 y5")
w = sp.symbols("w")

h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = a * p**3 + b * p**2 * q + sp.Rational(3, 2) * d * p * q**2 + d * q**3

D0 = (
    108 * a**2 * d
    - 108 * a * b * d
    + 54 * a * d**2
    + 16 * b**3
    - 9 * b**2 * d
)

N1 = (
    -2 * (24 * a * b - 72 * a * d - 32 * b**2 + 81 * b * d - 36 * d**2) * p**2
    + 2 * (90 * a * d + 8 * b**2 - 81 * b * d + 45 * d**2) * p * q
    + 12 * d * (6 * a - 5 * b + 3 * d) * q**2,
    -2 * b * (24 * a - 16 * b + 9 * d) * p * q
    - 2 * (8 * b - 3 * d) * (6 * a - 5 * b + 3 * d) * q**2,
    D0 * p,
)
N2 = (
    4 * (3 * a - 2 * b) * (6 * a - 5 * b + 3 * d) * p**2
    - 2 * b * (12 * a - 22 * b + 15 * d) * p * q
    + 4 * b * (4 * b - 3 * d) * q**2,
    12 * a * (6 * a - 5 * b + 3 * d) * p * q
    + 6 * (24 * a**2 - 24 * a * b + 12 * a * d + 2 * b**2 - b * d) * q**2,
    D0 * q,
)


def coefficient(value: sp.Expr, degree: int, index: int) -> sp.Expr:
    return sp.Poly(sp.expand(value), p, q).coeff_monomial(
        p ** (degree - index) * q**index
    )


def build_contact() -> sp.Matrix:
    tangent = tuple(
        sp.expand(s * N1[index] + t * N2[index]) for index in range(3)
    )
    H4 = sp.Matrix([P, Q, 0])
    H3 = sp.Matrix([r * tangent[0], r * tangent[1], R])
    H2 = sp.Matrix([x5 * r**2, y5 * r**2, r * tangent[2]])
    weighted = sp.Poly(
        sp.expand(
            (
                z * H2.jacobian((p, q, r))
                + z**2 * H3.jacobian((p, q, r))
                + z**3 * H4.jacobian((p, q, r))
            ).det()
        ),
        z,
    )
    assert sp.expand(weighted.coeff_monomial(z**7)) == 0
    e6r = sp.Poly(sp.expand(weighted.coeff_monomial(z**6)), r).coeff_monomial(r)
    rows = []
    for index in range(6):
        equation = coefficient(e6r, 5, index)
        polynomial = sp.Poly(equation, s, t)
        lifted = sp.expand(
            polynomial.coeff_monomial(s**2) * X
            + polynomial.coeff_monomial(s * t) * Y
            + polynomial.coeff_monomial(t**2) * Z
            + polynomial.coeff_monomial(1)
        )
        rows.append([lifted.coeff(variable) for variable in (X, Y, Z, x5, y5)])
    return sp.Matrix(rows)


contact = build_contact()
print("PASS contact matrix reconstructed")

for chart_name, substitutions in (("d=1", {d: 1}), ("d=0", {d: 0})):
    chart = contact.subs(substitutions)
    print("CHART", chart_name)
    minors = []
    for omitted in range(6):
        rows = tuple(index for index in range(6) if index != omitted)
        determinant = sp.factor(
            chart.extract(rows, range(5)).det(method="domain-ge")
        )
        minors.append(determinant)
        print("omit", omitted, determinant)
    common = sp.factor(sp.gcd_list(minors))
    print("gcd", common)
    residuals = [sp.factor(sp.cancel(value / common)) for value in minors]
    if chart_name == "d=1":
        basis = sp.groebner(residuals, a, b, order="grevlex")
        print("residual Groebner basis", tuple(sp.factor(value) for value in basis.polys))
        open_product = (
            (3 * a - 2 * b)
            * (2 * a - 2 * b + 1)
            * (6 * a - 5 * b + 3)
            * D0.subs(d, 1)
        )
        saturation = sp.groebner(
            (*residuals, w * open_product - 1),
            w,
            a,
            b,
            order="grevlex",
        )
        print(
            "residual exact-open saturation is unit",
            saturation.contains(sp.Integer(1)),
        )
    else:
        univariate = [
            sp.factor(value.subs(b, 1)) for value in residuals
        ]
        print("b=1 residual gcd", sp.factor(sp.gcd_list(univariate)))
