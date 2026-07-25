#!/usr/bin/python3
"""Exact checks for WORKING_SCALAR_ALIGNED_CUSPIDAL_CUBIC_EXIT.md."""

from __future__ import annotations

import sympy as sp

p, q, r, scale = sp.symbols("p q r scale")
variables = (p, q, r)


def jacobian_map(H: sp.Matrix) -> sp.Matrix:
    return H.jacobian(variables)


def coefficient_system(
    polynomial: sp.Expr, unknowns: list[sp.Symbol]
) -> tuple[sp.Matrix, sp.Matrix, sp.Poly]:
    poly = sp.Poly(sp.expand(polynomial), p, q, r)
    matrix, rhs = sp.linear_eq_to_matrix(poly.coeffs(), unknowns)
    return matrix, rhs, poly


def compatibility_list(matrix: sp.Matrix, rhs: sp.Matrix) -> list[sp.Expr]:
    return [
        sp.factor((vector.T * rhs)[0])
        for vector in matrix.T.nullspace()
    ]


def contains_constant_multiple(
    expressions: list[sp.Expr], target: sp.Expr
) -> bool:
    for expression in expressions:
        quotient = sp.cancel(expression / target)
        if quotient.is_number and quotient != 0:
            return True
    return False


def all_zero_after(
    expressions: list[sp.Expr], substitution: dict[sp.Symbol, sp.Expr]
) -> bool:
    return all(
        sp.expand(expression.subs(substitution)) == 0
        for expression in expressions
    )


A = sp.Matrix([p**2 * q, p**3, q**3])
Ap = A.diff(p)
Aq = A.diff(q)
S = sp.Matrix([2 * q, 3 * p, 0])
T = sp.Matrix([p**2, 0, 3 * q**2])
N = sp.Matrix([3 * p * q**2, -2 * q**3, -p**3])

assert S.cross(T) == 3 * N

leading_forms = {
    "cusp": p,
    "flex": q,
    "general": p + q,
}
expected_normal_factors = {
    "cusp": 4 * p**3,
    "flex": 4 * p * q**2,
    "general": 4 * p * (p + q) ** 2,
}
for name, h in leading_forms.items():
    B_leading = h * A
    assert all(
        sp.expand(entry) == 0
        for entry in (
            B_leading.diff(p).cross(B_leading.diff(q))
            - expected_normal_factors[name] * N
        )
    )

# Complete degree-eight tangent family.
binary_cubic_monomials = (p**3, p**2 * q, p * q**2, q**3)
v = sp.symbols("v0:12")
V = sp.Matrix(
    [
        sum(v[4 * component + j] * binary_cubic_monomials[j]
            for j in range(4))
        for component in range(3)
    ]
)
alpha, beta, gamma, delta = sp.symbols(
    "alpha beta gamma delta"
)
H3_top = (
    V
    + r * ((alpha * p + beta * q) * S + gamma * T)
    + delta * r**2 * S
)
assert sp.expand(N.dot(H3_top.diff(r))) == 0

quadratic_monomials = (p**2, p * q, p * r, q**2, q * r, r**2)
w = sp.symbols("w0:18")
H2_general = sp.Matrix(
    [
        sum(w[6 * component + j] * quadratic_monomials[j]
            for j in range(6))
        for component in range(3)
    ]
)


def degree_seven(H4: sp.Matrix, H3: sp.Matrix, H2: sp.Matrix) -> sp.Expr:
    C = jacobian_map(H4)
    return sp.expand(
        sp.trace(C.adjugate() * jacobian_map(H2))
        + sp.trace(jacobian_map(H3).adjugate() * C)
    )


# Raw degree-seven systems and their specialization-safe branch trees.
raw_data: dict[str, tuple[sp.Matrix, sp.Matrix, list[sp.Expr]]] = {}
for name, h in leading_forms.items():
    matrix, rhs, _ = coefficient_system(
        degree_seven(h * A, H3_top, H2_general), list(w)
    )
    assert matrix.rank() == 8
    raw_data[name] = (matrix, rhs, compatibility_list(matrix, rhs))

# h=p.
cusp_compatibility = raw_data["cusp"][2]
assert contains_constant_multiple(cusp_compatibility, delta**2)
cusp_after_delta = [
    sp.factor(item.subs({delta: 0})) for item in cusp_compatibility
]
assert contains_constant_multiple(cusp_after_delta, gamma**2)
assert contains_constant_multiple(cusp_after_delta, beta**2)
cusp_reduced = [
    sp.factor(item.subs({beta: 0, gamma: 0, delta: 0}))
    for item in cusp_compatibility
]
assert contains_constant_multiple(
    cusp_reduced, alpha * (9 * v[3] + 2 * v[6])
)
assert contains_constant_multiple(cusp_reduced, alpha * v[7])
assert all_zero_after(
    cusp_compatibility,
    {alpha: 0, beta: 0, gamma: 0, delta: 0},
)
assert all_zero_after(
    cusp_compatibility,
    {
        beta: 0,
        gamma: 0,
        delta: 0,
        v[6]: -sp.Rational(9, 2) * v[3],
        v[7]: 0,
    },
)

