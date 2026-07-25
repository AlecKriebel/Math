#!/usr/bin/env python3
"""Independent exact red-team of the long-case plus-fold orientation lift.

This independent audit starts from the authoritative 84/83 Eliahou rows and the
authoritative anti-fold quadratic models.  It does not import the parallel
primary orientation-cascade implementation.

For deterministic exact-weight characteristic-two supports it checks:

* the plus-fold PAF is automatically zero modulo 8;
* modulo 16 it is an affine system in the 39 endpoint choices;
* after the two root-profile parity equations, the modulo-32 digit is an
  exact quadratic Boolean system;
* all enumerated orientation points replay in the original rows; and
* exact root-profile values and the following modulo-64 digit are counted.

The bounded samples are diagnostics, not a whole-case exclusion.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
CHAR3 = SEARCH / "eliahou_char3_jet"
sys.path[:0] = [str(CHAR3), str(SEARCH)]

import search_char3_local as local  # noqa: E402
import verify_eliahou_adjacent42_repair as adjacent  # noqa: E402
import verify_eliahou_antifold42 as antifold  # noqa: E402


@dataclass(frozen=True)
class BinaryAffineSpace:
    particular: np.ndarray
    basis: np.ndarray
    rank: int


def rank_gf2(matrix: np.ndarray) -> int:
    """Exact binary row rank, independently implemented."""

    work = np.asarray(matrix, dtype=np.uint8).copy() & 1
    row = 0
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        pivot = row + int(choices[0])
        work[[row, pivot]] = work[[pivot, row]]
        for other in np.flatnonzero(work[:, column]):
            if other != row:
                work[other] ^= work[row]
        row += 1
        if row == work.shape[0]:
            break
    return row


def solve_gf2(matrix: np.ndarray, rhs: np.ndarray) -> BinaryAffineSpace | None:
    """Return a particular point and row null basis over F2."""

    matrix = np.asarray(matrix, dtype=np.uint8) & 1
    rhs = np.asarray(rhs, dtype=np.uint8) & 1
    work = np.column_stack((matrix, rhs))
    pivots: list[int] = []
    row = 0
    for column in range(matrix.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        pivot = row + int(choices[0])
        work[[row, pivot]] = work[[pivot, row]]
        for other in np.flatnonzero(work[:, column]):
            if other != row:
                work[other] ^= work[row]
        pivots.append(column)
        row += 1
        if row == matrix.shape[0]:
            break
    if any(
        not np.any(equation[:-1]) and equation[-1]
        for equation in work
    ):
        return None
    free = tuple(
        column
        for column in range(matrix.shape[1])
        if column not in pivots
    )
    particular = np.zeros(matrix.shape[1], dtype=np.uint8)
    for equation, pivot in enumerate(pivots):
        particular[pivot] = work[equation, -1]
    basis = np.zeros((len(free), matrix.shape[1]), dtype=np.uint8)
    for basis_index, free_column in enumerate(free):
        basis[basis_index, free_column] = 1
        for equation, pivot in enumerate(pivots):
            basis[basis_index, pivot] = work[equation, free_column]
    if not np.array_equal((matrix @ particular) & 1, rhs):
        raise AssertionError("particular point failed binary replay")
    if np.any((matrix @ basis.T) & 1):
        raise AssertionError("null basis failed binary replay")
    return BinaryAffineSpace(particular, basis, len(pivots))


def inconsistency_witness(
    matrix: np.ndarray, rhs: np.ndarray
) -> list[int] | None:
    """Return equation rows whose XOR is 0=1, when one exists."""

    augmented = np.vstack(
        (
            np.asarray(matrix, dtype=np.uint8).T,
            np.asarray(rhs, dtype=np.uint8)[np.newaxis, :],
        )
    )
    target = np.zeros(augmented.shape[0], dtype=np.uint8)
    target[-1] = 1
    space = solve_gf2(augmented, target)
    if space is None:
        return None
    chosen = np.flatnonzero(space.particular).tolist()
    if np.any(
        np.bitwise_xor.reduce(matrix[chosen], axis=0)
    ) or not np.bitwise_xor.reduce(rhs[chosen]):
        raise AssertionError("invalid affine inconsistency witness")
    return list(map(int, chosen))


def q_adjusted_rows(case) -> np.ndarray:
    rows = [list(row) for row in adjacent.eliahou_base()]
    active_row = 1 if case.block == "L" else 3
    length = adjacent.LONG if case.block == "L" else adjacent.SHORT
    for coordinate in (case.index, length - 1 - case.index):
        rows[active_row][coordinate] *= -1
    padded = np.zeros((4, adjacent.LONG), dtype=np.int16)
    for row, values in enumerate(rows):
        padded[row, : len(values)] = values
    return padded


def direct_fold(rows: np.ndarray) -> np.ndarray:
    return rows[:, :42] + rows[:, 42:84]


def independent_paf(folds: np.ndarray) -> np.ndarray:
    """Return plus-fold PAF at the 21 independent nonzero lags."""

    return np.asarray(
        [
            int(np.sum(folds * np.roll(folds, -lag, axis=1)))
            for lag in range(1, 22)
        ],
        dtype=np.int64,
    )


def orientation_fold_model(
    case, keys: tuple[tuple[str, int], ...], support: np.ndarray
) -> tuple[np.ndarray, np.ndarray, tuple[int, ...]]:
    """Return fold at orientation zero and its 39 signed cell deltas."""

    selected = tuple(map(int, np.flatnonzero(support)))
    rows = q_adjusted_rows(case)
    folds = direct_fold(rows)
    deltas = np.zeros((len(selected), 4, 42), dtype=np.int16)
    for local_index, variable in enumerate(selected):
        block, cell = keys[variable]
        row_pair = (0, 1) if block == "L" else (2, 3)
        for row in row_pair:
            lower = int(rows[row, cell])
            upper = int(rows[row, cell + 42])
            if lower != -upper:
                raise AssertionError("support cell endpoints are not opposite")
            deltas[local_index, row, cell] = -2 * lower
        folds += deltas[local_index]
    return folds, deltas, selected


def paf_from_model(
    orientation_zero_fold: np.ndarray,
    deltas: np.ndarray,
    orientations: np.ndarray,
) -> np.ndarray:
    # Changing endpoint choice reverses the signed delta, hence subtracts
    # twice the orientation-zero delta.
    folds = (
        orientation_zero_fold
        - 2
        * np.einsum(
            "i,irc->rc", orientations.astype(np.int16), deltas
        )
    )
    return independent_paf(folds)


def profile_targets(profile) -> np.ndarray:
    ordinary, alternating = profile
    return np.asarray(
        [ordinary[0], alternating[0], ordinary[1], alternating[1]],
        dtype=np.int16,
    )


def root_coefficients(
    keys: tuple[tuple[str, int], ...],
    selected: tuple[int, ...],
) -> np.ndarray:
    """Coefficients of the four signed support evaluations L±,S±."""

    base = adjacent.eliahou_base()
    coefficients = np.zeros((len(selected), 4), dtype=np.int16)
    for local_index, variable in enumerate(selected):
        block, cell = keys[variable]
        seed_row = 0 if block == "L" else 2
        block_offset = 0 if block == "L" else 2
        lower_delta_half = -base[seed_row][cell]
        coefficients[local_index, block_offset] = lower_delta_half
        coefficients[local_index, block_offset + 1] = (
            lower_delta_half * (-1) ** cell
        )
    return coefficients


def root_values(
    orientations: np.ndarray, coefficients: np.ndarray
) -> np.ndarray:
    signed_orientations = orientations.astype(np.int16)
    return np.sum(
        coefficients * (1 - 2 * signed_orientations[:, np.newaxis]),
        axis=0,
        dtype=np.int16,
    )


def profile_support_feasible(
    keys: tuple[tuple[str, int], ...],
    support: np.ndarray,
    profile,
) -> bool:
    ordinary, alternating = profile
    wanted = {
        ("L", 0): (ordinary[0] + alternating[0]) // 2,
        ("L", 1): (ordinary[0] - alternating[0]) // 2,
        ("S", 0): (ordinary[1] + alternating[1]) // 2,
        ("S", 1): (ordinary[1] - alternating[1]) // 2,
    }
    for (block, parity), target in wanted.items():
        count = sum(
            int(flag)
            for (key_block, cell), flag in zip(keys, support)
            if key_block == block and cell % 2 == parity
        )
        if count < abs(target) or (count - target) % 2:
            return False
    return True


def raw_antimod2_space(case_number: int):
    case, keys, _, constant, linear, quadratic = local.arrays(case_number)
    if np.any(quadratic & 1):
        raise AssertionError("anti-fold characteristic-two layer changed")
    matrix = np.vstack(
        (
            np.remainder(linear, 2).astype(np.uint8),
            np.ones((1, len(keys)), dtype=np.uint8),
        )
    )
    rhs = np.append(np.remainder(-constant, 2), 1).astype(np.uint8)
    space = solve_gf2(matrix, rhs)
    if space is None or space.rank != 21 or len(space.basis) != 57:
        raise AssertionError("anti-fold affine-space dimensions changed")
    return case, keys, constant, linear, quadratic, matrix, rhs, space


def deterministic_supports(
    case_number: int,
    profile_number: int,
    count: int,
    seed_base: int,
) -> list[np.ndarray]:
    case, keys, constant, linear, quadratic, _, _, space = (
        raw_antimod2_space(case_number)
    )
    generator = np.random.default_rng(
        seed_base + 1009 * case_number + 17 * profile_number
    )
    result: list[np.ndarray] = []
    seen: set[int] = set()
    attempts = 0
    while len(result) < count and attempts < 2_000_000:
        attempts += 1
        coordinates = generator.integers(
            0, 2, len(space.basis), dtype=np.uint8
        )
        support = space.particular ^ (
            (coordinates @ space.basis) & 1
        )
        if int(support.sum()) != 39:
            continue
        if not profile_support_feasible(
            keys, support, case.profiles[profile_number]
        ):
            continue
        mask = sum(
            int(bit) << index for index, bit in enumerate(support)
        )
        if mask in seen:
            continue
        # Cross-check the authoritative normalized anti-fold residual and
        # the independent physical negacyclic PAF.
        anti_values = local.exact_values(
            support.astype(np.int16), constant, linear, quadratic
        )
        if np.any(anti_values & 1):
            raise AssertionError("sample left the anti-mod2 slice")
        long_support = [
            cell
            for (block, cell), flag in zip(keys, support)
            if flag and block == "L"
        ]
        short_support = [
            cell
            for (block, cell), flag in zip(keys, support)
            if flag and block == "S"
        ]
        anti_rows = antifold.boundary_antifold_rows(
            case.block, case.index, long_support, short_support
        )
        physical = np.asarray(
            antifold.negacyclic_norm_coefficients(anti_rows)[1:21],
            dtype=np.int64,
        )
        if not np.array_equal(physical, 4 * anti_values):
            raise AssertionError("physical anti-fold replay disagrees")
        seen.add(mask)
        result.append(support)
    if len(result) != count:
        raise AssertionError("failed to obtain deterministic supports")
    return result


def verify_plus_mod8_redundancy(case_number: int) -> dict[str, object]:
    """Prove the restricted plus digit is zero as an affine functional."""

    case, keys, _, _, _, matrix, rhs, space = raw_antimod2_space(
        case_number
    )

    def value(support: np.ndarray) -> np.ndarray:
        fold0, deltas, _ = orientation_fold_model(case, keys, support)
        paf = paf_from_model(
            fold0, deltas, np.zeros(int(support.sum()), dtype=np.uint8)
        )
        if np.any(paf % 4):
            raise AssertionError("plus PAF is not universally divisible by 4")
        return np.remainder(paf // 4, 2).astype(np.uint8)

    constant = value(np.zeros(len(keys), dtype=np.uint8))
    columns = np.zeros((21, len(keys)), dtype=np.uint8)
    unit_values = []
    for variable in range(len(keys)):
        point = np.zeros(len(keys), dtype=np.uint8)
        point[variable] = 1
        current = value(point)
        unit_values.append(current)
        columns[:, variable] = current ^ constant

    # Directly verify all second differences vanish: plus PAF/4 mod 2 is
    # genuinely affine in support, so the null-basis restriction is exact.
    for left in range(len(keys)):
        for right in range(left + 1, len(keys)):
            point = np.zeros(len(keys), dtype=np.uint8)
            point[left] = point[right] = 1
            if np.any(
                value(point)
                ^ unit_values[left]
                ^ unit_values[right]
                ^ constant
            ):
                raise AssertionError("plus modulo-8 support digit is nonlinear")

    restricted_constant = value(space.particular)
    restricted_columns = np.asarray(
        [
            value(space.particular ^ generator) ^ restricted_constant
            for generator in space.basis
        ],
        dtype=np.uint8,
    ).T
    if np.any(restricted_constant) or np.any(restricted_columns):
        raise AssertionError("plus modulo 8 is not redundant on anti modulo 2")

    # Random affine-combination replay guards basis orientation/indexing.
    generator = np.random.default_rng(668_800 + case_number)
    for _ in range(64):
        coordinate = generator.integers(
            0, 2, len(space.basis), dtype=np.uint8
        )
        support = space.particular ^ ((coordinate @ space.basis) & 1)
        if np.any(value(support)):
            raise AssertionError("random anti-mod2 point failed plus mod8")

    return {
        "case": case_number,
        "q_index": case.index,
        "anti_mod2_rank": int(space.rank),
        "anti_mod2_dimension": int(len(space.basis)),
        "unrestricted_plus_digit_rank": rank_gf2(columns),
        "restricted_plus_digit_rank": rank_gf2(restricted_columns),
        "restricted_plus_digit_constant_weight": int(
            restricted_constant.sum()
        ),
        "all_support_second_differences_checked": (
            len(keys) * (len(keys) - 1) // 2
        ),
        "anti_equation_replay": bool(
            np.array_equal(
                (matrix @ space.particular) & 1, rhs
            )
        ),
    }


def variable_truth_masks(dimension: int) -> tuple[list[int], int, int]:
    point_count = 1 << dimension
    all_points = (1 << point_count) - 1
    masks = []
    for index in range(dimension):
        block = 1 << index
        pattern = ((1 << block) - 1) << block
        mask = 0
        for offset in range(0, point_count, 2 * block):
            mask |= pattern << offset
        masks.append(mask & all_points)
    return masks, all_points, point_count


def truth_mask(
    constant: int,
    linear: np.ndarray,
    quadratic: np.ndarray,
    variable_masks: list[int],
    all_points: int,
) -> int:
    result = all_points if constant else 0
    dimension = len(linear)
    for coordinate in np.flatnonzero(linear):
        result ^= variable_masks[int(coordinate)]
    for left in range(dimension):
        for right in range(left + 1, dimension):
            if quadratic[left, right]:
                result ^= variable_masks[left] & variable_masks[right]
    return result


def affine_points(space: BinaryAffineSpace) -> tuple[np.ndarray, np.ndarray]:
    dimension = len(space.basis)
    integers = np.arange(1 << dimension, dtype=np.uint32)
    coordinates = (
        (integers[:, np.newaxis] >> np.arange(dimension, dtype=np.uint32))
        & 1
    ).astype(np.uint8)
    points = space.particular ^ (
        (coordinates @ space.basis) & 1
    ).astype(np.uint8)
    return coordinates, points


def audit_fixture(
    case_number: int,
    profile_number: int,
    sample_number: int,
    support: np.ndarray,
    deep_replay: bool,
) -> dict[str, object]:
    case, keys, _, _, _, _, _, _ = raw_antimod2_space(case_number)
    fold0, deltas, selected = orientation_fold_model(case, keys, support)
    zero_orientation = np.zeros(len(selected), dtype=np.uint8)
    baseline = paf_from_model(fold0, deltas, zero_orientation)
    if np.any(baseline % 8):
        raise AssertionError("exact anti-mod2 support failed plus modulo 8")

    # Derive the exact affine modulo-16 system.
    paf_columns = np.zeros((21, len(selected)), dtype=np.uint8)
    singleton_pafs = []
    for variable in range(len(selected)):
        point = zero_orientation.copy()
        point[variable] = 1
        current = paf_from_model(fold0, deltas, point)
        singleton_pafs.append(current)
        difference = current - baseline
        if np.any(difference % 8):
            raise AssertionError("orientation derivative is not a multiple of 8")
        paf_columns[:, variable] = np.remainder(
            difference // 8, 2
        ).astype(np.uint8)

    # Quadratic orientation terms are multiples of 16.  Check all pairs
    # directly for the first sample of every case/profile.
    pair_checks = 0
    if deep_replay:
        for left in range(len(selected)):
            for right in range(left + 1, len(selected)):
                point = zero_orientation.copy()
                point[left] = point[right] = 1
                second = (
                    paf_from_model(fold0, deltas, point)
                    - singleton_pafs[left]
                    - singleton_pafs[right]
                    + baseline
                )
                if np.any(second % 16):
                    raise AssertionError(
                        "modulo-16 orientation system is not affine"
                    )
                pair_checks += 1

    coefficients = root_coefficients(keys, selected)
    targets = profile_targets(case.profiles[profile_number])
    root_baseline = np.sum(coefficients, axis=0, dtype=np.int16)
    root_rhs_four = (root_baseline - targets) // 2
    if np.any(2 * root_rhs_four != root_baseline - targets):
        raise AssertionError("root target parity is impossible")
    # L+ and L- give the same binary equation; likewise S+ and S-.
    if (
        (root_rhs_four[0] - root_rhs_four[1]) % 2
        or (root_rhs_four[2] - root_rhs_four[3]) % 2
    ):
        raise AssertionError("paired root parities disagree")
    root_matrix = np.zeros((2, len(selected)), dtype=np.uint8)
    for local_index, variable in enumerate(selected):
        root_matrix[0, local_index] = keys[variable][0] == "L"
        root_matrix[1, local_index] = keys[variable][0] == "S"
    root_rhs = np.asarray(
        [root_rhs_four[0] & 1, root_rhs_four[2] & 1],
        dtype=np.uint8,
    )
    matrix = np.vstack((paf_columns, root_matrix))
    rhs = np.concatenate(
        (
            np.remainder(-baseline // 8, 2).astype(np.uint8),
            root_rhs,
        )
    )
    mod16_space = solve_gf2(matrix, rhs)
    matrix_rank = rank_gf2(matrix)
    augmented_rank = rank_gf2(np.column_stack((matrix, rhs)))
    support_record = [
        [block, cell]
        for (block, cell), flag in zip(keys, support)
        if flag
    ]
    support_sha256 = hashlib.sha256(
        json.dumps(support_record, separators=(",", ":")).encode()
    ).hexdigest()
    if mod16_space is None:
        contradiction_rows = inconsistency_witness(matrix, rhs)
        if contradiction_rows is None:
            raise AssertionError("rank inconsistency has no XOR witness")
        row_labels = [
            *(f"plus_lag_{lag}" for lag in range(1, 22)),
            "root_L_parity",
            "root_S_parity",
        ]
        return {
            "case": case_number,
            "q_index": case.index,
            "profile": profile_number,
            "sample": sample_number,
            "support_sha256": support_sha256,
            "support": support_record,
            "mod16_rank": matrix_rank,
            "mod16_augmented_rank": augmented_rank,
            "mod16_consistent": False,
            "mod16_nullity": None,
            "mod16_exact_root_points": 0,
            "mod32_points": 0,
            "mod32_survivors": 0,
            "mod32_exact_root_survivors": 0,
            "mod64_exact_root_survivors": 0,
            "mod32_coefficient_rank": None,
            "mod32_augmented_coefficient_rank": None,
            "mod32_quadratic_row_rank": None,
            "mod32_polar_rank_histogram": None,
            "mod32_common_polar_radical_dimension": None,
            "mod16_pair_differences_checked": pair_checks,
            "mod16_xor_contradiction_rows": contradiction_rows,
            "mod16_xor_contradiction_labels": [
                row_labels[row] for row in contradiction_rows
            ],
        }
    if mod16_space.rank != matrix_rank:
        raise AssertionError("binary rank implementations disagree")

    # Enumerate the full mod-16 orientation fibre.  This independently
    # measures exact root-profile contraction before using modulo 32.
    coordinates, orientations = affine_points(mod16_space)
    signed_root_values = (
        root_baseline[np.newaxis, :]
        - 2 * (orientations.astype(np.int16) @ coefficients)
    )
    exact_root_flags = np.all(
        signed_root_values == targets[np.newaxis, :], axis=1
    )
    exact_root_count = int(np.count_nonzero(exact_root_flags))

    dimension = len(mod16_space.basis)

    def digit(coordinate: np.ndarray) -> np.ndarray:
        orientation = mod16_space.particular ^ (
            (coordinate @ mod16_space.basis) & 1
        )
        paf = paf_from_model(fold0, deltas, orientation)
        if np.any(paf % 16):
            raise AssertionError("modulo-16 solution failed physical replay")
        return np.remainder(paf // 16, 2).astype(np.uint8)

    zero = np.zeros(dimension, dtype=np.uint8)
    constant = digit(zero)
    linear = np.zeros((21, dimension), dtype=np.uint8)
    singleton_digits = []
    for variable in range(dimension):
        point = zero.copy()
        point[variable] = 1
        current = digit(point)
        singleton_digits.append(current)
        linear[:, variable] = current ^ constant
    quadratic = np.zeros((21, dimension, dimension), dtype=np.uint8)
    for left in range(dimension):
        for right in range(left + 1, dimension):
            point = zero.copy()
            point[left] = point[right] = 1
            coefficient = (
                digit(point)
                ^ singleton_digits[left]
                ^ singleton_digits[right]
                ^ constant
            )
            quadratic[:, left, right] = coefficient

    # The exact signed-fold PAF is quadratic in endpoint signs.  Direct
    # third-difference controls check the interpolated ANF convention.
    cubic_checks = 0
    if deep_replay and dimension >= 3:
        generator = np.random.default_rng(
            668_932_000
            + 1000 * case_number
            + 100 * profile_number
            + sample_number
        )
        for _ in range(256):
            indices = generator.choice(dimension, 3, replace=False)
            values = []
            for subset in range(8):
                point = zero.copy()
                for bit, variable in enumerate(indices):
                    point[variable] = (subset >> bit) & 1
                values.append(digit(point))
            third = values[0].copy()
            for value in values[1:]:
                third ^= value
            if np.any(third):
                raise AssertionError("modulo-32 digit has a cubic term")
            cubic_checks += 1

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
    coefficient_rank = rank_gf2(coefficient_rows)
    augmented_coefficient_rank = rank_gf2(
        np.column_stack((coefficient_rows, constant))
    )
    quadratic_rank = rank_gf2(quadratic_rows)
    polar = quadratic ^ np.swapaxes(quadratic, 1, 2)
    polar_ranks = [rank_gf2(form) for form in polar]
    common_radical_dimension = dimension - rank_gf2(
        polar.reshape(21 * dimension, dimension)
    )

    variable_masks, all_points, point_count = variable_truth_masks(dimension)
    failed = 0
    for equation in range(21):
        failed |= truth_mask(
            int(constant[equation]),
            linear[equation],
            quadratic[equation],
            variable_masks,
            all_points,
        )
    survivor_mask = all_points ^ failed
    survivor_count = survivor_mask.bit_count()

    mod32_exact_root = 0
    mod64_exact_root = 0
    survivor_examples = []
    remaining = survivor_mask
    while remaining:
        low = remaining & -remaining
        assignment = low.bit_length() - 1
        remaining ^= low
        orientation = orientations[assignment]
        paf = paf_from_model(fold0, deltas, orientation)
        if np.any(paf % 32):
            raise AssertionError("modulo-32 truth mask admitted false point")
        roots = root_values(orientation, coefficients)
        root_exact = np.array_equal(roots, targets)
        if root_exact:
            mod32_exact_root += 1
            if np.all((paf // 32) % 2 == 0):
                mod64_exact_root += 1
        if len(survivor_examples) < 4:
            survivor_examples.append(
                {
                    "coordinate_assignment": assignment,
                    "root_values": list(map(int, roots)),
                    "root_exact": bool(root_exact),
                    "paf": list(map(int, paf)),
                }
            )

    # Cross-check vectorized exact-root flags at all surviving assignments.
    if sum(
        int(exact_root_flags[index])
        for index in range(point_count)
        if (survivor_mask >> index) & 1
    ) != mod32_exact_root:
        raise AssertionError("root-count implementations disagree")

    return {
        "case": case_number,
        "q_index": case.index,
        "profile": profile_number,
        "sample": sample_number,
        "support_sha256": support_sha256,
        "support": support_record,
        "mod16_rank": matrix_rank,
        "mod16_augmented_rank": augmented_rank,
        "mod16_consistent": True,
        "mod16_nullity": dimension,
        "mod16_exact_root_points": exact_root_count,
        "mod32_points": point_count,
        "mod32_survivors": survivor_count,
        "mod32_exact_root_survivors": mod32_exact_root,
        "mod64_exact_root_survivors": mod64_exact_root,
        "mod32_coefficient_rank": coefficient_rank,
        "mod32_augmented_coefficient_rank": augmented_coefficient_rank,
        "mod32_quadratic_row_rank": quadratic_rank,
        "mod32_polar_rank_histogram": {
            str(rank): count
            for rank, count in sorted(Counter(polar_ranks).items())
        },
        "mod32_common_polar_radical_dimension": (
            common_radical_dimension
        ),
        "mod16_pair_differences_checked": pair_checks,
        "mod32_cubic_differences_checked": cubic_checks,
        "mod32_survivor_examples": survivor_examples,
    }


def summarize(fixtures: list[dict[str, object]]) -> dict[str, object]:
    consistent = [
        item for item in fixtures if item["mod16_consistent"]
    ]
    total_points = sum(int(item["mod32_points"]) for item in fixtures)
    total_survivors = sum(
        int(item["mod32_survivors"]) for item in fixtures
    )
    root_points = [
        int(item["mod16_exact_root_points"]) for item in consistent
    ]
    return {
        "fixtures": len(fixtures),
        "mod16_inconsistent_fixtures": len(fixtures) - len(consistent),
        "mod16_rank_histogram": {
            str(rank): count
            for rank, count in sorted(
                Counter(
                    int(item["mod16_rank"]) for item in fixtures
                ).items()
            )
        },
        "mod16_nullity_histogram": {
            str(nullity): count
            for nullity, count in sorted(
                Counter(
                    int(item["mod16_nullity"])
                    for item in consistent
                ).items()
            )
        },
        "mod16_exact_root_point_histogram": {
            str(points): count
            for points, count in sorted(Counter(root_points).items())
        },
        "mod16_exact_root_points_total": sum(root_points),
        "mod32_points_total": total_points,
        "mod32_survivors_total": total_survivors,
        "mod32_fixture_zero_count": sum(
            int(item["mod32_survivors"]) == 0 for item in fixtures
        ),
        "mod32_point_survival_rate": (
            total_survivors / total_points if total_points else 0.0
        ),
        "mod32_exact_root_survivors_total": sum(
            int(item["mod32_exact_root_survivors"])
            for item in fixtures
        ),
        "mod64_exact_root_survivors_total": sum(
            int(item["mod64_exact_root_survivors"])
            for item in fixtures
        ),
        "mod32_coefficient_rank_histogram": {
            str(rank): count
            for rank, count in sorted(
                Counter(
                    int(item["mod32_coefficient_rank"])
                    for item in consistent
                ).items()
            )
        },
        "mod32_quadratic_row_rank_histogram": {
            str(rank): count
            for rank, count in sorted(
                Counter(
                    int(item["mod32_quadratic_row_rank"])
                    for item in consistent
                ).items()
            )
        },
        "mod32_common_polar_radical_dimension_histogram": {
            str(dimension): count
            for dimension, count in sorted(
                Counter(
                    int(item["mod32_common_polar_radical_dimension"])
                    for item in consistent
                ).items()
            )
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples-per-profile", type=int, default=1)
    parser.add_argument("--seed-base", type=int, default=7_668_320_000)
    parser.add_argument(
        "--skip-redundancy",
        action="store_true",
        help="skip the all-case plus-mod8 affine proof",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="omit full fixture records from JSON",
    )
    args = parser.parse_args()
    if args.samples_per_profile < 1:
        raise ValueError("--samples-per-profile must be positive")

    redundancy = []
    if not args.skip_redundancy:
        redundancy = [
            verify_plus_mod8_redundancy(case_number)
            for case_number in range(1, 21)
        ]
    fixtures = []
    for case_number in range(1, 21):
        for profile_number in range(2):
            supports = deterministic_supports(
                case_number,
                profile_number,
                args.samples_per_profile,
                args.seed_base,
            )
            for sample_number, support in enumerate(supports):
                fixtures.append(
                    audit_fixture(
                        case_number,
                        profile_number,
                        sample_number,
                        support,
                        deep_replay=(sample_number == 0),
                    )
                )

    result: dict[str, object] = {
        "status": (
            "independent exact scoped audit; bounded support samples only; "
            "no long case, base sequence, or H(668) claimed"
        ),
        "samples_per_profile": args.samples_per_profile,
        "seed_base": args.seed_base,
        "plus_mod8_redundancy": redundancy,
        "summary": summarize(fixtures),
    }
    if not args.compact:
        result["fixtures"] = fixtures
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
