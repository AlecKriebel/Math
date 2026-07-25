#!/usr/bin/env python3
"""Independent exact audit of the zero-ell vertical-companion calculation.

This checker is dependency-free.  It implements sparse multivariate Laurent
polynomials over Q from scratch, reconstructs the Jacobian determinant from
the displayed homogeneous forms, and never imports the supplied SymPy
calculation.

The only negative exponents permitted are powers of ``s`` introduced by the
displayed solutions.  Since the lemma assumes s != 0, this is the correct
coefficient ring Q[s,s^-1,...].
"""

from __future__ import annotations

from fractions import Fraction
import sys


if not __debug__:
    raise SystemExit("refusing optimized Python: fail-closed checks required")


NAMES = (
    "x", "y", "z",
    "s", "w", "k",
    "r20", "r11", "r02", "r10", "r01",
    "a0", "a1", "a2", "a3", "a4", "a5",
    "b0", "b1", "b2", "b3", "b4", "b5",
    "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8",
    "l0", "l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8",
)
INDEX = {name: position for position, name in enumerate(NAMES)}
NVAR = len(NAMES)
ZERO_EXPONENT = (0,) * NVAR
SOURCE_POSITIONS = tuple(INDEX[name] for name in ("x", "y", "z"))


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def clean(poly):
    return {exponent: value for exponent, value in poly.items() if value}


def constant(value):
    value = Fraction(value)
    return {} if not value else {ZERO_EXPONENT: value}


def variable(name):
    exponent = [0] * NVAR
    exponent[INDEX[name]] = 1
    return {tuple(exponent): Fraction(1)}


def laurent_power_of_variable(name, exponent):
    powers = [0] * NVAR
    powers[INDEX[name]] = exponent
    return {tuple(powers): Fraction(1)}


def add(*polys):
    result = {}
    for poly in polys:
        for exponent, value in poly.items():
            result[exponent] = result.get(exponent, Fraction(0)) + value
    return clean(result)


def neg(poly):
    return {exponent: -value for exponent, value in poly.items()}


def sub(left, right):
    return add(left, neg(right))


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return clean({exponent: scalar * value for exponent, value in poly.items()})


def mul(left, right):
    result = {}
    for left_exponent, left_value in left.items():
        for right_exponent, right_value in right.items():
            exponent = tuple(
                first + second
                for first, second in zip(left_exponent, right_exponent)
            )
            # Only s may be inverted.
            check(
                all(
                    degree >= 0 or position == INDEX["s"]
                    for position, degree in enumerate(exponent)
                ),
                "negative exponent outside s",
            )
            result[exponent] = (
                result.get(exponent, Fraction(0))
                + left_value * right_value
            )
    return clean(result)


def power(poly, exponent):
    check(exponent >= 0, "negative exponent of a general polynomial")
    result = constant(1)
    base = poly
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = mul(result, base)
        remaining >>= 1
        if remaining:
            base = mul(base, base)
    return result


def derivative(poly, name):
    position = INDEX[name]
    result = {}
    for exponent, value in poly.items():
        degree = exponent[position]
        if degree:
            reduced = list(exponent)
            reduced[position] -= 1
            reduced = tuple(reduced)
            result[reduced] = (
                result.get(reduced, Fraction(0)) + degree * value
            )
    return clean(result)


def det3(matrix):
    positive = add(
        mul(matrix[0][0], mul(matrix[1][1], matrix[2][2])),
        mul(matrix[0][1], mul(matrix[1][2], matrix[2][0])),
        mul(matrix[0][2], mul(matrix[1][0], matrix[2][1])),
    )
    negative = add(
        mul(matrix[0][2], mul(matrix[1][1], matrix[2][0])),
        mul(matrix[0][1], mul(matrix[1][0], matrix[2][2])),
        mul(matrix[0][0], mul(matrix[1][2], matrix[2][1])),
    )
    return sub(positive, negative)


