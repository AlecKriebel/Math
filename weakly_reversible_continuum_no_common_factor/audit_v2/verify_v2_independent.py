#!/usr/bin/env python3
"""Independent exact audit of the v2 fixed-support strengthening.

The verifier is standalone: all asserted network, rate, conic, family, and
stability data are frozen below.  It imports no project module and reads no
v1/v2 verifier.  Its main algorithms deliberately differ from the asserted
implementations:

* the rate-family matrix is reconstructed by substituting out z and then
  taking a univariate remainder in y, rather than by multivariate reduction;
* integer optimality is checked with a pure-integer congruence-aware census;
* both steady ideals are decomposed by saturation and a fresh ideal-
  intersection elimination;
* real-root counts use the Sturm remainder sequence implemented here, rather
  than SymPy's root-count convenience method.

Every mathematical calculation uses integers or rational numbers.  No
floating-point arithmetic occurs.
"""

from __future__ import annotations

import argparse
import json
import math
from functools import reduce
from itertools import combinations
from pathlib import Path

import sympy as sy


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not bool(condition):
        raise AuditFailure(message)


x, y, z, w, t = sy.symbols("x y z w t")
xyz = (x, y, z)

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

DIRECTED_SUPPORT = (
    (0, 1), (1, 0),
    (0, 4), (4, 0),
    (0, 6), (6, 0),
    (1, 7), (7, 1),
    (2, 4), (4, 2),
    (2, 7), (7, 2),
    (2, 9), (9, 2),
    (3, 4), (4, 3),
    (5, 9), (9, 5),
    (8, 9), (9, 8),
)

ORIGINAL_RATES = (
    845740, 7732494, 702464, 3920, 437290, 4380128, 1405575, 5600,
    706384, 900816, 1518755, 6873328, 3920, 896896, 3863552, 3920,
    3863552, 15680, 4346496, 658560,
)

CLEAN_RATES = (
    1160, 10296, 976, 23, 560, 5977, 1800, 25, 1629, 1237,
    1, 9152, 653, 1214, 5368, 1, 5368, 70, 6039, 915,
)

L = z - x - y + 1
Q = 7 * x**2 - 2 * x * y - 16 * x + 7 * y**2 - 16 * y + 16


def source_monomial(complex_index: int) -> sy.Expr:
    exponent = COMPLEXES[complex_index]
    return x**exponent[0] * y**exponent[1] * z**exponent[2]


def mass_action_field(rates) -> tuple[sy.Expr, sy.Expr, sy.Expr]:
    require(len(rates) == len(DIRECTED_SUPPORT), "rate vector has wrong length")
    result = [sy.Integer(0), sy.Integer(0), sy.Integer(0)]
    for rate, (source, target) in zip(rates, DIRECTED_SUPPORT):
        kinetic = sy.sympify(rate) * source_monomial(source)
        for coordinate in range(3):
            result[coordinate] += kinetic * (
                COMPLEXES[target][coordinate] - COMPLEXES[source][coordinate]
            )
    return tuple(sy.expand(entry) for entry in result)


def canonical_conic_remainder(polynomial: sy.Expr) -> sy.Expr:
    """Normal form via z substitution followed by division in QQ(x)[y]."""

    plane_polynomial = sy.expand(polynomial.subs(z, x + y - 1))
    monic_plane_conic = sy.expand(Q / 7)
    _, remainder = sy.div(
        plane_polynomial,
        monic_plane_conic,
        y,
        domain=sy.QQ.frac_field(x),
    )
    return sy.expand(remainder)


REMAINDER_MONOMIALS = (1, x, y, x**2, x * y, x**3, x**2 * y)


def reconstruct_family_matrix() -> sy.Matrix:
    """Build the 21 by 20 conic-remainder map from raw reaction support."""

    allowed = {
        sy.Poly(monomial, x, y, domain=sy.QQ).monoms()[0]
        for monomial in REMAINDER_MONOMIALS
    }
    matrix = sy.zeros(21, 20)
    for column, (source, target) in enumerate(DIRECTED_SUPPORT):
        monomial = source_monomial(source)
        for coordinate in range(3):
            unit_contribution = monomial * (
                COMPLEXES[target][coordinate] - COMPLEXES[source][coordinate]
            )

            # Independently check that substitution is polynomial division by L.
            _, z_remainder = sy.div(
                unit_contribution, L, z, domain=sy.QQ.frac_field(x, y)
            )
            substituted = sy.expand(unit_contribution.subs(z, x + y - 1))
            require(
                sy.expand(z_remainder - substituted) == 0,
                "z-elimination is inconsistent with division by L",
            )

            remainder = canonical_conic_remainder(unit_contribution)
            remainder_poly = sy.Poly(remainder, x, y, domain=sy.QQ)
            require(
                set(remainder_poly.monoms()) <= allowed,
                "normal form escaped the seven asserted monomials",
            )
            for local_row, basis_monomial in enumerate(REMAINDER_MONOMIALS):
                matrix[7 * coordinate + local_row, column] = (
                    remainder_poly.coeff_monomial(basis_monomial)
                )
    return matrix


