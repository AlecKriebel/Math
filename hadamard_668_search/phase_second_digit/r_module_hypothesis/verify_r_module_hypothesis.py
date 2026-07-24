#!/usr/bin/env python3
"""Falsify the free-rank-two ramified-module hypothesis exactly.

The proposed coefficient algebra is

    R = (F_27 x F_27)[epsilon]/(epsilon^3),

of dimension 18 over F_3.  If the 36-dimensional first-digit translation
space were a free rank-two R-module and the full second digit were an
R-valued quadratic norm, then:

1. the residue layer T0 would factor through V/epsilon*V, of dimension 12;
2. epsilon*V, of dimension 24, would lie in the common T0 polar radical;
3. the compatible self-adjoint centroid of all 18 scalar polar forms would
   contain a faithful 18-dimensional copy of R.

This verifier reconstructs the five exact profiles and disproves all three
requirements using exact F_3 linear algebra.  No phase point is enumerated.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
SECOND_DIGIT = HERE.parent
SEARCH_ROOT = SECOND_DIGIT.parent
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_phase_second_digit as base  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    first_digit_equations,
    matrix_rank,
    profiles_from_ids,
)


P = 3
DIMENSION = 36
ENDOMORPHISM_DIMENSION = DIMENSION * DIMENSION
EXPECTED_CENTROID_DIMENSION = 1
EXPECTED_SEMANTIC_SHA256 = (
    "a09bcdb69480fb94c79e941db77c8081e8a5403b4472863c557db7c1f2d0ce58"
)

Vector = tuple[int, ...]
Matrix = tuple[tuple[int, ...], ...]
TernaryBits = tuple[int, int]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def combine_vectors(
    coefficients: Sequence[int],
    rows: Sequence[Sequence[int]],
) -> Vector:
    return tuple(
        sum(
            int(coefficient) * int(row[column])
            for coefficient, row in zip(coefficients, rows)
        )
        % P
        for column in range(len(rows[0]))
    )


def combine_matrices(
    coefficients: Sequence[int],
    matrices: Sequence[Matrix],
) -> Matrix:
    size = len(matrices[0])
    return tuple(
        tuple(
            sum(
                int(coefficient) * matrix[row][column]
                for coefficient, matrix in zip(coefficients, matrices)
            )
            % P
            for column in range(size)
        )
        for row in range(size)
    )


def flatten_symmetric(matrix: Matrix) -> Vector:
    return tuple(
        matrix[left][right]
        for left in range(len(matrix))
        for right in range(left, len(matrix))
    )


def hasse_layers(
    constants: Sequence[int],
    linears: Sequence[Vector],
    polars: Sequence[Matrix],
) -> tuple[
    tuple[Vector, tuple[Vector, ...], tuple[Matrix, ...]], ...
]:
    """Return coefficients of q0+epsilon*q1+epsilon^2*q2.

    At one lag,

        E0 + alpha E1 + alpha^2 E2
        = (E0+E1+E2)
          + epsilon*(E1+2E2)
          + epsilon^2*E2,

    where the displayed E1 at the opposite lag supplies E2 at this digit.
    """

    specifications = (
        tuple(
            ((1 + lag, 8 + lag, 14 + lag), (1, 1, 1))
            for lag in range(6)
        ),
        tuple(
            ((8 + lag, 14 + lag), (1, 2))
            for lag in range(6)
        ),
        tuple(
            ((14 + lag,), (1,))
            for lag in range(6)
        ),
    )
    result = []
    for layer in specifications:
        result.append((
            tuple(
                sum(
                    coefficient * constants[index]
                    for index, coefficient in zip(indices, coefficients)
                )
                % P
                for indices, coefficients in layer
            ),
            tuple(
                combine_vectors(
                    coefficients,
                    tuple(linears[index] for index in indices),
                )
                for indices, coefficients in layer
            ),
            tuple(
                combine_matrices(
                    coefficients,
                    tuple(polars[index] for index in indices),
                )
                for indices, coefficients in layer
            ),
        ))
    return tuple(result)


def common_radical_nullity(polars: Sequence[Matrix]) -> int:
    stacked = tuple(row for matrix in polars for row in matrix)
    return DIMENSION - matrix_rank(stacked)


def ternary_add(
    left: TernaryBits,
    right: TernaryBits,
    mask: int,
) -> TernaryBits:
    """Add two packed F_3 rows encoded by their digit-one/digit-two bits."""

    left_one, left_two = left
    right_one, right_two = right
    left_zero = mask ^ (left_one | left_two)
    right_zero = mask ^ (right_one | right_two)
    return (
        (left_zero & right_one)
        | (left_one & right_zero)
        | (left_two & right_two),
        (left_zero & right_two)
        | (left_two & right_zero)
        | (left_one & right_one),
    )


def packed_rank(
    rows: Iterable[TernaryBits],
    columns: int,
) -> int:
    """Streaming exact Gaussian rank over F_3 using two Python bitsets."""

    mask = (1 << columns) - 1
    basis: dict[int, TernaryBits] = {}
    for one, two in rows:
        if one & two or (one | two) & ~mask:
            raise ValueError("invalid packed ternary row")
        while one | two:
            lowest = (one | two) & -(one | two)
            pivot = lowest.bit_length() - 1
            if pivot not in basis:
                if two & lowest:
                    one, two = two, one
                basis[pivot] = (one, two)
                break
            basis_one, basis_two = basis[pivot]
            if one & lowest:
                # row - basis = row + 2*basis.
                one, two = ternary_add(
                    (one, two), (basis_two, basis_one), mask
                )
            else:
                # row - 2*basis = row + basis.
                one, two = ternary_add(
                    (one, two), (basis_one, basis_two), mask
                )
    return len(basis)


def audit_packed_rank_primitive() -> int:
    """Compare packed elimination with the established dense primitive."""

    checks = 0
    for rows in range(1, 7):
        for columns in range(1, 7):
            matrix = tuple(
                tuple(
                    (
                        row * row
                        + 2 * row * column
                        + column * column * column
                        + checks
                    )
                    % P
                    for column in range(columns)
                )
                for row in range(rows)
            )
            packed = []
            for row in matrix:
                one = two = 0
                for column, value in enumerate(row):
                    if value == 1:
                        one |= 1 << column
                    elif value == 2:
                        two |= 1 << column
                packed.append((one, two))
            if packed_rank(packed, columns) != matrix_rank(matrix):
                raise AssertionError("packed rank primitive disagrees")
            checks += 1
    if checks != 36:
        raise AssertionError("packed rank primitive check count changed")
    return checks


def centroid_constraint_rows(polars: Sequence[Matrix]) -> Iterable[TernaryBits]:
    """Yield A^T B_i-B_i A=0 as packed rows in the entries of A."""

    for polar in polars:
        for left in range(DIMENSION):
            for right in range(left + 1, DIMENSION):
                coefficients: dict[int, int] = {}
                for inner in range(DIMENSION):
                    # (A^T B)_(left,right)
                    value = polar[inner][right]
                    if value:
                        variable = inner * DIMENSION + left
                        coefficients[variable] = (
                            coefficients.get(variable, 0) + value
                        ) % P
                    # -(B A)_(left,right)
                    value = polar[left][inner]
                    if value:
                        variable = inner * DIMENSION + right
                        coefficients[variable] = (
                            coefficients.get(variable, 0) - value
                        ) % P
                one = two = 0
                for variable, value in coefficients.items():
                    if value == 1:
                        one |= 1 << variable
                    elif value == 2:
                        two |= 1 << variable
                if one | two:
                    yield one, two


def verify_identity_in_centroid(polars: Sequence[Matrix]) -> None:
    identity_vector = tuple(
        int(row == column)
        for row in range(DIMENSION)
        for column in range(DIMENSION)
    )
    for one, two in centroid_constraint_rows(polars):
        value = 0
        for variable, coefficient_bits in ((one, 1), (two, 2)):
            work = variable
            while work:
                lowest = work & -work
                index = lowest.bit_length() - 1
                value += coefficient_bits * identity_vector[index]
                work ^= lowest
        if value % P:
            raise AssertionError("identity is not in the polar centroid")


def audit_profile(index: int) -> dict[str, object]:
    label, partition, target, identifiers_a, identifiers_b = (
        base.CANDIDATES[index]
    )
    profiles = profiles_from_ids(identifiers_a, identifiers_b)
    equations = first_digit_equations(profiles)
    origin, basis = base.affine_parameterization(equations, 54)
    constants, linears, polars = base.derive_quadratics(
        base.second_digit_term_data(profiles), origin, basis
    )

    nonconstant_indices = tuple(range(1, 7)) + tuple(range(8, 20))
    full_polars = tuple(polars[row] for row in nonconstant_indices)
    polar_span_rank = matrix_rank(
        tuple(flatten_symmetric(matrix) for matrix in full_polars)
    )
    if polar_span_rank != 18:
        raise AssertionError("full second-digit polar span changed")

    layers = hasse_layers(constants, linears, polars)
    layer_records = []
    for layer_index, (_, _, layer_polars) in enumerate(layers):
        ranks = tuple(matrix_rank(matrix) for matrix in layer_polars)
        common_nullity = common_radical_nullity(layer_polars)
        layer_records.append({
            "layer": layer_index,
            "polar_ranks": ranks,
            "common_radical_nullity": common_nullity,
        })
    residue = layer_records[0]
    if max(residue["polar_ranks"]) <= 12:
        raise AssertionError("residue rank no longer falsifies free R-rank two")
    if residue["common_radical_nullity"] >= 24:
        raise AssertionError("a 24-dimensional nilpotent tangent appeared")

    verify_identity_in_centroid(full_polars)
    centroid_constraint_rank = packed_rank(
        centroid_constraint_rows(full_polars),
        ENDOMORPHISM_DIMENSION,
    )
    centroid_dimension = (
        ENDOMORPHISM_DIMENSION - centroid_constraint_rank
    )
    if centroid_dimension != EXPECTED_CENTROID_DIMENSION:
        raise AssertionError("compatible polar centroid changed")

    all_coordinate_ranks = tuple(
        matrix_rank(matrix) for matrix in full_polars
    )
    allowed_unimodular_norm_ranks = {0, 6, 12, 18, 24, 30, 36}
    forbidden_coordinate_ranks = tuple(
        rank
        for rank in all_coordinate_ranks
        if rank not in allowed_unimodular_norm_ranks
    )
    if not forbidden_coordinate_ranks:
        raise AssertionError("unimodular R-norm rank test stopped failing")

    return {
        "label": label,
        "partition": partition,
        "target": target,
        "first_digit_dimension": len(basis),
        "full_polar_span_rank": polar_span_rank,
        "hasse_layers": tuple(layer_records),
        "compatible_centroid": {
            "endomorphism_variables": ENDOMORPHISM_DIMENSION,
            "constraint_rank": centroid_constraint_rank,
            "dimension": centroid_dimension,
            "description": "F_3 scalar identity only",
        },
        "unimodular_norm_rank_test": {
            "allowed_ranks": tuple(sorted(allowed_unimodular_norm_ranks)),
            "actual_coordinate_ranks": all_coordinate_ranks,
            "forbidden_coordinate_ranks": forbidden_coordinate_ranks,
        },
    }


def build_certificate() -> dict[str, object]:
    primitive_checks = audit_packed_rank_primitive()
    profiles = tuple(
        audit_profile(index) for index in range(len(base.CANDIDATES))
    )
    return {
        "schema": "lp333-h2-r-module-hypothesis-falsification-v1",
        "scope": (
            "Exact homogeneous-polar test of the free rank-two module and "
            "R-valued norm hypothesis; no phase assignment enumeration."
        ),
        "proposed_algebra": (
            "F_27[epsilon]/(epsilon^3) x "
            "F_27[epsilon]/(epsilon^3)"
        ),
        "proposed_algebra_dimension": 18,
        "proposed_module_rank": 2,
        "required_residue_quotient_dimension": 12,
        "required_nilpotent_tangent_dimension": 24,
        "required_compatible_centroid_dimension_at_least": 18,
        "packed_rank_primitive_checks": primitive_checks,
        "profiles": profiles,
        "conclusion": (
            "The compatible free-rank-two R-module/R-valued norm "
            "hypothesis is false for every exact h=2 profile."
        ),
    }


def main() -> None:
    certificate = build_certificate()
    semantic_sha256 = compact_hash(certificate)
    if EXPECTED_SEMANTIC_SHA256 and (
        semantic_sha256 != EXPECTED_SEMANTIC_SHA256
    ):
        raise AssertionError("R-module falsification certificate changed")
    for profile in certificate["profiles"]:
        print(profile["label"])
        for layer in profile["hasse_layers"]:
            print(
                f"  T{layer['layer']}_ranks="
                f"{layer['polar_ranks']} "
                f"common_radical_nullity="
                f"{layer['common_radical_nullity']}"
            )
        centroid = profile["compatible_centroid"]
        print(
            "  centroid_rank_dimension="
            f"{centroid['constraint_rank']},"
            f"{centroid['dimension']}"
        )
    print(f"semantic_sha256={semantic_sha256}")


if __name__ == "__main__":
    main()
