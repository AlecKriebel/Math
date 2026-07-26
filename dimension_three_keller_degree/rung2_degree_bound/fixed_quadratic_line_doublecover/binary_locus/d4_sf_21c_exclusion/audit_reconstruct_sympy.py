#!/usr/bin/env python3
"""Clean-room reconstruction for the D4-SF-21C hostile audit.

This file uses only the stated normal form and the full homogeneous
Jacobian-determinant expansion.  It deliberately imports no primary proof or
verification code.
"""

from __future__ import annotations

import argparse
import itertools
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, z = sp.symbols("p q r z")
s = sp.sqrt(-5)
coords = (p, q, r)

line_2 = p - s * q
line_1 = s * p - q
h = sp.expand(line_2 * line_1)
R = sp.expand(line_2**2 * line_1)
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)


def jac2(f: sp.Expr, g: sp.Expr) -> sp.Expr:
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


alpha = jac2(Q, R)
beta = -jac2(P, R)
gamma = jac2(P, Q)
common = sp.Poly(sp.expand(p * R), p, q, extension=s)


def exact_quotient(poly: sp.Expr, divisor: sp.Poly) -> sp.Expr:
    quotient, remainder = sp.div(
        sp.Poly(sp.expand(poly), p, q, extension=s),
        divisor,
    )
    assert remainder.is_zero
    return sp.expand(quotient.as_expr())


alpha_reduced = exact_quotient(alpha, common)
beta_reduced = exact_quotient(beta, common)
gamma_reduced = exact_quotient(gamma, common)
assert sp.expand(alpha_reduced + 6 * s * q) == 0
assert sp.expand(beta_reduced + 6 * (4 * p + s * q)) == 0
assert sp.expand(gamma_reduced - 8 * q * (s * p - q)) == 0

# Solve E7 = alpha U_r + beta V_r + gamma T_r = 0 in the complete
# homogeneous degree-(2,2,1) coefficient spaces, allowing r dependence.
mon2 = (p**2, p * q, p * r, q**2, q * r, r**2)
mon1 = (p, q, r)
ur_coeff = sp.symbols("ur0:6")
vr_coeff = sp.symbols("vr0:6")
tr_coeff = sp.symbols("tr0:3")
Ur_raw = sum(value * monomial for value, monomial in zip(ur_coeff, mon2))
Vr_raw = sum(value * monomial for value, monomial in zip(vr_coeff, mon2))
Tr_raw = sum(value * monomial for value, monomial in zip(tr_coeff, mon1))
E7_reduced = sp.Poly(
    sp.expand(
        alpha_reduced * Ur_raw
        + beta_reduced * Vr_raw
        + gamma_reduced * Tr_raw
    ),
    p,
    q,
    r,
)
contact_variables = ur_coeff + vr_coeff + tr_coeff
contact_matrix, contact_rhs = sp.linear_eq_to_matrix(
    [coefficient for _, coefficient in E7_reduced.terms()],
    contact_variables,
)
assert contact_rhs == sp.zeros(contact_matrix.rows, 1)
assert contact_matrix.rank() == 9
assert len(contact_variables) - contact_matrix.rank() == 6

# Coordinates on the complete six-dimensional E7 contact space.
v1, v3, v4, t0, t1, t2 = sp.symbols("v1 v3 v4 t0 t1 t2")
contact_coordinates = (v1, v3, v4, t0, t1, t2)
Ur = (
    4 * (t0 + 3 * s * v1 / 5) * p**2 / 3
    + 4 * (s * t0 + 5 * t1 - sp.Rational(15, 4) * v1 + 3 * s * v3)
    * p
    * q
    / 15
    + 4 * (t2 + 3 * s * v4 / 5) * p * r / 3
    + 4 * (s * t1 - sp.Rational(15, 4) * v3) * q**2 / 15
    + 4 * (s * t2 - sp.Rational(15, 4) * v4) * q * r / 15
)
Vr = v1 * p * q + v3 * q**2 + v4 * q * r
Tr = t0 * p + t1 * q + t2 * r
assert sp.expand(
    alpha_reduced * Ur + beta_reduced * Vr + gamma_reduced * Tr
) == 0