def asserted_family_vector(a, b, c, d) -> tuple[sy.Expr, ...]:
    """The asserted formulas in free coordinates k12,k15,k17,k19."""

    return tuple(
        sy.cancel(entry)
        for entry in (
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
    )


def audit_family() -> dict:
    require(len(set(COMPLEXES)) == 10, "complex list has a duplicate")
    require(
        all(len(complex_value) == 3 and all(entry >= 0 for entry in complex_value)
            for complex_value in COMPLEXES),
        "invalid complex data",
    )
    support_set = set(DIRECTED_SUPPORT)
    require(
        len(support_set) == 20
        and all((target, source) in support_set for source, target in support_set),
        "fixed support is not ten reversible pairs",
    )
    matrix = reconstruct_family_matrix()
    require(matrix.shape == (21, 20), "wrong family matrix shape")

    rank_rows = (0, 1, 2, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 18, 19)
    rank_columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 18)
    rank_minor = matrix.extract(rank_rows, rank_columns).det()
    expected_minor = sy.Rational(7255941120, 823543)
    require(rank_minor == expected_minor, "asserted 16 by 16 minor is wrong")
    require(
        rank_minor == sy.Rational(2**13 * 3**11 * 5, 7**7),
        "factorized determinant certificate is wrong",
    )

    a, b, c, d = sy.symbols("a b c d")
    family = sy.Matrix(asserted_family_vector(a, b, c, d))
    parameter_matrix = family.jacobian((a, b, c, d))
    require(matrix * family == sy.zeros(21, 1), "family formulas leave the kernel")
    require(parameter_matrix.rank() == 4, "family parameters are dependent")
    require(
        parameter_matrix.extract((12, 15, 17, 19), range(4)) == sy.eye(4),
        "asserted coordinates are not the four free rates",
    )

    # The minor proves rank >=16.  Four independent kernel columns prove
    # nullity >=4 and rank <=16.  Thus no rank routine is needed for the proof.
    require(matrix.rank() == 16 and len(matrix.nullspace()) == 4, "rank replay failed")

    # Positive-cone equivalence as one matrix calculation.  Let
    # c=b+h and 154d=192a+221b+221h+s.  The transformation below sends the
    # positive orthant (a,b,h,s) bijectively to the asserted inequality cone.
    transform = sy.Matrix(
        (
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 1, 1, 0),
            (
                sy.Rational(192, 154),
                sy.Rational(221, 154),
                sy.Rational(221, 154),
                sy.Rational(1, 154),
            ),
        )
    )
    require(transform.det() == sy.Rational(1, 154), "cone map is not invertible")
    orthant_rate_matrix = parameter_matrix * transform
    require(
        all(entry >= 0 for entry in orthant_rate_matrix),
        "a rate has a negative orthant coefficient",
    )
    require(
        all(any(entry > 0 for entry in orthant_rate_matrix.row(row)) for row in range(20)),
        "a rate vanishes identically in the positive cone",
    )

    # Exact necessity witnesses: free rates, c-b, and the slack rate.
    require(
        tuple(family[index] for index in (12, 15, 17, 19)) == (a, b, c, d),
        "free-rate necessity witnesses changed",
    )
    require(sy.cancel(family[3] - (c - b) / 3) == 0, "b<c witness changed")
    require(
        sy.cancel(family[10] - (154 * d - 192 * a - 221 * c) / 64) == 0,
        "slack witness changed",
    )

    return {
        "matrix_shape": [21, 20],
        "rank": 16,
        "nullity": 4,
        "rank_minor": "7255941120/823543",
        "rank_minor_rows_zero_based": list(rank_rows),
        "rank_minor_columns_zero_based": list(rank_columns),
        "positive_cone": [
            "a>0", "b>0", "c>0", "d>0", "b<c",
            "192a+221c<154d",
        ],
        "orthant_map_determinant": "1/154",
        "orthant_nonzero_coefficients": sum(
            1 for entry in orthant_rate_matrix if entry > 0
        ),
    }


def evaluate_family(parameters) -> tuple[int, ...]:
    values = asserted_family_vector(*(sy.Integer(value) for value in parameters))
    require(all(value.is_Integer for value in values), "specialized rate is nonintegral")
    return tuple(int(value) for value in values)


