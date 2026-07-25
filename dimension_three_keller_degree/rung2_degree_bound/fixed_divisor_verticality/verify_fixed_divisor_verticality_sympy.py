#!/usr/bin/env python3
"""Exact checks for the quartic fixed-divisor verticality principle."""

from __future__ import annotations

if not __debug__:
    raise RuntimeError("verification requires assertions; do not use -O")

from itertools import product

import sympy as sp


x, y, z, s = sp.symbols("x y z s")
variables = (x, y, z)


def jac3(a: sp.Expr, b: sp.Expr, c: sp.Expr) -> sp.Expr:
    return sp.expand(sp.Matrix([a, b, c]).jacobian(variables).det())


def monomials(degree: int) -> tuple[sp.Expr, ...]:
    return tuple(
        x**i * y**j * z ** (degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def coefficient_matrix(
    expressions: tuple[sp.Expr, ...],
    coefficients: tuple[sp.Symbol, ...],
    degree: int,
) -> sp.Matrix:
    equations = []
    for expression in expressions:
        polynomial = sp.Poly(sp.expand(expression), *variables)
        equations.extend(
            polynomial.coeff_monomial(monomial)
            for monomial in monomials(degree)
        )
    matrix, constant = sp.linear_eq_to_matrix(equations, coefficients)
    assert constant == sp.zeros(len(equations), 1)
    return matrix


def formal_weight_eight() -> None:
    linear_symbols = sp.symbols("formalL0:9")
    quadratic_symbols = sp.symbols("formalA0:9")
    cubic_symbols = sp.symbols("formalB0:9")
    leading_symbols = sp.symbols("formalC0:6")
    linear = sp.Matrix(3, 3, linear_symbols)
    quadratic = sp.Matrix(3, 3, quadratic_symbols)
    cubic = sp.Matrix(3, 3, cubic_symbols)
    leading = sp.Matrix(
        [
            leading_symbols[0:3],
            leading_symbols[3:6],
            (0, 0, 0),
        ]
    )
    determinant = sp.Poly(
        (linear + s * quadratic + s**2 * cubic + s**3 * leading).det(),
        s,
    )
    weight_eight = sp.expand(determinant.coeff_monomial(s**8))
    expected = sp.Matrix(
        [leading.row(0), leading.row(1), cubic.row(2)]
    ).det()
    assert sp.expand(weight_eight - expected) == 0


def cubic_kernel_rank(h: sp.Expr, p: sp.Expr, q: sp.Expr) -> int:
    P = sp.expand(h * p)
    Q = sp.expand(h * q)
    cubic_coefficients = sp.symbols("horizontalCubic0:10")
    cubic = sum(
        coefficient * monomial
        for coefficient, monomial in zip(cubic_coefficients, monomials(3))
    )
    matrix = coefficient_matrix(
        (jac3(P, Q, cubic),), cubic_coefficients, 8
    )
    assert matrix.shape == (45, 10)
    return matrix.rank()


def horizontal_samples() -> None:
    # (e,a)=(1,3).  The fixed line z=0 is horizontal because the
    # restrictions of p,q are x^3,y^3.  A common constant annihilating
    # direction would be necessary for a degree-three composition of a
    # linear pencil; the displayed derivative matrix has full rank.
    h13 = z
    p13 = x**3 + y * z**2
    q13 = y**3 + x * z**2
    direction = sp.symbols("direction0:3")
    direction_equations = []
    for form in (p13, q13):
        derivative = sum(
            coefficient * sp.diff(form, variable)
            for coefficient, variable in zip(direction, variables)
        )
        direction_equations.extend(sp.Poly(derivative, *variables).coeffs())
    direction_matrix, direction_constant = sp.linear_eq_to_matrix(
        direction_equations, direction
    )
    assert direction_constant == sp.zeros(len(direction_equations), 1)
    assert direction_matrix.rank() == 3
    assert cubic_kernel_rank(h13, p13, q13) == 10

    # (e,a)=(2,2).  The unique prime z|h is horizontal:
    # p|_{z=0}=x^2 and q|_{z=0}=y^2 are independent.  The determinant
    # below makes the generic conic smooth and hence the pencil minimal.
    h22 = z**2
    p22 = x**2 + y * z
    q22 = y**2 + x * z
    t = sp.symbols("t")
    conic = sp.Poly(p22 - t * q22, *variables)
    symmetric = sp.Matrix(
        [
            [conic.coeff_monomial(x**2), conic.coeff_monomial(x * y) / 2,
             conic.coeff_monomial(x * z) / 2],
            [conic.coeff_monomial(x * y) / 2, conic.coeff_monomial(y**2),
             conic.coeff_monomial(y * z) / 2],
            [conic.coeff_monomial(x * z) / 2,
             conic.coeff_monomial(y * z) / 2,
             conic.coeff_monomial(z**2)],
        ]
    )
    assert sp.factor(symmetric.det() - (t**3 - 1) / 4) == 0
    assert cubic_kernel_rank(h22, p22, q22) == 10

    # (e,a)=(3,1).  The irreducible cubic h is automatically horizontal
    # for the line pencil <x,y>.
    h31 = x**3 + y * z**2
    p31 = x
    q31 = y
    assert sp.factor(h31) == h31
    assert cubic_kernel_rank(h31, p31, q31) == 10


def vertical_witness() -> None:
    h = z**2
    p = z**2
    q = x**2 + y**2
    P = h * p
    Q = h * q
    G = z**3
    assert jac3(P, Q, G) == 0

    t = sp.symbols("verticalT")
    conic = z**2 - t * (x**2 + y**2)
    gradient = [sp.diff(conic, variable) for variable in variables]
    # The three partials have no common projective zero for t != 0.
    assert gradient == [-2 * t * x, -2 * t * y, 2 * z]


def concrete_weight_eight() -> None:
    h = z**2
    p = x**2 + y * z
    q = y**2 + x * z
    H4 = sp.Matrix([h * p, h * q, 0])
    G = x**3 + 2 * x * y * z + 3 * z**3
    H3 = sp.Matrix([x**3 + y**3, x**2 * z + y * z**2, G])
    H2 = sp.Matrix([x**2 + y * z, y**2 + x * z, z**2 + x * y])
    L = sp.Matrix([x + y, y + z, z + x])
    determinant = sp.Poly(
        (L + s * H2 + s**2 * H3 + s**3 * H4)
        .jacobian(variables)
        .det(),
        s,
    )
    assert sp.expand(
        determinant.coeff_monomial(s**8)
        - jac3(H4[0], H4[1], G)
    ) == 0


def main() -> None:
    formal_weight_eight()
    concrete_weight_eight()
    horizontal_samples()
    vertical_witness()
    print("quartic fixed-divisor verticality SymPy checks passed")


if __name__ == "__main__":
    main()