# Integrate the r derivatives.  The integration constants are arbitrary
# binary forms of degrees 3, 3, and 2.
binary3 = (p**3, p**2 * q, p * q**2, q**3)
binary2 = (p**2, p * q, q**2)
u = sp.symbols("u0:4")
v = sp.symbols("w0:4")
t = sp.symbols("c0:3")
U0 = sum(value * monomial for value, monomial in zip(u, binary3))
V0 = sum(value * monomial for value, monomial in zip(v, binary3))
T0 = sum(value * monomial for value, monomial in zip(t, binary2))
U = sp.expand(U0 + r * Ur.subs(r, 0) + r**2 * sp.diff(Ur, r) / 2)
V = sp.expand(V0 + r * Vr.subs(r, 0) + r**2 * sp.diff(Vr, r) / 2)
T = sp.expand(T0 + r * Tr.subs(r, 0) + r**2 * sp.diff(Tr, r) / 2)
assert sp.expand(sp.diff(U, r) - Ur) == 0
assert sp.expand(sp.diff(V, r) - Vr) == 0
assert sp.expand(sp.diff(T, r) - Tr) == 0

# Full lower coefficient spaces.
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("ell0:9")
A = sum(value * monomial for value, monomial in zip(a, mon2))
B = sum(value * monomial for value, monomial in zip(b, mon2))
L = sp.Matrix(3, 3, ell)
H4 = sp.Matrix((P, Q, 0))
H3 = sp.Matrix((U, V, R))
H2 = sp.Matrix((A, B, T))
determinant = sp.Poly(
    sp.expand(
        (
            L
            + z * H2.jacobian(coords)
            + z**2 * H3.jacobian(coords)
            + z**3 * H4.jacobian(coords)
        ).det()
    ),
    z,
)
assert determinant.coeff_monomial(z**9) == 0
assert determinant.coeff_monomial(z**8) == 0
assert determinant.coeff_monomial(z**7) == 0

E6 = sp.Poly(sp.expand(determinant.coeff_monomial(z**6)), p, q, r)
lower_variables = (
    a[2],
    a[4],
    a[5],
    b[2],
    b[4],
    b[5],
    ell[8],
) + u + v + t
E6_equations = [coefficient for _, coefficient in E6.terms()]
E6_matrix, E6_rhs = sp.linear_eq_to_matrix(E6_equations, lower_variables)


def specialized_ranks(values: tuple[int, ...]) -> tuple[int, int]:
    substitution = dict(zip(contact_coordinates, values))
    matrix = E6_matrix.subs(substitution)
    rhs = E6_rhs.subs(substitution)
    return matrix.rank(), matrix.row_join(rhs).rank()


def report_equations() -> None:
    for monomial, equation in E6.terms():
        print(monomial, ":", equation)


