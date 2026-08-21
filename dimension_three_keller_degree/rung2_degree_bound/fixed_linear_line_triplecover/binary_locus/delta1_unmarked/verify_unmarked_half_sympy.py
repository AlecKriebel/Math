#!/usr/bin/env python3
"""Exact lower-identity certificate for the unmarked a3=1/2 family."""

from __future__ import annotations

import sympy as sp

import explore_half_family_lower as D


if not __debug__:
    raise RuntimeError("assertions must remain enabled")

p, q, r, z = D.p, D.q, D.r, D.z


def exact_zero(value) -> bool:
    return sp.factor(sp.together(value)) == 0


def staged_subs(value, *groups):
    result = value
    for group in groups:
        result = result.subs(group, simultaneous=True)
    return sp.expand(result)


# Exact-delta open and tangent/contact data.
alpha = sp.expand(
    sp.diff(D.Q, p) * sp.diff(D.R, q)
    - sp.diff(D.Q, q) * sp.diff(D.R, p)
)
beta = -sp.expand(
    sp.diff(D.P, p) * sp.diff(D.R, q)
    - sp.diff(D.P, q) * sp.diff(D.R, p)
)
gamma = sp.expand(
    sp.diff(D.P, p) * sp.diff(D.Q, q)
    - sp.diff(D.P, q) * sp.diff(D.Q, p)
)
assert exact_zero(gamma / q + p**2 * (2 * p + q) ** 2 * (4 * p + q) / 2)
for q_value, expected_alpha, expected_beta in (
    (-2 * p, -6 * z, -24 * z),
    (-4 * p, -sp.Rational(5, 4) * (64 * z - 1), -4 * (64 * z - 1)),
):
    assert exact_zero(alpha.subs({q: q_value}) / (q_value * p**4) - expected_alpha)
    assert exact_zero(beta.subs({q: q_value}) / (q_value * p**4) - expected_beta)
assert exact_zero(alpha.subs({p: 0}) / q**5 + sp.Rational(3, 8) * z)
assert exact_zero(beta.subs({p: 0}) / q**5 + sp.Rational(3, 2) * z)

assert exact_zero(D.Nu - (16 * p**2 + 8 * p * q - q**2) / 8)
assert exact_zero(D.Nv + (24 * p**2 + 12 * p * q - q**2) / 32)
assert exact_zero(D.Nt - (64 * z - 1) * (4 * p + q) / 32)

# Complete E6 solution in the legal gauge.
e6 = {
    D.u[0]: 0,
    D.v[0]: 0,
    D.t[0]: 0,
    D.t[2]: 0,
    D.v[1]: -sp.Rational(3, 8) * D.u[1],
    D.t[1]: (64 * z - 1) * D.u[1] / 16,
    D.x5: -sp.Rational(1, 4),
    D.y5: sp.Rational(5, 64),
    D.x3: -D.u[1] + 2 * D.u[2],
    D.x4: (D.u[1] - 4 * D.u[2] + 48 * D.u[3]) / 16,
    D.y3: (3 * D.u[1] + 16 * D.v[2]) / 8,
    D.y4: -(D.u[1] + 16 * D.v[2] - 192 * D.v[3]) / 64,
    D.l[8]: -D.u[1] * (64 * z - 1) / 32,
}
assert exact_zero(staged_subs(D.E[6].as_expr(), e6))

# E5 rank-two solution and constant-r solution.
e5_relations = {
    D.u[2]: sp.Rational(3, 4) * D.u[1] + 4 * D.u[3],
    D.v[2]: -sp.Rational(1, 4) * D.u[1] + 4 * D.v[3],
}
assert exact_zero(
    sp.Poly(
        staged_subs(D.E[5].as_expr(), e6, e5_relations), r
    ).coeff_monomial(r)
)
e5_lower = {
    D.x[0]: 8 * (-D.l[2] - 2 * D.u[1] * D.u[3] + 2 * D.x[2]),
    D.x[1]: (
        -16 * D.l[2]
        + D.u[1] ** 2
        - 16 * D.u[1] * D.u[3]
        + 32 * D.x[2]
    )
    / 4,
    D.y[0]: (
        -128 * D.l[5]
        - D.u[1] ** 2
        - 256 * D.u[1] * D.v[3]
        + 256 * D.y[2]
    )
    / 16,
    D.y[1]: (
        -128 * D.l[5]
        - 3 * D.u[1] ** 2
        - 128 * D.u[1] * D.v[3]
        + 256 * D.y[2]
    )
    / 32,
    D.l[6]: (
        64 * D.l[7] + D.u[1] ** 2 * (64 * z - 1)
    )
    / 16,
}
assert exact_zero(
    staged_subs(D.E[5].as_expr(), e6, e5_relations, e5_lower)
)

# E4: the r coefficient vanishes; the constant term gives two row
# covariants without fixing l13, l23, l32, x2, or y2.
assert exact_zero(
    sp.Poly(
        staged_subs(D.E[4].as_expr(), e6, e5_relations, e5_lower),
        r,
    ).coeff_monomial(r)
)

Az = (
    (2048 * z + 112) * (p**4 + p**3 * q)
    + (576 * z + 30) * p**2 * q**2
    + (32 * z + 1) * p * q**3
    - 24 * z * q**4
)
Bz = (
    384 * (p**4 + p**3 * q)
    + (-512 * z + 104) * p**2 * q**2
    + (-256 * z + 4) * p * q**3
    - 96 * z * q**4
)
M1 = D.l[0] - 4 * D.l[1] + 2 * D.u[1] * D.l[2]
M2 = D.l[3] - 4 * D.l[4] + 2 * D.u[1] * D.l[5]
e4_constant = sp.Poly(
    staged_subs(D.E[4].as_expr(), e6, e5_relations, e5_lower),
    r,
).coeff_monomial(1)
assert exact_zero(e4_constant - (Az * M1 + Bz * M2) / 256)
assert sp.factor(
    (32 * z + 1) * (-96 * z) - (-24 * z) * (-256 * z + 4)
) == -9216 * z**2

kernel = sp.Matrix((1, -4, 2 * D.u[1]))
L_reduced = D.L.applyfunc(
    lambda entry: staged_subs(entry, e6, e5_relations, e5_lower)
)
assert exact_zero((L_reduced * kernel)[0] - M1)
assert exact_zero((L_reduced * kernel)[1] - M2)
assert exact_zero((L_reduced * kernel)[2])

print("PASS unmarked half-family exact-open and tangent identities")
print("PASS complete E6/E5 lower solve with all free coefficients retained")
print("PASS E4 forces the literal nonzero kernel (1,-4,2u1)")
print("ALL UNMARKED HALF-FAMILY SYMPY CHECKS PASSED")
