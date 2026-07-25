#!/usr/bin/env python3
"""Exact contact exclusion for the unmarked-double {1,1} component."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp


p, q, r = sp.symbols("p q r")
b, c, d, e = sp.symbols("b c d e")
x, y, lam, mu = sp.symbols("x y lam mu")
variables = (p, q, r)


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
                [sp.diff(value, variable) for variable in variables]
                for value in (first, second, third)
            ]
        ).det()
    )


def normal_forms(
    b_value: sp.Expr,
    c_value: sp.Expr,
    d_value: sp.Expr,
    e_value: sp.Expr,
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    return (
        p * q**3,
        p
        * (
            p**3
            + b_value * p**2 * q
            + c_value * p * q**2
        ),
        d_value
        * (
            p**3
            + sp.Rational(3, 4) * b_value * p**2 * q
            + (
                sp.Rational(3, 4) * c_value
                - sp.Rational(3, 32) * b_value**2
            )
            * p
            * q**2
        )
        + e_value * q**3,
    )


def tangents(
    P: sp.Expr,
    Q: sp.Expr,
    R: sp.Expr,
    b_value: sp.Expr,
    c_value: sp.Expr,
) -> tuple[sp.Matrix, sp.Matrix]:
    gradient_p = sp.Matrix(
        [sp.diff(value, p) for value in (P, Q, R)]
    )
    gradient_q = sp.Matrix(
        [sp.diff(value, q) for value in (P, Q, R)]
    )
    first = sp.simplify((gradient_q - b_value * gradient_p / 4) / q)
    discriminant = 3 * b_value**2 - 8 * c_value
    second = sp.simplify(
        (p * first + discriminant * gradient_p / 16) / q
    )
    return first, second


def contact_coefficients(
    P: sp.Expr,
    Q: sp.Expr,
    R: sp.Expr,
    first: sp.Matrix,
    second: sp.Matrix,
) -> list[sp.Expr]:
    tangent = x * first + y * second
    curvature = sp.Poly(
        sp.expand(
            jac3(P, r * tangent[1], r * tangent[2])
            + jac3(r * tangent[0], Q, r * tangent[2])
            + jac3(r * tangent[0], r * tangent[1], R)
        ),
        r,
    ).coeff_monomial(r)
    residual = sp.Poly(
        sp.expand(
            curvature
            - lam * jac2(Q, R)
            - mu * (-jac2(P, R))
        ),
        p,
        q,
    )
    return [
        sp.factor(
            residual.coeff_monomial(p ** (5 - index) * q**index)
        )
        for index in range(6)
    ]


# General normal form and its two minimal Hilbert--Burch columns.
P, Q, R = normal_forms(b, c, d, e)
K = 3 * b**2 - 8 * c
N, M = tangents(P, Q, R, b, c)
gradient = sp.Matrix(
    [[sp.diff(value, p), sp.diff(value, q)] for value in (P, Q, R)]
)
change = sp.Matrix(
    [
        [-16 * p / K, (3 * b**2 * q - 4 * b * p - 8 * c * q) / K],
        [16 * q / K, 4 * b * q / K],
    ]
)
assert all(
    zero(value)
    for value in gradient - sp.Matrix.hstack(N, M) * change
)
assert zero(change.det() + 16 * q**2 / K)
alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)
assert zero(alpha * N[0] + beta * N[1] + gamma * N[2])
assert zero(alpha * M[0] + beta * M[1] + gamma * M[2])
print("PASS unmarked-double {1,1} Hilbert--Burch basis")


# On the generic scaling chart b=d=1, exact gcd q^2 is equivalent to
# e*J!=0 (and the present component also has K=3-8c!=0).
cg, eg = sp.symbols("cg eg")
Pg, Qg, Rg = normal_forms(1, cg, 1, eg)
Ng, Mg = tangents(Pg, Qg, Rg, 1, cg)
generic_contact = contact_coefficients(Pg, Qg, Rg, Ng, Mg)
Kg = 3 - 8 * cg
Jg = (
    192 * cg**3
    - 48 * cg**2
    - 1024 * cg * eg
    - 5 * cg
    + 1024 * eg**2
    + 320 * eg
)
Ag, Bg, Cg = (
    sp.factor(jac2(Qg, Rg) / q**2),
    sp.factor(-jac2(Pg, Rg) / q**2),
    sp.factor(jac2(Pg, Qg) / q**2),
)
Hg = 3 * p**2 + 2 * p * q + cg * q**2
assert zero(Cg + 4 * p**2 * Hg)
assert zero(Bg.subs(p, 0) + 3 * eg * q**3)
assert zero(
    sp.resultant(Bg.subs(q, 1), Hg.subs(q, 1), p)
    - sp.Rational(243, 1024) * Jg
)
print("PASS generic-chart exact-gcd boundary polynomial")


# Generic chart, y=0.  Exact contact has x!=0, so scale x=1.
y0 = [sp.factor(value.subs({y: 0, x: 1})) for value in generic_contact]
assert y0[0] == 0 and y0[1] == 0
assert zero(y0[5] - sp.Rational(3, 8) * eg * (cg + 8 * mu))
mu_value = -cg / 8
y0_mu = [sp.factor(value.subs(mu, mu_value)) for value in y0]
assert zero(
    y0_mu[4]
    + sp.Rational(3, 8)
    * eg
    * (16 * lam * cg - 8 * cg - 3)
)
# On eg!=0, the preceding coefficient forces cg!=0 and this lambda.
lam_value = (8 * cg + 3) / (16 * cg)
assert zero(
    y0_mu[2].subs(lam, lam_value)
    + 3
    * (8 * cg - 3)
    * (96 * cg**2 - 36 * cg - 128 * eg + 5)
    / (512 * cg)
)
assert zero(
    y0_mu[3].subs(lam, lam_value)
    + 3
    * (8 * cg - 3)
    * (32 * cg * eg + cg - 24 * eg)
    / (128 * cg)
)
eg_value = (96 * cg**2 - 36 * cg + 5) / 128
assert zero(
    (32 * cg * eg + cg - 24 * eg).subs(eg, eg_value)
    - sp.Rational(3, 16) * (4 * cg - 1) ** 2 * (8 * cg - 5)
)
assert zero(
    Jg.subs(eg, eg_value)
    - sp.Rational(9, 16)
    * (4 * cg - 1) ** 2
    * (8 * cg - 5) ** 2
)
# Thus the contact alternatives cg=1/4 or 5/8 both have Jg=0.
print("PASS generic y=0 contacts have larger gcd")


# Generic chart, y!=0.  Scale y=1.  The first two coefficients force
# eg=e0 and, off Kg=0, h=0.
y1 = [sp.factor(value.subs(y, 1)) for value in generic_contact]
e0 = -(25 - 144 * cg + 192 * cg**2) / 512
h = 64 * cg**2 - 16 * cg - 1
assert zero(
    y1[0]
    - sp.Rational(3, 128)
    * (192 * cg**2 - 144 * cg + 512 * eg + 25)
)
assert zero(
    y1[1].subs(eg, e0)
    + sp.Rational(45, 2048) * (8 * cg - 3) * h
)

# Reduce the last four cleared equations modulo h after eg=e0.  Two
# normalized remainders have a short compatibility.
cleared_y1: list[sp.Expr] = []
for value in y1[2:]:
    numerator = sp.Poly(
        sp.together(value.subs(eg, e0)).as_numer_denom()[0],
        cg,
        x,
        lam,
        mu,
    )
    cleared_y1.append(numerator.primitive()[1].as_expr())
remainders = [
    sp.factor(
        sp.rem(sp.Poly(value, cg), sp.Poly(h, cg)).as_expr()
    )
    for value in cleared_y1
]
R2 = (
    -1024 * lam * cg
    + 256 * lam
    - 2048 * mu
    + 1024 * cg * x**2
    - 512 * cg * x
    - 104 * cg
    - 320 * x**2
    + 160 * x
    + 31
)
R3 = (
    -5120 * lam * cg
    + 1280 * lam
    - 10240 * mu
    + 5120 * cg * x**2
    - 3904 * cg * x
    - 408 * cg
    - 1600 * x**2
    + 1208 * x
    + 121
)


def proportional(first: sp.Expr, second: sp.Expr) -> bool:
    first_poly = sp.Poly(first, cg, x, lam, mu)
    second_poly = sp.Poly(second, cg, x, lam, mu)
    if first_poly.monoms() != second_poly.monoms():
        return False
    ratios = {
        sp.cancel(a / b)
        for a, b in zip(first_poly.coeffs(), second_poly.coeffs())
    }
    return len(ratios) == 1 and 0 not in ratios


assert any(proportional(value, R2) for value in remainders)
assert any(proportional(value, R3) for value in remainders)
assert zero(R3 - 5 * R2 + 2 * (56 * cg - 17) * (12 * x - 1))
assert sp.resultant(h, 56 * cg - 17, cg) == 128

# With x=1/12, an integral rescaling of three remaining equations is
# incompatible: its augmented determinant is nonzero in Q[c]/(h).
E0 = (
    9216 * lam * cg
    - 2304 * lam
    + 18432 * mu
    + 1256 * cg
    - 379
)
E1 = (
    4608 * lam * cg
    - 1728 * lam
    - 73728 * mu * cg
    + 9216 * mu
    + 12792 * cg
    - 3865
)
E2 = 221184 * mu * cg - 64512 * mu - 824 * cg + 249
augmented = sp.Matrix(
    [
        [
            sp.diff(value, lam),
            sp.diff(value, mu),
            value.subs({lam: 0, mu: 0}),
        ]
        for value in (E0, E1, E2)
    ]
)
determinant_remainder = sp.factor(
    sp.rem(
        sp.Poly(augmented.det(), cg),
        sp.Poly(h, cg),
    ).as_expr()
)
assert zero(
    determinant_remainder
    + 31850496 * (79048 * cg - 23855)
)
assert sp.resultant(h, 79048 * cg - 23855, cg) == 278656

# A direct saturation/unit check guards the hand elimination.
sat = sp.symbols("sat")
y1_cleared = [
    sp.Poly(value, cg, eg, x, lam, mu).clear_denoms()[1].as_expr()
    for value in y1
]
unit_y1 = sp.groebner(
    y1_cleared,
    lam,
    mu,
    x,
    eg,
    cg,
    order="grevlex",
)
assert len(unit_y1.polys) == 1 and unit_y1.polys[0].as_expr() == 1
y0_cleared = [
    sp.Poly(value, cg, eg, lam, mu).clear_denoms()[1].as_expr()
    for value in y0[2:]
]
unit_y0_exact = sp.groebner(
    y0_cleared + [sat * Kg * eg * Jg - 1],
    sat,
    lam,
    mu,
    eg,
    cg,
    order="grevlex",
)
assert (
    len(unit_y0_exact.polys) == 1
    and unit_y0_exact.polys[0].as_expr() == 1
)
print("PASS generic y!=0 chart is empty")
print("PASS generic exact contact saturation is empty")


# Boundary b!=0,d=0.  Scale b=e=1.  The first contact equation gives
# y=0; then x=1 and two coefficients force K=0.
P10, Q10, R10 = normal_forms(1, cg, 0, 1)
N10, M10 = tangents(P10, Q10, R10, 1, cg)
contact10 = contact_coefficients(P10, Q10, R10, N10, M10)
assert zero(contact10[0] - 12 * y**2)
contact10_y0 = [
    sp.factor(value.subs({y: 0, x: 1})) for value in contact10
]
assert proportional(contact10_y0[2], lam - 1)
assert proportional(contact10_y0[3], 8 * cg + 12 * lam - 15)
print("PASS b!=0,d=0 boundary has no {1,1} contact")


# Boundary b=0,c!=0,d!=0.  Scale c=d=1; exact gcd forces e!=0.
P01, Q01, R01 = normal_forms(0, 1, 1, eg)
N01, M01 = tangents(P01, Q01, R01, 0, 1)
contact01 = contact_coefficients(P01, Q01, R01, N01, M01)
assert proportional(contact01[0], y**2)
contact01_y0 = [
    sp.factor(value.subs({y: 0, x: 1})) for value in contact01
]
assert proportional(contact01_y0[5], eg * mu)
assert proportional(contact01_y0[4], mu + 8 * eg * lam)
assert proportional(contact01_y0[3], 4 * eg + lam)
print("PASS b=0,c!=0,d!=0 boundary has no contact")


# Corner b=d=0,c!=0.  Scale c=e=1.  Again the first nonzero
# coefficient forces y=0, while the next curvature coefficient is a
# nonzero constant after x=1.
P00, Q00, R00 = normal_forms(0, 1, 0, 1)
N00, M00 = tangents(P00, Q00, R00, 0, 1)
contact00 = contact_coefficients(P00, Q00, R00, N00, M00)
assert proportional(contact00[1], y**2)
assert contact00[3].subs({y: 0, x: 1}) != 0
print("PASS b=d=0,c!=0 corner has no contact")

print("ALL UNMARKED-DOUBLE {1,1} SYMPY CHECKS PASSED")
