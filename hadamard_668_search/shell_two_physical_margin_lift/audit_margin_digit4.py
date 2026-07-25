#!/usr/bin/env python3
"""Audit the next (quadratic) lambda digit of every exact margin target.

After the six rank-one margin carries at lambda digit 3 are imposed, each
of the six exact phase-sum equalities has a quadratic digit-4 carry on a
parallel 30-dimensional affine chart.  This verifier interpolates those
quadrics, directly replays detached points, and exhausts their projective
five-form retractions.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
SECOND = SEARCH / "phase_second_digit"
sys.path[:0] = [str(HERE), str(SECOND), str(SEARCH)]

import audit_row_margin_retraction as base  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
import verify_phase_second_digit_pencil as pencil  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
)


EXPECTED_SEMANTIC_SHA256 = (
    "83fe2380c978de46e1f919fd34d7715a9f0ae4ad3bb4a95f187aeb7437effe9e"
)


def derive_target_quadrics(
    profiles,
    first_origin,
    first_basis,
    margin_rows,
    margin_kernel,
    base_sums,
    target,
):
    constants = base.target_constants(base_sums, target)
    target_origin = base.affine_solution(margin_rows, constants)

    def evaluate(point):
        y = tuple(
            (
                target_origin[row]
                + sum(
                    int(point[column]) * margin_kernel[column][row]
                    for column in range(30)
                )
            )
            % 3
            for row in range(36)
        )
        sums = base.phase_sums_for_affine_point(
            profiles, first_origin, first_basis, y
        )
        values = []
        for group in range(6):
            channel, residue = divmod(group, 3)
            difference = base.e_subtract(
                sums[channel][residue],
                target[channel][residue],
            )
            digits = second.lambda_digits(difference, 9)
            if any(digits[:4]):
                raise AssertionError(
                    "a point left the exact margin digit-3 chart"
                )
            values.append(digits[4])
        return tuple(values)

    quadrics = second.interpolate_quadratics(evaluate, 30, 6)
    validation = []
    for fixture in range(64):
        point = tuple(
            (
                fixture // (3 ** (index % 4))
                + fixture * (index + 1)
                + index * index
            )
            % 3
            for index in range(30)
        )
        actual = evaluate(point)
        predicted = second.evaluate_interpolation(*quadrics, point)
        if actual != predicted:
            raise AssertionError("a margin digit-4 quadric failed replay")
        validation.append((point, actual))
    return target_origin, quadrics, base.compact_hash(tuple(validation))


def audit_profile(index: int) -> dict[str, object]:
    candidate = second.CANDIDATES[index]
    label, _, _, identifiers_a, identifiers_b = candidate
    profiles = second.profiles_from_ids(identifiers_a, identifiers_b)
    first_equations = second.first_digit_equations(profiles)
    first_origin, first_basis = second.affine_parameterization(
        first_equations, 54
    )
    margin_rows, base_sums = base.derive_margin_digit_system(
        profiles, first_origin, first_basis
    )
    margin_kernel = second.nullspace_basis(margin_rows)
    catalog = catalog_phase_sum_intersection(identifiers_a, identifiers_b)
    targets = tuple(catalog["phase_sum_corpus"])
    if not targets:
        raise AssertionError("a shell-two profile lost all margin targets")
    _, first_quadrics, _ = derive_target_quadrics(
        profiles,
        first_origin,
        first_basis,
        margin_rows,
        margin_kernel,
        base_sums,
        targets[0][0],
    )
    common_polars = first_quadrics[2]
    common_polar_hash = base.compact_hash(common_polars)
    common_radical = second.nullspace_basis(
        tuple(row for polar in common_polars for row in polar),
        columns=30,
    )
    five_hyperplanes = base.hyperplane_retraction_data(common_polars)

    records = []
    rank_histogram: Counter[tuple[int, ...]] = Counter()
    common_radical_histogram: Counter[int] = Counter()
    full_retraction_histogram: Counter[int] = Counter()
    five_retraction_count_histogram: Counter[int] = Counter()
    five_normal_frequency: Counter[tuple[int, ...]] = Counter()
    for target_index, (target, multiplicity) in enumerate(
        targets
    ):
        target_origin, quadrics, validation_hash = derive_target_quadrics(
            profiles,
            first_origin,
            first_basis,
            margin_rows,
            margin_kernel,
            base_sums,
            target,
        )
        constants, linears, polars = quadrics
        polar_hash = base.compact_hash(polars)
        if polar_hash != common_polar_hash:
            raise AssertionError(
                "parallel margin targets changed the quadratic polars"
            )
        ranks = tuple(second.matrix_rank(polar) for polar in polars)
        rank_histogram[ranks] += 1
        common_radical_histogram[len(common_radical)] += 1
        full_rank = base.rank_on_radical(linears, common_radical)
        full_retraction_histogram[full_rank] += 1

        five_good = []
        for normal, coefficient_basis, radical in five_hyperplanes:
            combined_linears = tuple(
                pencil.combine_vectors(coefficients, linears)
                for coefficients in coefficient_basis
            )
            if base.rank_on_radical(
                combined_linears, radical
            ) == 5:
                five_good.append(normal)
                five_normal_frequency[normal] += 1
        five_retraction_count_histogram[len(five_good)] += 1
        records.append({
            "target_index": target_index,
            "raw_assignment_multiplicity": int(multiplicity),
            "target_origin_sha256": base.compact_hash(target_origin),
            "constants_sha256": base.compact_hash(constants),
            "linears_sha256": base.compact_hash(linears),
            "polars_sha256": polar_hash,
            "polar_ranks": ranks,
            "common_radical_dimension": len(common_radical),
            "full_six_linear_rank_on_radical": full_rank,
            "five_form_retraction_normals": tuple(five_good),
            "validation_sha256": validation_hash,
        })

    return {
        "candidate_index": index,
        "label": label,
        "target_count": len(records),
        "affine_dimension_before_margin_digit4": 30,
        "margin_digit4_equations": 6,
        "common_polar_sha256": common_polar_hash,
        "polar_rank_histogram": tuple(
            sorted(rank_histogram.items())
        ),
        "common_radical_dimension_histogram": tuple(
            sorted(common_radical_histogram.items())
        ),
        "full_six_linear_rank_on_radical_histogram": tuple(
            sorted(full_retraction_histogram.items())
        ),
        "five_form_retraction_count_histogram": tuple(
            sorted(five_retraction_count_histogram.items())
        ),
        "five_form_normal_frequency": tuple(
            sorted(five_normal_frequency.items())
        ),
        "targets": tuple(records),
    }


def verify() -> dict[str, object]:
    profiles = tuple(
        audit_profile(index) for index in range(len(second.CANDIDATES))
    )
    core = {
        "schema": "lp333-shell-two-margin-digit4-quadrics-v1",
        "scope": (
            "Exact quadratic margin-carry audit on all 405 physical "
            "target charts; no LP(333), Legendre pair, or H(668) claim."
        ),
        "profiles": profiles,
    }
    semantic_hash = base.compact_hash(core)
    if semantic_hash != EXPECTED_SEMANTIC_SHA256:
        raise AssertionError("the margin digit-4 audit changed")
    return {**core, "semantic_sha256": semantic_hash}


def main() -> None:
    result = verify()
    summary = {
        "schema": result["schema"],
        "profiles": tuple({
            "label": profile["label"],
            "target_count": profile["target_count"],
            "polar_rank_histogram": profile["polar_rank_histogram"],
            "common_radical_dimension_histogram": (
                profile["common_radical_dimension_histogram"]
            ),
            "full_six_linear_rank_on_radical_histogram": (
                profile["full_six_linear_rank_on_radical_histogram"]
            ),
            "five_form_retraction_count_histogram": (
                profile["five_form_retraction_count_histogram"]
            ),
            "five_form_normal_frequency": (
                profile["five_form_normal_frequency"]
            ),
        } for profile in result["profiles"]),
        "semantic_sha256": result["semantic_sha256"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