def generic_elimination() -> None:
    sample = dict(zip(contact_coordinates, (1, 2, 3, 4, 5, 6)))
    numeric = E6_matrix.subs(sample)
    column_pivots = numeric.rref()[1]
    row_pivots = numeric.T.rref()[1]
    assert len(column_pivots) == len(row_pivots) == 9
    print("GENERIC_COLUMNS", column_pivots)
    print("GENERIC_ROWS", row_pivots)
    square = E6_matrix.extract(row_pivots, column_pivots)
    formal_s = sp.symbols("formal_s")
    ring = sp.QQ.poly_ring(formal_s, *contact_coordinates)

    def to_domain(matrix: sp.Matrix) -> DomainMatrix:
        return DomainMatrix.from_list(
            [
                [
                    ring.from_sympy(
                        sp.expand(
                            matrix[row, column].subs(
                                sp.I,
                                formal_s / sp.sqrt(5),
                            )
                        )
                    )
                    for column in range(matrix.cols)
                ]
                for row in range(matrix.rows)
            ],
            ring,
        )

    def reduce_formal_s(element) -> sp.Expr:
        expression = ring.to_sympy(element)
        reduced = sp.Poly(
            expression,
            formal_s,
        ).rem(sp.Poly(formal_s**2 + 5, formal_s))
        return sp.expand(reduced.as_expr().subs(formal_s, s))

    square_domain = to_domain(square)
    inverse_numerator, inverse_denominator = square_domain.inv_den()
    determinant_square = sp.factor(
        reduce_formal_s(inverse_denominator),
        extension=s,
    )
    print("GENERIC_MINOR", determinant_square)
    selected_rhs = E6_rhs.extract(row_pivots, (0,))
    solution_numerator = inverse_numerator.matmul(to_domain(selected_rhs))
    residual_numerator = (
        to_domain(E6_matrix[:, column_pivots]).matmul(solution_numerator)
        - to_domain(E6_rhs).scalarmul(inverse_denominator)
    )
    nonzero = []
    for index in range(residual_numerator.shape[0]):
        expression = reduce_formal_s(residual_numerator[index, 0].element)
        if expression != 0:
            nonzero.append(
                (
                    index,
                    sp.factor(expression, extension=s),
                )
            )
    print("GENERIC_RESIDUAL_COUNT", len(nonzero))
    for item in nonzero:
        print("GENERIC_RESIDUAL", item)


def sample_contact_locus() -> None:
    basis = [
        tuple(int(index == selected) for index in range(6))
        for selected in range(6)
    ]
    for point in basis:
        print("CONTACT_SAMPLE", point, specialized_ranks(point))
    for left in range(6):
        for right in range(left + 1, 6):
            point = tuple(
                int(index in (left, right))
                for index in range(6)
            )
            print("CONTACT_SAMPLE", point, specialized_ranks(point))


def finite_field_search(
    prime: int = 7,
    square_root: int = 3,
    slice_only: bool = False,
) -> None:
    assert square_root * square_root % prime == (-5) % prime

    def formalize(expression: sp.Expr) -> sp.Poly:
        formal_s = sp.symbols("formal_s")
        expression = sp.expand(
            expression.subs(sp.I, formal_s / sp.sqrt(5)).subs(
                formal_s,
                square_root,
            )
        )
        return sp.Poly(expression, *contact_coordinates, domain=sp.QQ)

    def compile_expression(expression: sp.Expr):
        polynomial = formalize(expression)
        terms = []
        for exponents, coefficient in polynomial.terms():
            numerator, denominator = coefficient.as_numer_denom()
            scalar = int(numerator) * pow(int(denominator), -1, prime) % prime
            terms.append((exponents, scalar))
        return terms

    def evaluate(compiled, point):
        value = 0
        for exponents, scalar in compiled:
            term = scalar
            for coordinate, exponent in zip(point, exponents):
                term = term * pow(coordinate, exponent, prime) % prime
            value = (value + term) % prime
        return value

    compiled_matrix = [
        [compile_expression(E6_matrix[row, column]) for column in range(E6_matrix.cols)]
        for row in range(E6_matrix.rows)
    ]
    compiled_rhs = [
        compile_expression(E6_rhs[row, 0])
        for row in range(E6_rhs.rows)
    ]

    def rank_mod(matrix):
        work = [row[:] for row in matrix]
        rows = len(work)
        columns = len(work[0]) if rows else 0
        pivot_row = 0
        for column in range(columns):
            pivot = next(
                (
                    row
                    for row in range(pivot_row, rows)
                    if work[row][column] % prime
                ),
                None,
            )
            if pivot is None:
                continue
            work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
            inverse = pow(work[pivot_row][column] % prime, -1, prime)
            work[pivot_row] = [
                value * inverse % prime
                for value in work[pivot_row]
            ]
            for row in range(rows):
                if row == pivot_row:
                    continue
                scalar = work[row][column] % prime
                if scalar:
                    work[row] = [
                        (left - scalar * right) % prime
                        for left, right in zip(work[row], work[pivot_row])
                    ]
            pivot_row += 1
            if pivot_row == rows:
                break
        return pivot_row

    projective_points = []
    if slice_only:
        points = (
            (0, 1, 0, t0_value, t1_value, 0)
            for t0_value in range(prime)
            for t1_value in range(prime)
        )
    else:
        points = (
            (0,) * first_nonzero + (1,) + tail
            for first_nonzero in range(6)
            for tail in itertools.product(range(prime), repeat=5 - first_nonzero)
        )
    for point in points:
            matrix = [
                [
                    evaluate(compiled_matrix[row][column], point)
                    for column in range(E6_matrix.cols)
                ]
                for row in range(E6_matrix.rows)
            ]
            rhs = [
                evaluate(compiled_rhs[row], point)
                for row in range(E6_rhs.rows)
            ]
            rank = rank_mod(matrix)
            augmented_rank = rank_mod(
                [line + [value] for line, value in zip(matrix, rhs)]
            )
            if rank == augmented_rank:
                projective_points.append((point, rank))
    print("FINITE_FIELD", prime, square_root)
    print("FINITE_CONSISTENT_COUNT", len(projective_points))
    for point in projective_points:
        print("FINITE_CONSISTENT", point)


