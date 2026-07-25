#!/usr/bin/python3
"""Exact checks for WORKING_FIXED_CUBIC_LINE_ROW.md."""

from __future__ import annotations

import sympy as sp

p, q, r, t, s, z = sp.symbols("p q r t s z")
variables = (p, q, r)


def jacobian_map(vector: sp.Matrix) -> sp.Matrix:
    return vector.jacobian(variables)


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.expand(entry) == 0 for entry in matrix)


c = sp.symbols("c0:10")
cubic_monomials = (
    p**3,
    p**2 * q,
    p * q**2,
    q**3,
    p**2 * r,
    p * q * r,
    q**2 * r,
    p * r**2,
    q * r**2,
    r**3,
)
h = sum(c[i] * cubic_monomials[i] for i in range(10))
hr = sp.diff(h, r)

A = sp.Matrix([p, q, 0])
H4 = h * A
C = jacobian_map(H4)
k = sp.Matrix([p * hr, q * hr, r * hr - 4 * h])
e3 = sp.Matrix([0, 0, 1])

assert matrix_is_zero(C * k)
assert matrix_is_zero(C.adjugate() + h * k * e3.T)

# Euler/derivation identities.
Dk_h = sum(sp.diff(h, variables[i]) * k[i] for i in range(3))
assert sp.expand(Dk_h + h * hr) == 0

# General cubic and quadratic normal components.
g3c = sp.symbols("g3c0:10")
G3 = sum(g3c[i] * cubic_monomials[i] for i in range(10))
g2c = sp.symbols("g2c0:6")
quadratic_monomials = (p**2, p * q, q**2, p * r, q * r, r**2)
G2 = sum(g2c[i] * quadratic_monomials[i] for i in range(6))

Dk_G3 = sum(sp.diff(G3, variables[i]) * k[i] for i in range(3))
Dk_G2 = sum(sp.diff(G2, variables[i]) * k[i] for i in range(3))

u = sp.symbols("u0:20")
H3 = sp.Matrix(
    [
        sum(u[10 * row + j] * cubic_monomials[j] for j in range(10))
        if row < 2
        else 0
        for row in range(3)
    ]
)
B = jacobian_map(H3)

v = sp.symbols("v0:18")
H2 = sp.Matrix(
    [
        sum(v[6 * row + j] * quadratic_monomials[j] for j in range(6))
        for row in range(3)
    ]
)
JH2 = jacobian_map(H2)
Dk_H2_third = sum(
    sp.diff(H2[2], variables[i]) * k[i] for i in range(3)
)

assert sp.expand(sp.trace(C.adjugate() * jacobian_map(sp.Matrix([0, 0, G3]))) + h * Dk_G3) == 0
assert sp.expand(sp.trace(B.adjugate() * C)) == 0
assert sp.expand(
    sp.trace(C.adjugate() * JH2)
    + sp.trace(B.adjugate() * C)
    + h * Dk_H2_third
) == 0

# Check the dehomogenized derivation formula for general degrees 3 and 2.
for degree, coefficients, monomials in (
    (3, g3c, cubic_monomials),
    (2, g2c, quadratic_monomials),
):
    G = sum(coefficients[i] * monomials[i] for i in range(len(monomials)))
    Dk_G = sum(sp.diff(G, variables[i]) * k[i] for i in range(3))
    gts = sp.expand(G.subs({q: p * t, r: p * s}) / p**degree)
    hts_from_h = sp.expand(h.subs({q: p * t, r: p * s}) / p**3)
    expected = p ** (degree + 2) * (
        degree * sp.diff(hts_from_h, s) * gts
        - 4 * hts_from_h * sp.diff(gts, s)
    )
    substituted = sp.expand(Dk_G.subs({q: p * t, r: p * s}))
    assert sp.expand(substituted - expected) == 0

