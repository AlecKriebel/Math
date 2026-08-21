#!/usr/bin/env python3
"""Explore lower identities on the c0=0 unmarked contact boundary."""

from __future__ import annotations

import sympy as sp


p, q, r, tau = sp.symbols("p q r tau")
w = sp.symbols("w")
variables = (p, q, r)


def binary_form(prefix: str, degree: int):
    coeffs = sp.symbols(f"{prefix}0:{degree + 1}")
    value = sum(
        coeffs[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )
    return value, coeffs


P = p * (p * q**2 + sp.Rational(1, 2) * q**3)
Q = p * (p**3 + p**2 * q - sp.Rational(1, 8) * q**3)
R = p * q**2 + sp.Rational(1, 4) * q**3
direction = lambda form: sp.diff(form, q) - sp.Rational(1, 4) * sp.diff(form, p)
Nu, Nv, Nt = [sp.cancel(direction(form) / q) for form in (P, Q, R)]

U0, u = binary_form("u", 3)
V0, v = binary_form("v", 3)
T0, t = binary_form("t", 2)
A0, x = binary_form("x", 2)
B0, y = binary_form("y", 2)
x3, x4, x5, y3, y4, y5 = sp.symbols("x3 x4 x5 y3 y4 y5")

U = U0 + r * Nu
V = V0 + r * Nv
T = T0 + r * Nt
A = A0 + r * (x3 * p + x4 * q) + x5 * r**2
B = B0 + r * (y3 * p + y4 * q) + y5 * r**2

H4 = sp.Matrix((P, Q, 0))
H3 = sp.Matrix((U, V, R))
H2 = sp.Matrix((A, B, T))
l = sp.symbols("l11 l12 l13 l21 l22 l23 l31 l32 l33")
L = sp.Matrix(3, 3, l)
weighted = sp.Poly(
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
E = {
    degree: sp.Poly(
        sp.expand(weighted.coeff_monomial(tau**degree)), p, q, r
    )
    for degree in range(1, 9)
}

gauge = {
    u[3]: 0,
    v[3]: 0,
    t[0]: 0,
    t[2]: 0,
    u[1]: sp.Rational(3, 4) * u[0] + sp.Rational(8, 9) * w,
    u[2]: sp.Rational(1, 8) * u[0] + sp.Rational(2, 3) * w,
    v[1]: w + 6 * v[2],
    v[0]: sp.Rational(16, 9) * w + 8 * v[2],
    t[1]: sp.Rational(8, 9) * w,
    x5: -sp.Rational(1, 4),
    y5: sp.Rational(5, 64),
}
e6_solution = {
    x3: (3 * u[0] - 8 * u[1] + 16 * u[2]) / 8,
    x4: -(3 * u[0] - 4 * u[1] + 16 * u[2]) / 64,
    y3: -(9 * u[0] - 12 * u[1] + 32 * v[1] - 128 * v[2]) / 64,
    y4: (3 * u[0] - 4 * u[1] - 64 * v[2]) / 256,
    l[8]: (3 * u[0] - 4 * u[1]) / 8,
}
gauge.update(
    {
        variable: sp.factor(value.subs(gauge))
        for variable, value in e6_solution.items()
    }
)


def coefficients(poly: sp.Poly, r_degree: int):
    return [
        coefficient
        for monomial, coefficient in poly.terms()
        if monomial[2] == r_degree
    ]


def main() -> None:
    assert E[8].is_zero and E[7].is_zero
    e6 = sp.Poly(sp.expand(E[6].as_expr().subs(gauge)), p, q, r)
    assert e6.is_zero
    e5 = sp.Poly(sp.expand(E[5].as_expr().subs(gauge)), p, q, r)
    print("E5 r coefficients", [sp.factor(value) for value in coefficients(e5, 1)])

    constant = coefficients(e5, 0)
    candidates = (x[0], x[1], x[2], y[0], y[1], y[2], l[6], l[7])
    matrix, _ = sp.linear_eq_to_matrix(constant, candidates)
    pivots = matrix.rref()[1]
    print("E5 constant shape/rank/pivots", matrix.shape, matrix.rank(), pivots)
    pivot_variables = tuple(candidates[index] for index in pivots)
    solve_matrix, rhs = sp.linear_eq_to_matrix(constant, pivot_variables)
    compatibility = [
        sp.factor((vector.T * rhs)[0])
        for vector in solve_matrix.T.nullspace()
    ]
    print("E5 compatibility", compatibility)
    _, independent_rows = solve_matrix.T.rref()
    square = solve_matrix.extract(independent_rows, range(len(pivot_variables)))
    square_rhs = rhs.extract(independent_rows, [0])
    solution = [
        sp.factor(value)
        for value in square.inv() * square_rhs
    ]
    solved = dict(zip(pivot_variables, solution))
    for variable, value in solved.items():
        print(variable, "=", value)
    assert all(sp.factor(value.subs(solved)) == 0 for value in constant)

    e4 = sp.Poly(
        sp.expand(E[4].as_expr().subs(gauge).subs(solved)), p, q, r
    )
    for monomial, coefficient in e4.terms():
        print("E4", monomial, sp.factor(coefficient))


if __name__ == "__main__":
    main()