def slice_rank_minors() -> None:
    x, y, formal_s = sp.symbols("slice_x slice_y formal_s")
    slice_substitution = {
        v1: 0,
        v3: 1,
        v4: 0,
        t0: x,
        t1: y,
        t2: 0,
    }
    sliced = E6_matrix.subs(slice_substitution)
    numeric = sliced.subs({x: 1, y: 1})
    columns = numeric.rref()[1]
    rows = numeric.T.rref()[1]
    assert len(columns) == len(rows) == 9
    ring = sp.QQ.poly_ring(formal_s, x, y)

    def domain_determinant(matrix: sp.Matrix) -> sp.Expr:
        data = [
            [
                ring.from_sympy(
                    sp.expand(
                        matrix[row, column].subs(
                            sp.I,
                            formal_s / sp.sqrt(5),
                        )
                    )
                )
                for column in range(matrix.cols)
            ]
            for row in range(matrix.rows)
        ]
        value = DomainMatrix.from_list(data, ring).det()
        expression = ring.to_sympy(value)
        reduced = sp.Poly(expression, formal_s).rem(
            sp.Poly(formal_s**2 + 5, formal_s)
        )
        return sp.factor(
            sp.expand(reduced.as_expr().subs(formal_s, s)),
            extension=s,
        )

    print("SLICE_GENERIC_ROWS", rows)
    print("SLICE_GENERIC_COLUMNS", columns)
    row_sets = [rows]
    omitted_rows = [index for index in range(sliced.rows) if index not in rows]
    for replacement in omitted_rows[:8]:
        row_sets.append(rows[:-1] + (replacement,))
    for row_set in row_sets:
        value = domain_determinant(sliced.extract(row_set, columns))
        print("SLICE_MINOR", row_set, value)

    rank_eight_numeric = sliced.subs({x: 0, y: 0})
    columns_eight = rank_eight_numeric.rref()[1]
    rows_eight = rank_eight_numeric.T.rref()[1]
    assert len(columns_eight) == len(rows_eight) == 8
    print("SLICE_RANK8_ROWS", rows_eight)
    print("SLICE_RANK8_COLUMNS", columns_eight)
    candidates = [(rows_eight, columns_eight)]
    outside_rows = [
        index for index in range(sliced.rows)
        if index not in rows_eight
    ]
    outside_columns = [
        index for index in range(sliced.cols)
        if index not in columns_eight
    ]
    for position in range(len(rows_eight)):
        for replacement in outside_rows:
            row_set = (
                rows_eight[:position]
                + (replacement,)
                + rows_eight[position + 1 :]
            )
            candidates.append((row_set, columns_eight))
    for position in range(len(columns_eight)):
        for replacement in outside_columns:
            column_set = (
                columns_eight[:position]
                + (replacement,)
                + columns_eight[position + 1 :]
            )
            candidates.append((rows_eight, column_set))
    nonzero_count = 0
    minor_values = []
    for row_set, column_set in candidates:
        value = domain_determinant(sliced.extract(row_set, column_set))
        if value != 0:
            if nonzero_count < 12:
                print("SLICE_RANK8_MINOR", row_set, column_set, value)
            minor_values.append(value)
            nonzero_count += 1
            if nonzero_count == 140:
                break
    rank_drop_basis = sp.groebner(
        minor_values,
        x,
        y,
        extension=s,
        order="lex",
    )
    print(
        "SLICE_RANK7_GROEBNER",
        tuple(sp.factor(poly.as_expr(), extension=s) for poly in rank_drop_basis.polys),
    )


