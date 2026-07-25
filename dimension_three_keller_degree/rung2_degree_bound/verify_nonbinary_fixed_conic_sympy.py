#!/usr/bin/python3
"""Exact checks for the complete nonbinary fixed-conic reduction.

This regression verifies the general adjugate identity and the decisive
degree-seven and degree-six calculations for all five nonbinary normal
forms.  The logarithmic-valuation argument is mathematical input, not a
CAS check.
"""

from __future__ import annotations

import sympy as sp

p, q, r = sp.symbols("p q r")
variables = (p, q, r)

A = sp.Matrix([p**2, p * q, q**2])
Ap = A.diff(p)
Aq = A.diff(q)
Delta = Ap.cross(Aq)


def jacobian_map(H: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [[sp.diff(H[i], variable) for variable in variables] for i in range(3)]
    )


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.expand(entry) == 0 for entry in matrix)


# General quadratic fixed factor.
c = sp.symbols("c0:6")
h = (
    c[0] * p**2
    + c[1] * p * q
    + c[2] * q**2
    + c[3] * p * r
    + c[4] * q * r
    + c[5] * r**2
)
hr = sp.diff(h, r)
k = sp.Matrix([p * hr, q * hr, r * hr - 4 * h])
C = jacobian_map(h * A)

assert matrix_is_zero(C.adjugate() + h * k * Delta.T / 2)
assert matrix_is_zero(C * k)

Dk_Delta = Delta.jacobian(variables) * k
assert matrix_is_zero(Dk_Delta - 2 * hr * Delta)

# Check the scalar differential equation for a completely general cubic H3.
u = sp.symbols("u0:30")
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
H3_general = sp.Matrix(
    [
        sum(u[10 * i + j] * cubic_monomials[j] for j in range(10))
        for i in range(3)
    ]
)
N_general = sp.expand(Delta.dot(H3_general))
Dk_H3 = jacobian_map(H3_general) * k
Dk_N = sp.expand(sum(sp.diff(N_general, variables[j]) * k[j] for j in range(3)))
assert sp.expand(
    Dk_N - 2 * hr * N_general - Delta.dot(Dk_H3)
) == 0


# First nonbinary normal form h=r^2.
a0, a1, a2, a3, a4, a5 = sp.symbols("a0:6")
b0, b1, b2, b3, b4, b5 = sp.symbols("b0:6")
quadratic_monomials = (p**2, p * q, q**2, p * r, q * r, r**2)
f_general = sum(
    coefficient * monomial
    for coefficient, monomial in zip(
        (a0, a1, a2, a3, a4, a5), quadratic_monomials
    )
)
g_general = sum(
    coefficient * monomial
    for coefficient, monomial in zip(
        (b0, b1, b2, b3, b4, b5), quadratic_monomials
    )
)
H3_tangent_general = f_general * Ap + g_general * Aq
H4_square = r**2 * A
C_square = jacobian_map(H4_square)

f0 = sp.Poly(f_general, r).coeff_monomial(1)
f1 = sp.Poly(f_general, r).coeff_monomial(r)
g0 = sp.Poly(g_general, r).coeff_monomial(1)
g1 = sp.Poly(g_general, r).coeff_monomial(r)
R = sp.expand(q * f0 - p * g0)
S = sp.expand(q * f1 - p * g1)

normal_term = sp.expand(
    sp.trace(jacobian_map(H3_tangent_general).adjugate() * C_square)
)
normal_mod_r3 = sum(
    sp.Poly(normal_term, r).coeff_monomial(r**j) * r**j for j in range(3)
)
assert sp.expand(normal_mod_r3 - 12 * r * R**2 - 16 * r**2 * R * S) == 0

# R=0 is exactly f_0=pL and g_0=qL.  The following parametrization is
# substituted into the full degree-seven identity.
L = a0 * p + a1 * q
f = p * L + r * (a3 * p + a4 * q + a5 * r)
g = q * L + r * (b3 * p + b4 * q + b5 * r)
H3 = f * Ap + g * Aq
assert sp.expand(Delta.dot(H3)) == 0

