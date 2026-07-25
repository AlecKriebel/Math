#!/usr/bin/python3
"""Exact checks for the vertical fixed-linear cubic-pencil frontier."""

from __future__ import annotations

import sympy as sp

if not __debug__:
    raise SystemExit("refusing optimized Python: assertions would be disabled")

x, y, z, tau, spectral = sp.symbols("x y z tau spectral")
variables = (x, y, z)


def homogeneous_monomials(degree: int) -> list[sp.Expr]:
    return [
        x**i * y**j * z ** (degree - i - j)
        for i in range(degree + 1)
        for j in range(degree + 1 - i)
    ]


def jacobian(a: sp.Expr, b: sp.Expr, c: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix(
            [[sp.diff(form, variable) for variable in variables] for form in (a, b, c)]
        ).det()
    )


def kernel(p: sp.Expr, q: sp.Expr, degree: int) -> list[sp.Expr]:
    monomials = homogeneous_monomials(degree)
    coefficients = sp.symbols(f"k{degree}_0:{len(monomials)}")
    candidate = sum(c * m for c, m in zip(coefficients, monomials))
    equation = sp.Poly(jacobian(z * p, z * q, candidate), *variables)
    matrix, _ = sp.linear_eq_to_matrix(equation.coeffs(), coefficients)
    return [
        sp.factor(
            sum(vector[index] * monomials[index] for index in range(len(monomials)))
        )
        for vector in matrix.nullspace()
    ]


q = x**3 + y**3
marked_members = {
    "m1_rho2_rank2": z * x * y,
    "m1_rho2_rank3": z * (x * y + z**2),
    "m1_square": z * x**2,
    "m1_binary_rank2": z * (x**2 + z**2),
    "m1_rho1_rank3": z * (x**2 + y * z),
    "m2": z**2 * x,
    "m3": z**3,
}

expected_degree_two = {
    "m1_rho2_rank2": [],
    "m1_rho2_rank3": [],
    "m1_square": [x * z],
    "m1_binary_rank2": [],
    "m1_rho1_rank3": [],
    "m2": [],
    "m3": [z**2],
}
expected_degree_three_dimensions = {
    "m1_rho2_rank2": 0,
    "m1_rho2_rank3": 0,
    "m1_square": 0,
    "m1_binary_rank2": 0,
    "m1_rho1_rank3": 0,
    "m2": 0,
    "m3": 2,
}

for label, p in marked_members.items():
    degree_two_kernel = kernel(p, q, 2)
    assert degree_two_kernel == expected_degree_two[label], (
        label,
        degree_two_kernel,
    )
    degree_three_kernel = kernel(p, q, 3)
    assert len(degree_three_kernel) == expected_degree_three_dimensions[label]
    if label == "m3":
        assert all(jacobian(z * p, z * q, form) == 0 for form in (z**3, q))
        coefficient_matrix = sp.zeros(10, 4)
        degree_three_monomials = homogeneous_monomials(3)
        for column, form in enumerate(degree_three_kernel + [z**3, q]):
            polynomial = sp.Poly(form, *variables)
            for row, monomial in enumerate(degree_three_monomials):
                coefficient_matrix[row, column] = polynomial.coeff_monomial(monomial)
        assert coefficient_matrix.rank() == 2


# Exact E7 formulas on both triple-vertical companion branches.
u_coefficients = sp.symbols("u0:10")
v_coefficients = sp.symbols("v0:10")
w_coefficients = sp.symbols("w0:6")
U_general = sum(
    coefficient * monomial
    for coefficient, monomial in zip(u_coefficients, homogeneous_monomials(3))
)
V_general = sum(
    coefficient * monomial
    for coefficient, monomial in zip(v_coefficients, homogeneous_monomials(3))
)
W_general = sum(
    coefficient * monomial
    for coefficient, monomial in zip(w_coefficients, homogeneous_monomials(2))
)


def xy_bracket(a_form: sp.Expr, b_form: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(a_form, x) * sp.diff(b_form, y)
        - sp.diff(a_form, y) * sp.diff(b_form, x)
    )


P_triple = z**4
Q_triple = z * q
e7_vertical_companion = sp.expand(
    jacobian(P_triple, Q_triple, W_general)
    + jacobian(P_triple, V_general, z**3)
    + jacobian(U_general, Q_triple, z**3)
)
assert (
    sp.expand(
        e7_vertical_companion
        - z**3 * xy_bracket(q, 4 * z * W_general - 3 * U_general)
    )
    == 0
)