# The omitted double-factor locus has a genuine nonzero quadratic invariant.
h_exceptional = p * r**2
hr_exceptional = sp.diff(h_exceptional, r)
k_exceptional = sp.Matrix(
    [
        p * hr_exceptional,
        q * hr_exceptional,
        r * hr_exceptional - 4 * h_exceptional,
    ]
)
G2_exceptional = p * r
assert sp.expand(
    sum(
        sp.diff(G2_exceptional, variables[i]) * k_exceptional[i]
        for i in range(3)
    )
) == 0

# The full quadratic invariant space on h=p*r^2 is r*<p,q>.
exceptional_coefficients = sp.symbols("ec0:6")
exceptional_quadratic = sum(
    exceptional_coefficients[i] * quadratic_monomials[i] for i in range(6)
)
exceptional_derivative = sp.Poly(
    sp.expand(
        sum(
            sp.diff(exceptional_quadratic, variables[i]) * k_exceptional[i]
            for i in range(3)
        )
    ),
    p,
    q,
    r,
)
exceptional_matrix, _ = sp.linear_eq_to_matrix(
    [coefficient for _, coefficient in exceptional_derivative.terms()],
    exceptional_coefficients,
)
exceptional_kernel = exceptional_matrix.nullspace()
assert len(exceptional_kernel) == 2
assert {
    sp.expand(
        sum(vector[i] * quadratic_monomials[i] for i in range(6))
    )
    for vector in exceptional_kernel
} == {p * r, q * r}

H4_exceptional = h_exceptional * A
JH4_exceptional = jacobian_map(H4_exceptional)


def weighted_determinant(
    linear_part: sp.Matrix,
    quadratic_part: sp.Matrix,
    cubic_part: sp.Matrix,
) -> sp.Poly:
    expression = (
        linear_part
        + z * jacobian_map(quadratic_part)
        + z**2 * jacobian_map(cubic_part)
        + z**3 * JH4_exceptional
    ).det()
    return sp.Poly(sp.expand(expression), z)


def homogeneous_coefficient(
    expression: sp.Expr,
    exponents: tuple[int, int, int],
) -> sp.Expr:
    return sp.Poly(sp.expand(expression), p, q, r).coeff_monomial(exponents)


# The q*r orbit after the complete E6/E5 solve and affine normalization.
aq, bq, cq, xq, yq, dq, eq, fq, gq = sp.symbols(
    "aq bq cq xq yq dq eq fq gq"
)
lq = sp.symbols("lq0:6")
H3_q = sp.Matrix(
    [
        2 * cq * p * q * r,
        r * (aq * p**2 + bq * p * q + cq * q**2),
        0,
    ]
)
H2_q = sp.Matrix(
    [
        (2 * xq - 2 * aq * cq) * p**2
        + (2 * yq - 2 * bq * cq) * p * q
        + cq**2 * q**2
        + dq * p * r
        + eq * q * r,
        xq * p * q + yq * q**2 + fq * p * r + gq * q * r,
        q * r,
    ]
)
L0_q = sp.Matrix(
    [
        [lq[0], lq[1], lq[2]],
        [lq[3], lq[4], lq[5]],
        [aq, bq, 0],
    ]
)
weighted_q = weighted_determinant(L0_q, H2_q, H3_q)
assert sp.expand(weighted_q.coeff_monomial(z**6)) == 0
assert sp.expand(weighted_q.coeff_monomial(z**5)) == 0
E4_q = weighted_q.coeff_monomial(z**4)
assert homogeneous_coefficient(E4_q, (0, 1, 3)) == lq[2]
assert homogeneous_coefficient(E4_q, (1, 0, 3)) == -2 * lq[5]
assert sp.expand(L0_q.subs({lq[2]: 0, lq[5]: 0}).det()) == 0

