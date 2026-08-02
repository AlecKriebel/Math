#!/usr/bin/env python3
"""Exact verifier for the four-dimensional conic-preserving rate family.

The calculation uses only rational polynomial arithmetic.  It reconstructs
the linear normal-form map from the fixed directed support, compares it with
the checked-in matrix, certifies rank and nullity, verifies an integer-vector
kernel basis, proves the positive-cone parametrization coefficientwise, and
checks the original integer rate vector is an interior coprime witness.
"""

from __future__ import annotations

import csv
from functools import reduce
from pathlib import Path

import sympy as sp


x, y, z = sp.symbols("x y z")
variables = (x, y, z)

complexes = (
    (0, 0, 0),
    (0, 0, 1),
    (0, 0, 3),
    (0, 1, 1),
    (0, 3, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1),
    (2, 1, 0),
    (3, 0, 0),
)

# This is the exact directed order in ../network.csv and the column order of M.
directed_support = (
    (0, 1),
    (1, 0),
    (0, 4),
    (4, 0),
    (0, 6),
    (6, 0),
    (1, 7),
    (7, 1),
    (2, 4),
    (4, 2),
    (2, 7),
    (7, 2),
    (2, 9),
    (9, 2),
    (3, 4),
    (4, 3),
    (5, 9),
    (9, 5),
    (8, 9),
    (9, 8),
)

rate_names = tuple(f"k{source}_{target}" for source, target in directed_support)
rate_symbols = sp.symbols(" ".join(rate_names))

family_dir = Path(__file__).resolve().parent
project_dir = family_dir.parent


def read_original_network():
    rows = []
    with (project_dir / "network.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                (
                    int(row["source_index"]),
                    int(row["target_index"]),
                    int(row["rate"]),
                )
            )
    assert tuple((source, target) for source, target, _ in rows) == directed_support
    assert all(rate > 0 for _, _, rate in rows)
    return tuple(rate for _, _, rate in rows)


def monomial(complex_index):
    exponent = complexes[complex_index]
    return sp.prod(variable**power for variable, power in zip(variables, exponent))


L = z - x - y + 1
Q = 7 * x**2 - 2 * x * y - 16 * x + 7 * y**2 - 16 * y + 16

# Variable order z > y > x makes z and y^2 the two leading monomials.
conic_basis = sp.groebner((L, Q), z, y, x, order="lex", domain=sp.QQ)
expected_conic_basis = (
    z - x - y + 1,
    y**2 - sp.Rational(2, 7) * x * y + x**2
    - sp.Rational(16, 7) * (x + y) + sp.Rational(16, 7),
)
assert tuple(sp.expand(polynomial.as_expr()) for polynomial in conic_basis.polys) == tuple(
    sp.expand(polynomial) for polynomial in expected_conic_basis
)

remainder_monomials = (1, x, y, x**2, x * y, x**3, x**2 * y)
remainder_names = ("1", "x", "y", "x2", "xy", "x3", "x2y")


def unit_remainder(source, target, coordinate):
    contribution = monomial(source) * (
        complexes[target][coordinate] - complexes[source][coordinate]
    )
    return sp.expand(conic_basis.reduce(contribution)[1])


def construct_remainder_matrix():
    columns = []
    for source, target in directed_support:
        columns.append(
            tuple(unit_remainder(source, target, coordinate) for coordinate in range(3))
        )

    matrix = sp.zeros(21, 20)
    for coordinate in range(3):
        for monomial_index, basis_monomial in enumerate(remainder_monomials):
            row = 7 * coordinate + monomial_index
            for column in range(20):
                polynomial = sp.Poly(columns[column][coordinate], x, y, z, domain=sp.QQ)
                matrix[row, column] = polynomial.coeff_monomial(basis_monomial)

    # The listed seven monomials must capture every normal-form term.
    listed = {
        sp.Poly(basis_monomial, x, y, z).monoms()[0]
        for basis_monomial in remainder_monomials
    }
    for column in columns:
        for polynomial in column:
            assert set(sp.Poly(polynomial, x, y, z).monoms()) <= listed
    return matrix, columns


