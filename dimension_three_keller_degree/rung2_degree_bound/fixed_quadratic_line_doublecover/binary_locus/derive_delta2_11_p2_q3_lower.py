#!/usr/bin/env python3
"""Full lower solve on the R=q^3 endpoint of the h=p^2 branch-contact row."""

from __future__ import annotations

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
k, d = sp.symbols("k d", nonzero=True)
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


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


H4 = sp.Matrix([p**4, p**2 * q**2, 0])
H3 = sp.Matrix(
    [
        binary(u, 3) + 2 * k * r * p**2,
        binary(v, 3) + k * r * q**2,
        d * q**3,
    ]
)
H2 = sp.Matrix(
    [
        binary(x[:3], 2)
        + r * (x[3] * p + x[4] * q)
        + k**2 * r**2,
        binary(y[:3], 2) + r * (y[3] * p + y[4] * q),
        binary(t, 2),
    ]
)
L = sp.Matrix(3, 3, ell)
weighted = sp.Poly(
    sp.expand(
        (
            L
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
assert sp.expand(sp.Poly(E[6], r).coeff_monomial(r)) == 0

E6c = sp.Poly(E[6], r).coeff_monomial(1)
unknown6 = (x[3], x[4], y[3], y[4], ell[8], *t, *u, *v)
M6, rhs6 = sp.linear_eq_to_matrix(coefficients(E6c, 6), unknown6)
print("E6 rank", M6.rank(), "pivots", M6.rref()[1])
for omitted in range(7):
    rows = tuple(index for index in range(7) if index != omitted)
    determinant = sp.factor(
        M6.extract(rows, (0, 1, 2, 3, 4, 10)).det()
    )
    if determinant:
        print("E6 decisive", rows, determinant)
        break
print("E6 solution", sp.linsolve((M6, rhs6), unknown6))

e6_solution = {
    x[3]: k * (sp.Rational(3, 2) * u[0] - v[2]),
    x[4]: k * u[1],
    y[3]: k * (-t[1] / (3 * d) + sp.Rational(3, 2) * v[0]),
    y[4]: k * v[1],
    ell[8]: k * t[0],
    u[2]: 0,
}
assert sp.expand(E[6].subs(e6_solution)) == 0
E5after = sp.Poly(sp.expand(E[5].subs(e6_solution)), r)
print("E5 r degree", E5after.degree())
for power in range(E5after.degree(), 0, -1):
    print("E5 r^", power, sp.factor(E5after.coeff_monomial(r**power)))

e5_high = {
    t[1]: sp.Rational(3, 2) * d * v[0],
    u[0]: 2 * v[2],
}
E5constant = sp.expand(E5after.coeff_monomial(1).subs(e5_high))
eq5 = coefficients(E5constant, 5)
unknown5 = (x[1], y[1], ell[2], ell[5], ell[6])
M5, rhs5 = sp.linear_eq_to_matrix(eq5, unknown5)
print("E5 constant rank", M5.rank(), "pivots", M5.rref()[1])
for omitted in range(6):
    rows = tuple(index for index in range(6) if index != omitted)
    determinant = sp.factor(M5.extract(rows, range(5)).det())
    if determinant:
        print("E5 decisive", rows, determinant)
        break
print("E5 constant solution", sp.linsolve((M5, rhs5), unknown5))
left5 = M5.T.nullspace()
print(
    "E5 compatibility",
    [sp.factor((vector.T * rhs5)[0]) for vector in left5],
)
print("E5 left vector", [sp.factor(value) for value in left5[0]])
print("E5 p5 compatibility equation", sp.factor(eq5[0]))
e5_compat = {v[0]: 0}
M5c, rhs5c = sp.linear_eq_to_matrix(
    [equation.subs(e5_compat) for equation in eq5], unknown5
)
print(
    "E5 compatible solution",
    sp.linsolve((M5c, rhs5c), unknown5),
)

e5_solution = {
    t[1]: 0,
    u[0]: 2 * v[2],
    v[0]: 0,
    x[1]: u[1] * v[2],
    y[1]: v[1] * v[2],
    ell[2]: k * (x[0] - v[2] ** 2),
    ell[5]: k * y[0],
    ell[6]: t[0] * v[2],
}
assert sp.expand(E[5].subs(e6_solution).subs(e5_solution)) == 0
E4done = sp.factor(
    sp.expand(E[4].subs(e6_solution).subs(e5_solution))
)
print("E4", E4done)
M0 = sp.factor((k * ell[0] - v[2] * ell[2]).subs(e5_solution))
M3 = sp.factor((k * ell[3] - v[2] * ell[5]).subs(e5_solution))
expected_E4 = d * (6 * M3 * p**2 * q**2 - 3 * M0 * q**4)
print("E4 residual", sp.factor(E4done - expected_E4))
Ldone = L.subs(e6_solution).subs(e5_solution)
print(
    "L kernel residual",
    [sp.factor(value) for value in Ldone * sp.Matrix([k, 0, -v[2]])],
)
