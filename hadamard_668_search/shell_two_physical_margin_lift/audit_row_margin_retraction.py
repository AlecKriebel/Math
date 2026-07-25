#!/usr/bin/env python3
"""Exact row-margin and structured-retraction audit for the five h=2 charts.

This is an untracked research instrument.  It reconstructs every object from
the frozen repository certificates and proves three finite statements:

1. the first nonautomatic lambda digit of each exact phase-sum target is an
   affine rank-six system on the 36-dimensional first-correlation lift;
2. all 405 compatible catalog targets survive that system and leave parallel
   30-dimensional affine charts;
3. all projective five-hyperplanes in the six structured digit-two forms are
   tested both before and after the row-margin restriction.

It also checks the exact augmentation identity which makes the directed
origin coefficient two lambda digits later than the twelve nonzero
coefficients once the row margin is exact.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
SECOND = SEARCH / "phase_second_digit"
sys.path[:0] = [str(SECOND), str(SEARCH)]

import verify_phase_second_digit as second  # noqa: E402
import verify_phase_second_digit_pencil as pencil  # noqa: E402
from verify_lp333_order3_phase_hensel import canonical_solution  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
    channel_cross_term,
    phase_sums_from_masks,
)
from verify_lp333_order3_phase_factor import e_add  # noqa: E402


MODULUS = 3
EXPECTED_PROFILE_COUNT = 5
EXPECTED_TARGET_COUNTS = (72, 72, 72, 96, 93)
EXPECTED_TOTAL_TARGETS = 405
EXPECTED_SEMANTIC_SHA256 = (
    "7aed9978a72092c2146aff528734ac31afbc4c33fb1dd35c4bcd436015697c65"
)


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        separators=(",", ":"),
        sort_keys=True,
        ensure_ascii=True,
    )


def compact_hash(value: object) -> str:
    return sha256(canonical_json(value).encode("ascii")).hexdigest()


def e_subtract(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] - right[0], left[1] - right[1]


def dot(left: Sequence[int], right: Sequence[int]) -> int:
    return sum(int(a) * int(b) for a, b in zip(left, right)) % MODULUS


def projective_vectors(dimension: int) -> Iterable[tuple[int, ...]]:
    """Yield normalized representatives of P^(dimension-1)(F_3)."""

    for vector in product(range(MODULUS), repeat=dimension):
        if not any(vector):
            continue
        first = next(index for index, value in enumerate(vector) if value)
        if vector[first] == 1:
            yield vector


def affine_solution(
    coefficients: Sequence[Sequence[int]],
    constants: Sequence[int],
) -> tuple[int, ...]:
    """Solve A*x+constants=0 over F_3, asserting consistency."""

    if len(coefficients) != len(constants):
        raise ValueError("coefficient and constant row counts differ")
    columns = len(coefficients[0])
    rows = tuple(
        tuple(int(value) % MODULUS for value in row)
        + ((-int(constant)) % MODULUS,)
        for row, constant in zip(coefficients, constants)
    )
    solution = canonical_solution(rows, columns)
    if solution is None:
        raise AssertionError("a compatible row-margin digit became inconsistent")
    return solution


def restrict_polar(
    polar: Sequence[Sequence[int]],
    basis: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Pull back a symmetric polar matrix through a row-vector basis."""

    ambient = len(polar)
    return tuple(
        tuple(
            sum(
                int(basis[left][row])
                * int(polar[row][column])
                * int(basis[right][column])
                for row in range(ambient)
                for column in range(ambient)
            )
            % MODULUS
            for right in range(len(basis))
        )
        for left in range(len(basis))
    )


