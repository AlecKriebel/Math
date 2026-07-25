#!/usr/bin/env python3
"""Independent sparse audit of all three gamma=ell=0 triple charts.

The sparse Laurent-polynomial kernel is loaded from the earlier hostile
audit of the yz^2 chart.  Only its dependency-free arithmetic primitives
are reused: every chart, equation, pivot, and negative control below is
constructed afresh, without importing either supplied SymPy/PARI verifier.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
import itertools
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
check(ARITHMETIC_PATH.is_file(), "independent sparse arithmetic kernel missing")
spec = importlib.util.spec_from_file_location(
    "vertical_triple_sparse_arithmetic",
    ARITHMETIC_PATH,
)
check(spec is not None and spec.loader is not None, "cannot load arithmetic kernel")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)


ALPHA = sp.variable("alpha")


def build_determinant(q, v_form, b_form, linear):
    h4 = (sp.power(sp.Z, 4), sp.mul(sp.Z, q), {})
    h3 = (
        sp.add(
            sp.scale(sp.mul(sp.Z, sp.W), Fraction(4, 3)),
            sp.mul(sp.S, q),
        ),
        v_form,
        sp.power(sp.Z, 3),
    )
    h2 = (sp.A, b_form, sp.W)
    return sp.determinant_of_jets(linear, h2, h3, h4)


def rational_determinant(matrix):
    size = len(matrix)
    check(all(len(row) == size for row in matrix), "nonsquare rational matrix")
    work = [[Fraction(value) for value in row] for row in matrix]
    determinant = Fraction(1)
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant *= pivot_value
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            factor = work[row][column] / pivot_value
            for other_column in range(column + 1, size):
                work[row][other_column] -= (
                    factor * work[column][other_column]
                )
    return determinant


def find_claimed_row_minor(matrix, target_constant, target_polynomial, label):
    """Discover a claimed full-column minor without receiving its row list."""
    column_count = len(matrix[0])
    numeric = [
        [sp.numeric_specialization(entry) for entry in row]
        for row in matrix
    ]
    tested = 0
    numeric_matches = 0
    for rows in itertools.combinations(range(len(matrix)), column_count):
        tested += 1
        numeric_minor = [
            [numeric[row][column] for column in range(column_count)]
            for row in rows
        ]
        if rational_determinant(numeric_minor) != target_constant:
            continue
        numeric_matches += 1
        symbolic_minor = [
            [matrix[row][column] for column in range(column_count)]
            for row in rows
        ]
        if sp.polynomial_determinant(symbolic_minor) == target_polynomial:
            return rows, tested, numeric_matches
    fail(
        f"{label}: no independently discovered minor equals "
        f"{target_constant}*s^7"
    )


def e6_solution(q):
    a_without_z2 = sp.form(
        ("a0", "a1", "a2", "a3", "a4"),
        sp.QUADRATIC_MONOMIALS[:5],
    )
    transverse = sp.add(
        sp.mul(sp.variable("l6"), sp.X),
        sp.mul(sp.variable("l7"), sp.Y),
    )
    return sp.add(
        sp.mul(sp.K, q),
        sp.mul(sp.S_INVERSE, sp.mul(sp.Z, a_without_z2)),
        sp.scale(
            sp.mul(
                sp.S_INVERSE,
                sp.mul(sp.power(sp.Z, 2), transverse),
            ),
            Fraction(-4, 3),
        ),
    )


def after_e5_forms(q):
    a_without_z2 = sp.form(
        ("a0", "a1", "a2", "a3", "a4"),
        sp.QUADRATIC_MONOMIALS[:5],
    )
    v_form = sp.add(
        sp.mul(sp.K, q),
        sp.mul(sp.S_INVERSE, sp.mul(sp.Z, a_without_z2)),
    )
    b_coefficients = (
        sp.mul(sp.S_INVERSE, sp.mul(sp.variable("a0"), sp.K)),
        sp.mul(sp.S_INVERSE, sp.mul(sp.variable("a1"), sp.K)),
        sp.mul(sp.S_INVERSE, sp.mul(sp.variable("a2"), sp.K)),
        sp.mul(
            sp.S_INVERSE,
            sp.add(sp.mul(sp.variable("a3"), sp.K), sp.variable("l0")),
        ),
        sp.mul(
            sp.S_INVERSE,
            sp.add(sp.mul(sp.variable("a4"), sp.K), sp.variable("l1")),
        ),
        sp.variable("b5"),
    )
    b_form = sp.add(
        *(
            sp.mul(coefficient, basis)
            for coefficient, basis in zip(
                b_coefficients,
                sp.QUADRATIC_MONOMIALS,
            )
        )
    )
    return v_form, b_form


Q_C = sp.add(
    sp.power(sp.X, 3),
    sp.mul(sp.power(sp.Y, 2), sp.Z),
    sp.mul(ALPHA, sp.mul(sp.X, sp.power(sp.Z, 2))),
)
Q_B = sp.add(
    sp.power(sp.X, 3),
    sp.mul(sp.X, sp.mul(sp.Y, sp.Z)),
)
Q_E = sp.add(
    sp.power(sp.X, 3),
    sp.mul(sp.Y, sp.power(sp.Z, 2)),
)

CHARTS = {
    "quadratic-y": {
        "q": Q_C,
        "e6": -(2**5) * (3**15),
        "e5": (2**5) * (3**9),
        "e4_pivot": 2 * (3**3),
        "e4": {
            (2, 0, 2): sp.scale(
                sp.add(
                    sp.neg(sp.mul(sp.K, sp.variable("l1"))),
                    sp.mul(sp.S, sp.variable("l4")),
                ),
                9,
            ),
            (0, 1, 3): sp.scale(
                sp.add(
                    sp.neg(sp.mul(sp.K, sp.variable("l0"))),
                    sp.mul(sp.S, sp.variable("l3")),
                ),
                -6,
            ),
            (0, 0, 4): sp.scale(
                sp.mul(
                    ALPHA,
                    sp.add(
                        sp.neg(sp.mul(sp.K, sp.variable("l1"))),
                        sp.mul(sp.S, sp.variable("l4")),
                    ),
                ),
                3,
            ),
        },
        "mu": ((5, 0, 0), -3),
        "lambda": ((3, 1, 1), 2),
    },
    "mixed-xy": {
        "q": Q_B,
        "e6": (2**3) * (3**14),
        "e5": (2**2) * (3**8),
        "e4_pivot": 3**3,
        "e4": {
            (2, 0, 2): sp.scale(
                sp.add(
                    sp.neg(sp.mul(sp.K, sp.variable("l1"))),
                    sp.mul(sp.S, sp.variable("l4")),
                ),
                9,
            ),
            (1, 0, 3): sp.scale(
                sp.add(
                    sp.neg(sp.mul(sp.K, sp.variable("l0"))),
                    sp.mul(sp.S, sp.variable("l3")),
                ),
                -3,
            ),
            (0, 1, 3): sp.scale(
                sp.add(
                    sp.neg(sp.mul(sp.K, sp.variable("l1"))),
                    sp.mul(sp.S, sp.variable("l4")),
                ),
                3,
            ),
        },
        "mu": ((5, 0, 0), -3),
        "lambda": ((4, 0, 1), 1),
    },
    "linear-y": {
        "q": Q_E,
        "e6": -(2**3) * (3**15),
        "e5": (2**4) * (3**8),
        "e4_pivot": 3**3,
        "e4": {
            (2, 0, 2): sp.scale(
                sp.add(
                    sp.neg(sp.mul(sp.K, sp.variable("l1"))),
                    sp.mul(sp.S, sp.variable("l4")),
                ),
                9,
            ),
            (0, 0, 4): sp.scale(
                sp.add(
                    sp.neg(sp.mul(sp.K, sp.variable("l0"))),
                    sp.mul(sp.S, sp.variable("l3")),
                ),
                -3,
            ),
        },
        "mu": ((5, 0, 0), -3),
        "lambda_combo": (((3, 0, 2), 1), ((0, 1, 4), 3), 4),
    },
}


def audit_chart(label, data):
    q = data["q"]
    generic = build_determinant(
        q,
        sp.V_GENERAL,
        sp.B_GENERAL,
        sp.linear_matrix(),
    )
    check(sp.all_zero_in_degree(generic, 8), f"{label}: E8 survives")
    check(sp.all_zero_in_degree(generic, 7), f"{label}: E7 survives")

    e6 = sp.coefficients_of_source_degree(generic, 6)
    all_e6_rows = sorted(e6, reverse=True)
    e6_unknowns = (
        "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8",
        "l6", "l7",
    )
    sp.assert_jointly_linear(e6.values(), e6_unknowns, f"{label} E6")
    e6_matrix = [
        [sp.coefficient_of_parameter(e6[row], name) for name in e6_unknowns]
        for row in all_e6_rows
    ]
    e6_rows, e6_columns = sp.select_pivot(e6_matrix)
    check(len(e6_rows) == 8, f"{label}: E6 rank is not eight")
    e6_minor = [
        [e6_matrix[row][column] for column in e6_columns]
        for row in e6_rows
    ]
    expected_e6 = sp.scale(sp.power(sp.S, 8), data["e6"])
    check(
        sp.polynomial_determinant(e6_minor) == expected_e6,
        f"{label}: independently selected E6 pivot mismatch",
    )

    v_solution = e6_solution(q)
    after_e6 = build_determinant(
        q,
        v_solution,
        sp.B_GENERAL,
        sp.linear_matrix(),
    )
    check(
        sp.all_zero_in_degree(after_e6, 6),
        f"{label}: common E6 family misses an equation",
    )
    e6_negative = build_determinant(
        q,
        sp.add(v_solution, sp.monomial(3, 0, 0)),
        sp.B_GENERAL,
        sp.linear_matrix(),
    )
    check(
        not sp.all_zero_in_degree(e6_negative, 6),
        f"{label}: E6 negative control was not detected",
    )

    e5 = sp.coefficients_of_source_degree(after_e6, 5)
    all_e5_rows = sorted(e5, reverse=True)
    e5_unknowns = ("b0", "b1", "b2", "b3", "b4", "l6", "l7")
    sp.assert_jointly_linear(e5.values(), e5_unknowns, f"{label} E5")
    e5_matrix = [
        [sp.coefficient_of_parameter(e5[row], name) for name in e5_unknowns]
        for row in all_e5_rows
    ]
    independent_rows, independent_columns = sp.select_pivot(e5_matrix)
    check(
        len(independent_rows) == 7
        and independent_columns == tuple(range(7)),
        f"{label}: E5 rank is not seven",
    )
    independent_minor = [
        [e5_matrix[row][column] for column in independent_columns]
        for row in independent_rows
    ]
    check(
        bool(sp.polynomial_determinant(independent_minor)),
        f"{label}: independently selected E5 minor vanished",
    )

    expected_e5 = sp.scale(sp.power(sp.S, 7), data["e5"])
    claimed_rows, tested, matches = find_claimed_row_minor(
        e5_matrix,
        Fraction(data["e5"]),
        expected_e5,
        label,
    )

    mu_key, mu_scalar = data["mu"]
    check(
        e5[mu_key] == sp.scale(sp.mul(sp.S, sp.variable("l7")), mu_scalar),
        f"{label}: displayed mu coefficient mismatch",
    )
    if "lambda" in data:
        lambda_key, lambda_scalar = data["lambda"]
        check(
            e5[lambda_key]
            == sp.scale(sp.mul(sp.S, sp.variable("l6")), lambda_scalar),
            f"{label}: displayed lambda coefficient mismatch",
        )
    else:
        first, second, result_scalar = data["lambda_combo"]
        lambda_combination = sp.add(
            sp.scale(e5[first[0]], first[1]),
            sp.scale(e5[second[0]], second[1]),
        )
        check(
            lambda_combination
            == sp.scale(sp.mul(sp.S, sp.variable("l6")), result_scalar),
            f"{label}: displayed lambda combination mismatch",
        )

    v_after_e5, b_after_e5 = after_e5_forms(q)
    linear_after_e5 = sp.linear_matrix(l6={}, l7={})
    solved = build_determinant(
        q,
        v_after_e5,
        b_after_e5,
        linear_after_e5,
    )
    check(sp.all_zero_in_degree(solved, 6), f"{label}: E6 regressed")
    check(
        sp.all_zero_in_degree(solved, 5),
        f"{label}: common E5 solution misses an equation",
    )
    e5_negative = build_determinant(
        q,
        v_after_e5,
        sp.add(b_after_e5, sp.monomial(2, 0, 0)),
        linear_after_e5,
    )
    check(
        not sp.all_zero_in_degree(e5_negative, 5),
        f"{label}: E5 negative control was not detected",
    )

    e4 = sp.coefficients_of_source_degree(solved, 4)
    check(e4 == data["e4"], f"{label}: complete E4 residual mismatch")
    e4_rows_all = sorted(e4, reverse=True)
    e4_matrix = [
        [
            sp.coefficient_of_parameter(e4[row], name)
            for name in ("l3", "l4")
        ]
        for row in e4_rows_all
    ]
    e4_rows, e4_columns = sp.select_pivot(e4_matrix)
    check(
        len(e4_rows) == 2 and e4_columns == (0, 1),
        f"{label}: E4 rank is not two",
    )
    e4_minor = [
        [e4_matrix[row][column] for column in e4_columns]
        for row in e4_rows
    ]
    expected_e4 = sp.scale(sp.power(sp.S, 2), data["e4_pivot"])
    check(
        sp.polynomial_determinant(e4_minor) == expected_e4,
        f"{label}: E4 pivot mismatch",
    )

    l3_solution = sp.mul(sp.S_INVERSE, sp.mul(sp.K, sp.variable("l0")))
    l4_solution = sp.mul(sp.S_INVERSE, sp.mul(sp.K, sp.variable("l1")))
    final_linear = sp.linear_matrix(
        l3=l3_solution,
        l4=l4_solution,
        l6={},
        l7={},
    )
    final = build_determinant(q, v_after_e5, b_after_e5, final_linear)
    check(sp.all_zero_in_degree(final, 4), f"{label}: final E4 survives")
    check(not sp.det3(final_linear), f"{label}: det(L) is not zero")
    perturbed_linear = sp.linear_matrix(
        l3=sp.add(l3_solution, sp.constant(1)),
        l4=l4_solution,
        l6={},
        l7={},
    )
    check(
        bool(sp.det3(perturbed_linear)),
        f"{label}: det(L) negative control was not detected",
    )

    print(
        f"{label}: E6 rows={tuple(all_e6_rows[row] for row in e6_rows)}, "
        f"columns={tuple(e6_unknowns[column] for column in e6_columns)}"
    )
    print(
        f"{label}: claimed E5 rows discovered={tuple(all_e5_rows[row] for row in claimed_rows)}, "
        f"subsets_tested={tested}, numeric_matches_seen={matches}"
    )
    print(
        f"{label}: E6={data['e6']}*s^8, "
        f"E5={data['e5']}*s^7, E4={data['e4_pivot']}*s^2"
    )


def main():
    for label, data in CHARTS.items():
        audit_chart(label, data)
    print("PASS: independent sparse audit of all triple gamma=ell=0 charts")


if __name__ == "__main__":
    main()
