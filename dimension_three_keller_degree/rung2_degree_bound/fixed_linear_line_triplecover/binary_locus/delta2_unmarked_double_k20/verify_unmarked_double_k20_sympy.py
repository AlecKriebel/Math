#!/usr/bin/env python3
"""Exact checks for the full unmarked-double {2,0} delta=2 component."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp


p, q, r, z = sp.symbols("p q r z")
b, c0, c3 = sp.symbols("b c0 c3")
m, n, lam, mu = sp.symbols("m n lam mu")
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


# Reconstruct the unmarked-double normal form from a general q-jet.
a1, a2, a3 = sp.symbols("a1 a2 a3")
b1, b2, b3 = sp.symbols("b1 b2 b3")
d0, d1, d2, d3 = sp.symbols("d0 d1 d2 d3")
A_general = a1 * p**2 * q + a2 * p * q**2 + a3 * q**3
B_general = p**3 + b1 * p**2 * q + b2 * p * q**2 + b3 * q**3
P_general, Q_general = p * A_general, p * B_general
R_general = d0 * p**3 + d1 * p**2 * q + d2 * p * q**2 + d3 * q**3
forms_general = (
    jac2(Q_general, R_general),
    -jac2(P_general, R_general),
    jac2(P_general, Q_general),
)
q_jet = []
for form in forms_general:
    polynomial = sp.Poly(form, p, q)
    total = polynomial.total_degree()
    q_jet.extend(
        polynomial.coeff_monomial(p ** (total - index) * q**index)
        for index in (0, 1)
    )
normal_substitution = {
    a1: 0,
    a2: 0,
    d1: sp.Rational(3, 4) * b1 * d0,
    d2: (
        sp.Rational(3, 4) * b2
        - sp.Rational(3, 32) * b1**2
    )
    * d0,
}
assert all(zero(value.subs(normal_substitution)) for value in q_jet)
assert zero(q_jet[-2] + 4 * a1)
assert zero(q_jet[-1] + 8 * a2)
print("PASS unmarked-double normal form")


# Exceptional Hilbert--Burch divisor 3b1^2-8b2=0.  Normalize a3=1,
# remove b3 by a target shear, and write b=b1.
P = p * q**3
Q = p * (
    p**3 + b * p**2 * q + sp.Rational(3, 8) * b**2 * p * q**2
)
R = c0 * (
    p**3
    + sp.Rational(3, 4) * b * p**2 * q
    + sp.Rational(3, 16) * b**2 * p * q**2
) + c3 * q**3
alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)
direction = lambda form: sp.diff(form, q) - b * sp.diff(form, p) / 4
N = tuple(sp.factor(direction(form) / q**2) for form in (P, Q, R))
expected_N = (
    3 * p - b * q / 4,
    -sp.Rational(3, 16) * b**3 * p,
    -sp.Rational(3, 64) * (b**3 * c0 - 64 * c3),
)
assert all(zero(actual - expected) for actual, expected in zip(N, expected_N))
assert zero(alpha * N[0] + beta * N[1] + gamma * N[2])
gradient = sp.Matrix(
    [[sp.diff(form, p), sp.diff(form, q)] for form in (P, Q, R)]
)
basis = sp.Matrix.hstack(sp.Matrix(N), sp.Matrix([sp.diff(f, p) for f in (P, Q, R)]))
change = sp.Matrix([[0, q**2], [1, b / 4]])
assert all(zero(value) for value in gradient - basis * change)
assert change.det() == -q**2
print("PASS exceptional {2,0} Hilbert--Burch column")


# Its curvature is never zero on b!=0,R!=0, so an r-multiplier is
# impossible.
u, v, w = N
curvature_N = sp.factor(
    (
        w * jac2(P, v)
        + w * jac2(u, Q)
        - v * jac2(u, R)
        + u * jac2(v, R)
    )
    / 2
)
expected_curvature = -sp.Rational(3, 2048) * b * (
    3 * b**5 * c0 * p * q**2
    + 12 * b**4 * c0 * p**2 * q
    + 16 * b**3 * c0 * p**3
    - 48 * b**3 * c3 * q**3
    - 768 * b**2 * c3 * p * q**2
    - 3072 * b * c3 * p**2 * q
    - 4096 * c3 * p**3
)
assert zero(curvature_N - expected_curvature)
# If its p^3 coefficient vanishes, c3=b^3c0/256; its q^3
# coefficient then forces c0=0, hence c3=0.
assert zero(
    sp.Poly(
        expected_curvature.subs(c3, b**3 * c0 / 256), p, q
    ).coeff_monomial(q**3)
    - sp.Rational(9, 32768) * b**7 * c0
)
print("PASS curvature excludes the r-multiplier")


# Contact equations for f=mp+nq.
f = m * p + n * q
S = tuple(sp.expand(f * value) for value in N)
K_contact = sp.Poly(
    sp.expand(
        jac3(P, r * S[1], r * S[2])
        + jac3(r * S[0], Q, r * S[2])
        + jac3(r * S[0], r * S[1], R)
    ),
    r,
).coeff_monomial(r)
residual = sp.Poly(
    sp.expand(K_contact - lam * alpha - mu * beta), p, q
)
contact = [
    sp.factor(
        residual.coeff_monomial(p ** (5 - index) * q**index)
    )
    for index in range(6)
]
T = b**3 * c0 - 256 * c3
assert zero(contact[0] + sp.Rational(3, 64) * b * m**2 * T)
assert zero(
    contact[1]
    + sp.Rational(3, 256) * b * m * (3 * b * m + 8 * n) * T
)

contact_solution = {
    m: 0,
    lam: b * n**2,
    mu: -sp.Rational(3, 64) * b**4 * n**2,
}
assert all(zero(value.subs(contact_solution)) for value in contact)

# On T=0, the remaining equations still force m=0.
special_T = {c3: b**3 * c0 / 256}
special_solution = {
    **special_T,
    lam: b * n**2,
    mu: -sp.Rational(3, 64) * b**4 * n**2,
}
assert zero(
    contact[3].subs(special_solution)
    - sp.Rational(9, 16384) * b**7 * c0 * m**2
)
assert zero(
    contact[4].subs(special_solution)
    - sp.Rational(9, 8192) * b**7 * c0 * m * n
)
print("PASS every nonzero contact is f=nq")


# The r^2 part of E5 is independent of all lower integration constants.
u_full = sp.symbols("u_full0:4")
v_full = sp.symbols("v_full0:4")
w_full = sp.symbols("w_full0:3")
aa_full = sp.symbols("aa_full0:3")
bb_full = sp.symbols("bb_full0:3")
xp, xq, yp, yq = sp.symbols("xp xq yp yq")
ell_full = sp.symbols("ell_full0:9")
binary_cubic = (p**3, p**2 * q, p * q**2, q**3)
binary_quadratic = (p**2, p * q, q**2)
U0 = sum(u_full[index] * binary_cubic[index] for index in range(4))
V0 = sum(v_full[index] * binary_cubic[index] for index in range(4))
T0 = sum(w_full[index] * binary_quadratic[index] for index in range(3))
A0 = sum(aa_full[index] * binary_quadratic[index] for index in range(3))
B0 = sum(bb_full[index] * binary_quadratic[index] for index in range(3))
S_contact = tuple(value.subs(contact_solution) for value in S)
H4 = sp.Matrix((P, Q, 0))
H3_full = sp.Matrix((U0 + r * S_contact[0], V0 + r * S_contact[1], R))
H2_full = sp.Matrix(
    (
        A0 + r * (xp * p + xq * q) - b * n**2 * r**2 / 2,
        B0
        + r * (yp * p + yq * q)
        + sp.Rational(3, 128) * b**4 * n**2 * r**2,
        T0 + r * S_contact[2],
    )
)
L_full = sp.Matrix(3, 3, ell_full)
full_determinant = sp.Poly(
    sp.expand(
        (
            L_full
            + z * H2_full.jacobian(variables)
            + z**2 * H3_full.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
    p,
    q,
    r,
)
H3_top = sp.Matrix((r * S_contact[0], r * S_contact[1], R))
H2_top = sp.Matrix(
    (
        -b * n**2 * r**2 / 2,
        sp.Rational(3, 128) * b**4 * n**2 * r**2,
        r * S_contact[2],
    )
)
top_determinant = sp.Poly(
    sp.expand(
        (
            z * H2_top.jacobian(variables)
            + z**2 * H3_top.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
    p,
    q,
    r,
)
expected_E5 = (
    sp.Rational(3, 64) * b * n**3 * T,
    sp.Rational(9, 256) * b**2 * n**3 * T,
    sp.Rational(9, 1024) * b**3 * n**3 * T,
    -sp.Rational(9, 64) * b**4 * c3 * n**3,
)
for index, expected in enumerate(expected_E5):
    monomial = z**5 * p ** (3 - index) * q**index * r**2
    assert zero(top_determinant.coeff_monomial(monomial) - expected)
    assert zero(
        full_determinant.coeff_monomial(monomial)
        - top_determinant.coeff_monomial(monomial)
    )
# If T=0, then c3=b^3c0/256 is nonzero; otherwise the first
# coefficient is nonzero.
print("PASS every nonzero contact has an unavoidable E5 obstruction")


# Zero contact.  If N3!=0 the scalar E6 syzygy supplies a nonzero linear
# r coefficient in F3 and the plane-field exit applies.  On N3=0,
# normalize b=c0=1,c3=1/64 and retain every lower coefficient.
eta = sp.symbols("eta")
P0 = p * q**3
Q0 = p * (p**3 + p**2 * q + sp.Rational(3, 8) * p * q**2)
R0 = (
    p**3
    + sp.Rational(3, 4) * p**2 * q
    + sp.Rational(3, 16) * p * q**2
    + sp.Rational(1, 64) * q**3
)
N0 = (3 * p - q / 4, -sp.Rational(3, 16) * p, 0)
u0 = sp.symbols("u0:4")
v0 = sp.symbols("v0:4")
w0 = sp.symbols("w0:3")
aa0 = sp.symbols("aa0:3")
bb0 = sp.symbols("bb0:3")
ell0 = sp.symbols("ell0:9")
U_binary = sum(u0[index] * binary_cubic[index] for index in range(4))
V_binary = sum(v0[index] * binary_cubic[index] for index in range(4))
T_binary = sum(w0[index] * binary_quadratic[index] for index in range(3))
A_binary = sum(aa0[index] * binary_quadratic[index] for index in range(3))
B_binary = sum(bb0[index] * binary_quadratic[index] for index in range(3))
H4_zero = sp.Matrix((P0, Q0, 0))
H3_zero = sp.Matrix((U_binary, V_binary, R0))
H2_zero = sp.Matrix(
    (
        A_binary + eta * r * N0[0],
        B_binary + eta * r * N0[1],
        T_binary,
    )
)
L_zero = sp.Matrix(3, 3, ell0).subs(ell0[8], 0)
det_zero = sp.Poly(
    sp.expand(
        (
            L_zero
            + z * H2_zero.jacobian(variables)
            + z**2 * H3_zero.jacobian(variables)
            + z**3 * H4_zero.jacobian(variables)
        ).det()
    ),
    z,
    p,
    q,
    r,
)
det_zero_in_z = sp.Poly(det_zero.as_expr(), z)
E5_zero = sp.Poly(det_zero_in_z.coeff_monomial(z**5), p, q, r)
equations_zero = [coefficient for _, coefficient in E5_zero.terms()]
pivot_variables = (u0[0], u0[1], u0[2], v0[2], w0[0], w0[1])
solution_zero = sp.solve(equations_zero, pivot_variables, dict=True)[0]
E4_zero = sp.Poly(
    sp.expand(
        det_zero_in_z.coeff_monomial(z**4).subs(solution_zero)
    ),
    p,
    q,
    r,
)
expected_r = sp.expand(sp.Rational(9, 64) * eta**2 * R0)
actual_r = sp.Poly(E4_zero, r).coeff_monomial(r)
assert zero(actual_r - expected_r)
print("PASS exceptional zero contact is plane-field or obstructed at E4")


# The boundary b=0.  Exact gcd q^2 forces c3!=0, so scale it to one:
#
#   P=pq^3, Q=p^4, R=d p^3+q^3.
#
# First certify the complete E7 solution from an unrestricted
# r-dependent cubic/cubic/quadratic triple.
d_b0, m_b0, n_b0, rho_b0, t_b0 = sp.symbols(
    "d_b0 m_b0 n_b0 rho_b0 t_b0"
)
P_b0 = p * q**3
Q_b0 = p**4
R_b0 = d_b0 * p**3 + q**3
alpha_b0 = jac2(Q_b0, R_b0)
beta_b0 = -jac2(P_b0, R_b0)
gamma_b0 = jac2(P_b0, Q_b0)
assert sp.monic(sp.gcd(sp.gcd(alpha_b0, beta_b0), gamma_b0), q) == q**2

cubic_r_monomials = (
    p**2 * r,
    p * q * r,
    q**2 * r,
    p * r**2,
    q * r**2,
    r**3,
)
quadratic_r_monomials = (p * r, q * r, r**2)
e7_u = sp.symbols("e7u0:6")
e7_v = sp.symbols("e7v0:6")
e7_t = sp.symbols("e7t0:3")
U_e7 = sum(c * mon for c, mon in zip(e7_u, cubic_r_monomials))
V_e7 = sum(c * mon for c, mon in zip(e7_v, cubic_r_monomials))
T_e7 = sum(c * mon for c, mon in zip(e7_t, quadratic_r_monomials))
E7_general = sp.Poly(
    sp.expand(
        alpha_b0 * sp.diff(U_e7, r)
        + beta_b0 * sp.diff(V_e7, r)
        + gamma_b0 * sp.diff(T_e7, r)
    ),
    p,
    q,
    r,
)
e7_variables = e7_u + e7_v + e7_t
e7_matrix, _ = sp.linear_eq_to_matrix(
    [coefficient for _, coefficient in E7_general.terms()],
    e7_variables,
)
assert e7_matrix.rank() == 12
e7_parameterization = {
    e7_u[0]: 3 * m_b0,
    e7_u[1]: 3 * n_b0,
    e7_u[2]: 0,
    e7_u[3]: sp.Rational(3, 2) * rho_b0,
    e7_u[4]: 0,
    e7_u[5]: 0,
    **{value: 0 for value in e7_v},
    e7_t[0]: 3 * m_b0,
    e7_t[1]: 3 * n_b0,
    e7_t[2]: sp.Rational(3, 2) * rho_b0,
}
assert zero(E7_general.as_expr().subs(e7_parameterization))
parameter_columns = sp.Matrix(
    [
        [
            sp.diff(e7_parameterization[value], parameter)
            for parameter in (m_b0, n_b0, rho_b0)
        ]
        for value in e7_variables
    ]
)
assert parameter_columns.rank() == 3
print("PASS b1=0 exact gcd and complete E7 parameterization")


# Retain every lower homogeneous coefficient on the b=0 boundary.
b0_u = sp.symbols("b0u0:4")
b0_v = sp.symbols("b0v0:4")
b0_w = sp.symbols("b0w0:3")
b0_aa = sp.symbols("b0aa0:3")
b0_bb = sp.symbols("b0bb0:3")
b0_xp, b0_xq, b0_yp, b0_yq, b0_xrr, b0_yrr = sp.symbols(
    "b0_xp b0_xq b0_yp b0_yq b0_xrr b0_yrr"
)
b0_ell = sp.symbols("b0ell0:9")
b0_f0 = m_b0 * p + n_b0 * q
b0_U0 = sum(
    b0_u[index] * binary_cubic[index] for index in range(4)
)
b0_V0 = sum(
    b0_v[index] * binary_cubic[index] for index in range(4)
)
b0_T0 = sum(
    b0_w[index] * binary_quadratic[index] for index in range(3)
)
b0_A0 = sum(
    b0_aa[index] * binary_quadratic[index] for index in range(3)
)
b0_B0 = sum(
    b0_bb[index] * binary_quadratic[index] for index in range(3)
)
b0_U = (
    b0_U0
    + 3 * p * b0_f0 * r
    + sp.Rational(3, 2) * p * rho_b0 * r**2
)
b0_V = b0_V0
b0_T = (
    b0_T0
    + 3 * b0_f0 * r
    + sp.Rational(3, 2) * rho_b0 * r**2
)
b0_A = (
    b0_A0
    + r * (b0_xp * p + b0_xq * q)
    + b0_xrr * r**2
)
b0_B = (
    b0_B0
    + r * (b0_yp * p + b0_yq * q)
    + b0_yrr * r**2
)
b0_H4 = sp.Matrix((P_b0, Q_b0, 0))
b0_H3 = sp.Matrix((b0_U, b0_V, R_b0))
b0_H2 = sp.Matrix((b0_A, b0_B, b0_T))
b0_L = sp.Matrix(3, 3, b0_ell)
b0_weighted = sp.Poly(
    sp.expand(
        (
            b0_L
            + z * b0_H2.jacobian(variables)
            + z**2 * b0_H3.jacobian(variables)
            + z**3 * b0_H4.jacobian(variables)
        ).det()
    ),
    z,
)
b0_E = {
    degree: sp.Poly(
        sp.expand(b0_weighted.coeff_monomial(z**degree)), p, q, r
    )
    for degree in range(1, 9)
}
assert b0_E[8].is_zero and b0_E[7].is_zero


def b0_coeff(degree: int, ep: int, eq: int, er: int) -> sp.Expr:
    return b0_E[degree].coeff_monomial(p**ep * q**eq * r**er)


def b0_equations(polynomial: sp.Poly) -> list[sp.Expr]:
    return [coefficient for _, coefficient in polynomial.terms()]


b0_C = (
    -3 * d_b0 * b0_ell[5]
    + 3 * d_b0 * b0_ell[8] * b0_v[3]
    - 4 * b0_ell[2]
    + 4 * b0_ell[8] * b0_u[3]
)
b0_D = -b0_ell[5] + b0_ell[8] * b0_v[3]
b0_Arel = (
    -3 * d_b0 * b0_ell[4]
    + 3 * d_b0 * b0_ell[7] * b0_v[3]
    - 4 * b0_ell[1]
    + 4 * b0_ell[7] * b0_u[3]
)
b0_Brel = -b0_ell[4] + b0_ell[7] * b0_v[3]
b0_column_three = {
    b0_ell[5]: b0_ell[8] * b0_v[3],
    b0_ell[2]: b0_ell[8] * b0_u[3],
}
b0_column_two = {
    b0_ell[4]: b0_ell[7] * b0_v[3],
    b0_ell[1]: b0_ell[7] * b0_u[3],
}
assert zero(b0_L.det().subs(b0_column_three).subs(b0_column_two))


# Chart rho!=0.  Two E6 coefficients first force v1=v2=0;
# the remaining displayed substitution is the full E6 solution.
assert zero(b0_coeff(6, 2, 3, 1) - 3 * rho_b0 * b0_v[1])
assert zero(b0_coeff(6, 1, 4, 1) - 6 * rho_b0 * b0_v[2])
b0_rho_e6 = {
    b0_v[1]: 0,
    b0_v[2]: 0,
    b0_u[1]: b0_w[1],
    b0_u[2]: b0_w[2],
    b0_yp: 3 * m_b0 * b0_v[3],
    b0_yq: 3 * n_b0 * b0_v[3],
    b0_yrr: sp.Rational(3, 2) * rho_b0 * b0_v[3],
    b0_xp: b0_ell[8] + 3 * m_b0 * b0_u[3],
    b0_xq: 3 * n_b0 * b0_u[3],
    b0_xrr: sp.Rational(3, 2) * rho_b0 * b0_u[3],
}
assert all(
    zero(value.subs(b0_rho_e6)) for value in b0_equations(b0_E[6])
)
b0_rho_e5_lower = {
    b0_bb[1]: b0_v[3] * b0_w[1],
    b0_bb[2]: b0_v[3] * b0_w[2],
    b0_aa[1]: b0_ell[7] + b0_u[3] * b0_w[1],
    b0_aa[2]: b0_u[3] * b0_w[2],
}
b0_rho_e5 = sp.Poly(
    sp.expand(
        b0_E[5]
        .as_expr()
        .subs(b0_rho_e6)
        .subs(b0_rho_e5_lower)
    ),
    p,
    q,
    r,
)
assert zero(
    b0_rho_e5.as_expr()
    - (-3 * b0_C * p**3 * q**2 + 3 * b0_D * q**5)
)
b0_rho_e4 = sp.Poly(
    sp.expand(
        b0_E[4]
        .as_expr()
        .subs(b0_rho_e6)
        .subs(b0_rho_e5_lower)
        .subs(b0_column_three)
    ),
    p,
    q,
    r,
)
assert zero(
    sp.Poly(b0_rho_e4, r).coeff_monomial(r)
    - (3 * rho_b0 * b0_Arel * p**3 - 3 * rho_b0 * b0_Brel * q**3)
)
print("PASS b1=0 rho-nonzero chart forces singular linear part")


# Chart rho=0,m!=0; scale m=1 and put n=t.
b0_m_chart = {
    rho_b0: 0,
    m_b0: 1,
    n_b0: t_b0,
    b0_v[2]: -t_b0 * b0_v[1] / 2,
    b0_u[1]: b0_w[1] - sp.Rational(3, 4) * d_b0 * b0_v[1],
    b0_u[2]: (
        b0_w[2] + sp.Rational(3, 8) * d_b0 * t_b0 * b0_v[1]
    ),
    b0_yp: 3 * b0_v[3] - t_b0**2 * b0_v[1],
    b0_yq: 3 * t_b0 * b0_v[3],
    b0_xp: (
        b0_ell[8]
        + 3 * b0_u[3]
        + sp.Rational(3, 4) * d_b0 * t_b0**2 * b0_v[1]
    ),
    b0_xq: 3 * t_b0 * b0_u[3] - b0_v[1] / 4,
    b0_xrr: 0,
    b0_yrr: 0,
}
assert all(
    zero(value.subs(b0_m_chart)) for value in b0_equations(b0_E[6])
)
b0_m_e5 = sp.Poly(
    sp.expand(b0_E[5].as_expr().subs(b0_m_chart)), p, q, r
)
assert zero(b0_m_e5.coeff_monomial(p**4 * r) - 12 * b0_v[1])
b0_m_lower = {
    b0_v[1]: 0,
    b0_aa[1]: b0_ell[7] + b0_u[3] * b0_w[1],
    b0_aa[2]: b0_u[3] * b0_w[2],
    b0_bb[1]: b0_v[3] * b0_w[1],
    b0_bb[2]: b0_v[3] * b0_w[2],
}
b0_m_e5_residual = sp.Poly(
    sp.expand(b0_m_e5.as_expr().subs(b0_m_lower)), p, q, r
)
assert zero(
    b0_m_e5_residual.as_expr()
    - (-3 * b0_C * p**3 * q**2 + 3 * b0_D * q**5)
)
b0_m_e4 = sp.Poly(
    sp.expand(
        b0_E[4]
        .as_expr()
        .subs(b0_m_chart)
        .subs(b0_m_lower)
        .subs(b0_column_three)
    ),
    p,
    q,
    r,
)
assert zero(
    b0_m_e4.as_expr()
    - (
        3 * b0_Arel * p**4
        + 3 * t_b0 * b0_Arel * p**3 * q
        - 3 * b0_Brel * p * q**3
        - 3 * t_b0 * b0_Brel * q**4
    )
)
print("PASS b1=0 m-nonzero chart forces singular linear part")


# Chart rho=m=0,n!=0; scale n=1.
b0_n_chart = {
    rho_b0: 0,
    m_b0: 0,
    n_b0: 1,
    b0_v[1]: 0,
    b0_u[1]: b0_w[1],
    b0_yp: 2 * b0_v[2],
    b0_yq: 3 * b0_v[3],
    b0_xp: b0_ell[8] + 2 * b0_u[2] - 2 * b0_w[2],
    b0_xq: 3 * b0_u[3],
    b0_xrr: 0,
    b0_yrr: 0,
}
assert all(
    zero(value.subs(b0_n_chart)) for value in b0_equations(b0_E[6])
)
b0_n_e5 = sp.Poly(
    sp.expand(b0_E[5].as_expr().subs(b0_n_chart)), p, q, r
)
assert zero(b0_n_e5.coeff_monomial(p * q**3 * r) + 6 * b0_v[2])
b0_n_e5_first = {b0_v[2]: 0, b0_u[2]: b0_w[2]}
b0_n_lower = {
    b0_aa[1]: b0_ell[7] + b0_u[3] * b0_w[1],
    b0_aa[2]: (
        b0_ell[2]
        - b0_ell[8] * b0_u[3]
        + 2 * b0_u[3] * b0_w[2]
    )
    / 2,
    b0_bb[1]: b0_v[3] * b0_w[1],
    b0_bb[2]: (
        b0_ell[5]
        - b0_ell[8] * b0_v[3]
        + 2 * b0_v[3] * b0_w[2]
    )
    / 2,
}
b0_n_e5_residual = sp.Poly(
    sp.expand(
        b0_n_e5
        .as_expr()
        .subs(b0_n_e5_first)
        .subs(b0_n_lower)
    ),
    p,
    q,
    r,
)
assert b0_n_e5_residual.is_zero
b0_n_e4 = sp.Poly(
    sp.expand(
        b0_E[4]
        .as_expr()
        .subs(b0_n_chart)
        .subs(b0_n_e5_first)
        .subs(b0_n_lower)
    ),
    p,
    q,
    r,
)
assert zero(
    sp.Poly(b0_n_e4, r).coeff_monomial(r)
    - (-3 * b0_C * p**3 + 3 * b0_D * q**3)
)
b0_n_e4_columns = sp.Poly(
    sp.expand(b0_n_e4.as_expr().subs(b0_column_three)), p, q, r
)
assert zero(
    b0_n_e4_columns.as_expr()
    - (3 * b0_Arel * p**3 * q - 3 * b0_Brel * q**4)
)
print("PASS b1=0 n-nonzero chart forces singular linear part")


# Zero E7 contact.  E6 has exactly the following three pivots.
b0_zero_contact = {rho_b0: 0, m_b0: 0, n_b0: 0}
b0_zero_e6 = sp.Poly(
    sp.expand(b0_E[6].as_expr().subs(b0_zero_contact)), p, q, r
)
b0_zero_solution = sp.solve(
    b0_equations(b0_zero_e6),
    (b0_xp, b0_xq, b0_xrr, b0_yp, b0_yq, b0_yrr),
    dict=True,
)[0]
b0_zero_expected = {
    b0_xp: b0_ell[8],
    b0_xq: 0,
    b0_xrr: 0,
    b0_yp: 0,
    b0_yq: 0,
    b0_yrr: 0,
}
assert all(
    zero(b0_zero_solution[key] - value)
    for key, value in b0_zero_expected.items()
)
assert all(
    zero(value.subs(b0_zero_expected))
    for value in b0_equations(b0_zero_e6)
)
print("PASS b1=0 zero-contact E6 has the plane-field normal form")

print("ALL UNMARKED-DOUBLE {2,0} SYMPY CHECKS PASSED")
