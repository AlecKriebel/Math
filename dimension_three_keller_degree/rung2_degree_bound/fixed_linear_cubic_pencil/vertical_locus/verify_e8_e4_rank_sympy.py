#!/usr/bin/python3
"""Exact symbolic checks for the triple-vertical E8--E4 rank ledger."""

from __future__ import annotations

import sympy as sp

if not __debug__:
    raise SystemExit("refusing optimized Python: assertions would be disabled")

x, y, z, tau = sp.symbols("x y z tau")
variables = (x, y, z)


def bracket(a: sp.Expr, b: sp.Expr) -> sp.Expr:
    return sp.expand(sp.diff(a, x) * sp.diff(b, y) - sp.diff(a, y) * sp.diff(b, x))


def jacobian_matrix(vector: sp.Matrix) -> sp.Matrix:
    return vector.jacobian(variables)


# Binary E5 rank table.
v0, v1, v2, v3, r, s, modulus = sp.symbols("v0 v1 v2 v3 r s modulus")
V0 = v0 * x**3 + v1 * x**2 * y + v2 * x * y**2 + v3 * y**3
linear_row = r * x + s * y
unknowns = (v0, v1, v2, v3, r, s)


def binary_kernel(q0: sp.Expr, ell: sp.Expr) -> list[sp.Matrix]:
    equation = sp.Poly(
        sp.expand(ell * bracket(q0, V0) - q0 * bracket(q0, linear_row)),
        x,
        y,
    )
    matrix, _ = sp.linear_eq_to_matrix(equation.coeffs(), unknowns)
    return matrix.nullspace()


table = {
    "squarefree_nonzero": (
        x * y * (x - y),
        x + modulus * y,
        1,
    ),
    "double_generic": (x**2 * y, x + y, 1),
    "double_x": (x**2 * y, x, 2),
    "double_y": (x**2 * y, y, 2),
    "squarefree_zero": (x * y * (x - y), 0, 4),
    "double_zero": (x**2 * y, 0, 4),
}
for label, (q0, ell, expected_nullity) in table.items():
    vectors = binary_kernel(q0, ell)
    assert len(vectors) == expected_nullity, (label, vectors)

squarefree_vector = binary_kernel(x * y * (x - y), x + modulus * y)[0]
assert squarefree_vector == sp.Matrix([0, -1, 1, 0, 0, 0])

assert binary_kernel(x**2 * y, x) == [
    sp.Matrix([0, 1, 0, 0, 0, 0]),
    sp.Matrix([0, 0, sp.Rational(2, 3), 0, 0, 1]),
]
assert binary_kernel(x**2 * y, y) == [
    sp.Matrix([0, 1, 0, 0, 0, 0]),
    sp.Matrix([sp.Rational(1, 3), 0, 0, 0, 1, 0]),
]


# Reconstruct all z=0 determinant restrictions directly.
q30, q21, q12, q03 = sp.symbols("q30 q21 q12 q03")
q20, q11, q02, q10, q01, q00 = sp.symbols(
    "q20 q11 q02 q10 q01 q00"
)
q0_general = q30 * x**3 + q21 * x**2 * y + q12 * x * y**2 + q03 * y**3
q_general = (
    q0_general
    + z * (q20 * x**2 + q11 * x * y + q02 * y**2)
    + z**2 * (q10 * x + q01 * y)
    + q00 * z**3
)

quadratic_monomials = (x**2, x * y, y**2, x * z, y * z, z**2)
cA = sp.symbols("A0:6")
cB = sp.symbols("B0:6")
cW = sp.symbols("W0:6")
A = sum(c * m for c, m in zip(cA, quadratic_monomials))
B = sum(c * m for c, m in zip(cB, quadratic_monomials))
W = sum(c * m for c, m in zip(cW, quadratic_monomials))

cV = sp.symbols("V0:10")
cubic_monomials = (
    x**3,
    x**2 * y,
    x * y**2,
    y**3,
    x**2 * z,
    x * y * z,
    y**2 * z,
    x * z**2,
    y * z**2,
    z**3,
)
V = sum(c * m for c, m in zip(cV, cubic_monomials))
cL = sp.symbols("l0:9")
L = sp.Matrix(3, 3, cL)
H4 = sp.Matrix([z**4, z * q_general, 0])


