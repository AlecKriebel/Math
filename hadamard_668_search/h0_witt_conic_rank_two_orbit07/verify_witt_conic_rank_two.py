#!/usr/bin/env python3
"""Exhaust the full quadratic antipodal-center family for h=0 orbit 07.

Write every active local center as

    t_X(j,s) = P_X(x,s,p_X,j(s)) + h_j Q_X(x,s,p_X,j(s)),

where x=j mod 3, h_j is +1 on j<6 and -1 on j>=6, and all four
polynomials P_A, P_B, Q_A, Q_B have total degree at most two over F_3.
The two opposite-correction coefficient rows Q_A,Q_B therefore have rank
at most two, with no shared-shape restriction.  This is the complete
rank-at-most-two extension of the earlier shared-shape rank-one family
inside the stated quadratic feature space.

First-layer linear algebra quotients all duplicate coefficient
descriptions before enumeration.  For orbit 07 this leaves exactly 3^14
distinct physical placements.  The verifier exhausts that space in
batches, evaluates all 18 active second-digit quadrics, and directly
replays one physical representative at every attained score.  Any exact
second-digit survivor is also checked at the following digit and against
the exact 1,756-word row-margin catalog.
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
RANK_ONE = SEARCH / "h0_witt_conic_rank_one"
TRIAGE = SEARCH / "h0_new_orbits_lift_triage"
SECOND = SEARCH / "phase_second_digit"
sys.path[:0] = [
    str(RANK_ONE),
    str(TRIAGE),
    str(SECOND),
    str(SEARCH),
]

import verify_witt_conic_rank_one as rank_one  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
from verify_lp333_order3_labeled_jet import actual_word  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    first_digit_equations,
    profiles_from_ids,
)
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    row_sum_catalog,
)


MODULUS = 3
PROFILE_DIGEST = "0x86b13a0388d98a5e"
PROFILE_LABEL = "orbit-07"
CLASSIFICATION = (
    SEARCH
    / "dense_shell_h0_complete_classification"
    / "certificate.json"
)
FINAL_SCAN = TRIAGE / "FINAL_PRODUCTION_SCAN_18.json"
PINNED_CERTIFICATE = HERE / "rank_two_orbit07_certificate.json"
ACTIVE_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))


def compact_hash(value: object) -> str:
    payload = json.dumps(
        value, separators=(",", ":"), sort_keys=True
    ).encode("ascii")
    return sha256(payload).hexdigest()


def array_hash(value: np.ndarray) -> str:
    normalized = np.asarray(value, dtype=np.uint8, order="C")
    return sha256(normalized.tobytes(order="C")).hexdigest()


def normalize(value: np.ndarray) -> np.ndarray:
    return np.asarray(value, dtype=np.int16) % MODULUS


def rank(value: np.ndarray) -> int:
    return rank_one.rank(normalize(value))


def load_profile() -> tuple[
    dict[str, object], dict[str, object], dict[str, object]
]:
    classification = json.loads(CLASSIFICATION.read_text())
    if classification["schema"] != (
        "h668-dense-shell-h0-complete-classification-v1"
    ):
        raise AssertionError("complete-classification schema changed")
    if (
        not classification["census"]["complete"]
        or len(classification["profiles"]) != 18
    ):
        raise AssertionError("complete h0 classification changed")
    records = [
        record
        for record in classification["profiles"]
        if record["production_digest"] == PROFILE_DIGEST
    ]
    if len(records) != 1 or records[0]["label"] != PROFILE_LABEL:
        raise AssertionError("orbit-07 profile is not unique")

    scan = json.loads(FINAL_SCAN.read_text())
    if scan["exact_orbits"] != 18:
        raise AssertionError("final lift scan lost an orbit")
    scan_records = [
        record
        for record in scan["orbits"]
        if record["digest"] == PROFILE_DIGEST
    ]
    if len(scan_records) != 1:
        raise AssertionError("orbit-07 lift scan record is not unique")
    scanned = scan_records[0]
    transfer = scanned["row_margin_transfer"]
    if (
        transfer["compatible_catalog_rows"] != 96
        or transfer["accepted_raw_assignments"]
        != 405_962_790_888_377_068_200
        or scanned["structured_retraction"][
            "maximum_retraction_dimension"
        ]
        != 4
        or scanned["structured_characters"][
            "six_equation_zero_fiber"
        ]
        != 205_890_943_964_535
    ):
        raise AssertionError("orbit-07 selection invariants changed")
    return classification, records[0], scanned


def coefficient_family(
    profiles: Sequence[Sequence[Sequence[int]]],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the 54-by-40 evaluation matrix and its four blocks."""

    base, opposite_a, opposite_b = rank_one.feature_matrices(profiles)
    features = np.concatenate((base, opposite_a, opposite_b), axis=1) % 3
    if features.shape != (54, 40):
        raise AssertionError("rank-two feature matrix shape changed")
    return features, opposite_a, opposite_b