def shifted_restricted_linear(
    linear: Sequence[int],
    polar: Sequence[Sequence[int]],
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    """Pull back l+B*origin, the gradient after an affine translation."""

    gradient = tuple(
        (
            int(linear[row])
            + sum(
                int(polar[row][column]) * int(origin[column])
                for column in range(len(origin))
            )
        )
        % MODULUS
        for row in range(len(origin))
    )
    return tuple(dot(vector, gradient) for vector in basis)


def rank_on_radical(
    linears: Sequence[Sequence[int]],
    radical: Sequence[Sequence[int]],
) -> int:
    if not radical:
        return 0
    return second.matrix_rank(
        tuple(
            tuple(dot(linear, vector) for vector in radical)
            for linear in linears
        )
    )


def phase_sums_for_affine_point(
    profiles,
    first_origin: Sequence[int],
    first_basis: Sequence[Sequence[int]],
    affine: Sequence[int],
):
    placement = second.lift_affine_point(first_origin, first_basis, affine)
    masks = second.masks_from_trits(profiles, placement)
    return phase_sums_from_masks(*masks)


def derive_margin_digit_system(
    profiles,
    first_origin: Sequence[int],
    first_basis: Sequence[Sequence[int]],
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, int], ...],
]:
    """Interpolate the six first varying phase-sum digits on F_3^36."""

    zero = (0,) * len(first_basis)
    base_sums = phase_sums_for_affine_point(
        profiles, first_origin, first_basis, zero
    )
    rows: list[tuple[int, ...]] = []
    for group in range(6):
        channel, residue = divmod(group, 3)
        base_digit = second.lambda_digits(
            base_sums[channel][residue], 8
        )[3]
        coefficients = []
        for variable in range(len(first_basis)):
            point = [0] * len(first_basis)
            point[variable] = 1
            sums = phase_sums_for_affine_point(
                profiles, first_origin, first_basis, point
            )
            digit = second.lambda_digits(sums[channel][residue], 8)[3]
            coefficients.append((digit - base_digit) % MODULUS)
        rows.append(tuple(coefficients))

    # Detached deterministic interpolation checks.  The mathematical reason
    # for affinity is 3=-omega^2*lambda^2 and
    # omega^u=1-u*lambda (mod lambda^2), while the fixed signed augmentation
    # makes digits zero through two automatic.
    fixtures = []
    for fixture in range(96):
        point = tuple(
            (
                fixture // (3 ** (index % 5))
                + index * index
                + (fixture // 3) * (index + 2)
            )
            % MODULUS
            for index in range(len(first_basis))
        )
        fixtures.append(point)
    if len(set(fixtures)) < 24:
        raise AssertionError("the margin interpolation fixtures collapsed")
    for point in fixtures:
        sums = phase_sums_for_affine_point(
            profiles, first_origin, first_basis, point
        )
        for group, row in enumerate(rows):
            channel, residue = divmod(group, 3)
            actual = second.lambda_digits(
                sums[channel][residue], 8
            )[3]
            base = second.lambda_digits(
                base_sums[channel][residue], 8
            )[3]
            predicted = (base + dot(row, point)) % MODULUS
            if actual != predicted:
                raise AssertionError("a phase-sum digit is not affine")

    return tuple(rows), tuple(
        base_sums[channel][residue]
        for channel in range(2)
        for residue in range(3)
    )


def target_constants(
    base_sums: Sequence[tuple[int, int]],
    target,
) -> tuple[int, ...]:
    return tuple(
        second.lambda_digits(
            e_subtract(
                base_sums[group],
                target[group // 3][group % 3],
            ),
            8,
        )[3]
        for group in range(6)
    )


def augmentation_identity_audit(
    profiles,
    first_origin: Sequence[int],
    first_basis: Sequence[Sequence[int]],
    targets,
) -> dict[str, object]:
    """Check E1(0)+3 sum_(nonzero classes) E1(C)=augmentation."""

    checks = 0
    fixtures = [(0,) * len(first_basis)]
    fixtures.extend(
        tuple(
            (
                fixture
                + index * index
                + 2 * fixture * index
                + fixture // 2
            )
            % MODULUS
            for index in range(len(first_basis))
        )
        for fixture in range(1, 65)
    )
    for point in fixtures:
        placement = second.lift_affine_point(
            first_origin, first_basis, point
        )
        masks = second.masks_from_trits(profiles, placement)
        sums = phase_sums_from_masks(*masks)
        displayed = second.displayed_values(profiles, placement)
        coefficient_sum = displayed[7]
        for value in displayed[8:20]:
            coefficient_sum = e_add(
                coefficient_sum, (3 * value[0], 3 * value[1])
            )
        augmentation = e_add(
            channel_cross_term(sums[0]),
            channel_cross_term(sums[1]),
        )
        if coefficient_sum != augmentation:
            raise AssertionError("the exact E1 augmentation identity failed")
        checks += 1

    # Every compatible catalog target satisfies the exact augmentation gate.
    for target, _ in targets:
        augmentation = e_add(
            channel_cross_term(target[0]),
            channel_cross_term(target[1]),
        )
        if augmentation != (0, 0):
            raise AssertionError("a compatible target failed augmentation")

    return {
        "exact_identity_checks": checks,
        "compatible_target_augmentation_checks": len(targets),
        "origin_lag_advance_digits": 2,
    }


def hyperplane_retraction_data(
    structured_polars: Sequence[Sequence[Sequence[int]]],
) -> tuple[
    tuple[
        tuple[int, ...],
        tuple[tuple[int, ...], ...],
        tuple[tuple[int, ...], ...],
    ],
    ...,
]:
    """Precompute all 364 five-subspaces and their common radicals."""

    result = []
    for normal in projective_vectors(6):
        coefficient_basis = second.nullspace_basis((normal,))
        if len(coefficient_basis) != 5:
            raise AssertionError("a projective hyperplane lost dimension")
        combined_polars = tuple(
            pencil.combine_matrices(coefficients, structured_polars)
            for coefficients in coefficient_basis
        )
        radical = second.nullspace_basis(
            tuple(row for polar in combined_polars for row in polar),
            columns=len(structured_polars[0]),
        )
        result.append((normal, coefficient_basis, radical))
    if len(result) != 364:
        raise AssertionError("P^5(F_3) must have 364 points")
    return tuple(result)


def audit_profile(index: int) -> dict[str, object]:
    label, partition, aggregate, identifiers_a, identifiers_b = (
        second.CANDIDATES[index]
    )
    profiles = second.profiles_from_ids(identifiers_a, identifiers_b)
    first_equations = second.first_digit_equations(profiles)
    first_origin, first_basis = second.affine_parameterization(
        first_equations, 54
    )
    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles),
        first_origin,
        first_basis,
    )
    structured = pencil.structured_forms(constants, linears, polars)
    structured_linears = tuple(form[1] for form in structured)
    structured_polars = tuple(form[2] for form in structured)

    catalog = catalog_phase_sum_intersection(identifiers_a, identifiers_b)
    targets = tuple(catalog["phase_sum_corpus"])
    margin_rows, base_sums = derive_margin_digit_system(
        profiles, first_origin, first_basis
    )
    margin_rank = second.matrix_rank(margin_rows)
    if margin_rank != 6:
        raise AssertionError("the six margin digits lost rank")
    margin_kernel = second.nullspace_basis(margin_rows)
    if len(margin_kernel) != 30:
        raise AssertionError("the row-margin chart must have dimension 30")

    # The unrestricted five-form audit.
    unrestricted_hyperplanes = hyperplane_retraction_data(
        structured_polars
    )
    unrestricted_good = []
    unrestricted_histogram: Counter[tuple[int, int]] = Counter()
    for normal, coefficient_basis, radical in unrestricted_hyperplanes:
        combined_linears = tuple(
            pencil.combine_vectors(coefficients, structured_linears)
            for coefficients in coefficient_basis
        )
        restricted_rank = rank_on_radical(combined_linears, radical)
        unrestricted_histogram[(len(radical), restricted_rank)] += 1
        if restricted_rank == 5:
            unrestricted_good.append((normal, len(radical)))

    row_structured_polars = tuple(
        restrict_polar(polar, margin_kernel)
        for polar in structured_polars
    )
    row_hyperplanes = hyperplane_retraction_data(row_structured_polars)

    target_records = []
    five_hyperplane_frequency: Counter[tuple[int, ...]] = Counter()
    five_count_histogram: Counter[int] = Counter()
    coordinate_four_count_histogram: Counter[int] = Counter()
    for target_index, (target, multiplicity) in enumerate(targets):
        margin_constants = target_constants(base_sums, target)
        target_origin = affine_solution(margin_rows, margin_constants)

        # Directly replay all six digit-three margin equations.
        target_sums = phase_sums_for_affine_point(
            profiles, first_origin, first_basis, target_origin
        )
        for group in range(6):
            channel, residue = divmod(group, 3)
            difference = e_subtract(
                target_sums[channel][residue],
                target[channel][residue],
            )
            digits = second.lambda_digits(difference, 8)
            if any(digits[:4]):
                raise AssertionError(
                    "the 30-dimensional target origin failed margin digit 3"
                )

        row_linears = tuple(
            shifted_restricted_linear(
                linear, polar, target_origin, margin_kernel
            )
            for linear, polar in zip(structured_linears, structured_polars)
        )

        good_hyperplanes = []
        for normal, coefficient_basis, radical in row_hyperplanes:
            combined_linears = tuple(
                pencil.combine_vectors(coefficients, row_linears)
                for coefficients in coefficient_basis
            )
            if rank_on_radical(combined_linears, radical) == 5:
                good_hyperplanes.append(normal)
                five_hyperplane_frequency[normal] += 1
        five_count_histogram[len(good_hyperplanes)] += 1

        coordinate_four = 0
        for subset in combinations(range(6), 4):
            radical = second.nullspace_basis(
                tuple(
                    row
                    for form in subset
                    for row in row_structured_polars[form]
                ),
                columns=30,
            )
            if rank_on_radical(
                tuple(row_linears[form] for form in subset), radical
            ) == 4:
                coordinate_four += 1
        coordinate_four_count_histogram[coordinate_four] += 1

        target_records.append({
            "target_index": target_index,
            "target": target,
            "raw_assignment_multiplicity": int(multiplicity),
            "margin_digit_rank": margin_rank,
            "affine_dimension_after_margin_digit": len(margin_kernel),
            "target_origin_sha256": compact_hash(target_origin),
            "five_form_retraction_hyperplanes": tuple(good_hyperplanes),
            "coordinate_four_retraction_count": coordinate_four,
        })

    augmentation = augmentation_identity_audit(
        profiles, first_origin, first_basis, targets
    )
    return {
        "candidate_index": index,
        "label": label,
        "partition": partition,
        "aggregate": aggregate,
        "profile_ids_a": identifiers_a,
        "profile_ids_b": identifiers_b,
        "first_correlation_affine_dimension": len(first_basis),
        "compatible_catalog_targets": len(targets),
        "margin_first_varying_lambda_digit": 3,
        "margin_digit_rank": margin_rank,
        "affine_dimension_after_margin_digit": len(margin_kernel),
        "margin_coefficient_sha256": compact_hash(margin_rows),
        "margin_kernel_sha256": compact_hash(margin_kernel),
        "unrestricted_five_form_retractions": tuple(unrestricted_good),
        "unrestricted_hyperplane_radical_rank_histogram": tuple(
            sorted(
                (radical, rank, count)
                for (radical, rank), count
                in unrestricted_histogram.items()
            )
        ),
        "row_restricted_five_count_histogram": tuple(
            sorted(five_count_histogram.items())
        ),
        "row_restricted_five_hyperplane_frequency": tuple(
            sorted(five_hyperplane_frequency.items())
        ),
        "row_restricted_coordinate_four_count_histogram": tuple(
            sorted(coordinate_four_count_histogram.items())
        ),
        "row_restricted_polar_sha256": compact_hash(row_structured_polars),
        "augmentation": augmentation,
        "targets": tuple(target_records),
    }