def plane_rank_minors() -> None:
    m, n, formal_s = sp.symbols("plane_m plane_n formal_s")
    plane_substitution = {
        v1: m,
        v3: n,
        v4: 0,
        t0: sp.Rational(3, 4) * n,
        t1: -sp.Rational(3, 4) * s * n,
        t2: 0,
    }
    matrix = E6_matrix.subs(plane_substitution)
    rhs = E6_rhs.subs(plane_substitution)
    sample = {m: 1, n: 2}
    columns = matrix.subs(sample).rref()[1]
    rows = matrix.subs(sample).T.rref()[1]
    assert len(columns) == len(rows) == 7
    ring = sp.QQ.poly_ring(formal_s, m, n)

    def domain_determinant(source: sp.Matrix) -> sp.Expr:
        data = [
            [
                ring.from_sympy(
                    sp.expand(
                        source[row, column].subs(
                            sp.I,
                            formal_s / sp.sqrt(5),
                        )
                    )
                )
                for column in range(source.cols)
            ]
            for row in range(source.rows)
        ]
        value = DomainMatrix.from_list(data, ring).det()
        expression = ring.to_sympy(value)
        reduced = sp.Poly(expression, formal_s).rem(
            sp.Poly(formal_s**2 + 5, formal_s)
        )
        return sp.factor(
            sp.expand(reduced.as_expr().subs(formal_s, s)),
            extension=s,
        )

    print("PLANE_GENERIC_ROWS", rows)
    print("PLANE_GENERIC_COLUMNS", columns)
    base = domain_determinant(matrix.extract(rows, columns))
    print("PLANE_BASE_MINOR", base)
    nonzero = [base]
    outside_rows = [index for index in range(matrix.rows) if index not in rows]
    outside_columns = [index for index in range(matrix.cols) if index not in columns]
    candidates = []
    for position in range(len(rows)):
        for replacement in outside_rows:
            candidates.append(
                (
                    rows[:position] + (replacement,) + rows[position + 1 :],
                    columns,
                )
            )
    for position in range(len(columns)):
        for replacement in outside_columns:
            candidates.append(
                (
                    rows,
                    columns[:position] + (replacement,) + columns[position + 1 :],
                )
            )
    for row_set, column_set in candidates:
        value = domain_determinant(matrix.extract(row_set, column_set))
        if value != 0:
            nonzero.append(value)
            if len(nonzero) <= 8:
                print("PLANE_MINOR", value)
    gcd_value = sp.Poly(nonzero[0], m, n, extension=s)
    for value in nonzero[1:]:
        gcd_value = sp.gcd(gcd_value, sp.Poly(value, m, n, extension=s))
    print(
        "PLANE_RANKDROP_GCD",
        sp.factor(gcd_value.as_expr(), extension=s),
    )
    # Consistency on the claimed plane is checked by a fraction-free solve
    # at the generic function-field point and by exact substitutions below.
    for point in ((1, 0), (0, 1), (1, 2)):
        substitution = {m: point[0], n: point[1]}
        specialized = matrix.subs(substitution)
        specialized_rhs = rhs.subs(substitution)
        print(
            "PLANE_RANKS",
            point,
            specialized.rank(),
            specialized.row_join(specialized_rhs).rank(),
        )


