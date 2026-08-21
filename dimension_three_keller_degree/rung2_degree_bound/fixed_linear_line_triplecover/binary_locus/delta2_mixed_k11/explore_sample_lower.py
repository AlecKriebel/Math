#!/usr/bin/env python3
"""Full lower determinant at one exact-open rational point of the k11 contact."""

from __future__ import annotations

import sympy as sp


p, q, r, tau = sp.symbols("p q r tau")
variables = (p, q, r)


def binary_form(prefix: str, degree: int):
    coefficients = sp.symbols(f"{prefix}0:{degree + 1}")
    value = sum(
        coefficients[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )
    return value, coefficients


a = sp.Rational(6, 7)
b = sp.Rational(2, 7)
c = sp.Rational(22, 3)
x_contact = sp.Rational(1, 4)
y_contact = sp.Integer(1)
lam = sp.Rational(71, 28)
mu = -sp.Rational(1, 14)

A3 = q**2 * (a * p + q)
B3 = p**3 + p**2 * q + b * p * q**2
P, Q = p * A3, p * B3
R = p * (c * p**2 + sp.Rational(3, 4) * c * p * q + q**2)
Np = tuple(sp.cancel(sp.diff(form, q) / p) for form in (P, Q, R))
direction = lambda form: sp.diff(form, q) - sp.Rational(1, 4) * sp.diff(
    form, p
)
Nq = tuple(sp.cancel(direction(form) / q) for form in (P, Q, R))
S = tuple(
    sp.expand(x_contact * Np[index] + y_contact * Nq[index])
    for index in range(3)
)

U0, u = binary_form("u", 3)
V0, v = binary_form("v", 3)
T0, w = binary_form("w", 2)
A0, aa = binary_form("aa", 2)
B0, bb = binary_form("bb", 2)
x3, x4, y3, y4 = sp.symbols("x3 x4 y3 y4")
linear = sp.symbols("ell0:9")

H4 = sp.Matrix((P, Q, 0))
H3 = sp.Matrix((U0 + r * S[0], V0 + r * S[1], R))
H2 = sp.Matrix(
    (
        A0 + r * (x3 * p + x4 * q) - lam * r**2 / 2,
        B0 + r * (y3 * p + y4 * q) - mu * r**2 / 2,
        T0 + r * S[2],
    )
)
L = sp.Matrix(3, 3, linear)
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
    print("S", S)
    print("E6 terms", len(E[6].terms()))
    print("E6 r2", [
        (monomial, sp.factor(coefficient))
        for monomial, coefficient in E[6].terms()
        if monomial[2] == 2
    ])
    unknowns = (x3, x4, y3, y4, linear[8])
    matrix, rhs = sp.linear_eq_to_matrix(equations(E[6]), unknowns)
    print("E6 matrix", matrix.shape, "rank", matrix.rank())
    left = matrix.T.nullspace()
    print("E6 compatibility count", len(left))
    compatibility = [
        sp.factor((vector.T * rhs)[0])
        for vector in left
    ]
    for index, value in enumerate(compatibility):
        print("compatibility", index, value)
    _, rows = matrix.T.rref()
    independent_rows = list(rows[: len(unknowns)])
    print("independent rows", independent_rows)
    square = matrix.extract(independent_rows, range(len(unknowns)))
    square_rhs = rhs.extract(independent_rows, [0])
    solution = [
        sp.factor(value)
        for value in square.inv() * square_rhs
    ]
    for variable, value in zip(unknowns, solution):
        print(variable, "=", value)

    u1_solution = sp.solve(compatibility[0], u[1], dict=True)[0][u[1]]
    e6_substitution = {
        u[1]: u1_solution,
        v[3]: 0,
        **{
            variable: value.subs({u[1]: u1_solution, v[3]: 0})
            for variable, value in zip(unknowns, solution)
        },
    }
    e5 = sp.Poly(sp.expand(E[5].as_expr().subs(e6_substitution)), p, q, r)
    print(
        "E5 r2",
        [
            (monomial, sp.factor(coefficient))
            for monomial, coefficient in e5.terms()
            if monomial[2] == 2
        ],
    )
    e5_unknowns = aa + bb + linear[:8]
    e5_matrix, e5_rhs = sp.linear_eq_to_matrix(equations(e5), e5_unknowns)
    active_columns = [
        index
        for index in range(e5_matrix.cols)
        if any(e5_matrix[row, index] != 0 for row in range(e5_matrix.rows))
    ]
    reduced_unknowns = tuple(e5_unknowns[index] for index in active_columns)
    reduced_matrix = e5_matrix.extract(range(e5_matrix.rows), active_columns)
    print(
        "E5 matrix",
        reduced_matrix.shape,
        "rank",
        reduced_matrix.rank(),
        "unknowns",
        reduced_unknowns,
    )
    e5_left = reduced_matrix.T.nullspace()
    print("E5 compatibility count", len(e5_left))
    e5_compatibility = [
        sp.factor((vector.T * e5_rhs)[0])
        for vector in e5_left
    ]
    for index, value in enumerate(e5_compatibility):
        print("E5 compatibility", index, value)


if __name__ == "__main__":
    main()