def affine_coefficient_solution(
    matrix: np.ndarray, rhs: np.ndarray
) -> tuple[np.ndarray, np.ndarray, int]:
    """Canonical particular solution and nullspace rows over F_3."""

    reduced, transform, pivots = rank_one.rref_with_transform(matrix)
    transformed_rhs = transform @ rhs % MODULUS
    rank_value = len(pivots)
    if np.any(reduced[rank_value:]) or np.any(
        transformed_rhs[rank_value:]
    ):
        raise AssertionError("rank-two first layer became inconsistent")
    particular = np.zeros(matrix.shape[1], dtype=np.int16)
    for row, pivot in enumerate(pivots):
        particular[pivot] = transformed_rhs[row]
    kernel = rank_one.kernel_from_rref(reduced, pivots)
    if np.any(matrix @ particular % MODULUS != rhs):
        raise AssertionError("particular coefficient solution failed")
    if np.any(matrix @ kernel.T % MODULUS):
        raise AssertionError("coefficient kernel failed replay")
    return particular, kernel, rank_value


def canonical_row_basis(matrix: np.ndarray) -> np.ndarray:
    reduced, _, pivots = rank_one.rref_with_transform(matrix)
    dimension = len(pivots)
    basis = reduced[:dimension]
    if rank(basis) != dimension:
        raise AssertionError("canonical physical row basis lost rank")
    return basis


def map_to_affine_coordinates(
    physical_offset: np.ndarray,
    physical_basis: np.ndarray,
    affine_origin: np.ndarray,
    affine_basis: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, tuple[int, ...]]:
    selected = rank_one.select_coordinate_columns(affine_basis)
    inverse = rank_one.inverse_mod3(affine_basis[:, selected])
    offset = (
        (physical_offset[list(selected)] - affine_origin[list(selected)])
        @ inverse
    ) % MODULUS
    basis = physical_basis[:, selected] @ inverse % MODULUS
    if np.any(
        (affine_origin + offset @ affine_basis - physical_offset)
        % MODULUS
    ):
        raise AssertionError("physical offset left the first affine layer")
    if np.any((basis @ affine_basis - physical_basis) % MODULUS):
        raise AssertionError("physical directions failed affine mapping")
    return normalize(offset), normalize(basis), selected


