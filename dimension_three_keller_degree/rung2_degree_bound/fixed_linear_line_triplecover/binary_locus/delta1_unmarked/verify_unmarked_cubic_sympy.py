#!/usr/bin/env python3
"""Exact cubic-contact gcd jump in the unmarked fixed-linear chart."""

from __future__ import annotations

import sympy as sp


p, q, r, a = sp.symbols("p q r a")
C = 160 * a**3 - 384 * a**2 + 310 * a - 85


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


def assert_zero_mod_c(expr: sp.Expr, message: str) -> None:
    """Check every p,q,r coefficient after reduction modulo C(a)."""
    expression = sp.together(sp.expand(expr))
    numerator, denominator = expression.as_numer_denom()
    assert denominator != 0
    polynomial = sp.Poly(numerator, p, q, r)
    for coefficient in polynomial.coeffs():
        remainder = sp.rem(coefficient, C, a)
        assert sp.expand(remainder) == 0, (message, remainder)


A = p * q**2 + a * q**3
B = p**3 + p**2 * q - sp.Rational(5, 16) * (2 * a - 1) * q**3
R = (
    p**3
    + sp.Rational(3, 4) * p**2 * q
    - sp.Rational(3, 20) * (10 * a**2 - 19 * a + 8) * p * q**2
    - sp.Rational(1, 320) * (120 * a**2 - 198 * a + 79) * q**3
)
P, Q = p * A, p * B

alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)
assert all(sp.rem(form, q, q) == 0 for form in (alpha, beta, gamma))

direction = lambda form: (
    sp.diff(form, q) - sp.Rational(1, 4) * sp.diff(form, p)
)
N = tuple(sp.cancel(direction(form) / q) for form in (P, Q, R))
assert all(sp.denom(entry) == 1 for entry in N)
assert_zero_mod_c(
    alpha * N[0] + beta * N[1] + gamma * N[2],
    "directional-gradient syzygy",
)

curvature = sp.expand(
    jac3(P, r * N[1], r * N[2])
    + jac3(r * N[0], Q, r * N[2])
    + jac3(r * N[0], r * N[1], R)
)
K = sp.Poly(curvature, r).coeff_monomial(r)
lam = 2 * a**2 - 3 * a + 2
mu = -(16 * a - 5) / 32
assert_zero_mod_c(K - lam * alpha - mu * beta, "contact identity")

G = (
    p**2
    + (sp.Rational(5, 2) * a - sp.Rational(3, 4)) * p * q
    + (
        sp.Rational(5, 2) * a**2
        - sp.Rational(23, 8) * a
        + sp.Rational(15, 16)
    )
    * q**2
)
Qa = (
    p**2
    + (1 - a) * p * q
    + (
        sp.Rational(5, 16) * a**2
        - sp.Rational(27, 64) * a
        + sp.Rational(15, 128)
    )
    * q**2
)
Qb = (
    p**2
    + (1 - a) * p * q
    + (
        sp.Rational(1, 2) * a**2
        - sp.Rational(7, 10) * a
        + sp.Rational(17, 80)
    )
    * q**2
)
Qc = p + (sp.Rational(5, 4) - a) * q
Afac = -12 * a**2 + sp.Rational(114, 5) * a - sp.Rational(177, 20)

assert_zero_mod_c(alpha / q - Afac * G * Qa, "alpha common factor")
assert_zero_mod_c(beta / q - 6 * G * Qb, "beta common factor")
assert_zero_mod_c(gamma / q + 8 * p**2 * G * Qc, "gamma common factor")

# Mutation: deleting the q^2 coefficient of G cannot pass the certificate.
bad_g = G - sp.Poly(G, p, q).coeff_monomial(q**2) * q**2
mutation = sp.together(beta / q - 6 * bad_g * Qb)
try:
    assert_zero_mod_c(mutation, "deliberately bad common factor")
except AssertionError:
    pass
else:
    raise AssertionError("common-factor mutation was not detected")

assert sp.Poly(G, p, q).total_degree() == 2
assert sp.Poly(G, p, q).coeff_monomial(p**2) == 1
assert sp.gcd(sp.Poly(C, a), sp.Poly(sp.diff(C, a), a)).degree() == 0

print("PASS cubic contact relation over Q[a]/(C)")
print("PASS literal common divisor qG of degree three")
print("ALL UNMARKED CUBIC-CONTACT SYMPY CHECKS PASSED")
