#!/usr/bin/env python3
"""Exact primary certificate for the marked fixed-linear delta=1 component."""

from __future__ import annotations

import sympy as sp

import explore_contact as E


if not __debug__:
    raise RuntimeError("assertions must remain enabled")

lam, mu, t = sp.symbols("lam mu t")


def exact_zero(value) -> bool:
    return sp.factor(sp.together(value)) == 0


def coeffs(substitutions):
    residual = sp.Poly(
        sp.expand(
            (E.K - lam * E.alpha - mu * E.beta).subs(substitutions) / E.p
        ),
        E.p,
        E.q,
    )
    return [
        sp.factor(
            residual.coeff_monomial(E.p ** (4 - index) * E.q**index)
        )
        for index in range(5)
    ]


# The divided q-gradient is the required tangent.
assert exact_zero(
    E.alpha * E.N[0] + E.beta * E.N[1] + E.gamma * E.N[2]
)

# Double-root orbit: contact forces an additional q divisor.
double = {E.s0: 0, E.s1: 0}
double_equations = coeffs(double)
assert exact_zero(
    double_equations[0] + 8 * (E.a0 * E.b1 - E.a1 * E.b0)
)
alpha_double = sp.factor(E.alpha.subs(double) / E.p)
beta_double = sp.factor(E.beta.subs(double) / E.p)
gamma_double = sp.factor(E.gamma.subs(double) / E.p)
assert sp.rem(alpha_double, E.q, E.q) == 0
assert sp.rem(beta_double, E.q, E.q) == 0
assert exact_zero(
    gamma_double.subs({E.q: 0})
    - 4 * (E.a0 * E.b1 - E.a1 * E.b0) * E.p**5
)

# Squarefree orbit, followed by the legal a2=1, b2=0 gauge.
squarefree = {E.s0: 1, E.s1: 0}
raw = coeffs(squarefree)
raw_a2_zero = [
    sp.factor(value.subs({E.a2: 0})) for value in raw
]
assert exact_zero(raw_a2_zero[4] - lam)
assert sp.factor(raw_a2_zero[3].subs({lam: 0}) / 2) == 7 * E.a1
assert exact_zero(sp.factor(
    raw_a2_zero[1].subs({lam: 0, E.a1: 0}) / 2
) - 4 * E.a0 * mu)
assert exact_zero(sp.factor(
    raw_a2_zero[2].subs({lam: 0, E.a1: 0, mu: 0})
) - 24 * E.a0)

gauge = {**squarefree, E.a2: 1, E.b2: 0}
gauged = coeffs(gauge)
solution = {
    lam: -6,
    mu: -7 * E.a1,
    E.b0: (7 * E.a0 - 3) * E.a1 / 6,
    E.b1: (72 - 24 * E.a0 + 35 * E.a1**2) / 28,
}
assert exact_zero(gauged[4].subs({lam: -6}))
assert exact_zero(gauged[3].subs({lam: -6, mu: -7 * E.a1}))
assert exact_zero(gauged[1].subs(solution))
assert exact_zero(gauged[2].subs(solution))
assert exact_zero(
    gauged[0].subs(solution)
    - sp.Rational(2, 21)
    * (E.a0 - 3)
    * (72 * E.a0 - 7 * E.a1**2 + 108)
)

# First contact family: literal degree-three extra factor.
family_one = {
    **gauge,
    E.a0: 3,
    E.a1: t,
    E.b0: 3 * t,
    E.b1: sp.Rational(5, 4) * t**2,
}
G1 = 3 * t * E.p**3 - 18 * E.p**2 * E.q - 5 * t * E.p * E.q**2 - 2 * E.q**3
assert exact_zero(
    E.alpha.subs(family_one)
    + E.p * (5 * E.p * t - 2 * E.q) * G1 / 4
)
assert exact_zero(E.beta.subs(family_one) - E.p**2 * G1)
assert exact_zero(
    E.gamma.subs(family_one)
    - E.p**2 * (E.p * t - 2 * E.q) * G1
)

# Second contact family: literal degree-two extra factor.
family_two = {
    **gauge,
    E.a1: t,
    E.a0: sp.Rational(7, 72) * t**2 - sp.Rational(3, 2),
    E.b0: t * (49 * t**2 - 972) / 432,
    E.b1: (49 * t**2 + 162) / 42,
}
G2 = 27 * E.p**2 - 7 * t * E.p * E.q - 3 * E.q**2
assert exact_zero(
    E.alpha.subs(family_two)
    + E.p
    * G2
    * (
        49 * E.p**2 * t**2
        + 162 * E.p**2
        + 294 * E.p * E.q * t
        - 126 * E.q**2
    )
    / 378
)
assert exact_zero(
    E.beta.subs(family_two)
    - E.p**2 * (E.p * t + 6 * E.q) * G2 / 9
)
assert exact_zero(
    E.gamma.subs(family_two)
    - E.p**2
    * G2
    * (
        49 * E.p**2 * t**2
        - 324 * E.p**2
        + 168 * E.p * E.q * t
        - 504 * E.q**2
    )
    / 378
)

print("PASS marked delta=1 double-root contact routes to delta>=2")
print("PASS marked delta=1 squarefree contact has exactly two deeper families")
print("PASS literal common factors have total gcd degrees at least 4 and 3")
print("ALL MARKED FIXED-LINEAR DELTA1 SYMPY CHECKS PASSED")
