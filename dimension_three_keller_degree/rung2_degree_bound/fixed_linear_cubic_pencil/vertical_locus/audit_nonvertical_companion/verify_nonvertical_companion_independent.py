#!/usr/bin/env python3
"""Dependency-free reconstruction of the nonvertical-companion obstruction.

This audit uses sparse multivariate polynomial arithmetic over Q implemented
below.  It does not import SymPy, PARI/GP, or either supplied verifier.

For each root stratum it independently builds

    det(L + t JH2 + t^2 JH3 + t^3 JH4)

and its E6/E5 coefficient system.  It then:

* selects pivot rows by rational elimination after setting all parameters to
  zero (rather than importing the rows selected by the supplied scripts);
* proves that the resulting symbolic pivot determinant is a nonzero integer
  with no parameter dependence;
* verifies the claimed universal solution of every E6/E5 coefficient;
* verifies that the forced linear matrix is singular.
"""

from __future__ import annotations

from fractions import Fraction
import sys


NAMES = (
    "x", "y", "z", "t",
    "q0", "q1", "q2", "q3", "q4", "q5",
    "w0", "w1", "w2", "w3", "w4", "w5",
    "d", "f", "alpha", "beta",
    "a0", "a1", "a2", "a3", "a4", "a5",
    "b0", "b1", "b2", "b3", "b4", "b5",
    "l0", "l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8",
)
INDEX = {name: position for position, name in enumerate(NAMES)}
NVAR = len(NAMES)
ZERO_EXPONENT = (0,) * NVAR


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
            result[exponent] = (
                result.get(exponent, Fraction(0))
                + left_value * right_value
            )
    return clean(result)


def power(poly, exponent):
    check(exponent >= 0, "negative polynomial exponent")
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


def multiply_by_variable_power(poly, name, exponent):
    return mul(poly, power(variable(name), exponent))


def weighted_determinant(linear, h2, h3, h4):
    jac2 = jacobian(h2)
    jac3 = jacobian(h3)
    jac4 = jacobian(h4)
    matrix = []
    for row in range(3):
        matrix.append([])
        for column in range(3):
            matrix[row].append(
                add(
                    linear[row][column],
                    multiply_by_variable_power(jac2[row][column], "t", 1),
                    multiply_by_variable_power(jac3[row][column], "t", 2),
                    multiply_by_variable_power(jac4[row][column], "t", 3),
                )
            )
    return det3(matrix)


def coefficient_equations(determinant, weights):
    grouped = {}
    positions = tuple(INDEX[name] for name in ("x", "y", "z", "t"))
    for exponent, value in determinant.items():
        weight = exponent[INDEX["t"]]
        if weight not in weights:
            continue
        xyz = (
            exponent[INDEX["x"]],
            exponent[INDEX["y"]],
            exponent[INDEX["z"]],
        )
        reduced = list(exponent)
        for position in positions:
            reduced[position] = 0
        key = (weight, xyz)
        reduced = tuple(reduced)
        grouped.setdefault(key, {})
        grouped[key][reduced] = (
            grouped[key].get(reduced, Fraction(0)) + value
        )
    ordered_keys = sorted(
        grouped,
        key=lambda item: (-item[0], -item[1][0], -item[1][1], -item[1][2]),
    )
    return [clean(grouped[key]) for key in ordered_keys]


def tau_coefficient(poly, weight):
    result = {}
    position = INDEX["t"]
    for exponent, value in poly.items():
        if exponent[position] != weight:
            continue
        reduced = list(exponent)
        reduced[position] = 0
        reduced = tuple(reduced)
        result[reduced] = result.get(reduced, Fraction(0)) + value
    return clean(result)


def specialize_zero(poly, names):
    return rename_or_zero(poly, {name: None for name in names})


def xy_bracket(first, second):
    return sub(
        mul(derivative(first, "x"), derivative(second, "y")),
        mul(derivative(first, "y"), derivative(second, "x")),
    )


def linear_system(equations, unknown_names):
    unknown_positions = {INDEX[name]: column for column, name in enumerate(unknown_names)}
    matrix = [[{} for _ in unknown_names] for _ in equations]
    constants = [{} for _ in equations]
    for row, equation in enumerate(equations):
        for exponent, value in equation.items():
            occurrences = [
                (position, exponent[position])
                for position in unknown_positions
                if exponent[position]
            ]
            check(
                sum(degree for _, degree in occurrences) <= 1,
                f"nonlinear coefficient equation in row {row}",
            )
            reduced = list(exponent)
            if occurrences:
                position, degree = occurrences[0]
                check(degree == 1, f"unknown has degree {degree} in row {row}")
                reduced[position] = 0
                column = unknown_positions[position]
                target = matrix[row][column]
            else:
                target = constants[row]
            reduced = tuple(reduced)
            target[reduced] = target.get(reduced, Fraction(0)) + value
    return [[clean(entry) for entry in row] for row in matrix], [
        clean(entry) for entry in constants
    ]