# h=q.
flex_compatibility = raw_data["flex"][2]
assert contains_constant_multiple(flex_compatibility, delta**2)
flex_after_delta = [
    sp.factor(item.subs({delta: 0})) for item in flex_compatibility
]
assert contains_constant_multiple(flex_after_delta, beta**2)
flex_reduced = [
    sp.factor(item.subs({beta: 0, delta: 0}))
    for item in flex_compatibility
]
assert contains_constant_multiple(flex_reduced, alpha * gamma)
assert contains_constant_multiple(flex_reduced, gamma * v[8])
assert contains_constant_multiple(
    flex_reduced, 12 * alpha * v[8] + gamma * v[9]
)
assert all_zero_after(
    flex_compatibility,
    {alpha: 0, beta: 0, gamma: 0, delta: 0},
)
assert all_zero_after(
    flex_compatibility,
    {beta: 0, gamma: 0, delta: 0, v[8]: 0},
)
assert all_zero_after(
    flex_compatibility,
    {
        alpha: 0,
        beta: 0,
        delta: 0,
        v[8]: 0,
        v[9]: 0,
    },
)

# h=p+q.
general_compatibility = raw_data["general"][2]
assert contains_constant_multiple(general_compatibility, delta**2)
general_after_delta = [
    sp.factor(item.subs({delta: 0})) for item in general_compatibility
]
assert contains_constant_multiple(general_after_delta, gamma**2)
assert contains_constant_multiple(general_after_delta, beta**2)
general_reduced = [
    sp.factor(item.subs({beta: 0, gamma: 0, delta: 0}))
    for item in general_compatibility
]
assert contains_constant_multiple(general_reduced, alpha**2)
assert all_zero_after(
    general_compatibility,
    {alpha: 0, beta: 0, gamma: 0, delta: 0},
)

# Binary-cubic leaves: complete H2 family.
binary_quadratic_monomials = (p**2, p * q, q**2)
bcoef = sp.symbols("bcoef0:9")
B2 = sp.Matrix(
    [
        sum(bcoef[3 * component + j] * binary_quadratic_monomials[j]
            for j in range(3))
        for component in range(3)
    ]
)
kappa = sp.symbols("kappa")
H2_binary = B2 + kappa * r * S

for h in leading_forms.values():
    assert degree_seven(h * A, V, H2_binary) == 0

    matrix, rhs, _ = coefficient_system(
        degree_seven(h * A, V, H2_general), list(w)
    )
    assert matrix.rank() == 8
    assert matrix.row_join(rhs).rank() == 8

binary_family_coefficients = []
for component in H2_binary:
    poly = sp.Poly(component, p, q, r)
    binary_family_coefficients.extend(
        poly.coeff_monomial(monomial) for monomial in quadratic_monomials
    )
assert sp.Matrix(binary_family_coefficients).jacobian(
    (*bcoef, kappa)
).rank() == 10

linear_symbols = sp.symbols("linear0:9")
L0 = sp.Matrix(3, 3, linear_symbols)


def determinant_polynomial(
    H4: sp.Matrix, H3: sp.Matrix, H2: sp.Matrix
) -> sp.Poly:
    return sp.Poly(
        sp.expand(
            (
                L0
                + scale * jacobian_map(H2)
                + scale**2 * jacobian_map(H3)
                + scale**3 * jacobian_map(H4)
            ).det()
        ),
        scale,
    )


# kappa=0: direct third-column exits.
expected_zero_tangent = {
    "cusp": {
        p**6: -4 * linear_symbols[8],
        p**4 * q**2: 12 * linear_symbols[2],
        p**3 * q**3: -8 * linear_symbols[5],
    },
    "flex": {
        p**4 * q**2: -4 * linear_symbols[8],
        p**2 * q**4: 12 * linear_symbols[2],
        p * q**5: -8 * linear_symbols[5],
    },
    "general": {
        p**6: -4 * linear_symbols[8],
        p**4 * q**2: 12 * linear_symbols[2] - 4 * linear_symbols[8],
        p**3 * q**3: 24 * linear_symbols[2] - 8 * linear_symbols[5],
    },
}
for name, h in leading_forms.items():
    determinant = determinant_polynomial(h * A, V, B2)
    E6 = sp.Poly(determinant.coeff_monomial(scale**6), p, q, r)
    for monomial, expected in expected_zero_tangent[name].items():
        assert sp.expand(E6.coeff_monomial(monomial) - expected) == 0

