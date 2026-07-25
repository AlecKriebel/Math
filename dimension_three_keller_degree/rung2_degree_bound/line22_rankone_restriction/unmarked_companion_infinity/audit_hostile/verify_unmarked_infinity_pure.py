#!/usr/bin/env python3
"""Dependency-free hostile audit of the unmarked infinity obstruction.

This program implements sparse multivariate polynomial arithmetic over Q
directly.  It does not import SymPy, PARI matrices, or supplied certificates.
"""

from __future__ import annotations

from fractions import Fraction
import sys


NAMES = (
    "x", "y", "z", "t",
    "AA", "BB", "w0", "w1",
    "u0", "uq", "du1", "du2", "du3", "du4",
    "v0", "vq", "dv1", "dv2", "dv3", "dv4",
    "l0", "l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8",
)
INDEX = {name: index for index, name in enumerate(NAMES)}
NVAR = len(NAMES)
ZERO_EXP = (0,) * NVAR


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
    return {} if not value else {ZERO_EXP: value}


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
    for lexponent, lvalue in left.items():
        for rexponent, rvalue in right.items():
            exponent = tuple(a + b for a, b in zip(lexponent, rexponent))
            result[exponent] = (
                result.get(exponent, Fraction(0)) + lvalue * rvalue
            )
    return clean(result)


def power(poly, exponent):
    check(exponent >= 0, "negative polynomial exponent")
    result = constant(1)
    base = poly
    value = exponent
    while value:
        if value & 1:
            result = mul(result, base)
        value >>= 1
        if value:
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
            result[reduced] = result.get(reduced, Fraction(0)) + degree * value
    return clean(result)


def zero_variables(poly, names):
    positions = tuple(INDEX[name] for name in names)
    return {
        exponent: value
        for exponent, value in poly.items()
        if all(exponent[position] == 0 for position in positions)
    }


def shift_variable(poly, name, amount):
    """Multiply a polynomial by name**amount."""
    if not poly:
        return {}
    position = INDEX[name]
    result = {}
    for exponent, value in poly.items():
        shifted = list(exponent)
        shifted[position] += amount
        result[tuple(shifted)] = value
    return result


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


def jacobian(functions):
    return [
        [derivative(function, name) for name in ("x", "y", "z")]
        for function in functions
    ]


def jac3(first, second, third):
    return det3(jacobian((first, second, third)))


def homogeneous_exponents(degree):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def xyz_monomial(exponent):
    result = constant(1)
    for name, degree in zip(("x", "y", "z"), exponent):
        result = mul(result, power(variable(name), degree))
    return result


def xyz_coefficient(poly, exponent):
    wanted = list(ZERO_EXP)
    wanted[INDEX["x"]], wanted[INDEX["y"]], wanted[INDEX["z"]] = exponent
    return poly.get(tuple(wanted), Fraction(0))


def scalar_coefficient(poly, xyz_exponent, t_exponent):
    result = {}
    for exponent, value in poly.items():
        if (
            exponent[INDEX["x"]],
            exponent[INDEX["y"]],
            exponent[INDEX["z"]],
            exponent[INDEX["t"]],
        ) != (*xyz_exponent, t_exponent):
            continue
        reduced = list(exponent)
        for name in ("x", "y", "z", "t"):
            reduced[INDEX[name]] = 0
        reduced = tuple(reduced)
        result[reduced] = result.get(reduced, Fraction(0)) + value
    return clean(result)


