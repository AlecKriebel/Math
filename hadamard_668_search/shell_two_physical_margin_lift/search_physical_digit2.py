#!/usr/bin/env python3
"""Bounded retracted-Newton search inside one physical row-margin chart.

Unlike the earlier abundant digit-two search, this instrument fixes one
compatible exact row-margin target at the outset.  Its first nonautomatic
lambda digit is eliminated linearly, leaving 30 coordinates.  Four
structured quadrics are solved identically by a radical translation, and
Newton/tangent moves repair the remaining digit-two system while using the
*exact* six phase sums as a tie-break.

Only directly replayed digit-two points are reported.  A bounded miss is
UNKNOWN, never an exclusion.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
import time
from typing import Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
SECOND = SEARCH / "phase_second_digit"
H0 = SEARCH / "h0_new_orbits_lift_triage"
THEORY = SEARCH / "h0_orbit2_quadric_theory"
sys.path[:0] = [
    str(HERE),
    str(H0),
    str(THEORY),
    str(SECOND),
    str(SEARCH),
]

import audit_row_margin_retraction as audit  # noqa: E402
import audit_margin_digit4 as margin4  # noqa: E402
import search_retracted_newton as newton  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
import verify_phase_second_digit_pencil as pencil  # noqa: E402
from verify_lp333_order3_phase_hensel import phase_entries  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
    phase_sums_from_masks,
)
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
)
from verify_quadric_character_compression import (  # noqa: E402
    canonical_solution as solve_linear,
    nullspace_mod3,
    rank_mod3,
)


ACTIVE_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))
ROOT_COORDINATES = np.array(
    ((1, 0), (0, 1), (-1, -1)), dtype=np.int16
)
PINNED_STARTS = {
    # Found by the 6,000,000-point candidate-4/target-65 retracted scan.
    # Direct replay below is authoritative; the stochastic trajectory is not.
    (4, 65): (
        2, 2, 2, 2, 1, 2, 0, 1, 0, 2,
        0, 2, 1, 1, 2, 0, 2, 0, 0, 2,
        2, 0, 0, 1, 2, 2, 1, 0, 1, 0,
    ),
}


def compact_hash(value: object) -> str:
    return sha256(
        json.dumps(
            value, separators=(",", ":"), sort_keys=True
        ).encode("ascii")
    ).hexdigest()


def pullback_quadratics(
    constants: Sequence[int],
    linears: Sequence[Sequence[int]],
    polars: Sequence[Sequence[Sequence[int]]],
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Restrict affine quadratics through y=origin+z*basis."""

    pulled_constants = []
    pulled_linears = []
    pulled_polars = []
    for constant, linear, polar in zip(constants, linears, polars):
        pulled_constants.append(
            pencil.quadratic_value(constant, linear, polar, origin)
        )
        pulled_linears.append(
            audit.shifted_restricted_linear(
                linear, polar, origin, basis
            )
        )
        pulled_polars.append(audit.restrict_polar(polar, basis))
    return (
        np.array(pulled_constants, dtype=np.int16),
        np.array(pulled_linears, dtype=np.int16),
        np.array(pulled_polars, dtype=np.int16),
    )


def equation_basis(subset: Sequence[int]) -> np.ndarray:
    """Complete selected structured combinations to a basis of 18 rows."""

    rows = []
    for structured_index in subset:
        row = np.zeros(18, dtype=np.int16)
        row[structured_index] = 1
        row[structured_index + 6] = 1
        row[structured_index + 12] = 1
        rows.append(row)
    rank = rank_mod3(np.array(rows, dtype=np.int16))
    for index in range(18):
        row = np.zeros(18, dtype=np.int16)
        row[index] = 1
        candidate = np.array(rows + [row], dtype=np.int16)
        next_rank = rank_mod3(candidate)
        if next_rank > rank:
            rows.append(row)
            rank = next_rank
        if rank == 18:
            break
    result = np.array(rows, dtype=np.int16)
    if result.shape != (18, 18) or rank_mod3(result) != 18:
        raise AssertionError("failed to complete the equation basis")
    return result


