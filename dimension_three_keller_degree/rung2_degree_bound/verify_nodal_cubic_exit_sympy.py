#!/usr/bin/python3
"""Exact checks for WORKING_NODAL_CUBIC_CURVE_EXIT.md."""

from __future__ import annotations

import sympy as sp

p, q, r, scale = sp.symbols("p q r scale")
alpha, beta, lam, u, v = sp.symbols("alpha beta lam u v")
variables = (p, q, r)

A = sp.Matrix([p**2 * q, p * q**2, p**3 + q**3])
Ap = A.diff(p)
Aq = A.diff(q)

a, b, c, d = sp.symbols("a b c d")
ell = a * p + b * q
m = c * p + d * q
V = ell * Ap + m * Aq
normal_minor = sp.factor(sp.Matrix.hstack(V.diff(p), V.diff(q), A).det())
expected_minor = 6 * (p**3 + q**3) * (
    c * p**2 + (d - a) * p * q - b * q**2
) ** 2
assert sp.expand(normal_minor - expected_minor) == 0


def jacobian_map(H: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([[sp.diff(H[i], variable) for variable in variables]
                      for i in range(3)])


D2A = (
    alpha**2 * A.diff(p, 2)
    + 2 * alpha * beta * A.diff(p).diff(q)
    + beta**2 * A.diff(q, 2)
)
H4 = r * A
H3 = lam * A + r * (alpha * Ap + beta * Aq)
H2 = (u * Ap + v * Aq) / 3 + r * D2A / 2

L0 = sp.Matrix(
    [
        [
            -2 * alpha * beta * lam + sp.Rational(2, 3) * (alpha * v + beta * u),
            -alpha**2 * lam + sp.Rational(2, 3) * alpha * u,
            alpha**2 * beta,
        ],
        [
            -beta**2 * lam + sp.Rational(2, 3) * beta * v,
            -2 * alpha * beta * lam + sp.Rational(2, 3) * (alpha * v + beta * u),
            alpha * beta**2,
        ],
        [
            -3 * alpha**2 * lam + 2 * alpha * u,
            -3 * beta**2 * lam + 2 * beta * v,
            alpha**3 + beta**3,
        ],
    ]
)

weighted = (
    L0
    + scale * jacobian_map(H2)
    + scale**2 * jacobian_map(H3)
    + scale**3 * jacobian_map(H4)
)
determinant = sp.Poly(sp.expand(weighted.det()), scale)
assert sp.expand(determinant.coeff_monomial(scale**8)) == 0
assert sp.expand(determinant.coeff_monomial(scale**7)) == 0
assert sp.expand(determinant.coeff_monomial(scale**6)) == 0

expected_det = (
    sp.Rational(4, 9)
    * (alpha**3 + beta**3)
    * (alpha * v - beta * u) ** 2
)
assert sp.expand(L0.det() - expected_det) == 0

degree_five = sp.factor(determinant.coeff_monomial(scale**5))
expected_five = (
    sp.Rational(4, 9)
    * (p**3 + q**3)
    * ((3 * beta * lam - v) * p + (u - 3 * alpha * lam) * q) ** 2
)
assert sp.expand(degree_five - expected_five) == 0

print("nodal cubic-stratum exit SymPy checks passed")
