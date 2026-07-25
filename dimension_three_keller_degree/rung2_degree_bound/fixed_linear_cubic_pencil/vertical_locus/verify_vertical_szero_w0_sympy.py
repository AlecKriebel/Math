#!/usr/bin/env python3
"""Raw exact certificate for the s=0, W0=0 vertical companion.

The calculation starts with unrestricted H2, unrestricted second cubic
component, and an unrestricted linear part.  It retains every lower-z
coefficient of q on the squarefree and double-root charts and the moduli
on the three minimal triple-root charts.  No exploration/derivation script
is imported.
"""

from __future__ import annotations

import itertools
import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


x, y, z, tau = sp.symbols("x y z tau")
variables = (x, y, z)

mu, nu, omega = sp.symbols("mu nu omega")
eta = sp.symbols("eta")
alpha, beta = sp.symbols("alpha beta")
d0, d1, d2, e0, e1 = sp.symbols("d0 d1 d2 e0 e1")

a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
vcoef = sp.symbols("v0:10")
linear_symbols = sp.symbols(
    "L11 L12 L13 L21 L22 L23 L31 L32 L33"
)
(L11, L12, L13, L21, L22, L23, L31, L32, L33) = linear_symbols

quadratic_monomials = (x**2, x * y, y**2, x * z, y * z, z**2)
cubic_monomials = (
    x**3, x**2 * y, x * y**2, y**3,
    x**2 * z, x * y * z, y**2 * z,
    x * z**2, y * z**2, z**3,
)

A_raw = sum(coefficient * monomial
            for coefficient, monomial in zip(a, quadratic_monomials))
B_raw = sum(coefficient * monomial
            for coefficient, monomial in zip(b, quadratic_monomials))
V_raw = sum(coefficient * monomial
            for coefficient, monomial in zip(vcoef, cubic_monomials))
L_raw = sp.Matrix(3, 3, linear_symbols)

ell = mu * x + nu * y
W = z * (ell + omega * z)
U = sp.Rational(4, 3) * z * W

q_charts = {
    "squarefree": (
        x * y * (x - y)
        + z * (d0 * x**2 + d1 * x * y + d2 * y**2)
        + z**2 * (e0 * x + e1 * y)
        + beta * z**3
    ),
    "double": (
        x**2 * y
        + z * (d0 * x**2 + d1 * x * y + d2 * y**2)
        + z**2 * (e0 * x + e1 * y)
        + beta * z**3
    ),
    "triple_A": x**3 + y**2 * z + alpha * x * z**2 + beta * z**3,
    "triple_B": x**3 + x * y * z + beta * z**3,
    "triple_C": x**3 + y * z**2 + beta * z**3,
}

expected_pivots = {
    "squarefree": (
        ((3, 0, 3), (2, 1, 3), (2, 0, 4), (1, 2, 3), (1, 1, 4)),
        sp.Integer(3888),
    ),
    "double": (
        ((3, 0, 3), (2, 1, 3), (2, 0, 4), (1, 2, 3), (1, 1, 4)),
        sp.Integer(3888),
    ),
    "triple_A": (
        ((3, 0, 3), (2, 1, 3), (2, 0, 4), (1, 1, 4), (0, 1, 5)),
        sp.Integer(-104976),
    ),
    "triple_B": (
        ((3, 0, 3), (2, 1, 3), (2, 0, 4), (1, 0, 5), (0, 1, 5)),
        sp.Integer(-8748),
    ),
    "triple_C": (
        ((3, 0, 3), (2, 1, 3), (2, 0, 4), (1, 0, 5), (0, 0, 6)),
        sp.Integer(-26244),
    ),
}

e6_solution = {
    a[0]: sp.Rational(2, 9) * mu**2,
    a[1]: sp.Rational(4, 9) * mu * nu,
    a[2]: sp.Rational(2, 9) * nu**2,
    a[3]: sp.Rational(4, 9) * mu * omega + sp.Rational(4, 3) * L31,
    a[4]: sp.Rational(4, 9) * nu * omega + sp.Rational(4, 3) * L32,
    a[5]: eta,
}