def retraction_data(
    subset: Sequence[int],
    linears: np.ndarray,
    polars: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    radical = nullspace_mod3(polars[list(subset)].reshape(-1, 30))
    restriction = linears[list(subset)] @ radical.T % 3
    if rank_mod3(restriction) != len(subset):
        raise AssertionError("the selected four forms do not retract")
    columns = []
    for coordinate in range(len(subset)):
        target = np.zeros(len(subset), dtype=np.int16)
        target[coordinate] = 1
        coefficients = solve_linear(restriction, target)
        columns.append(coefficients @ radical % 3)
    directions = np.array(columns, dtype=np.int16).T % 3
    if np.any(
        np.einsum(
            "eij,jk->eik", polars[list(subset)], directions
        )
        % 3
    ):
        raise AssertionError("a correction left the common radical")
    if not np.array_equal(
        linears[list(subset)] @ directions % 3,
        np.eye(len(subset), dtype=np.int16),
    ):
        raise AssertionError("the correction response is not the identity")
    return radical, directions


def build_phase_sum_evaluator(
    profiles,
    placement_origin: Sequence[int],
    placement_basis: Sequence[Sequence[int]],
    target,
):
    """Return a vectorized exact six-Eisenstein-sum scorer."""

    coordinates = active_trit_coordinates(profiles)
    entries = phase_entries(profiles)
    variable_data: list[tuple[int, int, int]] = [(-1, 0, 0)] * len(
        coordinates
    )
    for channel in range(2):
        for column in range(1, 37):
            for residue in range(3):
                entry = entries[channel][column][residue]
                if entry is None or entry.variable is None:
                    continue
                data = (3 * channel + residue, entry.sign, entry.slope)
                previous = variable_data[entry.variable]
                if previous[0] >= 0 and previous != data:
                    raise AssertionError("one phase variable changed its data")
                variable_data[entry.variable] = data
    if any(group < 0 for group, _, _ in variable_data):
        raise AssertionError("an active phase variable was not found")

    zero_placement = (0,) * len(coordinates)
    base_sums = phase_sums_from_masks(
        *second.masks_from_trits(profiles, zero_placement)
    )
    base_array = np.array(
        [
            base_sums[channel][residue]
            for channel in range(2)
            for residue in range(3)
        ],
        dtype=np.int32,
    )
    target_array = np.array(
        [
            target[channel][residue]
            for channel in range(2)
            for residue in range(3)
        ],
        dtype=np.int32,
    )
    placement_origin_array = np.array(placement_origin, dtype=np.int16)
    placement_basis_array = np.array(placement_basis, dtype=np.int16)

    def phase_sums(points: np.ndarray) -> np.ndarray:
        placements = (
            placement_origin_array
            + points @ placement_basis_array
        ) % 3
        result = np.broadcast_to(
            base_array, (len(points), 6, 2)
        ).copy()
        for variable, (group, sign, slope) in enumerate(variable_data):
            exponent = slope * placements[:, variable] % 3
            contribution = (
                3
                * sign
                * (
                    ROOT_COORDINATES[exponent]
                    - ROOT_COORDINATES[0]
                )
            )
            result[:, group, :] += contribution
        return result

    def score(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        difference = phase_sums(points) - target_array
        bad_groups = np.count_nonzero(
            np.any(difference != 0, axis=2), axis=1
        )
        distance = np.sum(np.abs(difference), axis=(1, 2))
        return bad_groups, distance

    # Cross-check the vectorized evaluator against the frozen mask path.
    fixtures = np.zeros((32, 30), dtype=np.int16)
    for fixture in range(1, len(fixtures)):
        fixtures[fixture] = np.array(
            [
                (
                    fixture // (3 ** (index % 4))
                    + fixture * index
                    + index * index
                )
                % 3
                for index in range(30)
            ],
            dtype=np.int16,
        )
    vector_sums = phase_sums(fixtures)
    for point, expected in zip(fixtures, vector_sums):
        placement = (
            placement_origin_array + point @ placement_basis_array
        ) % 3
        direct = phase_sums_from_masks(
            *second.masks_from_trits(
                profiles, tuple(map(int, placement))
            )
        )
        direct_array = np.array(
            [
                direct[channel][residue]
                for channel in range(2)
                for residue in range(3)
            ],
            dtype=np.int32,
        )
        if not np.array_equal(direct_array, expected):
            raise AssertionError("vectorized phase sums failed direct replay")

    return phase_sums, score


def search(
    candidate_index: int,
    target_index: int | None,
    cpu_seconds: float,
    seed: int,
    samples: int,
    random_samples: int,
) -> dict[str, object]:
    candidate = second.CANDIDATES[candidate_index]
    label, partition, aggregate, identifiers_a, identifiers_b = candidate
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
    catalog = catalog_phase_sum_intersection(identifiers_a, identifiers_b)
    targets = tuple(catalog["phase_sum_corpus"])
    if target_index is None:
        target_index = max(
            range(len(targets)), key=lambda index: int(targets[index][1])
        )
    if not 0 <= target_index < len(targets):
        raise ValueError("target index is outside this profile corpus")
    target, target_multiplicity = targets[target_index]

    margin_rows, base_sums = audit.derive_margin_digit_system(
        profiles, first_origin, first_basis
    )
    margin_constants = audit.target_constants(base_sums, target)
    target_origin = audit.affine_solution(
        margin_rows, margin_constants
    )
    margin_kernel = second.nullspace_basis(margin_rows)
    if len(margin_kernel) != 30:
        raise AssertionError("the physical chart lost dimension 30")

    pulled = pullback_quadratics(
        constants, linears, polars, target_origin, margin_kernel
    )
    q_constants = pulled[0][list(ACTIVE_ROWS)]
    q_linears = pulled[1][list(ACTIVE_ROWS)]
    q_polars = pulled[2][list(ACTIVE_ROWS)]
    g_constants, g_linears, g_polars = newton.structured_forms(
        q_constants, q_linears, q_polars
    )

    # Find the first coordinate four-subset with an exact retraction.
    subset = None
    radical = None
    directions = None
    from itertools import combinations

    for proposed in combinations(range(6), 4):
        try:
            proposed_radical, proposed_directions = retraction_data(
                proposed, g_linears, g_polars
            )
        except AssertionError:
            continue
        subset = proposed
        radical = proposed_radical
        directions = proposed_directions
        break
    if subset is None or radical is None or directions is None:
        raise AssertionError(
            "this candidate/target has no coordinate four-form retraction"
        )

    transform = equation_basis(subset)
    h_constants = transform @ q_constants % 3
    h_linears = transform @ q_linears % 3
    h_polars = np.einsum(
        "ae,eij->aij", transform, q_polars
    ) % 3

    first_origin_array = np.array(first_origin, dtype=np.int16)
    first_basis_array = np.array(first_basis, dtype=np.int16)
    target_origin_array = np.array(target_origin, dtype=np.int16)
    margin_kernel_array = np.array(margin_kernel, dtype=np.int16)
    placement_origin = (
        first_origin_array + target_origin_array @ first_basis_array
    ) % 3
    placement_basis = (
        margin_kernel_array @ first_basis_array
    ) % 3
    phase_sums, margin_score = build_phase_sum_evaluator(
        profiles, placement_origin, placement_basis, target
    )
    _, margin_quadrics, _ = margin4.derive_target_quadrics(
        profiles,
        first_origin,
        first_basis,
        margin_rows,
        margin_kernel,
        base_sums,
        target,
    )
    m_constants = np.array(margin_quadrics[0], dtype=np.int16)
    m_linears = np.array(margin_quadrics[1], dtype=np.int16)
    m_polars = np.array(margin_quadrics[2], dtype=np.int16)

    def retract(points: np.ndarray) -> np.ndarray:
        values = newton.evaluate_batch(
            g_constants[list(subset)],
            g_linears[list(subset)],
            g_polars[list(subset)],
            points,
        )
        result = (points - values @ directions.T) % 3
        if np.any(
            newton.evaluate_batch(
                g_constants[list(subset)],
                g_linears[list(subset)],
                g_polars[list(subset)],
                result,
            )
        ):
            raise AssertionError("the four-form retraction failed")
        return result

    def q_values(point: np.ndarray) -> np.ndarray:
        return newton.evaluate(
            h_constants, h_linears, h_polars, point
        )

    def replay(point: np.ndarray) -> dict[str, object]:
        y = (
            target_origin_array + point @ margin_kernel_array
        ) % 3
        placement = (
            first_origin_array + y @ first_basis_array
        ) % 3
        placement_tuple = tuple(map(int, placement))
        if second.symbolic_first_digits(
            first_equations, placement_tuple
        ) != (0,) * 20:
            raise AssertionError("a search point failed first-digit replay")
        if second.symbolic_second_digits(
            second.second_digit_term_data(profiles), placement_tuple
        ) != (0,) * 20:
            raise AssertionError("a search point failed digit-two replay")
        masks = second.masks_from_trits(profiles, placement_tuple)
        sums = phase_sums_from_masks(*masks)
        row_exact = sums == target
        values = second.displayed_values(profiles, placement_tuple)
        digits = tuple(second.lambda_digits(value, 10) for value in values)
        active_digit_three_defect = sum(
            digits[row][3] != 0 for row in ACTIVE_ROWS
        )
        active_digit_four_defect = sum(
            digits[row][4] != 0 for row in ACTIVE_ROWS
        )
        return {
            "row_margin_exact": row_exact,
            "phase_sums": sums,
            "affine_coordinates_30": tuple(map(int, point)),
            "affine_coordinates_36": tuple(map(int, y)),
            "placement_trits": placement_tuple,
            "placement_sha256": compact_hash(placement_tuple),
            "masks_a": masks[0],
            "masks_b": masks[1],
            "displayed_exact_values": values,
            "nonzero_rows_by_digit": tuple(
                sum(row[digit] != 0 for row in digits)
                for digit in range(10)
            ),
            "active_digit_three_defect": active_digit_three_defect,
            "active_digit_four_defect": active_digit_four_defect,
        }

    rng = np.random.default_rng(seed)
    started_cpu = time.process_time()
    started_wall = time.monotonic()

    def within_budget() -> bool:
        return time.process_time() - started_cpu < cpu_seconds

    exact_points = 0
    distinct_points: set[tuple[int, ...]] = set()
    exact_margin_points = []
    margin_group_histogram: Counter[int] = Counter()
    margin_digit4_histogram: Counter[int] = Counter()
    best_key = (7, 7, 10**9, 19, 19)
    best_record = None
    iterations = 0
    restarts = 0
    tangent_rounds = 0
    random_points_scanned = 0
    seed_pool: list[np.ndarray] = []
    first_targeted_sheet_audit = None

    target_array = np.array(
        [
            target[channel][residue]
            for channel in range(2)
            for residue in range(3)
        ],
        dtype=np.int32,
    )

    def record_exact(point: np.ndarray) -> None:
        nonlocal exact_points, best_key, best_record
        key = tuple(map(int, point))
        if key in distinct_points:
            return
        distinct_points.add(key)
        exact_points += 1
        record = replay(point)
        difference = np.array(
            [
                record["phase_sums"][channel][residue]
                for channel in range(2)
                for residue in range(3)
            ],
            dtype=np.int32,
        ) - target_array
        bad_groups = int(
            np.count_nonzero(np.any(difference != 0, axis=1))
        )
        distance = int(np.sum(np.abs(difference)))
        margin_digit4_values = newton.evaluate(
            m_constants, m_linears, m_polars, point
        )
        margin_digit4_defect = int(
            np.count_nonzero(margin_digit4_values)
        )
        margin_group_histogram[bad_groups] += 1
        margin_digit4_histogram[margin_digit4_defect] += 1
        score = (
            margin_digit4_defect,
            bad_groups,
            distance,
            int(record["active_digit_three_defect"]),
            int(record["active_digit_four_defect"]),
        )
        record["margin_digit4_residuals"] = tuple(
            map(int, margin_digit4_values)
        )
        record["margin_digit4_defect"] = margin_digit4_defect
        q_jacobian = (
            h_linears + np.einsum("eij,j->ei", h_polars, point)
        ) % 3
        tangent = nullspace_mod3(q_jacobian)
        margin_jacobian = (
            m_linears + np.einsum("eij,j->ei", m_polars, point)
        ) % 3
        restricted = margin_jacobian @ tangent.T % 3
        record["digit2_jacobian_rank"] = int(rank_mod3(q_jacobian))
        record["digit2_tangent_dimension"] = len(tangent)
        record["margin_digit4_tangent_rank"] = int(
            rank_mod3(restricted)
        )
        record["margin_digit4_linearized_correction_consistent"] = (
            newton.affine_solve(
                restricted, -margin_digit4_values
            )
            is not None
        )
        if score < best_key:
            best_key = score
            best_record = record
        if record["row_margin_exact"]:
            exact_margin_points.append(record)

    pinned = PINNED_STARTS.get((candidate_index, target_index))
    if pinned is not None:
        pinned_point = np.array(pinned, dtype=np.int16)
        if np.any(q_values(pinned_point)):
            raise AssertionError("the pinned physical-chart seed left digit 2")
        record_exact(pinned_point)
        seed_pool.append(pinned_point)

    # A direct random scan on the exact four-form zero set has neutral hit
    # probability 3^-14 for the remaining basis rows.  It provides unbiased
    # seeds for the manifold walk and a measured rate, rather than relying
    # entirely on Newton convergence.
    remaining_random = max(0, int(random_samples))
    while remaining_random and within_budget():
        batch_size = min(20_000, remaining_random)
        batch = retract(
            rng.integers(
                0, 3, size=(batch_size, 30), dtype=np.int16
            )
        )
        residuals = newton.evaluate_batch(
            h_constants[len(subset):],
            h_linears[len(subset):],
            h_polars[len(subset):],
            batch,
        )
        hits = np.flatnonzero(np.all(residuals == 0, axis=1))
        for hit in hits:
            point = batch[int(hit)].copy()
            record_exact(point)
            seed_pool.append(point)
        random_points_scanned += batch_size
        remaining_random -= batch_size

    while within_budget():
        if seed_pool:
            point = seed_pool[restarts % len(seed_pool)].copy()
        else:
            point = retract(
                rng.integers(0, 3, size=(1, 30), dtype=np.int16)
            )[0]
        tangent_steps = 0
        for _ in range(140):
            if not within_budget():
                break
            values = q_values(point)
            defect = int(np.count_nonzero(values))
            if defect == 0:
                record_exact(point)
                if exact_margin_points and not int(
                    exact_margin_points[-1]["active_digit_three_defect"]
                ):
                    break

                # Move in the tangent space, then let Newton restore.
                jacobian = (
                    h_linears
                    + np.einsum("eij,j->ei", h_polars, point)
                ) % 3
                tangent = nullspace_mod3(jacobian)
                margin_values = newton.evaluate(
                    m_constants, m_linears, m_polars, point
                )
                margin_jacobian = (
                    m_linears
                    + np.einsum("eij,j->ei", m_polars, point)
                ) % 3
                restricted = margin_jacobian @ tangent.T % 3
                targeted = newton.affine_solve(
                    restricted, -margin_values
                )
                coefficient_blocks = []
                targeted_count = 0
                targeted_dimension = 0
                exhaustive_targeted_sheet = False
                if targeted is not None:
                    particular, kernel = targeted
                    targeted_dimension = len(kernel)
                    sheet_size = 3 ** len(kernel)
                    if sheet_size <= 10_000:
                        exhaustive_targeted_sheet = True
                        indices = np.arange(
                            sheet_size, dtype=np.int64
                        )[:, None]
                        powers = (
                            3 ** np.arange(len(kernel), dtype=np.int64)
                        )[None, :]
                        weights = (
                            indices // powers % 3
                        ).astype(np.int16)
                    else:
                        count = max(1, samples // 2)
                        weights = rng.integers(
                            0,
                            3,
                            size=(count, len(kernel)),
                            dtype=np.int16,
                        )
                    coefficient_blocks.append(
                        (particular + weights @ kernel) % 3
                    )
                    targeted_count = len(coefficient_blocks[-1])
                random_count = max(
                    0,
                    samples
                    - sum(len(block) for block in coefficient_blocks),
                )
                if random_count:
                    coefficient_blocks.append(
                        rng.integers(
                            0,
                            3,
                            size=(random_count, len(tangent)),
                            dtype=np.int16,
                        )
                    )
                coefficients = np.vstack(coefficient_blocks)
                candidates = retract(
                    (point + coefficients @ tangent) % 3
                )
                tangent_steps += 1
                tangent_rounds += 1
            else:
                jacobian = (
                    h_linears
                    + np.einsum("eij,j->ei", h_polars, point)
                ) % 3
                solved = newton.affine_solve(jacobian, -values)
                if solved is None:
                    break
                particular, kernel = solved
                coefficients = rng.integers(
                    0, 3, size=(samples, len(kernel)), dtype=np.int16
                )
                deltas = (particular + coefficients @ kernel) % 3
                candidates = retract((point + deltas) % 3)

            residuals = newton.evaluate_batch(
                h_constants, h_linears, h_polars, candidates
            )
            q_scores = np.count_nonzero(residuals, axis=1)
            if (
                defect == 0
                and exhaustive_targeted_sheet
                and first_targeted_sheet_audit is None
            ):
                sheet_margin = newton.evaluate_batch(
                    m_constants,
                    m_linears,
                    m_polars,
                    candidates[:targeted_count],
                )
                sheet_margin_scores = np.count_nonzero(
                    sheet_margin, axis=1
                )
                sheet_q_scores = q_scores[:targeted_count]
                pair_histogram = Counter(
                    zip(
                        map(int, sheet_q_scores),
                        map(int, sheet_margin_scores),
                    )
                )
                first_targeted_sheet_audit = {
                    "sheet_size": targeted_count,
                    "tangent_dimension": len(tangent),
                    "linearized_solution_dimension": targeted_dimension,
                    "digit2_defect_minimum": int(
                        sheet_q_scores.min()
                    ),
                    "margin_digit4_defect_minimum": int(
                        sheet_margin_scores.min()
                    ),
                    "joint_exact_points": int(
                        np.count_nonzero(
                            (sheet_q_scores == 0)
                            & (sheet_margin_scores == 0)
                        )
                    ),
                    "defect_pair_histogram": tuple(
                        sorted(
                            (left, right, count)
                            for (left, right), count
                            in pair_histogram.items()
                        )
                    ),
                }
            minimum = int(q_scores.min())
            choices = np.flatnonzero(q_scores == minimum)
            # The exact physical sums are only a tie-break: digit-two
            # correctness is never relaxed or conflated with the margin.
            limited = choices[: min(128, len(choices))]
            groups, distances = margin_score(candidates[limited])
            margin4_values = newton.evaluate_batch(
                m_constants, m_linears, m_polars, candidates[limited]
            )
            margin4_scores = np.count_nonzero(
                margin4_values, axis=1
            )
            order = np.lexsort((distances, groups, margin4_scores))
            point = candidates[int(limited[int(order[0])])]
            iterations += 1
            if tangent_steps >= 8 and minimum > 0:
                break
        restarts += 1
        if exact_margin_points and not int(
            exact_margin_points[-1]["active_digit_three_defect"]
        ):
            break

    status = (
        "SAT_DIGIT3_ROW_MARGIN"
        if exact_margin_points
        and any(
            not int(point["active_digit_three_defect"])
            for point in exact_margin_points
        )
        else "SAT_DIGIT2_ROW_MARGIN"
        if exact_margin_points
        else "UNKNOWN"
    )
    result = {
        "schema": "lp333-shell-two-physical-digit2-retracted-search-v1",
        "scope": (
            "Bounded search in one exact catalog-target chart. UNKNOWN is "
            "not an exclusion; a digit-two point is not an LP(333), "
            "Legendre pair, or H(668)."
        ),
        "status": status,
        "candidate_index": candidate_index,
        "label": label,
        "partition": partition,
        "aggregate": aggregate,
        "target_index": target_index,
        "target_phase_sums": target,
        "target_raw_assignment_multiplicity": int(target_multiplicity),
        "row_margin_linear_rank": 6,
        "search_dimension": 30,
        "retraction": {
            "structured_subset": subset,
            "equations": len(subset),
            "common_radical_dimension": len(radical),
            "direction_matrix": directions.tolist(),
        },
        "search": {
            "cpu_seconds_limit": cpu_seconds,
            "cpu_seconds_used": time.process_time() - started_cpu,
            "wall_seconds_used": time.monotonic() - started_wall,
            "seed": seed,
            "samples_per_step": samples,
            "requested_random_retracted_samples": random_samples,
            "random_retracted_samples_scanned": random_points_scanned,
            "iterations": iterations,
            "restarts": restarts,
            "tangent_rounds": tangent_rounds,
            "distinct_exact_digit2_points": exact_points,
            "exact_row_margin_digit2_points": len(exact_margin_points),
            "margin_bad_group_histogram": tuple(
                sorted(margin_group_histogram.items())
            ),
            "margin_digit4_defect_histogram": tuple(
                sorted(margin_digit4_histogram.items())
            ),
            "first_targeted_tangent_sheet": first_targeted_sheet_audit,
            "best_score": best_key,
        },
        "best_record": best_record,
        "exact_margin_points": tuple(exact_margin_points),
    }
    result["semantic_sha256"] = compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, default=4, choices=range(5))
    parser.add_argument("--target", type=int)
    parser.add_argument("--cpu-seconds", type=float, default=300)
    parser.add_argument("--seed", type=int, default=668_333_4)
    parser.add_argument("--samples", type=int, default=512)
    parser.add_argument("--random-samples", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = search(
        args.candidate,
        args.target,
        args.cpu_seconds,
        args.seed,
        args.samples,
        args.random_samples,
    )
    payload = json.dumps(result, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
