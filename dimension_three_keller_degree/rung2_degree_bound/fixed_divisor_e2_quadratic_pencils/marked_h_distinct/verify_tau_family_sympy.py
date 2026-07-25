#!/usr/bin/env python3
"""Exact symbolic E7/E6 certificate for the smooth-secant tau family."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: verification requires assertions; do not use -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

x, y, z, tau, k = sp.symbols("x y z tau k")
A, B, T = sp.symbols("A B T")
xyz = (x, y, z)

mon3 = tuple(
    x**i * y**j * z ** (3 - i - j)
    for i in range(3, -1, -1)
    for j in range(3 - i, -1, -1)
)
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
    poly = sp.Poly(sp.expand(value), *xyz)
    return [
        poly.coeff_monomial(x**i * y**j * z**ell)
        for i, j, ell in exponents(degree)
    ]


def jac3(f, g, h):
    return sp.Matrix([f, g, h]).jacobian(xyz).det()


def direction_column(direction):
    U, V, W = direction
    return sp.Matrix(
        [sp.Poly(U, *xyz).coeff_monomial(m) for m in mon3]
        + [sp.Poly(V, *xyz).coeff_monomial(m) for m in mon3]
        + [sp.Poly(W, *xyz).coeff_monomial(m) for m in mon2]
    )


h = x**2 + y * z
s = x**2
P, Q = h**2, h * s
R = x * (h + k * s)
q = 9 * k**2 + 6 * k - 1

u = sp.symbols("u0:10")
v = sp.symbols("v0:10")
w = sp.symbols("w0:6")
U0 = sum(c * m for c, m in zip(u, mon3))
V0 = sum(c * m for c, m in zip(v, mon3))
W0 = sum(c * m for c, m in zip(w, mon2))
raw_e7 = sp.expand(
    jac3(P, Q, W0) + jac3(P, V0, R) + jac3(U0, Q, R)
)
M7, rhs7 = sp.linear_eq_to_matrix(coefficients(raw_e7, 7), u + v + w)
assert rhs7 == sp.zeros(36, 1)
assert M7.shape == (36, 26)
assert M7.rank() == 18

columns7 = (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 23, 25)
rows7_q = (1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19, 23, 25, 31, 32)
rows7_l = (1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 17, 18, 23, 25, 30, 31, 32, 33)
assert sp.factor(M7.extract(rows7_q, columns7).det()) == (
    -557256278016 * k**8 * q**2
)
assert sp.factor(M7.extract(rows7_l, columns7).det()) == (
    -557256278016 * k**8 * (3 * k - 1) ** 2
)
assert sp.gcd(q, 3 * k - 1) == 1
assert M7.subs(k, 0).rank() == 14

gauges = [
    direction_column((R, 0, 0)),
    direction_column((0, R, 0)),
    *[
        direction_column(
            tuple(sp.diff(component, variable) for component in (P, Q, R))
        )
        for variable in xyz
    ],
]
normals = [
    direction_column((x**3, 0, 0)),
    direction_column((0, x**3, 0)),
    direction_column((0, 0, x**2)),
]
basis = sp.Matrix.hstack(*(gauges + normals))
assert M7 * basis == sp.zeros(36, 8)
assert basis.rank() == 8
basis_rows = (0, 1, 2, 4, 10, 14, 20, 24)
assert basis.extract(basis_rows, range(8)).det() == -4

U, V, W = A * x**3, B * x**3, T * x**2
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("l0:9")
H2 = sp.Matrix(
    [
        sum(c * m for c, m in zip(a, mon2)),
        sum(c * m for c, m in zip(b, mon2)),
        W,
    ]
)
L = sp.Matrix(3, 3, ell)
weighted = sp.Poly(
    sp.expand(
        (
            L
            + tau * H2.jacobian(xyz)
            + tau**2 * sp.Matrix([U, V, R]).jacobian(xyz)
            + tau**3 * sp.Matrix([P, Q, 0]).jacobian(xyz)
        ).det()
    ),
    tau,
)
assert all(weighted.coeff_monomial(tau**degree) == 0 for degree in (9, 8, 7))
E6 = weighted.coeff_monomial(tau**6)
lower = a + b + ell
M6, rhs6 = sp.linear_eq_to_matrix(coefficients(E6, 6), lower)
assert rhs6 == sp.zeros(28, 1)
assert M6.shape == (28, 21)
assert M6.rank() == 10

columns6 = (1, 2, 3, 5, 7, 8, 9, 11, 19, 20)
rows6_q = (1, 2, 3, 5, 7, 8, 11, 13, 17, 18)
rows6_l = (1, 2, 3, 5, 7, 8, 17, 18, 23, 25)
assert sp.factor(M6.extract(rows6_q, columns6).det()) == (
    -331776 * k**4 * q**2
)
assert sp.factor(M6.extract(rows6_l, columns6).det()) == (
    -331776 * k**4 * (3 * k - 1) ** 2
)
assert M6.subs(k, 0).rank() == 8

# Uniform sharp witness for every finite k.
witness = {parameter: 0 for parameter in (A, B, T) + lower}
witness[ell[1]] = 1
witness[ell[5]] = 1
witness[ell[6]] = 1
assert L.det().subs(witness) == 1
assert all(
    sp.expand(weighted.coeff_monomial(tau**degree).subs(witness)) == 0
    for degree in (9, 8, 7, 6)
)
witness_e5 = sp.Poly(
    sp.expand(weighted.coeff_monomial(tau**5).subs(witness)), *xyz
)
assert witness_e5.coeff_monomial(x**4 * y) == 3 * k - 1
assert witness_e5.coeff_monomial(x**4 * z) == 6 * k + 2
assert sp.gcd(3 * k - 1, 6 * k + 2) == 1

print(
    "PASS tau family: k!=0 has E7 rank 18, three legal normal "
    "parameters, E6 rank 10 with no compatibility, and k survives"
)
