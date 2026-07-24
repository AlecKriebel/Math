#!/usr/bin/env python3
"""Exact minimum-antisymmetric-weight census for the h=0 profile.

The first placement affine space splits into 21 symmetric and 15
antisymmetric coordinates under the profile half-turn.  In the natural 27
opposite-class pairs, the antisymmetric space is a ternary [27,15,4] code.
This verifier exhausts that code, then exhausts the complete second-digit
slice above each of its six minimum words.

NumPy is used only for batched exact arithmetic on small integers.  Every
emitted point is independently replayed through the repository's exact
Eisenstein evaluator and exact row-margin corpus.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys
from typing import Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
HALFTURN_ROOT = SEARCH_ROOT / "h0_halfturn_twists"
PHASE_ROOT = SEARCH_ROOT / "phase_second_digit"
sys.path.insert(0, str(HALFTURN_ROOT))
sys.path.insert(0, str(PHASE_ROOT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_h0_halfturn_twists as halfturn  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    first_digit_equations,
    matrix_rank,
    profiles_from_ids,
)
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
    phase_sums_from_masks,
)
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
)


EXPECTED_WEIGHT_HISTOGRAM = {
    0: 1,
    4: 6,
    5: 14,
    6: 98,
    7: 264,
    8: 1_876,
    9: 5_050,
    10: 19_030,
    11: 50_146,
    12: 133_618,
    13: 299_518,
    14: 612_210,
    15: 1_064_784,
    16: 1_616_746,
    17: 2_096_168,
    18: 2_322_302,
    19: 2_194_142,
    20: 1_741_610,
    21: 1_156_748,
    22: 631_994,
    23: 279_226,
    24: 95_704,
    25: 23_456,
    26: 3_906,
    27: 290,
}

EXPECTED_MINIMUM_COORDINATES = (
    (0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 2, 0, 1, 0, 0, 2, 1, 0, 0, 0, 0),
    (0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 0, 2, 0, 0, 1, 2, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1),
    (0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2),
)

EXPECTED_WEIGHT_FIVE_COORDINATES = (
    (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0),
    (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0),
    (0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1),
)

EXPECTED_SLICE_RECORDS = (
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 22,
        "digit_three_histogram": {
            9: 1, 10: 1, 11: 2, 12: 3, 13: 8,
            14: 2, 15: 2, 16: 2, 17: 1,
        },
    },
    {
        "odd_rank": 5,
        "affine_dimension": 16,
        "digit_two_points": 87,
        "digit_three_histogram": {
            6: 1, 8: 1, 9: 4, 10: 3, 11: 17, 12: 16,
            13: 16, 14: 14, 15: 9, 16: 6,
        },
    },
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 22,
        "digit_three_histogram": {
            9: 1, 10: 1, 11: 2, 12: 3, 13: 8,
            14: 2, 15: 2, 16: 2, 17: 1,
        },
    },
    {
        "odd_rank": 5,
        "affine_dimension": 16,
        "digit_two_points": 87,
        "digit_three_histogram": {
            6: 1, 8: 1, 9: 4, 10: 3, 11: 17, 12: 16,
            13: 16, 14: 14, 15: 9, 16: 6,
        },
    },
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 24,
        "digit_three_histogram": {
            6: 1, 8: 2, 10: 2, 11: 4, 12: 4, 13: 5,
            14: 3, 15: 1, 16: 1, 17: 1,
        },
    },
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 24,
        "digit_three_histogram": {
            6: 1, 8: 2, 10: 2, 11: 4, 12: 4, 13: 5,
            14: 3, 15: 1, 16: 1, 17: 1,
        },
    },
)

EXPECTED_WEIGHT_FIVE_RECORDS = (
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 36,
        "digit_three_histogram": {
            8: 1, 9: 1, 10: 5, 11: 7, 12: 9,
            13: 4, 14: 7, 15: 2,
        },
    },
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 27,
        "digit_three_histogram": {
            10: 4, 11: 2, 12: 6, 13: 5, 14: 2,
            15: 6, 16: 1, 19: 1,
        },
    },
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 27,
        "digit_three_histogram": {
            7: 1, 10: 1, 11: 6, 12: 3, 13: 4,
            14: 7, 15: 4, 16: 1,
        },
    },
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 25,
        "digit_three_histogram": {
            10: 2, 11: 2, 12: 5, 13: 6, 14: 5,
            15: 3, 16: 1, 17: 1,
        },
    },
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 19,
        "digit_three_histogram": {
            10: 3, 11: 2, 12: 4, 13: 4, 14: 3,
            15: 2, 16: 1,
        },
    },
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 36,
        "digit_three_histogram": {
            8: 1, 10: 2, 11: 2, 12: 5, 13: 12,
            14: 7, 15: 5, 16: 1, 18: 1,
        },
    },
    {
        "odd_rank": 6,
        "affine_dimension": 15,
        "digit_two_points": 26,
        "digit_three_histogram": {
            9: 1, 10: 1, 11: 3, 12: 4, 13: 5,
            14: 7, 15: 2, 16: 2, 17: 1,
        },
    },
)

PINNED_ROW_MARGIN_TARGET = 34
PINNED_ROW_MARGIN_PLACEMENT = (
    0, 1, 1, 0, 1, 2, 2, 0, 2, 0, 2, 0, 0, 0, 1, 1, 0, 1,
    2, 2, 0, 2, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 2, 0, 1,
    0, 0, 0, 2, 1, 0, 0, 1, 0, 2, 1, 2, 1, 0, 0, 0, 0, 2,
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def flattened_phase_sums(
    profiles: Sequence[Sequence[Sequence[int]]],
    point: Sequence[int],
) -> tuple[int, ...]:
    masks = second.masks_from_trits(profiles, point)
    return tuple(
        coordinate
        for channel in phase_sums_from_masks(*masks)
        for value in channel
        for coordinate in value
    )


def phase_sum_affine_data(
    profiles: Sequence[Sequence[Sequence[int]]],
) -> tuple[tuple[int, ...], tuple[tuple[tuple[int, ...], ...], ...]]:
    """Derive the separable twelve-coordinate phase-sum table exactly."""

    variable_count = len(active_trit_coordinates(profiles))
    zero = (0,) * variable_count
    baseline = flattened_phase_sums(profiles, zero)
    effects = []
    for index in range(variable_count):
        values = [baseline]
        for value in (1, 2):
            point = list(zero)
            point[index] = value
            values.append(flattened_phase_sums(profiles, tuple(point)))
        effects.append(tuple(values))
    return baseline, tuple(effects)


def reconstruct_halfturn_data() -> dict[str, object]:
    profiles = profiles_from_ids(
        halfturn.PROFILE_IDS_A,
        halfturn.PROFILE_IDS_B,
    )
    coordinates = active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    involution = tuple(
        coordinate_index[(channel, (class_index + 6) % 12, residue)]
        for channel, class_index, residue in coordinates
    )
    first_rows = augmented_system(first_digit_equations(profiles))
    coefficient_rows = tuple(row[:-1] for row in first_rows)
    fixed_rows = tuple(
        tuple(
            (
                1
                if column == index
                else -1
                if column == involution[index]
                else 0
            )
            % 3
            for column in range(54)
        )
        for index in range(54)
    )
    anti_rows = tuple(
        tuple(
            (
                1
                if column == index
                else 1
                if column == involution[index]
                else 0
            )
            % 3
            for column in range(54)
        )
        for index in range(54)
    )
    fixed_basis = second.nullspace_basis(
        coefficient_rows + fixed_rows,
        columns=54,
    )
    anti_basis = second.nullspace_basis(
        coefficient_rows + anti_rows,
        columns=54,
    )
    if (len(fixed_basis), len(anti_basis)) != (21, 15):
        raise AssertionError("the half-turn eigenspaces changed")
    eigenbasis = fixed_basis + anti_basis
    if matrix_rank(eigenbasis) != 36:
        raise AssertionError("the eigenspaces no longer span the lift")

    origin = canonical_solution(first_rows, 54)
    if origin is None:
        raise AssertionError("the first placement digit became inconsistent")
    fixed_origin = tuple(
        2 * (int(origin[index]) + int(origin[involution[index]])) % 3
        for index in range(54)
    )
    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles),
        fixed_origin,
        eigenbasis,
    )
    if any(
        int(polar[left][right]) != int(polar[right][left])
        for polar in polars
        for left in range(36)
        for right in range(36)
    ):
        raise AssertionError("a second-digit polar matrix lost symmetry")
    minus_forms = tuple(
        halfturn.combine_quadratics(
            constants,
            linears,
            polars,
            (8 + index, 14 + index),
            (1, 2),
        )
        for index in range(6)
    )
    for constant, linear, polar in minus_forms:
        if (
            int(constant)
            or any(map(int, linear[:21]))
            or any(
                int(polar[left][right])
                for left in range(21)
                for right in range(21)
            )
            or any(
                int(polar[left][right])
                for left in range(21, 36)
                for right in range(21, 36)
            )
        ):
            raise AssertionError(
                "an odd equation is not purely bilinear plus anti-linear"
            )
    return {
        "profiles": profiles,
        "coordinates": coordinates,
        "coordinate_index": coordinate_index,
        "involution": involution,
        "fixed_basis": fixed_basis,
        "anti_basis": anti_basis,
        "eigenbasis": eigenbasis,
        "fixed_origin": fixed_origin,
        "constants": constants,
        "linears": linears,
        "polars": polars,
        "minus_forms": minus_forms,
    }


def anti_code_census(
    data: dict[str, object],
    chunk_size: int = 300_000,
) -> tuple[
    dict[int, int],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[object, ...],
]:
    coordinates = data["coordinates"]
    coordinate_index = data["coordinate_index"]
    anti_basis = data["anti_basis"]
    if not isinstance(coordinates, tuple) or not isinstance(
        coordinate_index, dict
    ) or not isinstance(anti_basis, tuple):
        raise AssertionError("the reconstructed half-turn data has wrong types")

    pair_coordinates = tuple(
        coordinate for coordinate in coordinates if coordinate[1] < 6
    )
    if len(pair_coordinates) != 27:
        raise AssertionError("the natural pair coordinate count changed")
    pair_indices = tuple(
        int(coordinate_index[coordinate]) for coordinate in pair_coordinates
    )
    generator = np.asarray(
        tuple(
            tuple(int(vector[index]) for index in pair_indices)
            for vector in anti_basis
        ),
        dtype=np.int16,
    )
    if generator.shape != (15, 27):
        raise AssertionError("the anti-code generator shape changed")

    powers = 3 ** np.arange(15, dtype=np.int64)
    histogram = np.zeros(28, dtype=np.int64)
    minimum_weight = 28
    minimum_coordinates: list[tuple[int, ...]] = []
    weight_five_coordinates: list[tuple[int, ...]] = []
    for lower in range(0, 3**15, chunk_size):
        numbers = np.arange(
            lower,
            min(lower + chunk_size, 3**15),
            dtype=np.int64,
        )
        coefficients = (
            (numbers[:, None] // powers[None, :]) % 3
        ).astype(np.int16)
        words = (coefficients @ generator) % 3
        weights = np.count_nonzero(words, axis=1)
        histogram += np.bincount(weights, minlength=28)
        positive = weights[weights > 0]
        if not positive.size:
            continue
        local_minimum = int(positive.min())
        if local_minimum < minimum_weight:
            minimum_weight = local_minimum
            minimum_coordinates = []
        if local_minimum == minimum_weight:
            minimum_coordinates.extend(
                tuple(map(int, coefficients[index]))
                for index in np.flatnonzero(weights == minimum_weight)
            )
        for index in np.flatnonzero(weights == 5):
            word = words[index]
            first_nonzero = int(word[np.flatnonzero(word)[0]])
            if first_nonzero == 1:
                weight_five_coordinates.append(
                    tuple(map(int, coefficients[index]))
                )

    result = {
        weight: int(count)
        for weight, count in enumerate(histogram)
        if int(count)
    }
    if result != EXPECTED_WEIGHT_HISTOGRAM:
        raise AssertionError("the complete anti-code weight census changed")
    if sum(result.values()) != 3**15:
        raise AssertionError("the anti-code census lost a word")
    minimum_tuple = tuple(minimum_coordinates)
    if minimum_tuple != EXPECTED_MINIMUM_COORDINATES:
        raise AssertionError("the six minimum anti words changed")
    weight_five_tuple = tuple(weight_five_coordinates)
    if weight_five_tuple != EXPECTED_WEIGHT_FIVE_COORDINATES:
        raise AssertionError("the seven weight-five directions changed")
    return (
        result,
        minimum_tuple,
        weight_five_tuple,
        pair_coordinates,
    )


def natural_pair_model(data: dict[str, object]) -> dict[str, object]:
    """Build the two length-27 eigencodes and the six row-margin blocks."""

    profiles = data["profiles"]
    coordinates = data["coordinates"]
    coordinate_index = data["coordinate_index"]
    fixed_basis = data["fixed_basis"]
    anti_basis = data["anti_basis"]
    fixed_origin = data["fixed_origin"]
    if not all(
        isinstance(value, tuple)
        for value in (
            profiles,
            coordinates,
            fixed_basis,
            anti_basis,
            fixed_origin,
        )
    ) or not isinstance(coordinate_index, dict):
        raise AssertionError("the natural pair data has wrong types")

    pair_coordinates = tuple(
        coordinate for coordinate in coordinates if coordinate[1] < 6
    )
    first_indices = tuple(
        int(coordinate_index[coordinate])
        for coordinate in pair_coordinates
    )
    second_indices = tuple(
        int(
            coordinate_index[
                (coordinate[0], coordinate[1] + 6, coordinate[2])
            ]
        )
        for coordinate in pair_coordinates
    )
    fixed_generator = tuple(
        tuple(int(vector[index]) for index in first_indices)
        for vector in fixed_basis
    )
    anti_generator = tuple(
        tuple(int(vector[index]) for index in first_indices)
        for vector in anti_basis
    )
    parity_check = second.nullspace_basis(
        fixed_generator,
        columns=27,
    )
    if (
        matrix_rank(fixed_generator),
        len(parity_check),
        matrix_rank(parity_check),
    ) != (21, 6, 6):
        raise AssertionError("the fixed eigencode dimensions changed")
    if matrix_rank(anti_generator) != 15:
        raise AssertionError(
            "the anti eigenspace projection is not injective"
        )
    if any(
        sum(row[index] * check[index] for index in range(27)) % 3
        for row in fixed_generator
        for check in parity_check
    ):
        raise AssertionError("the fixed-code parity check changed")

    natural_origin = tuple(
        int(fixed_origin[index]) for index in first_indices
    )
    if any(
        int(fixed_origin[first]) != int(fixed_origin[second_index])
        for first, second_index in zip(first_indices, second_indices)
    ):
        raise AssertionError("the chosen affine origin lost its half-turn")

    baseline, effects = phase_sum_affine_data(profiles)
    baseline_array = np.asarray(baseline, dtype=np.int16)
    effects_array = np.asarray(effects, dtype=np.int16)
    deltas = effects_array - baseline_array[None, None, :]
    groups: dict[int, list[int]] = defaultdict(list)
    for pair_index, (first, second_index) in enumerate(
        zip(first_indices, second_indices)
    ):
        touched: set[int] = set()
        for first_value in range(3):
            for second_value in range(3):
                touched.update(
                    map(
                        int,
                        np.flatnonzero(
                            deltas[first, first_value]
                            + deltas[second_index, second_value]
                        ),
                    )
                )
        touched_tuple = tuple(sorted(touched))
        if (
            len(touched_tuple) != 2
            or touched_tuple[0] % 2
            or touched_tuple[1] != touched_tuple[0] + 1
        ):
            raise AssertionError("a pair crossed row-margin blocks")
        groups[touched_tuple[0] // 2].append(pair_index)
    normalized_groups = tuple(tuple(groups[index]) for index in range(6))
    if tuple(map(len, normalized_groups)) != (3, 4, 6, 4, 4, 6):
        raise AssertionError("the six row-margin group sizes changed")

    return {
        "pair_coordinates": pair_coordinates,
        "first_indices": first_indices,
        "second_indices": second_indices,
        "fixed_generator": np.asarray(fixed_generator, dtype=np.int16),
        "anti_generator": np.asarray(anti_generator, dtype=np.int16),
        "parity_check": np.asarray(parity_check, dtype=np.int16),
        "natural_origin": np.asarray(natural_origin, dtype=np.int16),
        "baseline": baseline_array,
        "deltas": deltas,
        "groups": normalized_groups,
    }


def exact_syndrome_convolution(
    factors: Sequence[np.ndarray],
) -> int:
    """Return the zero coefficient of a product in Z[F_3^6]."""

    axes = tuple(range(6))
    result = np.zeros((3,) * 6, dtype=np.int64)
    result[(0,) * 6] = 1
    for factor in factors:
        reshaped = factor.reshape((3,) * 6)
        updated = np.zeros_like(result)
        for syndrome in zip(*np.nonzero(reshaped)):
            updated += int(reshaped[syndrome]) * np.roll(
                result,
                shift=syndrome,
                axis=axes,
            )
        result = updated
    return int(result[(0,) * 6])


def row_margin_precursor_count(
    pair_model: dict[str, object],
    anti_coordinates: Sequence[int],
    allowed_targets: Sequence[Sequence[int]],
) -> tuple[int, tuple[tuple[int, int], ...]]:
    """Count first-digit points above one anti word in all margin fibers."""

    anti_generator = pair_model["anti_generator"]
    parity_check = pair_model["parity_check"]
    natural_origin = pair_model["natural_origin"]
    first_indices = pair_model["first_indices"]
    second_indices = pair_model["second_indices"]
    baseline = pair_model["baseline"]
    deltas = pair_model["deltas"]
    groups = pair_model["groups"]
    if not all(
        isinstance(value, np.ndarray)
        for value in (
            anti_generator,
            parity_check,
            natural_origin,
            baseline,
            deltas,
        )
    ) or not all(
        isinstance(value, tuple)
        for value in (first_indices, second_indices, groups)
    ):
        raise AssertionError("the row-margin pair model has wrong types")

    anti_word = (
        np.asarray(anti_coordinates, dtype=np.int16) @ anti_generator
    ) % 3
    tables: list[dict[tuple[int, int], np.ndarray]] = []
    for group_index, pair_group in enumerate(groups):
        table: dict[tuple[int, int], np.ndarray] = defaultdict(
            lambda: np.zeros(3**6, dtype=np.int64)
        )
        for symmetric_values in product(
            range(3), repeat=len(pair_group)
        ):
            syndrome = np.zeros(6, dtype=np.int16)
            contribution = np.zeros(2, dtype=np.int16)
            for pair_index, symmetric in zip(
                pair_group, symmetric_values
            ):
                first_value = int(
                    (
                        natural_origin[pair_index]
                        + symmetric
                        + anti_word[pair_index]
                    )
                    % 3
                )
                second_value = int(
                    (
                        natural_origin[pair_index]
                        + symmetric
                        - anti_word[pair_index]
                    )
                    % 3
                )
                first = int(first_indices[pair_index])
                second_index = int(second_indices[pair_index])
                contribution += (
                    deltas[
                        first,
                        first_value,
                        2 * group_index : 2 * group_index + 2,
                    ]
                    + deltas[
                        second_index,
                        second_value,
                        2 * group_index : 2 * group_index + 2,
                    ]
                )
                syndrome = (
                    syndrome
                    + parity_check[:, pair_index] * symmetric
                ) % 3
            syndrome_index = int(
                np.ravel_multi_index(
                    tuple(map(int, syndrome)),
                    (3,) * 6,
                )
            )
            table[tuple(map(int, contribution))][syndrome_index] += 1
        tables.append(dict(table))

    target_hits = []
    for target_index, target in enumerate(allowed_targets):
        target_array = np.asarray(target, dtype=np.int16)
        factors = []
        for group_index in range(6):
            desired = tuple(
                map(
                    int,
                    target_array[
                        2 * group_index : 2 * group_index + 2
                    ]
                    - baseline[
                        2 * group_index : 2 * group_index + 2
                    ],
                )
            )
            factor = tables[group_index].get(desired)
            if factor is None:
                break
            factors.append(factor)
        if len(factors) != 6:
            continue
        count = exact_syndrome_convolution(factors)
        if count:
            target_hits.append((target_index, count))
    return sum(count for _, count in target_hits), tuple(target_hits)


def evaluate_quadratic(
    constant: int,
    linear: Sequence[int],
    polar: Sequence[Sequence[int]],
    point: Sequence[int],
) -> int:
    """Evaluate c+l.x+(1/2)x^T Bx in the audited polar convention."""

    return (
        int(constant)
        + sum(int(a) * int(b) for a, b in zip(linear, point))
        + 2
        * sum(
            int(point[left])
            * int(polar[left][right])
            * int(point[right])
            for left in range(len(point))
            for right in range(len(point))
        )
    ) % 3


def restrict_quadratic(
    constant: int,
    linear: Sequence[int],
    polar: Sequence[Sequence[int]],
    origin: Sequence[int],
    directions: Sequence[Sequence[int]],
) -> tuple[int, np.ndarray, np.ndarray]:
    reduced_constant = evaluate_quadratic(
        constant, linear, polar, origin
    )
    reduced_linear = tuple(
        (
            sum(
                int(linear[column]) * int(direction[column])
                for column in range(len(origin))
            )
            + sum(
                int(origin[left])
                * int(polar[left][right])
                * int(direction[right])
                for left in range(len(origin))
                for right in range(len(origin))
            )
        )
        % 3
        for direction in directions
    )
    reduced_polar = tuple(
        tuple(
            sum(
                int(directions[row][left])
                * int(polar[left][right])
                * int(directions[column][right])
                for left in range(len(origin))
                for right in range(len(origin))
            )
            % 3
            for column in range(len(directions))
        )
        for row in range(len(directions))
    )
    return (
        reduced_constant,
        np.asarray(reduced_linear, dtype=np.int16),
        np.asarray(reduced_polar, dtype=np.int16),
    )


def enumerate_slice(
    data: dict[str, object],
    anti_coordinates: Sequence[int],
    allowed_margin_sums: set[tuple[int, ...]],
    chunk_size: int = 200_000,
) -> dict[str, object]:
    profiles = data["profiles"]
    eigenbasis = data["eigenbasis"]
    fixed_origin = data["fixed_origin"]
    constants = data["constants"]
    linears = data["linears"]
    polars = data["polars"]
    minus_forms = data["minus_forms"]
    if not all(
        isinstance(value, tuple)
        for value in (
            profiles,
            eigenbasis,
            fixed_origin,
            constants,
            linears,
            polars,
            minus_forms,
        )
    ):
        raise AssertionError("the reconstructed slice data has wrong types")

    odd_rows = []
    for _, linear, polar in minus_forms:
        coefficients = tuple(
            sum(
                int(polar[column][21 + anti_index])
                * int(anti_coordinates[anti_index])
                for anti_index in range(15)
            )
            % 3
            for column in range(21)
        )
        rhs = (
            -sum(
                int(linear[21 + anti_index])
                * int(anti_coordinates[anti_index])
                for anti_index in range(15)
            )
        ) % 3
        odd_rows.append(coefficients + (rhs,))
    odd_rows_tuple = tuple(odd_rows)
    odd_rank = matrix_rank(tuple(row[:-1] for row in odd_rows_tuple))
    symmetric_origin = canonical_solution(odd_rows_tuple, 21)
    if symmetric_origin is None:
        raise AssertionError("a minimum anti slice became inconsistent")
    symmetric_basis = second.nullspace_basis(
        tuple(row[:-1] for row in odd_rows_tuple),
        columns=21,
    )
    dimension = len(symmetric_basis)
    full_origin = tuple(symmetric_origin) + tuple(anti_coordinates)
    full_directions = tuple(
        tuple(direction) + (0,) * 15
        for direction in symmetric_basis
    )
    restricted = tuple(
        restrict_quadratic(
            constants[row],
            linears[row],
            polars[row],
            full_origin,
            full_directions,
        )
        for row in halfturn.ACTIVE_SECOND_ROWS
    )
    fixtures = (
        (0,) * dimension,
        tuple(index % 3 for index in range(dimension)),
        tuple((index * index + index + 1) % 3 for index in range(dimension)),
    )
    for fixture in fixtures:
        full_point = tuple(
            (
                int(full_origin[column])
                + sum(
                    int(fixture[index])
                    * int(full_directions[index][column])
                    for index in range(dimension)
                )
            )
            % 3
            for column in range(36)
        )
        expected = tuple(
            evaluate_quadratic(
                constants[row],
                linears[row],
                polars[row],
                full_point,
            )
            for row in halfturn.ACTIVE_SECOND_ROWS
        )
        actual = tuple(
            evaluate_quadratic(
                int(constant),
                tuple(map(int, linear)),
                tuple(tuple(map(int, row)) for row in polar),
                fixture,
            )
            for constant, linear, polar in restricted
        )
        if actual != expected:
            raise AssertionError("an affine quadratic restriction changed")

    powers = 3 ** np.arange(dimension, dtype=np.int64)
    solutions: list[tuple[int, ...]] = []
    for lower in range(0, 3**dimension, chunk_size):
        numbers = np.arange(
            lower,
            min(lower + chunk_size, 3**dimension),
            dtype=np.int64,
        )
        points = (
            (numbers[:, None] // powers[None, :]) % 3
        ).astype(np.int16)
        keep = np.ones(len(points), dtype=bool)
        for constant, linear, polar in restricted:
            if not keep.any():
                break
            indices = np.flatnonzero(keep)
            active_points = points[indices]
            values = (
                int(constant)
                + active_points @ linear
                + 2
                * np.sum(
                    (active_points @ polar) * active_points,
                    axis=1,
                )
            ) % 3
            keep[indices[values != 0]] = False
        solutions.extend(
            tuple(map(int, point)) for point in points[keep]
        )

    digit_three_histogram: Counter[int] = Counter()
    row_margin_points = 0
    term_data = second.second_digit_term_data(profiles)
    for solution in solutions:
        symmetric = tuple(
            (
                int(symmetric_origin[column])
                + sum(
                    int(solution[index])
                    * int(symmetric_basis[index][column])
                    for index in range(dimension)
                )
            )
            % 3
            for column in range(21)
        )
        eigen_coordinates = symmetric + tuple(anti_coordinates)
        placement = second.lift_affine_point(
            fixed_origin,
            eigenbasis,
            eigen_coordinates,
        )
        if second.symbolic_second_digits(
            term_data, placement
        ) != (0,) * 20:
            raise AssertionError("a reduced point failed symbolic replay")
        if second.direct_second_digits(
            profiles, placement
        ) != (0,) * 20:
            raise AssertionError("a reduced point failed direct replay")
        flattened = flattened_phase_sums(profiles, placement)
        row_margin_points += int(flattened in allowed_margin_sums)
        digits = tuple(
            second.lambda_digits(value, 10)
            for value in second.displayed_values(profiles, placement)
        )
        digit_three_histogram[
            sum(int(row[3] != 0) for row in digits)
        ] += 1

    return {
        "odd_rank": odd_rank,
        "affine_dimension": dimension,
        "digit_two_points": len(solutions),
        "row_margin_compatible_points": row_margin_points,
        "digit_three_histogram": dict(sorted(digit_three_histogram.items())),
    }


def verify() -> dict[str, object]:
    data = reconstruct_halfturn_data()
    (
        weight_histogram,
        minimum_words,
        weight_five_directions,
        pair_coordinates,
    ) = anti_code_census(data)
    catalog = catalog_phase_sum_intersection(
        halfturn.PROFILE_IDS_A,
        halfturn.PROFILE_IDS_B,
    )
    allowed_margin_targets = tuple(
        tuple(
            coordinate
            for channel in sums
            for value in channel
            for coordinate in value
        )
        for sums, _ in catalog["phase_sum_corpus"]
    )
    allowed_margin_sums = set(allowed_margin_targets)
    if (
        len(allowed_margin_sums) != 72
        or len(allowed_margin_targets) != 72
    ):
        raise AssertionError("the exact row-margin corpus changed")

    pair_model = natural_pair_model(data)
    symmetric_precursor_count, symmetric_hits = (
        row_margin_precursor_count(
            pair_model,
            (0,) * 15,
            allowed_margin_targets,
        )
    )
    if symmetric_precursor_count or symmetric_hits:
        raise AssertionError(
            "the exact row margins entered the symmetric half-turn fiber"
        )
    minimum_precursor_results = tuple(
        row_margin_precursor_count(
            pair_model,
            minimum_word,
            allowed_margin_targets,
        )
        for minimum_word in minimum_words
    )
    expected_precursor_counts = (0, 7_346, 0, 7_346, 0, 0)
    if tuple(
        count for count, _ in minimum_precursor_results
    ) != expected_precursor_counts:
        raise AssertionError("the minimum-word row-margin counts changed")
    expected_precursor_hits = (
        (),
        ((PINNED_ROW_MARGIN_TARGET, 7_346),),
        (),
        ((PINNED_ROW_MARGIN_TARGET, 7_346),),
        (),
        (),
    )
    if tuple(
        hits for _, hits in minimum_precursor_results
    ) != expected_precursor_hits:
        raise AssertionError("the minimum-word row-margin targets changed")

    profiles = data["profiles"]
    if not isinstance(profiles, tuple):
        raise AssertionError("the profile data has the wrong type")
    first_equations = second.first_digit_equations(profiles)
    if second.symbolic_first_digits(
        first_equations,
        PINNED_ROW_MARGIN_PLACEMENT,
    ) != (0,) * 20:
        raise AssertionError("the pinned row-margin point left digit one")
    if flattened_phase_sums(
        profiles,
        PINNED_ROW_MARGIN_PLACEMENT,
    ) != allowed_margin_targets[PINNED_ROW_MARGIN_TARGET]:
        raise AssertionError("the pinned point left row-margin target 34")
    first_indices = pair_model["first_indices"]
    second_indices = pair_model["second_indices"]
    anti_generator = pair_model["anti_generator"]
    if not isinstance(first_indices, tuple) or not isinstance(
        second_indices, tuple
    ) or not isinstance(anti_generator, np.ndarray):
        raise AssertionError("the pinned pair model has wrong types")
    pinned_anti_word = (
        np.asarray(minimum_words[1], dtype=np.int16) @ anti_generator
    ) % 3
    recovered_anti_word = np.asarray(
        tuple(
            2
            * (
                PINNED_ROW_MARGIN_PLACEMENT[first]
                - PINNED_ROW_MARGIN_PLACEMENT[second_index]
            )
            % 3
            for first, second_index in zip(first_indices, second_indices)
        ),
        dtype=np.int16,
    )
    if not np.array_equal(pinned_anti_word, recovered_anti_word):
        raise AssertionError("the pinned point left its minimum anti word")

    records = tuple(
        enumerate_slice(data, minimum_word, allowed_margin_sums)
        for minimum_word in minimum_words
    )
    stripped_records = tuple(
        {
            key: value
            for key, value in record.items()
            if key != "row_margin_compatible_points"
        }
        for record in records
    )
    if stripped_records != EXPECTED_SLICE_RECORDS:
        raise AssertionError("a minimum anti slice census changed")
    if any(record["row_margin_compatible_points"] for record in records):
        raise AssertionError("a minimum anti point entered a row-margin fiber")
    total_digit_two = sum(
        int(record["digit_two_points"]) for record in records
    )
    if total_digit_two != 266:
        raise AssertionError("the total minimum-family census changed")
    minimum_digit_three_defect = min(
        min(record["digit_three_histogram"])
        for record in records
    )
    if minimum_digit_three_defect != 6:
        raise AssertionError("the minimum digit-three defect changed")

    weight_five_records = tuple(
        enumerate_slice(data, direction, allowed_margin_sums)
        for direction in weight_five_directions
    )
    stripped_weight_five_records = tuple(
        {
            key: value
            for key, value in record.items()
            if key != "row_margin_compatible_points"
        }
        for record in weight_five_records
    )
    if stripped_weight_five_records != EXPECTED_WEIGHT_FIVE_RECORDS:
        raise AssertionError("a weight-five anti slice census changed")
    if any(
        record["row_margin_compatible_points"]
        for record in weight_five_records
    ):
        raise AssertionError("a weight-five point entered a row-margin fiber")
    weight_five_projective_digit_two = sum(
        int(record["digit_two_points"])
        for record in weight_five_records
    )
    if weight_five_projective_digit_two != 196:
        raise AssertionError("the weight-five digit-two total changed")
    weight_five_minimum_digit_three_defect = min(
        min(record["digit_three_histogram"])
        for record in weight_five_records
    )
    if weight_five_minimum_digit_three_defect != 7:
        raise AssertionError("the weight-five digit-three defect changed")

    minimum_supports = tuple(
        tuple(
            pair_coordinates[index]
            for index, value in enumerate(
                (
                    np.asarray(minimum_word, dtype=np.int16)
                    @ np.asarray(
                        tuple(
                            tuple(
                                int(vector[
                                    data["coordinate_index"][coordinate]
                                ])
                                for coordinate in pair_coordinates
                            )
                            for vector in data["anti_basis"]
                        ),
                        dtype=np.int16,
                    )
                )
                % 3
            )
            if int(value)
        )
        for minimum_word in minimum_words
    )
    result = {
        "schema": "lp333-h0-minimum-anti-code-v1",
        "anti_code_parameters": (27, 15, 4),
        "anti_code_words": 3**15,
        "weight_histogram": weight_histogram,
        "minimum_words": len(minimum_words),
        "projective_minimum_directions": len(minimum_words) // 2,
        "minimum_supports": minimum_supports,
        "symmetric_row_margin_precursors": symmetric_precursor_count,
        "minimum_word_row_margin_precursors": expected_precursor_counts,
        "minimum_word_row_margin_target_hits": expected_precursor_hits,
        "pinned_row_margin_target": PINNED_ROW_MARGIN_TARGET,
        "pinned_row_margin_placement_sha256": compact_hash(
            PINNED_ROW_MARGIN_PLACEMENT
        ),
        "slice_records": records,
        "total_digit_two_points": total_digit_two,
        "row_margin_compatible_points": 0,
        "minimum_digit_three_defect": minimum_digit_three_defect,
        "weight_five_projective_directions": len(
            weight_five_directions
        ),
        "weight_five_records": weight_five_records,
        "weight_five_signed_digit_two_points": (
            2 * weight_five_projective_digit_two
        ),
        "weight_five_row_margin_compatible_points": 0,
        "weight_five_minimum_digit_three_defect": (
            weight_five_minimum_digit_three_defect
        ),
        "status": (
            "the complete anti-weight four and five digit-two families "
            "fail the exact row-margin join and digit three"
        ),
    }
    return result


def main() -> None:
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"semantic_sha256={compact_hash(result)}")
    print("PASS")


if __name__ == "__main__":
    main()
