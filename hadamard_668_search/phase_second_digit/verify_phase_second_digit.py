#!/usr/bin/env python3
"""Second placement lambda digit on the five exact h=2 profile orbits.

The first placement digit is an affine rank-18 system in 54 trits.  This
module parameterizes its 36-dimensional solution space and reconstructs the
next exact lambda digit as twenty quadratic polynomials over F_3.  It audits
the symbolic quadratics against direct Eisenstein phase equations, computes
their polar ranks and common radical, and extracts every linear combination
whose polar form vanishes.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SHELL_TWO = next(
    (
        candidate
        for candidate in (
            SEARCH_ROOT / "shell_two_exact",
            SEARCH_ROOT / "scratch_shell_two_novel",
        )
        if candidate.is_dir()
    ),
    SEARCH_ROOT / "shell_two_exact",
)
sys.path.insert(0, str(SHELL_TWO))
sys.path.insert(0, str(SEARCH_ROOT))

from verify_shell_two_exact_orbits import CANDIDATES  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    MODULUS,
    augmented_system,
    canonical_solution,
    coefficient_terms,
    first_digit_equations,
    lambda_digits,
    matrix_rank,
    matrix_rref,
    masks_from_trits,
    PhaseTerm,
    phase_entries,
    profiles_from_ids,
    symbolic_first_digits,
)
from verify_lp333_order3_phase_factor import (  # noqa: E402
    phase_columns,
    phase_equations,
)
from verify_lp333_order3_quotient import PARTS  # noqa: E402
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
)


EXPECTED_SEMANTIC_SHA256 = (
    "b8958ea3d3179aec2ae73c3e1bbb2ac76fd4f668a31422a3863f74c41bcafd60"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def nullspace_basis(
    rows: Sequence[Sequence[int]],
    columns: int | None = None,
) -> tuple[tuple[int, ...], ...]:
    """Return the canonical free-column basis of a matrix kernel."""

    if rows:
        width = len(rows[0])
        if any(len(row) != width for row in rows):
            raise ValueError("matrix is not rectangular")
        if columns is not None and columns != width:
            raise ValueError("declared column count disagrees with matrix")
        columns = width
    elif columns is None:
        raise ValueError("an empty matrix needs an explicit column count")
    assert columns is not None
    rref, pivots, _ = matrix_rref(rows)
    pivot_set = set(pivots)
    free = tuple(index for index in range(columns) if index not in pivot_set)
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rref[row][free_column] % MODULUS
        basis.append(tuple(vector))
    for vector in basis:
        if any(
            sum(left * right for left, right in zip(row, vector)) % MODULUS
            for row in rows
        ):
            raise AssertionError("kernel basis failed direct replay")
    return tuple(basis)


def displayed_values(
    profiles: Sequence[Sequence[Sequence[int]]],
    trits: Sequence[int],
) -> tuple[tuple[int, int], ...]:
    masks_a, masks_b = masks_from_trits(profiles, trits)
    equations = phase_equations(phase_columns(masks_a, masks_b))
    values = [equations[PARTS[0][0]][0]]
    values.extend(
        equations[PARTS[class_index + 1][0]][0]
        for class_index in range(6)
    )
    values.append(equations[PARTS[0][0]][1])
    values.extend(
        equations[PARTS[class_index + 1][0]][1]
        for class_index in range(12)
    )
    return tuple(values)


def direct_second_digits(
    profiles: Sequence[Sequence[Sequence[int]]],
    trits: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        lambda_digits(value, 3)[2]
        for value in displayed_values(profiles, trits)
    )


def displayed_specifications() -> tuple[tuple[str, int], ...]:
    """Return the twenty reversal-independent component/lag pairs."""

    specifications: list[tuple[str, int]] = [("E0", PARTS[0][0])]
    specifications.extend(
        ("E0", PARTS[class_index + 1][0])
        for class_index in range(6)
    )
    specifications.append(("E1", PARTS[0][0]))
    specifications.extend(
        ("E1", PARTS[class_index + 1][0])
        for class_index in range(12)
    )
    return tuple(specifications)


def second_digit_term_data(
    profiles: Sequence[Sequence[Sequence[int]]],
) -> tuple[tuple[tuple[PhaseTerm, ...], int], ...]:
    """Return terms and the lambda-zero integer constant for twenty rows."""

    entries = phase_entries(profiles)
    result = []
    for component, lag in displayed_specifications():
        terms, target = coefficient_terms(
            entries,
            component,
            lag,
        )
        constant_at_zero = sum(term.sign for term in terms) - target
        if constant_at_zero % 3:
            raise AssertionError("profile failed the lambda-zero digit")
        result.append((terms, constant_at_zero))
    return tuple(result)


def symbolic_second_digits(
    term_data: Sequence[tuple[Sequence[PhaseTerm], int]],
    trits: Sequence[int],
) -> tuple[int, ...]:
    """Evaluate the exact lambda^2 digit as a quadratic over F_3."""

    result = []
    for terms, constant_at_zero in term_data:
        # The rational integer 3 has lambda^2 digit 2.  Thus the constant
        # sum of signs contributes 2*(C/3).
        value = 2 * (constant_at_zero // 3)
        for term in terms:
            exponent = term.constant
            exponent += sum(
                coefficient * int(trits[variable])
                for variable, coefficient in term.coefficients
            )
            exponent %= 3
            # binom(exponent,2) = 2*x^2+x over F_3.
            value += term.sign * (2 * exponent * exponent + exponent)
        result.append(value % 3)
    return tuple(result)


def derive_quadratics(
    term_data: Sequence[tuple[Sequence[PhaseTerm], int]],
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
) -> tuple[
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[tuple[int, ...], ...], ...],
]:
    """Derive the second digit directly from affine phase exponents.

    If ``L=d+b.y`` then the lambda-square digit of ``omega^L`` is
    ``2 L^2+L``.  Its polar matrix is the rank-one matrix ``b b^T`` and
    its linear coefficient is ``(d+1)b`` over F_3.
    """

    variables = len(basis)
    constants = []
    linears = []
    polars = []
    for terms, constant_at_zero in term_data:
        constant = 2 * (constant_at_zero // 3)
        linear = [0] * variables
        polar = [[0] * variables for _ in range(variables)]
        for term in terms:
            affine_constant = (
                term.constant
                + sum(
                    coefficient * int(origin[variable])
                    for variable, coefficient in term.coefficients
                )
            ) % MODULUS
            affine_slope = tuple(
                sum(
                    coefficient * int(basis[column][variable])
                    for variable, coefficient in term.coefficients
                )
                % MODULUS
                for column in range(variables)
            )
            sign = term.sign % MODULUS
            constant += sign * (
                2 * affine_constant * affine_constant + affine_constant
            )
            for left in range(variables):
                linear[left] += (
                    sign
                    * (affine_constant + 1)
                    * affine_slope[left]
                )
                for right in range(variables):
                    polar[left][right] += (
                        sign
                        * affine_slope[left]
                        * affine_slope[right]
                    )
        constants.append(constant % MODULUS)
        linears.append(tuple(value % MODULUS for value in linear))
        polars.append(
            tuple(
                tuple(value % MODULUS for value in row)
                for row in polar
            )
        )
    return tuple(constants), tuple(linears), tuple(polars)


def affine_parameterization(
    equations: Sequence[object],
    variable_count: int,
) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    rows = augmented_system(equations)
    solution = canonical_solution(rows, variable_count)
    if solution is None:
        raise AssertionError("first placement digit became inconsistent")
    coefficient_rows = tuple(row[:-1] for row in rows)
    basis = nullspace_basis(coefficient_rows)
    if len(basis) != 36:
        raise AssertionError("first placement nullity changed")
    return solution, basis


def lift_affine_point(
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
    coordinates: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        (
            int(origin[row])
            + sum(
                int(coordinates[column]) * basis[column][row]
                for column in range(len(basis))
            )
        )
        % 3
        for row in range(len(origin))
    )


def interpolate_quadratics(
    evaluate,
    variables: int,
    equations: int,
) -> tuple[
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[tuple[int, ...], ...], ...],
]:
    """Interpolate constants, linears, and symmetric polar matrices."""

    zero = (0,) * variables
    constant = evaluate(zero)
    if len(constant) != equations:
        raise AssertionError("quadratic evaluator has wrong row count")
    plus_values = []
    minus_values = []
    linears = [[0] * variables for _ in range(equations)]
    diagonals = [[0] * variables for _ in range(equations)]
    polar = [
        [[0] * variables for _ in range(variables)]
        for _ in range(equations)
    ]
    for variable in range(variables):
        plus = [0] * variables
        minus = [0] * variables
        plus[variable] = 1
        minus[variable] = 2
        q_plus = evaluate(tuple(plus))
        q_minus = evaluate(tuple(minus))
        plus_values.append(q_plus)
        minus_values.append(q_minus)
        for equation in range(equations):
            linear = (q_minus[equation] - q_plus[equation]) % 3
            diagonal = (
                q_plus[equation] - constant[equation] - linear
            ) % 3
            linears[equation][variable] = linear
            diagonals[equation][variable] = diagonal
            polar[equation][variable][variable] = 2 * diagonal % 3

    for left in range(variables):
        for right in range(left + 1, variables):
            point = [0] * variables
            point[left] = point[right] = 1
            value = evaluate(tuple(point))
            for equation in range(equations):
                cross = (
                    value[equation]
                    - plus_values[left][equation]
                    - plus_values[right][equation]
                    + constant[equation]
                ) % 3
                polar[equation][left][right] = cross
                polar[equation][right][left] = cross

    # Reconstruct the diagonal coefficients from the polar matrix during
    # evaluation, so only the canonical (constant,linear,polar) data leaves
    # this function.
    for equation in range(equations):
        for variable in range(variables):
            if polar[equation][variable][variable] != (
                2 * diagonals[equation][variable] % 3
            ):
                raise AssertionError("polar diagonal changed")
    return (
        tuple(constant),
        tuple(tuple(row) for row in linears),
        tuple(
            tuple(tuple(row) for row in matrix) for matrix in polar
        ),
    )


def evaluate_interpolation(
    constant: Sequence[int],
    linears: Sequence[Sequence[int]],
    polar: Sequence[Sequence[Sequence[int]]],
    point: Sequence[int],
) -> tuple[int, ...]:
    result = []
    for equation in range(len(constant)):
        value = constant[equation]
        value += sum(
            linears[equation][index] * int(point[index])
            for index in range(len(point))
        )
        # q(y)=c+l.y + 1/2 y^T B y; inverse(2)=2 in F_3.
        quadratic = 0
        for left in range(len(point)):
            quadratic += (
                polar[equation][left][left]
                * int(point[left])
                * int(point[left])
            )
            for right in range(left + 1, len(point)):
                quadratic += (
                    2
                    * polar[equation][left][right]
                    * int(point[left])
                    * int(point[right])
                )
        value += 2 * quadratic
        result.append(value % 3)
    return tuple(result)


def flatten_symmetric(
    matrix: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    return tuple(
        int(matrix[left][right]) % 3
        for left in range(len(matrix))
        for right in range(left, len(matrix))
    )


def combine_rows(
    coefficients: Sequence[int],
    rows: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    return tuple(
        sum(
            int(coefficients[row]) * int(rows[row][column])
            for row in range(len(rows))
        )
        % 3
        for column in range(len(rows[0]))
    )


def audit_candidate(index: int) -> dict[str, object]:
    label, partition, target, identifiers_a, identifiers_b = CANDIDATES[index]
    profiles = profiles_from_ids(identifiers_a, identifiers_b)
    variable_count = len(active_trit_coordinates(profiles))
    equations = first_digit_equations(profiles)
    first_rank = matrix_rank(
        tuple(row[:-1] for row in augmented_system(equations))
    )
    if variable_count != 54 or first_rank != 18:
        raise AssertionError("first placement layer changed")
    origin, basis = affine_parameterization(equations, variable_count)
    term_data = second_digit_term_data(profiles)

    def evaluate(affine_coordinates: Sequence[int]) -> tuple[int, ...]:
        trits = lift_affine_point(origin, basis, affine_coordinates)
        if symbolic_first_digits(equations, trits) != (0,) * 20:
            raise AssertionError("affine point left the first-digit space")
        return symbolic_second_digits(term_data, trits)

    constant, linears, polar = interpolate_quadratics(
        evaluate, len(basis), len(equations)
    )
    if (constant, linears, polar) != derive_quadratics(
        term_data, origin, basis
    ):
        raise AssertionError("interpolated/direct quadratic forms disagree")

    # Validate interpolation and symbolic lambda expansion on a detached
    # deterministic corpus.
    validation_points = [
        tuple(
            (
                (fixture // (3 ** row)) % 3
                if row < 2
                else (
                    row * row
                    + 2 * index
                    + fixture * (row + 1)
                    + fixture * fixture
                ) % 3
            )
            for row in range(36)
        )
        for fixture in range(8)
    ]
    if len(set(validation_points)) != len(validation_points):
        raise AssertionError("the validation corpus contains duplicates")
    for point in validation_points:
        trits = lift_affine_point(origin, basis, point)
        symbolic = evaluate(point)
        if symbolic != evaluate_interpolation(
            constant, linears, polar, point
        ):
            raise AssertionError("quadratic interpolation failed")
        if symbolic != direct_second_digits(profiles, trits):
            raise AssertionError("symbolic/direct second digits disagree")

    polar_ranks = tuple(matrix_rank(matrix) for matrix in polar)
    stacked = tuple(row for matrix in polar for row in matrix)
    common_radical_rank = matrix_rank(stacked)
    common_radical_nullity = 36 - common_radical_rank

    flattened = tuple(flatten_symmetric(matrix) for matrix in polar)
    polar_span_rank = matrix_rank(flattened)
    transposed = tuple(
        tuple(flattened[row][column] for row in range(20))
        for column in range(len(flattened[0]))
    )
    zero_polar_combinations = nullspace_basis(transposed, columns=20)
    if len(zero_polar_combinations) != 20 - polar_span_rank:
        raise AssertionError("polar combination nullity changed")

    affine_combination_rows = []
    combination_records = []
    for coefficients in zero_polar_combinations:
        combined_linear = combine_rows(coefficients, linears)
        combined_constant = sum(
            coefficients[row] * constant[row] for row in range(20)
        ) % 3
        combined_polar = tuple(
            sum(
                coefficients[row] * polar[row][left][right]
                for row in range(20)
            )
            % 3
            for left in range(36)
            for right in range(36)
        )
        if any(combined_polar):
            raise AssertionError("declared zero-polar combination is nonzero")
        affine_combination_rows.append(
            combined_linear + ((-combined_constant) % 3,)
        )
        combination_records.append({
            "equation_coefficients": coefficients,
            "constant": combined_constant,
            "linear": combined_linear,
        })

    affine_coefficient_rank = matrix_rank(
        tuple(row[:-1] for row in affine_combination_rows)
    )
    affine_augmented_rank = matrix_rank(affine_combination_rows)
    affine_consistent = affine_coefficient_rank == affine_augmented_rank
    if not affine_consistent:
        reduced_nullity = None
    else:
        reduced_nullity = 36 - affine_coefficient_rank

    # A contradiction can also arise from a dependency among complete
    # nonconstant polynomial coefficient vectors, even if its polar part
    # was not considered separately.
    monomial_rows = []
    for equation in range(20):
        features = list(linears[equation])
        features.extend(flattened[equation])
        monomial_rows.append(
            tuple(features) + ((-constant[equation]) % 3,)
        )
    polynomial_coefficient_rank = matrix_rank(
        tuple(row[:-1] for row in monomial_rows)
    )
    polynomial_augmented_rank = matrix_rank(monomial_rows)
    if polynomial_augmented_rank != polynomial_coefficient_rank:
        raise AssertionError("second digit has a constant contradiction")

    return {
        "label": label,
        "partition": partition,
        "target": target,
        "profile_ids_a": identifiers_a,
        "profile_ids_b": identifiers_b,
        "first_digit": {
            "variables": variable_count,
            "rank": first_rank,
            "affine_dimension": len(basis),
            "origin_sha256": compact_hash(origin),
            "nullspace_basis_sha256": compact_hash(basis),
        },
        "second_digit": {
            "equations": len(equations),
            "equation_labels": tuple(
                f"{component}@{lag}"
                for component, lag in displayed_specifications()
            ),
            "derivation": (
                "For L=d+b.y, [lambda^2] omega^L=2L^2+L, "
                "polar=b*b^T, linear=(d+1)b over F_3."
            ),
            "polar_ranks": polar_ranks,
            "polar_rank_histogram": {
                str(rank): polar_ranks.count(rank)
                for rank in sorted(set(polar_ranks))
            },
            "polar_span_rank": polar_span_rank,
            "zero_polar_combination_dimension": len(
                zero_polar_combinations
            ),
            "common_radical_rank": common_radical_rank,
            "common_radical_nullity": common_radical_nullity,
            "zero_polar_affine_rank": affine_coefficient_rank,
            "zero_polar_affine_augmented_rank": affine_augmented_rank,
            "zero_polar_affine_consistent": affine_consistent,
            "linearly_reduced_dimension": reduced_nullity,
            "polynomial_coefficient_rank": polynomial_coefficient_rank,
            "polynomial_augmented_rank": polynomial_augmented_rank,
            "constant_sha256": compact_hash(constant),
            "linear_sha256": compact_hash(linears),
            "polar_sha256": compact_hash(polar),
            "zero_polar_combinations": tuple(combination_records),
            "validation_points": len(validation_points),
        },
    }


def build_certificate() -> dict[str, object]:
    audits = tuple(audit_candidate(index) for index in range(len(CANDIDATES)))
    return {
        "schema": "lp333-order3-phase-second-digit-v1",
        "scope": (
            "Second placement lambda digit on the five exact h=2 "
            "profile orbits; no labelled LP(333) or H(668) claim."
        ),
        "profiles": len(audits),
        "audits": audits,
    }


def main() -> None:
    certificate = build_certificate()
    semantic_sha256 = compact_hash(certificate)
    if EXPECTED_SEMANTIC_SHA256 and (
        semantic_sha256 != EXPECTED_SEMANTIC_SHA256
    ):
        raise AssertionError("second-digit semantic certificate changed")
    print(f"profiles={certificate['profiles']}")
    for audit in certificate["audits"]:
        second = audit["second_digit"]
        print(
            f"{audit['label']}: "
            f"polar_ranks={second['polar_ranks']} "
            f"span={second['polar_span_rank']} "
            f"common_radical_nullity={second['common_radical_nullity']} "
            f"zero_polar_dim={second['zero_polar_combination_dimension']} "
            f"linear_rank={second['zero_polar_affine_rank']} "
            f"reduced_dim={second['linearly_reduced_dimension']}"
        )
    print(f"semantic_sha256={semantic_sha256}")


if __name__ == "__main__":
    main()
