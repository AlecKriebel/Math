#!/usr/bin/env python3
"""Exact contact and lower obstruction on the unmarked c0=0 boundary."""

from __future__ import annotations

import sympy as sp


p, q, r, tau = sp.symbols("p q r tau")
a, b, d, lam, mu = sp.symbols("a b d lam mu")
variables = (p, q, r)


def jac2(f: sp.Expr, g: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(f, p) * sp.diff(g, q)
        - sp.diff(f, q) * sp.diff(g, p)
    )


def jac3(f: sp.Expr, g: sp.Expr, h: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix(
            [
                [sp.diff(value, variable) for variable in variables]
                for value in (f, g, h)
            ]
        ).det()
    )


P0 = p * (p * q**2 + a * q**3)
Q0 = p * (p**3 + p**2 * q + b * q**3)
R0 = p * q**2 + d * q**3
alpha0, beta0, gamma0 = (
    jac2(Q0, R0),
    -jac2(P0, R0),
    jac2(P0, Q0),
)
direction0 = lambda form: sp.diff(form, q) - sp.Rational(1, 4) * sp.diff(form, p)
N0 = tuple(sp.cancel(direction0(form) / q) for form in (P0, Q0, R0))
curvature0 = sp.expand(
    jac3(P0, r * N0[1], r * N0[2])
    + jac3(r * N0[0], Q0, r * N0[2])
    + jac3(r * N0[0], r * N0[1], R0)
)
K0 = sp.Poly(curvature0, r).coeff_monomial(r)
residual0 = sp.Poly(sp.expand(K0 - lam * alpha0 - mu * beta0), p, q)
contact = [
    sp.factor(residual0.coeff_monomial(p ** (5 - index) * q**index))
    for index in range(6)
]

dsol = (4 * a - 1) / 4
lamsol = (4 * a - 1) / 2
reduced = [sp.factor(value.subs(d, dsol).subs(lam, lamsol)) for value in contact]
assert reduced[0] == 0 and reduced[1] == 0
assert sp.expand(
    reduced[2] + sp.Rational(3, 8) * (32 * a**2 - 30 * a - 16 * b + 5)
) == 0

bsol = (32 * a**2 - 30 * a + 5) / 16
musol = -(192 * a**3 - 368 * a**2 + 216 * a - 35) / 32
f4 = sp.factor(reduced[4].subs({b: bsol, mu: musol}))
f5 = sp.factor(reduced[5].subs({b: bsol, mu: musol}) / (4 * a - 1))
assert sp.expand(
    f4
    + sp.Rational(3, 128)
    * (2 * a - 1)
    * (640 * a**3 - 1056 * a**2 + 480 * a - 65)
) == 0
assert sp.expand(
    f5
    + sp.Rational(9, 512)
    * (2 * a - 1)
    * (128 * a**3 - 96 * a**2 + 5)
) == 0
assert sp.resultant(
    640 * a**3 - 1056 * a**2 + 480 * a - 65,
    128 * a**3 - 96 * a**2 + 5,
    a,
) == -11324620800

orbit = {
    a: sp.Rational(1, 2),
    b: -sp.Rational(1, 8),
    d: sp.Rational(1, 4),
    lam: sp.Rational(1, 2),
    mu: -sp.Rational(5, 32),
}
assert all(sp.expand(value.subs(orbit)) == 0 for value in contact)

# Endpoint subcharts before b1 and c2 are normalized.
b1g, c2g = sp.symbols("b1g c2g")
Bg = p**3 + b1g * p**2 * q + b * q**3
Rg = c2g * p * q**2 + d * q**3
Qg = p * Bg
alphag, betag, gammag = jac2(Qg, Rg), -jac2(P0, Rg), jac2(P0, Qg)
Ng = tuple(
    sp.cancel(
        (
            sp.diff(form, q)
            - sp.Rational(1, 4) * b1g * sp.diff(form, p)
        )
        / q
    )
    for form in (P0, Qg, Rg)
)
curvg = sp.expand(
    jac3(P0, r * Ng[1], r * Ng[2])
    + jac3(r * Ng[0], Qg, r * Ng[2])
    + jac3(r * Ng[0], r * Ng[1], Rg)
)
Kg = sp.Poly(curvg, r).coeff_monomial(r)
resg = sp.Poly(sp.expand(Kg - lam * alphag - mu * betag), p, q)
assert sp.expand(
    resg.coeff_monomial(p**5)
    + 6 * (4 * a * c2g - b1g * c2g - 4 * d)
) == 0

endpoint = {b1g: 0, c2g: 1, d: a, b: 0, lam: 0, mu: 0}
assert all(
    sp.expand(
        resg.coeff_monomial(p ** (5 - index) * q**index).subs(endpoint)
    )
    == 0
    for index in range(6)
)
lineg = 2 * p + 3 * a * q
assert sp.expand(alphag.subs(endpoint) - 4 * p**3 * q * lineg) == 0
assert sp.expand(
    betag.subs(endpoint) + q**3 * (p + a * q) * lineg
) == 0
assert sp.expand(gammag.subs(endpoint) + 4 * p**4 * q * lineg) == 0