w = [sp.Integer(0) for _ in range(18)]
w[0] = (a3 - b4) ** 2 - 2 * a4 * b3
w[1] = 2 * a4 * (a3 - b4)
w[2] = a4**2
w[5] = a5**2
w[6] = b3 * (a3 - b4)
w[11] = a5 * b5
w[12] = b3**2
w[17] = b5**2
H2 = sp.Matrix(
    [
        sum(w[6 * i + j] * quadratic_monomials[j] for j in range(6))
        for i in range(3)
    ]
)

degree_seven = sp.expand(
    sp.trace(C_square.adjugate() * jacobian_map(H2))
    + sp.trace(jacobian_map(H3).adjugate() * C_square)
)
assert degree_seven == 0

# Affine translations in p,q shift (a5,b5) arbitrarily.
xi, eta = sp.symbols("xi eta")
translation_cubic = xi * H4_square.diff(p) + eta * H4_square.diff(q)
assert matrix_is_zero(translation_cubic - r**2 * (xi * Ap + eta * Aq))

# After normalizing a5=b5=0, retain the complete affine kernel of the
# degree-seven H2 equation and check the parameter-free degree-six exit.
ell_p, ell_q, m_p, m_q = sp.symbols("ell_p ell_q m_p m_q")
kernel_u = sp.symbols("kernel_u0:6")
ell = ell_p * p + ell_q * q
m_form = m_p * p + m_q * q
H3_normalized = H3.subs({a5: 0, b5: 0})
H2_base = H2.subs({a5: 0, b5: 0})
H2_full = (
    H2_base
    + ell * Ap
    + m_form * Aq
    + r
    * sp.Matrix(
        [
            kernel_u[0] * p + kernel_u[1] * q,
            kernel_u[2] * p + kernel_u[3] * q,
            kernel_u[4] * p + kernel_u[5] * q,
        ]
    )
)
degree_seven_full = sp.expand(
    sp.trace(C_square.adjugate() * jacobian_map(H2_full))
    + sp.trace(jacobian_map(H3_normalized).adjugate() * C_square)
)
assert degree_seven_full == 0

linear_symbols = sp.symbols("linear0:9")
linear_part = sp.Matrix(3, 3, linear_symbols)
scale = sp.symbols("scale")
weighted = sp.expand(
    (
        linear_part
        + scale * jacobian_map(H2_full)
        + scale**2 * jacobian_map(H3_normalized)
        + scale**3 * C_square
    ).det()
)
degree_six = sp.Poly(weighted, scale).coeff_monomial(scale**6)
degree_six_poly = sp.Poly(degree_six, p, q, r)
assert sp.expand(
    degree_six_poly.coeff_monomial(p**2 * r**4)
    - 2 * linear_symbols[8]
) == 0
assert sp.expand(
    degree_six_poly.coeff_monomial(p * q * r**4)
    + 4 * linear_symbols[5]
) == 0
assert sp.expand(
    degree_six_poly.coeff_monomial(q**2 * r**4)
    - 2 * linear_symbols[2]
) == 0


# Second normal form h=r^2+p^2: raw degree-seven compatibility.
fa = sp.symbols("fa0:6")
gb = sp.symbols("gb0:6")
h_plus = r**2 + p**2
H4_plus = h_plus * A
C_plus = jacobian_map(H4_plus)
f_plus_general = sum(
    fa[j] * quadratic_monomials[j] for j in range(6)
)
g_plus_general = sum(
    gb[j] * quadratic_monomials[j] for j in range(6)
)
H3_plus_general = f_plus_general * Ap + g_plus_general * Aq
raw_w = sp.symbols("raw_w0:18")
H2_plus_general = sp.Matrix(
    [
        sum(
            raw_w[6 * i + j] * quadratic_monomials[j]
            for j in range(6)
        )
        for i in range(3)
    ]
)
degree_seven_plus = sp.expand(
    sp.trace(C_plus.adjugate() * jacobian_map(H2_plus_general))
    + sp.trace(jacobian_map(H3_plus_general).adjugate() * C_plus)
)
plus_equations = [
    coefficient
    for _, coefficient in sp.Poly(
        degree_seven_plus, p, q, r
    ).terms()
]
plus_matrix, plus_rhs = sp.linear_eq_to_matrix(
    plus_equations, list(raw_w)
)
assert plus_matrix.rank() == 12
plus_compatibility = [
    sp.factor((vector.T * plus_rhs)[0])
    for vector in plus_matrix.T.nullspace()
]


