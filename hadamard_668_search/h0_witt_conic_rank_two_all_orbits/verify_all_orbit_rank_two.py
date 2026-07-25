#!/usr/bin/env python3
"""Dimension gate and exhaustive safe-orbit rank-two conic audit.

For each of the 18 exact dense-shell h=0 profiles, this verifier studies

    t_X(j,s) = P_X(x,s,p_X,j(s)) + h_j Q_X(x,s,p_X,j(s)),

with all four P_A,P_B,Q_A,Q_B arbitrary ternary polynomials of total
degree at most two.  Thus the two opposite-correction coefficient rows
are arbitrary and have rank at most two.

The 40 coefficient variables are solved through the first placement
layer and quotiented by their exact physical evaluation kernel.  Every
orbit with physical image dimension at most 16 is exhaustively enumerated.
Larger images are not enumerated: their exact denominators, batch counts,
and dense-quadratic work proxies are frozen instead.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
BASE = SEARCH / "h0_witt_conic_rank_two_orbit07"
RANK_ONE = SEARCH / "h0_witt_conic_rank_one"
SECOND = SEARCH / "phase_second_digit"
TRIAGE = SEARCH / "h0_new_orbits_lift_triage"
sys.path[:0] = [
    str(BASE),
    str(RANK_ONE),
    str(SECOND),
    str(TRIAGE),
    str(SEARCH),
]

import verify_witt_conic_rank_two as base  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    first_digit_equations,
    profiles_from_ids,
)
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    row_sum_catalog,
)


MODULUS = 3
DIMENSION_GATE = 16
BATCH_SIZE = 32_768
CLASSIFICATION = (
    SEARCH
    / "dense_shell_h0_complete_classification"
    / "certificate.json"
)
FINAL_SCAN = TRIAGE / "FINAL_PRODUCTION_SCAN_18.json"
PINNED_CERTIFICATE = HERE / "all_orbit_rank_two_certificate.json"


def compact_hash(value: object) -> str:
    return base.compact_hash(value)


def array_hash(value: np.ndarray) -> str:
    return base.array_hash(value)


def load_inputs() -> tuple[
    dict[str, object],
    tuple[dict[str, object], ...],
    dict[str, dict[str, object]],
]:
    classification = json.loads(CLASSIFICATION.read_text())
    if classification["schema"] != (
        "h668-dense-shell-h0-complete-classification-v1"
    ):
        raise AssertionError("classification schema changed")
    profiles = tuple(classification["profiles"])
    if (
        not classification["census"]["complete"]
        or len(profiles) != 18
        or tuple(record["label"] for record in profiles)
        != tuple(f"orbit-{index:02d}" for index in range(1, 19))
    ):
        raise AssertionError("complete classification changed")

    scan = json.loads(FINAL_SCAN.read_text())
    if scan["exact_orbits"] != 18:
        raise AssertionError("final 18-orbit scan changed")
    scanned = {record["digest"]: record for record in scan["orbits"]}
    if set(scanned) != {
        record["production_digest"] for record in profiles
    }:
        raise AssertionError("classification and lift scan disagree")
    return classification, profiles, scanned


def prepare_quotient(
    orbit: dict[str, object],
) -> tuple[
    Sequence[Sequence[Sequence[int]]],
    dict[str, object],
    dict[str, np.ndarray],
]:
    profiles = profiles_from_ids(
        orbit["profile_ids_a"], orbit["profile_ids_b"]
    )
    features, opposite_a, opposite_b = base.coefficient_family(profiles)
    equations = augmented_system(first_digit_equations(profiles))
    equation_matrix = np.asarray(
        [row[:-1] for row in equations], dtype=np.int16
    ) % MODULUS
    rhs = np.asarray(
        [row[-1] for row in equations], dtype=np.int16
    ) % MODULUS
    coefficient_system = equation_matrix @ features % MODULUS
    particular, coefficient_kernel, constraint_rank = (
        base.affine_coefficient_solution(coefficient_system, rhs)
    )
    feature_rank = base.rank(features)
    coefficient_dimension = len(coefficient_kernel)
    physical_offset = particular @ features.T % MODULUS
    physical_directions = coefficient_kernel @ features.T % MODULUS
    physical_basis = base.canonical_row_basis(physical_directions)
    physical_dimension = len(physical_basis)
    evaluation_kernel_dimension = (
        coefficient_dimension - physical_dimension
    )
    if (
        constraint_rank != 18
        or coefficient_dimension != 22
        or physical_dimension != feature_rank - constraint_rank
        or evaluation_kernel_dimension != 40 - feature_rank
    ):
        raise AssertionError(
            f"{orbit['label']}: quotient dimension identities failed"
        )
    if np.any(
        (equation_matrix @ physical_offset - rhs) % MODULUS
    ) or np.any(equation_matrix @ physical_basis.T % MODULUS):
        raise AssertionError(
            f"{orbit['label']}: physical quotient left first layer"
        )
    states = MODULUS**physical_dimension
    quotient = {
        "feature_evaluation_rank": feature_rank,
        "first_layer_constraint_rank": constraint_rank,
        "coefficient_solution_dimension": coefficient_dimension,
        "coefficient_solution_count": MODULUS**coefficient_dimension,
        "evaluation_kernel_dimension": evaluation_kernel_dimension,
        "coefficient_descriptions_per_physical_placement": (
            MODULUS**evaluation_kernel_dimension
        ),
        "physical_image_dimension": physical_dimension,
        "physical_image_denominator": states,
        "feature_matrix_sha256": array_hash(features),
        "physical_offset_sha256": array_hash(physical_offset),
        "physical_basis_sha256": array_hash(physical_basis),
    }
    arrays = {
        "features": features,
        "opposite_a": opposite_a,
        "opposite_b": opposite_b,
        "physical_offset": physical_offset,
        "physical_basis": physical_basis,
    }
    return profiles, quotient, arrays


def survivor_record(
    orbit: dict[str, object],
    profiles: Sequence[Sequence[Sequence[int]]],
    affine_origin: np.ndarray,
    affine_basis: np.ndarray,
    affine_point: np.ndarray,
    catalog: set[tuple[int, ...]],
) -> dict[str, object]:
    placement, active = base.direct_replay(
        profiles,
        affine_origin,
        affine_basis,
        affine_point,
        len(base.ACTIVE_ROWS),
    )
    if active != (0,) * len(base.ACTIVE_ROWS):
        raise AssertionError("stored digit-two survivor is not exact")
    values = base.second.displayed_values(profiles, placement)
    digits = tuple(
        base.second.lambda_digits(value, 12) for value in values
    )
    counts = tuple(
        sum(row[digit] != 0 for row in digits)
        for digit in range(12)
    )
    if counts[:3] != (0, 0, 0):
        raise AssertionError("survivor lost a certified zero digit")
    masks = base.second.masks_from_trits(profiles, placement)
    aggregate = base.labelled_aggregate(*masks)
    margin_member = aggregate in catalog
    record = {
        "affine_coordinates": tuple(map(int, affine_point)),
        "placement_trits": tuple(map(int, placement)),
        "displayed_exact_values": values,
        "nonzero_rows_by_digit": counts,
        "following_digit_defect": counts[3],
        "masks_a": masks[0],
        "masks_b": masks[1],
        "row_margin_aggregate": aggregate,
        "row_margin_catalog_member": margin_member,
        "assignment_sha256": compact_hash(
            {
                "affine": tuple(map(int, affine_point)),
                "placement": tuple(map(int, placement)),
                "masks": masks,
                "aggregate": aggregate,
            }
        ),
    }
    if counts[3] == 0:
        alert = {
            "profile_label": orbit["label"],
            "profile_digest": orbit["production_digest"],
            "assignment": record,
        }
        print(
            "CONSECUTIVE_WITNESS=" + json.dumps(alert, separators=(",", ":")),
            flush=True,
        )
    return record


def exhaustive_audit(
    orbit: dict[str, object],
    profiles: Sequence[Sequence[Sequence[int]]],
    quotient: dict[str, object],
    arrays: dict[str, np.ndarray],
    catalog: set[tuple[int, ...]],
) -> dict[str, object]:
    physical_dimension = int(quotient["physical_image_dimension"])
    if physical_dimension > DIMENSION_GATE:
        raise AssertionError("unsafe orbit reached exhaustive audit")
    (
        affine_origin_raw,
        affine_basis_raw,
        constants_raw,
        linears_raw,
        polars_raw,
    ) = base.rank_one.exact_quadratic_forms(profiles)
    affine_origin = base.normalize(np.asarray(affine_origin_raw))
    affine_basis = base.normalize(np.asarray(affine_basis_raw))
    constants = base.normalize(np.asarray(constants_raw))
    linears = base.normalize(np.asarray(linears_raw))
    polars = base.normalize(np.asarray(polars_raw))
    affine_offset, family_basis, selected = (
        base.map_to_affine_coordinates(
            arrays["physical_offset"],
            arrays["physical_basis"],
            affine_origin,
            affine_basis,
        )
    )
    (
        restricted_constants,
        restricted_linears,
        restricted_polars,
    ) = base.restrict_quadratics(
        affine_offset, family_basis, constants, linears, polars
    )

    total_points = int(quotient["physical_image_denominator"])
    histogram = np.zeros(len(constants) + 1, dtype=np.int64)
    first_point_by_score: dict[int, np.ndarray] = {}
    exact_points: list[np.ndarray] = []
    coordinate_hasher = sha256()
    score_hasher = sha256()
    for start in range(0, total_points, BATCH_SIZE):
        coordinates = base.ternary_batch(
            start,
            min(start + BATCH_SIZE, total_points),
            physical_dimension,
        )
        coordinate_hasher.update(
            np.asarray(coordinates, dtype=np.uint8).tobytes(order="C")
        )
        values = base.rank_one.evaluate_quadratics(
            coordinates,
            restricted_constants,
            restricted_linears,
            restricted_polars,
        )
        scores = np.sum(values == 0, axis=1).astype(np.uint8)
        score_hasher.update(scores.tobytes(order="C"))
        histogram += np.bincount(scores, minlength=len(histogram))
        for score in np.unique(scores):
            integer_score = int(score)
            if integer_score not in first_point_by_score:
                offset = int(np.flatnonzero(scores == score)[0])
                first_point_by_score[integer_score] = (
                    affine_offset + coordinates[offset] @ family_basis
                ) % MODULUS
        for offset in np.flatnonzero(scores == len(constants)):
            exact_points.append(
                (
                    affine_offset
                    + coordinates[int(offset)] @ family_basis
                )
                % MODULUS
            )
        if len(exact_points) > 100_000:
            raise AssertionError(
                f"{orbit['label']}: survivor replay resource cap exceeded"
            )
    if int(histogram.sum()) != total_points:
        raise AssertionError(f"{orbit['label']}: score census lost points")

    direct_replays = []
    for score, affine_point in sorted(first_point_by_score.items()):
        placement, active = base.direct_replay(
            profiles,
            affine_origin,
            affine_basis,
            affine_point,
            score,
        )
        derived = tuple(
            int(value)
            for value in base.rank_one.evaluate_quadratics(
                affine_point[None, :], constants, linears, polars
            )[0]
        )
        if active != derived:
            raise AssertionError(
                f"{orbit['label']}: direct second-digit replay failed"
            )
        direct_replays.append(
            {
                "score": score,
                "affine_point_sha256": compact_hash(
                    tuple(map(int, affine_point))
                ),
                "placement_sha256": compact_hash(
                    tuple(map(int, placement))
                ),
                "active_second_digit_values": active,
            }
        )

    survivors = [
        survivor_record(
            orbit,
            profiles,
            affine_origin,
            affine_basis,
            affine_point,
            catalog,
        )
        for affine_point in exact_points
    ]
    maximum_score = max(
        score for score, count in enumerate(histogram) if count
    )
    return {
        "status": "EXHAUSTIVE",
        "coverage_numerator": total_points,
        "coverage_denominator": total_points,
        "batch_size": BATCH_SIZE,
        "batches": (total_points + BATCH_SIZE - 1) // BATCH_SIZE,
        "affine_coordinate_columns": selected,
        "affine_offset_sha256": array_hash(affine_offset),
        "affine_family_basis_sha256": array_hash(family_basis),
        "restricted_constants_sha256": array_hash(restricted_constants),
        "restricted_linears_sha256": array_hash(restricted_linears),
        "restricted_polars_sha256": array_hash(restricted_polars),
        "coordinate_stream_sha256": coordinate_hasher.hexdigest(),
        "score_stream_sha256": score_hasher.hexdigest(),
        "score_histogram": {
            str(score): int(count)
            for score, count in enumerate(histogram)
            if count
        },
        "maximum_active_second_digit_equations": maximum_score,
        "active_second_digit_equations": len(constants),
        "exact_second_digit_survivors": len(survivors),
        "two_consecutive_digit_survivors": sum(
            survivor["following_digit_defect"] == 0
            for survivor in survivors
        ),
        "margin_compatible_second_digit_survivors": sum(
            survivor["row_margin_catalog_member"]
            for survivor in survivors
        ),
        "two_consecutive_and_margin_survivors": sum(
            survivor["following_digit_defect"] == 0
            and survivor["row_margin_catalog_member"]
            for survivor in survivors
        ),
        "survivors": survivors,
        "direct_score_replays": direct_replays,
    }


def deferred_audit(quotient: dict[str, object]) -> dict[str, object]:
    dimension = int(quotient["physical_image_dimension"])
    states = int(quotient["physical_image_denominator"])
    batches = (states + BATCH_SIZE - 1) // BATCH_SIZE
    reference_work = MODULUS**DIMENSION_GATE * 18 * DIMENSION_GATE**2
    work = states * 18 * dimension**2
    return {
        "status": "DEFERRED_DIMENSION_GATE",
        "coverage_numerator": 0,
        "coverage_denominator": states,
        "reason": (
            f"Physical image dimension {dimension} exceeds the frozen "
            f"complete-pilot gate {DIMENSION_GATE}; no point was enumerated."
        ),
        "exact_states": states,
        "batch_size_if_resumed": BATCH_SIZE,
        "exact_batches_if_resumed": batches,
        "dense_quadratic_term_proxy": work,
        "work_proxy_relative_to_one_dimension_16_orbit": {
            "numerator": work,
            "denominator": reference_work,
        },
        "fallback": (
            "Derive an additional exact quotient, character-sum zero-fiber "
            "certificate, or lossless meet-in-the-middle split before "
            "enumeration. No survivor or exclusion claim is made."
        ),
    }


def build_certificate() -> dict[str, object]:
    classification, orbits, scanned = load_inputs()
    catalog = set(row_sum_catalog())
    if len(catalog) != 1_756:
        raise AssertionError("row-margin catalog changed")

    records = []
    covered_states = 0
    total_states = 0
    covered_orbits = 0
    consecutive = 0
    margin_compatible = 0
    for orbit in orbits:
        profiles, quotient, arrays = prepare_quotient(orbit)
        dimension = int(quotient["physical_image_dimension"])
        states = int(quotient["physical_image_denominator"])
        print(
            f"{orbit['label']} dimension={dimension} states={states} "
            f"status={'ENUMERATE' if dimension <= DIMENSION_GATE else 'DEFER'}",
            flush=True,
        )
        if dimension <= DIMENSION_GATE:
            pilot = exhaustive_audit(
                orbit, profiles, quotient, arrays, catalog
            )
            covered_orbits += 1
            covered_states += states
            consecutive += int(
                pilot["two_consecutive_digit_survivors"]
            )
            margin_compatible += int(
                pilot["margin_compatible_second_digit_survivors"]
            )
            print(
                f"{orbit['label']} complete max="
                f"{pilot['maximum_active_second_digit_equations']}/18 "
                f"digit2={pilot['exact_second_digit_survivors']} "
                f"digit3={pilot['two_consecutive_digit_survivors']} "
                f"margin={pilot['margin_compatible_second_digit_survivors']}",
                flush=True,
            )
        else:
            pilot = deferred_audit(quotient)
        total_states += states
        scan_record = scanned[orbit["production_digest"]]
        records.append(
            {
                "profile": {
                    "label": orbit["label"],
                    "digest": orbit["production_digest"],
                    "ids_a": orbit["profile_ids_a"],
                    "ids_b": orbit["profile_ids_b"],
                    "target": orbit["target"],
                    "classification_record_sha256": orbit["record_sha256"],
                    "compatible_catalog_rows": scan_record[
                        "row_margin_transfer"
                    ]["compatible_catalog_rows"],
                    "accepted_raw_assignments": scan_record[
                        "row_margin_transfer"
                    ]["accepted_raw_assignments"],
                },
                "quotient": quotient,
                "pilot": pilot,
            }
        )

    expected_dimensions = {
        14: 1,
        16: 4,
        17: 6,
        18: 7,
    }
    actual_dimensions = {
        dimension: sum(
            record["quotient"]["physical_image_dimension"] == dimension
            for record in records
        )
        for dimension in expected_dimensions
    }
    if actual_dimensions != expected_dimensions:
        raise AssertionError("all-orbit dimension distribution changed")
    if (
        covered_orbits,
        covered_states,
        total_states,
    ) != (5, 176_969_853, 3_663_754_254):
        raise AssertionError("covered-family denominator changed")

    certificate: dict[str, object] = {
        "schema": "h668-h0-witt-conic-rank-two-all-orbits-v1",
        "scope": (
            "Exact quotient census for the arbitrary-quadratic antipodal "
            "rank-at-most-two center family on all 18 dense-shell h0 "
            "profiles, with exhaustive enumeration exactly through "
            "physical dimension 16. This is not an LP(333) or H(668) "
            "exclusion."
        ),
        "inputs": {
            "classification_path": str(CLASSIFICATION.relative_to(SEARCH)),
            "classification_sha256": sha256(
                CLASSIFICATION.read_bytes()
            ).hexdigest(),
            "classification_semantic_sha256": classification["census"][
                "semantic_sha256"
            ],
            "final_scan_path": str(FINAL_SCAN.relative_to(SEARCH)),
            "final_scan_sha256": sha256(FINAL_SCAN.read_bytes()).hexdigest(),
            "base_rank_two_verifier_path": str(
                Path(base.__file__).resolve().relative_to(SEARCH)
            ),
            "base_rank_two_verifier_sha256": sha256(
                Path(base.__file__).read_bytes()
            ).hexdigest(),
        },
        "family": {
            "center_law": (
                "t_X=P_X(x,s,p_X,j(s))+h_j*Q_X(x,s,p_X,j(s)); "
                "u_X=-p_X,j(s)*t_X"
            ),
            "quadratic_monomials_per_polynomial": 10,
            "coefficient_parameters_per_profile": 40,
            "first_layer_coefficient_dimension_per_profile": 22,
            "coefficient_laws_per_profile": MODULUS**22,
            "opposite_correction_coefficient_rank_upper_bound": 2,
            "coverage_qualification": (
                "All rank-0, rank-1, and rank-2 opposite corrections in "
                "the total-degree-at-most-two antipodal feature space are "
                "included. Degree>=3 and non-antipodal laws are excluded."
            ),
        },
        "dimension_gate": {
            "maximum_exhausted_physical_dimension": DIMENSION_GATE,
            "maximum_exhausted_states_per_orbit": MODULUS**DIMENSION_GATE,
            "batch_size": BATCH_SIZE,
            "dimension_distribution": {
                str(key): value
                for key, value in sorted(actual_dimensions.items())
            },
        },
        "coverage": {
            "profiles_total": 18,
            "profiles_exhausted": covered_orbits,
            "profiles_deferred": 18 - covered_orbits,
            "coefficient_law_weighted_fraction": {
                "numerator": covered_orbits,
                "denominator": 18,
            },
            "physical_quotient_states_exhausted": covered_states,
            "physical_quotient_states_total": total_states,
            "physical_state_weighted_fraction": {
                "numerator": 37,
                "denominator": 766,
            },
            "qualification": (
                "The five exhausted profiles are covered completely after "
                "quotienting duplicate coefficient descriptions. The "
                "thirteen deferred profiles have exact denominators but "
                "zero enumerated states and no outcome claim."
            ),
        },
        "outcomes_on_exhausted_profiles": {
            "two_consecutive_digit_survivors": consecutive,
            "margin_compatible_second_digit_survivors": margin_compatible,
        },
        "orbits": records,
    }
    certificate["semantic_sha256"] = compact_hash(certificate)
    return certificate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-certificate",
        action="store_true",
        help="atomically freeze the deterministic all-orbit certificate",
    )
    args = parser.parse_args()
    certificate = build_certificate()
    if args.write_certificate:
        rendered = json.dumps(
            certificate, indent=2, sort_keys=True
        ) + "\n"
        temporary = PINNED_CERTIFICATE.with_suffix(".json.tmp")
        temporary.write_text(rendered, encoding="utf-8")
        temporary.replace(PINNED_CERTIFICATE)
    else:
        pinned = json.loads(PINNED_CERTIFICATE.read_text())
        if compact_hash(certificate) != compact_hash(pinned):
            raise AssertionError("pinned all-orbit certificate changed")
    coverage = certificate["coverage"]
    outcome = certificate["outcomes_on_exhausted_profiles"]
    print(
        "profiles_exhausted="
        f"{coverage['profiles_exhausted']}/{coverage['profiles_total']}"
    )
    print(
        "physical_states_exhausted="
        f"{coverage['physical_quotient_states_exhausted']}/"
        f"{coverage['physical_quotient_states_total']}"
    )
    print(
        "two_consecutive_digit_survivors="
        f"{outcome['two_consecutive_digit_survivors']}"
    )
    print(
        "margin_compatible_second_digit_survivors="
        f"{outcome['margin_compatible_second_digit_survivors']}"
    )
    print(f"semantic_sha256={certificate['semantic_sha256']}")
    print("PASS: all-orbit rank-two dimension gate replayed")
    print("STATUS: five profiles exhaustive; thirteen explicitly deferred")


if __name__ == "__main__":
    main()