common_zero_e5 = {
    mu: 0,
    nu: 0,
    L11: sp.Rational(4, 9) * omega * L31,
    L12: sp.Rational(4, 9) * omega * L32,
}

triple_b_nonzero_e5 = {
    nu: 0,
    L32: -mu**2 / 9,
    L31: mu * omega / 3,
    L12: -4 * mu**2 * omega / 81,
    L11: mu * (-12 * L33 + 18 * eta - 4 * omega**2) / 27,
}

triple_c_nonzero_e5 = {
    nu: 0,
    L32: 0,
    L31: mu * omega / 3,
    L12: 4 * mu**3 / 81,
    L11: mu * (-12 * L33 + 18 * eta - 4 * omega**2) / 27,
}


def coefficient(expression: sp.Expr, exponents: tuple[int, int, int]) -> sp.Expr:
    return sp.Poly(sp.expand(expression), x, y, z).coeff_monomial(exponents)


def coefficient_dictionary(expression: sp.Expr) -> dict[tuple[int, int, int], sp.Expr]:
    return dict(sp.Poly(sp.expand(expression), x, y, z).terms())


def same(left: sp.Expr, right: sp.Expr) -> bool:
    return sp.expand(left - right) == 0


def weighted_determinant(q: sp.Expr) -> sp.Poly:
    H4 = sp.Matrix([z**4, z * q, 0])
    H3 = sp.Matrix([U, V_raw, z**3])
    H2 = sp.Matrix([A_raw, B_raw, W])
    matrix = (
        L_raw
        + tau * H2.jacobian(variables)
        + tau**2 * H3.jacobian(variables)
        + tau**3 * H4.jacobian(variables)
    )
    return sp.Poly(sp.expand(matrix.det()), tau)


def check_e6_complete(
    label: str,
    e6: sp.Expr,
) -> None:
    table = coefficient_dictionary(e6)
    equations = list(table.values())
    matrix, _ = sp.linear_eq_to_matrix(equations, a[:5])
    require(matrix.rank() == 5, f"{label}: E6 rank is not five")

    pivot_monomials, expected_determinant = expected_pivots[label]
    pivot_equations = [table[monomial] for monomial in pivot_monomials]
    pivot_matrix, _ = sp.linear_eq_to_matrix(pivot_equations, a[:5])
    require(
        sp.expand(pivot_matrix.det() - expected_determinant) == 0,
        f"{label}: constant E6 pivot determinant mismatch",
    )
    require(
        sp.expand(e6.subs(e6_solution)) == 0,
        f"{label}: proposed complete E6 solution fails",
    )

    # Negative control: the coefficient 2/9 in A0 is detected on every
    # chart, including all three triple-root charts.
    mutated = dict(e6_solution)
    mutated[a[0]] = sp.Rational(1, 9) * mu**2
    require(
        sp.expand(e6.subs(mutated)) != 0,
        f"{label}: E6 failed to detect a mutated A0 coefficient",
    )


