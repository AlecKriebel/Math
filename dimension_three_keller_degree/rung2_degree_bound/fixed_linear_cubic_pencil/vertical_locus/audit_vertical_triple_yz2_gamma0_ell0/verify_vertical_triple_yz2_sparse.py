#!/usr/bin/env python3
"""Dependency-free hostile check for the vertical q=x^3+y*z^2 chart.

Sparse multivariate Laurent polynomials over Q are implemented below.
The checker constructs det(L+JH2+JH3+JH4) directly and does not import
either supplied CAS certificate or its pivot choices.
"""

from __future__ import annotations

from fractions import Fraction
import sys


if not __debug__:
    raise SystemExit("refusing optimized Python: fail-closed checks required")


NAMES = (
    "x", "y", "z",
    "s", "w", "k", "alpha", "u", "v", "kappa", "c", "t",
    "r20", "r11", "r02", "r10", "r01",
    "g0", "g1", "g2",
    "a0", "a1", "a2", "a3", "a4", "a5",
    "b0", "b1", "b2", "b3", "b4", "b5",
    "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8",
    "l0", "l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8",
)
INDEX = {name: index for index, name in enumerate(NAMES)}
NVAR = len(NAMES)
ZERO = (0,) * NVAR
SOURCE = tuple(INDEX[name] for name in ("x", "y", "z"))


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check(condition, message):
    if not condition:
        fail(message)


def clean(poly):
    return {exponent: value for exponent, value in poly.items() if value}


def constant(value):
    value = Fraction(value)
    return {} if not value else {ZERO: value}


def variable(name, exponent=1):
    powers = [0] * NVAR
    powers[INDEX[name]] = exponent
    return {tuple(powers): Fraction(1)}


def add(*polys):
    answer = {}
    for poly in polys:
        for exponent, coefficient in poly.items():
            answer[exponent] = answer.get(exponent, Fraction(0)) + coefficient
    return clean(answer)


def neg(poly):
    return {exponent: -coefficient for exponent, coefficient in poly.items()}


def sub(left, right):
    return add(left, neg(right))


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return clean(
        {exponent: scalar * coefficient for exponent, coefficient in poly.items()}
    )


def mul(left, right):
    answer = {}
    for exponent_left, coefficient_left in left.items():
        for exponent_right, coefficient_right in right.items():
            exponent = tuple(
                first + second
                for first, second in zip(exponent_left, exponent_right)
            )
            check(
                all(
                    degree >= 0 or position == INDEX["s"]
                    for position, degree in enumerate(exponent)
                ),
                "only s may have a negative exponent",
            )
            answer[exponent] = (
                answer.get(exponent, Fraction(0))
                + coefficient_left * coefficient_right
            )
    return clean(answer)


def power(poly, exponent):
    check(exponent >= 0, "negative power of a general polynomial")
    answer = constant(1)
    base = poly
    remaining = exponent
    while remaining:
        if remaining & 1:
            answer = mul(answer, base)
        remaining >>= 1
        if remaining:
            base = mul(base, base)
    return answer


def derivative(poly, name):
    position = INDEX[name]
    answer = {}
    for exponent, coefficient in poly.items():
        degree = exponent[position]
        if degree:
            reduced = list(exponent)
            reduced[position] -= 1
            reduced = tuple(reduced)
            answer[reduced] = (
                answer.get(reduced, Fraction(0)) + degree * coefficient
            )
    return clean(answer)


def jacobian(forms):
    return [
        [derivative(form, variable_name) for variable_name in ("x", "y", "z")]
        for form in forms
    ]


def det3(matrix):
    return sub(
        add(
            mul(matrix[0][0], mul(matrix[1][1], matrix[2][2])),
            mul(matrix[0][1], mul(matrix[1][2], matrix[2][0])),
            mul(matrix[0][2], mul(matrix[1][0], matrix[2][1])),
        ),
        add(
            mul(matrix[0][2], mul(matrix[1][1], matrix[2][0])),
            mul(matrix[0][1], mul(matrix[1][0], matrix[2][2])),
            mul(matrix[0][0], mul(matrix[1][2], matrix[2][1])),
        ),
    )


def determinant_of_jets(linear, h2, h3, h4):
    j2, j3, j4 = jacobian(h2), jacobian(h3), jacobian(h4)
    return det3(
        [
            [
                add(
                    linear[row][column],
                    j2[row][column],
                    j3[row][column],
                    j4[row][column],
                )
                for column in range(3)
            ]
            for row in range(3)
        ]
    )