P, Q, R = P0.subs(orbit), Q0.subs(orbit), R0.subs(orbit)
alpha, beta, gamma = alpha0.subs(orbit), beta0.subs(orbit), gamma0.subs(orbit)
abar, bbar, gbar = alpha / q, beta / q, gamma / q
assert sp.expand(
    abar
    - (8 * p**2 + 4 * p * q + q**2)
    * (32 * p**2 + 16 * p * q - 3 * q**2)
    / 32
) == 0
assert sp.expand(bbar + q**2 * (16 * p**2 + 8 * p * q + 3 * q**2) / 8) == 0
assert sp.expand(gbar + p**2 * (2 * p + q) ** 2 * (4 * p + q) / 2) == 0
affine_gcd = sp.gcd(
    sp.gcd(sp.Poly(abar.subs(q, 1), p), sp.Poly(bbar.subs(q, 1), p)),
    sp.Poly(gbar.subs(q, 1), p),
)
assert affine_gcd.degree() == 0
assert not all(sp.expand(form.subs(q, 0)) == 0 for form in (abar, bbar, gbar))

Nu, Nv, Nt = [sp.cancel(direction0(form) / q) for form in (P, Q, R)]
u0, v2, w = sp.symbols("u0 v2 w")
x2, y2 = sp.symbols("x2 y2")
l11, l12, l13, l21, l22, l23, l32 = sp.symbols(
    "l11 l12 l13 l21 l22 l23 l32"
)
u1 = sp.Rational(3, 4) * u0 + sp.Rational(8, 9) * w
u2 = sp.Rational(1, 8) * u0 + sp.Rational(2, 3) * w
v0 = sp.Rational(16, 9) * w + 8 * v2
v1 = w + 6 * v2
t1 = sp.Rational(8, 9) * w
U = u0 * p**3 + u1 * p**2 * q + u2 * p * q**2 + r * Nu
V = v0 * p**3 + v1 * p**2 * q + v2 * p * q**2 + r * Nv
T = t1 * p * q + r * Nt

x0 = -8 * l13 + sp.Rational(2, 9) * u0 * w + 16 * x2
x1 = (
    -4 * l13
    + sp.Rational(1, 18) * u0 * w
    + sp.Rational(16, 81) * w**2
    + 8 * x2
)
y0 = (
    -8 * l23
    + sp.Rational(16, 9) * v2 * w
    + sp.Rational(28, 81) * w**2
    + 16 * y2
)
y1 = (
    -4 * l23
    + sp.Rational(4, 9) * v2 * w
    + sp.Rational(2, 81) * w**2
    + 8 * y2
)
x3 = -u0 / 8 + sp.Rational(4, 9) * w
x4 = -u0 / 32 - w / 9
y3 = -w / 3 - v2
y4 = -w / 72 - v2 / 4
A2 = x0 * p**2 + x1 * p * q + x2 * q**2 + r * (x3 * p + x4 * q) - r**2 / 4
B2 = y0 * p**2 + y1 * p * q + y2 * q**2 + r * (y3 * p + y4 * q) + 5 * r**2 / 64

l31 = 4 * l32 + sp.Rational(64, 81) * w**2
l33 = -sp.Rational(4, 9) * w
L = sp.Matrix(
    [
        [l11, l12, l13],
        [l21, l22, l23],
        [l31, l32, l33],
    ]
)
H4 = sp.Matrix((P, Q, 0))
H3 = sp.Matrix((U, V, R))
H2 = sp.Matrix((A2, B2, T))
weighted = sp.Poly(
    sp.expand(
        (
            L
            + tau * H2.jacobian(variables)
            + tau**2 * H3.jacobian(variables)
            + tau**3 * H4.jacobian(variables)
        ).det()
    ),
    tau,
)
for degree in (8, 7, 6, 5):
    assert sp.expand(weighted.coeff_monomial(tau**degree)) == 0

M1 = 9 * l11 - 36 * l12 + 16 * w * l13
M2 = 9 * l21 - 36 * l22 + 16 * w * l23
expected_e4 = (
    sp.Rational(2, 9) * M1 * (p**4 + p**3 * q)
    + (9 * M1 - 8 * M2) * p**2 * q**2 / 144
    + (M1 - 8 * M2) * p * q**3 / 288
    - (M1 + 4 * M2) * q**4 / 384
)
assert sp.expand(weighted.coeff_monomial(tau**4) - expected_e4) == 0

kernel = sp.Matrix((9, -36, 16 * w))
assert sp.expand((L * kernel)[0] - M1) == 0
assert sp.expand((L * kernel)[1] - M2) == 0
assert sp.expand((L * kernel)[2]) == 0
assert kernel[0] != 0

print("PASS c0=0 unique exact contact orbit")
print("PASS complete E6/E5/E4 lower reconstruction")
print("PASS literal kernel (9,-36,16w)")
print("ALL C0-ZERO BOUNDARY SYMPY CHECKS PASSED")
