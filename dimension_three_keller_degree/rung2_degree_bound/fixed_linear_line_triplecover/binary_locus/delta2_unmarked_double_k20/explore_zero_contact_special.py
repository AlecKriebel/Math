#!/usr/bin/env python3
"""Lower identities on the exceptional unmarked-double zero-contact locus."""

from __future__ import annotations

import sympy as sp


p, q, r, tau, eta = sp.symbols("p q r tau eta")
variables = (p, q, r)


def binary_form(prefix: str, degree: int):
    coefficients = sp.symbols(f"{prefix}0:{degree + 1}")
    value = sum(
        coefficients[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )
    return value, coefficients


# Normalize b=c0=1 and impose N_3=0, hence c3=1/64.
P = p * q**3
Q = p * (p**3 + p**2 * q + sp.Rational(3, 8) * p * q**2)
R = (
    p**3
    + sp.Rational(3, 4) * p**2 * q
    + sp.Rational(3, 16) * p * q**2
    + sp.Rational(1, 64) * q**3
)
direction = lambda form: sp.diff(form, q) - sp.Rational(1, 4) * sp.diff(
    form, p
)
N = tuple(sp.factor(direction(form) / q**2) for form in (P, Q, R))
assert all(
    sp.expand(actual - expected) == 0
    for actual, expected in zip(N, (3 * p - q / 4, -3 * p / 16, 0))
)

U0, u = binary_form("u", 3)
V0, v = binary_form("v", 3)
T0, w = binary_form("w", 2)
A0, aa = binary_form("aa", 2)
B0, bb = binary_form("bb", 2)
linear = sp.symbols("ell0:9")

H4 = sp.Matrix((P, Q, 0))
H3 = sp.Matrix((U0, V0, R))
H2 = sp.Matrix((A0 + eta * r * N[0], B0 + eta * r * N[1], T0))
L = sp.Matrix(3, 3, linear).subs(linear[8], 0)
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
assert E[8].is_zero and E[7].is_zero


def equations(polynomial: sp.Poly):
    return [coefficient for _, coefficient in polynomial.terms()]


def main() -> None:
    print("E6 terms", len(E[6].terms()))
    e6_unknowns = aa + bb + w
    matrix, rhs = sp.linear_eq_to_matrix(equations(E[6]), e6_unknowns)
    active = [
        index
        for index in range(matrix.cols)
        if any(matrix[row, index] != 0 for row in range(matrix.rows))
    ]
    matrix = matrix.extract(range(matrix.rows), active)
    unknowns = tuple(e6_unknowns[index] for index in active)
    print("E6", matrix.shape, "rank", matrix.rank(), unknowns)
    left = matrix.T.nullspace()
    compatibility = [
        sp.factor((vector.T * rhs)[0])
        for vector in left
    ]
    print("E6 compatibilities", len(compatibility))
    for index, value in enumerate(compatibility):
        print(index, value)
    _, rows = matrix.T.rref()
    independent = list(rows[: matrix.cols])
    square = matrix.extract(independent, range(matrix.cols))
    square_rhs = rhs.extract(independent, [0])
    solution = [
        sp.factor(value)
        for value in square.inv() * square_rhs
    ]
    for variable, value in zip(unknowns, solution):
        print(variable, "=", value)

    print("E5 terms", len(E[5].terms()))
    for monomial, coefficient in E[5].terms():
        print("E5", monomial, sp.factor(coefficient))
    e5_unknowns = u + v + w + (linear[2], linear[5])
    e5_matrix, e5_rhs = sp.linear_eq_to_matrix(
        equations(E[5]), e5_unknowns
    )
    print("E5 matrix", e5_matrix.shape, "rank", e5_matrix.rank())
    print("E5 nullity", len(e5_matrix.nullspace()))
    rref, pivots = e5_matrix.rref()
    print("E5 pivots", pivots)
    print("E5 rref")
    for row in range(rref.rows):
        print([sp.factor(value) for value in rref.row(row)])

    pivot_variables = tuple(e5_unknowns[index] for index in pivots)
    e5_solution = sp.solve(
        equations(E[5]), pivot_variables, dict=True
    )[0]
    e5_solution = {
        variable: sp.factor(value.subs(eta, 1))
        for variable, value in e5_solution.items()
    }
    e4 = sp.Poly(
        sp.expand(E[4].as_expr().subs(eta, 1).subs(e5_solution)),
        p,
        q,
        r,
    )
    print("E4 terms", len(e4.terms()))
    print("E4 r-positive")
    for monomial, coefficient in e4.terms():
        if monomial[2] > 0:
            print(monomial, sp.factor(coefficient))


if __name__ == "__main__":
    main()
