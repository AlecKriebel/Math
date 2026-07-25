#!/usr/bin/env python3
"""Exact regression checks for the quadratic-component exit.

This script checks the algebraic identities and degree bookkeeping used in
WORKING_QUADRATIC_COMPONENT_EXIT.md.  The published bounded-degree plane
theorem and Ax--Grothendieck are literature inputs, not computer claims, and
are audited separately in REPORT.md.
"""

from itertools import product

import sympy as sp


def require(condition: bool, message: str) -> None:
    """Fail even when Python is invoked with optimization."""
    if not condition:
        raise RuntimeError(message)


def polynomial_zero(expression: sp.Expr) -> bool:
    return sp.cancel(sp.expand(expression)) == 0


def check_hessian_basis_identity() -> None:
    """Check what completing a Hessian-kernel vector to a basis does."""
    h11, h12, h13, h22, h23, h33 = sp.symbols(
        "h11 h12 h13 h22 h23 h33"
    )
    H = sp.Matrix(
        [
            [h11, h12, h13],
            [h12, h22, h23],
            [h13, h23, h33],
        ]
    )
    u = sp.Matrix(sp.symbols("u1:4"))
    w = sp.Matrix(sp.symbols("w1:4"))
    v = sp.Matrix(sp.symbols("v1:4"))
    b = sp.Matrix(sp.symbols("b1:4"))
    P = sp.Matrix.hstack(u, w, v)

    transformed_hessian = P.T * H * P
    require(
        all(
            polynomial_zero(entry)
            for entry in transformed_hessian[:, 2] - P.T * (H * v)
        ),
        "third Hessian column is not P^T H v",
    )
    require(
        all(
            polynomial_zero(entry)
            for entry in transformed_hessian[2, :].T - P.T * (H * v)
        ),
        "symmetry does not give the matching third Hessian row",
    )
    require(
        (P.T * b)[2] == (b.T * v)[0],
        "third transformed linear coefficient is not b^T v",
    )


def check_quadratic_coordinate_and_inverse() -> None:
    """Check a fully generic quadratic g and the triangular inverse."""
    x, y, z, X, Y, Z = sp.symbols("x y z X Y Z")
    beta = sp.symbols("beta", nonzero=True)
    coefficients = sp.symbols("a00 a10 a01 a20 a11 a02")
    a00, a10, a01, a20, a11, a02 = coefficients
    g_xy = a00 + a10 * x + a01 * y + a20 * x**2 + a11 * x * y + a02 * y**2
    g_XY = g_xy.subs({x: X, y: Y})

    T = sp.Matrix([x, y, g_xy + beta * z])
    T_inverse = sp.Matrix([X, Y, (Z - g_XY) / beta])

    inverse_after_forward = T_inverse.subs({X: T[0], Y: T[1], Z: T[2]})
    forward_after_inverse = T.subs(
        {x: T_inverse[0], y: T_inverse[1], z: T_inverse[2]},
        simultaneous=True,
    )
    require(
        all(polynomial_zero(value - expected) for value, expected in zip(
            inverse_after_forward, (x, y, z)
        )),
        "T^{-1} o T is not the identity",
    )
    require(
        all(polynomial_zero(value - expected) for value, expected in zip(
            forward_after_inverse, (X, Y, Z)
        )),
        "T o T^{-1} is not the identity",
    )

    determinant_T = sp.det(T.jacobian((x, y, z)))
    determinant_inverse = sp.det(T_inverse.jacobian((X, Y, Z)))
    require(polynomial_zero(determinant_T - beta), "det(JT) != beta")
    require(
        polynomial_zero(determinant_inverse - 1 / beta),
        "det(JT^{-1}) != 1/beta",
    )

    degrees_T = [sp.Poly(component, x, y, z).total_degree() for component in T]
    inverse_numerators = [X, Y, Z - g_XY]
    degrees_inverse = [
        sp.Poly(component, X, Y, Z).total_degree()
        for component in inverse_numerators
    ]
    require(max(degrees_T) == 2, "generic T does not have degree two")
    require(
        max(degrees_inverse) == 2,
        "generic inverse does not have degree two",
    )


def check_composition_degree_bound() -> None:
    """Exhaust all source monomials of total degree at most four."""
    exponents = [
        (i, j, k)
        for i, j, k in product(range(5), repeat=3)
        if i + j + k <= 4
    ]
    pulled_back_degrees = [i + j + 2 * k for i, j, k in exponents]
    require(len(exponents) == 35, "wrong number of ternary monomials through degree four")
    require(max(pulled_back_degrees) == 8, "composition degree bound is not eight")
    require(max(pulled_back_degrees) <= 12, "plane theorem threshold is exceeded")


def check_fibre_jacobian_identity() -> None:
    """Check the determinant of a map (G1,G2,z) on every z-fibre."""
    a, b, c, d, e, f = sp.symbols("a b c d e f")
    jacobian = sp.Matrix(
        [
            [a, b, c],
            [d, e, f],
            [0, 0, 1],
        ]
    )
    fibre_jacobian = sp.Matrix([[a, b], [d, e]])
    require(
        polynomial_zero(jacobian.det() - fibre_jacobian.det()),
        "threefold and fibre Jacobian determinants differ",
    )


def main() -> None:
    check_hessian_basis_identity()
    check_quadratic_coordinate_and_inverse()
    check_composition_degree_bound()
    check_fibre_jacobian_identity()
    print("PASS: exact quadratic-coordinate, degree, and fibre identities verified")


if __name__ == "__main__":
    main()