def check_e5_classification(
    label: str,
    e5: sp.Expr,
) -> None:
    e5 = sp.expand(e5.subs(e6_solution))

    if label == "squarefree":
        require(same(coefficient(e5, (4, 0, 1)), sp.Rational(4, 9) * mu**3),
                "squarefree: missing mu-cube pivot")
        require(same(coefficient(e5, (0, 4, 1)), sp.Rational(4, 9) * nu**3),
                "squarefree: missing nu-cube pivot")
        require(sp.expand(e5.subs(common_zero_e5)) == 0,
                "squarefree: zero-ell E5 converse fails")
        return

    if label == "double":
        require(same(coefficient(e5, (4, 0, 1)), sp.Rational(4, 9) * mu**3),
                "double: missing mu-cube pivot")
        require(same(coefficient(e5, (1, 3, 1)), -sp.Rational(8, 9) * nu**3),
                "double: missing nu-cube pivot")
        require(sp.expand(e5.subs(common_zero_e5)) == 0,
                "double: zero-ell E5 converse fails")
        return

    if label == "triple_A":
        require(same(coefficient(e5, (2, 2, 1)), -sp.Rational(4, 3) * nu**3),
                "triple_A: missing nu-cube pivot")
        require(
            sp.expand(coefficient(e5, (2, 1, 2)).subs({nu: 0}))
            - sp.Rational(8, 9) * mu**3 == 0,
            "triple_A: missing residual mu-cube pivot",
        )
        require(sp.expand(e5.subs(common_zero_e5)) == 0,
                "triple_A: zero-ell E5 converse fails")
        return

    if label == "triple_B":
        require(same(coefficient(e5, (2, 2, 1)), -sp.Rational(4, 3) * nu**3),
                "triple_B: missing nu-cube pivot")
        e5_nu_zero = sp.expand(e5.subs({nu: 0}))
        require(
            same(
                coefficient(e5_nu_zero, (3, 0, 2)),
                sp.Rational(4, 9) * mu * (9 * L32 + mu**2),
            ),
            "triple_B: first nonzero-mu relation mismatch",
        )
        require(
            same(
                coefficient(e5_nu_zero, (0, 1, 4)),
                -(27 * L12 - 12 * L32 * omega) / 9,
            ),
            "triple_B: L12 relation mismatch",
        )
        require(sp.expand(e5.subs(common_zero_e5)) == 0,
                "triple_B: zero-mu E5 converse fails")
        require(sp.expand(e5.subs(triple_b_nonzero_e5)) == 0,
                "triple_B: nonzero-mu E5 converse fails")
        return

    if label == "triple_C":
        require(same(coefficient(e5, (2, 2, 1)), -sp.Rational(4, 3) * nu**3),
                "triple_C: missing nu-cube pivot")
        e5_nu_zero = sp.expand(e5.subs({nu: 0}))
        require(
            same(coefficient(e5_nu_zero, (3, 0, 2)), 4 * L32 * mu),
            "triple_C: first nonzero-mu relation mismatch",
        )
        require(
            same(
                coefficient(e5_nu_zero, (2, 0, 3)),
                -(81 * L12 - 36 * L32 * omega - 4 * mu**3) / 9,
            ),
            "triple_C: L12 relation mismatch",
        )
        require(sp.expand(e5.subs(common_zero_e5)) == 0,
                "triple_C: zero-mu E5 converse fails")
        require(sp.expand(e5.subs(triple_c_nonzero_e5)) == 0,
                "triple_C: nonzero-mu E5 converse fails")
        return

    raise RuntimeError(f"unknown chart: {label}")


def check_zero_ell_e4(label: str, e4: sp.Expr) -> None:
    e4 = sp.expand(e4.subs(e6_solution).subs(common_zero_e5))
    if label == "squarefree":
        require(same(coefficient(e4, (3, 0, 1)), -sp.Rational(4, 3) * L31**2),
                "squarefree: first E4 square mismatch")
        require(same(coefficient(e4, (0, 3, 1)), -sp.Rational(4, 3) * L32**2),
                "squarefree: second E4 square mismatch")
    elif label == "double":
        require(same(coefficient(e4, (3, 0, 1)), -sp.Rational(4, 3) * L31**2),
                "double: first E4 square mismatch")
        require(same(coefficient(e4, (1, 2, 1)), sp.Rational(8, 3) * L32**2),
                "double: second E4 square mismatch")
    elif label == "triple_A":
        require(same(coefficient(e4, (2, 1, 1)), 4 * L32**2),
                "triple_A: first E4 square mismatch")
        require(same(coefficient(e4, (1, 1, 2)), -sp.Rational(8, 3) * L31**2),
                "triple_A: second E4 square mismatch")
    elif label == "triple_B":
        require(same(coefficient(e4, (2, 1, 1)), 4 * L32**2),
                "triple_B: first E4 square mismatch")
        require(
            sp.expand(coefficient(e4, (2, 0, 2)).subs({L32: 0}))
            + sp.Rational(4, 3) * L31**2 == 0,
            "triple_B: residual E4 square mismatch",
        )
    elif label == "triple_C":
        require(same(coefficient(e4, (2, 1, 1)), 4 * L32**2),
                "triple_C: first E4 square mismatch")
        require(same(coefficient(e4, (1, 0, 3)), -sp.Rational(4, 3) * L31**2),
                "triple_C: second E4 square mismatch")
    else:
        raise RuntimeError(f"unknown chart: {label}")

    normalized_linear = L_raw.subs(common_zero_e5).subs({L31: 0, L32: 0})
    require(sp.expand(normalized_linear.det()) == 0,
            f"{label}: zero-ell branch does not force det L=0")


