#!/usr/bin/env python3
"""Audit the low-rank six-form pencil in the second placement digit.

For each exact h=2 profile orbit, the twenty displayed lambda-square
equations contain eighteen nonzero quadratic forms on the 36-dimensional
first-digit affine space.  The six combinations

    T_b = E0(b) + E1(b) + E1(27 b),  b in {1,2,4,8,16,32},

have unexpectedly small polar rank.  This verifier proves that they are
exactly the projective support-at-most-three combinations of polar rank
below 28, and uses exact quadratic Gauss sums over F_3 to count every fiber
of the joint map T:F_3^36 -> F_3^6.  It never enumerates the 3^36 domain.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from typing import Sequence

from verify_phase_second_digit import (
    CANDIDATES,
    MODULUS,
    affine_parameterization,
    canonical_solution,
    derive_quadratics,
    displayed_specifications,
    first_digit_equations,
    flatten_symmetric,
    matrix_rank,
    profiles_from_ids,
    second_digit_term_data,
)
from verify_lp333_order3_phase_hensel import (
    multiply_phase_entries,
    phase_entries,
)


EXPECTED_SEMANTIC_SHA256 = (
    "91cf19a2a9099d86908230df4d179cca877f1990be2a0c19a379235fcaa25615"
)
EXPECTED_CERTIFICATE_FILENAME = "phase_second_digit_pencil_certificate.json"

Eisenstein = tuple[int, int]
ROOTS: tuple[Eisenstein, ...] = ((1, 0), (0, 1), (-1, -1))
# Sum_x omega^(d*x^2/2), with 1/2=2 in F_3.
ONE_DIMENSIONAL_GAUSS: dict[int, Eisenstein] = {
    1: (-1, -2),
    2: (1, 2),
}


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def e_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] + right[0], left[1] + right[1]


def e_scale(scale: int, value: Eisenstein) -> Eisenstein:
    return scale * value[0], scale * value[1]


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def combine_vectors(
    coefficients: Sequence[int],
    rows: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    return tuple(
        sum(
            int(coefficients[row]) * int(rows[row][column])
            for row in range(len(rows))
        )
        % MODULUS
        for column in range(len(rows[0]))
    )


def combine_matrices(
    coefficients: Sequence[int],
    matrices: Sequence[Sequence[Sequence[int]]],
) -> tuple[tuple[int, ...], ...]:
    size = len(matrices[0])
    return tuple(
        tuple(
            sum(
                int(coefficients[index])
                * int(matrices[index][row][column])
                for index in range(len(matrices))
            )
            % MODULUS
            for column in range(size)
        )
        for row in range(size)
    )


def quadratic_value(
    constant: int,
    linear: Sequence[int],
    polar: Sequence[Sequence[int]],
    point: Sequence[int],
) -> int:
    """Evaluate c+l.y+(1/2)y^T B y over F_3."""

    value = int(constant)
    value += sum(
        int(left) * int(right) for left, right in zip(linear, point)
    )
    bilinear = sum(
        int(point[row])
        * int(polar[row][column])
        * int(point[column])
        for row in range(len(point))
        for column in range(len(point))
    )
    value += 2 * bilinear
    return value % MODULUS


def symmetric_diagonal(
    matrix: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    """Diagonalize a symmetric matrix by congruence over F_3."""

    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("a polar matrix must be square")
    work = [
        [int(value) % MODULUS for value in row]
        for row in matrix
    ]
    if any(
        work[row][column] != work[column][row]
        for row in range(size)
        for column in range(size)
    ):
        raise ValueError("a polar matrix must be symmetric")

    pivot_count = 0
    while pivot_count < size:
        diagonal_pivot = next(
            (
                row
                for row in range(pivot_count, size)
                if work[row][row]
            ),
            None,
        )
        if diagonal_pivot is None:
            off_diagonal = next(
                (
                    (row, column)
                    for row in range(pivot_count, size)
                    for column in range(row + 1, size)
                    if work[row][column]
                ),
                None,
            )
            if off_diagonal is None:
                break
            row, column = off_diagonal
            # Replace basis vector e_row by e_row+e_column.
            for source in range(size):
                work[source][row] = (
                    work[source][row] + work[source][column]
                ) % MODULUS
            for target in range(size):
                work[row][target] = (
                    work[row][target] + work[column][target]
                ) % MODULUS
            if not work[row][row]:
                raise AssertionError("off-diagonal pivot stayed isotropic")
            diagonal_pivot = row

        if diagonal_pivot != pivot_count:
            work[pivot_count], work[diagonal_pivot] = (
                work[diagonal_pivot],
                work[pivot_count],
            )
            for row in work:
                row[pivot_count], row[diagonal_pivot] = (
                    row[diagonal_pivot],
                    row[pivot_count],
                )

        pivot = work[pivot_count][pivot_count]
        inverse = pow(pivot, -1, MODULUS)
        for row in range(pivot_count + 1, size):
            entry = work[row][pivot_count]
            if not entry:
                continue
            factor = entry * inverse % MODULUS
            # Replace e_row by e_row-factor*e_pivot_count.
            for source in range(size):
                work[source][row] = (
                    work[source][row]
                    - factor * work[source][pivot_count]
                ) % MODULUS
            for target in range(size):
                work[row][target] = (
                    work[row][target]
                    - factor * work[pivot_count][target]
                ) % MODULUS
            if (
                work[row][pivot_count]
                or work[pivot_count][row]
            ):
                raise AssertionError("symmetric elimination failed")
        pivot_count += 1

    if any(
        work[row][column]
        for row in range(size)
        for column in range(size)
        if row != column
    ):
        raise AssertionError("congruence diagonalization left a cross term")
    diagonal = tuple(
        work[index][index] for index in range(pivot_count)
    )
    if any(value not in (1, 2) for value in diagonal):
        raise AssertionError("a nonzero diagonal entry left F_3^*")
    if len(diagonal) != matrix_rank(matrix):
        raise AssertionError("congruence and row ranks disagree")
    return diagonal


def quadratic_character_sum(
    constant: int,
    linear: Sequence[int],
    polar: Sequence[Sequence[int]],
) -> tuple[Eisenstein, int, bool]:
    """Return sum_y omega^q(y), polar rank, and completion consistency."""

    variables = len(linear)
    rank = matrix_rank(polar)
    augmented = tuple(
        tuple(polar[row])
        + ((-int(linear[row])) % MODULUS,)
        for row in range(variables)
    )
    if matrix_rank(augmented) != rank:
        return (0, 0), rank, False
    translation = canonical_solution(augmented, variables)
    if translation is None:
        raise AssertionError("a consistent completion had no solution")
    shifted_constant = quadratic_value(
        constant, linear, polar, translation
    )
    value = ROOTS[shifted_constant]
    diagonal = symmetric_diagonal(polar)
    for entry in diagonal:
        value = e_multiply(value, ONE_DIMENSIONAL_GAUSS[entry])
    value = e_scale(MODULUS ** (variables - rank), value)
    return value, rank, True


def structured_forms(
    constants: Sequence[int],
    linears: Sequence[Sequence[int]],
    polars: Sequence[Sequence[Sequence[int]]],
) -> tuple[
    tuple[int, tuple[int, ...], tuple[tuple[int, ...], ...]], ...
]:
    """Return T_b=E0(b)+E1(b)+E1(27b) for the six lag classes."""

    result = []
    specifications = displayed_specifications()
    for class_index in range(6):
        indices = (
            1 + class_index,
            8 + class_index,
            14 + class_index,
        )
        lag = specifications[indices[0]][1]
        if (
            specifications[indices[1]] != ("E1", lag)
            or specifications[indices[2]]
            != ("E1", 27 * lag % 37)
        ):
            raise AssertionError("the opposite-class lag pairing changed")
        result.append(
            (
                sum(constants[index] for index in indices) % MODULUS,
                combine_vectors(
                    (1, 1, 1),
                    tuple(linears[index] for index in indices),
                ),
                combine_matrices(
                    (1, 1, 1),
                    tuple(polars[index] for index in indices),
                ),
            )
        )
    return tuple(result)


def collapsed_autocorrelation_polar(
    entries: Sequence[Sequence[Sequence[object | None]]],
    lag: int,
    basis: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Return the polar form of sum_{s,t} K_st(lag) directly.

    This is the Hessian of the autocorrelation of the collapsed phase
    sequence V_X(c)=sum_s U_{X,s}(c).  It is constructed from all nine
    residue-pair correlations, independently of the displayed E0/E1 rows.
    """

    variables = len(basis)
    polar = [[0] * variables for _ in range(variables)]
    for channel in range(2):
        columns = len(entries[channel])
        for column in range(columns):
            for left_residue in range(3):
                for right_residue in range(3):
                    left = entries[channel][
                        (column + lag) % columns
                    ][left_residue]
                    right = entries[channel][column][right_residue]
                    if left is None or right is None:
                        continue
                    term = multiply_phase_entries(left, right, 0)
                    slope = tuple(
                        sum(
                            coefficient
                            * int(basis[coordinate][variable])
                            for variable, coefficient
                            in term.coefficients
                        )
                        % MODULUS
                        for coordinate in range(variables)
                    )
                    sign = term.sign % MODULUS
                    for row in range(variables):
                        for target in range(variables):
                            polar[row][target] += (
                                sign * slope[row] * slope[target]
                            )
    return tuple(
        tuple(value % MODULUS for value in row) for row in polar
    )


