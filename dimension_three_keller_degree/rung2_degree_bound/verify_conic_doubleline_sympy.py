#!/usr/bin/python3
"""Exact SymPy checks for the unique-double-line conic exclusion.

The proof's rank and cokernel statements are recorded in the note.  This
script checks the canonical-pencil determinants, both degree-seven solution
families, the singular-linear-part degree-six family, the residual
degree-six matrix, its five decisive degree-five coefficients, and the final
rank-two factorization obstruction.
"""

from __future__ import annotations

import sympy as sp


x, y, z, scale = sp.symbols("x y z scale")
variables = (x, y, z)


def ver(first: sp.Expr, second: sp.Expr) -> sp.Matrix:
    return sp.Matrix([first**2, first * second, second**2])


def determinant_coefficient(
    linear: sp.Matrix,
    quadratic: sp.Matrix,
    cubic: sp.Matrix,
    quartic: sp.Matrix,
    degree: int,
) -> sp.Expr:
    determinant = sp.expand(
        (
            linear
            + scale * quadratic.jacobian(variables)
            + scale**2 * cubic.jacobian(variables)
            + scale**3 * quartic.jacobian(variables)
        ).det()
    )
    return sp.expand(sp.Poly(determinant, scale).coeff_monomial(scale**degree))


def canonical_and_degree_seven_checks() -> None:
    parameter = sp.symbols("parameter")
    matrix_yz = sp.Matrix(
        [[1, 0, 0], [0, 0, -parameter / 2], [0, -parameter / 2, 0]]
    )
    matrix_jordan = sp.Matrix(
        [[1, 0, -parameter], [0, -parameter, 0], [-parameter, 0, 0]]
    )
    assert sp.factor(matrix_yz.det()) == -parameter**2 / 4
    assert sp.factor(matrix_jordan.det()) == parameter**3

    alpha, beta, gamma, delta = sp.symbols("alpha beta gamma delta")
    ell_x, ell_y, ell_z = sp.symbols("ell_x ell_y ell_z")
    m_x, m_y, m_z = sp.symbols("m_x m_y m_z")
    ell = ell_x * x + ell_y * y + ell_z * z
    emm = m_x * x + m_y * y + m_z * z
    ell_bar = ell_y * y + ell_z * z
    emm_bar = m_y * y + m_z * z
    u = sp.Matrix(sp.symbols("u1:4"))
    v = sp.Matrix(sp.symbols("v1:4"))
    zero_linear = sp.zeros(3)

    for q_form in (y * z, y**2 + 2 * x * z):
        p_form = x**2
        quartic = ver(p_form, q_form)
        tangent = sp.Matrix(
            [2 * p_form * ell, q_form * ell + p_form * emm, 2 * q_form * emm]
        )
        exceptional = x * sp.Matrix(
            [alpha * q_form + beta * p_form, 0, gamma * q_form + delta * p_form]
        )
        cubic = tangent + exceptional

        alpha_zero_quadratic = (
            ver(ell, emm)
            + x
            * sp.Matrix(
                [
                    sp.Rational(3, 2) * beta * ell_bar,
                    -sp.Rational(1, 4) * gamma * ell_bar,
                    sp.Rational(3, 2) * delta * ell_bar + gamma * emm_bar,
                ]
            )
            + u * p_form
            + v * q_form
        )
        assert determinant_coefficient(
            zero_linear,
            alpha_zero_quadratic,
            cubic.subs(alpha, 0),
            quartic,
            7,
        ) == 0

        ell_zero_cubic = cubic.subs(
            {ell_x: 0, ell_y: 0, ell_z: 0}
        )
        ell_zero_quadratic = (
            ver(0, emm)
            + x * sp.Matrix([alpha * emm_bar, 0, gamma * emm_bar])
            + u * p_form
            + v * q_form
        )
        assert determinant_coefficient(
            zero_linear,
            ell_zero_quadratic,
            ell_zero_cubic,
            quartic,
            7,
        ) == 0

        a_column = sp.Matrix(sp.symbols("a1:4"))
        forced_linear = sp.Matrix.hstack(a_column, v * m_y, v * m_z)
        assert determinant_coefficient(
            forced_linear,
            ell_zero_quadratic,
            ell_zero_cubic,
            quartic,
            6,
        ) == 0
        assert forced_linear.det() == 0