EXPECTED_ORIGINAL_FIELD = (
    -3380608 * x**3 + 4346496 * x**2 * y - 6878928 * x * y * z
    - 4380128 * x * y + 7727104 * x * z + 1530515 * z**3
    + 1405575 * z + 437290,
    658560 * x**3 - 4346496 * x**2 * y - 6878928 * x * y * z
    - 4380128 * x * y - 2722048 * y**3 + 7727104 * y * z
    + 3637907 * z**3 + 1405575 * z + 2544682,
    2706368 * x**3 + 13746656 * x * y * z - 3863552 * x * z
    + 2706368 * y**3 - 3863552 * y * z - 5168422 * z**3
    - 7732494 * z + 845740,
)

EXPECTED_CLEAN_FIELD = (
    -4697 * x**3 + 6039 * x**2 * y - 9177 * x * y * z - 5977 * x * y
    + 10736 * x * z + 1960 * z**3 + 1800 * z + 560,
    915 * x**3 - 6039 * x**2 * y - 9177 * x * y * z - 5977 * x * y
    - 3782 * y**3 + 10736 * y * z + 4888 * z**3 + 1800 * z + 3488,
    3712 * x**3 + 18304 * x * y * z - 5368 * x * z + 3712 * y**3
    - 5368 * y * z - 6848 * z**3 - 10296 * z + 1160,
)


def gcd_certificates(field) -> dict:
    primitive = tuple(
        sy.Poly(coordinate, *xyz, domain=sy.QQ).primitive()[1]
        for coordinate in field
    )
    total_gcd = reduce(sy.gcd, primitive).monic()
    pairwise = tuple(
        sy.gcd(primitive[i], primitive[j]).total_degree()
        for i, j in combinations(range(3), 2)
    )
    homogenized = tuple(polynomial.homogenize(w) for polynomial in primitive)
    homogeneous_gcd = reduce(sy.gcd, homogenized).monic()
    require(total_gcd.total_degree() == 0, "affine coordinate gcd is nonconstant")
    require(pairwise == (0, 0, 0), "a coordinate pair has a common factor")
    require(
        homogeneous_gcd.total_degree() == 0,
        "degree-three homogenizations have a common factor",
    )
    return {
        "affine_gcd_degree": 0,
        "pairwise_gcd_degrees": list(pairwise),
        "homogenized_gcd_degree": 0,
        "geometrically_coprime": True,
    }


def audit_rate_specializations(matrix: sy.Matrix) -> tuple[dict, dict, tuple, tuple]:
    original_parameters = (3920, 3920, 15680, 658560)
    clean_parameters = (653, 1, 70, 915)
    require(evaluate_family(original_parameters) == ORIGINAL_RATES, "original rates miss family")
    require(evaluate_family(clean_parameters) == CLEAN_RATES, "clean rates miss family")
    require(matrix * sy.Matrix(ORIGINAL_RATES) == sy.zeros(21, 1), "original Mk != 0")
    require(matrix * sy.Matrix(CLEAN_RATES) == sy.zeros(21, 1), "clean Mk != 0")

    original_field = mass_action_field(ORIGINAL_RATES)
    clean_field = mass_action_field(CLEAN_RATES)
    require(
        all(sy.expand(left - right) == 0 for left, right in zip(original_field, EXPECTED_ORIGINAL_FIELD)),
        "original displayed field mismatch",
    )
    require(
        all(sy.expand(left - right) == 0 for left, right in zip(clean_field, EXPECTED_CLEAN_FIELD)),
        "clean displayed field mismatch",
    )
    require(
        all(canonical_conic_remainder(coordinate) == 0 for coordinate in original_field),
        "original field does not vanish on conic",
    )
    require(
        all(canonical_conic_remainder(coordinate) == 0 for coordinate in clean_field),
        "clean field does not vanish on conic",
    )

    displayed_point = {
        x: sy.Rational(3, 2), y: sy.Rational(1, 2), z: sy.Integer(1)
    }
    original_jacobian_rank = sy.Matrix(original_field).jacobian(xyz).subs(displayed_point).rank()
    clean_jacobian_rank = sy.Matrix(clean_field).jacobian(xyz).subs(displayed_point).rank()
    require(original_jacobian_rank == 2, "original Jacobian rank changed")
    require(clean_jacobian_rank == 2, "clean Jacobian rank is not two")

    for rates in (ORIGINAL_RATES, CLEAN_RATES):
        require(all(isinstance(rate, int) and rate > 0 for rate in rates), "nonpositive rate")
        require(reduce(math.gcd, rates) == 1, "rate vector is not primitive")

    original_orthant = (
        original_parameters[0],
        original_parameters[1],
        original_parameters[2] - original_parameters[1],
        154 * original_parameters[3]
        - 192 * original_parameters[0]
        - 221 * original_parameters[2],
    )
    clean_orthant = (
        clean_parameters[0],
        clean_parameters[1],
        clean_parameters[2] - clean_parameters[1],
        154 * clean_parameters[3]
        - 192 * clean_parameters[0]
        - 221 * clean_parameters[2],
    )
    require(original_orthant == (3920, 3920, 11760, 97200320), "original cone data wrong")
    require(clean_orthant == (653, 1, 69, 64), "clean cone data wrong")
    require(all(value > 0 for value in original_orthant + clean_orthant), "not cone interior")

    original_summary = {
        "parameters_abcd": list(original_parameters),
        "orthant_coordinates_abhs": list(original_orthant),
        "primitive": True,
        "maximum_rate": max(ORIGINAL_RATES),
        "rate_sum": sum(ORIGINAL_RATES),
        "jacobian_rank_at_3_2__1_2__1": original_jacobian_rank,
        **gcd_certificates(original_field),
    }
    clean_summary = {
        "parameters_abcd": list(clean_parameters),
        "orthant_coordinates_abhs": list(clean_orthant),
        "primitive": True,
        "maximum_rate": max(CLEAN_RATES),
        "rate_sum": sum(CLEAN_RATES),
        "jacobian_rank_at_3_2__1_2__1": clean_jacobian_rank,
        **gcd_certificates(clean_field),
    }
    require(original_summary["maximum_rate"] == 7732494, "original maximum wrong")
    require(original_summary["rate_sum"] == 39165070, "original sum wrong")
    require(clean_summary["maximum_rate"] == 10296, "clean maximum wrong")
    require(clean_summary["rate_sum"] == 52464, "clean sum wrong")
    return original_summary, clean_summary, original_field, clean_field