def constant_term(poly):
    return poly.get(ZERO_EXPONENT, Fraction(0))


def rational_rank(matrix):
    if not matrix:
        return 0
    work = [[Fraction(entry) for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
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
        if pivot_row == row_count:
            break
    return pivot_row


def independently_select_rows(matrix, columns):
    selected = []
    current_rank = 0
    for row in range(len(matrix)):
        candidate_rows = selected + [row]
        numeric = [
            [constant_term(matrix[index][column]) for column in columns]
            for index in candidate_rows
        ]
        rank = rational_rank(numeric)
        if rank > current_rank:
            selected.append(row)
            current_rank = rank
        if current_rank == len(columns):
            break
    check(
        current_rank == len(columns),
        f"constant specialization has rank only {current_rank}/{len(columns)}",
    )
    return tuple(selected)


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
    minimum_row = min(range(size), key=lambda row: row_counts[row])
    minimum_column = min(range(size), key=lambda column: column_counts[column])

    result = {}
    if row_counts[minimum_row] <= column_counts[minimum_column]:
        row = minimum_row
        for column, entry in enumerate(matrix[row]):
            if not entry:
                continue
            minor = [
                [
                    matrix[other_row][other_column]
                    for other_column in range(size)
                    if other_column != column
                ]
                for other_row in range(size)
                if other_row != row
            ]
            term = mul(entry, polynomial_determinant(minor))
            result = add(result, term if (row + column) % 2 == 0 else neg(term))
    else:
        column = minimum_column
        for row in range(size):
            entry = matrix[row][column]
            if not entry:
                continue
            minor = [
                [
                    matrix[other_row][other_column]
                    for other_column in range(size)
                    if other_column != column
                ]
                for other_row in range(size)
                if other_row != row
            ]
            term = mul(entry, polynomial_determinant(minor))
            result = add(result, term if (row + column) % 2 == 0 else neg(term))
    return clean(result)


def rename_or_zero(poly, replacements):
    """Substitute selected variables by zero or by another variable."""
    replacement_positions = {
        INDEX[source]: (None if target is None else INDEX[target])
        for source, target in replacements.items()
    }
    result = {}
    for exponent, value in poly.items():
        rewritten = list(exponent)
        killed = False
        for source, target in replacement_positions.items():
            degree = rewritten[source]
            if not degree:
                continue
            rewritten[source] = 0
            if target is None:
                killed = True
                break
            rewritten[target] += degree
        if killed:
            continue
        rewritten = tuple(rewritten)
        result[rewritten] = result.get(rewritten, Fraction(0)) + value
    return clean(result)


X, Y, Z = (variable(name) for name in ("x", "y", "z"))
D, F = variable("d"), variable("f")
ALPHA, BETA = variable("alpha"), variable("beta")


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
LOWER_CUBIC_MONOMIALS = (
    monomial(2, 0, 1),
    monomial(1, 1, 1),
    monomial(0, 2, 1),
    monomial(1, 0, 2),
    monomial(0, 1, 2),
    monomial(0, 0, 3),
)


def form_from_coefficients(names, monomials):
    return add(
        *(
            mul(variable(name), basis)
            for name, basis in zip(names, monomials)
        )
    )


W = form_from_coefficients(
    ("w0", "w1", "w2", "w3", "w4", "w5"),
    QUADRATIC_MONOMIALS,
)
Q_TAIL = form_from_coefficients(
    ("q0", "q1", "q2", "q3", "q4", "q5"),
    LOWER_CUBIC_MONOMIALS,
)


def linear_matrix(first_two_zero=False):
    entries = [[variable(f"l{3 * row + column}") for column in range(3)] for row in range(3)]
    if first_two_zero:
        entries[0][0] = {}
        entries[0][1] = {}
    return entries


def build_equations(q, a_form, b_form, linear):
    h4 = (power(Z, 4), mul(Z, q), {})
    h3 = (mul(D, power(Z, 3)), add(mul(Z, W), mul(F, power(Z, 3))), q)
    h2 = (a_form, b_form, W)
    determinant = weighted_determinant(linear, h2, h3, h4)
    check(
        not coefficient_equations(determinant, (7,)),
        "gauged E7 family is not identically zero",
    )
    return coefficient_equations(determinant, (6, 5))


def binary_coefficient_vector(poly, degree):
    specialized = specialize_zero(
        poly,
        tuple(name for name in NAMES if name not in ("x", "y")),
    )
    return [
        specialized.get(
            tuple(
                degree - index if position == INDEX["x"]
                else index if position == INDEX["y"]
                else 0
                for position in range(NVAR)
            ),
            Fraction(0),
        )
        for index in range(degree + 1)
    ]


def binary_bracket_rank(q_leading, basis, output_degree):
    columns = [
        binary_coefficient_vector(
            xy_bracket(candidate, q_leading),
            output_degree,
        )
        for candidate in basis
    ]
    matrix = [
        [columns[column][row] for column in range(len(columns))]
        for row in range(output_degree + 1)
    ]
    return rational_rank(matrix)


def audit_binary_restrictions():
    root_types = {
        "squarefree": sub(mul(X, mul(Y, X)), mul(X, power(Y, 2))),
        "double": mul(power(X, 2), Y),
        "triple": power(X, 3),
    }
    quadratic_binary = (power(X, 2), mul(X, Y), power(Y, 2))
    linear_binary = (X, Y)
    expected_ranks = {
        "squarefree": (3, 2),
        "double": (3, 2),
        "triple": (2, 1),
    }
    for label, q_leading in root_types.items():
        ranks = (
            binary_bracket_rank(q_leading, quadratic_binary, 3),
            binary_bracket_rank(q_leading, linear_binary, 2),
        )
        check(ranks == expected_ranks[label], f"{label}: binary kernel ranks {ranks}")

    # Reconstruct the three successive z=0 identities before imposing either
    # nontriple E4 branch.
    a_general = form_from_coefficients(
        ("a0", "a1", "a2", "a3", "a4", "a5"),
        QUADRATIC_MONOMIALS,
    )
    b_general = form_from_coefficients(
        ("b0", "b1", "b2", "b3", "b4", "b5"),
        QUADRATIC_MONOMIALS,
    )
    a_zero = form_from_coefficients(
        ("a3", "a4", "a5"),
        QUADRATIC_MONOMIALS[3:],
    )
    a0 = form_from_coefficients(("a0", "a1", "a2"), QUADRATIC_MONOMIALS[:3])
    b0 = form_from_coefficients(("b0", "b1", "b2"), QUADRATIC_MONOMIALS[:3])
    a1 = add(mul(variable("a3"), X), mul(variable("a4"), Y))
    first_linear = add(mul(variable("l0"), X), mul(variable("l1"), Y))
    for label in ("squarefree", "double"):
        q_leading = root_types[label]
        q = add(q_leading, Q_TAIL)
        linear = linear_matrix()
        h4 = (power(Z, 4), mul(Z, q), {})
        h3 = (
            mul(D, power(Z, 3)),
            add(mul(Z, W), mul(F, power(Z, 3))),
            q,
        )

        determinant = weighted_determinant(linear, (a_general, b_general, W), h3, h4)
        e6_plane = specialize_zero(tau_coefficient(determinant, 6), ("z",))
        check(
            e6_plane == neg(mul(q_leading, xy_bracket(a0, q_leading))),
            f"{label}: E6 plane identity mismatch",
        )

        determinant = weighted_determinant(linear, (a_zero, b_general, W), h3, h4)
        e5_plane = specialize_zero(tau_coefficient(determinant, 5), ("z",))
        check(
            e5_plane == neg(mul(q_leading, xy_bracket(first_linear, q_leading))),
            f"{label}: E5 plane identity mismatch",
        )

        plane_linear = linear_matrix(first_two_zero=True)
        determinant = weighted_determinant(
            plane_linear,
            (a_zero, b_general, W),
            h3,
            h4,
        )
        e4_plane = specialize_zero(tau_coefficient(determinant, 4), ("z",))
        check(
            e4_plane == mul(a1, xy_bracket(b0, q_leading)),
            f"{label}: E4 plane identity mismatch",
        )
    print("binary root kernels and successive E6/E5/E4 plane identities passed")


def audit_system(
    label,
    equations,
    unknown_names,
    forced_names,
    replacements,
    expected_absolute_minor,
    linear,
):
    matrix, constants = linear_system(equations, unknown_names)
    check(not any(constants), f"{label}: unexpected affine term")
    columns = tuple(unknown_names.index(name) for name in forced_names)
    rows = independently_select_rows(matrix, columns)
    pivot = [[matrix[row][column] for column in columns] for row in rows]
    determinant = polynomial_determinant(pivot)
    check(
        len(determinant) == 1 and ZERO_EXPONENT in determinant,
        f"{label}: selected pivot determinant depends on parameters",
    )
    determinant_value = determinant[ZERO_EXPONENT]
    check(
        abs(determinant_value) == expected_absolute_minor,
        f"{label}: unexpected pivot determinant {determinant_value}",
    )
    check(
        all(not rename_or_zero(equation, replacements) for equation in equations),
        f"{label}: claimed universal solution misses an E6/E5 coefficient",
    )
    reduced_linear = [
        [rename_or_zero(entry, replacements) for entry in row]
        for row in linear
    ]
    check(
        not polynomial_determinant(reduced_linear),
        f"{label}: forced linear matrix is not singular",
    )
    print(
        f"{label}: rows={rows}, pivot={determinant_value}, "
        f"equations={len(equations)}"
    )


def audit_nontriple():
    root_types = {
        "squarefree": sub(mul(X, mul(Y, X)), mul(X, power(Y, 2))),
        "double": mul(power(X, 2), Y),
    }
    for root_label, q_leading in root_types.items():
        q = add(q_leading, Q_TAIL)

        # Branch A = alpha*z^2.
        a_form = mul(ALPHA, power(Z, 2))
        b_form = form_from_coefficients(
            ("b0", "b1", "b2", "b3", "b4", "b5"),
            QUADRATIC_MONOMIALS,
        )
        linear = linear_matrix(first_two_zero=True)
        equations = build_equations(q, a_form, b_form, linear)
        unknowns = (
            "b0", "b1", "b2", "b3", "b4", "b5",
            "l2", "l3", "l4", "l5", "l6", "l7", "l8",
        )
        forced = ("b0", "b1", "b2", "b3", "b4", "l3", "l4")
        replacements = {
            "b0": None,
            "b1": None,
            "b2": None,
            "b3": "l6",
            "b4": "l7",
            "l3": None,
            "l4": None,
        }
        audit_system(
            f"{root_label}/A=z2",
            equations,
            unknowns,
            forced,
            replacements,
            524288,
            linear,
        )

        # Branch B|_{z=0}=0.
        a_form = add(
            mul(variable("a3"), monomial(1, 0, 1)),
            mul(variable("a4"), monomial(0, 1, 1)),
            mul(variable("a5"), monomial(0, 0, 2)),
        )
        b_form = add(
            mul(variable("b3"), monomial(1, 0, 1)),
            mul(variable("b4"), monomial(0, 1, 1)),
            mul(variable("b5"), monomial(0, 0, 2)),
        )
        linear = linear_matrix(first_two_zero=True)
        equations = build_equations(q, a_form, b_form, linear)
        unknowns = (
            "a3", "a4", "a5", "b3", "b4", "b5",
            "l2", "l3", "l4", "l5", "l6", "l7", "l8",
        )
        forced = ("a3", "a4", "b3", "b4", "l3", "l4")
        replacements = {
            "a3": None,
            "a4": None,
            "b3": "l6",
            "b4": "l7",
            "l3": None,
            "l4": None,
        }
        audit_system(
            f"{root_label}/B0=0",
            equations,
            unknowns,
            forced,
            replacements,
            2048,
            linear,
        )


def audit_triple():
    families = {
        "C_nonzero": (
            add(
                power(X, 3),
                mul(power(Y, 2), Z),
                mul(ALPHA, mul(X, power(Z, 2))),
                mul(BETA, power(Z, 3)),
            ),
            110075314176,
        ),
        "B_nonzero": (
            add(power(X, 3), mul(X, mul(Y, Z)), mul(BETA, power(Z, 3))),
            191102976,
        ),
        "E_nonzero": (
            add(power(X, 3), mul(Y, power(Z, 2))),
            2293235712,
        ),
    }
    a_form = form_from_coefficients(
        ("a0", "a1", "a2", "a3", "a4", "a5"),
        QUADRATIC_MONOMIALS,
    )
    b_form = form_from_coefficients(
        ("b0", "b1", "b2", "b3", "b4", "b5"),
        QUADRATIC_MONOMIALS,
    )
    unknowns = (
        "a0", "a1", "a2", "a3", "a4", "a5",
        "b0", "b1", "b2", "b3", "b4", "b5",
        "l0", "l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8",
    )
    forced = (
        "a0", "a1", "a2", "a3", "a4",
        "b0", "b1", "b2", "b3", "b4",
        "l0", "l1", "l3", "l4",
    )
    replacements = {
        "a0": None,
        "a1": None,
        "a2": None,
        "a3": None,
        "a4": None,
        "b0": None,
        "b1": None,
        "b2": None,
        "b3": "l6",
        "b4": "l7",
        "l0": None,
        "l1": None,
        "l3": None,
        "l4": None,
    }
    for label, (q, expected_minor) in families.items():
        linear = linear_matrix()
        equations = build_equations(q, a_form, b_form, linear)
        audit_system(
            f"triple/{label}",
            equations,
            unknowns,
            forced,
            replacements,
            expected_minor,
            linear,
        )


def main():
    audit_binary_restrictions()
    audit_nontriple()
    audit_triple()
    print("PASS: independent nonvertical-companion exact reconstruction")


if __name__ == "__main__":
    if not __debug__:
        fail("refusing optimized Python: audit checks would be disabled")
    main()
