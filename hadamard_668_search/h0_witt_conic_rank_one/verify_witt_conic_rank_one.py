#!/usr/bin/env python3
"""Verify the quadratic-center rank-one obstruction for the c90c h=0 orbit.

The row coordinate in Z/9 is written r=s+3q.  For every h=0 residue
profile p(s), every normalized local three-subset has the unique conic form

    (q-t_s)^2 = p(s)-1

on its active fibers.  This verifier exhausts the structured center family

    t_X(j,s) = P_X(x,s,p_X,j(s))
                 + a_X h_j R(x,s,p_X,j(s)),

where x=j mod 3, h_j is +1 on j<6 and -1 on j>=6, P_A and P_B are
arbitrary ternary quadratics, and R is a shared nonzero quadratic shape
up to scalar.  It proves that no member passes the second placement digit.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys
from typing import Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
SECOND = SEARCH / "phase_second_digit"
sys.path[:0] = [
    str(SECOND),
    str(SEARCH),
]

from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    first_digit_equations,
    matrix_rank,
    profiles_from_ids,
)
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
    quotient_support,
)
import verify_phase_second_digit as second  # noqa: E402


MODULUS = 3
PROFILE_DIGEST = "0xc90c2887b652140a"
ACTIVE_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))
CLASSIFICATION = (
    SEARCH
    / "dense_shell_h0_complete_classification"
    / "certificate.json"
)
PINNED_CERTIFICATE = HERE / "conic_rank_one_certificate.json"


def compact_hash(value: object) -> str:
    payload = json.dumps(
        value, separators=(",", ":"), sort_keys=True
    ).encode("ascii")
    return sha256(payload).hexdigest()


def array_hash(value: np.ndarray) -> str:
    normalized = np.asarray(value, dtype=np.uint8, order="C")
    return sha256(normalized.tobytes(order="C")).hexdigest()


def rank(matrix: Sequence[Sequence[int]] | np.ndarray) -> int:
    rows = tuple(
        tuple(int(value) % MODULUS for value in row)
        for row in np.asarray(matrix).tolist()
    )
    return matrix_rank(rows)


def inverse_mod3(matrix: np.ndarray) -> np.ndarray:
    value = np.asarray(matrix, dtype=np.int16) % MODULUS
    rows, columns = value.shape
    if rows != columns:
        raise ValueError("only square matrices can be inverted")
    work = np.concatenate(
        (value, np.eye(rows, dtype=np.int16)), axis=1
    )
    pivot_row = 0
    for column in range(columns):
        choices = np.flatnonzero(work[pivot_row:, column])
        if not len(choices):
            raise ValueError("matrix is singular")
        pivot = pivot_row + int(choices[0])
        work[[pivot_row, pivot]] = work[[pivot, pivot_row]]
        if work[pivot_row, column] == 2:
            work[pivot_row] = 2 * work[pivot_row] % MODULUS
        for other in range(rows):
            if other != pivot_row and work[other, column]:
                work[other] = (
                    work[other]
                    - work[other, column] * work[pivot_row]
                ) % MODULUS
        pivot_row += 1
    if not np.array_equal(
        work[:, :columns], np.eye(rows, dtype=np.int16)
    ):
        raise AssertionError("mod-three inversion failed")
    return work[:, columns:]


def rref_with_transform(
    matrix: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, tuple[int, ...]]:
    """Return R, T, pivots with R=T*matrix over F_3."""

    value = np.asarray(matrix, dtype=np.int16) % MODULUS
    rows, columns = value.shape
    work = np.concatenate(
        (value, np.eye(rows, dtype=np.int16)), axis=1
    )
    pivots: list[int] = []
    pivot_row = 0
    for column in range(columns):
        choices = np.flatnonzero(work[pivot_row:, column])
        if not len(choices):
            continue
        pivot = pivot_row + int(choices[0])
        work[[pivot_row, pivot]] = work[[pivot, pivot_row]]
        if work[pivot_row, column] == 2:
            work[pivot_row] = 2 * work[pivot_row] % MODULUS
        for other in range(rows):
            if other != pivot_row and work[other, column]:
                work[other] = (
                    work[other]
                    - work[other, column] * work[pivot_row]
                ) % MODULUS
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    reduced = work[:, :columns]
    transform = work[:, columns:]
    if np.any((transform @ value - reduced) % MODULUS):
        raise AssertionError("row-operation transform failed replay")
    return reduced, transform, tuple(pivots)


def quadratic_monomials(
    class_index: int, residue: int, profile_value: int
) -> np.ndarray:
    """The ten total-degree-at-most-two monomials in x,s,p."""

    x = class_index % MODULUS
    s = residue
    p = profile_value
    return np.asarray(
        (1, x, s, p, x * x, s * s, p * p, x * s, x * p, s * p),
        dtype=np.int16,
    ) % MODULUS


def projective_shapes() -> np.ndarray:
    """All points of P^9(F_3), first nonzero coordinate normalized to one."""

    result = []
    for leading in range(10):
        for tail in product(range(MODULUS), repeat=9 - leading):
            result.append((0,) * leading + (1,) + tail)
    shapes = np.asarray(result, dtype=np.int16)
    expected = (MODULUS**10 - 1) // (MODULUS - 1)
    if len(shapes) != expected or expected != 29_524:
        raise AssertionError("projective shape census changed")
    return shapes


def conic_local_theorem() -> dict[str, object]:
    """Exhaust the local center/trit correspondence for h=0 profiles."""

    checks = 0
    records = []
    for count in range(3):
        for trit in range(MODULUS):
            support = tuple(quotient_support(count, trit))
            if count == 0:
                centers = tuple(range(MODULUS))
                expected_support = ()
            else:
                center = (-count * trit) % MODULUS
                centers = (center,)
                expected_support = tuple(
                    quotient
                    for quotient in range(MODULUS)
                    if (
                        (quotient - center) ** 2 - (count - 1)
                    )
                    % MODULUS
                    == 0
                )
            if support != expected_support:
                raise AssertionError("local conic support identity failed")
            records.append((count, trit, centers, support))
            checks += 1
    return {
        "profile_values": (0, 1, 2),
        "trits_per_value": 3,
        "checks": checks,
        "records_sha256": compact_hash(records),
        "active_center_formula": "t=-p*u in F_3",
    }


def load_complete_h0() -> tuple[dict[str, object], dict[str, object]]:
    payload = json.loads(CLASSIFICATION.read_text())
    if payload["schema"] != "h668-dense-shell-h0-complete-classification-v1":
        raise AssertionError("unexpected h0 classification schema")
    census = payload["census"]
    if census["status"] != "PASS: every required prefix shard is complete":
        raise AssertionError("h0 aggregate is not complete")
    if not census["complete"]:
        raise AssertionError("h0 shell lost complete status")
    orbits = payload["profiles"]
    if len(orbits) != 18:
        raise AssertionError("complete h0 orbit count changed")
    allowed = {1, 2, 4, 5, 6, 7, 8}
    for orbit in orbits:
        if (
            set(orbit["profile_ids_a"]) | set(orbit["profile_ids_b"])
            > allowed
        ):
            raise AssertionError("an h0 orbit contains a profile value three")
    matches = [
        orbit
        for orbit in orbits
        if orbit["production_digest"] == PROFILE_DIGEST
    ]
    if len(matches) != 1:
        raise AssertionError("priority h0 orbit was not unique")
    return payload, matches[0]


def feature_matrices(
    profiles: Sequence[Sequence[Sequence[int]]],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return base P and opposite-correction matrices for A and B."""

    coordinates = active_trit_coordinates(profiles)
    if len(coordinates) != 54:
        raise AssertionError("h0 active placement count changed")
    base = np.zeros((54, 20), dtype=np.int16)
    opposite_a = np.zeros((54, 10), dtype=np.int16)
    opposite_b = np.zeros((54, 10), dtype=np.int16)
    for index, (channel, class_index, residue) in enumerate(coordinates):
        profile_value = int(profiles[channel][class_index][residue])
        monomials = quadratic_monomials(
            class_index, residue, profile_value
        )
        # For active fibers t=-p*u, equivalently u=-p*t.
        center_features = (-profile_value * monomials) % MODULUS
        base[
            index, channel * 10 : (channel + 1) * 10
        ] = center_features
        opposite_sign = 1 if class_index < 6 else -1
        correction = opposite_sign * center_features % MODULUS
        (opposite_a if channel == 0 else opposite_b)[index] = correction
    return base, opposite_a, opposite_b