def jacobian(forms):
    return [
        [derivative(form, name) for name in ("x", "y", "z")]
        for form in forms
    ]


def determinant_of_jets(linear, h2, h3, h4):
    jac2, jac3, jac4 = jacobian(h2), jacobian(h3), jacobian(h4)
    matrix = [
        [
            add(
                linear[row][column],
                jac2[row][column],
                jac3[row][column],
                jac4[row][column],
            )
            for column in range(3)
        ]
        for row in range(3)
    ]
    return det3(matrix)


def source_degree_coefficients(poly, degree):
    """Return (x,y,z)-monomial -> coefficient for one source degree."""
    result = {}
    for exponent, value in poly.items():
        xyz = tuple(exponent[position] for position in SOURCE_POSITIONS)
        if sum(xyz) != degree:
            continue
        reduced = list(exponent)
        for position in SOURCE_POSITIONS:
            reduced[position] = 0
        reduced = tuple(reduced)
        result.setdefault(xyz, {})
        result[xyz][reduced] = (
            result[xyz].get(reduced, Fraction(0)) + value
        )
    return {monomial: clean(coefficient) for monomial, coefficient in result.items()}


def coefficient_of_parameter(poly, name):
    """Coefficient of a parameter, asserting linearity in that parameter."""
    position = INDEX[name]
    result = {}
    for exponent, value in poly.items():
        degree = exponent[position]
        check(degree <= 1, f"equation nonlinear in {name}")
        if degree == 1:
            reduced = list(exponent)
            reduced[position] = 0
            reduced = tuple(reduced)
            result[reduced] = result.get(reduced, Fraction(0)) + value
    return clean(result)


def assert_jointly_linear(polys, names, label):
    positions = tuple(INDEX[name] for name in names)
    for equation_number, poly in enumerate(polys):
        for exponent in poly:
            total = sum(exponent[position] for position in positions)
            check(
                total <= 1,
                f"{label}: equation {equation_number} is not jointly linear",
            )


def evaluate_at_origin_except_s(poly):
    """Set s=1 and every other nonsource parameter to zero."""
    value = Fraction(0)
    for exponent, coefficient in poly.items():
        survives = True
        for name in NAMES:
            if name in ("x", "y", "z", "s"):
                continue
            if exponent[INDEX[name]]:
                survives = False
                break
        if survives:
            check(
                all(exponent[position] == 0 for position in SOURCE_POSITIONS),
                "source variable survived coefficient extraction",
            )
            value += coefficient  # s is evaluated at 1, including s^-1.
    return value


def rational_rank(matrix):
    if not matrix:
        return 0
    work = [[Fraction(entry) for entry in row] for row in matrix]
    row_count, column_count = len(work), len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    left - factor * right
                    for left, right in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
    return pivot_row


def select_numeric_pivot(matrix):
    """Select rows and columns without consulting the supplied verifier."""
    numeric = [
        [evaluate_at_origin_except_s(entry) for entry in row]
        for row in matrix
    ]
    work = [row[:] for row in numeric]
    row_ids = list(range(len(work)))
    pivot_rows, pivot_columns = [], []
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
        pivot_rows.append(row_ids[next_row])
        pivot_columns.append(column)
        next_row += 1
        if next_row == len(work):
            break
    check(
        rational_rank(numeric) == len(pivot_rows),
        "pivot-selection rank inconsistency",
    )
    return tuple(pivot_rows), tuple(pivot_columns)


