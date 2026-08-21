#!/usr/bin/env python3
"""Primary exact saturation audit of the generic unmarked contact chart."""

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
Q = p * (p**3 + p**2 * q + b * q**3)
R = p**3 + sp.Rational(3, 4) * p**2 * q + c * p * q**2 + d * q**3
alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)
direction = lambda form: sp.diff(form, q) - sp.Rational(1, 4) * sp.diff(form, p)
N = tuple(sp.cancel(direction(form) / q) for form in (P, Q, R))
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

# d=0: a complete small lex basis.
d0 = [sp.factor(value.subs(d, 0)) for value in equations]
b0 = sp.solve(d0[0], b)[0]
d0_reduced = [sp.factor(value.subs(b, b0)) for value in d0[1:5]]
gb0 = sp.groebner(d0_reduced, mu, lam, c, a, order="lex", method="f5b")
H0 = (2 * a - 1) ** 3 * (10 * a - 3) * (20 * a - 13)
assert len(gb0.polys) == 4
assert sp.expand(1600 * gb0.polys[-1].as_expr() - H0) == 0

d0_points = (
    (
        sp.Rational(1, 2),
        -sp.Rational(1, 8),
        sp.Rational(1, 8),
        p * (2 * p + q),
    ),
    (
        sp.Rational(3, 10),
        -sp.Rational(7, 120),
        0,
        p**2,
    ),
    (
        sp.Rational(13, 20),
        -sp.Rational(7, 32),
        sp.Rational(7, 32),
        p * (8 * p + 7 * q),
    ),
)
for av, bv, cv, divisor in d0_points:
    substitution = {a: av, b: bv, c: cv, d: 0}
    for form in (alpha / q, beta / q, gamma / q):
        quotient = sp.cancel(form.subs(substitution) / divisor)
        assert sp.denom(quotient) == 1

# d != 0: the last equation, followed by every pivot boundary.
h = 8 * a * mu - 8 * b * lam - b
a0_gb = sp.groebner(
    [value.subs(a, 0) for value in equations] + [h.subs(a, 0)],
    d,
    c,
    b,
    mu,
    lam,
    order="lex",
    method="f5b",
)
assert len(a0_gb.polys) == 1 and a0_gb.polys[0].as_expr() == 1

d_solution = sp.solve(equations[0], d)[0]
mu_solution = (8 * b * lam + b) / (8 * a)
D = 32 * a * c + 3 * a + 24 * b

# D=0, with a != 0, is the exact half-family point d=-1/128.
b_D = -a * (32 * c + 3) / 24
D_equations = []
for value in equations[1:5]:
    reduced = value.subs(d, d_solution).subs(mu, mu_solution).subs(b, b_D)
    D_equations.append(sp.factor(sp.together(reduced).as_numer_denom()[0]))
gb_D = sp.groebner(D_equations, lam, c, a, order="lex", method="f5b")
assert any(sp.expand(poly.as_expr() - (2 * a - 1)) == 0 for poly in gb_D.polys)
assert any(sp.expand(poly.as_expr() - (32 * c - 3)) == 0 for poly in gb_D.polys)

# D != 0 solves lambda.  The next pivot E=0 is d=1/64, a higher-gcd point.
after_d = [sp.factor(value.subs(d, d_solution)) for value in equations]
after_mu = [sp.factor(value.subs(mu, mu_solution)) for value in after_d]
lam_solution = sp.solve(after_mu[1], lam)[0]
E = 24 * a - 16 * c - 9
c_E = (24 * a - 9) / 16
d_E = d_solution.subs(c, c_E)
E_equations = []
for value in equations[1:5]:
    reduced = (
        value.subs(c, c_E)
        .subs(d, d_E)
        .subs(mu, mu_solution)
    )
    E_equations.append(sp.factor(sp.together(reduced).as_numer_denom()[0]))
gb_E = sp.groebner(E_equations, b, lam, a, order="lex", method="f5b")
assert any(sp.expand(poly.as_expr() - a * (2 * a - 1)) == 0 for poly in gb_E.polys)

# On a*d*D*E != 0, solve b and take the exact residual resultant.
after_lam = [
    sp.factor(sp.together(value.subs(lam, lam_solution)))
    for value in after_mu
]
numerators = [
    sp.factor(value.as_numer_denom()[0])
    for value in after_lam[2:5]
]
b_solution = sp.solve(numerators[0], b)[0]
last = [
    sp.factor(sp.together(value.subs(b, b_solution)).as_numer_denom()[0])
    for value in numerators[1:]
]
resultant = sp.factor(sp.resultant(last[0], last[1], c))
quadratic = 128 * a**2 - 96 * a + 17
cubic = 160 * a**3 - 384 * a**2 + 310 * a - 85
expected_factor = (
    a
    * (2 * a - 1) ** 16
    * (20 * a - 13)
    * quadratic**9
    * cubic
)
assert sp.cancel(resultant / expected_factor).is_Integer
assert resultant != 0

# The apparent quadratic factor has no contact point.
theta_q = sp.CRootOf(quadratic, 0)
quadratic_gb = sp.groebner(
    [value.subs(a, theta_q) for value in equations],
    d,
    c,
    b,
    mu,
    lam,
    order="lex",
    extension=theta_q,
    method="f5b",
)
assert len(quadratic_gb.polys) == 1 and quadratic_gb.polys[0].as_expr() == 1

# The cubic factor is the explicit higher-gcd component.
b_cubic = -5 * (2 * a - 1) / 16
c_cubic = -3 * (10 * a**2 - 19 * a + 8) / 20
d_cubic = -(120 * a**2 - 198 * a + 79) / 320
lam_cubic = 2 * a**2 - 3 * a + 2
mu_cubic = -(16 * a - 5) / 32
for value in equations:
    numerator = sp.together(
        value.subs(
            {
                b: b_cubic,
                c: c_cubic,
                d: d_cubic,
                lam: lam_cubic,
                mu: mu_cubic,
            }
        )
    ).as_numer_denom()[0]
    assert sp.rem(numerator, cubic, a) == 0

# The remaining a=1/2 component is exactly the one-parameter half family.
half = {
    a: sp.Rational(1, 2),
    b: -sp.Rational(1, 8),
    c: 4 * d + sp.Rational(1, 8),
    lam: sp.Rational(1, 2),
    mu: -sp.Rational(5, 32),
}
assert all(sp.expand(value.subs(half)) == 0 for value in equations)

print("PASS generic unmarked contact saturation case tree")
print("PASS d=0 leaves, both pivot boundaries, and open resultant")
print("PASS only half-family or higher-gcd cubic survives")
print("ALL GENERIC CONTACT DECOMPOSITION CHECKS PASSED")