def contains_constant_multiple(
    expressions: list[sp.Expr], target: sp.Expr
) -> bool:
    for expression in expressions:
        quotient = sp.cancel(expression / target)
        if quotient.is_number and quotient != 0:
            return True
    return False


assert contains_constant_multiple(plus_compatibility, fa[2] ** 2)
after_a2 = [sp.factor(item.subs({fa[2]: 0})) for item in plus_compatibility]
assert contains_constant_multiple(
    after_a2, fa[4] * (fa[1] - gb[2])
)
assert contains_constant_multiple(
    after_a2, (fa[1] - gb[2]) ** 2 - fa[4] ** 2
)
assert contains_constant_multiple(
    plus_compatibility, gb[3] * (gb[0] - gb[5])
)
assert contains_constant_multiple(
    plus_compatibility, (gb[0] - gb[5]) ** 2 - gb[3] ** 2
)
forced_plus = {
    fa[2]: 0,
    fa[4]: 0,
    gb[3]: 0,
    gb[2]: fa[1],
    gb[5]: gb[0],
}
after_first_relations = [
    sp.factor(item.subs(forced_plus)) for item in plus_compatibility
]
plus_x = fa[3] - gb[4]
plus_y = fa[0] - fa[5] - gb[1]
assert contains_constant_multiple(
    after_first_relations, plus_x * plus_y
)
assert contains_constant_multiple(
    after_first_relations, plus_y**2 - plus_x**2
)
final_plus = {
    **forced_plus,
    fa[3]: gb[4],
    fa[0]: fa[5] + gb[1],
}
assert all(
    sp.expand(item.subs(final_plus)) == 0
    for item in plus_compatibility
)

# Translation-normalized degree-seven and degree-six endgame.
xp, yq = sp.symbols("xp yq")
plus_u = sp.symbols("plus_u0:6")
H3_plus = 2 * (xp * p + yq * q) * A
H2_plus = sp.Matrix(
    [
        (-plus_u[4] + 2 * plus_u[0]) * p**2
        + 2 * plus_u[1] * p * q
        + 2 * plus_u[2] * p * r,
        plus_u[3] * p**2 / 2
        + plus_u[0] * p * q
        + plus_u[1] * q**2
        + plus_u[5] * p * r / 2
        + plus_u[2] * q * r,
        plus_u[3] * p * q
        + plus_u[4] * q**2
        + plus_u[5] * q * r,
    ]
)
assert sp.expand(
    sp.trace(C_plus.adjugate() * jacobian_map(H2_plus))
    + sp.trace(jacobian_map(H3_plus).adjugate() * C_plus)
) == 0
weighted_plus = sp.expand(
    (
        linear_part
        + scale * jacobian_map(H2_plus)
        + scale**2 * jacobian_map(H3_plus)
        + scale**3 * C_plus
    ).det()
)
degree_six_plus = sp.Poly(
    sp.Poly(weighted_plus, scale).coeff_monomial(scale**6),
    p,
    q,
    r,
)
plus_expected = {
    p**6: 4 * linear_symbols[8],
    p**5 * q: -8 * linear_symbols[5],
    p**5 * r: -2 * linear_symbols[6],
    p**4 * q**2: 4 * linear_symbols[2],
    p**4 * q * r: 2 * (2 * linear_symbols[3] - linear_symbols[7]),
    p**3 * q**2 * r: -2 * (
        linear_symbols[0] - 2 * linear_symbols[4]
    ),
    p**2 * q**3 * r: -2 * linear_symbols[1],
}
for monomial, expected in plus_expected.items():
    assert sp.expand(
        degree_six_plus.coeff_monomial(monomial) - expected
    ) == 0


