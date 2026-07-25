#!/usr/bin/env python3
"""Exact checks for the unresolved double-line line-(2,2) frontier.

The script verifies the degree-seven determinant extraction, both canonical
quadratic pencils, the critical/noncritical outer maps, and the kernel/image
claims used in the critical normal forms.  It does not test or claim that the
remaining leading data extend to a Keller map.
"""

from __future__ import annotations

import sympy as sp


x, y, z = sp.symbols("x y z")
variables = (x, y, z)


def homogeneous_form(prefix: str, degree: int) -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    monomials = []
    for x_degree in range(degree, -1, -1):
        for y_degree in range(degree - x_degree, -1, -1):
            z_degree = degree - x_degree - y_degree
            monomials.append(x**x_degree * y**y_degree * z**z_degree)
    coefficients = sp.symbols(f"{prefix}0:{len(monomials)}")
    return (
        sp.Add(*(coefficient * monomial
                 for coefficient, monomial in zip(coefficients, monomials))),
        coefficients,
    )


def jacobian(first: sp.Expr, second: sp.Expr, third: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix(
            [[sp.diff(form, variable) for variable in variables]
             for form in (first, second, third)]
        ).det()
    )


def vertical_derivative(q_form: sp.Expr, form: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(q_form, y) * sp.diff(form, z)
        - sp.diff(q_form, z) * sp.diff(form, y)
    )


def determinant_extraction_check() -> None:
    scale = sp.symbols("scale")
    quadratic = sp.Matrix(3, 3, sp.symbols("a0:9"))
    cubic = sp.Matrix(3, 3, sp.symbols("b0:9"))
    leading_entries = sp.symbols("c0:6")
    leading = sp.Matrix(
        [
            leading_entries[0:3],
            leading_entries[3:6],
            (0, 0, 0),
        ]
    )
    determinant = sp.expand(
        (scale * quadratic + scale**2 * cubic + scale**3 * leading).det()
    )
    expected = (
        sp.Matrix.vstack(leading[0, :], leading[1, :], quadratic[2, :]).det()
        + sp.Matrix.vstack(leading[0, :], cubic[1, :], cubic[2, :]).det()
        + sp.Matrix.vstack(cubic[0, :], leading[1, :], cubic[2, :]).det()
    )
    actual = sp.Poly(determinant, scale).coeff_monomial(scale**7)
    assert sp.expand(actual - expected) == 0


def specialized_degree_seven_checks() -> None:
    p = x**2
    cubic_first, _ = homogeneous_form("u", 3)
    cubic_second, _ = homogeneous_form("v", 3)
    quadratic_third, _ = homogeneous_form("w", 2)

    pencil_forms = (y * z, y**2 + x * z)
    outer_maps = (
        ("critical", lambda q: (p**2, q**2)),
        ("noncritical", lambda q: (p**2 + q**2, p * q)),
    )

    for q in pencil_forms:
        delta = lambda form: vertical_derivative(q, form)
        for outer_name, outer_map in outer_maps:
            leading_first, leading_second = outer_map(q)
            # Differentiate before substituting p=x^2 to avoid treating p as
            # an independent source variable.
            p_symbol, q_symbol = sp.symbols("p_symbol q_symbol")
            if outer_name == "critical":
                binary_first = p_symbol**2
                binary_second = q_symbol**2
                expected_binary_jacobian = 4 * p_symbol * q_symbol
            else:
                binary_first = p_symbol**2 + q_symbol**2
                binary_second = p_symbol * q_symbol
                expected_binary_jacobian = 2 * (p_symbol**2 - q_symbol**2)
            binary_jacobian = sp.expand(
                sp.diff(binary_first, p_symbol)
                * sp.diff(binary_second, q_symbol)
                - sp.diff(binary_first, q_symbol)
                * sp.diff(binary_second, p_symbol)
            )
            assert sp.expand(binary_jacobian - expected_binary_jacobian) == 0
            kappa = expected_binary_jacobian.subs(
                {p_symbol: p, q_symbol: q}
            )

            cubic_third = x**3
            actual = sp.expand(
                jacobian(leading_first, leading_second, quadratic_third)
                + jacobian(leading_first, cubic_second, cubic_third)
                + jacobian(cubic_first, leading_second, cubic_third)
            )
            first_q = sp.diff(binary_first, q_symbol).subs(
                {p_symbol: p, q_symbol: q}
            )
            second_q = sp.diff(binary_second, q_symbol).subs(
                {p_symbol: p, q_symbol: q}
            )
            expected = x * (
                2 * kappa * delta(quadratic_third)
                + 3 * x
                * (first_q * delta(cubic_second)
                   - second_q * delta(cubic_first))
            )
            assert sp.expand(actual - expected) == 0

            cubic_third = x * q
            actual = sp.expand(
                jacobian(leading_first, leading_second, quadratic_third)
                + jacobian(leading_first, cubic_second, cubic_third)
                + jacobian(cubic_first, leading_second, cubic_third)
            )
            first_p = sp.diff(binary_first, p_symbol).subs(
                {p_symbol: p, q_symbol: q}
            )
            second_p = sp.diff(binary_second, p_symbol).subs(
                {p_symbol: p, q_symbol: q}
            )
            expected = (
                2 * x * kappa * delta(quadratic_third)
                + (q * first_q - 2 * p * first_p) * delta(cubic_second)
                + (2 * p * second_p - q * second_q) * delta(cubic_first)
            )
            assert sp.expand(actual - expected) == 0


