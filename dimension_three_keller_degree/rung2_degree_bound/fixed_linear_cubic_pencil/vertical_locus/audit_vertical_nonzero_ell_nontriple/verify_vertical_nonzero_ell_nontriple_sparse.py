#!/usr/bin/env python3
"""Dependency-free hostile audit of the nonzero-ell nontriple lemma.

This checker builds both the raw Jacobian determinant and exterior
multilinear E6/E5 formulas over a custom sparse polynomial ring.  It
imports no equation, pivot, or CAS result from the supplied verifier.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import sys


if not __debug__:
    raise SystemExit("refusing optimized Python: fail-closed checks required")


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check(condition, message):
    if not condition:
        fail(message)


ARITHMETIC_PATH = (
    Path(__file__).resolve().parent.parent
    / "audit_vertical_triple_yz2_gamma0_ell0"
    / "verify_vertical_triple_yz2_sparse.py"
)
check(ARITHMETIC_PATH.is_file(), "sparse arithmetic kernel missing")
spec = importlib.util.spec_from_file_location(
    "vertical_nonzero_ell_sparse_arithmetic",
    ARITHMETIC_PATH,
)
check(spec is not None and spec.loader is not None, "cannot load arithmetic kernel")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)


U_PARAMETER = sp.variable("u")
V_PARAMETER = sp.variable("v")
KAPPA = sp.variable("kappa")
COLLISION_SCALE = sp.variable("c")
COLLISION_PARAMETER = sp.variable("t")

Q_TAIL = sp.add(
    sp.mul(sp.variable("r20"), sp.monomial(2, 0, 1)),
    sp.mul(sp.variable("r11"), sp.monomial(1, 1, 1)),
    sp.mul(sp.variable("r02"), sp.monomial(0, 2, 1)),
    sp.mul(sp.variable("r10"), sp.monomial(1, 0, 2)),
    sp.mul(sp.variable("r01"), sp.monomial(0, 1, 2)),
)
V_TAIL = sp.form(
    ("v4", "v5", "v6", "v7", "v8"),
    sp.CUBIC_MONOMIALS_NO_Z3[4:],
)
V0_GENERAL = sp.form(
    ("v0", "v1", "v2", "v3"),
    sp.CUBIC_MONOMIALS_NO_Z3[:4],
)
Q0_SQUAREFREE = sp.sub(
    sp.mul(sp.power(sp.X, 2), sp.Y),
    sp.mul(sp.X, sp.power(sp.Y, 2)),
)
Q0_DOUBLE = sp.mul(sp.power(sp.X, 2), sp.Y)


def xy_bracket(first, second):
    return sp.sub(
        sp.mul(sp.derivative(first, "x"), sp.derivative(second, "y")),
        sp.mul(sp.derivative(first, "y"), sp.derivative(second, "x")),
    )


def jacobian_triple(first, second, third):
    return sp.det3(sp.jacobian((first, second, third)))


def linear_form(row):
    offset = 3 * row
    return sp.add(
        sp.mul(sp.variable(f"l{offset}"), sp.X),
        sp.mul(sp.variable(f"l{offset + 1}"), sp.Y),
        sp.mul(sp.variable(f"l{offset + 2}"), sp.Z),
    )


def build_data(
    q0,
    ell,
    v0_form,
    l6_form,
    l7_form,
    s_multiplier=1,
    w0_form=None,
):
    q = sp.add(q0, Q_TAIL)
    if w0_form is None:
        w0_form = {}
    w_form = sp.add(
        w0_form,
        sp.mul(
            sp.Z,
            sp.add(ell, sp.mul(sp.variable("w"), sp.Z)),
        ),
    )
    v_form = sp.add(v0_form, V_TAIL)
    linear = sp.linear_matrix(l6=l6_form, l7=l7_form)
    p = sp.power(sp.Z, 4)
    capital_q = sp.mul(sp.Z, q)
    r = sp.power(sp.Z, 3)
    first_cubic = sp.add(
        sp.scale(sp.mul(sp.Z, w_form), Fraction(4, 3)),
        sp.scale(sp.mul(sp.S, q), s_multiplier),
    )
    h2 = (sp.A, sp.B_GENERAL, w_form)
    h3 = (first_cubic, v_form, r)
    h4 = (p, capital_q, {})
    raw = sp.determinant_of_jets(linear, h2, h3, h4)

    l1 = linear_form(0)
    l2 = linear_form(1)
    l3 = sp.add(
        sp.mul(l6_form, sp.X),
        sp.mul(l7_form, sp.Y),
        sp.mul(sp.variable("l8"), sp.Z),
    )
    exterior_e6 = sp.add(
        jacobian_triple(p, capital_q, l3),
        jacobian_triple(first_cubic, capital_q, w_form),
        jacobian_triple(p, v_form, w_form),
        jacobian_triple(sp.A, capital_q, r),
        jacobian_triple(first_cubic, v_form, r),
        jacobian_triple(p, sp.B_GENERAL, r),
    )
    exterior_e5 = sp.add(
        jacobian_triple(first_cubic, capital_q, l3),
        jacobian_triple(p, v_form, l3),
        jacobian_triple(sp.A, capital_q, w_form),
        jacobian_triple(first_cubic, v_form, w_form),
        jacobian_triple(p, sp.B_GENERAL, w_form),
        jacobian_triple(l1, capital_q, r),
        jacobian_triple(sp.A, v_form, r),
        jacobian_triple(first_cubic, sp.B_GENERAL, r),
        jacobian_triple(p, l2, r),
    )
    return raw, exterior_e6, exterior_e5


def source_plane_part(poly, degree):
    answer = {}
    for exponent, coefficient in poly.items():
        xyz = tuple(exponent[position] for position in sp.SOURCE)
        if sum(xyz) != degree or xyz[2] != 0:
            continue
        answer[exponent] = answer.get(exponent, Fraction(0)) + coefficient
    return sp.clean(answer)


def matrix_from_binary_equation(equation, unknowns, degree):
    rows = []
    for y_degree in range(degree + 1):
        monomial_key = (degree - y_degree, y_degree, 0)
        coefficient = sp.coefficients_of_source_degree(
            equation,
            degree,
        ).get(monomial_key, {})
        rows.append(
            [
                sp.coefficient_of_parameter(coefficient, unknown)
                for unknown in unknowns
            ]
        )
    sp.assert_jointly_linear(
        sp.coefficients_of_source_degree(equation, degree).values(),
        unknowns,
        "binary equation",
    )
    return rows


def matrix_minor(matrix, rows, columns):
    return sp.polynomial_determinant(
        [[matrix[row][column] for column in columns] for row in rows]
    )


def matrix_vector(matrix, vector):
    return [
        sp.add(
            *(sp.mul(entry, coordinate) for entry, coordinate in zip(row, vector))
        )
        for row in matrix
    ]


def check_zero_vector(vector, message):
    check(all(not entry for entry in vector), message)


def binary_equation(q0, ell):
    l3_binary = sp.add(
        sp.mul(sp.variable("l6"), sp.X),
        sp.mul(sp.variable("l7"), sp.Y),
    )
    return sp.sub(
        sp.mul(ell, xy_bracket(q0, V0_GENERAL)),
        sp.mul(q0, xy_bracket(q0, l3_binary)),
    )


def audit_w0_reduction():
    ell = sp.add(
        sp.mul(U_PARAMETER, sp.X),
        sp.mul(V_PARAMETER, sp.Y),
    )
    w0 = sp.form(
        ("g0", "g1", "g2"),
        sp.QUADRATIC_MONOMIALS[:3],
    )
    for label, q0 in (
        ("squarefree", Q0_SQUAREFREE),
        ("double", Q0_DOUBLE),
    ):
        raw, exterior_e6, _ = build_data(
            q0,
            ell,
            V0_GENERAL,
            sp.variable("l6"),
            sp.variable("l7"),
            w0_form=w0,
        )
        check(
            sp.coefficients_of_source_degree(raw, 6)
            == sp.coefficients_of_source_degree(exterior_e6, 6),
            f"{label}: raw/exterior E6 mismatch before W0 reduction",
        )
        expected = sp.neg(
            sp.mul(sp.S, sp.mul(q0, xy_bracket(q0, w0)))
        )
        check(
            source_plane_part(raw, 6) == expected,
            f"{label}: W0 plane reduction mismatch",
        )
        bracket_matrix = matrix_from_binary_equation(
            xy_bracket(q0, w0),
            ("g0", "g1", "g2"),
            3,
        )
        check(
            matrix_minor(bracket_matrix, (0, 1, 2), (0, 1, 2))
            == sp.constant(-8),
            f"{label}: W0 bracket map is not injective",
        )


def audit_raw_binary_identity(label, q0):
    ell = sp.add(
        sp.mul(U_PARAMETER, sp.X),
        sp.mul(V_PARAMETER, sp.Y),
    )
    raw, _, exterior_e5 = build_data(
        q0,
        ell,
        V0_GENERAL,
        sp.variable("l6"),
        sp.variable("l7"),
    )
    raw_e5 = sp.coefficients_of_source_degree(raw, 5)
    exterior_map = sp.coefficients_of_source_degree(exterior_e5, 5)
    check(raw_e5 == exterior_map, f"{label}: raw/exterior E5 mismatch")
    expected_plane = sp.mul(sp.S, binary_equation(q0, ell))
    check(
        source_plane_part(raw, 5) == expected_plane,
        f"{label}: binary E5 plane identity mismatch",
    )
    check(sp.all_zero_in_degree(raw, 8), f"{label}: E8 survives")
    check(sp.all_zero_in_degree(raw, 7), f"{label}: E7 survives")


def audit_binary_kernels():
    unknowns = ("v0", "v1", "v2", "v3", "l6", "l7")
    ell = sp.add(
        sp.mul(U_PARAMETER, sp.X),
        sp.mul(V_PARAMETER, sp.Y),
    )

    squarefree_matrix = matrix_from_binary_equation(
        binary_equation(Q0_SQUAREFREE, ell),
        unknowns,
        5,
    )
    squarefree_q_kernel = (
        sp.constant(0),
        sp.constant(1),
        sp.constant(-1),
        sp.constant(0),
        sp.constant(0),
        sp.constant(0),
    )
    check_zero_vector(
        matrix_vector(squarefree_matrix, squarefree_q_kernel),
        "squarefree: q0 kernel missing",
    )
    columns = (0, 1, 3, 4, 5)
    squarefree_minors = (
        (
            (0, 1, 2, 3, 4),
            sp.scale(
                sp.mul(
                    U_PARAMETER,
                    sp.add(
                        sp.power(U_PARAMETER, 2),
                        sp.scale(sp.mul(U_PARAMETER, V_PARAMETER), -4),
                        sp.scale(sp.power(V_PARAMETER, 2), -4),
                    ),
                ),
                -27,
            ),
        ),
        (
            (0, 1, 2, 4, 5),
            sp.scale(
                sp.mul(sp.power(U_PARAMETER, 2), V_PARAMETER),
                27,
            ),
        ),
        (
            (1, 2, 3, 4, 5),
            sp.scale(
                sp.mul(
                    V_PARAMETER,
                    sp.add(
                        sp.scale(sp.power(U_PARAMETER, 2), 4),
                        sp.scale(sp.mul(U_PARAMETER, V_PARAMETER), 4),
                        sp.neg(sp.power(V_PARAMETER, 2)),
                    ),
                ),
                27,
            ),
        ),
    )
    for rows, expected in squarefree_minors:
        check(
            matrix_minor(squarefree_matrix, rows, columns) == expected,
            f"squarefree: minor {rows} mismatch",
        )

    double_matrix = matrix_from_binary_equation(
        binary_equation(Q0_DOUBLE, ell),
        unknowns,
        5,
    )
    double_q_kernel = (
        sp.constant(0),
        sp.constant(1),
        sp.constant(0),
        sp.constant(0),
        sp.constant(0),
        sp.constant(0),
    )
    check_zero_vector(
        matrix_vector(double_matrix, double_q_kernel),
        "double: q0 kernel missing",
    )
    expected_double_minor = sp.scale(
        sp.mul(U_PARAMETER, sp.power(V_PARAMETER, 2)),
        108,
    )
    check(
        matrix_minor(
            double_matrix,
            (0, 1, 2, 3, 4),
            (0, 2, 3, 4, 5),
        )
        == expected_double_minor,
        "double: noncollision minor mismatch",
    )

    # Build both collision matrices directly; no specialization of the
    # generic solve is imported.
    double_x_matrix = matrix_from_binary_equation(
        binary_equation(Q0_DOUBLE, sp.mul(COLLISION_SCALE, sp.X)),
        unknowns,
        5,
    )
    check(
        matrix_minor(
            double_x_matrix,
            (0, 1, 2, 3),
            (0, 2, 3, 4),
        )
        == sp.scale(sp.power(COLLISION_SCALE, 3), -54),
        "double ell=c*x: rank-four minor mismatch",
    )
    double_x_extra = (
        sp.constant(0),
        sp.constant(0),
        sp.constant(Fraction(2, 3)),
        sp.constant(0),
        sp.constant(0),
        COLLISION_SCALE,
    )
    check_zero_vector(
        matrix_vector(double_x_matrix, double_q_kernel),
        "double ell=c*x: q0 kernel missing",
    )
    check_zero_vector(
        matrix_vector(double_x_matrix, double_x_extra),
        "double ell=c*x: extra kernel missing",
    )

    double_y_matrix = matrix_from_binary_equation(
        binary_equation(Q0_DOUBLE, sp.mul(COLLISION_SCALE, sp.Y)),
        unknowns,
        5,
    )
    check(
        matrix_minor(
            double_y_matrix,
            (1, 2, 3, 4),
            (0, 2, 3, 5),
        )
        == sp.scale(sp.power(COLLISION_SCALE, 3), 108),
        "double ell=c*y: rank-four minor mismatch",
    )
    double_y_extra = (
        sp.constant(Fraction(1, 3)),
        sp.constant(0),
        sp.constant(0),
        sp.constant(0),
        COLLISION_SCALE,
        sp.constant(0),
    )
    check_zero_vector(
        matrix_vector(double_y_matrix, double_q_kernel),
        "double ell=c*y: q0 kernel missing",
    )
    check_zero_vector(
        matrix_vector(double_y_matrix, double_y_extra),
        "double ell=c*y: extra kernel missing",
    )

    # Negative controls: perturb the two exceptional kernel coefficients.
    bad_x = list(double_x_extra)
    bad_x[2] = sp.add(bad_x[2], sp.constant(1))
    check(
        any(matrix_vector(double_x_matrix, tuple(bad_x))),
        "double ell=c*x: kernel mutation escaped",
    )
    bad_y = list(double_y_extra)
    bad_y[0] = sp.add(bad_y[0], sp.constant(1))
    check(
        any(matrix_vector(double_y_matrix, tuple(bad_y))),
        "double ell=c*y: kernel mutation escaped",
    )


def audit_e4_aside():
    ell = sp.add(
        sp.mul(U_PARAMETER, sp.X),
        sp.mul(V_PARAMETER, sp.Y),
    )
    a0 = sp.form(("a0", "a1", "a2"), sp.QUADRATIC_MONOMIALS[:3])
    b0 = sp.form(("b0", "b1", "b2"), sp.QUADRATIC_MONOMIALS[:3])
    for label, q0 in (
        ("squarefree", Q0_SQUAREFREE),
        ("double", Q0_DOUBLE),
    ):
        raw, _, _ = build_data(
            q0,
            ell,
            sp.mul(KAPPA, q0),
            {},
            {},
        )
        expected = sp.neg(
            sp.mul(
                ell,
                xy_bracket(
                    q0,
                    sp.sub(sp.mul(KAPPA, a0), sp.mul(sp.S, b0)),
                ),
            )
        )
        check(
            source_plane_part(raw, 4) == expected,
            f"{label}: E4 aside mismatch",
        )

        quadratic = sp.form(
            ("a0", "a1", "a2"),
            sp.QUADRATIC_MONOMIALS[:3],
        )
        bracket_matrix = matrix_from_binary_equation(
            xy_bracket(q0, quadratic),
            ("a0", "a1", "a2"),
            3,
        )
        check(
            matrix_minor(bracket_matrix, (0, 1, 2), (0, 1, 2))
            == sp.constant(-8),
            f"{label}: quadratic bracket minor mismatch",
        )


def compare_raw_exterior_e6(label, raw, exterior):
    check(
        sp.coefficients_of_source_degree(raw, 6)
        == sp.coefficients_of_source_degree(exterior, 6),
        f"{label}: raw/exterior E6 mismatch",
    )


def audit_decisive_e6():
    generic_cases = (
        (
            "squarefree",
            Q0_SQUAREFREE,
            sp.add(
                sp.mul(U_PARAMETER, sp.X),
                sp.mul(V_PARAMETER, sp.Y),
            ),
            sp.mul(KAPPA, Q0_SQUAREFREE),
            ((4, 1, 1), sp.mul(sp.S, U_PARAMETER)),
            ((1, 4, 1), sp.neg(sp.mul(sp.S, V_PARAMETER))),
        ),
        (
            "double noncollision",
            Q0_DOUBLE,
            sp.add(
                sp.mul(U_PARAMETER, sp.X),
                sp.mul(V_PARAMETER, sp.Y),
            ),
            sp.mul(KAPPA, Q0_DOUBLE),
            ((4, 1, 1), sp.mul(sp.S, U_PARAMETER)),
            ((3, 2, 1), sp.scale(sp.mul(sp.S, V_PARAMETER), -2)),
        ),
    )
    for label, q0, ell, v0_form, first, second in generic_cases:
        raw, exterior, _ = build_data(q0, ell, v0_form, {}, {})
        compare_raw_exterior_e6(label, raw, exterior)
        e6 = sp.coefficients_of_source_degree(raw, 6)
        check(e6.get(first[0], {}) == first[1], f"{label}: first E6 obstruction")
        check(
            e6.get(second[0], {}) == second[1],
            f"{label}: second E6 obstruction",
        )
        # E4 is deliberately not substituted: A and B remain the fully
        # generic global forms in build_data.  Changing the s*q coefficient
        # is a raw-form negative control for both decisive equations.
        mutated, _, _ = build_data(
            q0,
            ell,
            v0_form,
            {},
            {},
            s_multiplier=2,
        )
        mutated_e6 = sp.coefficients_of_source_degree(mutated, 6)
        check(
            mutated_e6.get(first[0], {}) != first[1]
            and mutated_e6.get(second[0], {}) != second[1],
            f"{label}: decisive E6 negative control escaped",
        )

    collision_cases = (
        (
            "double ell=c*x",
            sp.mul(COLLISION_SCALE, sp.X),
            sp.add(
                sp.mul(KAPPA, Q0_DOUBLE),
                sp.scale(
                    sp.mul(
                        COLLISION_PARAMETER,
                        sp.mul(sp.X, sp.power(sp.Y, 2)),
                    ),
                    Fraction(2, 3),
                ),
            ),
            {},
            sp.mul(COLLISION_SCALE, COLLISION_PARAMETER),
            (4, 1, 1),
            sp.mul(sp.S, COLLISION_SCALE),
        ),
        (
            "double ell=c*y",
            sp.mul(COLLISION_SCALE, sp.Y),
            sp.add(
                sp.mul(KAPPA, Q0_DOUBLE),
                sp.scale(
                    sp.mul(COLLISION_PARAMETER, sp.power(sp.X, 3)),
                    Fraction(1, 3),
                ),
            ),
            sp.mul(COLLISION_SCALE, COLLISION_PARAMETER),
            {},
            (3, 2, 1),
            sp.scale(sp.mul(sp.S, COLLISION_SCALE), -2),
        ),
    )
    for label, ell, v0_form, l6, l7, key, expected in collision_cases:
        raw, exterior, _ = build_data(q0=Q0_DOUBLE, ell=ell, v0_form=v0_form,
                                      l6_form=l6, l7_form=l7)
        compare_raw_exterior_e6(label, raw, exterior)
        e6 = sp.coefficients_of_source_degree(raw, 6)
        check(e6.get(key, {}) == expected, f"{label}: collision obstruction")
        # The obstruction must be independent of the extra kernel parameter.
        check(
            all(exponent[sp.INDEX["t"]] == 0 for exponent in expected),
            f"{label}: expected obstruction depends on t",
        )
        mutated, _, _ = build_data(
            q0=Q0_DOUBLE,
            ell=ell,
            v0_form=v0_form,
            l6_form=l6,
            l7_form=l7,
            s_multiplier=2,
        )
        check(
            sp.coefficients_of_source_degree(mutated, 6).get(key, {})
            != expected,
            f"{label}: collision negative control escaped",
        )


def main():
    audit_w0_reduction()
    audit_raw_binary_identity("squarefree", Q0_SQUAREFREE)
    audit_raw_binary_identity("double", Q0_DOUBLE)
    audit_binary_kernels()
    audit_e4_aside()
    audit_decisive_e6()
    print("PASS: independent sparse audit of nonzero-ell nontriple lemma")


if __name__ == "__main__":
    main()