def kernel_from_rref(
    reduced: np.ndarray, pivots: Sequence[int]
) -> np.ndarray:
    columns = reduced.shape[1]
    free = tuple(column for column in range(columns) if column not in pivots)
    result = []
    for free_column in free:
        vector = np.zeros(columns, dtype=np.int16)
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row, free_column] % MODULUS
        result.append(vector)
    return np.asarray(result, dtype=np.int16)


def select_coordinate_columns(basis: np.ndarray) -> tuple[int, ...]:
    selected: list[int] = []
    current_rank = 0
    for column in range(basis.shape[1]):
        candidate = basis[:, selected + [column]].T
        next_rank = rank(candidate)
        if next_rank > current_rank:
            selected.append(column)
            current_rank = next_rank
        if current_rank == basis.shape[0]:
            break
    if len(selected) != basis.shape[0]:
        raise AssertionError("failed to select affine coordinate columns")
    return tuple(selected)


def ternary_points(dimension: int) -> np.ndarray:
    return np.asarray(
        tuple(product(range(MODULUS), repeat=dimension)), dtype=np.int16
    )


def exact_quadratic_forms(
    profiles: Sequence[Sequence[Sequence[int]]],
) -> tuple[
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[tuple[int, ...], ...], ...],
]:
    """Derive the c90c first affine layer and active second quadrics."""

    equations = first_digit_equations(profiles)
    rows = augmented_system(equations)
    coefficients = tuple(row[:-1] for row in rows)
    origin = canonical_solution(rows, 54)
    if origin is None:
        raise AssertionError("c90c first placement layer became inconsistent")
    basis = second.nullspace_basis(coefficients, columns=54)
    if matrix_rank(coefficients) != 18 or len(basis) != 36:
        raise AssertionError("c90c first rank/nullity changed")
    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles), origin, basis
    )
    active = tuple(
        index
        for index in range(20)
        if (
            constants[index]
            or any(linears[index])
            or any(
                value
                for row in polars[index]
                for value in row
            )
        )
    )
    if active != ACTIVE_ROWS:
        raise AssertionError("c90c active second-digit rows changed")
    return (
        origin,
        basis,
        tuple(constants[index] for index in active),
        tuple(linears[index] for index in active),
        tuple(polars[index] for index in active),
    )


