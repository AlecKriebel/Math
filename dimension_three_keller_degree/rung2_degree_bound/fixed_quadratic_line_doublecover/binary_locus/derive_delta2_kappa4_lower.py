#!/usr/bin/env python3
"""Exploratory full-lower solve on the doubled-root kappa=4 {2,0} row."""

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


h = (p + q) ** 2
d = (5 * b - 6 * a) / 3
R = a * p**3 + b * p**2 * q + sp.Rational(3, 2) * d * p * q**2 + d * q**3
Nu, Nv, Nt = 6 * p + 4 * q, -2 * q, 6 * a - b
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
print("E6 r3", sp.factor(sp.Poly(E[6], r).coeff_monomial(r**3)))
print("E5 r5", sp.factor(sp.Poly(E[5], r).coeff_monomial(r**5)))

E6k = sp.Poly(sp.expand(E[6].subs(k, 0)), r)
print("E6 k0 rdeg", E6k.degree())
for index, value in enumerate(
    homogeneous_coefficients(E6k.coeff_monomial(r), 5)
):
    print(index, sp.factor(value))

high = {k: 0, m: 0, n: 0, x[5]: 0, y[5]: 0}
E6c = sp.expand(E[6].subs(high))
eq6 = homogeneous_coefficients(E6c, 6)
unknown6 = (x[3], x[4], y[3], y[4], ell[8])
M6, rhs6 = sp.linear_eq_to_matrix(eq6, unknown6)
print("E6c rank", M6.rank(), "kernel", [
    [sp.factor(zv) for zv in vec] for vec in M6.nullspace()
])

lam = sp.symbols("lam")
e6sol = {
    **high,
    x[3]: 6 * lam,
    x[4]: 4 * lam,
    y[3]: 0,
    y[4]: -2 * lam,
    ell[8]: (6 * a - b) * lam,
}
print("E6 residual", sp.factor(E[6].subs(e6sol)))
E5after = sp.expand(E[5].subs(e6sol))
E5zero = E5after.subs(lam, 0)
M5z, rhs5z = sp.linear_eq_to_matrix(
    homogeneous_coefficients(E5zero, 5), (ell[2], ell[5])
)
print("E5 lambda0 rank", M5z.rank())

# Residual non-plane branch 6a=b.
E5res = sp.expand(E5after.subs(a, b / 6))
eq5res = homogeneous_coefficients(E5res, 5)
unknown5 = (
    ell[2], ell[5], t[0], t[1], t[2],
    v[0], v[1], v[2], v[3],
)
M5, rhs5 = sp.linear_eq_to_matrix(eq5res, unknown5)
print("E5 residual rank", M5.rank(), "pivots", M5.rref()[1])
print("E5 residual solve", sp.solve(eq5res, unknown5, dict=True))

e5sol = {
    ell[2]: (
        -12 * lam * u[0] + 14 * lam * u[1] - 15 * lam * u[2]
        + sp.Rational(27, 2) * lam * u[3]
    ),
    ell[5]: (
        6 * lam * u[0] - 5 * lam * u[1] + 6 * lam * u[2]
        - 6 * lam * u[3] + 4 * lam * v[1] - 3 * lam * v[3]
    ),
    t[0]: t[2] / 4,
    t[1]: t[2],
    v[0]: (
        u[0] - sp.Rational(5, 6) * u[1] + u[2] - u[3]
        + sp.Rational(5, 6) * v[1] - sp.Rational(1, 2) * v[3]
    ),
    v[2]: -u[2] / 2 + sp.Rational(3, 4) * u[3] + sp.Rational(3, 2) * v[3],
}
print("E5 solved residual", sp.factor(E5res.subs(e5sol)))
E4done = sp.Poly(
    sp.expand(E[4].subs(e6sol).subs(a, b / 6).subs(e5sol)), r
)
print("E4 rdegree", E4done.degree())
for power in range(E4done.degree(), -1, -1):
    value = sp.factor(E4done.coeff_monomial(r**power))
    if value:
        print("E4", power, value)
