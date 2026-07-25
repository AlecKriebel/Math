#!/usr/bin/env python3
"""Division-free certificates for the remaining A != 0, w3 = 0 leaves."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: verification requires assertions; do not use -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp


x, y, z, scale = sp.symbols("x y z scale")
variables = (x, y, z)
q = y**2 + x * z
P, Q, R = x**4, x**2 * q, x**3


def exact_zero(value: sp.Expr) -> bool:
    return sp.cancel(sp.expand(value)) == 0


def coefficient(value: sp.Expr, monomial: sp.Expr) -> sp.Expr:
    return sp.Poly(sp.expand(value), x, y, z).coeff_monomial(monomial)


def weighted_determinant(
    U: sp.Expr,
    V: sp.Expr,
    W: sp.Expr,
    H2_first: sp.Expr,
    H2_second: sp.Expr,
    linear_matrix: sp.Matrix,
) -> sp.Poly:
    H4 = sp.Matrix([P, Q, 0])
    H3 = sp.Matrix([U, V, R])
    H2 = sp.Matrix([H2_first, H2_second, W])
    matrix = (
        linear_matrix
        + scale * H2.jacobian(variables)
        + scale**2 * H3.jacobian(variables)
        + scale**3 * H4.jacobian(variables)
    )
    return sp.Poly(sp.expand(matrix.det()), scale)


def check_top_and_parametrized_e6_e5(weighted: sp.Poly) -> None:
    for degree in (9, 8, 7, 6, 5):
        assert exact_zero(weighted.coeff_monomial(scale**degree))


def c3_open_chart() -> None:
    """C3 != 0; C2 is arbitrary."""
    A, C0, C1, C2, C3 = sp.symbols(
        "c3_A c3_C0 c3_C1 c3_C2 c3_C3"
    )
    r, beta, eta, gamma = sp.symbols(
        "c3_r c3_beta c3_eta c3_gamma"
    )
    a0, b0 = sp.symbols("c3_a0 c3_b0")
    l0, l3, l4, l5, l6 = sp.symbols(
        "c3_l0 c3_l3 c3_l4 c3_l5 c3_l6"
    )
    D = C0 - C1

    U = A * x * q
    V = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C3 * x * z**2
    )
    W = sp.Integer(0)
    H2_first = (
        a0 * x**2
        + A * (C0 - r) * x * z
        + A * (C1 - r) * y**2
        + A * C2 * y * z
        + A * C3 * z**2
    )
    H2_second = (
        b0 * x**2
        + beta * x * y
        + (gamma + D * r + eta) * x * z
        + gamma * y**2
        + C2 * r * y * z
        + C3 * r * z**2
    )
    linear = sp.Matrix(
        [
            [l0, A * beta, A * eta],
            [l3, l4, l5],
            [l6, 0, 0],
        ]
    )
    weighted = weighted_determinant(
        U, V, W, H2_first, H2_second, linear
    )
    check_top_and_parametrized_e6_e5(weighted)

    E4 = weighted.coeff_monomial(scale**4)
    S = C1 * r - gamma - r**2
    e0 = coefficient(E4, x**4)
    e1 = coefficient(E4, x**3 * y)
    eS = coefficient(E4, x**2 * y * z)
    assert exact_zero(e0 + 3 * A * (l4 - r * beta))
    assert exact_zero(e1 - 6 * A * (D * S + l5 - r * eta))
    assert exact_zero(eS - 12 * A * C3 * S)

    detL = sp.expand(linear.det())
    certificate = l6 * (
        2 * C3 * linear[0, 1] * e1
        - D * linear[0, 1] * eS
        + 4 * C3 * linear[0, 2] * e0
    )
    assert exact_zero(12 * A * C3 * detL - certificate)
    print(
        "PASS C3!=0 leaf: E4 gives a division-free "
        "12*A*C3*det(L) identity"
    )


def c2_open_chart() -> None:
    """C3 = 0 and C2 != 0."""
    A, C0, C1, C2 = sp.symbols("c2_A c2_C0 c2_C1 c2_C2")
    r, beta, eta, gamma = sp.symbols(
        "c2_r c2_beta c2_eta c2_gamma"
    )
    a0, b0 = sp.symbols("c2_a0 c2_b0")
    l0, l3, l4, l5, l6 = sp.symbols(
        "c2_l0 c2_l3 c2_l4 c2_l5 c2_l6"
    )
    D = C0 - C1

    U = A * x * q
    V = C0 * x**2 * z + C1 * x * y**2 + C2 * x * y * z
    W = sp.Integer(0)
    H2_first = (
        a0 * x**2
        + A * (C0 - r) * x * z
        + A * (C1 - r) * y**2
        + A * C2 * y * z
    )
    H2_second = (
        b0 * x**2
        + beta * x * y
        + (gamma + D * r + eta) * x * z
        + gamma * y**2
        + C2 * r * y * z
    )
    linear = sp.Matrix(
        [
            [l0, A * beta, A * eta],
            [l3, l4, l5],
            [l6, 0, 0],
        ]
    )
    weighted = weighted_determinant(
        U, V, W, H2_first, H2_second, linear
    )
    check_top_and_parametrized_e6_e5(weighted)

    E4 = weighted.coeff_monomial(scale**4)
    S = C1 * r - gamma - r**2
    e0 = coefficient(E4, x**4)
    e1 = coefficient(E4, x**3 * y)
    eS = coefficient(E4, x**3 * z)
    assert exact_zero(e0 + 3 * A * (l4 - r * beta))
    assert exact_zero(e1 - 6 * A * (D * S + l5 - r * eta))
    assert exact_zero(eS + 3 * A * C2 * S)

    detL = sp.expand(linear.det())
    certificate = l6 * (
        C2 * linear[0, 1] * e1
        + 2 * D * linear[0, 1] * eS
        + 2 * C2 * linear[0, 2] * e0
    )
    assert exact_zero(6 * A * C2 * detL - certificate)
    print(
        "PASS C2!=0 leaf: E4 gives a division-free "
        "6*A*C2*det(L) identity"
    )


def aligned_chart() -> None:
    """C2 = C3 = 0, uniformly for every D=C0-C1, including D=0."""
    A, C, D = sp.symbols("al_A al_C al_D")
    rho, beta, eta, gamma = sp.symbols(
        "al_rho al_beta al_eta al_gamma"
    )
    a0, b0 = sp.symbols("al_a0 al_b0")
    l0, l3, l4, l5, l6 = sp.symbols(
        "al_l0 al_l3 al_l4 al_l5 al_l6"
    )

    U = A * x * q
    V = (C + D) * x**2 * z + C * x * y**2
    W = sp.Integer(0)
    H2_first = a0 * x**2 + A * (D + rho) * x * z + A * rho * y**2
    H2_second = (
        b0 * x**2
        + beta * x * y
        + (gamma - D * (rho - C) + eta) * x * z
        + gamma * y**2
    )
    linear = sp.Matrix(
        [
            [l0, A * beta, A * eta],
            [l3, l4, l5],
            [l6, 0, 0],
        ]
    )
    weighted = weighted_determinant(
        U, V, W, H2_first, H2_second, linear
    )
    check_top_and_parametrized_e6_e5(weighted)

    E4 = weighted.coeff_monomial(scale**4)
    e0 = coefficient(E4, x**4)
    e1 = coefficient(E4, x**3 * y)
    S = C * rho - gamma - rho**2
    assert exact_zero(e0 + 3 * A * (l4 + (rho - C) * beta))
    assert exact_zero(
        e1 - 6 * A * (l5 + (rho - C) * eta + D * S)
    )
    assert all(
        exact_zero(value)
        for monomial, value in sp.Poly(E4, x, y, z).terms()
        if monomial not in ((4, 0, 0), (3, 1, 0))
    )

    e4_solution = {
        l4: -(rho - C) * beta,
        l5: -(rho - C) * eta - D * S,
    }
    E3 = sp.expand(
        weighted.coeff_monomial(scale**3).subs(e4_solution)
    )
    e30 = coefficient(E3, x**3)
    e21 = coefficient(E3, x**2 * y)
    assert exact_zero(e30 + 3 * A * beta * S)
    assert exact_zero(e21 + 6 * A * (D * rho - eta) * S)
    assert all(
        exact_zero(value)
        for monomial, value in sp.Poly(E3, x, y, z).terms()
        if monomial not in ((3, 0, 0), (2, 1, 0))
    )

    detL = sp.expand(linear.det().subs(e4_solution))
    assert exact_zero(3 * detL - D * l6 * e30)
    print(
        "PASS aligned leaf (all D): E4 followed by E3 gives the "
        "division-free 3*det(L)=D*l6*[x^3]E3 identity"
    )


if __name__ == "__main__":
    c3_open_chart()
    c2_open_chart()
    aligned_chart()
    print("all w3=0 leaf certificates passed")