def sparse_projective_audit(
    polars: Sequence[Sequence[Sequence[int]]],
) -> dict[str, object]:
    """Exhaust every projective combination supported on at most 3 rows."""

    active = tuple(
        index
        for index, matrix in enumerate(polars)
        if any(value for row in matrix for value in row)
    )
    if active != tuple(range(1, 7)) + tuple(range(8, 20)):
        raise AssertionError("the two structural zero equations changed")

    histograms: dict[str, dict[str, int]] = {}
    minima: dict[str, int] = {}
    low_records = []
    structured_index_sets = {
        (1 + class_index, 8 + class_index, 14 + class_index)
        for class_index in range(6)
    }
    for support in (1, 2, 3):
        histogram: Counter[int] = Counter()
        minimum = 37
        for indices in combinations(active, support):
            for tail in product((1, 2), repeat=support - 1):
                coefficients = (1,) + tail
                matrix = combine_matrices(
                    coefficients,
                    tuple(polars[index] for index in indices),
                )
                rank = matrix_rank(matrix)
                histogram[rank] += 1
                minimum = min(minimum, rank)
                if rank < 28:
                    low_records.append(
                        (indices, coefficients, rank)
                    )
        histograms[str(support)] = {
            str(rank): histogram[rank] for rank in sorted(histogram)
        }
        minima[str(support)] = minimum

    if len(low_records) != 6:
        raise AssertionError("the sparse low-rank family changed size")
    if {
        indices for indices, _, _ in low_records
    } != structured_index_sets:
        raise AssertionError("a nonstructured sparse low-rank form appeared")
    if any(
        coefficients != (1, 1, 1)
        for _, coefficients, _ in low_records
    ):
        raise AssertionError("a low-rank coefficient pattern changed")
    return {
        "active_equation_indices": active,
        "projective_combinations_tested": sum(
            sum(support_histogram.values())
            for support_histogram in histograms.values()
        ),
        "histograms_by_support": histograms,
        "minimum_rank_by_support": minima,
        "rank_below_28_count": len(low_records),
        "rank_below_28_records": tuple(low_records),
        "rank_below_28_exactly_structured_family": True,
    }


