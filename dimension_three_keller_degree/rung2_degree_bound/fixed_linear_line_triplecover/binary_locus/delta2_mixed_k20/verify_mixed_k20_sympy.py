#!/usr/bin/env python3
"""Exact checks for the fixed-linear mixed-divisor {2,0} delta=2 leaf."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp


p, q, r, z = sp.symbols("p q r z")
a2, a3, b2, b3, c0, c2 = sp.symbols("a2 a3 b2 b3 c0 c2")
m, n, lam, mu = sp.symbols("m n lam mu")


def zero(value: sp.Expr) -> bool:
    return sp.cancel(sp.expand(value)) == 0


def jac2(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, p) * sp.diff(second, q)
        - sp.diff(first, q) * sp.diff(second, p)
    )


def jac3(first: sp.Expr, second: sp.Expr, third: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix(
            [
                [sp.diff(value, variable) for variable in (p, q, r)]
                for value in (first, second, third)
            ]
        ).det()
    )


A = q**2 * (a2 * p + a3 * q)
B = p**3 + b2 * p * q**2 + b3 * q**3
P, Q = p * A, p * B
R = p * (c0 * p**2 + c2 * q**2)
alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)

for form in (alpha, beta, gamma):
    assert not sp.denom(sp.cancel(form / (p * q))).has(p, q)

N = tuple(sp.cancel(sp.diff(form, q) / (p * q)) for form in (P, Q, R))
expected_N = (
    2 * a2 * p + 3 * a3 * q,
    2 * b2 * p + 3 * b3 * q,
    2 * c2,
)
assert all(zero(actual - expected) for actual, expected in zip(N, expected_N))
assert zero(alpha * N[0] + beta * N[1] + gamma * N[2])
print("PASS twice-divided gradient and {2,0} tangent")

# The r-part of the E7 multiplier is killed by the curvature.
u, v, w = N
C = sp.factor(
    (
        w * jac2(P, v)
        + w * jac2(u, Q)
        - v * jac2(u, R)
        + u * jac2(v, R)
    )
    / 2
)
D = a2 * b3 - a3 * b2
expected_C = -3 * p * (
    (3 * c0 * D + 4 * a3 * c2) * p**2 - c2 * D * q**2
)
assert zero(C - expected_C)
print("PASS nonzero curvature excludes the r-multiplier")

# Contact equations for f=mp+nq.
f = m * p + n * q
tangent = tuple(sp.expand(f * value) for value in N)
curvature = sp.expand(
    jac3(P, r * tangent[1], r * tangent[2])
    + jac3(r * tangent[0], Q, r * tangent[2])
    + jac3(r * tangent[0], r * tangent[1], R)
)
K = sp.Poly(curvature, r).coeff_monomial(r)
residual = sp.Poly(sp.expand(K - lam * alpha - mu * beta), p, q)
equations = [
    sp.factor(residual.coeff_monomial(p ** (5 - index) * q**index))
    for index in range(6)
]
expected_equations = (
    -6 * m**2 * (3 * a2 * b3 * c0 - 3 * a3 * b2 * c0 + 4 * a3 * c2),
    -2
    * (
        18 * a2 * b3 * c0 * m * n
        + 3 * a2 * c0 * mu
        - 18 * a3 * b2 * c0 * m * n
        + 24 * a3 * c2 * m * n
        - 3 * b2 * c0 * lam
        + 4 * c2 * lam
    ),
    -3
    * (
        6 * a2 * b3 * c0 * n**2
        - 2 * a2 * b3 * c2 * m**2
        - 6 * a3 * b2 * c0 * n**2
        + 2 * a3 * b2 * c2 * m**2
        + 3 * a3 * c0 * mu
        + 8 * a3 * c2 * n**2
        - 3 * b3 * c0 * lam
    ),
    2
    * c2
    * (
        6 * a2 * b3 * m * n
        + a2 * mu
        - 6 * a3 * b2 * m * n
        - b2 * lam
    ),
    c2
    * (
        6 * a2 * b3 * n**2
        - 6 * a3 * b2 * n**2
        - a3 * mu
        + b3 * lam
    ),
    sp.Integer(0),
)
assert all(
    zero(actual - expected)
    for actual, expected in zip(equations, expected_equations)
)

# Endpoint chart a3=0: (a2,a3,b2,b3,c2)=(1,0,0,1,1).
c = sp.symbols("c")
chart_one = {a2: 1, a3: 0, b2: 0, b3: 1, c2: 1, c0: c}
chart_one_equations = [sp.factor(value.subs(chart_one)) for value in equations[:-1]]
expected_one = (
    -18 * c * m**2,
    -2 * (18 * c * m * n + 3 * c * mu + 4 * lam),
    -3 * (6 * c * n**2 - 2 * m**2 - 3 * c * lam),
    2 * (6 * m * n + mu),
    6 * n**2 + lam,
)
assert all(
    zero(actual - expected)
    for actual, expected in zip(chart_one_equations, expected_one)
)
gb_m = sp.groebner(
    [value.subs(m, 1) for value in chart_one_equations],
    n,
    lam,
    mu,
    c,
    order="lex",
)
gb_n = sp.groebner(
    [value.subs({m: 0, n: 1}) for value in chart_one_equations],
    lam,
    mu,
    c,
    order="lex",
)
assert gb_m.polys[0].as_expr() == 1
assert gb_n.polys[0].as_expr() == 1
print("PASS first endpoint chart has no projective contact")

# Endpoint chart a3=1,b3=0.
a, b = sp.symbols("a b")
chart_two = {a2: a, a3: 1, b2: b, b3: 0, c2: 1, c0: c}
chart_two_equations = [sp.factor(value.subs(chart_two)) for value in equations[:-1]]
E = 4 - 3 * b * c
expected_two = (
    -6 * E * m**2,
    -2 * ((24 - 18 * b * c) * m * n + 3 * a * c * mu + E * lam),
    -3 * ((8 - 6 * b * c) * n**2 + 2 * b * m**2 + 3 * c * mu),
    2 * (-6 * b * m * n + a * mu - b * lam),
    -6 * b * n**2 - mu,
)
assert all(
    zero(actual - expected)
    for actual, expected in zip(chart_two_equations, expected_two)
)

# The m=0 projective chart is exactly a=0, 3bc=1.
gb_two_m0 = sp.groebner(
    [value.subs({m: 0, n: 1}) for value in chart_two_equations],
    lam,
    mu,
    a,
    c,
    b,
    order="lex",
)
assert [
    sp.factor(poly.as_expr()) for poly in gb_two_m0.polys
] == [lam, mu + 6 * b, a, 3 * b * c - 1]

# On E=0, saturate b and set n=1.  This gives a=0, bm^2=12.
inverse_b = sp.symbols("inverse_b")
E_zero_equations = [
    sp.together(
        value.subs({c: sp.Rational(4, 3) / b, n: 1})
    ).as_numer_denom()[0]
    for value in chart_two_equations
]
gb_two_E0 = sp.groebner(
    E_zero_equations + [inverse_b * b - 1],
    lam,
    mu,
    a,
    m,
    inverse_b,
    b,
    order="lex",
)
assert [
    sp.factor(poly.as_expr()) for poly in gb_two_E0.polys
] == [
    lam + 6 * m,
    mu + 6 * b,
    a,
    -12 * inverse_b + m**2,
    b * inverse_b - 1,
]
print("PASS second endpoint projective contact decomposition")

# Both projective contact loci have larger gcd.
high_three = {a2: 0, a3: 1, b2: b, b3: 0, c2: 1, c0: sp.Rational(4, 3) / b}
expected_high_three = (
    2 * b * p**2 * q**3,
    p * q**2 * (b * q**2 + 12 * p**2) / b,
    -4 * p**2 * q**2 * (b * q**2 + 3 * p**2),
)
for actual, expected in zip((alpha, beta, gamma), expected_high_three):
    assert zero(actual.subs(high_three) - expected)

high_four = {a2: 0, a3: 1, b2: b, b3: 0, c2: 1, c0: sp.Rational(1, 3) / b}
G = 3 * p**2 + b * q**2
expected_high_four = (
    2 * p**2 * q * G,
    p * q**2 * G / b,
    -4 * p**2 * q**2 * G,
)
for actual, expected in zip((alpha, beta, gamma), expected_high_four):
    assert zero(actual.subs(high_four) - expected)
assert sp.Poly(G, p, q).coeff_monomial(p**2) == 3
print("PASS both nonzero contacts route to higher gcd")

# Optional E5 boundary regression on the degree-four-gcd contact.
tau = sp.symbols("tau")
P0, Q0, R0 = P.subs(high_four), Q.subs(high_four), R.subs(high_four)
N0 = tuple(value.subs(high_four) for value in N)
S0 = tuple(sp.expand(tau * q * value) for value in N0)
H4 = sp.Matrix([P0, Q0, 0])
H3 = sp.Matrix([r * S0[0], r * S0[1], R0])
H2 = sp.Matrix([0, 3 * b * tau**2 * r**2, r * S0[2]])
weighted = sp.Poly(
    sp.expand(
        (
            z * H2.jacobian((p, q, r))
            + z**2 * H3.jacobian((p, q, r))
            + z**3 * H4.jacobian((p, q, r))
        ).det()
    ),
    z,
)
assert zero(weighted.coeff_monomial(z**7))
assert zero(weighted.coeff_monomial(z**6))
assert zero(
    sp.Poly(weighted.coeff_monomial(z**5), r).coeff_monomial(r**2)
    - 12 * tau**3 * q * G
)
print("PASS optional higher-gcd E5 boundary regression")
print("ALL FIXED-LINEAR MIXED {2,0} DELTA2 SYMPY CHECKS PASSED")