# Integer numerators and positive denominators for the twenty family rates.
def rate_numerator_denominators(a: int, b: int, c: int, d: int):
    return (
        (62 * d - 15 * c, 48),
        (33 * (58 * d - 45 * c), 160),
        (16 * d, 15),
        (c - b, 3),
        (154 * d - 221 * c, 224),
        (9856 * d - 3315 * c, 1470),
        (45 * (154 * d - 221 * c), 3136),
        (5 * c, 14),
        (15 * a + 16 * d, 15),
        (62 * d - 15 * b - 15 * c, 45),
        (154 * d - 192 * a - 221 * c, 64),
        (11 * (58 * d - 45 * c), 60),
        (a, 1),
        (2 * (31 * d - 15 * c), 45),
        (88 * d, 15),
        (b, 1),
        (88 * d, 15),
        (c, 1),
        (33 * d, 5),
        (d, 1),
    )


def positive_integer_rates(a: int, b: int, c: int, d: int):
    values = []
    for numerator, denominator_value in rate_numerator_denominators(a, b, c, d):
        if numerator <= 0 or numerator % denominator_value:
            return None
        values.append(numerator // denominator_value)
    return tuple(values)


FIXED_INDICES = (0, 1, 2, 4, 5, 6, 7, 11, 13, 14, 16, 17, 18, 19)


def fixed_rates_for_cd(c: int, d: int):
    raw = rate_numerator_denominators(0, 0, c, d)
    values = []
    for index in FIXED_INDICES:
        numerator, denominator_value = raw[index]
        if numerator <= 0 or numerator % denominator_value:
            return None
        values.append(numerator // denominator_value)
    return tuple(values)


def enumerate_integer_family(maximum_d: int) -> dict:
    """Exhaust all relevant (c,d), and every admissible a and b, exactly."""

    scanned_cd = 0
    integral_fixed_cd = 0
    admissible_a_count = 0
    admissible_b_count = 0
    best_maximum = None
    best_sum = None
    maximum_witness_cd = None
    sum_witness_cd = None

    # k2=16d/15 and k7=5c/14 prove 15|d and 14|c.
    require(math.gcd(16, 15) == 1 and math.gcd(5, 14) == 1, "divisibility premise failed")
    for d in range(15, maximum_d + 1, 15):
        # Positivity of k10 with a>=1 implies 221c < 154d.  Using the weaker
        # strict bound here can only scan extra c values and remains exhaustive.
        largest_c = (154 * d - 1) // 221
        for c in range(14, largest_c + 1, 14):
            scanned_cd += 1
            fixed = fixed_rates_for_cd(c, d)
            if fixed is None:
                continue
            integral_fixed_cd += 1

            a_groups = []
            largest_a = (154 * d - 221 * c - 1) // 192
            for a in range(1, largest_a + 1):
                numerator = 154 * d - 192 * a - 221 * c
                if numerator > 0 and numerator % 64 == 0:
                    group = (a + 16 * d // 15, numerator // 64, a)
                    a_groups.append((a, group))
                    admissible_a_count += 1

            b_groups = []
            for b in range(1, c):
                numerator_3 = c - b
                numerator_9 = 62 * d - 15 * b - 15 * c
                if (
                    numerator_3 > 0
                    and numerator_9 > 0
                    and numerator_3 % 3 == 0
                    and numerator_9 % 45 == 0
                ):
                    group = (numerator_3 // 3, numerator_9 // 45, b)
                    b_groups.append((b, group))
                    admissible_b_count += 1

            if not a_groups or not b_groups:
                continue

            minimum_a_max = min(max(group) for _, group in a_groups)
            minimum_b_max = min(max(group) for _, group in b_groups)
            local_maximum = max(max(fixed), minimum_a_max, minimum_b_max)
            minimum_a_sum = min(sum(group) for _, group in a_groups)
            minimum_b_sum = min(sum(group) for _, group in b_groups)
            local_sum = sum(fixed) + minimum_a_sum + minimum_b_sum

            if best_maximum is None or local_maximum < best_maximum:
                best_maximum = local_maximum
                maximum_witness_cd = (d, c)
            if best_sum is None or local_sum < best_sum:
                best_sum = local_sum
                sum_witness_cd = (d, c)

    return {
        "d_bound": maximum_d,
        "cd_pairs_scanned": scanned_cd,
        "integral_fixed_cd_pairs": integral_fixed_cd,
        "admissible_a_values": admissible_a_count,
        "admissible_b_values": admissible_b_count,
        "minimum_maximum": best_maximum,
        "minimum_sum": best_sum,
        "maximum_witness_dc": list(maximum_witness_cd),
        "sum_witness_dc": list(sum_witness_cd),
    }


def audit_integer_optimality() -> dict:
    require(positive_integer_rates(653, 1, 70, 915) == CLEAN_RATES, "clean tuple mismatch")

    # Exact dependency partition justifying the independent minimization of
    # the a- and b-groups for each fixed (c,d).
    symbolic_a, symbolic_b, symbolic_c, symbolic_d = sy.symbols("a b c d")
    symbolic_rates = asserted_family_vector(
        symbolic_a, symbolic_b, symbolic_c, symbolic_d
    )
    a_indices = (8, 10, 12)
    b_indices = (3, 9, 15)
    require(
        set(FIXED_INDICES) | set(a_indices) | set(b_indices) == set(range(20))
        and not (set(FIXED_INDICES) & set(a_indices))
        and not (set(FIXED_INDICES) & set(b_indices))
        and not (set(a_indices) & set(b_indices)),
        "rate dependency partition is not disjoint",
    )
    require(
        all(symbolic_a not in symbolic_rates[index].free_symbols
            and symbolic_b not in symbolic_rates[index].free_symbols
            for index in FIXED_INDICES),
        "a fixed rate depends on a or b",
    )
    require(
        all(symbolic_b not in symbolic_rates[index].free_symbols for index in a_indices)
        and all(symbolic_a not in symbolic_rates[index].free_symbols for index in b_indices),
        "a- and b-dependent rate groups are coupled",
    )

    maximum_census = enumerate_integer_family(1754)
    sum_census = enumerate_integer_family(2713)
    require(maximum_census["minimum_maximum"] == 10296, "smaller maximum exists")
    require(sum_census["minimum_sum"] == 52464, "smaller rate sum exists")

    # Completeness beyond the enumerated finite ranges.
    require(sy.Rational(88 * 1755, 15) == 10296, "maximum cutoff is wrong")
    require(
        2 * sy.Rational(88, 15) + sy.Rational(33, 5) + 1
        == sy.Rational(58, 3),
        "partial-sum coefficient is wrong",
    )
    require(
        sy.Rational(58 * 2714, 3) > 52464,
        "sum cutoff does not exclude larger d",
    )
    require(
        sy.Rational(88 * 915, 15) < 10296,
        "clean vector maximum witness unexpectedly changed",
    )
    require(reduce(math.gcd, CLEAN_RATES) == 1, "optimal vector is not primitive")

    return {
        "minimum_maximum": 10296,
        "maximum_cutoff_d": 1754,
        "minimum_sum": 52464,
        "sum_cutoff_d": 2713,
        "clean_parameters_abcd": [653, 1, 70, 915],
        "maximum_census": maximum_census,
        "sum_census": sum_census,
        "scope": "positive integral rates on the fixed directed support",
    }


def groebner(expressions, generators):
    return sy.groebner(tuple(expressions), *tuple(generators), order="lex", domain=sy.QQ)


def basis_tuple(basis) -> tuple[sy.Expr, ...]:
    return tuple(polynomial.as_expr() for polynomial in basis.polys)


def eliminate(basis, variable: sy.Symbol) -> tuple[sy.Expr, ...]:
    return tuple(
        expression
        for expression in basis_tuple(basis)
        if variable not in expression.free_symbols
    )


def audit_radical(field, label: str) -> dict:
    """Recompute K=p intersection q by saturation and intersection elimination."""

    steady_basis = groebner(field, xyz)
    conic_basis = groebner((L, Q), xyz)
    require(
        all(conic_basis.reduce(coordinate)[1] == 0 for coordinate in field),
        f"{label}: K is not contained in conic prime",
    )

    eliminated_q = sy.rem(Q, L, x)
    D = sy.Poly(eliminated_q, y, z, domain=sy.QQ).monic().as_expr()
    u = sy.symbols(f"u_{label}")
    saturation = groebner(tuple(field) + (1 - u * D,), (u, x, y, z))
    residual_generators = eliminate(saturation, u)
    residual_basis = groebner(residual_generators, xyz)
    residual = basis_tuple(residual_basis)
    require(len(residual) == 3, f"{label}: residual basis length is not three")
    require(
        residual[0].free_symbols <= {x, z}
        and sy.degree(residual[0], x) == 1
        and sy.Poly(residual[0], x).LC() == 1,
        f"{label}: first residual equation is not x+r(z)",
    )
    require(
        residual[1].free_symbols <= {y, z}
        and sy.degree(residual[1], y) == 1
        and sy.Poly(residual[1], y).LC() == 1,
        f"{label}: second residual equation is not y+r(z)",
    )
    require(
        residual[2].free_symbols <= {z}
        and sy.degree(residual[2], z) == 15
        and sy.Poly(residual[2], z).LC() == 1,
        f"{label}: residual univariate polynomial has wrong shape",
    )
    R = sy.Poly(residual[2], z, domain=sy.QQ)
    factorization = sy.factor_list(R.as_expr(), z)[1]
    require(
        len(factorization) == 1
        and sy.degree(factorization[0][0], z) == 15
        and factorization[0][1] == 1,
        f"{label}: residual degree-fifteen polynomial is reducible",
    )
    require(sy.gcd(R, R.diff()).degree() == 0, f"{label}: residual is not squarefree")

    sum_basis = groebner((L, Q) + residual, xyz)
    require(basis_tuple(sum_basis) == (sy.Integer(1),), f"{label}: components meet")

    v = sy.symbols(f"v_{label}")
    intersection_input = tuple(v * generator for generator in (L, Q)) + tuple(
        (1 - v) * generator for generator in residual
    )
    intersection_extended = groebner(intersection_input, (v, x, y, z))
    intersection_basis = groebner(eliminate(intersection_extended, v), xyz)
    require(
        basis_tuple(intersection_basis) == basis_tuple(steady_basis),
        f"{label}: K != p intersection q",
    )

    # p is absolutely prime: the projective conic matrix is nonsingular.
    projective_matrix = sy.Matrix(((7, -1, -8), (-1, 7, -8), (-8, -8, 16)))
    require(projective_matrix.det() == -256, "conic prime certificate failed")

    return {
        "radical": True,
        "dimension": 1,
        "minimal_components_over_Q": 2,
        "conic_component": "absolutely prime",
        "residual_degree": 15,
        "residual_irreducible_over_Q": True,
        "residual_squarefree": True,
        "components_disjoint": True,
        "certificate": "saturation plus auxiliary-variable intersection elimination",
    }


def polynomial_sign(value) -> int:
    value = sy.Rational(value)
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def sturm_sequence(polynomial: sy.Poly) -> tuple[sy.Poly, ...]:
    """Construct the exact signed remainder sequence over QQ."""

    p0 = sy.Poly(polynomial, t, domain=sy.QQ)
    require(not p0.is_zero, "zero polynomial has no Sturm sequence")
    p1 = p0.diff()
    sequence = [p0, p1]
    while not sequence[-1].is_zero:
        remainder = -sequence[-2].rem(sequence[-1])
        if remainder.is_zero:
            break
        # Divide only by a positive rational, preserving all signs.
        _, primitive = remainder.primitive()
        if primitive.LC() * remainder.LC() < 0:
            primitive = -primitive
        sequence.append(primitive)
    return tuple(sequence)


def sign_at(poly: sy.Poly, endpoint) -> int:
    if endpoint == "-inf":
        return polynomial_sign(poly.LC() * ((-1) ** poly.degree()))
    if endpoint == "+inf":
        return polynomial_sign(poly.LC())
    return polynomial_sign(poly.eval(sy.Rational(endpoint)))


def sign_variations(signs) -> int:
    nonzero = [sign for sign in signs if sign]
    return sum(nonzero[index] != nonzero[index - 1] for index in range(1, len(nonzero)))


def sturm_root_count(sequence, left, right) -> int:
    left_signs = [sign_at(poly, left) for poly in sequence]
    right_signs = [sign_at(poly, right) for poly in sequence]
    return sign_variations(left_signs) - sign_variations(right_signs)


T_POLYNOMIAL = sy.Poly(
    5399367 * t**4 + 1602005 * t**3 + 11579010 * t**2
    + 1602005 * t + 6979911,
    t,
    domain=sy.QQ,
)

N_POLYNOMIAL = sy.Poly(
    5730530769 * t**8 + 20026244073 * t**7 + 29613209084 * t**6
    + 118245415239 * t**5 - 38238695578 * t**4 + 127692520263 * t**3
    - 127590858244 * t**2 + 10579139049 * t - 79465564719,
    t,
    domain=sy.QQ,
)

E_POLYNOMIAL = sy.Poly(
    31399532062137 * t**8 + 25149913538286 * t**7
    + 139213446954293 * t**6 + 100751092465458 * t**5
    + 199590946186248 * t**4 + 109518436416306 * t**3
    + 114191722124597 * t**2 + 26510727150318 * t
    + 17568656198073,
    t,
    domain=sy.QQ,
)


def audit_transverse_stability(original_field) -> dict:
    denominator = t**2 - t + 1
    parametrization = (
        (t**2 + 3) / (2 * denominator),
        (3 * t**2 + 1) / (2 * denominator),
        (t**2 + t + 1) / denominator,
    )
    substitution = dict(zip(xyz, parametrization))
    require(
        all(sy.cancel(coordinate.subs(substitution)) == 0 for coordinate in original_field),
        "parametrization is not steady for original field",
    )
    require(sy.discriminant(denominator, t) == -3, "parametrization has real pole")

    jacobian = sy.Matrix(original_field).jacobian(xyz).subs(substitution).applyfunc(sy.cancel)
    tangent = sy.Matrix([sy.diff(coordinate, t) for coordinate in parametrization])
    require(
        all(sy.cancel(entry) == 0 for entry in jacobian * tangent),
        "Jacobian does not annihilate the conic tangent",
    )

    trace = sy.cancel(jacobian.trace())
    transverse_product = sy.cancel(
        sum(jacobian.extract(indices, indices).det() for indices in combinations(range(3), 2))
    )
    determinant = sy.cancel(jacobian.det())
    require(determinant == 0, "Jacobian lacks the tangent zero eigenvalue")
    require(
        sy.cancel(trace + 8 * T_POLYNOMIAL.as_expr() / denominator**2) == 0,
        "asserted transverse trace formula is wrong",
    )
    require(
        sy.cancel(
            transverse_product + 6272 * N_POLYNOMIAL.as_expr() / denominator**4
        )
        == 0,
        "asserted transverse product formula is wrong",
    )
    discriminant = sy.cancel(trace**2 - 4 * transverse_product)
    require(
        sy.cancel(discriminant - 64 * E_POLYNOMIAL.as_expr() / denominator**4) == 0,
        "asserted transverse discriminant formula is wrong",
    )

    sturm_T = sturm_sequence(T_POLYNOMIAL)
    sturm_E = sturm_sequence(E_POLYNOMIAL)
    sturm_N = sturm_sequence(N_POLYNOMIAL)
    T_roots = sturm_root_count(sturm_T, "-inf", "+inf")
    E_roots = sturm_root_count(sturm_E, "-inf", "+inf")
    N_roots = sturm_root_count(sturm_N, "-inf", "+inf")
    require(T_roots == 0 and T_POLYNOMIAL.eval(0) > 0, "T is not globally positive")
    require(E_roots == 0 and E_POLYNOMIAL.eval(0) > 0, "E is not globally positive")
    require(N_roots == 2, "N does not have exactly two real roots")
    require(sy.gcd(N_POLYNOMIAL, N_POLYNOMIAL.diff()).degree() == 0, "N has repeated root")

    interval_counts = {
        "(-inf,-4)": sturm_root_count(sturm_N, "-inf", -4),
        "(-4,-3)": sturm_root_count(sturm_N, -4, -3),
        "(-3,9/10)": sturm_root_count(sturm_N, -3, sy.Rational(9, 10)),
        "(9/10,1)": sturm_root_count(sturm_N, sy.Rational(9, 10), 1),
        "(1,+inf)": sturm_root_count(sturm_N, 1, "+inf"),
    }
    require(
        interval_counts
        == {
            "(-inf,-4)": 0,
            "(-4,-3)": 1,
            "(-3,9/10)": 0,
            "(9/10,1)": 1,
            "(1,+inf)": 0,
        },
        "transition-root isolating intervals are wrong",
    )
    endpoint_signs = {
        "N(-4)": polynomial_sign(N_POLYNOMIAL.eval(-4)),
        "N(-3)": polynomial_sign(N_POLYNOMIAL.eval(-3)),
        "N(9/10)": polynomial_sign(N_POLYNOMIAL.eval(sy.Rational(9, 10))),
        "N(1)": polynomial_sign(N_POLYNOMIAL.eval(1)),
    }
    require(
        endpoint_signs == {"N(-4)": 1, "N(-3)": -1, "N(9/10)": -1, "N(1)": 1},
        "N endpoint signs are wrong",
    )

    # At the missing t=infinity point, the leading-coefficient product is
    # negative, so it is also saddle-type.
    infinity_point = tuple(
        sy.Rational(sy.Poly(sy.together(coordinate).as_numer_denom()[0], t).LC(),
                    sy.Poly(sy.together(coordinate).as_numer_denom()[1], t).LC())
        for coordinate in parametrization
    )
    require(infinity_point == (sy.Rational(1, 2), sy.Rational(3, 2), 1), "bad limit point")

    # Exact rational inverse away from the missing point.  On the conic put
    # tau=(z-1)/(1+x-y+(z-1)/2).  Substitution recovers t, and reducing the
    # inverse-parametrization numerators modulo (L,Q) recovers x,y,z.  The
    # denominator's conic zero set is exactly the single infinity point.
    inverse_denominator = 1 + x - y + (z - 1) / 2
    inverse_parameter = sy.cancel((z - 1) / inverse_denominator)
    require(
        sy.cancel(inverse_parameter.subs(substitution) - t) == 0,
        "rational inverse does not recover t",
    )
    conic_basis = groebner((L, Q), xyz)
    for variable, coordinate_formula in zip(xyz, parametrization):
        recovered = sy.cancel(coordinate_formula.subs(t, inverse_parameter) - variable)
        numerator = sy.together(recovered).as_numer_denom()[0]
        require(
            sy.expand(conic_basis.reduce(sy.expand(numerator))[1]) == 0,
            "inverse parametrization does not recover a conic coordinate",
        )
    missing_basis = groebner((L, Q, inverse_denominator), xyz)
    require(
        basis_tuple(missing_basis)
        == (
            x - z / 4 - sy.Rational(1, 4),
            y - 3 * z / 4 - sy.Rational(3, 4),
            z**2 - 2 * z + 1,
        ),
        "parametrization has more than one missing conic point",
    )
    require(
        -6272 * N_POLYNOMIAL.LC() < 0 and -8 * T_POLYNOMIAL.LC() < 0,
        "infinity stability sign is wrong",
    )

    return {
        "trace_formula": "-8*T(t)/d(t)^2",
        "product_formula": "-6272*N(t)/d(t)^4",
        "discriminant_formula": "64*E(t)/d(t)^4",
        "sturm_sequence_degrees": {
            "T": [poly.degree() for poly in sturm_T],
            "E": [poly.degree() for poly in sturm_E],
            "N": [poly.degree() for poly in sturm_N],
        },
        "real_root_counts": {"T": T_roots, "E": E_roots, "N": N_roots},
        "N_interval_counts": interval_counts,
        "N_endpoint_signs": endpoint_signs,
        "transition_intervals": ["(-4,-3)", "(9/10,1)"],
        "normally_attracting": "alpha<t<beta",
        "saddle_type": "t<alpha or t>beta, including t=infinity",
        "nonhyperbolic": "t=alpha or t=beta",
        "theorem_interval_classification": {
            "attracting": "-1<t<beta",
            "nonhyperbolic": "t=beta",
            "saddle_type": "beta<t<1",
        },
        "infinity_point": ["1/2", "3/2", "1"],
        "parametrization_coverage": "all_real_ellipse_points_except_infinity_point",
    }


def run_audit() -> dict:
    family_summary = audit_family()
    matrix = reconstruct_family_matrix()
    original_summary, clean_summary, original_field, clean_field = (
        audit_rate_specializations(matrix)
    )
    optimality = audit_integer_optimality()
    radicals = {
        "original": audit_radical(original_field, "original"),
        "clean": audit_radical(clean_field, "clean"),
    }
    stability = audit_transverse_stability(original_field)

    result = {
        "schema": "wr-continuum-independent-v2-audit-1",
        "status": "PASS",
        "arithmetic": "exact_QQ_no_floating_point",
        "family": family_summary,
        "original_rates": original_summary,
        "clean_rates": clean_summary,
        "integer_optimality": optimality,
        "steady_ideals": radicals,
        "transverse_stability": stability,
        "geometric_gcd_audit": {
            "status": "PASS",
            "lemma": "gcd_one_over_Q_persists_after_extension_to_R_and_C",
            "generic_family_claim": "nonempty_Zariski_open_geometrically_coprime_subset",
        },
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit only the machine-readable audit result",
    )
    arguments = parser.parse_args()
    result = run_audit()

    frozen_output = Path(__file__).with_name("audit_results.json")
    if frozen_output.exists():
        with frozen_output.open(encoding="utf-8") as handle:
            require(json.load(handle) == result, "audit_results.json is stale")

    if arguments.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    print("PASS: independent v2 audit succeeded")
    print("  family matrix rank/nullity: 16/4; asserted minor exact")
    print("  positive cone and both interior rate specializations: exact")
    print("  original and clean affine/homogenized gcds: 1")
    print("  fixed-support integer minima: max=10296, sum=52464")
    print("  original and clean steady ideals: radical conic + 15 points")
    print("  Sturm counts: roots(T,E,N)=(0,0,2); transition intervals exact")
    print("  machine-readable result: audit_results.json")


if __name__ == "__main__":
    main()
