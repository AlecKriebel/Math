#!/usr/bin/env python3
"""Exact repeated-divisor certificate on the unmarked a2=0 boundary."""

from __future__ import annotations

import sympy as sp


p, q, r = sp.symbols("p q r")
a3, b1, b2, b3, c0, c2, c3 = sp.symbols(
    "a3 b1 b2 b3 c0 c2 c3"
)
lam, mu = sp.symbols("lam mu")


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


A = a3 * q**3
B = p**3 + b1 * p**2 * q + b2 * p * q**2 + b3 * q**3
R = (
    c0 * p**3
    + sp.Rational(3, 4) * b1 * c0 * p**2 * q
    + c2 * p * q**2
    + c3 * q**3
)
P, Q = p * A, p * B
alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)
assert all(sp.rem(form, q, q) == 0 for form in (alpha, beta, gamma))

direction = lambda form: (
    sp.diff(form, q) - sp.Rational(1, 4) * b1 * sp.diff(form, p)
)
N = tuple(sp.cancel(direction(form) / q) for form in (P, Q, R))
assert all(sp.denom(entry) == 1 for entry in N)
assert sp.expand(alpha * N[0] + beta * N[1] + gamma * N[2]) == 0

curvature = sp.expand(
    jac3(P, r * N[1], r * N[2])
    + jac3(r * N[0], Q, r * N[2])
    + jac3(r * N[0], r * N[1], R)
)
K = sp.Poly(curvature, r).coeff_monomial(r)
residual = sp.Poly(sp.expand(K - lam * alpha - mu * beta), p, q)
D = 3 * b1**2 * c0 - 24 * b2 * c0 + 32 * c2
assert sp.expand(
    residual.coeff_monomial(p**5) + sp.Rational(3, 4) * a3 * D
) == 0

abar, bbar, gbar = (sp.cancel(form / q) for form in (alpha, beta, gamma))
assert sp.expand(abar.subs(q, 0) - D * p**4 / 4) == 0
expected_beta = (
    a3
    * q
    * (
        15 * b1 * c0 * p**2 * q
        + 36 * c0 * p**3
        + 4 * c2 * p * q**2
        - 12 * c3 * q**3
    )
    / 4
)
expected_gamma = -4 * a3 * p**2 * q * (
    2 * b1 * p * q + b2 * q**2 + 3 * p**2
)
assert sp.expand(bbar - expected_beta) == 0
assert sp.expand(gbar - expected_gamma) == 0

# Reduction by the contact equation D=0 makes every reduced minor divisible q.
c2_solution = (24 * b2 * c0 - 3 * b1**2 * c0) / 32
for form in (abar, bbar, gbar):
    reduced = sp.cancel(form.subs(c2, c2_solution))
    assert sp.rem(reduced, q, q) == 0

# Mutation: removing the b1^2 term from D fails at the alpha endpoint.
bad_d = -24 * b2 * c0 + 32 * c2
assert sp.expand(abar.subs(q, 0) - bad_d * p**4 / 4) != 0

print("PASS general a2=0 contact coefficient")
print("PASS contact forces the repeated divisor q^2")
print("ALL A2-ZERO BOUNDARY SYMPY CHECKS PASSED")