def polynomial_determinant(matrix):
    """Exact determinant by sparse Laplace recursion."""
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
    sparse_row = min(range(size), key=lambda row: row_counts[row])
    sparse_column = min(range(size), key=lambda column: column_counts[column])
    result = {}
    if row_counts[sparse_row] <= column_counts[sparse_column]:
        for column, entry in enumerate(matrix[sparse_row]):
            if not entry:
                continue
            minor = [
                [
                    matrix[row][other_column]
                    for other_column in range(size)
                    if other_column != column
                ]
                for row in range(size)
                if row != sparse_row
            ]
            term = mul(entry, polynomial_determinant(minor))
            result = add(
                result,
                term if (sparse_row + column) % 2 == 0 else neg(term),
            )
    else:
        for row in range(size):
            entry = matrix[row][sparse_column]
            if not entry:
                continue
            minor = [
                [
                    matrix[other_row][column]
                    for column in range(size)
                    if column != sparse_column
                ]
                for other_row in range(size)
                if other_row != row
            ]
            term = mul(entry, polynomial_determinant(minor))
            result = add(
                result,
                term if (row + sparse_column) % 2 == 0 else neg(term),
            )
    return clean(result)


X, Y, Z = (variable(name) for name in ("x", "y", "z"))
S, W_SCALAR, K = (variable(name) for name in ("s", "w", "k"))
S_INV = laurent_power_of_variable("s", -1)


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


def form(coefficient_names, monomials):
    return add(
        *(
            mul(variable(coefficient), basis)
            for coefficient, basis in zip(coefficient_names, monomials)
        )
    )


def generic_linear(l6=None, l7=None, l3=None, l4=None):
    entries = [
        [variable(f"l{3 * row + column}") for column in range(3)]
        for row in range(3)
    ]
    if l6 is not None:
        entries[2][0] = l6
    if l7 is not None:
        entries[2][1] = l7
    if l3 is not None:
        entries[1][0] = l3
    if l4 is not None:
        entries[1][1] = l4
    return entries


A = form(("a0", "a1", "a2", "a3", "a4", "a5"), QUADRATIC_MONOMIALS)
B_GENERIC = form(("b0", "b1", "b2", "b3", "b4", "b5"), QUADRATIC_MONOMIALS)
W_FORM = mul(W_SCALAR, power(Z, 2))
V_GENERIC = form(
    ("v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8"),
    CUBIC_MONOMIALS_NO_Z3,
)
Q_TAIL = add(
    mul(variable("r20"), monomial(2, 0, 1)),
    mul(variable("r11"), monomial(1, 1, 1)),
    mul(variable("r02"), monomial(0, 2, 1)),
    mul(variable("r10"), monomial(1, 0, 2)),
    mul(variable("r01"), monomial(0, 1, 2)),
)


def build_determinant(q, v_form, b_form, linear):
    h4 = (power(Z, 4), mul(Z, q), {})
    h3 = (
        add(scale(mul(Z, W_FORM), Fraction(4, 3)), mul(S, q)),
        v_form,
        power(Z, 3),
    )
    h2 = (A, b_form, W_FORM)
    return determinant_of_jets(linear, h2, h3, h4)


def all_zero_at_degree(determinant, degree):
    return all(
        not coefficient
        for coefficient in source_degree_coefficients(determinant, degree).values()
    )