def coefficients_of_source_degree(poly, degree):
    answer = {}
    for exponent, coefficient in poly.items():
        xyz = tuple(exponent[position] for position in SOURCE)
        if sum(xyz) != degree:
            continue
        reduced = list(exponent)
        for position in SOURCE:
            reduced[position] = 0
        reduced = tuple(reduced)
        answer.setdefault(xyz, {})
        answer[xyz][reduced] = (
            answer[xyz].get(reduced, Fraction(0)) + coefficient
        )
    return {monomial: clean(value) for monomial, value in answer.items()}


def all_zero_in_degree(poly, degree):
    return all(
        not coefficient
        for coefficient in coefficients_of_source_degree(poly, degree).values()
    )


def assert_jointly_linear(polys, names, label):
    positions = tuple(INDEX[name] for name in names)
    for row, poly in enumerate(polys):
        for exponent in poly:
            check(
                sum(exponent[position] for position in positions) <= 1,
                f"{label}: row {row} is not jointly linear",
            )


def coefficient_of_parameter(poly, name):
    position = INDEX[name]
    answer = {}
    for exponent, coefficient in poly.items():
        check(exponent[position] <= 1, f"nonlinear occurrence of {name}")
        if exponent[position]:
            reduced = list(exponent)
            reduced[position] = 0
            reduced = tuple(reduced)
            answer[reduced] = answer.get(reduced, Fraction(0)) + coefficient
    return clean(answer)


def numeric_specialization(poly):
    """Evaluate s=1 and every other parameter at zero."""
    answer = Fraction(0)
    for exponent, coefficient in poly.items():
        if any(exponent[position] for position in SOURCE):
            fail("source variable survived coefficient extraction")
        if any(
            exponent[INDEX[name]]
            for name in NAMES
            if name not in ("x", "y", "z", "s")
        ):
            continue
        answer += coefficient
    return answer


def rational_rank(matrix):
    if not matrix:
        return 0
    work = [[Fraction(entry) for entry in row] for row in matrix]
    next_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(next_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[next_row], work[pivot] = work[pivot], work[next_row]
        pivot_value = work[next_row][column]
        work[next_row] = [value / pivot_value for value in work[next_row]]
        for row in range(len(work)):
            if row == next_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[next_row])
            ]
        next_row += 1
    return next_row


def select_pivot(matrix):
    """Greedy exact elimination at a fixed specialization."""
    numeric = [
        [numeric_specialization(entry) for entry in row]
        for row in matrix
    ]
    work = [row[:] for row in numeric]
    row_ids = list(range(len(work)))
    rows, columns = [], []
    next_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(next_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[next_row], work[pivot] = work[pivot], work[next_row]
        row_ids[next_row], row_ids[pivot] = row_ids[pivot], row_ids[next_row]
        pivot_value = work[next_row][column]
        for row in range(next_row + 1, len(work)):
            if not work[row][column]:
                continue
            factor = work[row][column] / pivot_value
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[next_row])
            ]
        rows.append(row_ids[next_row])
        columns.append(column)
        next_row += 1
    check(
        len(rows) == rational_rank(numeric),
        "pivot selection disagrees with independent rank reduction",
    )
    return tuple(sorted(rows)), tuple(sorted(columns))


def polynomial_determinant(matrix):
    size = len(matrix)
    check(all(len(row) == size for row in matrix), "nonsquare determinant")
    if size == 0:
        return constant(1)
    if size == 1:
        return matrix[0][0]
    row_counts = [sum(bool(entry) for entry in row) for row in matrix]
    column_counts = [
        sum(bool(matrix[row][column]) for row in range(size))
        for column in range(size)
    ]
    row_choice = min(range(size), key=lambda row: row_counts[row])
    column_choice = min(range(size), key=lambda column: column_counts[column])
    answer = {}
    if row_counts[row_choice] <= column_counts[column_choice]:
        for column, entry in enumerate(matrix[row_choice]):
            if not entry:
                continue
            minor = [
                [
                    matrix[row][other_column]
                    for other_column in range(size)
                    if other_column != column
                ]
                for row in range(size)
                if row != row_choice
            ]
            term = mul(entry, polynomial_determinant(minor))
            answer = add(
                answer,
                term if (row_choice + column) % 2 == 0 else neg(term),
            )
    else:
        for row in range(size):
            entry = matrix[row][column_choice]
            if not entry:
                continue
            minor = [
                [
                    matrix[other_row][column]
                    for column in range(size)
                    if column != column_choice
                ]
                for other_row in range(size)
                if other_row != row
            ]
            term = mul(entry, polynomial_determinant(minor))
            answer = add(
                answer,
                term if (row + column_choice) % 2 == 0 else neg(term),
            )
    return clean(answer)