# Third normal form h=pr: raw degree-seven radical and triangular exit.
fpr = sp.symbols("fpr0:6")
gpr = sp.symbols("gpr0:6")
H4_pr = p * r * A
C_pr = jacobian_map(H4_pr)
H3_pr_general = (
    sum(fpr[j] * quadratic_monomials[j] for j in range(6)) * Ap
    + sum(gpr[j] * quadratic_monomials[j] for j in range(6)) * Aq
)
pr_w = sp.symbols("pr_w0:18")
H2_pr_general = sp.Matrix(
    [
        sum(
            pr_w[6 * i + j] * quadratic_monomials[j]
            for j in range(6)
        )
        for i in range(3)
    ]
)
degree_seven_pr = sp.expand(
    sp.trace(C_pr.adjugate() * jacobian_map(H2_pr_general))
    + sp.trace(jacobian_map(H3_pr_general).adjugate() * C_pr)
)
pr_equations = [
    coefficient
    for _, coefficient in sp.Poly(
        degree_seven_pr, p, q, r
    ).terms()
]
pr_matrix, pr_rhs = sp.linear_eq_to_matrix(
    pr_equations, list(pr_w)
)
assert pr_matrix.rank() == 12
pr_compatibility = [
    sp.factor((vector.T * pr_rhs)[0])
    for vector in pr_matrix.T.nullspace()
]
assert contains_constant_multiple(pr_compatibility, gpr[0] ** 2)
after_g0 = [
    sp.factor(item.subs({gpr[0]: 0})) for item in pr_compatibility
]
assert contains_constant_multiple(after_g0, (fpr[0] - gpr[1]) ** 2)
assert contains_constant_multiple(pr_compatibility, fpr[2] ** 2)
assert contains_constant_multiple(pr_compatibility, fpr[5] ** 2)
assert contains_constant_multiple(pr_compatibility, gpr[5] ** 2)
after_f2 = [
    sp.factor(item.subs({fpr[2]: 0})) for item in pr_compatibility
]
assert contains_constant_multiple(after_f2, (fpr[1] - gpr[2]) ** 2)
assert contains_constant_multiple(after_f2, fpr[4] ** 2)
pr_relations = {
    gpr[0]: 0,
    fpr[0]: gpr[1],
    fpr[1]: gpr[2],
    fpr[2]: 0,
    fpr[4]: 0,
    fpr[5]: 0,
    gpr[5]: 0,
}
assert all(
    sp.expand(item.subs(pr_relations)) == 0
    for item in pr_compatibility
)

zr = sp.symbols("zr")
H3_pr = 2 * (xp * p + yq * q + zr * r) * A
assert sp.expand(
    sp.trace(C_pr.adjugate() * jacobian_map(H2_plus))
    + sp.trace(jacobian_map(H3_pr).adjugate() * C_pr)
) == 0
weighted_pr = sp.expand(
    (
        linear_part
        + scale * jacobian_map(H2_plus)
        + scale**2 * jacobian_map(H3_pr)
        + scale**3 * C_pr
    ).det()
)
degree_six_pr = sp.Poly(
    sp.Poly(weighted_pr, scale).coeff_monomial(scale**6),
    p,
    q,
    r,
)
pr_expected = {
    p**5 * r: -linear_symbols[6],
    p**4 * q * r: 2 * linear_symbols[3] - linear_symbols[7],
    p**4 * r**2: 3 * linear_symbols[8],
    p**3 * q**2 * r: -linear_symbols[0] + 2 * linear_symbols[4],
    p**3 * q * r**2: -6 * linear_symbols[5],
    p**2 * q**3 * r: -linear_symbols[1],
    p**2 * q**2 * r**2: 3 * linear_symbols[2],
}
assert len(degree_six_pr.terms()) == len(pr_expected)
for monomial, expected in pr_expected.items():
    assert sp.expand(
        degree_six_pr.coeff_monomial(monomial) - expected
    ) == 0