def check_nonzero_triple_e4(label: str, e4: sp.Expr) -> None:
    e4 = sp.expand(e4.subs(e6_solution))
    if label == "triple_B":
        e4 = sp.expand(e4.subs(triple_b_nonzero_e5))
        c400 = coefficient(e4, (4, 0, 0))
        c211 = coefficient(e4, (2, 1, 1))
        c022 = coefficient(e4, (0, 2, 2))
        require(same(c400, 4 * mu**3 * (mu + 9 * vcoef[1]) / 81),
                "triple_B: c400 mismatch")
        require(same(c211, -4 * mu**3 * (-mu + vcoef[1] - 6 * vcoef[6]) / 27),
                "triple_B: c211 mismatch")
        require(same(c022, 4 * mu**3 * (mu + 18 * vcoef[6]) / 243),
                "triple_B: c022 mismatch")
        require(
            sp.expand(81 * c400 + 243 * c211 - 729 * c022 - 28 * mu**4)
            == 0,
            "triple_B: division-free E4 contradiction mismatch",
        )
        return

    if label == "triple_C":
        e4 = sp.expand(e4.subs(triple_c_nonzero_e5))
        c301 = coefficient(e4, (3, 0, 1))
        c013 = coefficient(e4, (0, 1, 3))
        require(same(c301, 4 * mu**3 * (-2 * mu + 9 * vcoef[5]) / 81),
                "triple_C: c301 mismatch")
        require(same(c013, -4 * mu**3 * (-mu + vcoef[5]) / 27),
                "triple_C: c013 mismatch")
        require(
            sp.expand(81 * c301 + 243 * c013 - 28 * mu**4) == 0,
            "triple_C: division-free E4 contradiction mismatch",
        )
        return

    raise RuntimeError(f"nonzero triple branch requested on {label}")


def main() -> None:
    require(__debug__, "refusing optimized Python: fail-closed checks required")

    results: dict[str, sp.Poly] = {}
    for label, q in q_charts.items():
        determinant = weighted_determinant(q)
        results[label] = determinant
        require(sp.expand(determinant.coeff_monomial(tau**8)) == 0,
                f"{label}: E8 is not identically zero")
        require(sp.expand(determinant.coeff_monomial(tau**7)) == 0,
                f"{label}: E7 is not identically zero")

        e6 = sp.expand(determinant.coeff_monomial(tau**6))
        e5 = sp.expand(determinant.coeff_monomial(tau**5))
        e4 = sp.expand(determinant.coeff_monomial(tau**4))
        check_e6_complete(label, e6)
        check_e5_classification(label, e5)
        check_zero_ell_e4(label, e4)

    check_nonzero_triple_e4(
        "triple_B", results["triple_B"].coeff_monomial(tau**4)
    )
    check_nonzero_triple_e4(
        "triple_C", results["triple_C"].coeff_monomial(tau**4)
    )

    require(
        set(q_charts) == {
            "squarefree", "double", "triple_A", "triple_B", "triple_C"
        },
        "chart coverage changed",
    )
    print(
        "PASS: s=0, W0=0 vertical companion excluded on "
        "2 nontriple + 3 minimal triple-root charts"
    )


if __name__ == "__main__":
    main()