X, Y, Z = variable("x"), variable("y"), variable("z")
S, W_PARAMETER, K = variable("s"), variable("w"), variable("k")
S_INVERSE = variable("s", -1)


def monomial(x_degree, y_degree, z_degree):
    return mul(power(X, x_degree), mul(power(Y, y_degree), power(Z, z_degree)))


QUADRATIC_MONOMIALS = (
    monomial(2, 0, 0),
    monomial(1, 1, 0),
    monomial(0, 2, 0),
    monomial(1, 0, 1),
    monomial(0, 1, 1),
    monomial(0, 0, 2),
)
CUBIC_MONOMIALS_NO_Z3 = (
    monomial(3, 0, 0),
    monomial(2, 1, 0),
    monomial(1, 2, 0),
    monomial(0, 3, 0),
    monomial(2, 0, 1),
    monomial(1, 1, 1),
    monomial(0, 2, 1),
    monomial(1, 0, 2),
    monomial(0, 1, 2),
)


def form(names, monomials):
    return add(
        *(
            mul(variable(name), basis)
            for name, basis in zip(names, monomials)
        )
    )


def linear_matrix(l3=None, l4=None, l6=None, l7=None):
    matrix = [
        [variable(f"l{3 * row + column}") for column in range(3)]
        for row in range(3)
    ]
    replacements = ((1, 0, l3), (1, 1, l4), (2, 0, l6), (2, 1, l7))
    for row, column, value in replacements:
        if value is not None:
            matrix[row][column] = value
    return matrix


A = form(("a0", "a1", "a2", "a3", "a4", "a5"), QUADRATIC_MONOMIALS)
B_GENERAL = form(
    ("b0", "b1", "b2", "b3", "b4", "b5"),
    QUADRATIC_MONOMIALS,
)
V_GENERAL = form(
    ("v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8"),
    CUBIC_MONOMIALS_NO_Z3,
)
Q = add(power(X, 3), mul(Y, power(Z, 2)))
W = mul(W_PARAMETER, power(Z, 2))


def build_determinant(v_form, b_form, linear):
    h4 = (power(Z, 4), mul(Z, Q), {})
    h3 = (
        add(scale(mul(Z, W), Fraction(4, 3)), mul(S, Q)),
        v_form,
        power(Z, 3),
    )
    h2 = (A, b_form, W)
    return determinant_of_jets(linear, h2, h3, h4)