def read_recorded_matrix():
    rows = []
    with (family_dir / "remainder_matrix.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        reader = csv.reader(handle)
        header = next(reader)
        assert header == ["coordinate", "monomial", *rate_names]
        for row_index, row in enumerate(reader):
            coordinate = f"F{row_index // 7 + 1}"
            monomial_name = remainder_names[row_index % 7]
            assert row[:2] == [coordinate, monomial_name]
            rows.append([sp.Rational(entry) for entry in row[2:]])
    assert len(rows) == 21 and all(len(row) == 20 for row in rows)
    return sp.Matrix(rows)


M, unit_remainders = construct_remainder_matrix()
assert M == read_recorded_matrix()

# Explicitly connect M to the symbolic 20-rate vector: each block of seven
# entries is the coefficient vector of the corresponding coordinate normal form.
symbolic_rate_vector = sp.Matrix(rate_symbols)
symbolic_remainder_coefficients = M * symbolic_rate_vector
for coordinate in range(3):
    symbolic_remainder = sp.expand(
        sum(
            rate_symbols[column] * unit_remainders[column][coordinate]
            for column in range(20)
        )
    )
    reconstructed = sp.expand(
        sum(
            symbolic_remainder_coefficients[7 * coordinate + index]
            * remainder_monomials[index]
            for index in range(7)
        )
    )
    assert sp.expand(symbolic_remainder - reconstructed) == 0


# A compact nonzero-minor rank certificate.
rank_rows = (0, 1, 2, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 18, 19)
rank_columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 18)
rank_minor = M.extract(rank_rows, rank_columns).det()
assert rank_minor == sp.Rational(7255941120, 823543)
assert rank_minor == sp.Rational(2**13 * 3**11 * 5, 7**7)


# Primitive integer vectors spanning the rational kernel.
integer_kernel_basis = sp.Matrix(
    [
        (0, 0, 2940, 13020),
        (0, 0, 87318, 120582),
        (0, 0, 0, 10752),
        (0, 1, -3136, 0),
        (0, 0, 9282, 6930),
        (0, 0, 21216, 67584),
        (0, 0, 29835, 22275),
        (0, 0, -3360, 0),
        (1, 0, 0, 10752),
        (0, 1, 3136, 13888),
        (-3, 0, 32487, 24255),
        (0, 0, 77616, 107184),
        (1, 0, 0, 0),
        (0, 0, 6272, 13888),
        (0, 0, 0, 59136),
        (0, -3, 0, 0),
        (0, 0, 0, 59136),
        (0, 0, -9408, 0),
        (0, 0, 0, 66528),
        (0, 0, 0, 10080),
    ]
)
assert M * integer_kernel_basis == sp.zeros(21, 4)
assert integer_kernel_basis.rank() == 4
for column in range(4):
    entries = [abs(int(entry)) for entry in integer_kernel_basis[:, column] if entry]
    assert reduce(sp.igcd, entries) == 1

# The nonzero minor gives rank >= 16; four independent kernel vectors give
# rank <= 16.  These two exact certificates prove rank and nullity without
# relying on a numerical rank routine.
assert M.rank() == 16
assert len(M.nullspace()) == 4


a, b, c, d = sp.symbols("a b c d")
normalized_kernel_basis = integer_kernel_basis * sp.diag(
    1, -sp.Rational(1, 3), -sp.Rational(1, 9408), sp.Rational(1, 10080)
)
assert normalized_kernel_basis.extract((12, 15, 17, 19), range(4)) == sp.eye(4)

rate_family = tuple(
    sp.factor(entry)
    for entry in normalized_kernel_basis * sp.Matrix((a, b, c, d))
)
expected_rate_family = (
    (62 * d - 15 * c) / 48,
    33 * (58 * d - 45 * c) / 160,
    16 * d / 15,
    (c - b) / 3,
    (154 * d - 221 * c) / 224,
    (9856 * d - 3315 * c) / 1470,
    45 * (154 * d - 221 * c) / 3136,
    5 * c / 14,
    (15 * a + 16 * d) / 15,
    (62 * d - 15 * b - 15 * c) / 45,
    (154 * d - 192 * a - 221 * c) / 64,
    11 * (58 * d - 45 * c) / 60,
    a,
    2 * (31 * d - 15 * c) / 45,
    88 * d / 15,
    b,
    88 * d / 15,
    c,
    33 * d / 5,
    d,
)
assert all(
    sp.cancel(actual - expected) == 0
    for actual, expected in zip(rate_family, expected_rate_family)
)
assert all(sp.cancel(entry) == 0 for entry in M * sp.Matrix(rate_family))