# Third listed orbit h=r^2+pq.
frp = sp.symbols("frp0:6")
grp = sp.symbols("grp0:6")
H4_rp = (r**2 + p * q) * A
C_rp = jacobian_map(H4_rp)
H3_rp_general = (
    sum(frp[j] * quadratic_monomials[j] for j in range(6)) * Ap
    + sum(grp[j] * quadratic_monomials[j] for j in range(6)) * Aq
)
rp_w = sp.symbols("rp_w0:18")
H2_rp_general = sp.Matrix(
    [
        sum(
            rp_w[6 * i + j] * quadratic_monomials[j]
            for j in range(6)
        )
        for i in range(3)
    ]
)
degree_seven_rp = sp.expand(
    sp.trace(C_rp.adjugate() * jacobian_map(H2_rp_general))
    + sp.trace(jacobian_map(H3_rp_general).adjugate() * C_rp)
)
rp_equations = [
    coefficient
    for _, coefficient in sp.Poly(
        degree_seven_rp, p, q, r
    ).terms()
]
rp_matrix, rp_rhs = sp.linear_eq_to_matrix(
    rp_equations, list(rp_w)
)
assert rp_matrix.rank() == 12
rp_compatibility = [
    sp.factor((vector.T * rp_rhs)[0])
    for vector in rp_matrix.T.nullspace()
]
assert contains_constant_multiple(rp_compatibility, grp[0] ** 2)
after_grp0 = [
    sp.factor(item.subs({grp[0]: 0})) for item in rp_compatibility
]
assert contains_constant_multiple(after_grp0, grp[3] ** 2)
assert contains_constant_multiple(rp_compatibility, frp[2] ** 2)
after_frp2 = [
    sp.factor(item.subs({frp[2]: 0})) for item in rp_compatibility
]
assert contains_constant_multiple(after_frp2, frp[4] ** 2)
rp_first = {grp[0]: 0, grp[3]: 0, frp[2]: 0, frp[4]: 0}
rp_after = [
    sp.factor(item.subs(rp_first)) for item in rp_compatibility
]
rp_x = frp[0] - grp[1] + grp[5]
rp_y = frp[1] - frp[5] - grp[2]
rp_z = frp[3] - grp[4]
assert contains_constant_multiple(rp_after, rp_x**2)
assert contains_constant_multiple(rp_after, rp_y**2)
assert contains_constant_multiple(rp_after, 2 * rp_x * rp_y - rp_z**2)
rp_relations = {
    **rp_first,
    frp[0]: grp[1] - grp[5],
    frp[1]: frp[5] + grp[2],
    frp[3]: grp[4],
}
assert all(
    sp.expand(item.subs(rp_relations)) == 0
    for item in rp_compatibility
)

H3_rp = 2 * (xp * p + yq * q + zr * r) * A
assert sp.expand(
    sp.trace(C_rp.adjugate() * jacobian_map(H2_plus))
    + sp.trace(jacobian_map(H3_rp).adjugate() * C_rp)
) == 0
weighted_rp = sp.expand(
    (
        linear_part
        + scale * jacobian_map(H2_plus)
        + scale**2 * jacobian_map(H3_rp)
        + scale**3 * C_rp
    ).det()
)
degree_six_rp = sp.Poly(
    sp.Poly(weighted_rp, scale).coeff_monomial(scale**6),
    p,
    q,
    r,
)
rp_expected = {
    p**4 * q**2: 4 * linear_symbols[8],
    p**4 * q * r: -2 * linear_symbols[6],
    p**3 * q**3: -8 * linear_symbols[5],
    p**3 * q**2 * r: 2 * (
        2 * linear_symbols[3] - linear_symbols[7]
    ),
    p**2 * q**4: 4 * linear_symbols[2],
    p**2 * q**3 * r: -2 * (
        linear_symbols[0] - 2 * linear_symbols[4]
    ),
    p * q**4 * r: -2 * linear_symbols[1],
}
for monomial, expected in rp_expected.items():
    assert sp.expand(
        degree_six_rp.coeff_monomial(monomial) - expected
    ) == 0


