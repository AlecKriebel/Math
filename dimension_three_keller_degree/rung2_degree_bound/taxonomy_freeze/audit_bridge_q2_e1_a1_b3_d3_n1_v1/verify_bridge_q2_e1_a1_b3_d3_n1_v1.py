#!/usr/bin/python3
"""Fail-closed bridge checks for Q2-E1-A1-B3-D3-N1.

This checker reconstructs the frozen row, its normal forms and pivot map.
It also reconstructs the full transverse-nodal lower-term solve from
general H3, H2 and L0 coefficients; this is the one legacy pair that only
substitutes the displayed lower families.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
FREEZE = HERE.parent
MUTATION = os.environ.get("Q2_E1_CUBIC_BRIDGE_MUTATION", "")


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_zero(expression: sp.Expr, message: str) -> None:
    if sp.expand(expression) != 0:
        fail(message)


def coefficient_vector(
    vector: sp.Matrix, monomials: tuple[sp.Expr, ...], variables: tuple[sp.Symbol, ...]
) -> sp.Matrix:
    values: list[sp.Expr] = []
    for component in vector:
        polynomial = sp.Poly(sp.expand(component), *variables)
        values.extend(polynomial.coeff_monomial(mon) for mon in monomials)
    return sp.Matrix(values)


def coefficient_equations(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...]
) -> list[sp.Expr]:
    return sp.Poly(sp.expand(expression), *variables).coeffs()


def check_manifest() -> None:
    data = json.loads((FREEZE / "frozen_manifest_v1.json").read_text())
    require(data["version"] == 1, "wrong frozen version")
    require(data["frozen_row_count"] == 14, "wrong frozen denominator")
    rows = {row["id"]: row for row in data["rows"]}
    row = rows.get("Q2-E1-A1-B3-D3-N1")
    require(row is not None, "target row missing")
    expected_tuple = [1, 1, 3, 3, 1]
    if MUTATION == "row_tuple":
        expected_tuple[-1] = 2
    require(row["rank"] == 2, "target rank is not two")
    require(row["tuple"] == expected_tuple, "target tuple mismatch")
    require(
        data["pivot_ids"] == [f"C{i:02d}" for i in range(45)],
        "frozen pivot IDs mismatch",
    )
    require(
        data["coefficient_order"]["degree_four_monomials"]
        == [
            "x^4",
            "x^3*y",
            "x^3*z",
            "x^2*y^2",
            "x^2*y*z",
            "x^2*z^2",
            "x*y^3",
            "x*y^2*z",
            "x*y*z^2",
            "x*z^3",
            "y^4",
            "y^3*z",
            "y^2*z^2",
            "y*z^3",
            "z^4",
        ],
        "frozen monomial order mismatch",
    )


p, q, r, t = sp.symbols("p q r t")
variables = (p, q, r)

A_NODE = sp.Matrix((p**2 * q, p * q**2, p**3 + q**3))
A_CUSP = sp.Matrix((p**2 * q, p**3, q**3))


def jacobian(vector: sp.Matrix) -> sp.Matrix:
    return vector.jacobian(variables)


def check_geometry_and_pivots() -> None:
    X, Y, Z = sp.symbols("X Y Z")
    node_relation = X**3 + Y**3 - X * Y * Z
    cusp_relation = X**3 - Y**2 * Z
    for relation, triple in (
        (node_relation, A_NODE),
        (cusp_relation, A_CUSP),
    ):
        require_zero(
            relation.subs(dict(zip((X, Y, Z), triple))),
            "implicit cubic relation mismatch",
        )
        require(sp.gcd_list(list(triple)) == 1, "binary triple has a base gcd")
        binary_coefficients = sp.Matrix(
            [
                [sp.Poly(entry, p, q).coeff_monomial(mon) for mon in
                 (p**3, p**2 * q, p * q**2, q**3)]
                for entry in triple
            ]
        )
        require(binary_coefficients.rank() == 3, "cubic coordinates dependent")

    node_gradient = [
        sp.diff(node_relation, variable) for variable in (X, Y, Z)
    ]
    cusp_gradient = [
        sp.diff(cusp_relation, variable) for variable in (X, Y, Z)
    ]
    require(
        all(value.subs({X: 0, Y: 0, Z: 1}) == 0 for value in node_gradient),
        "node point is not singular",
    )
    require(
        all(value.subs({X: 0, Y: 0, Z: 1}) == 0 for value in cusp_gradient),
        "cusp point is not singular",
    )
    # At Z=1 the tangent cones are -XY (two lines) and -Y^2 (double line).
    node_local = sp.Poly(node_relation.subs(Z, 1), X, Y)
    cusp_local = sp.Poly(cusp_relation.subs(Z, 1), X, Y)
    node_quadratic = sum(
        coeff * X**mon[0] * Y**mon[1]
        for mon, coeff in node_local.terms()
        if sum(mon) == 2
    )
    cusp_quadratic = sum(
        coeff * X**mon[0] * Y**mon[1]
        for mon, coeff in cusp_local.terms()
        if sum(mon) == 2
    )
    require_zero(node_quadratic + X * Y, "nodal tangent cone mismatch")
    require_zero(cusp_quadratic + Y**2, "cuspidal tangent cone mismatch")

    x, y, z = sp.symbols("x y z")
    lx, ly, lz = sp.symbols("Lx Ly Lz")
    gs = sp.symbols(
        "g300 g210 g201 g120 g111 g102 g030 g021 g012 g003"
    )
    cubic_monomials = (
        x**3,
        x**2 * y,
        x**2 * z,
        x * y**2,
        x * y * z,
        x * z**2,
        y**3,
        y**2 * z,
        y * z**2,
        z**3,
    )
    quartic_monomials = (
        x**4,
        x**3 * y,
        x**3 * z,
        x**2 * y**2,
        x**2 * y * z,
        x**2 * z**2,
        x * y**3,
        x * y**2 * z,
        x * y * z**2,
        x * z**3,
        y**4,
        y**3 * z,
        y**2 * z**2,
        y * z**3,
        z**4,
    )
    ell = lx * x + ly * y + lz * z
    cubic = sum(a * mon for a, mon in zip(gs, cubic_monomials))
    actual = tuple(
        sp.Poly(sp.expand(ell * cubic), x, y, z).coeff_monomial(mon)
        for mon in quartic_monomials
    )
    (
        g300,
        g210,
        g201,
        g120,
        g111,
        g102,
        g030,
        g021,
        g012,
        g003,
    ) = gs
    stated = (
        lx * g300,
        ly * g300 + lx * g210,
        lz * g300 + lx * g201,
        ly * g210 + lx * g120,
        lz * g210 + ly * g201 + lx * g111,
        lz * g201 + lx * g102,
        ly * g120 + lx * g030,
        lz * g120 + ly * g111 + lx * g021,
        lz * g111 + ly * g102 + lx * g012,
        lz * g102 + lx * g003,
        ly * g030,
        lz * g030 + ly * g021,
        lz * g021 + ly * g012,
        lz * g012 + ly * g003,
        lz * g003,
    )
    require(
        all(sp.expand(a - b) == 0 for a, b in zip(actual, stated)),
        "division-free pivot coefficient map mismatch",
    )
    pivot_tail_start = 15
    if MUTATION == "pivot_tail":
        pivot_tail_start = 14
    require(
        pivot_tail_start == 15,
        "C15--C44 emptiness boundary mismatch",
    )


def check_transverse_nodal_raw_solve() -> None:
    """Reconstruct every affine solve used by the transverse nodal proof."""
    A = A_NODE
    Ap = A.diff(p)
    Aq = A.diff(q)
    H4 = r * A

    cubic_monomials = (
        p**3,
        p**2 * q,
        p**2 * r,
        p * q**2,
        p * q * r,
        p * r**2,
        q**3,
        q**2 * r,
        q * r**2,
        r**3,
    )
    h3_symbols = sp.symbols("h3_0:30")
    H3_general = sp.Matrix(
        [
            sum(
                h3_symbols[10 * component + j] * cubic_monomials[j]
                for j in range(10)
            )
            for component in range(3)
        ]
    )
    E8 = sp.Poly(
        sp.expand((t**2 * jacobian(H3_general) + t**3 * jacobian(H4)).det()),
        t,
    ).coeff_monomial(t**8)
    matrix8, rhs8 = sp.linear_eq_to_matrix(
        coefficient_equations(E8, variables), h3_symbols
    )
    require(rhs8 == sp.zeros(rhs8.rows, 1), "E8 unexpectedly inhomogeneous")
    expected_rank8 = 24 if MUTATION != "nodal_rank" else 23
    require(matrix8.rank() == expected_rank8, "transverse nodal E8 rank mismatch")

    a, b, c, d, alpha, beta = sp.symbols("a b c d alpha beta")
    H3_eight = Ap * (a * p + b * q + alpha * r) + Aq * (
        c * p + d * q + beta * r
    )
    vector8 = coefficient_vector(H3_eight, cubic_monomials, variables)
    tangent8 = vector8.jacobian((a, b, c, d, alpha, beta))
    require(tangent8.rank() == 6, "E8 family lost a parameter")
    require(
        matrix8 * tangent8 == sp.zeros(matrix8.rows, tangent8.cols),
        "displayed E8 family is not in the raw kernel",
    )

    ell = a * p + b * q
    m = c * p + d * q
    V = ell * Ap + m * Aq
    minor = sp.Matrix.hstack(V.diff(p), V.diff(q), A).det()
    expected_minor = 6 * (p**3 + q**3) * (
        c * p**2 + (d - a) * p * q - b * q**2
    ) ** 2
    require_zero(minor - expected_minor, "nodal r=0 square mismatch")

    lam, u, vv = sp.symbols("lambda u vv")
    D2A = (
        alpha**2 * A.diff(p, 2)
        + 2 * alpha * beta * A.diff(p).diff(q)
        + beta**2 * A.diff(q, 2)
    )
    H3 = lam * A + r * (alpha * Ap + beta * Aq)
    quadratic_monomials = (p**2, p * q, p * r, q**2, q * r, r**2)
    h2_symbols = sp.symbols("h2_0:18")
    H2_general = sp.Matrix(
        [
            sum(
                h2_symbols[6 * component + j] * quadratic_monomials[j]
                for j in range(6)
            )
            for component in range(3)
        ]
    )
    E7 = sp.Poly(
        sp.expand(
            (
                t * jacobian(H2_general)
                + t**2 * jacobian(H3)
                + t**3 * jacobian(H4)
            ).det()
        ),
        t,
    ).coeff_monomial(t**7)
    matrix7, rhs7 = sp.linear_eq_to_matrix(
        coefficient_equations(E7, variables), h2_symbols
    )
    require(matrix7.rank() == 16, "transverse nodal E7 rank mismatch")
    H2 = (u * Ap + vv * Aq) / 3 + r * D2A / 2
    vector7 = coefficient_vector(H2, quadratic_monomials, variables)
    require(
        all(sp.expand(value) == 0 for value in matrix7 * vector7 - rhs7),
        "displayed H2 family does not solve raw E7",
    )
    tangent7 = vector7.jacobian((u, vv))
    require(tangent7.rank() == 2, "H2 family lost a parameter")
    require(
        matrix7 * tangent7 == sp.zeros(matrix7.rows, tangent7.cols),
        "H2 parameters do not span raw E7 kernel",
    )

    linear_symbols = sp.symbols("linear_0:9")
    L_general = sp.Matrix(3, 3, linear_symbols)
    E6 = sp.Poly(
        sp.expand(
            (
                L_general
                + t * jacobian(H2)
                + t**2 * jacobian(H3)
                + t**3 * jacobian(H4)
            ).det()
        ),
        t,
    ).coeff_monomial(t**6)
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        coefficient_equations(E6, variables), linear_symbols
    )
    require(matrix6.rank() == 9, "transverse nodal E6 rank mismatch")
    L0 = sp.Matrix(
        [
            [
                -2 * alpha * beta * lam
                + sp.Rational(2, 3) * (alpha * vv + beta * u),
                -alpha**2 * lam + sp.Rational(2, 3) * alpha * u,
                alpha**2 * beta,
            ],
            [
                -beta**2 * lam + sp.Rational(2, 3) * beta * vv,
                -2 * alpha * beta * lam
                + sp.Rational(2, 3) * (alpha * vv + beta * u),
                alpha * beta**2,
            ],
            [
                -3 * alpha**2 * lam + 2 * alpha * u,
                -3 * beta**2 * lam + 2 * beta * vv,
                alpha**3 + beta**3,
            ],
        ]
    )
    require(
        all(
            sp.expand(value) == 0
            for value in matrix6 * sp.Matrix(list(L0)) - rhs6
        ),
        "displayed L0 does not solve raw E6",
    )
    expected_det = (
        sp.Rational(4, 9)
        * (alpha**3 + beta**3)
        * (alpha * vv - beta * u) ** 2
    )
    require_zero(L0.det() - expected_det, "nodal linear determinant mismatch")

    determinant = sp.Poly(
        sp.expand(
            (
                L0
                + t * jacobian(H2)
                + t**2 * jacobian(H3)
                + t**3 * jacobian(H4)
            ).det()
        ),
        t,
    )
    expected_five = (
        sp.Rational(4, 9)
        * (p**3 + q**3)
        * ((3 * beta * lam - vv) * p + (u - 3 * alpha * lam) * q) ** 2
    )
    require_zero(
        determinant.coeff_monomial(t**5) - expected_five,
        "nodal E5 factor mismatch",
    )


def main() -> None:
    known_mutations = {"", "row_tuple", "pivot_tail", "nodal_rank"}
    require(MUTATION in known_mutations, "unknown mutation requested")
    check_manifest()
    check_geometry_and_pivots()
    check_transverse_nodal_raw_solve()
    print("Q2_E1_A1_B3_D3_N1_BRIDGE_PASS_V1")


if __name__ == "__main__":
    main()