def restrict_quadratics(
    offset: np.ndarray,
    basis: np.ndarray,
    constants: np.ndarray,
    linears: np.ndarray,
    polars: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    dimension = len(basis)
    restricted_constants = np.empty(len(constants), dtype=np.int16)
    restricted_linears = np.empty(
        (len(constants), dimension), dtype=np.int16
    )
    restricted_polars = np.empty(
        (len(constants), dimension, dimension), dtype=np.int16
    )
    for equation, polar in enumerate(polars):
        restricted_constants[equation] = (
            constants[equation]
            + linears[equation] @ offset
            + 2 * offset @ polar @ offset
        ) % MODULUS
        restricted_linears[equation] = (
            linears[equation] @ basis.T
            + 2
            * (
                offset @ polar @ basis.T
                + basis @ polar @ offset
            )
        ) % MODULUS
        restricted_polars[equation] = basis @ polar @ basis.T % MODULUS

    # Deterministic substitution check on a spanning set and one dense point.
    tests = [np.zeros(dimension, dtype=np.int16)]
    tests.extend(np.eye(dimension, dtype=np.int16))
    tests.append(np.arange(dimension, dtype=np.int16) % MODULUS)
    test_points = np.asarray(tests, dtype=np.int16)
    ambient = (offset + test_points @ basis) % MODULUS
    original_values = rank_one.evaluate_quadratics(
        ambient, constants, linears, polars
    )
    restricted_values = rank_one.evaluate_quadratics(
        test_points,
        restricted_constants,
        restricted_linears,
        restricted_polars,
    )
    if not np.array_equal(original_values, restricted_values):
        raise AssertionError("restricted quadrics failed substitution replay")
    return (
        restricted_constants,
        restricted_linears,
        restricted_polars,
    )


def ternary_batch(start: int, stop: int, dimension: int) -> np.ndarray:
    integers = np.arange(start, stop, dtype=np.int64)
    result = np.empty((len(integers), dimension), dtype=np.int16)
    quotient = integers.copy()
    for column in range(dimension - 1, -1, -1):
        result[:, column] = quotient % MODULUS
        quotient //= MODULUS
    if np.any(quotient):
        raise AssertionError("ternary coordinate conversion overflowed")
    return result


def labelled_aggregate(
    masks_a: tuple[int, ...], masks_b: tuple[int, ...]
) -> tuple[int, ...]:
    words = tuple(
        tuple(
            actual_word(channel, class_index, masks[class_index])
            for class_index in range(12)
        )
        for channel, masks in enumerate((masks_a, masks_b))
    )
    aggregate = []
    for row in range(9):
        plus_a = sum(word[row] for word in words[0])
        plus_b = sum(word[row] for word in words[1])
        aggregate.extend((plus_a + plus_b - 12, plus_b - plus_a))
    return tuple(aggregate)


def direct_replay(
    profiles: Sequence[Sequence[Sequence[int]]],
    affine_origin: np.ndarray,
    affine_basis: np.ndarray,
    affine_point: np.ndarray,
    expected_score: int,
) -> tuple[np.ndarray, tuple[int, ...]]:
    placement = (
        affine_origin + affine_point @ affine_basis
    ) % MODULUS
    first = second.symbolic_first_digits(
        first_digit_equations(profiles), placement
    )
    direct_second = second.direct_second_digits(profiles, placement)
    if first != (0,) * 20:
        raise AssertionError("enumerated point left the first layer")
    active = tuple(direct_second[row] for row in ACTIVE_ROWS)
    if sum(value == 0 for value in active) != expected_score:
        raise AssertionError("direct second-digit score changed")
    return placement, active


def build_certificate() -> dict[str, object]:
    classification, orbit, scanned = load_profile()
    profiles = profiles_from_ids(
        orbit["profile_ids_a"], orbit["profile_ids_b"]
    )
    local = rank_one.conic_local_theorem()
    features, opposite_a, opposite_b = coefficient_family(profiles)

    equations = augmented_system(first_digit_equations(profiles))
    equation_matrix = np.asarray(
        [row[:-1] for row in equations], dtype=np.int16
    ) % MODULUS
    rhs = np.asarray(
        [row[-1] for row in equations], dtype=np.int16
    ) % MODULUS
    coefficient_system = equation_matrix @ features % MODULUS
    particular, coefficient_kernel, constraint_rank = (
        affine_coefficient_solution(coefficient_system, rhs)
    )
    feature_rank = rank(features)
    coefficient_solution_dimension = len(coefficient_kernel)
    physical_offset = particular @ features.T % MODULUS
    physical_directions = coefficient_kernel @ features.T % MODULUS
    physical_basis = canonical_row_basis(physical_directions)
    physical_dimension = len(physical_basis)
    evaluation_kernel_dimension = (
        coefficient_solution_dimension - physical_dimension
    )
    if (
        feature_rank,
        constraint_rank,
        coefficient_solution_dimension,
        physical_dimension,
        evaluation_kernel_dimension,
    ) != (32, 18, 22, 14, 8):
        raise AssertionError("rank-two quotient dimensions changed")
    if np.any(
        (equation_matrix @ physical_offset - rhs) % MODULUS
    ) or np.any(equation_matrix @ physical_basis.T % MODULUS):
        raise AssertionError("physical first-layer quotient failed replay")

    (
        affine_origin_raw,
        affine_basis_raw,
        constants_raw,
        linears_raw,
        polars_raw,
    ) = rank_one.exact_quadratic_forms(profiles)
    affine_origin = normalize(np.asarray(affine_origin_raw))
    affine_basis = normalize(np.asarray(affine_basis_raw))
    constants = normalize(np.asarray(constants_raw))
    linears = normalize(np.asarray(linears_raw))
    polars = normalize(np.asarray(polars_raw))
    affine_offset, family_basis, selected = map_to_affine_coordinates(
        physical_offset,
        physical_basis,
        affine_origin,
        affine_basis,
    )
    (
        restricted_constants,
        restricted_linears,
        restricted_polars,
    ) = restrict_quadratics(
        affine_offset, family_basis, constants, linears, polars
    )

    total_points = MODULUS**physical_dimension
    batch_size = 32_768
    histogram = np.zeros(len(constants) + 1, dtype=np.int64)
    first_point_by_score: dict[int, np.ndarray] = {}
    exact_points: list[np.ndarray] = []
    codimension_one_points: list[np.ndarray] = []
    coordinate_hasher = sha256()
    score_hasher = sha256()
    for start in range(0, total_points, batch_size):
        coordinates = ternary_batch(
            start, min(start + batch_size, total_points), physical_dimension
        )
        coordinate_hasher.update(
            np.asarray(coordinates, dtype=np.uint8).tobytes(order="C")
        )
        values = rank_one.evaluate_quadratics(
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
        exact_offsets = np.flatnonzero(scores == len(constants))
        for offset in exact_offsets:
            exact_points.append(
                (
                    affine_offset
                    + coordinates[int(offset)] @ family_basis
                )
                % MODULUS
            )
        codimension_one_offsets = np.flatnonzero(
            scores == len(constants) - 1
        )
        for offset in codimension_one_offsets:
            codimension_one_points.append(
                (
                    affine_offset
                    + coordinates[int(offset)] @ family_basis
                )
                % MODULUS
            )
        if len(exact_points) > 100_000:
            raise AssertionError(
                "digit-three replay cap exceeded; pilot needs a new bound"
            )
    if int(histogram.sum()) != total_points:
        raise AssertionError("complete family histogram lost points")

    direct_replays = []
    for score, affine_point in sorted(first_point_by_score.items()):
        placement, active = direct_replay(
            profiles,
            affine_origin,
            affine_basis,
            affine_point,
            score,
        )
        derived = tuple(
            int(value)
            for value in rank_one.evaluate_quadratics(
                affine_point[None, :], constants, linears, polars
            )[0]
        )
        if active != derived:
            raise AssertionError("direct and derived second digits differ")
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

    catalog = set(row_sum_catalog())
    if len(catalog) != 1_756:
        raise AssertionError("row-margin catalog size changed")
    following_defects: dict[int, int] = {}
    margin_compatible = 0
    consecutive = 0
    consecutive_and_margin = 0
    exact_replays = []
    for affine_point in exact_points:
        placement, active = direct_replay(
            profiles,
            affine_origin,
            affine_basis,
            affine_point,
            len(constants),
        )
        if active != (0,) * len(constants):
            raise AssertionError("stored exact point is not exact")
        values = second.displayed_values(profiles, placement)
        digits = tuple(second.lambda_digits(value, 12) for value in values)
        digit_counts = tuple(
            sum(row[digit] != 0 for row in digits)
            for digit in range(12)
        )
        if digit_counts[:3] != (0, 0, 0):
            raise AssertionError("exact point lost its first three digits")
        defect = digit_counts[3]
        following_defects[defect] = following_defects.get(defect, 0) + 1
        masks = second.masks_from_trits(profiles, placement)
        aggregate = labelled_aggregate(*masks)
        margin_member = aggregate in catalog
        margin_compatible += int(margin_member)
        consecutive += int(defect == 0)
        consecutive_and_margin += int(defect == 0 and margin_member)
        exact_replays.append(
            {
                "affine_point_sha256": compact_hash(
                    tuple(map(int, affine_point))
                ),
                "placement_sha256": compact_hash(
                    tuple(map(int, placement))
                ),
                "following_digit_defect": defect,
                "row_margin_catalog_member": margin_member,
                "row_margin_aggregate_sha256": compact_hash(aggregate),
            }
        )

    missing_row_histogram: dict[int, int] = {}
    margin_compatible_codimension_one = 0
    codimension_one_replays = []
    for affine_point in codimension_one_points:
        placement, active = direct_replay(
            profiles,
            affine_origin,
            affine_basis,
            affine_point,
            len(constants) - 1,
        )
        missing = tuple(
            index for index, value in enumerate(active) if value
        )
        if len(missing) != 1:
            raise AssertionError("a codimension-one point changed score")
        active_index = missing[0]
        physical_row = ACTIVE_ROWS[active_index]
        missing_row_histogram[physical_row] = (
            missing_row_histogram.get(physical_row, 0) + 1
        )
        masks = second.masks_from_trits(profiles, placement)
        aggregate = labelled_aggregate(*masks)
        margin_member = aggregate in catalog
        margin_compatible_codimension_one += int(margin_member)
        codimension_one_replays.append(
            {
                "affine_point_sha256": compact_hash(
                    tuple(map(int, affine_point))
                ),
                "placement_sha256": compact_hash(
                    tuple(map(int, placement))
                ),
                "missing_active_equation_index": active_index,
                "missing_physical_row": physical_row,
                "missing_value": active[active_index],
                "row_margin_catalog_member": margin_member,
                "row_margin_aggregate_sha256": compact_hash(aggregate),
            }
        )

    maximum_score = max(
        score for score, count in enumerate(histogram) if count
    )
    coefficient_solutions = MODULUS**coefficient_solution_dimension
    multiplicity = MODULUS**evaluation_kernel_dimension
    if coefficient_solutions != total_points * multiplicity:
        raise AssertionError("coefficient quotient accounting failed")
    certificate: dict[str, object] = {
        "schema": "h668-h0-witt-conic-rank-two-orbit07-v1",
        "scope": (
            "Complete pilot of all independent-channel quadratic antipodal "
            "center laws for exact dense-shell h0 orbit-07. This is not an "
            "LP(333) or H(668) exclusion."
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
            "rank_one_verifier_sha256": sha256(
                Path(rank_one.__file__).read_bytes()
            ).hexdigest(),
        },
        "profile": {
            "label": orbit["label"],
            "digest": orbit["production_digest"],
            "ids_a": orbit["profile_ids_a"],
            "ids_b": orbit["profile_ids_b"],
            "target": orbit["target"],
            "classification_record_sha256": orbit["record_sha256"],
            "selection": {
                "compatible_catalog_rows": scanned[
                    "row_margin_transfer"
                ]["compatible_catalog_rows"],
                "accepted_raw_assignments": scanned[
                    "row_margin_transfer"
                ]["accepted_raw_assignments"],
                "structured_six_zero_fiber": scanned[
                    "structured_characters"
                ]["six_equation_zero_fiber"],
                "maximum_structured_retraction_dimension": scanned[
                    "structured_retraction"
                ]["maximum_retraction_dimension"],
                "reason": (
                    "Tied maximum of 96 compatible catalog rows, "
                    "second-largest raw transfer mass, and smallest "
                    "structured six-zero fiber; its full quadratic "
                    "rank-two image also has the smallest observed "
                    "first-layer dimension, 14."
                ),
            },
        },
        "local_conic_theorem": local,
        "family": {
            "center_law": (
                "t_X=P_X(x,s,p_X,j(s))+h_j*Q_X(x,s,p_X,j(s)); "
                "u_X=-p_X,j(s)*t_X"
            ),
            "quadratic_monomials_per_polynomial": 10,
            "independent_polynomials": ("P_A", "P_B", "Q_A", "Q_B"),
            "coefficient_parameters": 40,
            "opposite_correction_coefficient_rank_upper_bound": 2,
            "coverage": (
                "All four total-degree-at-most-two polynomials over F_3 "
                "are arbitrary. Thus every rank-0, rank-1, and rank-2 "
                "opposite correction in this quadratic antipodal feature "
                "space is included. No degree>=3 or non-antipodal center "
                "law is claimed."
            ),
            "feature_matrix_sha256": array_hash(features),
            "opposite_a_sha256": array_hash(opposite_a),
            "opposite_b_sha256": array_hash(opposite_b),
            "feature_evaluation_rank": feature_rank,
        },
        "first_layer_quotient": {
            "constraint_rank": constraint_rank,
            "coefficient_solution_dimension": (
                coefficient_solution_dimension
            ),
            "coefficient_solutions": coefficient_solutions,
            "evaluation_kernel_dimension": evaluation_kernel_dimension,
            "coefficient_descriptions_per_physical_placement": multiplicity,
            "distinct_physical_dimension": physical_dimension,
            "distinct_physical_placements": total_points,
            "ambient_first_layer_dimension": 36,
            "ambient_fraction_numerator": 1,
            "ambient_fraction_denominator": MODULUS ** (
                36 - physical_dimension
            ),
            "physical_offset_sha256": array_hash(physical_offset),
            "physical_basis_sha256": array_hash(physical_basis),
            "affine_coordinate_columns": selected,
            "affine_offset_sha256": array_hash(affine_offset),
            "affine_family_basis_sha256": array_hash(family_basis),
        },
        "complete_pilot": {
            "coverage_numerator": total_points,
            "coverage_denominator": total_points,
            "batch_size": batch_size,
            "coordinate_stream_sha256": coordinate_hasher.hexdigest(),
            "score_stream_sha256": score_hasher.hexdigest(),
            "score_histogram": {
                str(score): int(count)
                for score, count in enumerate(histogram)
                if count
            },
            "maximum_active_second_digit_equations": maximum_score,
            "active_second_digit_equations": len(constants),
            "exact_second_digit_survivors": len(exact_points),
            "codimension_one_near_misses": len(
                codimension_one_points
            ),
            "codimension_one_missing_row_histogram": {
                str(key): value
                for key, value in sorted(missing_row_histogram.items())
            },
            "margin_compatible_codimension_one_near_misses": (
                margin_compatible_codimension_one
            ),
            "following_digit_defect_histogram": {
                str(key): value
                for key, value in sorted(following_defects.items())
            },
            "two_consecutive_digit_survivors": consecutive,
            "row_margin_catalog_rows": len(catalog),
            "margin_compatible_second_digit_survivors": margin_compatible,
            "two_consecutive_and_margin_survivors": (
                consecutive_and_margin
            ),
            "direct_score_replays": direct_replays,
            "codimension_one_replays": codimension_one_replays,
            "exact_survivor_replays": exact_replays,
        },
        "resource_bound": {
            "enumerated_states": total_points,
            "largest_persistent_array": (
                "14x54 physical/affine bases; enumeration is batched"
            ),
            "batch_rows": batch_size,
            "declared_ram_limit_bytes": 8_000_000_000,
            "qualification": (
                "The 3^14 quotient is exhaustive. No 3^22 coefficient "
                "array or 3^36 ambient array is materialized."
            ),
        },
        "conclusion": (
            f"The complete {total_points}-placement quadratic rank-two "
            f"pilot has {len(exact_points)} exact second-digit survivors, "
            f"{consecutive} two-consecutive-digit survivors, and "
            f"{margin_compatible} margin-compatible second-digit lifts."
        ),
    }
    certificate["semantic_sha256"] = compact_hash(certificate)
    return certificate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-certificate",
        action="store_true",
        help="atomically freeze the deterministic certificate",
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
            raise AssertionError("pinned rank-two certificate changed")
    pilot = certificate["complete_pilot"]
    print(
        "family_physical_placements="
        f"{certificate['first_layer_quotient']['distinct_physical_placements']}"
    )
    print(
        "maximum_second_digit_score="
        f"{pilot['maximum_active_second_digit_equations']}/"
        f"{pilot['active_second_digit_equations']}"
    )
    print(
        "exact_second_digit_survivors="
        f"{pilot['exact_second_digit_survivors']}"
    )
    print(
        "two_consecutive_digit_survivors="
        f"{pilot['two_consecutive_digit_survivors']}"
    )
    print(
        "margin_compatible_second_digit_survivors="
        f"{pilot['margin_compatible_second_digit_survivors']}"
    )
    print(f"semantic_sha256={certificate['semantic_sha256']}")
    print("PASS: complete orbit-07 quadratic rank-two pilot replayed")
    print("STATUS: delimited family result only; no LP(333) or H(668)")


if __name__ == "__main__":
    main()
