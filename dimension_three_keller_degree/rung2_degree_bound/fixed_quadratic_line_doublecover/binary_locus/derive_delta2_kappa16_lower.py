#!/usr/bin/env python3
"""Derive E6 and E5 after the kappa=16 r^1 tangent is killed."""

from __future__ import annotations

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
a, d, m, n = sp.symbols("a d m n")
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
        poly.coeff_monomial(p**i * q ** (degree - i))
        for i in range(degree, -1, -1)
    ]


h = p**2 + 4 * p * q + q**2
R = a * p**3 + 3 * a * p**2 * q + 3 * d * p * q**2 + d * q**3
Nu = 5 * p + q
Nv = -p - 5 * q
Nt = 3 * (a - d)
W = m * p + n * q

H4 = sp.Matrix([h * p**2, h * q**2, 0])
H3 = sp.Matrix(
    [binary(u, 3) + Nu * W * r, binary(v, 3) + Nv * W * r, R]
)
H2 = sp.Matrix(
    [
        binary(x[:3], 2) + r * (x[3] * p + x[4] * q) + x[5] * r**2,
        binary(y[:3], 2) + r * (y[3] * p + y[4] * q) + y[5] * r**2,
        binary(t, 2) + Nt * W * r,
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
E6 = sp.expand(weighted.coeff_monomial(z**6))
E5 = sp.expand(weighted.coeff_monomial(z**5))
E4 = sp.expand(weighted.coeff_monomial(z**4))

E6r = sp.factor(sp.Poly(E6, r).coeff_monomial(r))
print("E6 r =", E6r)
eq6r = homogeneous_coefficients(E6r, 5)
M6r, rhs6r = sp.linear_eq_to_matrix(eq6r, (x[5], y[5]))
print("E6 r matrix rank", M6r.rank())
print("E6 r augmented rank", M6r.row_join(rhs6r).rank())
print("E6 r solve", sp.solve(eq6r, (x[5], y[5]), dict=True))
print("E6 r Groebner", sp.groebner(eq6r, x[5], y[5], m, n).polys)

high_solution = {m: 0, n: 0, x[5]: 0, y[5]: 0}
E6c = sp.factor(E6.subs(high_solution))
eq6c = homogeneous_coefficients(E6c, 6)
unknown6c = (x[3], x[4], y[3], y[4], ell[8])
M6c, rhs6c = sp.linear_eq_to_matrix(eq6c, unknown6c)
print("E6 c matrix rank", M6c.rank())
print("E6 c kernel", [
    [sp.factor(entry) for entry in vector]
    for vector in M6c.nullspace()
])
compatibility6 = [
    sp.factor((vector.T * rhs6c)[0])
    for vector in M6c.T.nullspace()
]
print("E6 c compatibility count", len(compatibility6))
for index, value in enumerate(compatibility6):
    print("E6 c compatibility", index, value)
print("E6 c solve", sp.solve(eq6c, unknown6c, dict=True))

lam = sp.symbols("lam")
e6_solution = {
    **high_solution,
    x[3]: 5 * lam,
    x[4]: lam,
    y[3]: -lam,
    y[4]: -5 * lam,
    ell[8]: 3 * (a - d) * lam,
}
assert sp.expand(E6.subs(e6_solution)) == 0
E5_after_E6 = sp.Poly(sp.expand(E5.subs(e6_solution)), r)
print("E5 after E6 r-degree", E5_after_E6.degree())
for power in range(E5_after_E6.degree(), -1, -1):
    value = sp.factor(E5_after_E6.coeff_monomial(r**power))
    if value:
        print("E5 r^", power, "=", value)

E5_equal = sp.factor(E5_after_E6.coeff_monomial(1).subs(d, a))
eq5_equal = homogeneous_coefficients(E5_equal, 5)
print("E5 a=d coefficients")
for index, value in enumerate(eq5_equal):
    print(index, sp.factor(value / (2 * a)))
unknown5 = (
    ell[2], ell[5],
    t[0], t[1], t[2],
    v[0], v[1], v[2], v[3],
)
M5, rhs5 = sp.linear_eq_to_matrix(eq5_equal, unknown5)
print("E5 a=d selected rank", M5.rank())
print("E5 a=d selected solve", sp.solve(eq5_equal, unknown5, dict=True))

e5_solution = {
    ell[2]: (
        -sp.Rational(3, 10) * lam * u[0]
        + sp.Rational(11, 10) * lam * u[1]
        - sp.Rational(7, 2) * lam * u[2]
        + sp.Rational(15, 2) * lam * u[3]
    ),
    ell[5]: (
        sp.Rational(3, 2) * lam * u[0]
        - sp.Rational(1, 2) * lam * u[1]
        + sp.Rational(11, 2) * lam * u[2]
        - sp.Rational(33, 2) * lam * u[3]
        + lam * v[1]
        - 3 * lam * v[3]
    ),
    t[0]: t[2],
    t[1]: 2 * t[2],
    v[0]: -u[0] / 5 + u[1] / 15 + v[1] / 3,
    v[2]: -5 * u[2] + 15 * u[3] + 3 * v[3],
}
assert sp.expand(E5.subs(e6_solution).subs(d, a).subs(e5_solution)) == 0
E4_after_E5 = sp.Poly(
    sp.expand(E4.subs(e6_solution).subs(d, a).subs(e5_solution)), r
)
print("E4 after E5 r-degree", E4_after_E5.degree())
for power in range(E4_after_E5.degree(), -1, -1):
    value = sp.factor(E4_after_E5.coeff_monomial(r**power))
    if value:
        print("E4 r^", power, "=", value)