# The p*r orbit before the K=0/K!=0 degree-four split.
tau, K, D = sp.symbols("tau K D")
up = sp.symbols("up0:10")
wp = sp.symbols("wp0:6")
lp = sp.symbols("lp0:6")
H3_p_raw = sp.Matrix(
    [
        2 * tau * p * q * r,
        sum(up[i] * cubic_monomials[i] for i in range(10)),
        0,
    ]
)
H2_p_raw = sp.Matrix(
    [
        tau**2 * q**2 + D * p * r + K * q * r,
        sum(wp[i] * quadratic_monomials[i] for i in range(6)),
        p * r,
    ]
)
L0_p_raw = sp.Matrix(
    [
        [lp[0], lp[1], lp[2]],
        [lp[3], lp[4], lp[5]],
        [0, tau, 0],
    ]
)
weighted_p_raw = weighted_determinant(L0_p_raw, H2_p_raw, H3_p_raw)
for degree in (8, 7, 6, 5):
    assert sp.expand(weighted_p_raw.coeff_monomial(z**degree)) == 0
E4_p_raw = sp.expand(weighted_p_raw.coeff_monomial(z**4))
expected_E4_p_raw = (
    3 * K * up[9] * r**4
    + K * up[8] * q * r**3
    + (K * up[7] - lp[2]) * p * r**3
    + K * (tau - up[6]) * q**2 * r**2
    + (-D * tau - K * up[5] + lp[1]) * p * q * r**2
    + (-K * up[4] + lp[0]) * p**2 * r**2
    - 3 * K * up[3] * q**3 * r
    - 3 * K * up[2] * p * q**2 * r
    - 3 * K * up[1] * p**2 * q * r
    - 3 * K * up[0] * p**3 * r
)
assert sp.expand(E4_p_raw - expected_E4_p_raw) == 0

L0_p_K0 = sp.Matrix(
    [
        [0, tau * D, 0],
        [lp[3], lp[4], lp[5]],
        [0, tau, 0],
    ]
)
assert sp.expand(L0_p_K0.det()) == 0

# The K!=0 branch after E4 and E3.
Ap0, Bp0, Cp0, Ep0, Gp0 = sp.symbols("Ap0 Bp0 Cp0 Ep0 Gp0")
mp0, np0, op0 = sp.symbols("mp0 np0 op0")
H3_p = sp.Matrix(
    [
        2 * tau * p * q * r,
        r
        * (
            Ap0 * p**2
            + Bp0 * p * q
            + tau * q**2
            + Cp0 * p * r
        ),
        0,
    ]
)
H2_p = sp.Matrix(
    [
        tau**2 * q**2 + D * p * r + K * q * r,
        Ap0 * tau * p * q
        + Bp0 * tau * q**2
        + Ep0 * p * r
        + Gp0 * q * r,
        p * r,
    ]
)
L0_p = sp.Matrix(
    [
        [K * Ap0, tau * D + K * Bp0, K * Cp0],
        [mp0, np0, op0],
        [0, tau, 0],
    ]
)
weighted_p = weighted_determinant(L0_p, H2_p, H3_p)
for degree in (8, 7, 6, 5, 4, 3):
    assert sp.expand(weighted_p.coeff_monomial(z**degree)) == 0
E2_p = sp.expand(weighted_p.coeff_monomial(z**2))
expected_E2_p = (
    -K * (Ap0 * Cp0 * tau - Ap0 * Gp0 + mp0) * p * r
    - K
    * (Bp0 * Cp0 * tau - Bp0 * Gp0 - Ep0 * tau + np0)
    * q
    * r
    + K * (Cp0**2 * tau - Cp0 * Gp0 + op0) * r**2
)
assert sp.expand(E2_p - expected_E2_p) == 0

lower_solution = {
    mp0: Ap0 * (Gp0 - Cp0 * tau),
    np0: Ep0 * tau + Bp0 * (Gp0 - Cp0 * tau),
    op0: Cp0 * (Gp0 - Cp0 * tau),
}
assert sp.expand(E2_p.subs(lower_solution)) == 0
assert sp.expand(weighted_p.coeff_monomial(z).subs(lower_solution)) == 0
assert sp.expand(L0_p.det().subs(lower_solution)) == 0

print("fixed-cubic line-row SymPy checks passed")