def determinant_coefficients(H3: sp.Matrix, H2: sp.Matrix) -> dict[int, sp.Expr]:
    determinant = sp.Poly(
        sp.expand(
            (
                L
                + tau * jacobian_matrix(H2)
                + tau**2 * jacobian_matrix(H3)
                + tau**3 * jacobian_matrix(H4)
            ).det()
        ),
        tau,
    )
    return {weight: sp.expand(determinant.coeff_monomial(tau**weight)) for weight in (6, 5, 4)}


# Vertical companion, a != 0 formulas.
a = sp.symbols("a")
U_vertical = sp.Rational(4, 3) * z * W + a * q_general
vertical_coefficients = determinant_coefficients(
    sp.Matrix([U_vertical, V, z**3]), sp.Matrix([A, B, W])
)
assert sp.expand(
    vertical_coefficients[6].subs(z, 0)
    + a * q0_general * bracket(q0_general, W.subs(z, 0))
) == 0

# Set W0=0 and compare the E5 binary formula.
w_linear = cW[3] * x + cW[4] * y
V_binary = V.subs(z, 0)
third_linear_binary = cL[6] * x + cL[7] * y
vertical_e5_w0_zero = vertical_coefficients[5].subs(
    {z: 0, cW[0]: 0, cW[1]: 0, cW[2]: 0}
)
expected_vertical_e5 = a * (
    w_linear * bracket(q0_general, V_binary)
    - q0_general * bracket(q0_general, third_linear_binary)
)
assert sp.expand(vertical_e5_w0_zero - expected_vertical_e5) == 0

# The a=0 E5 family.
vertical_e5_a_zero = vertical_coefficients[5].subs({z: 0, a: 0})
expected_a_zero = sp.Rational(1, 3) * (
    4 * W.subs(z, 0) * bracket(V_binary, W.subs(z, 0))
    + 3 * q0_general * bracket(W.subs(z, 0), A.subs(z, 0))
)
assert sp.expand(vertical_e5_a_zero - expected_a_zero) == 0


# Nonvertical companion formulas.
d, f = sp.symbols("d f")
nonvertical_coefficients = determinant_coefficients(
    sp.Matrix([d * z**3, z * W + f * z**3, q_general]),
    sp.Matrix([A, B, W]),
)
expected_nonvertical_e6 = -q0_general * bracket(A.subs(z, 0), q0_general)
assert sp.expand(nonvertical_coefficients[6].subs(z, 0) - expected_nonvertical_e6) == 0

nontriple_substitutions = {
    z: 0,
    cA[0]: 0,
    cA[1]: 0,
    cA[2]: 0,
    cL[0]: 0,
    cL[1]: 0,
}
assert nonvertical_coefficients[5].subs(nontriple_substitutions) == 0

nonvertical_e4_reduced = sp.factor(
    nonvertical_coefficients[4].subs(nontriple_substitutions)
)
A1 = cA[3] * x + cA[4] * y
expected_nonvertical_e4 = A1 * bracket(B.subs(z, 0), q0_general)
assert sp.expand(nonvertical_e4_reduced - expected_nonvertical_e4) == 0


# E5 regression guard remains on the ell=0 exceptional leaf.
q_sample = x**3 + y**3
H4_sample = sp.Matrix([z**4, z * q_sample, 0])
H3_sample = sp.Matrix([q_sample + sp.Rational(4, 3) * z**3, 0, z**3])
H2_sample = sp.Matrix([0, x * z, z**2])
regression = sp.Poly(
    sp.expand(
        (
            sp.eye(3)
            + tau * H2_sample.jacobian((x, y, z))
            + tau**2 * H3_sample.jacobian((x, y, z))
            + tau**3 * H4_sample.jacobian((x, y, z))
        ).det()
    ),
    tau,
)
for weight in (8, 7, 6, 5):
    assert regression.coeff_monomial(tau**weight) == 0
assert regression.coeff_monomial(tau**4) == 9 * x**2 * z**2

print("triple-vertical E8--E4 rank-ledger SymPy checks passed")