def evaluate_quadratics(
    points: np.ndarray,
    constants: np.ndarray,
    linears: np.ndarray,
    polars: np.ndarray,
) -> np.ndarray:
    result = (constants[None, :] + points @ linears.T) % MODULUS
    for equation in range(len(constants)):
        result[:, equation] = (
            result[:, equation]
            + 2
            * np.sum(
                (points @ polars[equation]) * points,
                axis=1,
            )
        ) % MODULUS
    return result


def build_certificate() -> dict[str, object]:
    aggregate, orbit = load_complete_h0()
    local = conic_local_theorem()
    profiles = profiles_from_ids(
        orbit["profile_ids_a"], orbit["profile_ids_b"]
    )
    base, opposite_a, opposite_b = feature_matrices(profiles)

    equations = augmented_system(first_digit_equations(profiles))
    coefficient_matrix = np.asarray(
        tuple(row[:-1] for row in equations), dtype=np.int16
    ) % MODULUS
    right_hand_side = np.asarray(
        tuple(row[-1] for row in equations), dtype=np.int16
    ) % MODULUS
    base_system = coefficient_matrix @ base % MODULUS
    correction_a = coefficient_matrix @ opposite_a % MODULUS
    correction_b = coefficient_matrix @ opposite_b % MODULUS
    reduced, transform, pivots = rref_with_transform(base_system)
    base_rank = len(pivots)
    full_rank = rank(
        np.concatenate((base_system, correction_a, correction_b), axis=1)
    )
    if (base_rank, full_rank) != (17, 18):
        raise AssertionError("first-layer rank pair changed")
    parameter_kernel = kernel_from_rref(reduced, pivots)
    if parameter_kernel.shape != (3, 20):
        raise AssertionError("base parameter kernel changed")

    # Map physical first-layer solutions into the certified 36-dimensional
    # affine coordinate system in which the second digit is quadratic.
    (
        affine_origin_raw,
        affine_basis_raw,
        constants_raw,
        linears_raw,
        polars_raw,
    ) = exact_quadratic_forms(profiles)
    affine_origin = np.asarray(affine_origin_raw, dtype=np.int16)
    affine_basis = np.asarray(affine_basis_raw, dtype=np.int16)
    selected = select_coordinate_columns(affine_basis)
    coordinate_inverse = inverse_mod3(affine_basis[:, selected])
    base_to_affine = base[list(selected)].T @ coordinate_inverse % MODULUS
    a_to_affine = (
        opposite_a[list(selected)].T @ coordinate_inverse % MODULUS
    )
    b_to_affine = (
        opposite_b[list(selected)].T @ coordinate_inverse % MODULUS
    )
    affine_offset = (
        -affine_origin[list(selected)] @ coordinate_inverse
    ) % MODULUS
    kernel_affine = parameter_kernel @ base_to_affine % MODULUS
    physical_kernel_rank = rank(kernel_affine)
    if physical_kernel_rank != 1:
        raise AssertionError("base parameter evaluation-kernel changed")

    shapes = projective_shapes()
    transformed_rhs = transform @ right_hand_side % MODULUS
    transformed_a = (transform @ correction_a % MODULUS) @ shapes.T
    transformed_b = (transform @ correction_b % MODULUS) @ shapes.T

    centers = []
    amplitude_histogram: dict[str, int] = {}
    for amplitude_a in range(MODULUS):
        for amplitude_b in range(MODULUS):
            feasible = np.all(
                (
                    amplitude_a * transformed_a[base_rank:]
                    + amplitude_b * transformed_b[base_rank:]
                    - transformed_rhs[base_rank:, None]
                )
                % MODULUS
                == 0,
                axis=0,
            )
            shape_indices = np.flatnonzero(feasible)
            amplitude_histogram[
                f"{amplitude_a},{amplitude_b}"
            ] = int(len(shape_indices))
            if not len(shape_indices):
                continue
            transformed_target = (
                transformed_rhs[:, None]
                - amplitude_a * transformed_a[:, shape_indices]
                - amplitude_b * transformed_b[:, shape_indices]
            ) % MODULUS
            particular = np.zeros(
                (len(shape_indices), 20), dtype=np.int16
            )
            for row, pivot in enumerate(pivots):
                particular[:, pivot] = transformed_target[row]
            selected_shapes = shapes[shape_indices]
            affine_centers = (
                particular @ base_to_affine
                + amplitude_a * (selected_shapes @ a_to_affine)
                + amplitude_b * (selected_shapes @ b_to_affine)
                + affine_offset
            ) % MODULUS
            centers.append(affine_centers)
    all_centers = np.concatenate(centers, axis=0)
    raw_feasible_amplitude_centers = len(all_centers)
    canonical_shape_amplitude_centers = (
        1
        + sum(
            count
            for amplitudes, count in amplitude_histogram.items()
            if amplitudes != "0,0"
        )
    )
    raw_coefficient_point_incidences = raw_feasible_amplitude_centers * (
        MODULUS ** len(parameter_kernel)
    )
    canonical_coefficient_point_incidences = (
        canonical_shape_amplitude_centers
        * MODULUS ** len(parameter_kernel)
    )
    if (
        raw_coefficient_point_incidences,
        canonical_coefficient_point_incidences,
    ) != (2_922_804, 2_125_683):
        raise AssertionError("rank-one family incidence count changed")

    unique_centers = np.unique(
        np.asarray(all_centers, dtype=np.uint8), axis=0
    ).astype(np.int16)
    kernel_parameters = ternary_points(len(parameter_kernel))
    kernel_offsets = np.unique(
        np.asarray(
            kernel_parameters @ kernel_affine % MODULUS,
            dtype=np.uint8,
        ),
        axis=0,
    ).astype(np.int16)
    if len(kernel_offsets) != MODULUS**physical_kernel_rank:
        raise AssertionError("physical kernel image count changed")
    raw_physical_point_incidences = (
        raw_feasible_amplitude_centers * len(kernel_offsets)
    )
    canonical_physical_point_incidences = (
        canonical_shape_amplitude_centers * len(kernel_offsets)
    )
    if (
        raw_physical_point_incidences,
        canonical_physical_point_incidences,
    ) != (324_756, 236_187):
        raise AssertionError("physical incidence count changed")
    expanded = (
        unique_centers[:, None, :] + kernel_offsets[None, :, :]
    ) % MODULUS
    unique_points = np.unique(
        np.asarray(expanded.reshape(-1, 36), dtype=np.uint8), axis=0
    ).astype(np.int16)

    constants = np.asarray(constants_raw, dtype=np.int16)
    linears = np.asarray(linears_raw, dtype=np.int16)
    polars = np.asarray(polars_raw, dtype=np.int16)
    histogram = np.zeros(len(constants) + 1, dtype=np.int64)
    first_point_by_score: dict[int, tuple[int, ...]] = {}
    batch_size = 32_768
    for start in range(0, len(unique_points), batch_size):
        points = unique_points[start : start + batch_size]
        values = evaluate_quadratics(points, constants, linears, polars)
        scores = np.sum(values == 0, axis=1)
        histogram += np.bincount(scores, minlength=len(histogram))
        for offset, score_raw in enumerate(scores):
            score = int(score_raw)
            if score not in first_point_by_score:
                first_point_by_score[score] = tuple(
                    int(value) for value in points[offset]
                )
    maximum_score = max(
        score for score, count in enumerate(histogram) if count
    )
    if maximum_score != 16 or histogram[17] or histogram[18]:
        raise AssertionError("a rank-one conic center reached digit two")

    # Directly replay one deterministic point at every attained score.
    direct_replays = []
    for score in sorted(first_point_by_score):
        affine_point = np.asarray(
            first_point_by_score[score], dtype=np.int16
        )
        placement = (
            affine_origin + affine_point @ affine_basis
        ) % MODULUS
        first_values = second.symbolic_first_digits(
            first_digit_equations(profiles), placement
        )
        second_values = second.direct_second_digits(profiles, placement)
        if first_values != (0,) * 20:
            raise AssertionError("structured point left the first layer")
        direct_active = tuple(second_values[row] for row in ACTIVE_ROWS)
        derived = tuple(
            int(value)
            for value in evaluate_quadratics(
                affine_point[None, :], constants, linears, polars
            )[0]
        )
        if direct_active != derived:
            raise AssertionError("direct and quadratic digit-two replay differ")
        if sum(value == 0 for value in direct_active) != score:
            raise AssertionError("score replay changed")
        direct_replays.append(
            {
                "score": score,
                "affine_point_sha256": compact_hash(
                    tuple(int(value) for value in affine_point)
                ),
                "placement_sha256": compact_hash(
                    tuple(int(value) for value in placement)
                ),
                "active_values": direct_active,
            }
        )

    certificate: dict[str, object] = {
        "schema": "h668-h0-witt-conic-rank-one-v1",
        "scope": (
            "Complete obstruction for a profile-aware rank-one structured "
            "center family on c90c; not an LP(333) or H(668) exclusion."
        ),
        "classification": {
            "path": str(CLASSIFICATION.relative_to(SEARCH)),
            "file_sha256": sha256(
                CLASSIFICATION.read_bytes()
            ).hexdigest(),
            "source_sha256": aggregate["census"]["source_sha256"],
            "classification_semantic_sha256": aggregate["census"][
                "semantic_sha256"
            ],
            "complete_h0_orbits": 18,
        },
        "profile": {
            "digest": orbit["production_digest"],
            "ids_a": orbit["profile_ids_a"],
            "ids_b": orbit["profile_ids_b"],
            "target": orbit["target"],
            "classification_record_sha256": orbit["record_sha256"],
            "active_placement_centers": 54,
        },
        "local_conic_theorem": local,
        "family": {
            "center_law": (
                "t_X=P_X(x,s,p)+a_X*h_j*R(x,s,p), "
                "u_X=-p*t_X"
            ),
            "quadratic_monomials": 10,
            "independent_base_polynomials": 2,
            "shared_projective_shapes": len(shapes),
            "channel_amplitudes": 9,
            "shape_sha256": array_hash(shapes),
            "base_feature_sha256": array_hash(base),
            "opposite_a_sha256": array_hash(opposite_a),
            "opposite_b_sha256": array_hash(opposite_b),
        },
        "first_layer": {
            "base_parameter_rank": base_rank,
            "full_parameter_rank": full_rank,
            "base_coefficient_kernel_dimension": len(parameter_kernel),
            "base_physical_kernel_dimension": physical_kernel_rank,
            "raw_feasible_amplitude_centers": (
                raw_feasible_amplitude_centers
            ),
            "canonical_shape_amplitude_centers": (
                canonical_shape_amplitude_centers
            ),
            "amplitude_histogram": amplitude_histogram,
            "raw_coefficient_point_incidences": (
                raw_coefficient_point_incidences
            ),
            "canonical_coefficient_point_incidences": (
                canonical_coefficient_point_incidences
            ),
            "raw_physical_point_incidences": (
                raw_physical_point_incidences
            ),
            "canonical_physical_point_incidences": (
                canonical_physical_point_incidences
            ),
            "unique_affine_centers": len(unique_centers),
            "unique_physical_placements": len(unique_points),
            "all_centers_sha256": array_hash(all_centers),
            "unique_centers_sha256": array_hash(unique_centers),
            "unique_points_sha256": array_hash(unique_points),
        },
        "second_layer": {
            "active_equations": len(constants),
            "score_histogram_on_unique_placements": {
                str(score): int(count)
                for score, count in enumerate(histogram)
                if count
            },
            "maximum_zero_equations": maximum_score,
            "exact_digit_two_survivors": int(histogram[len(constants)]),
            "direct_replays": direct_replays,
        },
        "reference_run": {
            "date": "2026-07-24",
            "python": (
                "/Users/alec/Documents/Math/tmp/hadamard-env/bin/python"
            ),
            "thread_limits": (
                "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "
                "VECLIB_MAXIMUM_THREADS=1"
            ),
            "wall_seconds": 2.06,
            "user_seconds": 1.82,
            "system_seconds": 0.03,
            "maximum_resident_set_bytes": 98_156_544,
            "peak_memory_footprint_bytes": 84_886_008,
        },
        "conclusion": (
            "Every member of the complete rank-one antipodal quadratic-"
            "center family fails the second placement digit; the best "
            "members satisfy 16 of 18 active equations."
        ),
    }
    certificate["semantic_sha256"] = compact_hash(certificate)
    return certificate


def main() -> None:
    certificate = build_certificate()
    pinned = json.loads(PINNED_CERTIFICATE.read_text())
    if compact_hash(certificate) != compact_hash(pinned):
        raise AssertionError("pinned conic rank-one certificate changed")
    print(
        "complete_h0_orbits="
        f"{certificate['classification']['complete_h0_orbits']}"
    )
    print(
        "projective_shapes="
        f"{certificate['family']['shared_projective_shapes']}"
    )
    first = certificate["first_layer"]
    print(
        "canonical_coefficient_point_incidences="
        f"{first['canonical_coefficient_point_incidences']}"
    )
    print(
        f"unique_physical_placements={first['unique_physical_placements']}"
    )
    second_layer = certificate["second_layer"]
    print(
        f"maximum_zero_equations={second_layer['maximum_zero_equations']}/"
        f"{second_layer['active_equations']}"
    )
    print(
        "exact_digit_two_survivors="
        f"{second_layer['exact_digit_two_survivors']}"
    )
    print(f"semantic_sha256={certificate['semantic_sha256']}")
    print("PASS: rank-one antipodal quadratic-center family excluded")
    print("STATUS: structured obstruction only; no LP(333) or H(668)")


if __name__ == "__main__":
    main()