def determinant_fraction(matrix):
    size = len(matrix)
    check(all(len(row) == size for row in matrix), "nonsquare determinant")
    work = [[Fraction(value) for value in row] for row in matrix]
    sign = 1
    determinant = Fraction(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        determinant *= pivot_value
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            factor = work[row][column] / pivot_value
            for entry in range(column, size):
                work[row][entry] -= factor * work[column][entry]
    return sign * determinant


def matrix_vector(matrix, vector):
    return [
        sum(
            (Fraction(entry) * Fraction(value)
             for entry, value in zip(row, vector)),
            Fraction(0),
        )
        for row in matrix
    ]


def direction_vector(direction, mon3, mon2):
    result = []
    for function, monomials in zip(direction, (mon3, mon3, mon2)):
        for monomial in monomials:
            exponent = next(iter(monomial))
            result.append(function.get(exponent, Fraction(0)))
    return result


X, Y, Z, T = (variable(name) for name in ("x", "y", "z", "t"))
p = power(X, 2)
q = add(power(Y, 2), mul(X, Z))
P = power(sub(p, q), 2)
Q = power(add(p, q), 2)
R = mul(X, q)


def raw_e7_audit():
    check(not jac3(P, Q, R), "top E8 is nonzero")
    exponents3 = homogeneous_exponents(3)
    exponents2 = homogeneous_exponents(2)
    exponents7 = homogeneous_exponents(7)
    mon3 = tuple(xyz_monomial(exponent) for exponent in exponents3)
    mon2 = tuple(xyz_monomial(exponent) for exponent in exponents2)

    columns = []
    for index in range(26):
        U = mon3[index] if index < 10 else {}
        V = mon3[index - 10] if 10 <= index < 20 else {}
        W = mon2[index - 20] if index >= 20 else {}
        E7 = add(jac3(P, Q, W), jac3(P, V, R), jac3(U, Q, R))

        def delta(function):
            return sub(scale(mul(Y, derivative(function, "z")), 2),
                       mul(X, derivative(function, "y")))

        compact = scale(
            add(
                scale(
                    mul(
                        mul(mul(X, sub(p, q)), add(p, q)),
                        delta(W),
                    ),
                    8,
                ),
                mul(mul(add(p, q), sub(scale(p, 2), q)), delta(U)),
                neg(mul(mul(sub(p, q), add(scale(p, 2), q)), delta(V))),
            ),
            2,
        )
        check(E7 == compact, f"compact E7 mismatch in raw column {index}")
        column = [xyz_coefficient(E7, exponent) for exponent in exponents7]
        check(
            all(value.denominator == 1 for value in column),
            f"nonintegral raw column {index}",
        )
        columns.append(column)

    matrix = [
        [columns[column][row] for column in range(26)]
        for row in range(36)
    ]
    rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 22)
    selected_columns = (
        1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17, 18, 19, 24, 25
    )
    minor = [
        [matrix[row][column] for column in selected_columns]
        for row in rows
    ]
    check(
        determinant_fraction(minor) == 1709960483517235200,
        "raw E7 maximal minor",
    )

    translations = tuple(
        tuple(derivative(function, name) for function in (P, Q, R))
        for name in ("x", "y", "z")
    )
    directions = (
        (power(X, 3), {}, {}),
        (R, {}, {}),
        ({}, power(X, 3), {}),
        ({}, R, {}),
        ({}, {}, p),
        ({}, {}, q),
        translations[0],
        translations[1],
    )
    kernel_columns = [
        direction_vector(direction, mon3, mon2) for direction in directions
    ]
    for index, column in enumerate(kernel_columns):
        check(
            not any(matrix_vector(matrix, column)),
            f"claimed raw kernel column {index} is not in the kernel",
        )
    kernel_rows = (0, 1, 2, 3, 10, 12, 20, 22)
    kernel_minor = [
        [kernel_columns[column][row] for column in range(8)]
        for row in kernel_rows
    ]
    check(determinant_fraction(kernel_minor) == -8, "kernel minor")

    relation = tuple(
        add(
            translations[2][coordinate],
            scale(directions[0][coordinate], 2),
            scale(directions[1][coordinate], -2),
            scale(directions[2][coordinate], -2),
            scale(directions[3][coordinate], -2),
            neg(directions[4][coordinate]),
        )
        for coordinate in range(3)
    )
    check(relation == ({}, {}, {}), "third source-translation relation")

    # The nonzero 18-minor gives rank >= 18.  Eight independent kernel
    # columns give rank <= 26-8=18, proving completeness.  Four of the
    # eight directions are legal gauge jets; the remaining four are the
    # displayed normal.
    gauges = (directions[1], directions[3], directions[6], directions[7])
    normals = (directions[0], directions[2], directions[4], directions[5])
    partition_columns = [
        tuple(direction_vector(direction, mon3, mon2))
        for direction in gauges + normals
    ]
    check(
        sorted(partition_columns) == sorted(map(tuple, kernel_columns)),
        "gauge/normal partition",
    )
    target_shear_1 = ((1, 0, 1), (0, 1, 0), (0, 0, 1))
    target_shear_2 = ((1, 0, 0), (0, 1, 1), (0, 0, 1))
    check(
        determinant_fraction(target_shear_1) == 1
        and determinant_fraction(target_shear_2) == 1,
        "target shears are not determinant-one",
    )
    check(
        determinant_fraction(((1, 0, 0), (0, 1, 0), (0, 0, 1))) == 1,
        "source translations do not have identity Jacobian",
    )
    check(
        translations[0] == directions[6]
        and translations[1] == directions[7],
        "source-translation jets",
    )
    print(
        "PASS pure raw E7: nonzero rank-18 minor plus eight independent "
        "kernel directions prove completeness and the four/four gauge split"
    )