def audit_root_type(label, q0):
    q = add(q0, Q_TAIL)
    generic_determinant = build_determinant(
        q,
        V_GENERIC,
        B_GENERIC,
        generic_linear(),
    )
    check(
        all_zero_at_degree(generic_determinant, 8),
        f"{label}: normalized family misses E8",
    )
    check(
        all_zero_at_degree(generic_determinant, 7),
        f"{label}: normalized family misses E7",
    )
    e6_map = source_degree_coefficients(generic_determinant, 6)
    row_monomials = sorted(e6_map, reverse=True)
    unknowns = (
        "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8",
        "l6", "l7",
    )
    assert_jointly_linear(e6_map.values(), unknowns, f"{label} E6")
    e6_matrix = [
        [coefficient_of_parameter(e6_map[monomial_key], name) for name in unknowns]
        for monomial_key in row_monomials
    ]
    pivot_rows, pivot_columns = select_numeric_pivot(e6_matrix)
    check(len(pivot_rows) == 8, f"{label}: numeric E6 rank is not eight")
    # Record the literal determinant in the ambient monomial/unknown order;
    # the discovery order of Gaussian pivots has an irrelevant row sign.
    pivot_rows = tuple(sorted(pivot_rows))
    pivot_columns = tuple(sorted(pivot_columns))
    pivot = [
        [e6_matrix[row][column] for column in pivot_columns]
        for row in pivot_rows
    ]
    pivot_determinant = polynomial_determinant(pivot)
    expected_e6 = scale(power(S, 8), 2**5 * 3**11)
    check(
        pivot_determinant == expected_e6,
        f"{label}: literal E6 pivot is not 2^5*3^11*s^8: "
        f"{pivot_determinant}; rows={pivot_rows}; columns={pivot_columns}",
    )

    # The displayed E6 family, built directly rather than substituted into
    # the generic determinant.
    a_without_z2 = form(("a0", "a1", "a2", "a3", "a4"), QUADRATIC_MONOMIALS[:5])
    transverse = add(
        mul(variable("l6"), X),
        mul(variable("l7"), Y),
    )
    v_solution = add(
        mul(K, q),
        mul(S_INV, mul(Z, a_without_z2)),
        scale(mul(S_INV, mul(power(Z, 2), transverse)), Fraction(-4, 3)),
    )
    solved_e6_determinant = build_determinant(
        q,
        v_solution,
        B_GENERIC,
        generic_linear(),
    )
    check(
        all_zero_at_degree(solved_e6_determinant, 6),
        f"{label}: displayed V family misses an E6 equation",
    )
    mutated_v_determinant = build_determinant(
        q,
        add(v_solution, monomial(3, 0, 0)),
        B_GENERIC,
        generic_linear(),
    )
    check(
        not all_zero_at_degree(mutated_v_determinant, 6),
        f"{label}: E6 negative control was not detected",
    )

    e5_transverse = source_degree_coefficients(solved_e6_determinant, 5)
    if label == "squarefree":
        actual = (
            e5_transverse.get((4, 1, 0), {}),
            e5_transverse.get((1, 4, 0), {}),
        )
        expected = (mul(S, variable("l6")), neg(mul(S, variable("l7"))))
    else:
        actual = (
            e5_transverse.get((4, 1, 0), {}),
            e5_transverse.get((3, 2, 0), {}),
        )
        expected = (mul(S, variable("l6")), scale(mul(S, variable("l7")), -2))
    check(actual == expected, f"{label}: E5 transverse pair mismatch")

    zero_transverse_linear = generic_linear(l6={}, l7={})
    zero_transverse_v = add(
        mul(K, q),
        mul(S_INV, mul(Z, a_without_z2)),
    )
    e5_determinant = build_determinant(
        q,
        zero_transverse_v,
        B_GENERIC,
        zero_transverse_linear,
    )
    e5_map = source_degree_coefficients(e5_determinant, 5)
    e5_rows = sorted(e5_map, reverse=True)
    b_unknowns = ("b0", "b1", "b2", "b3", "b4")
    assert_jointly_linear(e5_map.values(), b_unknowns, f"{label} E5")
    e5_matrix = [
        [coefficient_of_parameter(e5_map[key], name) for name in b_unknowns]
        for key in e5_rows
    ]
    b_pivot_rows, b_pivot_columns = select_numeric_pivot(e5_matrix)
    check(
        len(b_pivot_rows) == len(b_unknowns),
        f"{label}: degree-five B rank is not five",
    )
    # Use the ambient descending-lex row order when recording the literal
    # minor.  Gaussian elimination may discover the same rows in swapped
    # order, which changes only the determinant sign.
    b_pivot_rows = tuple(sorted(b_pivot_rows))
    b_pivot_columns = tuple(sorted(b_pivot_columns))
    check(
        b_pivot_columns == tuple(range(5)),
        f"{label}: unexpected degree-five pivot columns",
    )
    b_pivot = [
        [e5_matrix[row][column] for column in b_pivot_columns]
        for row in b_pivot_rows
    ]
    b_pivot_determinant = polynomial_determinant(b_pivot)
    expected_e5 = scale(power(S, 5), -(2**4) * (3**5))
    check(
        b_pivot_determinant == expected_e5,
        f"{label}: literal E5 pivot is not -2^4*3^5*s^5: "
        f"{b_pivot_determinant}; rows={b_pivot_rows}",
    )

    b_solution_coefficients = (
        mul(S_INV, mul(variable("a0"), K)),
        mul(S_INV, mul(variable("a1"), K)),
        mul(S_INV, mul(variable("a2"), K)),
        mul(
            S_INV,
            add(mul(variable("a3"), K), variable("l0")),
        ),
        mul(
            S_INV,
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
    e5_solved_determinant = build_determinant(
        q,
        zero_transverse_v,
        b_solution,
        zero_transverse_linear,
    )
    check(
        all_zero_at_degree(e5_solved_determinant, 5),
        f"{label}: displayed B family misses an E5 equation",
    )
    mutated_b_determinant = build_determinant(
        q,
        zero_transverse_v,
        add(b_solution, monomial(2, 0, 0)),
        zero_transverse_linear,
    )
    check(
        not all_zero_at_degree(mutated_b_determinant, 5),
        f"{label}: E5 negative control was not detected",
    )

    e4_map = source_degree_coefficients(e5_solved_determinant, 4)
    if label == "squarefree":
        e4_keys = ((2, 0, 2), (0, 2, 2))
        e4_expected = (
            scale(sub(mul(K, variable("l0")), mul(S, variable("l3"))), 3),
            scale(sub(mul(K, variable("l1")), mul(S, variable("l4"))), 3),
        )
    else:
        e4_keys = ((2, 0, 2), (1, 1, 2))
        e4_expected = (
            scale(sub(mul(K, variable("l0")), mul(S, variable("l3"))), 3),
            scale(sub(mul(K, variable("l1")), mul(S, variable("l4"))), -6),
        )
    actual_e4 = tuple(e4_map.get(key, {}) for key in e4_keys)
    check(actual_e4 == e4_expected, f"{label}: E4 proportionality pair mismatch")

    proportional_l3 = mul(S_INV, mul(K, variable("l0")))
    proportional_l4 = mul(S_INV, mul(K, variable("l1")))
    reduced_linear = generic_linear(
        l6={},
        l7={},
        l3=proportional_l3,
        l4=proportional_l4,
    )
    check(
        not det3(reduced_linear),
        f"{label}: proportional linear matrix is not singular",
    )
    mutated_linear = generic_linear(
        l6={},
        l7={},
        l3=add(proportional_l3, constant(1)),
        l4=proportional_l4,
    )
    check(
        bool(det3(mutated_linear)),
        f"{label}: det(L) negative control was not detected",
    )

    row_labels = tuple(row_monomials[row] for row in pivot_rows)
    column_labels = tuple(unknowns[column] for column in pivot_columns)
    b_row_labels = tuple(e5_rows[row] for row in b_pivot_rows)
    print(
        f"{label}: E6 rows={row_labels}, columns={column_labels}, "
        f"pivot={2**5 * 3**11}*s^8"
    )
    print(
        f"{label}: E5 rows={b_row_labels}, "
        f"pivot={-(2**4) * (3**5)}*s^5; E4 and det(L) passed"
    )


def main():
    squarefree = sub(mul(power(X, 2), Y), mul(X, power(Y, 2)))
    double = mul(power(X, 2), Y)
    audit_root_type("squarefree", squarefree)
    audit_root_type("double", double)
    print("PASS: independent sparse audit of zero-ell nontriple lemma")


if __name__ == "__main__":
    main()
