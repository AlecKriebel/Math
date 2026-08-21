#!/usr/bin/env python3
"""Explore the exact mixed-divisor {1,1} leaf in the fixed-linear row."""

from __future__ import annotations

import sympy as sp


p, q, r, t = sp.symbols("p q r t")
a, b, c = sp.symbols("a b c")
x, y, lam, mu = sp.symbols("x y lam mu")
variables = (p, q, r)


def jac2(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, p) * sp.diff(second, q)
        - sp.diff(first, q) * sp.diff(second, p)
    )


def jac3(first: sp.Expr, second: sp.Expr, third: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix(
            [
                [sp.diff(value, variable) for variable in variables]
                for value in (first, second, third)
            ]
        ).det()
    )


A = q**2 * (a * p + q)
B = p**3 + p**2 * q + b * p * q**2
P, Q = p * A, p * B
R = p * (c * p**2 + sp.Rational(3, 4) * c * p * q + q**2)
alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)

Np = tuple(sp.cancel(sp.diff(form, q) / p) for form in (P, Q, R))
direction = lambda form: sp.diff(form, q) - sp.Rational(1, 4) * sp.diff(
    form, p
)
Nq = tuple(sp.cancel(direction(form) / q) for form in (P, Q, R))
assert all(
    sp.cancel(alpha * N[0] + beta * N[1] + gamma * N[2]) == 0
    for N in (Np, Nq)
)

S = tuple(sp.expand(x * Np[index] + y * Nq[index]) for index in range(3))
curvature = sp.expand(
    jac3(P, r * S[1], r * S[2])
    + jac3(r * S[0], Q, r * S[2])
    + jac3(r * S[0], r * S[1], R)
)
K = sp.Poly(curvature, r).coeff_monomial(r)
contact_residual = sp.Poly(sp.expand(K - lam * alpha - mu * beta), p, q)
contact = [
    sp.factor(contact_residual.coeff_monomial(p ** (5 - index) * q**index))
    for index in range(6)
]


def main() -> None:
    print("Np", Np)
    print("Nq", Nq)
    print("contact")
    for index, value in enumerate(contact):
        print(index, value)

    # Linearize in the quadratic Veronese coordinates.
    xx, xy, yy = sp.symbols("xx xy yy")
    lifted = [
        sp.expand(value).subs({x**2: xx, x * y: xy, y**2: yy})
        for value in contact
    ]
    matrix, rhs = sp.linear_eq_to_matrix(lifted, (xx, xy, yy, lam, mu))
    assert rhs == sp.zeros(len(contact), 1)
    print("lifted matrix", matrix.shape)
    print("5x5 minors gcd")
    minors = []
    for omitted in range(matrix.rows):
        rows = [index for index in range(matrix.rows) if index != omitted]
        minor = sp.factor(matrix.extract(rows, range(matrix.cols)).det())
        minors.append(minor)
        print("omit", omitted, minor)
    print("gcd", sp.factor(sp.gcd_list(minors)))

    H = a * c - 16 * a - 48 * b * c + 6 * c + 64
    asol = sp.cancel((48 * b * c - 6 * c - 64) / (c - 16))
    V = (
        408 * b**2 * c**2
        - 6528 * b**2 * c
        + 27648 * b**2
        - 171 * b * c**2
        + 2768 * b * c
        - 12032 * b
        + 18 * c**2
        - 296 * c
        + 1328
    )
    print("H", H)
    matrix_h = sp.simplify(matrix.subs(a, asol))
    print("rank sample", matrix_h.subs({b: sp.Rational(1, 10), c: 4}).rank())

    # Compute the lifted kernel with yy=1 from the generically independent
    # rows 1--4.  Cramer's rule is much faster here than symbolic rref.
    rows = [1, 2, 3, 4]
    unknown_columns = [0, 1, 3, 4]
    square = matrix_h.extract(rows, unknown_columns)
    right = -matrix_h.extract(rows, [2])
    denominator = sp.factor(square.det(method="domain-ge"))
    print("kernel denominator", denominator)
    solution = []
    for column in range(4):
        numerator_matrix = sp.MutableDenseMatrix(square)
        numerator_matrix[:, column] = right
        solution.append(
            sp.factor(
                sp.cancel(
                    numerator_matrix.det(method="domain-ge") / denominator
                )
            )
        )
    vector = [solution[0], solution[1], sp.Integer(1), solution[2], solution[3]]
    print("kernel")
    for value in vector:
        print(value)
    residuals = [
        sp.factor(sp.cancel(value))
        for value in matrix_h * sp.Matrix(vector)
    ]
    print("kernel residuals")
    for value in residuals:
        print(value)
    veronese = sp.factor(sp.cancel(vector[1] ** 2 - vector[0]))
    print("Veronese", veronese)
    print("V", V)

    # The r^2 part of E5 is independent of every lower integration
    # constant.  Reconstruct it on the lifted contact with yy=1.
    top_substitution = {
        a: asol,
        x: vector[1],
        y: 1,
        lam: vector[3],
        mu: vector[4],
    }
    S_top = tuple(sp.factor(value.subs(top_substitution)) for value in S)
    H4_top = sp.Matrix((P.subs(a, asol), Q, 0))
    H3_top = sp.Matrix((r * S_top[0], r * S_top[1], R))
    H2_top = sp.Matrix(
        (
            -vector[3] * r**2 / 2,
            -vector[4] * r**2 / 2,
            r * S_top[2],
        )
    )
    determinant_top = sp.Poly(
        sp.expand(
            (
                t * H2_top.jacobian(variables)
                + t**2 * H3_top.jacobian(variables)
                + t**3 * H4_top.jacobian(variables)
            ).det()
        ),
        t,
    )
    e5_r2 = sp.Poly(
        determinant_top.coeff_monomial(t**5), p, q, r
    )
    print("E5 r2 coefficients")
    obstruction_numerators = []
    for index in range(4):
        coefficient = sp.factor(
            e5_r2.coeff_monomial(p ** (3 - index) * q**index * r**2)
        )
        numerator, denominator_value = sp.cancel(coefficient).as_numer_denom()
        numerator = sp.factor(numerator)
        denominator_value = sp.factor(denominator_value)
        obstruction_numerators.append(numerator)
        print(index, numerator, "/", denominator_value)
    print(
        "obstruction numerator gcd",
        sp.factor(sp.gcd_list(obstruction_numerators)),
    )
    groebner_obstruction = sp.groebner(
        [V] + obstruction_numerators, b, c, order="lex"
    )
    print(
        "V plus E5 numerator Groebner",
        [sp.factor(poly.as_expr()) for poly in groebner_obstruction.polys],
    )


if __name__ == "__main__":
    main()
