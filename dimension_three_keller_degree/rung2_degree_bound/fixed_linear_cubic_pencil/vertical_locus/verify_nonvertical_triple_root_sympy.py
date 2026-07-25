#!/usr/bin/python3
"""Exact constant-minor checks for the nonvertical triple-root leaf."""

from __future__ import annotations

import sympy as sp

if not __debug__:
    raise SystemExit("refusing optimized Python: assertions would be disabled")

x, y, z, tau = sp.symbols("x y z tau")
variables = (x, y, z)
alpha, beta, d, f = sp.symbols("alpha beta d f")

quadratic_monomials = (x**2, x * y, y**2, x * z, y * z, z**2)
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
w = sp.symbols("w0:6")
linear = sp.symbols("l0:9")
A = sum(coefficient * monomial for coefficient, monomial in zip(a, quadratic_monomials))
B = sum(coefficient * monomial for coefficient, monomial in zip(b, quadratic_monomials))
W = sum(coefficient * monomial for coefficient, monomial in zip(w, quadratic_monomials))
L = sp.Matrix(3, 3, linear)
unknowns = a + b + linear

families = {
    "quadratic_y": {
        "q": x**3 + y**2 * z + alpha * x * z**2 + beta * z**3,
        "pivot_rows": (0, 1, 2, 3, 6, 7, 10, 11, 14, 19, 21, 25, 30, 38),
        "minor": -110075314176,
    },
    "mixed_xy": {
        "q": x**3 + x * y * z + beta * z**3,
        "pivot_rows": (0, 1, 2, 4, 6, 7, 8, 9, 12, 14, 15, 17, 24, 28),
        "minor": -191102976,
    },
    "linear_y": {
        "q": x**3 + y * z**2,
        "pivot_rows": (0, 1, 2, 3, 5, 7, 8, 10, 12, 13, 14, 19, 23, 30),
        "minor": -2293235712,
    },
}
pivot_columns = (0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 15, 16)

expected_solution = {
    a[0]: 0,
    a[1]: 0,
    a[2]: 0,
    a[3]: 0,
    a[4]: 0,
    b[0]: 0,
    b[1]: 0,
    b[2]: 0,
    b[3]: linear[6],
    b[4]: linear[7],
    linear[0]: 0,
    linear[1]: 0,
    linear[3]: 0,
    linear[4]: 0,
}

for label, data in families.items():
    q = data["q"]
    H4 = sp.Matrix([z**4, z * q, 0])
    H3 = sp.Matrix([d * z**3, z * W + f * z**3, q])
    H2 = sp.Matrix([A, B, W])
    determinant = sp.Poly(
        sp.expand(
            (
                L
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
    matrix, rhs = sp.linear_eq_to_matrix(equations, unknowns)

    pivot_rows = data["pivot_rows"]
    pivot = matrix.extract(pivot_rows, pivot_columns)
    assert sp.factor(pivot.det()) == data["minor"], label

    free_columns = [
        index for index in range(len(unknowns)) if index not in pivot_columns
    ]
    pivot_solution = pivot.inv() * (
        rhs.extract(pivot_rows, [0])
        - matrix.extract(pivot_rows, free_columns)
        * sp.Matrix([unknowns[index] for index in free_columns])
    )
    solved = {
        unknowns[column]: sp.factor(pivot_solution[row])
        for row, column in enumerate(pivot_columns)
    }
    assert solved == expected_solution, (label, solved)
    assert all(sp.expand(equation.subs(solved)) == 0 for equation in equations)
    assert sp.expand(L.subs(solved).det()) == 0

print("nonvertical triple-root constant-minor checks passed")
