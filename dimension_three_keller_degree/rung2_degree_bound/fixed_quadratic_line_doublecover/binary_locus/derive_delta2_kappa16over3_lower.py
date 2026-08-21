#!/usr/bin/env python3
"""Exploratory full-lower solve on the kappa=16/3 {2,0} row."""

from __future__ import annotations

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
a, b, k, m, n = sp.symbols("a b k m n")
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


def homogeneous_coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p**index * q ** (degree - index))
        for index in range(degree, -1, -1)
    ]


h = (p + q) * (3 * p + q)
R = (
    a * p**3 + (a + 2 * b) * p**2 * q
    + 3 * b * p * q**2 + b * q**3
)
Nu = 4 * p + q
Nv = -3 * q
Nt = a - b
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
print("PASS E8/E7")

E6_r3 = sp.factor(sp.Poly(E[6], r).coeff_monomial(r**3))
print("E6 r3 =", E6_r3)
E5_r5 = sp.factor(sp.Poly(E[5], r).coeff_monomial(r**5))
print("E5 r5 =", E5_r5)

E6_after_k = sp.Poly(sp.expand(E[6].subs(k, 0)), r)
print("E6|k0 r degree", E6_after_k.degree())
E6_r1 = sp.factor(E6_after_k.coeff_monomial(r))
for index, value in enumerate(homogeneous_coefficients(E6_r1, 5)):
    print("E6 r1 coeff", index, sp.factor(value))

high_solution = {k: 0, m: 0, n: 0, x[5]: 0, y[5]: 0}
E6c = sp.expand(E[6].subs(high_solution))
eq6c = homogeneous_coefficients(E6c, 6)
unknown6 = (x[3], x[4], y[3], y[4], ell[8])
M6, rhs6 = sp.linear_eq_to_matrix(eq6c, unknown6)
print("E6 constant rank", M6.rank())
print("E6 constant kernel", [
    [sp.factor(item) for item in vector] for vector in M6.nullspace()
])

lam = sp.symbols("lam")
e6_solution = {
    **high_solution,
    x[3]: 4 * lam,
    x[4]: lam,
    y[3]: 0,
    y[4]: -3 * lam,
    ell[8]: (a - b) * lam,
}
print("E6 solution residual", sp.factor(E[6].subs(e6_solution)))
E5zero = sp.expand(E[5].subs(e6_solution).subs(lam, 0))
eq5zero = homogeneous_coefficients(E5zero, 5)
M5zero, rhs5zero = sp.linear_eq_to_matrix(eq5zero, (ell[2], ell[5]))
print("E5 lambda0 rank", M5zero.rank())
print("E5 lambda0 matrix", M5zero)