def verify() -> dict[str, object]:
    profiles = tuple(
        audit_profile(index) for index in range(len(second.CANDIDATES))
    )
    if len(profiles) != EXPECTED_PROFILE_COUNT:
        raise AssertionError("the shell-two profile count changed")
    target_counts = tuple(
        int(profile["compatible_catalog_targets"]) for profile in profiles
    )
    if target_counts != EXPECTED_TARGET_COUNTS:
        raise AssertionError("the compatible target census changed")
    total_targets = sum(target_counts)
    if total_targets != EXPECTED_TOTAL_TARGETS:
        raise AssertionError("the compatible target total changed")

    core = {
        "schema": "lp333-shell-two-row-margin-retraction-audit-v1",
        "scope": (
            "Exact row-margin digit and structured-retraction audit on the "
            "five classified h=2 profile charts; no LP(333), Legendre pair, "
            "or H(668) claim."
        ),
        "profile_count": len(profiles),
        "compatible_target_counts": target_counts,
        "compatible_target_total": total_targets,
        "profiles": profiles,
    }
    semantic_hash = compact_hash(core)
    if semantic_hash != EXPECTED_SEMANTIC_SHA256:
        raise AssertionError("the row-margin/retraction audit changed")
    return {**core, "semantic_sha256": semantic_hash}


def main() -> None:
    result = verify()
    summary = {
        "schema": result["schema"],
        "profile_count": result["profile_count"],
        "compatible_target_counts": result["compatible_target_counts"],
        "compatible_target_total": result["compatible_target_total"],
        "profiles": tuple({
            "label": profile["label"],
            "margin_digit_rank": profile["margin_digit_rank"],
            "affine_dimension_after_margin_digit": (
                profile["affine_dimension_after_margin_digit"]
            ),
            "unrestricted_five_form_retractions": (
                profile["unrestricted_five_form_retractions"]
            ),
            "row_restricted_five_count_histogram": (
                profile["row_restricted_five_count_histogram"]
            ),
            "row_restricted_five_hyperplane_frequency": (
                profile["row_restricted_five_hyperplane_frequency"]
            ),
            "row_restricted_coordinate_four_count_histogram": (
                profile["row_restricted_coordinate_four_count_histogram"]
            ),
            "augmentation": profile["augmentation"],
        } for profile in result["profiles"]),
        "semantic_sha256": result["semantic_sha256"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
