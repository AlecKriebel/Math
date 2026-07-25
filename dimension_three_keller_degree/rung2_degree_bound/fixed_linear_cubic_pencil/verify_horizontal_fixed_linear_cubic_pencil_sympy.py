#!/usr/bin/python3
"""Exact checks for the horizontal fixed-linear cubic-pencil theorem."""

from __future__ import annotations

import sympy as sp

if not __debug__:
    raise SystemExit("refusing optimized Python: exact assertions would be disabled")

x, y, z, tau, spectral = sp.symbols("x y z tau spectral")
variables = (x, y, z)


def gradient(form: sp.Expr) -> sp.Matrix:
    return sp.Matrix([sp.diff(form, variable) for variable in variables])


def jacobian(form1: sp.Expr, form2: sp.Expr, form3: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix(
            [
                [sp.diff(form1, variable) for variable in variables],
                [sp.diff(form2, variable) for variable in variables],
                [sp.diff(form3, variable) for variable in variables],
            ]
        ).det()
    )


def homogeneous_monomials(degree: int) -> list[sp.Expr]:
    return [
        x**i * y**j * z ** (degree - i - j)
        for i in range(degree + 1)
        for j in range(degree + 1 - i)
    ]


def invariant_kernel(
    leading_first: sp.Expr, leading_second: sp.Expr, degree: int
) -> list[sp.Expr]:
    monomials = homogeneous_monomials(degree)
    coefficients = sp.symbols(f"k{degree}_0:{len(monomials)}")
    candidate = sum(
        coefficient * monomial
        for coefficient, monomial in zip(coefficients, monomials)
    )
    equation = sp.Poly(
        jacobian(leading_first, leading_second, candidate), x, y, z
    )
    matrix, _ = sp.linear_eq_to_matrix(equation.coeffs(), coefficients)
    return [
        sp.expand(
            sum(vector[index] * monomials[index] for index in range(len(monomials)))
        )
        for vector in matrix.nullspace()
    ]


# Universal derivation identities for a general linear h and two general cubics.
linear_coefficients = sp.symbols("h0:3")
cubic_monomials = homogeneous_monomials(3)
p_coefficients = sp.symbols("p0:10")
q_coefficients = sp.symbols("q0:10")

h_general = sum(
    coefficient * variable
    for coefficient, variable in zip(linear_coefficients, variables)
)
p_general = sum(
    coefficient * monomial
    for coefficient, monomial in zip(p_coefficients, cubic_monomials)
)
q_general = sum(
    coefficient * monomial
    for coefficient, monomial in zip(q_coefficients, cubic_monomials)
)
P_general = sp.expand(h_general * p_general)
Q_general = sp.expand(h_general * q_general)
derivation_vector = gradient(P_general).cross(gradient(Q_general))
small_jacobian = jacobian(p_general, q_general, h_general)

assert (
    sp.expand(derivation_vector.dot(gradient(h_general)) - h_general**2 * small_jacobian)
    == 0
)
assert (
    sp.expand(
        derivation_vector.dot(gradient(p_general))
        + h_general * p_general * small_jacobian
    )
    == 0
)
assert (
    sp.expand(
        derivation_vector.dot(gradient(q_general))
        + h_general * q_general * small_jacobian
    )
    == 0
)
assert sp.expand(derivation_vector.dot(gradient(P_general))) == 0
assert sp.expand(derivation_vector.dot(gradient(Q_general))) == 0


# Formal 3-by-3 matrix bookkeeping for the E8 and E7 weights.
linear_entries = sp.symbols("l0:9")
quadratic_entries = sp.symbols("a0:9")
cubic_entries = sp.symbols("b0:9")
leading_entries = sp.symbols("c0:6")

linear_matrix = sp.Matrix(3, 3, linear_entries)
quadratic_matrix = sp.Matrix(3, 3, quadratic_entries)
cubic_matrix = sp.Matrix(3, 3, cubic_entries)
leading_matrix = sp.Matrix(
    [
        leading_entries[0:3],
        leading_entries[3:6],
        (0, 0, 0),
    ]
)
weighted = sp.Poly(
    sp.expand(
        (
            linear_matrix
            + tau * quadratic_matrix
            + tau**2 * cubic_matrix
            + tau**3 * leading_matrix
        ).det()
    ),
    tau,
)
expected_e8 = sp.trace(leading_matrix.adjugate() * cubic_matrix)
assert sp.expand(weighted.coeff_monomial(tau**8) - expected_e8) == 0