def residual_degree_five_checks() -> None:
    lam, kappa = sp.symbols("lam kappa", nonzero=True)
    beta, gamma, delta = sp.symbols("beta gamma delta")
    u = sp.Matrix(sp.symbols("u1:4"))
    v = sp.Matrix(sp.symbols("v1:4"))
    a_column = sp.Matrix(sp.symbols("a1:4"))
    p_form = x**2
    q_form = y**2 + 2 * x * z
    ell = lam * y
    emm = kappa * z

    quartic = ver(p_form, q_form)
    cubic = (
        sp.Matrix(
            [2 * p_form * ell, q_form * ell + p_form * emm, 2 * q_form * emm]
        )
        + x * sp.Matrix([beta * p_form, 0, gamma * q_form + delta * p_form])
    )
    quadratic = (
        ver(ell, emm)
        + x
        * sp.Matrix(
            [
                sp.Rational(3, 2) * beta * ell,
                -sp.Rational(1, 4) * gamma * ell,
                sp.Rational(3, 2) * delta * ell + gamma * emm,
            ]
        )
        + u * p_form
        + v * q_form
    )
    linear = sp.Matrix(
        [
            [
                a_column[0],
                lam * u[0],
                kappa * v[0] - sp.Rational(3, 4) * beta * lam**2,
            ],
            [
                a_column[1],
                lam * u[1],
                kappa * v[1] + sp.Rational(3, 8) * gamma * lam**2,
            ],
            [
                a_column[2],
                lam * u[2] - sp.Rational(1, 4) * gamma**2 * lam,
                kappa * v[2] - sp.Rational(3, 4) * delta * lam**2,
            ],
        ]
    )

    assert determinant_coefficient(linear, quadratic, cubic, quartic, 6) == 0
    degree_five = sp.Poly(
        determinant_coefficient(linear, quadratic, cubic, quartic, 5),
        x,
        y,
        z,
    )
    expected = {
        x**2 * z**3: 12 * beta * lam**3,
        x * y**4: 2 * lam * (-v[0] * gamma + 2 * a_column[0]),
        x**3 * z**2: 2
        * lam
        * (-4 * v[0] * gamma + 3 * gamma * lam**2 + 8 * a_column[0]),
        x**3 * y**2: -4 * lam * (-v[1] * gamma + 2 * a_column[1]),
        x**4 * z: -lam
        * (-8 * v[1] * gamma - 3 * delta * lam**2 + 16 * a_column[1]),
    }
    for monomial, value in expected.items():
        assert sp.expand(degree_five.coeff_monomial(monomial) - value) == 0


def factorization_top_degree_check() -> None:
    source, first, second, dilation = sp.symbols(
        "source first second dilation"
    )
    a_column = sp.Matrix(sp.symbols("factor_a1:4"))
    u = sp.Matrix(sp.symbols("factor_u1:4"))
    v = sp.Matrix(sp.symbols("factor_v1:4"))
    map_g = (
        a_column * source
        + ver(first, second)
        + u * first
        + v * second
    )
    determinant = sp.expand(map_g.jacobian((source, first, second)).det())
    scaled = sp.Poly(
        sp.expand(determinant.subs({first: dilation * first, second: dilation * second})),
        dilation,
    )
    assert sp.expand(
        scaled.coeff_monomial(dilation**2)
        - 2
        * (
            a_column[0] * second**2
            - 2 * a_column[1] * first * second
            + a_column[2] * first**2
        )
    ) == 0


if __name__ == "__main__":
    canonical_and_degree_seven_checks()
    residual_degree_five_checks()
    factorization_top_degree_check()
    print("PASS: exact SymPy unique-double-line conic regressions")