# Fifth normal form h=pr+q^2.
fpq = sp.symbols("fpq0:6")
gpq = sp.symbols("gpq0:6")
H4_pq = (p * r + q**2) * A
C_pq = jacobian_map(H4_pq)
H3_pq_general = (
    sum(fpq[j] * quadratic_monomials[j] for j in range(6)) * Ap
    + sum(gpq[j] * quadratic_monomials[j] for j in range(6)) * Aq
)
pq_w = sp.symbols("pq_w0:18")
H2_pq_general = sp.Matrix(
    [
        sum(
            pq_w[6 * i + j] * quadratic_monomials[j]
            for j in range(6)
        )
        for i in range(3)
    ]
)
degree_seven_pq = sp.expand(
    sp.trace(C_pq.adjugate() * jacobian_map(H2_pq_general))
    + sp.trace(jacobian_map(H3_pq_general).adjugate() * C_pq)
)
pq_equations = [
    coefficient
    for _, coefficient in sp.Poly(
        degree_seven_pq, p, q, r
    ).terms()
]
pq_matrix, pq_rhs = sp.linear_eq_to_matrix(
    pq_equations, list(pq_w)
)
assert pq_matrix.rank() == 12
pq_compatibility = [
    sp.factor((vector.T * pq_rhs)[0])
    for vector in pq_matrix.T.nullspace()
]
assert contains_constant_multiple(pq_compatibility, gpq[0] ** 2)
assert contains_constant_multiple(pq_compatibility, fpq[5] ** 2)
assert contains_constant_multiple(pq_compatibility, gpq[5] ** 2)
pq_first = {gpq[0]: 0, fpq[5]: 0, gpq[5]: 0}
pq_after = [
    sp.factor(item.subs(pq_first)) for item in pq_compatibility
]
assert contains_constant_multiple(pq_after, (fpq[0] - gpq[1]) ** 2)
assert contains_constant_multiple(pq_after, fpq[4] ** 2)
pq_x = fpq[1] - gpq[2] + gpq[3]
pq_y = fpq[2] - fpq[3] + gpq[4]
pq_second = {
    **pq_first,
    fpq[0]: gpq[1],
    fpq[4]: 0,
}
pq_after_second = [
    sp.factor(item.subs(pq_second)) for item in pq_compatibility
]
assert contains_constant_multiple(pq_after_second, pq_x**2)
assert contains_constant_multiple(pq_after_second, pq_y**2)
pq_relations = {
    **pq_second,
    fpq[1]: gpq[2] - gpq[3],
    fpq[2]: fpq[3] - gpq[4],
}
assert all(
    sp.expand(item.subs(pq_relations)) == 0
    for item in pq_compatibility
)

H3_pq = 2 * (xp * p + yq * q + zr * r) * A
assert sp.expand(
    sp.trace(C_pq.adjugate() * jacobian_map(H2_plus))
    + sp.trace(jacobian_map(H3_pq).adjugate() * C_pq)
) == 0
weighted_pq = sp.expand(
    (
        linear_part
        + scale * jacobian_map(H2_plus)
        + scale**2 * jacobian_map(H3_pq)
        + scale**3 * C_pq
    ).det()
)
degree_six_pq = sp.Poly(
    sp.Poly(weighted_pq, scale).coeff_monomial(scale**6),
    p,
    q,
    r,
)
pq_expected = {
    p**5 * r: -linear_symbols[6],
    p**4 * q * r: 2 * linear_symbols[3] - linear_symbols[7],
    p**4 * r**2: 3 * linear_symbols[8],
    p**3 * q * r**2: -6 * linear_symbols[5],
    p**2 * q**2 * r**2: 3 * linear_symbols[2],
    p**3 * q**2 * r: -linear_symbols[0]
    + 2 * linear_symbols[4]
    + 7 * linear_symbols[8],
    p**2 * q**3 * r: -linear_symbols[1]
    - 14 * linear_symbols[5],
}
for monomial, expected in pq_expected.items():
    assert sp.expand(
        degree_six_pq.coeff_monomial(monomial) - expected
    ) == 0

print("nonbinary fixed-conic SymPy checks passed")
