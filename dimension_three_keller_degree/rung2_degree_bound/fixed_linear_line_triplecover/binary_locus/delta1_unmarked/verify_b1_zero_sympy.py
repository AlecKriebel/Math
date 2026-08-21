#!/usr/bin/env python3
"""Exact contact obstruction on the unmarked b1=0 boundary."""

from __future__ import annotations

import sympy as sp


p, q, r = sp.symbols("p q r")
a, b, c, d, lam, mu = sp.symbols("a b c d lam mu")


def jac2(f: sp.Expr, g: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(f, p) * sp.diff(g, q)
        - sp.diff(f, q) * sp.diff(g, p)
    )


def jac3(f: sp.Expr, g: sp.Expr, h: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix(
            [
                [sp.diff(value, variable) for variable in (p, q, r)]
                for value in (f, g, h)
            ]
        ).det()
    )


P = p * (p * q**2 + a * q**3)
Q = p * (p**3 + b * q**3)
R = p**3 + c * p * q**2 + d * q**3
alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)

N = tuple(sp.cancel(sp.diff(form, q) / q) for form in (P, Q, R))
assert all(sp.denom(entry) == 1 for entry in N)
assert sp.expand(alpha * N[0] + beta * N[1] + gamma * N[2]) == 0

curvature = sp.expand(
    jac3(P, r * N[1], r * N[2])
    + jac3(r * N[0], Q, r * N[2])
    + jac3(r * N[0], r * N[1], R)
)
K = sp.Poly(curvature, r).coeff_monomial(r)
residual = sp.Poly(sp.expand(K - lam * alpha - mu * beta), p, q)
equations = [
    sp.factor(residual.coeff_monomial(p ** (5 - index) * q**index))
    for index in range(6)
]

d_solution = a * c + sp.Rational(3, 4) * b
expected = (
    0,
    -2 * (4 * c * lam + 3 * mu),
    -3 * (4 * a * c * lam + 3 * a * mu - 2 * b * c),
    (12 * a * b * c + 9 * b**2 + 4 * c * mu) / 2,
    (10 * a * c * mu + 2 * b * c * lam + 9 * b * mu) / 2,
    3 * (4 * a * c + 3 * b) * (a * mu - b * lam) / 4,
)
for actual, target in zip(equations, expected):
    assert sp.expand(actual.subs(d, d_solution) - target) == 0

# The three displayed equations imply bc=0 and then b=0 by the two cases.
f1 = 4 * c * lam + 3 * mu
f2 = 4 * a * c * lam + 3 * a * mu - 2 * b * c
f3 = 12 * a * b * c + 9 * b**2 + 4 * c * mu
assert sp.expand(f2 - a * f1 + 2 * b * c) == 0
assert sp.expand(f3.subs(c, 0) - 9 * b**2) == 0
assert sp.expand(f3.subs(b, 0) - 4 * c * mu) == 0

contact = {b: 0, d: a * c}
line = 2 * p + 3 * a * q
assert sp.expand(alpha.subs(contact) - 4 * c * p**3 * q * line) == 0
assert sp.expand(
    beta.subs(contact)
    - q * line * (3 * p**3 - c * p * q**2 - a * c * q**3)
) == 0
assert sp.expand(gamma.subs(contact) + 4 * p**4 * q * line) == 0
assert sp.Poly(q * line, p, q).total_degree() == 2

# Mutation: the coefficient 3 in the extra line is essential.
bad_line = 2 * p + 2 * a * q
assert sp.expand(gamma.subs(contact) + 4 * p**4 * q * bad_line) != 0

print("PASS b1=0 division-free contact solve")
print("PASS every contact point has a degree-two common divisor")
print("ALL B1-ZERO BOUNDARY SYMPY CHECKS PASSED")