def weighted_determinant():
    scalar = {name: variable(name) for name in NAMES[4:]}
    AA, BB = scalar["AA"], scalar["BB"]
    w0, w1 = scalar["w0"], scalar["w1"]
    u0, uq = scalar["u0"], scalar["uq"]
    du1, du2, du3, du4 = (
        scalar["du1"], scalar["du2"], scalar["du3"], scalar["du4"]
    )
    v0, vq = scalar["v0"], scalar["vq"]
    dv1, dv2, dv3, dv4 = (
        scalar["dv1"], scalar["dv2"], scalar["dv3"], scalar["dv4"]
    )
    ell = [scalar[f"l{index}"] for index in range(9)]

    U2 = add(
        mul(u0, p), mul(uq, q), mul(du1, mul(X, Y)),
        mul(du2, mul(X, Z)), mul(du3, mul(Y, Z)),
        mul(du4, power(Z, 2)),
    )
    V2 = add(
        mul(v0, p), mul(vq, q), mul(dv1, mul(X, Y)),
        mul(dv2, mul(X, Z)), mul(dv3, mul(Y, Z)),
        mul(dv4, power(Z, 2)),
    )
    H2 = (U2, V2, add(mul(w0, p), mul(w1, q)))
    H3 = (mul(AA, power(X, 3)), mul(BB, power(X, 3)), R)
    H4 = (P, Q, {})
    L = (
        add(mul(ell[0], X), mul(ell[1], Y), mul(ell[2], Z)),
        add(mul(ell[3], X), mul(ell[4], Y), mul(ell[5], Z)),
        add(mul(ell[6], X), mul(ell[7], Y), mul(ell[8], Z)),
    )
    matrices = tuple(jacobian(functions) for functions in (L, H2, H3, H4))
    weighted = [
        [
            add(
                matrices[0][row][column],
                shift_variable(matrices[1][row][column], "t", 1),
                shift_variable(matrices[2][row][column], "t", 2),
                shift_variable(matrices[3][row][column], "t", 3),
            )
            for column in range(3)
        ]
        for row in range(3)
    ]
    return det3(weighted)


def lower_audit():
    weighted = weighted_determinant()
    constrained = (
        "l7", "l8", "du1", "du2", "du3", "du4",
        "dv1", "dv2", "dv3", "dv4",
    )
    constrained_positions = {INDEX[name]: column for column, name in enumerate(constrained)}
    exponents6 = homogeneous_exponents(6)
    row_index = {exponent: row for row, exponent in enumerate(exponents6)}
    matrix = [[Fraction(0) for _ in constrained] for _ in exponents6]
    E6_terms = {
        exponent: value
        for exponent, value in weighted.items()
        if exponent[INDEX["t"]] == 6
    }
    check(E6_terms, "empty E6")
    for exponent, value in E6_terms.items():
        xyz = (
            exponent[INDEX["x"]],
            exponent[INDEX["y"]],
            exponent[INDEX["z"]],
        )
        check(sum(xyz) == 6, "E6 has wrong x,y,z degree")
        scalar_support = [
            position
            for position in range(4, NVAR)
            for _ in range(exponent[position])
        ]
        check(
            len(scalar_support) == 1
            and scalar_support[0] in constrained_positions,
            "E6 is not constant homogeneous linear in the ten constrained variables",
        )
        matrix[row_index[xyz]][constrained_positions[scalar_support[0]]] += value

    rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 11)
    minor = [[matrix[row][column] for column in range(10)] for row in rows]
    check(determinant_fraction(minor) == 4831838208, "E6 forcing minor")
    check(
        not zero_variables(E6_terms, constrained),
        "E6 converse failed after all ten variables were set to zero",
    )

    normalized = zero_variables(weighted, constrained)
    expected = {
        (5, 0, 0): add(scale(variable("l1"), -4), scale(variable("l4"), 4)),
        (4, 0, 1): add(scale(variable("l1"), -2), scale(variable("l4"), -2)),
        (4, 1, 0): add(scale(variable("l2"), 8), scale(variable("l5"), -8)),
        (3, 1, 1): add(scale(variable("l2"), 4), scale(variable("l5"), 4)),
    }
    for exponent, wanted in expected.items():
        got = scalar_coefficient(normalized, exponent, 5)
        check(got == wanted, f"E5 coefficient {exponent}")

    forced_linear = ("l1", "l2", "l4", "l5", "l7", "l8")
    E5_terms = {
        exponent: value
        for exponent, value in normalized.items()
        if exponent[INDEX["t"]] == 5
    }
    check(
        not zero_variables(E5_terms, forced_linear),
        "full E5 converse failed after the six linear coefficients vanished",
    )
    Lmatrix = (
        (variable("l0"), variable("l1"), variable("l2")),
        (variable("l3"), variable("l4"), variable("l5")),
        (variable("l6"), variable("l7"), variable("l8")),
    )
    check(
        not zero_variables(det3(Lmatrix), forced_linear),
        "forced linear part is not singular",
    )
    print(
        "PASS pure E6/E5: E6 is exactly a constant rank-10 homogeneous "
        "system with full converse; four E5 coefficients force det L=0"
    )


def main():
    raw_e7_audit()
    lower_audit()
    print("ALL HOSTILE PURE-PYTHON UNMARKED-INFINITY CHECKS PASSED")


if __name__ == "__main__":
    main()
