#!/usr/bin/env python3
"""Exact exploratory audit of the long-case adjacent-fold orientation lift.

This is deliberately a scoped verifier.  It derives every object from the
authoritative Eliahou long-case models and makes no existence or exclusion
claim beyond the assertions executed below.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import argparse
import json
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
TRIAGE = SEARCH / "eliahou_long_block_exact_triage"
CHAR3 = SEARCH / "eliahou_char3_jet"
sys.path[:0] = [str(CHAR3), str(TRIAGE), str(SEARCH)]

import search_char3_local as local  # noqa: E402
import verify_eliahou_adjacent42_repair as adjacent  # noqa: E402
import verify_long_block_exact_triage as triage  # noqa: E402


@dataclass(frozen=True)
class SupportFixture:
    case_number: int
    profile_number: int
    support: np.ndarray


def cyclic_fold(row: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        row[cell] + (row[cell + 42] if cell + 42 < len(row) else 0)
        for cell in range(42)
    )


def positive_fold_correlations(
    rows: list[list[int]] | tuple[tuple[int, ...], ...],
) -> np.ndarray:
    folds = tuple(cyclic_fold(row) for row in rows)
    return np.asarray(
        [
            sum(
                fold[cell] * fold[(cell + lag) % 42]
                for fold in folds
                for cell in range(42)
            )
            for lag in range(1, 22)
        ],
        dtype=np.int64,
    )


def q_adjusted_original_rows(case) -> list[list[int]]:
    rows = [list(row) for row in adjacent.eliahou_base()]
    active_row = 1 if case.block == "L" else 3
    length = adjacent.LONG if case.block == "L" else adjacent.SHORT
    for coordinate in (case.index, length - 1 - case.index):
        rows[active_row][coordinate] *= -1
    return rows


def oriented_correlations(
    case,
    keys: tuple[tuple[str, int], ...],
    support: np.ndarray,
    orientations: np.ndarray | None = None,
) -> np.ndarray:
    selected = tuple(map(int, np.flatnonzero(support)))
    if orientations is None:
        orientations = np.zeros(len(selected), dtype=np.uint8)
    if len(orientations) != len(selected):
        raise ValueError("orientation vector has the wrong length")
    rows = q_adjusted_original_rows(case)
    for orientation_index, variable in enumerate(selected):
        block, cell = keys[variable]
        coordinate = cell + (42 if orientations[orientation_index] else 0)
        for row in ((0, 1) if block == "L" else (2, 3)):
            rows[row][coordinate] *= -1
    return positive_fold_correlations(rows)


def root_targets(profile) -> dict[tuple[str, int], int]:
    ordinary, alternating = profile
    return {
        ("L", 1): ordinary[0],
        ("L", -1): alternating[0],
        ("S", 1): ordinary[1],
        ("S", -1): alternating[1],
    }


def support_profile_feasible(keys, support, profile) -> bool:
    ordinary, alternating = profile
    targets = {
        ("L", 0): (ordinary[0] + alternating[0]) // 2,
        ("L", 1): (ordinary[0] - alternating[0]) // 2,
        ("S", 0): (ordinary[1] + alternating[1]) // 2,
        ("S", 1): (ordinary[1] - alternating[1]) // 2,
    }
    for block_parity, target in targets.items():
        count = sum(
            int(flag)
            for key, flag in zip(keys, support)
            if key[0] == block_parity[0]
            and key[1] % 2 == block_parity[1]
        )
        if count < abs(target) or (count - target) % 2:
            return False
    return True


def find_fixture(
    case_number: int, profile_number: int, seed: int
) -> SupportFixture:
    case, keys, _, _, _, _ = local.arrays(case_number)
    _, _, _, _, _, affine_payload, _ = (
        triage.grouped_affine_coordinates(case_number)
    )
    particular = affine_payload[0]
    basis = affine_payload[1:]
    generator = np.random.default_rng(seed)
    profile = case.profiles[profile_number]
    for _ in range(1_000_000):
        coordinates = generator.integers(
            0, 2, len(basis), dtype=np.uint8
        )
        support = particular ^ ((coordinates @ basis) & 1)
        if (
            int(support.sum()) == 39
            and support_profile_feasible(keys, support, profile)
        ):
            return SupportFixture(case_number, profile_number, support)
    raise AssertionError("failed to find a deterministic support fixture")


def root_orientation_rows(
    case, keys, support, profile
) -> tuple[np.ndarray, np.ndarray]:
    selected = tuple(map(int, np.flatnonzero(support)))
    targets = root_targets(profile)
    matrix = []
    rhs = []
    base = adjacent.eliahou_base()
    for block in ("L", "S"):
        row = np.asarray(
            [int(keys[variable][0] == block) for variable in selected],
            dtype=np.uint8,
        )
        residues = []
        seed_row = 0 if block == "L" else 2
        for root in (1, -1):
            baseline = sum(
                -base[seed_row][keys[variable][1]]
                * root ** keys[variable][1]
                for variable in selected
                if keys[variable][0] == block
            )
            target = targets[(block, root)]
            if (baseline - target) % 2:
                raise AssertionError("support failed root parity")
            residues.append(((baseline - target) // 2) & 1)
        if residues[0] != residues[1]:
            raise AssertionError("ordinary/alternating root parities split")
        matrix.append(row)
        rhs.append(residues[0])
    return np.asarray(matrix, dtype=np.uint8), np.asarray(rhs, dtype=np.uint8)


@lru_cache(maxsize=None)
def universal_mod16_orientation_matrix(case_number: int) -> np.ndarray:
    """Return the fixed 23-by-78 first orientation-lift matrix.

    The first 21 rows are the positive-fold correlation digit.  The last
    two rows are the long/short root-orientation parities.  Although a
    support chooses only 39 columns, the columns themselves do not depend
    on the other 38 selected cells.
    """

    case, keys, _, _, _, _ = local.arrays(case_number)
    columns = []
    for variable in range(len(keys)):
        support = np.zeros(len(keys), dtype=np.uint8)
        support[variable] = 1
        lower = oriented_correlations(case, keys, support)
        upper = oriented_correlations(
            case, keys, support, np.ones(1, dtype=np.uint8)
        )
        difference = upper - lower
        if np.any(difference % 8):
            raise AssertionError("universal orientation column is not integral")
        columns.append(np.remainder(difference // 8, 2))
    correlation_matrix = np.asarray(columns, dtype=np.uint8).T
    root_matrix = np.asarray(
        [
            [int(block == "L") for block, _ in keys],
            [int(block == "S") for block, _ in keys],
        ],
        dtype=np.uint8,
    )
    return np.vstack((correlation_matrix, root_matrix))


def mod16_orientation_system(
    case_number: int, profile_number: int, support: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    case, keys, _, _, _, _ = local.arrays(case_number)
    selected = tuple(map(int, np.flatnonzero(support)))
    baseline = oriented_correlations(case, keys, support)
    if np.any(baseline % 8):
        raise AssertionError("anti-mod2 support failed automatic plus mod8")
    universal = universal_mod16_orientation_matrix(case_number)
    matrix = universal[:21, selected]
    rhs = np.remainder(-baseline // 8, 2).astype(np.uint8)
    root_matrix, root_rhs = root_orientation_rows(
        case, keys, support, case.profiles[profile_number]
    )
    if not np.array_equal(root_matrix, universal[21:, selected]):
        raise AssertionError("root rows disagree with the universal matrix")
    return (
        np.vstack((matrix, root_matrix)),
        np.concatenate((rhs, root_rhs)),
    )


def quadratic_next_digit(
    fixture: SupportFixture,
) -> dict[str, object]:
    case, keys, _, _, _, _ = local.arrays(fixture.case_number)
    matrix, rhs = mod16_orientation_system(
        fixture.case_number, fixture.profile_number, fixture.support
    )
    matrix_rank = triage.rank_mod(matrix, 2)
    augmented_matrix_rank = triage.rank_mod(
        np.column_stack((matrix, rhs)), 2
    )
    support_record = [
        list(key)
        for key, flag in zip(keys, fixture.support)
        if flag
    ]
    if augmented_matrix_rank > matrix_rank:
        return {
            "case": fixture.case_number,
            "q_index": case.index,
            "profile": fixture.profile_number,
            "support": support_record,
            "mod16_system_rows": int(matrix.shape[0]),
            "mod16_rank": matrix_rank,
            "mod16_augmented_rank": augmented_matrix_rank,
            "mod16_consistent": False,
            "mod16_orientation_nullity": None,
            "mod16_orientation_points": 0,
            "mod16_plus_exact_roots_survivors": 0,
            "mod32_quadratic_coefficient_rank": None,
            "mod32_augmented_coefficient_rank": None,
            "mod32_pure_quadratic_row_rank": None,
            "mod32_linear_row_rank": None,
            "mod32_individual_polar_rank_histogram": None,
            "mod32_common_polar_radical_dimension": None,
            "mod32_xor_contradiction": None,
            "mod32_survivors": 0,
            "mod32_points": 0,
            "mod32_plus_exact_roots_survivors": 0,
            "mod64_plus_exact_roots_survivors": 0,
            "root_exact_assignment_examples": [],
            "root_group_cardinality_targets": None,
        }
    pivots, particular, basis = triage.affine_parameterization(matrix, rhs)
    dimension = len(basis)

    def value(coordinates: np.ndarray) -> np.ndarray:
        orientations = particular ^ ((coordinates @ basis) & 1)
        correlations = oriented_correlations(
            case, keys, fixture.support, orientations
        )
        if np.any(correlations % 16):
            raise AssertionError("mod-16 orientation solution failed replay")
        return np.remainder(correlations // 16, 2).astype(np.uint8)

    zero = np.zeros(dimension, dtype=np.uint8)
    constant = value(zero)
    linear = np.zeros((21, dimension), dtype=np.uint8)
    one_values = []
    for coordinate in range(dimension):
        point = zero.copy()
        point[coordinate] = 1
        current = value(point)
        one_values.append(current)
        linear[:, coordinate] = current ^ constant
    quadratic = np.zeros((21, dimension, dimension), dtype=np.uint8)
    for left in range(dimension):
        for right in range(left + 1, dimension):
            point = zero.copy()
            point[left] = point[right] = 1
            coefficient = (
                value(point)
                ^ one_values[left]
                ^ one_values[right]
                ^ constant
            )
            quadratic[:, left, right] = coefficient

    # The degree bound is algebraic: an orientation flip changes a fold
    # coefficient by a multiple of four.  Hence, after the mod-16 affine
    # layer, linear XOR terms of degree at least three carry a factor 32,
    # and quadratic orientation terms reduce to quadratic Boolean terms.
    # Random higher-weight replay guards the interpolation.
    generator = np.random.default_rng(
        668_321_000
        + 2 * fixture.case_number
        + fixture.profile_number
    )
    for _ in range(64):
        point = generator.integers(
            0, 2, dimension, dtype=np.uint8
        )
        predicted = constant ^ ((linear @ point) & 1)
        for left in np.flatnonzero(point):
            predicted ^= (quadratic[:, left] @ point) & 1
        if not np.array_equal(predicted, value(point)):
            raise AssertionError("mod-32 quadratic ANF failed replay")

    coefficient_rows = np.asarray(
        [
            [
                *map(int, linear[equation]),
                *(
                    int(quadratic[equation, left, right])
                    for left in range(dimension)
                    for right in range(left + 1, dimension)
                ),
            ]
            for equation in range(21)
        ],
        dtype=np.uint8,
    )
    quadratic_rows = np.asarray(
        [
            [
                int(quadratic[equation, left, right])
                for left in range(dimension)
                for right in range(left + 1, dimension)
            ]
            for equation in range(21)
        ],
        dtype=np.uint8,
    )
    coefficient_rank = triage.rank_mod(coefficient_rows, 2)
    augmented_rank = triage.rank_mod(
        np.column_stack((coefficient_rows, constant)), 2
    )
    quadratic_rank = triage.rank_mod(quadratic_rows, 2)
    linear_rank = triage.rank_mod(linear, 2)
    polar_matrices = np.asarray(
        [
            quadratic[equation] ^ quadratic[equation].T
            for equation in range(21)
        ],
        dtype=np.uint8,
    )
    individual_polar_ranks = [
        triage.rank_mod(matrix, 2) for matrix in polar_matrices
    ]
    common_radical_dimension = dimension - triage.rank_mod(
        polar_matrices.reshape(21 * dimension, dimension), 2
    )

    # Evaluate all points as Python integer bitsets.
    point_count = 1 << dimension
    all_points = (1 << point_count) - 1

    def variable_mask(index: int) -> int:
        block = 1 << index
        pattern = ((1 << block) - 1) << block
        result = 0
        offset = 0
        while offset < point_count:
            result |= pattern << offset
            offset += 2 * block
        return result & all_points

    variable_masks = [variable_mask(index) for index in range(dimension)]
    failed = 0
    for equation in range(21):
        truth = all_points if constant[equation] else 0
        for coordinate in range(dimension):
            if linear[equation, coordinate]:
                truth ^= variable_masks[coordinate]
        for left in range(dimension):
            for right in range(left + 1, dimension):
                if quadratic[equation, left, right]:
                    truth ^= (
                        variable_masks[left] & variable_masks[right]
                    )
        failed |= truth
    survivor_mask = all_points ^ failed
    survivors = survivor_mask.bit_count()

    selected = tuple(map(int, np.flatnonzero(fixture.support)))
    targets = root_targets(case.profiles[fixture.profile_number])
    root_exact_survivors = 0
    mod64_survivors = 0
    root_exact_examples: list[int] = []

    # Exact +1/-1 root lifting is four cardinality equations.  If
    # a_j=-seed_j is the lower-orientation support sign, put
    # n_j=e_j xor [a_j=-1].  On each block/parity group G,
    #
    #     sum_G a_j (-1)^e_j = |G|-2 wt(n|G),
    #
    # so the target t_G is equivalent to
    # wt(n|G)=(|G|-t_G)/2.
    group_masks: dict[tuple[str, int], int] = {}
    negative_masks: dict[tuple[str, int], int] = {}
    target_negative_weights: dict[tuple[str, int], int] = {}
    ordinary, alternating = case.profiles[fixture.profile_number]
    signed_group_targets = {
        ("L", 0): (ordinary[0] + alternating[0]) // 2,
        ("L", 1): (ordinary[0] - alternating[0]) // 2,
        ("S", 0): (ordinary[1] + alternating[1]) // 2,
        ("S", 1): (ordinary[1] - alternating[1]) // 2,
    }
    for block in ("L", "S"):
        seed_row = 0 if block == "L" else 2
        for parity in (0, 1):
            group = (block, parity)
            group_mask = 0
            negative_mask = 0
            for local_index, variable in enumerate(selected):
                key_block, cell = keys[variable]
                if key_block != block or cell % 2 != parity:
                    continue
                group_mask |= 1 << local_index
                if -adjacent.eliahou_base()[seed_row][cell] == -1:
                    negative_mask |= 1 << local_index
            size = group_mask.bit_count()
            target = signed_group_targets[group]
            if size < abs(target) or (size - target) % 2:
                raise AssertionError("fixture failed exact root cardinality")
            group_masks[group] = group_mask
            negative_masks[group] = negative_mask
            target_negative_weights[group] = (size - target) // 2

    particular_mask = sum(
        int(bit) << index for index, bit in enumerate(particular)
    )
    basis_masks = tuple(
        sum(int(bit) << index for index, bit in enumerate(row))
        for row in basis
    )
    exact_root_orientations_in_mod16_fiber = 0
    orientation_mask = particular_mask
    previous_gray = 0
    for integer in range(1 << dimension):
        if integer:
            gray = integer ^ (integer >> 1)
            changed = gray ^ previous_gray
            coordinate = changed.bit_length() - 1
            orientation_mask ^= basis_masks[coordinate]
            previous_gray = gray
        if all(
            (
                (orientation_mask ^ negative_masks[group])
                & group_masks[group]
            ).bit_count()
            == target_negative_weights[group]
            for group in group_masks
        ):
            exact_root_orientations_in_mod16_fiber += 1

    remaining = survivor_mask
    while remaining:
        lowest = remaining & -remaining
        assignment = lowest.bit_length() - 1
        remaining ^= lowest
        coordinates = np.asarray(
            [
                (assignment >> coordinate) & 1
                for coordinate in range(dimension)
            ],
            dtype=np.uint8,
        )
        orientations = particular ^ ((coordinates @ basis) & 1)
        root_exact = True
        for block in ("L", "S"):
            seed_row = 0 if block == "L" else 2
            for root in (1, -1):
                value_at_root = sum(
                    -adjacent.eliahou_base()[seed_row][keys[variable][1]]
                    * root ** keys[variable][1]
                    * (-1 if orientations[local_index] else 1)
                    for local_index, variable in enumerate(selected)
                    if keys[variable][0] == block
                )
                if value_at_root != targets[(block, root)]:
                    root_exact = False
        if not root_exact:
            continue
        root_exact_survivors += 1
        root_exact_examples.append(assignment)
        correlations = oriented_correlations(
            case, keys, fixture.support, orientations
        )
        if np.any(correlations % 32):
            raise AssertionError("mod-32 truth table accepted a false point")
        if not np.any(np.remainder(correlations // 32, 2)):
            mod64_survivors += 1

    # A rank jump after adjoining the constant is an explicit XOR
    # contradiction among the 21 next-digit equations.
    return {
        "case": fixture.case_number,
        "q_index": case.index,
        "profile": fixture.profile_number,
        "support": support_record,
        "mod16_system_rows": int(matrix.shape[0]),
        "mod16_rank": len(pivots),
        "mod16_augmented_rank": augmented_matrix_rank,
        "mod16_consistent": True,
        "mod16_orientation_nullity": dimension,
        "mod16_orientation_points": 1 << dimension,
        "mod16_plus_exact_roots_survivors": (
            exact_root_orientations_in_mod16_fiber
        ),
        "mod32_quadratic_coefficient_rank": coefficient_rank,
        "mod32_augmented_coefficient_rank": augmented_rank,
        "mod32_pure_quadratic_row_rank": quadratic_rank,
        "mod32_linear_row_rank": linear_rank,
        "mod32_individual_polar_rank_histogram": {
            str(rank): count
            for rank, count in sorted(Counter(individual_polar_ranks).items())
        },
        "mod32_common_polar_radical_dimension": common_radical_dimension,
        "mod32_xor_contradiction": augmented_rank > coefficient_rank,
        "mod32_survivors": survivors,
        "mod32_points": point_count,
        "mod32_plus_exact_roots_survivors": root_exact_survivors,
        "mod64_plus_exact_roots_survivors": mod64_survivors,
        "root_exact_assignment_examples": root_exact_examples[:4],
        "root_group_cardinality_targets": {
            f"{block}{parity}": target_negative_weights[(block, parity)]
            for block in ("L", "S")
            for parity in (0, 1)
        },
    }


def adjacent_mod8_redundancy_audit(case_number: int) -> dict[str, object]:
    case, keys, _, constant, linear, _ = local.arrays(case_number)
    _, _, _, _, _, affine_payload, _ = (
        triage.grouped_affine_coordinates(case_number)
    )
    particular = affine_payload[0]
    basis = affine_payload[1:]

    # Build the complete quadratic support polynomial directly at the fold
    # level.  A lower-endpoint support choice adds one two-row fold vector
    # delta_i; the upper-endpoint choice adds -delta_i.  Matrix products
    # below check all constants, singletons, and pairs simultaneously.
    q_rows = q_adjusted_original_rows(case)
    base_fold = np.asarray(
        [cyclic_fold(row) for row in q_rows], dtype=np.int64
    )
    seed = adjacent.eliahou_base()
    deltas = np.zeros((len(keys), 4, 42), dtype=np.int64)
    for variable, (block, cell) in enumerate(keys):
        for row in ((0, 1) if block == "L" else (2, 3)):
            lower = -2 * seed[row][cell]
            upper = -2 * seed[row][cell + 42]
            if upper != -lower:
                raise AssertionError("eligible support cell is not opposite")
            deltas[variable, row, cell] = lower

    raw_constants = []
    raw_linear = []
    raw_quadratic = []
    for lag in range(1, 22):
        shifted_base = np.roll(base_fold, -lag, axis=1)
        shifted_deltas = np.roll(deltas, -lag, axis=2)
        constant_coefficient = int(np.sum(base_fold * shifted_base))
        cross_base = (
            np.einsum("rc,vrc->v", base_fold, shifted_deltas)
            + np.einsum("vrc,rc->v", deltas, shifted_base)
        )
        product_matrix = np.einsum(
            "vrc,wrc->vw", deltas, shifted_deltas
        )
        cross_matrix = product_matrix + product_matrix.T
        diagonal_norm = np.diag(product_matrix)
        linear_coefficients = cross_base + diagonal_norm
        if (
            constant_coefficient % 4
            or np.any(linear_coefficients % 4)
            or np.any(cross_matrix % 4)
        ):
            raise AssertionError(
                "the shell plus-fold support polynomial is not 0 mod 4"
            )
        # Replacing delta_i by -delta_i changes the base cross term by
        # -2*cross_base and its interaction with delta_j by -2*cross_ij.
        # Divisibility of cross_base by four proves orientation independence
        # of C/4 mod 2.  The stronger divisibility of every cross_ij by eight
        # is what makes the following C/8 mod-2 orientation matrix fixed:
        # selecting any other support cells cannot change one of its columns.
        if np.any(cross_base % 4) or np.any(cross_matrix % 8):
            raise AssertionError("plus mod8 depends on endpoint orientation")
        raw_constants.append((constant_coefficient // 4) & 1)
        raw_linear.append(np.remainder(linear_coefficients // 4, 2))
        raw_quadratic.append(np.remainder(cross_matrix // 4, 2))
    raw_constants_array = np.asarray(raw_constants, dtype=np.uint8)
    raw_linear_array = np.asarray(raw_linear, dtype=np.uint8)
    raw_quadratic_array = np.asarray(raw_quadratic, dtype=np.uint8)

    # Directly interpolate the support-only plus-fold digit on the
    # anti-fold characteristic-two affine code.
    baseline = oriented_correlations(case, keys, particular)
    if np.any(baseline % 8):
        raise AssertionError("affine particular point failed plus mod8")
    baseline_digit = np.remainder(baseline // 4, 2)
    matrix = []
    basis_values = []
    for generator in basis:
        value = oriented_correlations(case, keys, particular ^ generator)
        if np.any(value % 4):
            raise AssertionError("plus fold lost automatic divisibility by 4")
        digit = np.remainder(value // 4, 2)
        basis_values.append(digit)
        matrix.append(digit ^ baseline_digit)
    matrix = np.asarray(matrix, dtype=np.uint8).T
    if np.any(baseline_digit) or np.any(matrix):
        raise AssertionError("plus mod8 is not redundant on anti mod2")
    # The support-only plus-fold digit is quadratic over F_2, so constant,
    # singleton, and pair evaluations are a complete proof on the affine
    # code rather than a sample of its 2^57 points.
    for left in range(len(basis)):
        for right in range(left + 1, len(basis)):
            value = oriented_correlations(
                case, keys, particular ^ basis[left] ^ basis[right]
            )
            if np.any(value % 4):
                raise AssertionError("plus fold pair lost divisibility by 4")
            coefficient = (
                np.remainder(value // 4, 2)
                ^ basis_values[left]
                ^ basis_values[right]
                ^ baseline_digit
            )
            if np.any(coefficient):
                raise AssertionError(
                    "plus mod8 has a nonzero restricted quadratic term"
                )

    # The anti-fold code equations themselves have the authoritative shape.
    if triage.rank_mod(
        np.vstack((linear % 2, np.ones((1, len(keys)), dtype=np.uint8))),
        2,
    ) != 21:
        raise AssertionError("anti-fold affine-code rank changed")
    return {
        "case": case_number,
        "q_index": case.index,
        "anti_mod2_affine_dimension": len(basis),
        "plus_mod8_raw_quadratic_row_rank": triage.rank_mod(
            raw_quadratic_array.reshape(21, -1), 2
        ),
        "plus_mod8_raw_linear_row_rank": triage.rank_mod(
            raw_linear_array, 2
        ),
        "plus_mod8_raw_constant_weight": int(raw_constants_array.sum()),
        "plus_mod8_orientation_independent": True,
        "plus_mod8_restricted_rank": 0,
        "plus_mod8_restricted_constant": [0] * 21,
    }


def low_weight_code_span(case_number: int, profile_conditioned: bool) -> dict:
    case, keys, _, _, linear, _ = local.arrays(case_number)
    rows = [*np.remainder(linear, 2).astype(np.uint8)]
    rows.append(np.ones(len(keys), dtype=np.uint8))
    if profile_conditioned:
        for block in ("L", "S"):
            for parity in (0, 1):
                rows.append(
                    np.asarray(
                        [
                            key[0] == block and key[1] % 2 == parity
                            for key in keys
                        ],
                        dtype=np.uint8,
                    )
                )
    check = np.asarray(rows, dtype=np.uint8)
    rank = triage.rank_mod(check, 2)
    dimension = len(keys) - rank
    columns = tuple(
        sum(int(check[row, column]) << row for row in range(len(check)))
        for column in range(len(keys))
    )

    class BinaryBasis:
        def __init__(self) -> None:
            self.reduced: dict[int, int] = {}
            self.original: list[int] = []

        def add(self, vector: int) -> bool:
            reduced = vector
            while reduced:
                pivot = reduced.bit_length() - 1
                if pivot in self.reduced:
                    reduced ^= self.reduced[pivot]
                else:
                    self.reduced[pivot] = reduced
                    self.original.append(vector)
                    return True
            return False

    basis = BinaryBasis()
    pair_bins: dict[int, list[int]] = defaultdict(list)
    for left in range(len(keys)):
        for right in range(left + 1, len(keys)):
            pair_bins[columns[left] ^ columns[right]].append(
                (1 << left) | (1 << right)
            )
    for values in pair_bins.values():
        first = values[0]
        for value in values[1:]:
            basis.add(first ^ value)
    rank_through_four = len(basis.original)

    if rank_through_four < dimension:
        triple_bins: dict[int, list[int]] = defaultdict(list)
        for first in range(len(keys) - 2):
            for second in range(first + 1, len(keys) - 1):
                syndrome = columns[first] ^ columns[second]
                mask = (1 << first) | (1 << second)
                for third in range(second + 1, len(keys)):
                    triple_bins[syndrome ^ columns[third]].append(
                        mask | (1 << third)
                    )
        for values in triple_bins.values():
            first = values[0]
            for value in values[1:]:
                basis.add(first ^ value)
                if len(basis.original) == dimension:
                    break
            if len(basis.original) == dimension:
                break
    if len(basis.original) != dimension:
        raise AssertionError("weight-at-most-six words did not span the code")
    return {
        "case": case_number,
        "q_index": case.index,
        "profile_conditioned": profile_conditioned,
        "check_rank": rank,
        "code_dimension": dimension,
        "rank_generated_by_weight_at_most_4": rank_through_four,
        "rank_generated_by_weight_at_most_6": len(basis.original),
        "basis_weight_histogram": {
            str(weight): count
            for weight, count in sorted(
                Counter(vector.bit_count() for vector in basis.original).items()
            )
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full",
        action="store_true",
        help="also run all forty pinned mod-32 fixture audits",
    )
    parser.add_argument(
        "--samples-per-profile",
        type=int,
        default=1,
        help="deterministic exact-weight fixtures per profile with --full",
    )
    args = parser.parse_args()
    if args.samples_per_profile < 1:
        raise ValueError("--samples-per-profile must be positive")

    redundancy = [
        adjacent_mod8_redundancy_audit(case_number)
        for case_number in range(1, 21)
    ]
    code_spans = [
        low_weight_code_span(case_number, conditioned)
        for conditioned in (False, True)
        for case_number in range(1, 21)
    ]
    result: dict[str, object] = {
        "status": "exact scoped audit; no long case excluded",
        "adjacent_mod8_redundancy": redundancy,
        "low_weight_code_spans": code_spans,
    }
    if args.full:
        result["mod32_fixtures"] = [
            quadratic_next_digit(
                find_fixture(
                    case_number,
                    profile_number,
                    seed=(
                        668_320_000
                        + 10_000 * sample_number
                        + 2 * case_number
                        + profile_number
                    ),
                )
            )
            for case_number in range(1, 21)
            for profile_number in range(2)
            for sample_number in range(args.samples_per_profile)
        ]
    else:
        result["mod32_fixtures"] = [
            quadratic_next_digit(find_fixture(1, 0, seed=668_320_002))
        ]
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
