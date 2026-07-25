#!/usr/bin/python3
"""Exact constant-minor exclusion for the nonvertical nontriple companion."""

from __future__ import annotations

import sympy as sp

if not __debug__:
    raise SystemExit("refusing optimized Python: assertions would be disabled")

x, y, z, tau = sp.symbols("x y z tau")
variables = (x, y, z)

q_lower = sp.symbols("q4:10")
w = sp.symbols("w0:6")
d, f = sp.symbols("d f")
quadratic_monomials = (x**2, x * y, y**2, x * z, y * z, z**2)
lower_cubic_monomials = (
    x**2 * z,
    x * y * z,
    y**2 * z,
    x * z**2,
    y * z**2,
    z**3,
)
W = sum(coefficient * monomial for coefficient, monomial in zip(w, quadratic_monomials))
q_tail = sum(
    coefficient * monomial
    for coefficient, monomial in zip(q_lower, lower_cubic_monomials)
)

linear_symbols = sp.symbols("l0:9")
L = sp.Matrix(3, 3, linear_symbols)


def coefficient_equations(
    q0: sp.Expr, A: sp.Expr, B: sp.Expr, specialized_linear: sp.Matrix
) -> list[sp.Expr]:
    q = q0 + q_tail
    H4 = sp.Matrix([z**4, z * q, 0])
    H3 = sp.Matrix([d * z**3, z * W + f * z**3, q])
    H2 = sp.Matrix([A, B, W])
    determinant = sp.Poly(
        sp.expand(
            (
                specialized_linear
                + tau * H2.jacobian(variables)
                + tau**2 * H3.jacobian(variables)
                + tau**3 * H4.jacobian(variables)
            ).det()
        ),
        tau,
    )
    equations: list[sp.Expr] = []
    for weight in (6, 5):
        equations.extend(
            sp.Poly(determinant.coeff_monomial(tau**weight), *variables).coeffs()
        )
    return equations


root_types = {
    "squarefree": x * y * (x - y),
    "double": x**2 * y,
}


for label, q0 in root_types.items():
    # E4 leaf N1: A is already a multiple of z^2.
    alpha = sp.symbols(f"alpha_{label}")
    b = sp.symbols(f"b_{label}_0:6")
    B = sum(coefficient * monomial for coefficient, monomial in zip(b, quadratic_monomials))
    L1 = L.subs({linear_symbols[0]: 0, linear_symbols[1]: 0})
    unknowns_n1 = b + (linear_symbols[2],) + linear_symbols[3:]
    equations_n1 = coefficient_equations(q0, alpha * z**2, B, L1)
    matrix_n1, rhs_n1 = sp.linear_eq_to_matrix(equations_n1, unknowns_n1)

    pivot_columns_n1 = (0, 1, 2, 3, 4, 7, 8)
    pivot_rows_n1 = (
        (0, 1, 2, 3, 4, 12, 14)
        if label == "squarefree"
        else (0, 1, 2, 3, 4, 11, 13)
    )
    pivot_n1 = matrix_n1.extract(pivot_rows_n1, pivot_columns_n1)
    assert sp.factor(pivot_n1.det()) == -524288

    free_columns_n1 = [
        index for index in range(len(unknowns_n1)) if index not in pivot_columns_n1
    ]
    pivot_solution_n1 = pivot_n1.inv() * (
        rhs_n1.extract(pivot_rows_n1, [0])
        - matrix_n1.extract(pivot_rows_n1, free_columns_n1)
        * sp.Matrix([unknowns_n1[index] for index in free_columns_n1])
    )
    solved_n1 = {
        unknowns_n1[column]: sp.factor(pivot_solution_n1[row])
        for row, column in enumerate(pivot_columns_n1)
    }
    expected_n1 = {
        b[0]: 0,
        b[1]: 0,
        b[2]: 0,
        b[3]: linear_symbols[6],
        b[4]: linear_symbols[7],
        linear_symbols[3]: 0,
        linear_symbols[4]: 0,
    }
    assert solved_n1 == expected_n1, (label, solved_n1)
    assert all(sp.expand(equation.subs(solved_n1)) == 0 for equation in equations_n1)

    # E4 leaf N2: B_0=0, while A may initially have z-linear terms.
    a3, a4, a5 = sp.symbols(f"a_{label}_3:6")
    b3, b4, b5 = sp.symbols(f"bb_{label}_3:6")
    A2 = a3 * x * z + a4 * y * z + a5 * z**2
    B2 = b3 * x * z + b4 * y * z + b5 * z**2
    unknowns_n2 = (
        a3,
        a4,
        a5,
        b3,
        b4,
        b5,
        linear_symbols[2],
    ) + linear_symbols[3:]
    equations_n2 = coefficient_equations(q0, A2, B2, L1)
    matrix_n2, rhs_n2 = sp.linear_eq_to_matrix(equations_n2, unknowns_n2)

    pivot_columns_n2 = (0, 1, 3, 4, 7, 8)
    pivot_rows_n2 = (
        (0, 2, 8, 12, 24, 27)
        if label == "squarefree"
        else (0, 2, 7, 10, 21, 24)
    )
    pivot_n2 = matrix_n2.extract(pivot_rows_n2, pivot_columns_n2)
    assert sp.factor(pivot_n2.det()) == -2048

    free_columns_n2 = [
        index for index in range(len(unknowns_n2)) if index not in pivot_columns_n2
    ]
    pivot_solution_n2 = pivot_n2.inv() * (
        rhs_n2.extract(pivot_rows_n2, [0])
        - matrix_n2.extract(pivot_rows_n2, free_columns_n2)
        * sp.Matrix([unknowns_n2[index] for index in free_columns_n2])
    )
    solved_n2 = {
        unknowns_n2[column]: sp.factor(pivot_solution_n2[row])
        for row, column in enumerate(pivot_columns_n2)
    }
    expected_n2 = {
        a3: 0,
        a4: 0,
        b3: linear_symbols[6],
        b4: linear_symbols[7],
        linear_symbols[3]: 0,
        linear_symbols[4]: 0,
    }
    assert solved_n2 == expected_n2, (label, solved_n2)
    assert all(sp.expand(equation.subs(solved_n2)) == 0 for equation in equations_n2)

    # Both leaves make the first two linear rows multiples of dz.
    for solved in (solved_n1, solved_n2):
        reduced_linear = L1.subs(solved)
        assert sp.expand(reduced_linear.det()) == 0

print("nonvertical nontriple E4 constant-minor checks passed")