def lower_replay() -> None:
    Mpar, Npar = sp.symbols("Mpar Npar")
    primary_plane = {
        v1: Mpar,
        v3: 4 * s * Npar / 15,
        v4: 0,
        t0: s * Npar / 5,
        t1: Npar,
        t2: 0,
    }
    descended_determinant = sp.Poly(
        sp.expand(determinant.as_expr().subs(primary_plane)),
        z,
    )

    def homogeneous_coefficients(poly: sp.Expr, degree: int):
        polynomial = sp.Poly(sp.expand(poly), p, q, r)
        return tuple(
            polynomial.coeff_monomial(p**ip * q**iq * r**ir)
            for ip in range(degree, -1, -1)
            for iq in range(degree - ip, -1, -1)
            for ir in (degree - ip - iq,)
        )

    def coefficient(poly: sp.Expr, exponent: tuple[int, int, int]):
        return sp.Poly(sp.expand(poly), p, q, r).coeff_monomial(
            p ** exponent[0] * q ** exponent[1] * r ** exponent[2]
        )

    def solve_by_probe(equations, probe, expected_rank):
        matrix, rhs = sp.linear_eq_to_matrix(equations, lower_variables)
        tested = matrix.subs(probe)
        pivot_columns = tested.rref()[1]
        pivot_rows = tested.T.rref()[1]
        assert len(pivot_columns) == len(pivot_rows) == expected_rank
        free_columns = tuple(
            index
            for index in range(len(lower_variables))
            if index not in pivot_columns
        )
        pivot_matrix = matrix.extract(pivot_rows, pivot_columns)
        free_matrix = matrix.extract(pivot_rows, free_columns)
        free_vector = sp.Matrix(
            [lower_variables[index] for index in free_columns]
        )
        effective_rhs = rhs.extract(pivot_rows, (0,)) - free_matrix * free_vector
        pivot_values = pivot_matrix.inv() * effective_rhs
        substitution = {
            lower_variables[column]: sp.cancel(pivot_values[index])
            for index, column in enumerate(pivot_columns)
        }
        assert all(
            sp.cancel(equation.subs(substitution)) == 0
            for equation in equations
        )
        return matrix, substitution

    raw_E6 = homogeneous_coefficients(
        descended_determinant.coeff_monomial(z**6),
        6,
    )
    matrix_generic, substitution_generic = solve_by_probe(
        raw_E6,
        {Mpar: 1, Npar: 0},
        7,
    )
    assert matrix_generic.subs({Mpar: 1, Npar: 3}).rank() == 6
    assert matrix_generic.subs({Mpar: -1, Npar: 6}).rank() == 6
    assert matrix_generic.subs({Mpar: 0, Npar: 0}).rank() == 5

    raw_E5 = descended_determinant.coeff_monomial(z**5)
    first = sp.cancel(
        coefficient(raw_E5, (2, 1, 2)).subs(substitution_generic)
    )
    second = sp.cancel(
        coefficient(raw_E5, (1, 2, 2)).subs(substitution_generic)
    )
    first_numerator = sp.factor(first, extension=s)
    second_numerator = sp.factor(second, extension=s)
    assert not (
        set(lower_variables) & first_numerator.free_symbols
        or set(lower_variables) & second_numerator.free_symbols
    )
    first_polynomial = sp.Poly(first_numerator, Mpar, Npar, extension=s)
    second_polynomial = sp.Poly(second_numerator, Mpar, Npar, extension=s)
    resultant_M = sp.factor(
        sp.resultant(
            first_polynomial.as_expr(),
            second_polynomial.as_expr(),
            Mpar,
        ),
        extension=s,
    )
    resultant_N = sp.factor(
        sp.resultant(
            first_polynomial.as_expr(),
            second_polynomial.as_expr(),
            Npar,
        ),
        extension=s,
    )
    assert sp.Poly(resultant_M, Npar, extension=s).monoms() == [(9,)]
    assert sp.Poly(resultant_N, Mpar, extension=s).monoms() == [(9,)]
    print("CLEANROOM_GENERIC_RESULTANTS", resultant_M, resultant_N)

    for boundary in (
        {Mpar: 1, Npar: 3},
        {Mpar: -1, Npar: 6},
    ):
        equations = tuple(value.subs(boundary) for value in raw_E6)
        _, substitution = solve_by_probe(equations, {}, 6)
        obstruction = sp.factor(
            coefficient(raw_E5, (3, 0, 2))
            .subs(boundary)
            .subs(substitution),
            extension=s,
        )
        assert obstruction == -sp.Rational(108, 5)
        print("CLEANROOM_BOUNDARY", boundary, obstruction)

    origin = {Mpar: 0, Npar: 0}
    origin_equations = tuple(value.subs(origin) for value in raw_E6)
    _, origin_substitution = solve_by_probe(origin_equations, {}, 5)
    raw_E4 = descended_determinant.coeff_monomial(z**4)
    first_square = sp.factor(
        coefficient(raw_E4, (3, 0, 1))
        .subs(origin)
        .subs(origin_substitution),
        extension=s,
    )
    second_square = sp.factor(
        coefficient(raw_E4, (2, 1, 1))
        .subs(origin)
        .subs(origin_substitution)
        .subs({b[4]: 0}),
        extension=s,
    )
    assert first_square == 12 * b[4] ** 2
    assert second_square == 8 * s * ell[8] ** 2 / 3
    forced = {b[4]: 0, ell[8]: 0}
    nonbinary_quadratic = (a[2], a[4], a[5], b[2], b[4], b[5])
    for variable in nonbinary_quadratic:
        value = sp.factor(
            variable.subs(origin_substitution).subs(forced),
            extension=s,
        )
        assert value == 0
    print("CLEANROOM_ZERO_SQUARES", first_square, second_square)
    print("D4_SF_21C_CLEANROOM_LOWER_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--equations", action="store_true")
    parser.add_argument("--generic-eliminate", action="store_true")
    parser.add_argument("--samples", action="store_true")
    parser.add_argument("--finite-search", action="store_true")
    parser.add_argument("--finite-slice", action="store_true")
    parser.add_argument("--prime", type=int, default=7)
    parser.add_argument("--sqrt-minus-five", type=int, default=3)
    parser.add_argument("--slice-minors", action="store_true")
    parser.add_argument("--plane-minors", action="store_true")
    parser.add_argument("--lower-replay", action="store_true")
    arguments = parser.parse_args()
    print("E7_REDUCED", alpha_reduced, beta_reduced, gamma_reduced)
    print("E7_CONTACT_DIMENSION", len(contact_variables) - contact_matrix.rank())
    print("E6_MATRIX_SHAPE", E6_matrix.shape)
    for point in (
        (1, 2, 3, 4, 5, 6),
        (1, 0, 0, 0, 0, 0),
        (0, 0, 0, 1, 0, 0),
        (0, 0, 0, 0, 0, 0),
    ):
        print("E6_RANKS", point, specialized_ranks(point))
    if arguments.equations:
        report_equations()
    if arguments.generic_eliminate:
        generic_elimination()
    if arguments.samples:
        sample_contact_locus()
    if arguments.finite_search:
        finite_field_search(
            arguments.prime,
            arguments.sqrt_minus_five,
            arguments.finite_slice,
        )
    if arguments.slice_minors:
        slice_rank_minors()
    if arguments.plane_minors:
        plane_rank_minors()
    if arguments.lower_replay:
        lower_replay()
    print("D4_SF_21C_CLEANROOM_TOP_PASS")


if __name__ == "__main__":
    main()