# kappa=1: solve the complete E6 system, then read the constant E5
# obstruction.
binary_nonzero_certificates = {
    "cusp": {(1, 3, 1): 24},
    "flex": {(0, 4, 1): 24},
    "general": {(1, 3, 1): 24, (0, 4, 1): 24},
}
binary_e6_ranks = {"cusp": 7, "flex": 6, "general": 7}
for name, h in leading_forms.items():
    determinant = determinant_polynomial(h * A, V, B2 + r * S)
    E6 = sp.Poly(determinant.coeff_monomial(scale**6), p, q, r)
    solve_variables = [
        *v,
        linear_symbols[2],
        linear_symbols[5],
        linear_symbols[8],
    ]
    matrix, rhs = sp.linear_eq_to_matrix(E6.coeffs(), solve_variables)
    assert matrix.rank() == binary_e6_ranks[name]
    assert matrix.row_join(rhs).rank() == binary_e6_ranks[name]
    solution = list(sp.linsolve((matrix, rhs), solve_variables))[0]
    substitution = dict(zip(solve_variables, solution))
    assert sp.expand(E6.as_expr().xreplace(substitution)) == 0
    E5 = sp.Poly(
        sp.expand(
            determinant.coeff_monomial(scale**5).xreplace(substitution)
        ),
        p,
        q,
        r,
    )
    for monomial, expected in binary_nonzero_certificates[name].items():
        assert sp.expand(E5.coeff_monomial(monomial) - expected) == 0


def check_tangent_leaf(
    H4: sp.Matrix,
    H3: sp.Matrix,
    expected_solution: list[sp.Expr],
    certificate_monomial: sp.Expr,
    certificate_value: sp.Expr,
) -> None:
    matrix, rhs, _ = coefficient_system(
        degree_seven(H4, H3, H2_general), list(w)
    )
    assert matrix.rank() == 8
    assert matrix.row_join(rhs).rank() == 8
    actual_solution = list(sp.linsolve((matrix, rhs), w))[0]
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(actual_solution, expected_solution)
    )
    H2 = H2_general.xreplace(dict(zip(w, actual_solution)))
    assert degree_seven(H4, H3, H2) == 0
    determinant = determinant_polynomial(H4, H3, H2)
    E6 = sp.Poly(determinant.coeff_monomial(scale**6), p, q, r)
    assert sp.expand(
        E6.coeff_monomial(certificate_monomial) - certificate_value
    ) == 0


# h=p, tangent A_p.
cusp_tangent_H3 = (V + r * Ap).subs(
    {v[6]: -sp.Rational(9, 2) * v[3], v[7]: 0}
)
cusp_tangent_solution = list(w)
cusp_tangent_solution[2] = (27 * v[0] - v[10]) / 12
cusp_tangent_solution[4] = (
    15 * v[1] + 3 * v[11] - 18 * v[4] + 8 * w[8]
) / 12
cusp_tangent_solution[5] = 0
cusp_tangent_solution[10] = -(3 * v[2] - 10 * v[5]) / 8
cusp_tangent_solution[11] = sp.Rational(3, 2)
cusp_tangent_solution[14] = 9 * v[8] / 4
cusp_tangent_solution[16] = 5 * v[9] / 4
cusp_tangent_solution[17] = 0
check_tangent_leaf(
    p * A,
    cusp_tangent_H3,
    cusp_tangent_solution,
    p * q**3 * r**2,
    -12,
)

# h=q, tangent A_p.
flex_ap_H3 = (V + r * Ap).subs({v[8]: 0})
flex_ap_solution = list(w)
flex_ap_solution[2] = 2 * (v[1] - v[4])
flex_ap_solution[4] = (3 * v[2] - 4 * v[5] + 2 * w[8]) / 3
flex_ap_solution[5] = -1
flex_ap_solution[10] = v[6]
flex_ap_solution[11] = 0
flex_ap_solution[14] = 2 * v[9]
flex_ap_solution[16] = -9 * v[0] + v[10]
flex_ap_solution[17] = 0
check_tangent_leaf(
    q * A,
    flex_ap_H3,
    flex_ap_solution,
    p * q**3 * r**2,
    -48,
)

# h=q, tangent A_q.
flex_aq_H3 = (V + r * Aq).subs({v[8]: 0, v[9]: 0})
flex_aq_solution = list(w)
flex_aq_solution[2] = (15 * v[2] - 2 * v[5]) / 12
flex_aq_solution[4] = (27 * v[3] - 10 * v[6] + 8 * w[8]) / 12
flex_aq_solution[5] = 0
flex_aq_solution[10] = 9 * v[7] / 4
flex_aq_solution[11] = 0
flex_aq_solution[14] = (9 * v[0] + 5 * v[10]) / 4
flex_aq_solution[16] = -3 * (v[1] - 3 * v[11] + 2 * v[4]) / 4
flex_aq_solution[17] = 3
check_tangent_leaf(
    q * A,
    flex_aq_H3,
    flex_aq_solution,
    p**4 * r**2,
    12,
)

print("scalar-aligned cuspidal-cubic SymPy checks passed")