def main():
    generic = build_determinant(V_GENERAL, B_GENERAL, linear_matrix())
    check(all_zero_in_degree(generic, 8), "E8 survives the gauge")
    check(all_zero_in_degree(generic, 7), "E7 survives the gauge")

    e6 = coefficients_of_source_degree(generic, 6)
    e6_rows_all = sorted(e6, reverse=True)
    e6_unknowns = (
        "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8",
        "l6", "l7",
    )
    assert_jointly_linear(e6.values(), e6_unknowns, "E6")
    e6_matrix = [
        [coefficient_of_parameter(e6[row], name) for name in e6_unknowns]
        for row in e6_rows_all
    ]
    e6_rows, e6_columns = select_pivot(e6_matrix)
    check(len(e6_rows) == 8, "E6 specialized rank is not eight")
    e6_pivot = [
        [e6_matrix[row][column] for column in e6_columns]
        for row in e6_rows
    ]
    e6_determinant = polynomial_determinant(e6_pivot)
    check(
        e6_determinant == scale(power(S, 8), -(2**3) * (3**15)),
        f"unexpected E6 pivot {e6_determinant}",
    )

    a_without_z2 = form(
        ("a0", "a1", "a2", "a3", "a4"),
        QUADRATIC_MONOMIALS[:5],
    )
    transverse = add(mul(variable("l6"), X), mul(variable("l7"), Y))
    v_solution = add(
        mul(K, Q),
        mul(S_INVERSE, mul(Z, a_without_z2)),
        scale(
            mul(S_INVERSE, mul(power(Z, 2), transverse)),
            Fraction(-4, 3),
        ),
    )
    after_e6 = build_determinant(v_solution, B_GENERAL, linear_matrix())
    check(all_zero_in_degree(after_e6, 6), "displayed E6 family is incomplete")
    e6_negative = build_determinant(
        add(v_solution, monomial(3, 0, 0)),
        B_GENERAL,
        linear_matrix(),
    )
    check(
        not all_zero_in_degree(e6_negative, 6),
        "E6 negative control was not detected",
    )

    e5 = coefficients_of_source_degree(after_e6, 5)
    e5_rows_all = sorted(e5, reverse=True)
    e5_unknowns = ("b0", "b1", "b2", "b3", "b4", "l6", "l7")
    check(len(e5_rows_all) == 7, "E5 does not have exactly seven equations")
    assert_jointly_linear(e5.values(), e5_unknowns, "E5")
    e5_matrix = [
        [coefficient_of_parameter(e5[row], name) for name in e5_unknowns]
        for row in e5_rows_all
    ]
    e5_rows, e5_columns = select_pivot(e5_matrix)
    check(
        e5_rows == tuple(range(7)) and e5_columns == tuple(range(7)),
        "E5 is not a full square pivot",
    )
    e5_determinant = polynomial_determinant(e5_matrix)
    check(
        e5_determinant == scale(power(S, 7), (2**4) * (3**8)),
        f"unexpected E5 determinant {e5_determinant}",
    )
    check(
        e5[(5, 0, 0)] == scale(mul(S, variable("l7")), -3),
        "x^5 coefficient does not kill l32",
    )
    lambda_combination = add(
        e5[(3, 0, 2)],
        scale(e5[(0, 1, 4)], 3),
    )
    check(
        lambda_combination == scale(mul(S, variable("l6")), 4),
        "E5 coefficient combination does not kill l31",
    )

    b_solution_coefficients = (
        mul(S_INVERSE, mul(variable("a0"), K)),
        mul(S_INVERSE, mul(variable("a1"), K)),
        mul(S_INVERSE, mul(variable("a2"), K)),
        mul(
            S_INVERSE,
            add(mul(variable("a3"), K), variable("l0")),
        ),
        mul(
            S_INVERSE,
            add(mul(variable("a4"), K), variable("l1")),
        ),
        variable("b5"),
    )
    b_solution = add(
        *(
            mul(coefficient, basis)
            for coefficient, basis in zip(
                b_solution_coefficients,
                QUADRATIC_MONOMIALS,
            )
        )
    )
    v_after_e5 = add(mul(K, Q), mul(S_INVERSE, mul(Z, a_without_z2)))
    linear_after_e5 = linear_matrix(l6={}, l7={})
    after_e5 = build_determinant(
        v_after_e5,
        b_solution,
        linear_after_e5,
    )
    check(all_zero_in_degree(after_e5, 6), "E6 fails after E5 solution")
    check(all_zero_in_degree(after_e5, 5), "displayed E5 solution is incomplete")
    b_negative = build_determinant(
        v_after_e5,
        add(b_solution, monomial(2, 0, 0)),
        linear_after_e5,
    )
    check(
        not all_zero_in_degree(b_negative, 5),
        "E5 negative control was not detected",
    )

    e4 = coefficients_of_source_degree(after_e5, 4)
    expected_e4 = {
        (2, 0, 2): scale(
            add(neg(mul(K, variable("l1"))), mul(S, variable("l4"))),
            9,
        ),
        (0, 0, 4): scale(
            add(neg(mul(K, variable("l0"))), mul(S, variable("l3"))),
            -3,
        ),
    }
    check(e4 == expected_e4, f"incomplete E4 residual {e4}")
    e4_rows = sorted(e4, reverse=True)
    e4_matrix = [
        [
            coefficient_of_parameter(e4[row], name)
            for name in ("l3", "l4")
        ]
        for row in e4_rows
    ]
    check(
        polynomial_determinant(e4_matrix) == scale(power(S, 2), 27),
        "E4 proportionality pivot is not 27*s^2",
    )

    l3_solution = mul(S_INVERSE, mul(K, variable("l0")))
    l4_solution = mul(S_INVERSE, mul(K, variable("l1")))
    final_linear = linear_matrix(
        l3=l3_solution,
        l4=l4_solution,
        l6={},
        l7={},
    )
    final_determinant = build_determinant(
        v_after_e5,
        b_solution,
        final_linear,
    )
    check(all_zero_in_degree(final_determinant, 4), "final E4 does not vanish")
    check(not det3(final_linear), "final linear matrix is not singular")
    negative_linear = linear_matrix(
        l3=add(l3_solution, constant(1)),
        l4=l4_solution,
        l6={},
        l7={},
    )
    check(
        bool(det3(negative_linear)),
        "det(L) negative control was not detected",
    )

    print(
        "E6 rows=",
        tuple(e6_rows_all[row] for row in e6_rows),
        "columns=",
        tuple(e6_unknowns[column] for column in e6_columns),
    )
    print(
        f"E6 pivot={-(2**3) * (3**15)}*s^8; "
        f"E5 pivot={(2**4) * (3**8)}*s^7; E4 pivot=27*s^2"
    )
    print("PASS: independent sparse audit of vertical yz2 chart")


if __name__ == "__main__":
    main()