def critical_normal_form_checks() -> None:
    p = x**2
    a, b, alpha, beta, gamma = sp.symbols("a b alpha beta gamma")
    ell_x, ell_y, ell_z = sp.symbols("ell_x ell_y ell_z")
    ell = ell_x * x + ell_y * y + ell_z * z

    for index, q in enumerate((y * z, y**2 + x * z)):
        delta = lambda form: vertical_derivative(q, form)

        cubic, cubic_coefficients = homogeneous_form(f"kernel3_{index}_", 3)
        cubic_equations = sp.Poly(delta(cubic), *variables).coeffs()
        cubic_matrix, _ = sp.linear_eq_to_matrix(
            cubic_equations, cubic_coefficients
        )
        assert len(cubic_coefficients) - cubic_matrix.rank() == 2
        assert delta(x**3) == 0
        assert delta(x * q) == 0

        quartic, quartic_coefficients = homogeneous_form(f"kernel4_{index}_", 4)
        quartic_equations = sp.Poly(delta(quartic), *variables).coeffs()
        quartic_matrix, _ = sp.linear_eq_to_matrix(
            quartic_equations, quartic_coefficients
        )
        assert len(quartic_coefficients) - quartic_matrix.rank() == 3
        assert delta(x**4) == 0
        assert delta(x**2 * q) == 0
        assert delta(q**2) == 0

        image_equations = sp.Poly(delta(quartic) - q**2, *variables).coeffs()
        image_matrix, image_rhs = sp.linear_eq_to_matrix(
            image_equations, quartic_coefficients
        )
        assert image_matrix.row_join(image_rhs).rank() > image_matrix.rank()

        arbitrary_quadratic, _ = homogeneous_form(f"critical_w_{index}_", 2)
        cubic_first = (
            4 * x * arbitrary_quadratic + a * x**3 + b * x * q
        ) / 3
        assert sp.expand(
            delta(3 * cubic_first - 4 * x * arbitrary_quadratic)
        ) == 0

        cubic_first = a * x**3 + b * x * q
        quadratic_third = x * ell - gamma * q / 2
        cubic_second = alpha * x**3 + beta * x * q + 2 * q * ell
        critical_equation = (
            q**2 * delta(cubic_first)
            + 2 * x**4 * delta(cubic_second)
            - 4 * x**3 * q * delta(quadratic_third)
        )
        assert sp.expand(critical_equation) == 0


def missed_simultaneous_chart_check() -> None:
    """Check the exact configuration that disproves exhaustiveness."""

    p = x**2
    q = y * z
    leading = sp.Matrix([p**2, 2 * p * q - q**2, 0])
    cubic = sp.Matrix([0, 0, x * q])
    scale = sp.symbols("scope_scale")
    determinant = sp.Poly(
        sp.expand(
            (
                scale**2 * cubic.jacobian(variables)
                + scale**3 * leading.jacobian(variables)
            ).det()
        ),
        scale,
    )
    assert determinant.coeff_monomial(scale**8) == 0
    assert determinant.coeff_monomial(scale**7) == 0


if __name__ == "__main__":
    determinant_extraction_check()
    specialized_degree_seven_checks()
    critical_normal_form_checks()
    missed_simultaneous_chart_check()
    print("PASS: exact line-(2,2) double-line degree-seven regressions")
