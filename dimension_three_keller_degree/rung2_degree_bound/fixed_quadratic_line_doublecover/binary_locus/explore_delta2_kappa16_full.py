#!/usr/bin/env python3
"""Exploratory full-lower solve on the kappa=16, delta=2 {2,0} row."""

from __future__ import annotations

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
a, d, k, m, n = sp.symbols("a d k m n")
variables = (p, q, r)

u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
t = sp.symbols("t0:3")
x = sp.symbols("x0:6")
y = sp.symbols("y0:6")
ell = sp.symbols("l0:9")


def binary(coefficients, degree):
    return sum(
        coefficients[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )


def equations(value):
    return [
        coefficient
        for coefficient in sp.Poly(sp.expand(value), p, q, r).coeffs()
        if coefficient != 0
    ]


h = p**2 + 4 * p * q + q**2
R = a * p**3 + 3 * a * p**2 * q + 3 * d * p * q**2 + d * q**3
Nu = 5 * p + q
Nv = -p - 5 * q
Nt = 3 * (a - d)
W = m * p + n * q
S = sp.Rational(1, 2) * k * r**2 + W * r

H4 = sp.Matrix([h * p**2, h * q**2, 0])
H3 = sp.Matrix([binary(u, 3) + Nu * S, binary(v, 3) + Nv * S, R])
H2 = sp.Matrix(
    [
        binary(x[:3], 2) + r * (x[3] * p + x[4] * q) + x[5] * r**2,
        binary(y[:3], 2) + r * (y[3] * p + y[4] * q) + y[5] * r**2,
        binary(t, 2) + Nt * S,
    ]
)
L0 = sp.Matrix(3, 3, ell)

weighted = sp.Poly(
    sp.expand(
        (
            L0
            + z * H2.jacobian(variables)
            + z**2 * H3.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
E = {
    degree: sp.expand(weighted.coeff_monomial(z**degree))
    for degree in range(9)
}

assert sp.expand(E[8]) == 0
assert sp.expand(E[7]) == 0
print("PASS E8/E7 identically")

for degree in (6, 5, 4):
    poly_r = sp.Poly(E[degree], r)
    print("E", degree, "r-degree", poly_r.degree())
    for power in range(poly_r.degree(), -1, -1):
        value = sp.factor(poly_r.coeff_monomial(r**power))
        if value:
            print("E", degree, "r^", power, "terms", len(sp.Poly(value, p, q).terms()))
            print(value)
