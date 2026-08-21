#!/usr/bin/env python3
"""Full lower exploration of the first exact-delta=2 {1,1} E6 survivor."""

from __future__ import annotations

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
k = sp.symbols("k", nonzero=True)
variables = (p, q, r)
u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
t = sp.symbols("t0:3")
x = sp.symbols("x0:5")
y = sp.symbols("y0:5")
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


h = p**2
R = p * (-11 * p**2 + 16 * p * q + q**2)
Nu = 4 * p**2
Nv = 6 * p * q + q**2
Nt = 15 * p + 30 * q
H4 = sp.Matrix([h * p**2, h * q**2, 0])
H3 = sp.Matrix(
    [
        binary(u, 3) + k * r * Nu,
        binary(v, 3) + k * r * Nv,
        R,
    ]
)
H2 = sp.Matrix(
    [
        binary(x[:3], 2) + r * (x[3] * p + x[4] * q) + 6 * k**2 * r**2,
        binary(y[:3], 2) + r * (y[3] * p + y[4] * q) + 9 * k**2 * r**2,
        binary(t, 2) + k * r * Nt,
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
E6r = sp.factor(sp.Poly(E[6], r).coeff_monomial(r))
assert E6r == 0
print("PASS exact rational E7/E6-r survivor with (x5,y5)=(6k^2,9k^2)")

E6c = sp.Poly(E[6], r).coeff_monomial(1)
assert sp.Poly(E[6], r).degree() <= 0
eq6 = homogeneous_coefficients(E6c, 6)
unknown6 = (
    x[3], x[4], y[3], y[4], ell[8],
    *t, *u, *v,
)
M6, rhs6 = sp.linear_eq_to_matrix(eq6, unknown6)
print("E6 rank", M6.rank(), "shape", M6.shape)
print("E6 pivots", M6.rref()[1])
for omitted_row in range(7):
    rows = tuple(index for index in range(7) if index != omitted_row)
    determinant = sp.factor(
        M6.extract(rows, (0, 1, 2, 3, 4, 11)).det()
    )
    if determinant:
        print("E6 decisive rows", rows, "det", determinant)
        break
solution6 = sp.linsolve((M6, rhs6), unknown6)
print("E6 solution", solution6)

e6_solution = {
    x[3]: k * (-4 * t[2] + 3 * u[0] + 3 * u[1] + 108 * v[3]),
    x[4]: k * (sp.Rational(3, 2) * u[1] + 6 * u[2] + 6 * v[3]),
    y[3]: 3 * k * (v[0] + v[1]),
    y[4]: k * (
        -sp.Rational(1, 2) * t[1]
        + 10 * t[2]
        + sp.Rational(3, 2) * v[1]
        + 6 * v[2]
        - sp.Rational(621, 2) * v[3]
    ),
    ell[8]: k * (2 * t[0] - t[1] + 113 * t[2] - 3375 * v[3]),
    u[3]: 0,
}
assert sp.expand(E[6].subs(e6_solution)) == 0

E5after = sp.Poly(sp.expand(E[5].subs(e6_solution)), r)
print("E5 r degree", E5after.degree())
for power in range(E5after.degree(), 0, -1):
    coefficient = sp.factor(E5after.coeff_monomial(r**power))
    print("E5 r^", power, "=", coefficient)