def gauss_fiber_audit(
    forms: Sequence[
        tuple[int, Sequence[int], Sequence[Sequence[int]]]
    ],
) -> dict[str, object]:
    """Count all 729 fibers of the six-form map by exact Fourier inversion."""

    coefficients = tuple(product(range(MODULUS), repeat=6))
    fourier: dict[tuple[int, ...], Eisenstein] = {}
    rank_consistency: Counter[tuple[int, bool]] = Counter()
    for coefficient in coefficients:
        constant = sum(
            coefficient[index] * int(forms[index][0])
            for index in range(6)
        ) % MODULUS
        linear = combine_vectors(
            coefficient,
            tuple(form[1] for form in forms),
        )
        polar = combine_matrices(
            coefficient,
            tuple(form[2] for form in forms),
        )
        character_sum, rank, consistent = quadratic_character_sum(
            constant, linear, polar
        )
        fourier[coefficient] = character_sum
        rank_consistency[(rank, consistent)] += 1

    fiber_counts = []
    for target in coefficients:
        total: Eisenstein = (0, 0)
        for coefficient, character_sum in fourier.items():
            exponent = -sum(
                left * right
                for left, right in zip(coefficient, target)
            ) % MODULUS
            total = e_add(
                total,
                e_multiply(ROOTS[exponent], character_sum),
            )
        if total[1] or total[0] % (MODULUS ** 6):
            raise AssertionError("Fourier inversion was not rational integral")
        fiber_counts.append(total[0] // (MODULUS ** 6))

    if sum(fiber_counts) != MODULUS ** 36:
        raise AssertionError("the six-form fibers do not partition F_3^36")
    if min(fiber_counts) <= 0:
        raise AssertionError("the six-form map stopped being surjective")
    uniform_baseline = MODULUS ** 30
    fiber_count_quantum = MODULUS ** 13
    corrections = tuple(
        (count - uniform_baseline) // fiber_count_quantum
        for count in fiber_counts
    )
    if any(
        count != uniform_baseline + fiber_count_quantum * correction
        for count, correction in zip(fiber_counts, corrections)
    ):
        raise AssertionError("a fiber count left its 3^13 congruence class")
    return {
        "pencil_coefficient_vectors": len(coefficients),
        "zero_character_sums": sum(
            value == (0, 0) for value in fourier.values()
        ),
        "rank_completion_histogram": {
            f"{rank}:{'consistent' if consistent else 'inconsistent'}":
                rank_consistency[(rank, consistent)]
            for rank, consistent in sorted(rank_consistency)
        },
        "joint_zero_fiber_count": fiber_counts[0],
        "uniform_baseline": uniform_baseline,
        "fiber_count_quantum": fiber_count_quantum,
        "joint_zero_fiber_delta": fiber_counts[0] - uniform_baseline,
        "joint_zero_fiber_correction": corrections[0],
        "all_target_fibers_nonempty": True,
        "minimum_fiber_count": min(fiber_counts),
        "maximum_fiber_count": max(fiber_counts),
        "minimum_fiber_correction": min(corrections),
        "maximum_fiber_correction": max(corrections),
        "distinct_fiber_counts": len(set(fiber_counts)),
        "fiber_counts_sha256": compact_hash(tuple(fiber_counts)),
        "fiber_corrections_sha256": compact_hash(corrections),
        "fiber_count_sum": sum(fiber_counts),
    }


def audit_candidate(index: int) -> dict[str, object]:
    label, partition, target, identifiers_a, identifiers_b = CANDIDATES[index]
    profiles = profiles_from_ids(identifiers_a, identifiers_b)
    equations = first_digit_equations(profiles)
    origin, basis = affine_parameterization(equations, 54)
    constants, linears, polars = derive_quadratics(
        second_digit_term_data(profiles), origin, basis
    )
    forms = structured_forms(constants, linears, polars)
    entries = phase_entries(profiles)

    structured_records = []
    for class_index, (constant, linear, polar) in enumerate(forms):
        rank = matrix_rank(polar)
        augmented_rank = matrix_rank(tuple(polar) + (tuple(linear),))
        if augmented_rank != rank + 1:
            raise AssertionError(
                "a structured form lost its radical-linear direction"
            )
        lag = displayed_specifications()[1 + class_index][1]
        collapsed = collapsed_autocorrelation_polar(entries, lag, basis)
        if collapsed != polar:
            raise AssertionError(
                "the structured polar form did not factor through "
                "collapsed phase autocorrelation"
            )
        structured_records.append({
            "lag": lag,
            "opposite_class_representative": 27 * lag % 37,
            "equation_indices": (
                1 + class_index,
                8 + class_index,
                14 + class_index,
            ),
            "constant": constant,
            "polar_rank": rank,
            "polar_nullity": 36 - rank,
            "polar_plus_linear_rank": augmented_rank,
            "linear_nonzero_on_polar_radical": True,
            "collapsed_phase_autocorrelation_factorization": True,
            "linear_sha256": compact_hash(linear),
            "polar_sha256": compact_hash(polar),
        })

    polar_span_rank = matrix_rank(
        tuple(
            flatten_symmetric(form[2]) for form in forms
        )
    )
    common_radical_rank = matrix_rank(
        tuple(row for form in forms for row in form[2])
    )
    if polar_span_rank != 6:
        raise AssertionError("the structured polar pencil lost dimension")

    return {
        "label": label,
        "partition": partition,
        "target": target,
        "profile_ids_a": identifiers_a,
        "profile_ids_b": identifiers_b,
        "structured_identity": (
            "T_b=E0(b)+E1(b)+E1(27b), "
            "b in (1,2,4,8,16,32), with 27b representing -C_b."
        ),
        "structured_forms": tuple(structured_records),
        "structured_polar_span_rank": polar_span_rank,
        "structured_common_radical_rank": common_radical_rank,
        "structured_common_radical_nullity": 36 - common_radical_rank,
        "sparse_projective_audit": sparse_projective_audit(polars),
        "gauss_fiber_audit": gauss_fiber_audit(forms),
    }


def verify_gauss_primitives() -> None:
    if quadratic_character_sum(0, (0,), ((1,),))[0] != (-1, -2):
        raise AssertionError("the first one-dimensional Gauss sum changed")
    if quadratic_character_sum(0, (0,), ((2,),))[0] != (1, 2):
        raise AssertionError("the second one-dimensional Gauss sum changed")
    if quadratic_character_sum(0, (1,), ((0,),))[0] != (0, 0):
        raise AssertionError("a radical-linear character sum did not vanish")


def build_certificate() -> dict[str, object]:
    verify_gauss_primitives()
    audits = tuple(audit_candidate(index) for index in range(len(CANDIDATES)))
    return {
        "schema": "lp333-order3-phase-second-digit-pencil-v1",
        "scope": (
            "Low-rank second-digit subsystem on five exact h=2 profile "
            "orbits; no labelled LP(333), Legendre pair, or H(668) claim."
        ),
        "method": (
            "Exhaustive 3,588-element sparse projective pencil audit per "
            "profile, followed by exact 729-character quadratic Gauss "
            "inversion; the 3^36 domains are never enumerated."
        ),
        "profiles": len(audits),
        "audits": audits,
    }


def main() -> None:
    certificate = build_certificate()
    semantic_sha256 = compact_hash(certificate)
    if (
        EXPECTED_SEMANTIC_SHA256
        and semantic_sha256 != EXPECTED_SEMANTIC_SHA256
    ):
        raise AssertionError("the pencil semantic certificate changed")
    print(f"profiles={certificate['profiles']}")
    for audit in certificate["audits"]:
        ranks = tuple(
            record["polar_rank"]
            for record in audit["structured_forms"]
        )
        gauss = audit["gauss_fiber_audit"]
        sparse = audit["sparse_projective_audit"]
        print(
            f"{audit['label']}: structured_ranks={ranks} "
            f"sparse_tested={sparse['projective_combinations_tested']} "
            f"zero_fiber={gauss['joint_zero_fiber_count']} "
            f"all_729_nonempty={gauss['all_target_fibers_nonempty']}"
        )
    print(f"semantic_sha256={semantic_sha256}")


if __name__ == "__main__":
    main()
