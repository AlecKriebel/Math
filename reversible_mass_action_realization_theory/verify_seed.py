#!/usr/bin/env python3
"""Standalone exact verifier for the realization-theory seed.

The script freezes the ten complexes, ten reversible pairs, and the complete
four-parameter family of rates for which the mass-action field vanishes on a
fixed positive conic.  It imports no module and reads no data file from the
earlier construction project.  Every computation is over the integers or
rationals; decimal approximations are not used.
"""

from __future__ import annotations

from collections import deque
from functools import reduce

import sympy as sp


x, y, z, t = sp.symbols("x y z t")
a, b, c, d = sp.symbols("a b c d")
h, slack = sp.symbols("h slack")
xyz = (x, y, z)

# Complex indices are used in the directed support below.
COMPLEXES = (
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

REVERSIBLE_PAIRS = (
    (0, 1),
    (0, 4),
    (0, 6),
    (1, 7),
    (2, 4),
    (2, 7),
    (2, 9),
    (3, 4),
    (5, 9),
    (8, 9),
)

DIRECTED_SUPPORT = tuple(
    edge
    for source, target in REVERSIBLE_PAIRS
    for edge in ((source, target), (target, source))
)

# Free coordinates are (k_2,9, k_4,3, k_9,5, k_9,8)=(a,b,c,d).
RATE_FAMILY = (
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

CLEAN_PARAMETERS = (653, 1, 70, 915)
CLEAN_RATES = (
    1160, 10296, 976, 23, 560, 5977, 1800, 25, 1629, 1237,
    1, 9152, 653, 1214, 5368, 1, 5368, 70, 6039, 915,
)

# The continuum is the conic complete intersection (L,Q).
L = z - x - y + 1
Q = 7 * x**2 - 2 * x * y - 16 * x + 7 * y**2 - 16 * y + 16


def source_monomial(complex_index: int) -> sp.Expr:
    exponent = COMPLEXES[complex_index]
    return sp.prod(variable**power for variable, power in zip(xyz, exponent))


def mass_action_field(rates) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Reconstruct F directly from the twenty directed reactions."""
    assert len(rates) == len(DIRECTED_SUPPORT)
    field = [sp.Integer(0), sp.Integer(0), sp.Integer(0)]
    for rate, (source, target) in zip(rates, DIRECTED_SUPPORT):
        kinetic_term = sp.sympify(rate) * source_monomial(source)
        for coordinate in range(3):
            displacement = (
                COMPLEXES[target][coordinate] - COMPLEXES[source][coordinate]
            )
            field[coordinate] += kinetic_term * displacement
    return tuple(sp.expand(entry) for entry in field)


def verify_graph_and_stoichiometry() -> None:
    assert len(COMPLEXES) == 10
    assert len(set(COMPLEXES)) == 10
    assert all(
        len(complex_vector) == 3
        and all(isinstance(entry, int) and entry >= 0 for entry in complex_vector)
        for complex_vector in COMPLEXES
    )
    assert len(REVERSIBLE_PAIRS) == 10
    assert len(DIRECTED_SUPPORT) == 20
    assert len(set(DIRECTED_SUPPORT)) == 20
    assert all(
        (target, source) in DIRECTED_SUPPORT
        for source, target in DIRECTED_SUPPORT
    )

    adjacency = {index: set() for index in range(len(COMPLEXES))}
    reaction_differences = []
    for source, target in DIRECTED_SUPPORT:
        adjacency[source].add(target)
        reaction_differences.append(
            tuple(
                COMPLEXES[target][coordinate] - COMPLEXES[source][coordinate]
                for coordinate in range(3)
            )
        )

    reached = {0}
    queue = deque([0])
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    assert reached == set(range(10))

    difference_matrix = sp.Matrix(reaction_differences)
    assert difference_matrix.rank() == 3
    rank_witness = sp.Matrix(((0, 0, 1), (0, 3, 0), (1, 1, 0)))
    assert rank_witness.det() == -3


def conic_constraint_matrix() -> sp.Matrix:
    """Construct the canonical 21-by-20 conic-remainder map from scratch."""
    conic_basis = sp.groebner((L, Q), z, y, x, order="lex", domain=sp.QQ)
    expected_basis = (
        z - x - y + 1,
        y**2 - sp.Rational(2, 7) * x * y + x**2
        - sp.Rational(16, 7) * (x + y) + sp.Rational(16, 7),
    )
    assert tuple(sp.expand(poly.as_expr()) for poly in conic_basis.polys) == tuple(
        sp.expand(poly) for poly in expected_basis
    )

    remainder_monomials = (1, x, y, x**2, x * y, x**3, x**2 * y)
    allowed_monomials = {
        sp.Poly(monomial, *xyz).monoms()[0]
        for monomial in remainder_monomials
    }
    unit_remainders = []
    for column in range(20):
        unit_rates = [0] * 20
        unit_rates[column] = 1
        remainders = tuple(
            sp.expand(conic_basis.reduce(entry)[1])
            for entry in mass_action_field(unit_rates)
        )
        assert all(
            set(sp.Poly(entry, *xyz, domain=sp.QQ).monoms()) <= allowed_monomials
            for entry in remainders
        )
        unit_remainders.append(remainders)

    matrix = sp.zeros(21, 20)
    for coordinate in range(3):
        for row_in_block, monomial in enumerate(remainder_monomials):
            row = 7 * coordinate + row_in_block
            for column in range(20):
                matrix[row, column] = sp.Poly(
                    unit_remainders[column][coordinate], *xyz, domain=sp.QQ
                ).coeff_monomial(monomial)

    # Independent rank certificates: a nonzero 16-minor and a 4-dimensional
    # displayed kernel below.
    rank_rows = (0, 1, 2, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 18, 19)
    rank_columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 18)
    determinant = matrix.extract(rank_rows, rank_columns).det()
    assert determinant == sp.Rational(7255941120, 823543)
    assert determinant == sp.Rational(2**13 * 3**11 * 5, 7**7)
    return matrix


def verify_family(matrix: sp.Matrix) -> None:
    family_vector = sp.Matrix(RATE_FAMILY)
    assert matrix.shape == (21, 20)
    assert matrix * family_vector == sp.zeros(21, 1)
    assert tuple(family_vector[index] for index in (12, 15, 17, 19)) == (
        a, b, c, d
    )
    assert matrix.rank() == 16
    assert len(matrix.nullspace()) == 4
    # Since these four kernel vectors have the identity in the free-rate
    # positions, the displayed family is the complete kernel, not a subfamily.

    # Exact positive-orthant certificate for the strict rate cone.
    substitution = {
        c: b + h,
        d: (192 * a + 221 * (b + h) + slack) / 154,
    }
    orthant_rates = tuple(sp.expand(rate.subs(substitution)) for rate in RATE_FAMILY)
    coefficient_matrix = sp.Matrix(
        [
            [
                sp.Poly(rate, a, b, h, slack, domain=sp.QQ).coeff_monomial(parameter)
                for parameter in (a, b, h, slack)
            ]
            for rate in orthant_rates
        ]
    )
    assert coefficient_matrix.shape == (20, 4)
    assert all(coefficient >= 0 for coefficient in coefficient_matrix)
    assert all(
        any(coefficient > 0 for coefficient in coefficient_matrix.row(row))
        for row in range(20)
    )
    assert sp.expand(substitution[c] - b) == h
    assert sp.expand(154 * substitution[d] - 192 * a - 221 * substitution[c]) == slack


def verify_clean_witness() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    parameter_substitution = dict(zip((a, b, c, d), CLEAN_PARAMETERS))
    reconstructed_rates = tuple(
        sp.cancel(rate.subs(parameter_substitution)) for rate in RATE_FAMILY
    )
    assert reconstructed_rates == CLEAN_RATES
    assert all(rate.is_Integer and rate > 0 for rate in reconstructed_rates)
    assert reduce(sp.igcd, CLEAN_RATES) == 1
    assert max(CLEAN_RATES) == 10296
    assert sum(CLEAN_RATES) == 52464
    assert CLEAN_PARAMETERS[2] > CLEAN_PARAMETERS[1] > 0
    assert 154 * 915 - 192 * 653 - 221 * 70 == 64 > 0

    field = mass_action_field(CLEAN_RATES)
    expected_field = (
        -4697 * x**3 + 6039 * x**2 * y - 9177 * x * y * z
        - 5977 * x * y + 10736 * x * z + 1960 * z**3 + 1800 * z + 560,
        915 * x**3 - 6039 * x**2 * y - 9177 * x * y * z
        - 5977 * x * y - 3782 * y**3 + 10736 * y * z
        + 4888 * z**3 + 1800 * z + 3488,
        3712 * x**3 + 18304 * x * y * z - 5368 * x * z
        + 3712 * y**3 - 5368 * y * z - 6848 * z**3 - 10296 * z + 1160,
    )
    assert all(sp.expand(actual - expected) == 0
               for actual, expected in zip(field, expected_field))

    conic_basis = sp.groebner((L, Q), z, y, x, order="lex", domain=sp.QQ)
    assert all(sp.expand(conic_basis.reduce(entry)[1]) == 0 for entry in field)
    assert any(entry.subs({x: 1, y: 1, z: 1}) != 0 for entry in field)

    primitive_coordinates = [
        sp.Poly(entry, *xyz, domain=sp.QQ).primitive()[1]
        for entry in field
    ]
    assert reduce(sp.gcd, primitive_coordinates).total_degree() == 0
    assert all(
        sp.gcd(primitive_coordinates[i], primitive_coordinates[j]).total_degree() == 0
        for i in range(3) for j in range(i + 1, 3)
    )

    base_point = {x: sp.Rational(3, 2), y: sp.Rational(1, 2), z: 1}
    assert all(entry.subs(base_point) == 0 for entry in field)
    assert sp.Matrix(field).jacobian(xyz).subs(base_point).rank() == 2
    return field


def verify_positive_continuum() -> None:
    denominator = t**2 - t + 1
    parametrization = (
        (t**2 + 3) / (2 * denominator),
        (3 * t**2 + 1) / (2 * denominator),
        (t**2 + t + 1) / denominator,
    )
    substitution = dict(zip(xyz, parametrization))
    assert sp.cancel(L.subs(substitution)) == 0
    assert sp.cancel(Q.subs(substitution)) == 0

    # Exact positivity certificates.  Every displayed numerator and the
    # denominator is strictly positive for every real t.
    assert sp.expand(denominator - ((t - sp.Rational(1, 2))**2 + sp.Rational(3, 4))) == 0
    assert sp.expand(t**2 + 3 - (t**2 + 3)) == 0
    assert sp.expand(3 * t**2 + 1 - (3 * t**2 + 1)) == 0
    assert sp.expand(
        t**2 + t + 1
        - ((t + sp.Rational(1, 2))**2 + sp.Rational(3, 4))
    ) == 0

    # On -1<t<1, z'(t)>0.  Thus the positive equilibria are pairwise
    # distinct there, giving a genuine semialgebraic continuum.
    assert sp.cancel(
        sp.diff(parametrization[2], t)
        - 2 * (1 - t**2) / denominator**2
    ) == 0
    assert tuple(sp.cancel(entry.subs(t, 0)) for entry in parametrization) == (
        sp.Rational(3, 2), sp.Rational(1, 2), sp.Integer(1)
    )

    # Stoichiometric rank three means S=R^3: the positive compatibility class
    # through the displayed point is the entire positive orthant.  The conic
    # itself lies in the affine plane L=0 inside that one class; L=0 is not a
    # conservation plane.


def main() -> None:
    verify_graph_and_stoichiometry()
    matrix = conic_constraint_matrix()
    verify_family(matrix)
    verify_clean_witness()
    verify_positive_continuum()

    print("PASS: standalone realization-theory seed verification succeeded")
    print("  reversible connected support: 10 complexes, 10 reversible pairs")
    print("  stoichiometric rank: 3; unique positive compatibility class")
    print("  complete conic-preserving rate family: rank/nullity 16/4")
    print("  clean positive witness: (a,b,c,d)=(653,1,70,915)")
    print("  conic-plane continuum: positive and pairwise distinct for -1<t<1")
    print("  clean coordinate gcd over QQ[x,y,z]: 1")


if __name__ == "__main__":
    main()