cubic_zero_normal = cubic_matrix.copy()
cubic_zero_normal[2, 0] = 0
cubic_zero_normal[2, 1] = 0
cubic_zero_normal[2, 2] = 0
weighted_zero_normal = sp.Poly(
    sp.expand(
        (
            linear_matrix
            + tau * quadratic_matrix
            + tau**2 * cubic_zero_normal
            + tau**3 * leading_matrix
        ).det()
    ),
    tau,
)
expected_e7 = sp.trace(leading_matrix.adjugate() * quadratic_matrix)
assert sp.expand(weighted_zero_normal.coeff_monomial(tau**7) - expected_e7) == 0
assert sp.expand(sp.trace(cubic_zero_normal.adjugate() * leading_matrix)) == 0


# A concrete primitive horizontal Hesse pencil.
h_horizontal = x + 2 * y + 3 * z
p_horizontal = x**3 + y**3 + z**3
q_horizontal = x * y * z
P_horizontal = sp.expand(h_horizontal * p_horizontal)
Q_horizontal = sp.expand(h_horizontal * q_horizontal)

# Restriction to h=0 has rank two, so h divides no pencil member.
restriction = {z: -(x + 2 * y) / 3}
restricted_p = sp.Poly(sp.expand(p_horizontal.subs(restriction)), x, y)
restricted_q = sp.Poly(sp.expand(q_horizontal.subs(restriction)), x, y)
binary_basis = (x**3, x**2 * y, x * y**2, y**3)
restriction_matrix = sp.Matrix(
    [
        [restricted_p.coeff_monomial(monomial) for monomial in binary_basis],
        [restricted_q.coeff_monomial(monomial) for monomial in binary_basis],
    ]
)
assert restriction_matrix.rank() == 2
assert invariant_kernel(P_horizontal, Q_horizontal, 2) == []
assert invariant_kernel(P_horizontal, Q_horizontal, 3) == []


# The generic Hesse member is smooth away from its finite discriminant.
hesse_member = p_horizontal - spectral * q_horizontal
hesse_gradient = [sp.diff(hesse_member, variable) for variable in variables]
spectral_field = sp.QQ.frac_field(spectral)
for projective_chart in variables:
    chart_ideal = sp.groebner(
        hesse_gradient + [projective_chart - 1],
        x,
        y,
        z,
        domain=spectral_field,
    )
    assert chart_ideal.polys == [sp.Poly(1, x, y, z, domain=spectral_field)]


# A primitive m=1 vertical example with a quadratic invariant.
h_vertical_simple = z
p_vertical_simple = z * x**2
q_vertical_simple = x**3 + y**3
P_vertical_simple = sp.expand(h_vertical_simple * p_vertical_simple)
Q_vertical_simple = sp.expand(h_vertical_simple * q_vertical_simple)
G2_vertical_simple = x * z
assert P_vertical_simple == G2_vertical_simple**2
assert jacobian(P_vertical_simple, Q_vertical_simple, G2_vertical_simple) == 0
assert sp.gcd(x**2, x**3 + y**3) == 1


# A primitive m=3 vertical example with cubic and quadratic invariants.
p_vertical_triple = z**3
q_vertical_triple = x**3 + y**3
P_vertical_triple = z**4
Q_vertical_triple = z * q_vertical_triple
assert jacobian(P_vertical_triple, Q_vertical_triple, z**3) == 0
assert jacobian(P_vertical_triple, Q_vertical_triple, z**2) == 0

generic_triple_fibre = z**3 - spectral * (x**3 + y**3)
triple_gradient_ideal = [
    sp.diff(generic_triple_fibre, variable) for variable in variables
]
assert triple_gradient_ideal == [
    -3 * spectral * x**2,
    -3 * spectral * y**2,
    3 * z**2,
]
for projective_chart in variables:
    chart_ideal = sp.groebner(
        triple_gradient_ideal + [projective_chart - 1],
        x,
        y,
        z,
        domain=spectral_field,
    )
    assert chart_ideal.polys == [sp.Poly(1, x, y, z, domain=spectral_field)]

print("horizontal fixed-linear cubic-pencil SymPy checks passed")