# Exact positive-orthant parametrization of the entire strict positive cone.
h, slack = sp.symbols("h slack")
orthant_substitution = {
    c: b + h,
    d: (192 * a + 221 * (b + h) + slack) / 154,
}
orthant_rates = tuple(sp.expand(rate.subs(orthant_substitution)) for rate in rate_family)
orthant_coefficient_matrix = sp.Matrix(
    [
        [sp.Poly(rate, a, b, h, slack, domain=sp.QQ).coeff_monomial(parameter)
         for parameter in (a, b, h, slack)]
        for rate in orthant_rates
    ]
)
assert orthant_coefficient_matrix.shape == (20, 4)
assert all(entry >= 0 for entry in orthant_coefficient_matrix)
assert all(any(entry > 0 for entry in orthant_coefficient_matrix.row(row)) for row in range(20))

# The inverse cone coordinates are a,b,h=c-b,slack=154d-192a-221c.
assert sp.expand(orthant_substitution[c] - b) == h
assert sp.expand(
    154 * orthant_substitution[d]
    - 192 * a
    - 221 * orthant_substitution[c]
) == slack


original_rates = read_original_network()
original_free_parameters = tuple(original_rates[index] for index in (12, 15, 17, 19))
assert original_free_parameters == (3920, 3920, 15680, 658560)
assert original_free_parameters == tuple(3920 * value for value in (1, 1, 4, 168))
assert tuple(
    sp.Rational(rate.subs(dict(zip((a, b, c, d), original_free_parameters))))
    for rate in rate_family
) == original_rates

original_h = original_free_parameters[2] - original_free_parameters[1]
original_slack = (
    154 * original_free_parameters[3]
    - 192 * original_free_parameters[0]
    - 221 * original_free_parameters[2]
)
assert (original_free_parameters[0], original_free_parameters[1], original_h, original_slack) == (
    3920,
    3920,
    11760,
    97200320,
)
assert all(value > 0 for value in (3920, 3920, original_h, original_slack))


# Exact coprime specialization witnessing that generic coprimality is nonempty.
original_field = [sp.Integer(0), sp.Integer(0), sp.Integer(0)]
for (source, target), rate in zip(directed_support, original_rates):
    source_monomial = monomial(source)
    for coordinate in range(3):
        original_field[coordinate] += (
            rate
            * source_monomial
            * (complexes[target][coordinate] - complexes[source][coordinate])
        )
original_field = tuple(sp.expand(polynomial) for polynomial in original_field)
primitive_coordinates = [
    sp.Poly(polynomial, x, y, z, domain=sp.QQ).primitive()[1]
    for polynomial in original_field
]
coordinate_gcd = reduce(sp.gcd, primitive_coordinates)
assert coordinate_gcd.total_degree() == 0
assert all(
    sp.gcd(primitive_coordinates[first], primitive_coordinates[second]).total_degree() == 0
    for first in range(3)
    for second in range(first + 1, 3)
)

# The projective closed-locus argument in README uses the stronger witness
# that the common-degree homogenizations also have gcd one.
w = sp.symbols("w")
homogenized_coordinates = [
    polynomial.homogenize(w)
    for polynomial in primitive_coordinates
]
homogenized_gcd = reduce(sp.gcd, homogenized_coordinates)
assert homogenized_gcd.total_degree() == 0


print("PASS: exact fixed-support family checks succeeded")
print(f"  canonical remainder matrix: {M.rows} x {M.cols}")
print(f"  rank/nullity: {M.rank()}/{len(M.nullspace())}")
print("  positive cone coordinates: a,b,h,slack > 0")
print(f"  original interior coordinates: {(3920, 3920, original_h, original_slack)}")
print("  original affine and homogenized coordinate gcds: 1")