e7_nonvertical_companion = sp.expand(
    jacobian(P_triple, Q_triple, W_general)
    + jacobian(P_triple, V_general, q)
    + jacobian(U_general, Q_triple, q)
)
assert (
    sp.expand(
        e7_nonvertical_companion
        - xy_bracket(q, 4 * z**4 * W_general - 4 * z**3 * V_general + q * U_general)
    )
    == 0
)


# The five m=1 representatives have exactly the advertised two ranks.
quadratic_representatives = [
    (x * y, (2, 2)),
    (x * y + z**2, (2, 3)),
    (x**2, (1, 1)),
    (x**2 + z**2, (1, 2)),
    (x**2 + y * z, (1, 3)),
]
for quadratic, expected_ranks in quadratic_representatives:
    full_matrix = sp.hessian(quadratic, variables)
    restricted_matrix = sp.hessian(quadratic.subs(z, 0), (x, y))
    assert (restricted_matrix.rank(), full_matrix.rank()) == expected_ranks


# Exact preservation by the two explicitly displayed residual stabilizers.
a, c, d, e, f = sp.symbols("a c d e f", nonzero=True)
v1, v2 = sp.symbols("v1 v2")
A11, A12, A21, A22 = sp.symbols("A11 A12 A21 A22")

triple_substitution = {
    x: A11 * x + A12 * y + v1 * z,
    y: A21 * x + A22 * y + v2 * z,
    z: c * z,
}
assert sp.expand((z**3).subs(triple_substitution, simultaneous=True) - c**3 * z**3) == 0

simple_square_substitution = {
    x: a * x,
    y: d * y + e * x + f * z,
    z: c * z,
}
assert (
    sp.expand(
        (z * x**2).subs(simple_square_substitution, simultaneous=True)
        - c * a**2 * z * x**2
    )
    == 0
)


# The two primitive E8/E7/E6 survivors.
H4 = sp.Matrix([z**4, z * q, 0])
linear_matrix = sp.eye(3)
for normal_cubic in (z**3, q):
    H3 = sp.Matrix([0, 0, normal_cubic])
    weighted_matrix = (
        linear_matrix
        + tau**2 * H3.jacobian(variables)
        + tau**3 * H4.jacobian(variables)
    )
    determinant = sp.Poly(sp.expand(weighted_matrix.det()), tau)
    assert determinant.coeff_monomial(tau**8) == 0
    assert determinant.coeff_monomial(tau**7) == 0
    assert determinant.coeff_monomial(tau**6) == 0
    assert determinant.degree() <= 5
    assert determinant.as_expr() != 1

first_survivor = sp.Poly(
    sp.expand(
        (
            linear_matrix
            + tau**2 * sp.Matrix([0, 0, z**3]).jacobian(variables)
            + tau**3 * H4.jacobian(variables)
        ).det()
    ),
    tau,
)
assert sp.factor(first_survivor.as_expr()) == (
    3 * tau**2 * z**2 + 1
) * (3 * tau**3 * y**2 * z + 1)


# A stronger vertical-companion survivor through E5.
H3_e5 = sp.Matrix([q + sp.Rational(4, 3) * z**3, 0, z**3])
H2_e5 = sp.Matrix([0, x * z, z**2])
e5_survivor = sp.Poly(
    sp.expand(
        (
            linear_matrix
            + tau * H2_e5.jacobian(variables)
            + tau**2 * H3_e5.jacobian(variables)
            + tau**3 * H4.jacobian(variables)
        ).det()
    ),
    tau,
)
assert sp.factor(e5_survivor.as_expr()) == (
    3 * tau**2 * x**2 + 1
) * (3 * tau**2 * z**2 + 2 * tau * z + 1)
for weight in (8, 7, 6, 5):
    assert e5_survivor.coeff_monomial(tau**weight) == 0
assert e5_survivor.coeff_monomial(tau**4) == 9 * x**2 * z**2


# The witness pencil is geometrically integral: its generic cubic is smooth.
generic_member = z**3 - spectral * (x**3 + y**3)
generic_gradient = [sp.diff(generic_member, variable) for variable in variables]
spectral_field = sp.QQ.frac_field(spectral)
for chart_variable in variables:
    chart_ideal = sp.groebner(
        generic_gradient + [chart_variable - 1],
        x,
        y,
        z,
        domain=spectral_field,
    )
    assert chart_ideal.polys == [sp.Poly(1, x, y, z, domain=spectral_field)]


# Exhaust the elementary congruence cases used in the proof.
for residue in range(4):
    if (6 + residue) % 4 == 0:  # m=1,d=3, h equation
        assert residue == 2
        assert all((multiplicity * (3 + residue)) % 4 for multiplicity in (1, 2))

assert all((9 + 2 * integer) % 4 != 0 for integer in range(4))

print("vertical fixed-linear cubic-pencil SymPy checks passed")
