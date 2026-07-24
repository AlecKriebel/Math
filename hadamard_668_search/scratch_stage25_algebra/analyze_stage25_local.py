#!/usr/bin/env python3
"""Exact local algebra at the two certified stage-2.5 phase witnesses.

This is deliberately a diagnostic instrument, not a solver.  It replays a
stored 36-coordinate witness in the 35-dimensional delayed-E1 hyperplane,
then computes:

* the Jacobian and tangent space of the eighteen digit-2 quadrics;
* restricted Hessian ranks and their common radical;
* the first-order correction system for the eighteen remaining digit-3
  cubics;
* exact searches on small affine sheets selected by those linearized
  corrections.

Every calculation is over F_3.  The script does not infer a global
nonexistence statement from a local or bounded calculation.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
CARRY_ROOT = SEARCH_ROOT / "digit3_carry_algebra"
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
HIGHER_DIGITS = SECOND_DIGIT / "higher_digits"
sys.path.insert(0, str(CARRY_ROOT))
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(HIGHER_DIGITS))
sys.path.insert(0, str(SEARCH_ROOT))

import audit_digit3_carry as carry  # noqa: E402
import audit_digit3_xl as xl  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402


WITNESSES = HIGHER_DIGITS / "stage_2_5_witnesses.json"
GENERIC_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def dot(left: Sequence[int], right: Sequence[int]) -> int:
    return sum(int(a) * int(b) for a, b in zip(left, right)) % 3


def matvec(
    matrix: Sequence[Sequence[int]], vector: Sequence[int]
) -> tuple[int, ...]:
    return tuple(dot(row, vector) for row in matrix)


def transpose(matrix: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    if not matrix:
        return ()
    return tuple(tuple(row[column] for row in matrix) for column in range(len(matrix[0])))


def linear_combination(
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
    coordinates: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        (
            int(origin[index])
            + sum(
                int(coefficient) * int(vector[index])
                for coefficient, vector in zip(coordinates, basis)
            )
        )
        % 3
        for index in range(len(origin))
    )


def evaluate_polynomial(
    polynomial: xl.Polynomial, point: Sequence[int]
) -> int:
    """Small allocation-free evaluator for repeated sheet checks."""

    total = 0
    for monomial, coefficient in polynomial.items():
        value = int(coefficient)
        for variable in monomial:
            value *= int(point[variable])
        total += value
    return total % 3


def gradient(polynomial: xl.Polynomial, point: Sequence[int]) -> tuple[int, ...]:
    """Formal gradient of a reduced polynomial at a ternary point."""

    values = []
    for variable in range(len(point)):
        plus = list(point)
        minus = list(point)
        plus[variable] = (plus[variable] + 1) % 3
        minus[variable] = (minus[variable] - 1) % 3
        values.append(
            2
            * (
                evaluate_polynomial(polynomial, tuple(plus))
                - evaluate_polynomial(polynomial, tuple(minus))
            )
            % 3
        )
    return tuple(values)


def hessian(
    polynomial: xl.Polynomial, point: Sequence[int]
) -> tuple[tuple[int, ...], ...]:
    """Formal Hessian of a reduced degree-at-most-three polynomial."""

    variables = len(point)
    result = [[0] * variables for _ in range(variables)]
    for monomial, coefficient in polynomial.items():
        multiplicities = Counter(monomial)
        for left in range(variables):
            if not multiplicities[left]:
                continue
            for right in range(variables):
                if left == right:
                    multiplier = (
                        multiplicities[left]
                        * (multiplicities[left] - 1)
                    )
                    if not multiplier:
                        continue
                    remaining = dict(multiplicities)
                    remaining[left] -= 2
                else:
                    if not multiplicities[right]:
                        continue
                    multiplier = (
                        multiplicities[left] * multiplicities[right]
                    )
                    remaining = dict(multiplicities)
                    remaining[left] -= 1
                    remaining[right] -= 1
                value = int(coefficient) * multiplier
                for variable, exponent in remaining.items():
                    value *= int(point[variable]) ** exponent
                result[left][right] += value
    return tuple(
        tuple(value % 3 for value in row) for row in result
    )


def solve_affine(
    matrix: Sequence[Sequence[int]],
    target: Sequence[int],
    variables: int,
) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]] | None:
    augmented = tuple(
        tuple(int(value) % 3 for value in row) + (int(rhs) % 3,)
        for row, rhs in zip(matrix, target)
    )
    origin = second.canonical_solution(augmented, variables)
    if origin is None:
        return None
    return origin, second.nullspace_basis(matrix, variables)


def normalize_monomial(monomial: Iterable[int]) -> tuple[int, ...]:
    """Reduce by x^3=x in the ternary function ring."""

    reduced = []
    for variable, exponent in sorted(Counter(monomial).items()):
        reduced.extend(
            [variable] * (1 if exponent % 2 else 2)
        )
    return tuple(reduced)


def multiply_polynomials(
    left: xl.Polynomial, right: xl.Polynomial
) -> xl.Polynomial:
    result: xl.Polynomial = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            xl.add_term(
                result,
                normalize_monomial(monomial_left + monomial_right),
                coefficient_left * coefficient_right,
            )
    return result


def substitute_affine(
    polynomial: xl.Polynomial,
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
) -> xl.Polynomial:
    """Substitute x=origin+basis*z into a reduced polynomial."""

    expressions = []
    for source in range(len(origin)):
        expression: xl.Polynomial = {}
        xl.add_term(expression, (), origin[source])
        for variable, vector in enumerate(basis):
            xl.add_term(expression, (variable,), vector[source])
        expressions.append(expression)
    result: xl.Polynomial = {}
    for monomial, coefficient in polynomial.items():
        term: xl.Polynomial = {(): coefficient % 3}
        for source in monomial:
            term = multiply_polynomials(term, expressions[source])
        for reduced, value in term.items():
            xl.add_term(result, reduced, value)
    return result


def xl_tangent_audit(
    quadrics: Sequence[xl.Polynomial],
    cubics: Sequence[xl.Polynomial],
    point: Sequence[int],
    tangent_basis: Sequence[Sequence[int]],
) -> dict[str, object]:
    """Degree-three XL on the affine tangent slice through the witness."""

    restricted_quadrics = tuple(
        substitute_affine(polynomial, point, tangent_basis)
        for polynomial in quadrics
    )
    restricted_cubics = tuple(
        substitute_affine(polynomial, point, tangent_basis)
        for polynomial in cubics
    )
    if any(
        any(len(monomial) < 2 for monomial in polynomial)
        for polynomial in restricted_quadrics
    ):
        raise AssertionError(
            "a tangent-restricted root quadric retained degree below two"
        )
    variables = len(tangent_basis)
    rows = []
    for polynomial in restricted_quadrics:
        rows.append(polynomial)
        rows.extend(
            xl.multiply_by_variable(polynomial, variable)
            for variable in range(variables)
        )
    rows.extend(restricted_cubics)
    monomials = xl.monomial_catalog(variables)
    indices = {monomial: index for index, monomial in enumerate(monomials)}
    if any(
        monomial not in indices
        for polynomial in rows
        for monomial in polynomial
    ):
        raise AssertionError("tangent XL escaped reduced degree three")
    bit_rows = tuple(
        xl.polynomial_bits(polynomial, indices) for polynomial in rows
    )
    degree_masks = {
        degree: sum(
            1 << index
            for index, monomial in enumerate(monomials)
            if len(monomial) == degree
        )
        for degree in range(4)
    }
    all_mask = (1 << len(monomials)) - 1
    full_rank = xl.rank_bits(bit_rows, all_mask)
    cubic_projection = xl.rank_bits(bit_rows, degree_masks[3])
    degree_at_least_two = xl.rank_bits(
        bit_rows, degree_masks[2] | degree_masks[3]
    )
    nonconstant = xl.rank_bits(
        bit_rows,
        degree_masks[1] | degree_masks[2] | degree_masks[3],
    )
    quadric_bits = tuple(
        xl.polynomial_bits(polynomial, indices)
        for polynomial in restricted_quadrics
    )
    quadric_rank = xl.rank_bits(
        quadric_bits, degree_masks[2]
    )
    return {
        "variables": variables,
        "quadrics": len(restricted_quadrics),
        "cubics": len(restricted_cubics),
        "rows": len(rows),
        "monomials": len(monomials),
        "original_quadric_rank": quadric_rank,
        "full_rank": full_rank,
        "cubic_projection_rank": cubic_projection,
        "quadratic_or_lower_intersection": full_rank - cubic_projection,
        "linear_or_lower_intersection": full_rank - degree_at_least_two,
        "constant_only_intersection": full_rank - nonconstant,
        "degree3_refutation": full_rank - nonconstant > 0,
        "quadrics_sha256": compact_hash(
            tuple(tuple(sorted(polynomial.items())) for polynomial in restricted_quadrics)
        ),
        "cubics_sha256": compact_hash(
            tuple(tuple(sorted(polynomial.items())) for polynomial in restricted_cubics)
        ),
    }


def xl_delayed_hyperplane_audit(
    quadrics: Sequence[xl.Polynomial],
    cubics: Sequence[xl.Polynomial],
    variables: int,
) -> dict[str, object]:
    """Degree-three XL on the full delayed-row hyperplane.

    Unlike the optional tangent substitution, this is the same small
    bit-packed calculation as the production XL certificate, generalized
    here to the witness's profile.
    """

    rows = []
    for polynomial in quadrics:
        rows.append(polynomial)
        rows.extend(
            xl.multiply_by_variable(polynomial, variable)
            for variable in range(variables)
        )
    rows.extend(cubics)
    monomials = xl.monomial_catalog(variables)
    indices = {monomial: index for index, monomial in enumerate(monomials)}
    bit_rows = tuple(
        xl.polynomial_bits(polynomial, indices) for polynomial in rows
    )
    degree_masks = {
        degree: sum(
            1 << index
            for index, monomial in enumerate(monomials)
            if len(monomial) == degree
        )
        for degree in range(4)
    }
    all_mask = (1 << len(monomials)) - 1
    full_rank = xl.rank_bits(bit_rows, all_mask)
    cubic_projection = xl.rank_bits(bit_rows, degree_masks[3])
    degree_at_least_two = xl.rank_bits(
        bit_rows, degree_masks[2] | degree_masks[3]
    )
    nonconstant = xl.rank_bits(
        bit_rows,
        degree_masks[1] | degree_masks[2] | degree_masks[3],
    )
    quadric_bits = tuple(
        xl.polynomial_bits(polynomial, indices)
        for polynomial in quadrics
    )
    quadric_rank = xl.rank_bits(
        quadric_bits,
        degree_masks[0] | degree_masks[1] | degree_masks[2],
    )
    quadratic_or_lower = full_rank - cubic_projection
    linear_or_lower = full_rank - degree_at_least_two
    constant_only = full_rank - nonconstant
    return {
        "variables": variables,
        "rows": len(rows),
        "monomials": len(monomials),
        "original_quadric_rank": quadric_rank,
        "full_rank": full_rank,
        "cubic_projection_rank": cubic_projection,
        "quadratic_or_lower_intersection": quadratic_or_lower,
        "linear_or_lower_intersection": linear_or_lower,
        "constant_only_intersection": constant_only,
        "new_quadratic_beyond_original_span": (
            quadratic_or_lower - quadric_rank
        ),
        "degree3_refutation": constant_only > 0,
        "new_linear_consequence": linear_or_lower > 0,
        "new_quadratic_consequence": quadratic_or_lower > quadric_rank,
    }


def restrict_polar(
    polar: Sequence[Sequence[int]],
    basis: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(
                int(left[source_left])
                * int(polar[source_left][source_right])
                * int(right[source_right])
                for source_left in range(len(polar))
                for source_right in range(len(polar))
            )
            % 3
            for right in basis
        )
        for left in basis
    )


def common_radical_dimension(
    restricted_polars: Sequence[Sequence[Sequence[int]]],
    variables: int,
) -> tuple[int, int]:
    stacked = tuple(
        tuple(matrix[row][column] for column in range(variables))
        for matrix in restricted_polars
        for row in range(variables)
    )
    rank = second.matrix_rank(stacked)
    return rank, variables - rank


def evaluate_system(
    quadrics: Sequence[xl.Polynomial],
    cubics: Sequence[xl.Polynomial],
    point: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return (
        tuple(evaluate_polynomial(polynomial, point) for polynomial in quadrics),
        tuple(evaluate_polynomial(polynomial, point) for polynomial in cubics),
    )


def enumerate_sheet(
    base_point: Sequence[int],
    tangent_basis: Sequence[Sequence[int]],
    sheet_origin: Sequence[int],
    sheet_basis: Sequence[Sequence[int]],
    quadrics: Sequence[xl.Polynomial],
    cubics: Sequence[xl.Polynomial],
    maximum_dimension: int,
) -> dict[str, object]:
    dimension = len(sheet_basis)
    if dimension > maximum_dimension:
        return {
            "dimension": dimension,
            "enumerated": False,
            "reason": f"dimension exceeds cap {maximum_dimension}",
        }
    points = 3**dimension
    digit2_hits = 0
    best_digit3 = len(cubics) + 1
    histogram: Counter[int] = Counter()
    best_point = None
    digit3_hits = 0
    for coefficients in itertools.product(range(3), repeat=dimension):
        tangent_coordinates = linear_combination(
            sheet_origin, sheet_basis, coefficients
        )
        displacement = linear_combination(
            (0,) * len(base_point), tangent_basis, tangent_coordinates
        )
        point = tuple(
            (int(left) + int(right)) % 3
            for left, right in zip(base_point, displacement)
        )
        q_values, c_values = evaluate_system(quadrics, cubics, point)
        if any(q_values):
            continue
        digit2_hits += 1
        residual = sum(value != 0 for value in c_values)
        histogram[residual] += 1
        if residual < best_digit3:
            best_digit3 = residual
            best_point = point
        if residual == 0:
            digit3_hits += 1
    return {
        "dimension": dimension,
        "enumerated": True,
        "points": points,
        "digit2_hits": digit2_hits,
        "digit3_hits": digit3_hits,
        "digit3_residual_histogram": dict(sorted(histogram.items())),
        "best_digit3_nonzero": None if best_point is None else best_digit3,
        "best_point_sha256": None if best_point is None else compact_hash(best_point),
        "best_point": best_point,
    }


def select_witness(stored: dict[str, object], candidate_index: int) -> dict[str, object]:
    candidates = [
        item
        for item in stored["witnesses"]
        if int(item["candidate_index"]) == candidate_index
    ]
    if len(candidates) != 1:
        raise AssertionError(
            f"expected one stored witness for candidate {candidate_index}"
        )
    return candidates[0]


def analyze(
    candidate_index: int,
    maximum_sheet_dimension: int,
    include_xl: bool,
) -> dict[str, object]:
    stored = json.loads(WITNESSES.read_text())
    witness = select_witness(stored, candidate_index)
    original_point = tuple(map(int, witness["affine_coordinates"]))

    candidate = second.CANDIDATES[candidate_index]
    profiles = second.profiles_from_ids(candidate[3], candidate[4])
    equations = second.first_digit_equations(profiles)
    original_origin, original_basis = second.affine_parameterization(equations, 54)
    placement = second.lift_affine_point(
        original_origin, original_basis, original_point
    )
    if compact_hash(original_point) != witness["affine_coordinates_sha256"]:
        raise AssertionError("the stored affine-coordinate hash changed")
    if compact_hash(placement) != witness["placement_trits_sha256"]:
        raise AssertionError("the stored placement hash changed")

    (
        profiles35,
        origin35,
        basis35,
        rows35,
        hyperplane,
    ) = xl.delayed_hyperplane(candidate_index)
    if profiles35 != profiles:
        raise AssertionError("profile reconstruction disagreed")
    pivot = int(hyperplane["eliminated_coordinate"])
    free = tuple(index for index in range(36) if index != pivot)
    point = tuple(original_point[index] for index in free)
    if second.lift_affine_point(origin35, basis35, point) != placement:
        raise AssertionError("the witness did not lie on the delayed hyperplane")

    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles), origin35, basis35
    )
    quadrics = tuple(
        xl.quadratic_polynomial(
            constants[index], linears[index], polars[index]
        )
        for index in GENERIC_ROWS
    )
    cubics = tuple(xl.digit3_polynomial(rows35[index]) for index in GENERIC_ROWS)
    q_values, c_values = evaluate_system(quadrics, cubics, point)
    if any(q_values):
        raise AssertionError("stored stage-2.5 point failed a digit-2 quadric")
    exact_statistics = tuple(
        carry.row_statistics(row, point) for row in rows35
    )
    exact_values = second.displayed_values(profiles, placement)
    if tuple(
        (a_value, 3 * q_value - a_value)
        for a_value, q_value in exact_statistics
    ) != exact_values:
        raise AssertionError("the local A,Q replay disagreed with exact phases")
    exact_digits = tuple(
        second.lambda_digits(value, 9) for value in exact_values
    )
    nonzero_by_digit = tuple(
        sum(row[digit] != 0 for row in exact_digits)
        for digit in range(9)
    )
    if nonzero_by_digit != tuple(witness["digit_nonzero_rows_through_8"]):
        raise AssertionError("the stored exact digit counts changed")
    if exact_values[7] != tuple(witness["delayed_e1_origin_exact_value"]):
        raise AssertionError("the stored delayed-row exact value changed")
    if tuple(exact_digits[7]) != tuple(
        witness["delayed_e1_origin_digits_through_8"]
    ):
        raise AssertionError("the stored delayed-row digits changed")
    if witness["row_margin_join_holds"] is not False:
        raise AssertionError("the witness unexpectedly entered the row-margin join")
    if exact_statistics[7][0] % 9:
        raise AssertionError("stored point failed delayed E1 at digit 3")
    if c_values != tuple(
        (exact_statistics[index][0] // 3) % 3 for index in GENERIC_ROWS
    ):
        raise AssertionError("digit-3 cubics failed exact replay")

    jacobian_q = tuple(gradient(polynomial, point) for polynomial in quadrics)
    jacobian_c = tuple(gradient(polynomial, point) for polynomial in cubics)
    q_rank = second.matrix_rank(jacobian_q)
    tangent_basis = second.nullspace_basis(jacobian_q, 35)
    tangent_dimension = len(tangent_basis)
    restricted_polars = tuple(
        restrict_polar(polars[index], tangent_basis)
        for index in GENERIC_ROWS
    )
    if tuple(hessian(polynomial, point) for polynomial in quadrics) != tuple(
        polars[index] for index in GENERIC_ROWS
    ):
        raise AssertionError("formal quadric Hessians changed")
    radical_rank, radical_dimension = common_radical_dimension(
        restricted_polars, tangent_dimension
    )
    restricted_ranks = tuple(
        second.matrix_rank(matrix) for matrix in restricted_polars
    )
    cubic_hessians = tuple(
        hessian(polynomial, point) for polynomial in cubics
    )
    restricted_cubic_hessians = tuple(
        restrict_polar(matrix, tangent_basis) for matrix in cubic_hessians
    )
    cubic_hessian_ranks = tuple(
        second.matrix_rank(matrix) for matrix in restricted_cubic_hessians
    )
    (
        cubic_hessian_stack_rank,
        cubic_hessian_common_radical,
    ) = common_radical_dimension(
        restricted_cubic_hessians, tangent_dimension
    )

    jacobian_c_tangent = tuple(
        tuple(dot(row, vector) for vector in tangent_basis)
        for row in jacobian_c
    )
    c_tangent_rank = second.matrix_rank(jacobian_c_tangent)
    combined_rank = second.matrix_rank((*jacobian_q, *jacobian_c))
    cubic_gradient_relations = second.nullspace_basis(
        transpose(jacobian_c_tangent), len(cubics)
    )
    cubic_relation_syndrome = tuple(
        dot(relation, c_values) for relation in cubic_gradient_relations
    )
    all_linearized = solve_affine(
        jacobian_c_tangent,
        tuple(-value % 3 for value in c_values),
        tangent_dimension,
    )

    nonzero_rows = tuple(
        index for index, value in enumerate(c_values) if value
    )
    nonzero_matrix = tuple(jacobian_c_tangent[index] for index in nonzero_rows)
    nonzero_target = tuple(-c_values[index] % 3 for index in nonzero_rows)
    nonzero_linearized = solve_affine(
        nonzero_matrix, nonzero_target, tangent_dimension
    )
    nonzero_sheet = (
        {
            "consistent": False,
            "equations": len(nonzero_rows),
            "rank": second.matrix_rank(nonzero_matrix),
        }
        if nonzero_linearized is None
        else {
            "consistent": True,
            "equations": len(nonzero_rows),
            "rank": second.matrix_rank(nonzero_matrix),
            "search": enumerate_sheet(
                point,
                tangent_basis,
                nonzero_linearized[0],
                nonzero_linearized[1],
                quadrics,
                cubics,
                maximum_sheet_dimension,
            ),
        }
    )

    # Also test every leave-one-out correction sheet when the full
    # linearized cubic system is inconsistent.  These sheets are usually
    # zero- or one-dimensional and hence exactly enumerable.
    leave_one_out = []
    if all_linearized is None:
        for omitted in range(len(cubics)):
            selected = tuple(
                index for index in range(len(cubics)) if index != omitted
            )
            system = solve_affine(
                tuple(jacobian_c_tangent[index] for index in selected),
                tuple(-c_values[index] % 3 for index in selected),
                tangent_dimension,
            )
            record: dict[str, object] = {"omitted_equation": omitted}
            if system is None:
                record["consistent"] = False
            else:
                record["consistent"] = True
                record["search"] = enumerate_sheet(
                    point,
                    tangent_basis,
                    system[0],
                    system[1],
                    quadrics,
                    cubics,
                    maximum_sheet_dimension,
                )
            leave_one_out.append(record)

    # The preferred candidate 0 happens to satisfy one equation beyond the
    # stage-2.5 target: delayed E1(origin)'s digit 4.  Interpolate that
    # quadratic exactly on the 35-space and measure whether it changes the
    # local geometry.  Candidate 2 is retained as a comparison even though
    # it does not satisfy this extra equation.
    def delayed_digit4_evaluate(value: Sequence[int]) -> tuple[int, ...]:
        a_value, q_value = carry.row_statistics(rows35[7], value)
        exact = (a_value, 3 * q_value - a_value)
        digits = second.lambda_digits(exact, 5)
        if any(digits[:4]):
            raise AssertionError(
                "the delayed hyperplane lost its first four row-7 digits"
            )
        return (digits[4],)

    (
        delayed4_constants,
        delayed4_linears,
        delayed4_polars,
    ) = second.interpolate_quadratics(
        delayed_digit4_evaluate, 35, 1
    )
    delayed4 = xl.quadratic_polynomial(
        delayed4_constants[0],
        delayed4_linears[0],
        delayed4_polars[0],
    )
    if evaluate_polynomial(delayed4, point) != delayed_digit4_evaluate(point)[0]:
        raise AssertionError("the delayed digit-4 interpolation failed replay")
    delayed4_gradient = gradient(delayed4, point)
    extended_jacobian = (*jacobian_q, delayed4_gradient)
    extended_tangent_basis = second.nullspace_basis(
        extended_jacobian, 35
    )
    extra_geometry: dict[str, object] = {
        "value": evaluate_polynomial(delayed4, point),
        "quadratic_sha256": compact_hash(tuple(sorted(delayed4.items()))),
        "polar_rank_in_35_space": second.matrix_rank(
            delayed4_polars[0]
        ),
        "jacobian_rank_with_digit2": second.matrix_rank(
            extended_jacobian
        ),
        "extended_tangent_dimension": len(extended_tangent_basis),
        "quadratic_function_span_rank_before": second.matrix_rank(
            tuple(
                tuple(
                    polynomial.get(monomial, 0)
                    for monomial in xl.monomial_catalog(35)
                    if len(monomial) <= 2
                )
                for polynomial in quadrics
            )
        ),
    }
    degree2_catalog = tuple(
        monomial
        for monomial in xl.monomial_catalog(35)
        if len(monomial) <= 2
    )
    q_vectors = tuple(
        tuple(polynomial.get(monomial, 0) for monomial in degree2_catalog)
        for polynomial in quadrics
    )
    delayed4_vector = tuple(
        delayed4.get(monomial, 0) for monomial in degree2_catalog
    )
    extra_geometry["quadratic_function_span_rank_after"] = (
        second.matrix_rank((*q_vectors, delayed4_vector))
    )
    if evaluate_polynomial(delayed4, point) == 0:
        extended_c_jacobian = tuple(
            tuple(dot(row, vector) for vector in extended_tangent_basis)
            for row in jacobian_c
        )
        extra_geometry.update(
            {
                "remaining_cubic_jacobian_rank_on_extended_tangent": (
                    second.matrix_rank(extended_c_jacobian)
                ),
                "combined_rank_with_remaining_cubics": second.matrix_rank(
                    (*extended_jacobian, *jacobian_c)
                ),
            }
        )
        if include_xl:
            extra_geometry["degree3_xl_on_extended_tangent"] = (
                xl_tangent_audit(
                    (*quadrics, delayed4),
                    cubics,
                    point,
                    extended_tangent_basis,
                )
            )

    result = {
        "schema": "lp333-order3-stage25-local-algebra-v1",
        "candidate_index": candidate_index,
        "label": candidate[0],
        "witness": {
            "affine_coordinates_sha256": compact_hash(original_point),
            "placement_trits_sha256": compact_hash(placement),
            "delayed_e1_exact_A_Q": exact_statistics[7],
            "remaining_digit3_values": c_values,
            "remaining_digit3_nonzero": sum(value != 0 for value in c_values),
        },
        "digit2_local_geometry": {
            "ambient_hyperplane_dimension": 35,
            "jacobian_rank": q_rank,
            "tangent_dimension": tangent_dimension,
            "restricted_hessian_ranks": restricted_ranks,
            "restricted_hessian_rank_histogram": dict(
                sorted(Counter(restricted_ranks).items())
            ),
            "stacked_restricted_hessian_rank": radical_rank,
            "common_radical_dimension": radical_dimension,
        },
        "digit3_linearization": {
            "restricted_jacobian_rank": c_tangent_rank,
            "combined_jacobian_rank_in_35_space": combined_rank,
            "restricted_gradient_relation_dimension": len(
                cubic_gradient_relations
            ),
            "restricted_gradient_relations": cubic_gradient_relations,
            "residual_syndrome_on_gradient_relations": (
                cubic_relation_syndrome
            ),
            "all_18_corrections_consistent": all_linearized is not None,
            "all_18_correction_dimension": (
                None if all_linearized is None else len(all_linearized[1])
            ),
            "nonzero_residual_correction_sheet": nonzero_sheet,
            "leave_one_out_sheets": leave_one_out,
            "restricted_cubic_hessian_ranks": cubic_hessian_ranks,
            "restricted_cubic_hessian_rank_histogram": dict(
                sorted(Counter(cubic_hessian_ranks).items())
            ),
            "stacked_restricted_cubic_hessian_rank": (
                cubic_hessian_stack_rank
            ),
            "common_cubic_hessian_radical_dimension": (
                cubic_hessian_common_radical
            ),
        },
        "degree3_xl_on_digit2_tangent": (
            xl_tangent_audit(
                quadrics, cubics, point, tangent_basis
            )
            if include_xl
            else {
                "status": "SKIPPED",
                "reason": (
                    "Optional diagnostic omitted; the exact Jacobian, "
                    "Hessian, and bounded-sheet conclusions do not depend "
                    "on it."
                ),
            }
        ),
        "degree3_xl_on_delayed_hyperplane": (
            xl_delayed_hyperplane_audit(
                quadrics, cubics, 35
            )
        ),
        "delayed_e1_digit4_extra": extra_geometry,
        "scope_warning": (
            "This witness fails the independent row-margin/trivial-character "
            "transfer.  The calculation concerns only the phase system and "
            "does not put the witness on the physical LP(333) intersection."
        ),
    }
    result["semantic_sha256"] = compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, choices=(0, 2), default=0)
    parser.add_argument("--maximum-sheet-dimension", type=int, default=10)
    parser.add_argument("--include-xl", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(
        args.candidate,
        args.maximum_sheet_dimension,
        args.include_xl,
    )
    payload = json.dumps(result, indent=2)
    if args.output is not None:
        args.output.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()
