#!/usr/bin/env python3
"""Verify the case-26 reflection gauge and global-reuse obstructions.

This script proves an exact contraction of the whole characteristic-six
case-26 census.  It also checks three boundaries of the contraction:

* the quotient compatibility relation has full Walsh support;
* the direct quotient tensor graph contains K_18;
* at the pinned quotient, every component's quadratic coefficient matrices
  generate the full matrix algebra and admit a full-rank scalar combination.

None of these modular calculations proves or disproves the integer
anti-fold instance.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
GLOBAL = SEARCH / "eliahou_global_quotient_plan"
FIXED = SEARCH / "eliahou_defect2_math"
JET = SEARCH / "eliahou_char3_jet"
AUDIT = SEARCH / "eliahou_char3_jet_audit"
sys.path[:0] = [
    str(GLOBAL),
    str(FIXED),
    str(JET),
    str(AUDIT),
    str(SEARCH),
]

import search_char3_local as local  # noqa: E402
from verify_fixed_quotient_join import derive_reduction  # noqa: E402
from verify_global_quotient_plan import derive as derive_global  # noqa: E402


EXPECTED = HERE / "EXPECTED_GLOBAL_REUSE_MATH.json"
HASHES = HERE / "ARTIFACT_HASHES.json"


def rank_mod(matrix: np.ndarray, modulus: int) -> int:
    """Return the rank of a small matrix over a prime field."""

    work = np.remainder(np.asarray(matrix, dtype=np.int64), modulus).copy()
    row = 0
    for column in range(work.shape[1]):
        candidates = np.flatnonzero(work[row:, column])
        if not len(candidates):
            continue
        pivot = row + int(candidates[0])
        work[[row, pivot]] = work[[pivot, row]]
        inverse = pow(int(work[row, column]), -1, modulus)
        work[row] = np.remainder(inverse * work[row], modulus)
        for other in range(work.shape[0]):
            if other != row and work[other, column]:
                work[other] = np.remainder(
                    work[other]
                    - int(work[other, column]) * work[row],
                    modulus,
                )
        row += 1
        if row == work.shape[0]:
            break
    return row


def rref_mod2(matrix: np.ndarray) -> tuple[np.ndarray, tuple[int, ...]]:
    """Return reduced row echelon form and pivot columns over F_2."""

    work = np.asarray(matrix, dtype=np.uint8).copy() & 1
    row = 0
    pivots = []
    for column in range(work.shape[1]):
        candidates = np.flatnonzero(work[row:, column])
        if not len(candidates):
            continue
        pivot = row + int(candidates[0])
        work[[row, pivot]] = work[[pivot, row]]
        for other in np.flatnonzero(work[:, column]):
            if other != row:
                work[other] ^= work[row]
        pivots.append(column)
        row += 1
        if row == work.shape[0]:
            break
    return work, tuple(pivots)


def inverse_mod2(matrix: np.ndarray) -> np.ndarray:
    """Invert a nonsingular binary matrix."""

    square = np.asarray(matrix, dtype=np.uint8)
    if square.ndim != 2 or square.shape[0] != square.shape[1]:
        raise AssertionError("binary inverse requires a square matrix")
    size = square.shape[0]
    augmented = np.concatenate(
        [square.copy() & 1, np.eye(size, dtype=np.uint8)], axis=1
    )
    for column in range(size):
        candidates = np.flatnonzero(augmented[column:, column])
        if not len(candidates):
            raise AssertionError("binary matrix is singular")
        pivot = column + int(candidates[0])
        augmented[[column, pivot]] = augmented[[pivot, column]]
        for other in np.flatnonzero(augmented[:, column]):
            if other != column:
                augmented[other] ^= augmented[column]
    return augmented[:, size:]


def right_nullspace_mod2(matrix: np.ndarray) -> tuple[np.ndarray, ...]:
    """Return the canonical free-column basis for the right nullspace."""

    reduced, pivots = rref_mod2(matrix)
    free = [
        column for column in range(reduced.shape[1])
        if column not in pivots
    ]
    vectors = []
    for free_column in free:
        vector = np.zeros(reduced.shape[1], dtype=np.uint8)
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = reduced[row, free_column]
        if np.any(np.remainder(matrix @ vector, 2)):
            raise AssertionError("binary nullspace construction failed")
        vectors.append(vector)
    return tuple(vectors)


class IncrementalBasis:
    """Insertion-ordered row basis over F_3."""

    def __init__(self) -> None:
        self.vectors: list[np.ndarray] = []
        self.pivots: list[int] = []

    def add(self, vector: np.ndarray) -> np.ndarray | None:
        reduced = np.remainder(
            np.asarray(vector, dtype=np.int64).reshape(-1), 3
        )
        for basis, pivot in zip(self.vectors, self.pivots):
            if reduced[pivot]:
                reduced = np.remainder(
                    reduced - int(reduced[pivot]) * basis, 3
                )
        nonzero = np.flatnonzero(reduced)
        if not len(nonzero):
            return None
        pivot = int(nonzero[0])
        if reduced[pivot] == 2:
            reduced = np.remainder(2 * reduced, 3)
        self.vectors.append(reduced)
        self.pivots.append(pivot)
        return reduced


def algebra_dimension(generators: tuple[np.ndarray, ...]) -> int:
    """Return the dimension of the unital algebra generated over F_3."""

    size = generators[0].shape[0]
    basis = IncrementalBasis()
    queue: list[np.ndarray] = []

    def insert(matrix: np.ndarray) -> None:
        reduced = basis.add(matrix)
        if reduced is not None:
            queue.append(reduced.reshape((size, size)))

    insert(np.eye(size, dtype=np.int64))
    for generator in generators:
        insert(generator)
    cursor = 0
    while cursor < len(queue):
        left = queue[cursor]
        cursor += 1
        for generator in generators:
            insert(np.remainder(left @ generator, 3))
            if len(basis.vectors) == size * size:
                return size * size
    return len(basis.vectors)


def component_matrices(
    quadratic: np.ndarray, component: tuple[int, ...]
) -> tuple[np.ndarray, ...]:
    """Build the twenty polar coefficient matrices on one component."""

    size = len(component)
    result = []
    for equation in range(20):
        matrix = np.zeros((size, size), dtype=np.int64)
        for local_left, left in enumerate(component):
            for local_right in range(local_left + 1, size):
                right = component[local_right]
                first, second = sorted((left, right))
                value = int(quadratic[equation, first, second]) % 3
                matrix[local_left, local_right] = value
                matrix[local_right, local_left] = value
        result.append(matrix)
    return tuple(result)


def first_full_rank_combination(
    matrices: tuple[np.ndarray, ...],
) -> tuple[int, ...]:
    """Find the first weight-one or weight-two full-rank combination."""

    size = matrices[0].shape[0]
    for weight in (1, 2):
        for support in combinations(range(len(matrices)), weight):
            for coefficients in product((1, 2), repeat=weight):
                candidate = np.zeros((size, size), dtype=np.int64)
                for index, coefficient in zip(support, coefficients):
                    candidate += coefficient * matrices[index]
                if rank_mod(candidate, 3) == size:
                    vector = [0] * len(matrices)
                    for index, coefficient in zip(support, coefficients):
                        vector[index] = coefficient
                    return tuple(vector)
    raise AssertionError("no weight-at-most-two full-rank combination")


def pair_coupling(
    raw_quadratic: np.ndarray,
    pairs: np.ndarray,
    left: int,
    right: int,
    left_parity: int,
    right_parity: int,
) -> np.ndarray:
    """Return the twenty-trit y_left*y_right coefficient."""

    a, b = map(int, pairs[left])
    c, d = map(int, pairs[right])
    left_sign = 1 if left_parity == 0 else -1
    right_sign = 1 if right_parity == 0 else -1
    return np.remainder(
        left_sign * right_sign * raw_quadratic[:, a, c]
        + left_sign * raw_quadratic[:, a, d]
        + right_sign * raw_quadratic[:, b, c]
        + raw_quadratic[:, b, d],
        3,
    )


def derive() -> dict[str, object]:
    """Derive and verify the contraction and the reuse audits."""

    global_result = derive_global()
    model = global_result["_model"]
    pairs = np.asarray(model["pairs"], dtype=np.int64)
    pair_blocks = np.asarray(model["pair_blocks"], dtype=np.uint8)
    particular = np.asarray(model["particular"], dtype=np.uint8)
    basis = np.asarray(model["basis"], dtype=np.uint8)
    central = int(global_result["central_pair_index"])

    case, keys, equations, constant, linear, raw_quadratic = local.arrays(26)
    if (case.block, case.index) != ("S", 12):
        raise AssertionError("canonical case 26 changed")
    if tuple(equation.lag for equation in equations) != tuple(range(1, 21)):
        raise AssertionError("normalized lag ordering changed")

    # Spatial reflection j -> 40-j preserves the case-26 holes {12,28}.
    key_index = {key: index for index, key in enumerate(keys)}
    reflection = np.array(
        [key_index[(block, 40 - cell)] for block, cell in keys],
        dtype=np.int64,
    )
    if not np.array_equal(
        reflection[reflection], np.arange(len(keys), dtype=np.int64)
    ):
        raise AssertionError("support reflection is not an involution")
    lag_signs = np.array(
        [-1 if equation.lag % 2 else 1 for equation in equations],
        dtype=np.int64,
    )
    if not np.array_equal(constant, lag_signs * constant):
        raise AssertionError("reflection changed the constant polynomial")
    if not np.array_equal(
        linear[:, reflection], lag_signs[:, np.newaxis] * linear
    ):
        raise AssertionError("reflection changed the linear polynomial")
    if not np.array_equal(
        raw_quadratic[:, reflection][:, :, reflection],
        lag_signs[:, np.newaxis, np.newaxis] * raw_quadratic,
    ):
        raise AssertionError("reflection changed the quadratic polynomial")

    for pair_index, (left, right) in enumerate(pairs):
        left = int(left)
        right = int(right)
        if pair_index == central:
            if reflection[left] != left or reflection[right] != right:
                raise AssertionError("central cells are not reflection-fixed")
        elif reflection[left] != right or reflection[right] != left:
            raise AssertionError("a noncentral syndrome pair is not reflected")

    left_pairs = tuple(
        map(int, np.flatnonzero(pair_blocks == 0))
    )
    right_pairs = tuple(
        map(int, np.flatnonzero(pair_blocks == 1))
    )
    if len(left_pairs) != 20 or len(right_pairs) != 18:
        raise AssertionError("block pair counts changed")

    # The affine L-parity coset is disjoint from zero.  Therefore every
    # quotient has an odd noncentral L pair, on whose orientation reflection
    # acts freely.
    left_basis = basis[:, left_pairs]
    left_rank = rank_mod(left_basis, 2)
    left_augmented_rank = rank_mod(
        np.vstack([left_basis, particular[list(left_pairs)]]), 2
    )
    if (left_rank, left_augmented_rank) != (18, 19):
        raise AssertionError("the affine L-parity coset now contains zero")

    # Parameterize by the eighteen S parities.  The L graph map has rank 18,
    # so its Fourier dual hits every one of the 2^18 quotient characters and
    # has a two-dimensional kernel.
    right_basis = basis[:, right_pairs]
    inverse_right = inverse_mod2(right_basis)
    right_to_left = np.remainder(inverse_right @ left_basis, 2)
    if rank_mod(right_to_left, 2) != 18:
        raise AssertionError("S-to-L quotient map lost full rank")
    affine_offset = np.remainder(
        particular[list(left_pairs)]
        + particular[list(right_pairs)] @ right_to_left,
        2,
    ).astype(np.uint8)
    dual_checks = right_nullspace_mod2(right_to_left)
    if len(dual_checks) != 2:
        raise AssertionError("L quotient code no longer has codimension two")
    dual_payload = []
    for check in dual_checks:
        rhs = int(affine_offset @ check % 2)
        if rhs != 1:
            raise AssertionError("an L dual check no longer has odd syndrome")
        dual_payload.append(
            {
                "support": list(map(int, np.flatnonzero(check))),
                "weight": int(check.sum()),
                "rhs": rhs,
            }
        )
    dual_payload.sort(key=lambda item: (item["weight"], item["support"]))

    # Direct tensor elimination of the S quotient bits sees every pairwise
    # edge: the conditional y_i*y_j coefficient is nonzero precisely in one
    # of the two equality patterns.  Hence the quotient primal graph is K_18.
    s_edges = 0
    for offset, left in enumerate(right_pairs):
        for right in right_pairs[offset + 1:]:
            pattern = tuple(
                int(np.any(pair_coupling(
                    raw_quadratic,
                    pairs,
                    left,
                    right,
                    left_parity,
                    right_parity,
                )))
                for left_parity in (0, 1)
                for right_parity in (0, 1)
            )
            if pattern not in ((1, 0, 0, 1), (0, 1, 1, 0)):
                raise AssertionError("an S quotient interaction lost its edge")
            mixed_difference = np.remainder(
                pair_coupling(
                    raw_quadratic, pairs, left, right, 0, 0
                )
                - pair_coupling(
                    raw_quadratic, pairs, left, right, 0, 1
                )
                - pair_coupling(
                    raw_quadratic, pairs, left, right, 1, 0
                )
                + pair_coupling(
                    raw_quadratic, pairs, left, right, 1, 1
                ),
                3,
            )
            if not np.any(mixed_difference):
                raise AssertionError(
                    "an S quotient interaction is additively separable"
                )
            s_edges += 1
    if s_edges != 153:
        raise AssertionError("the S quotient graph is not K_18")

    # At the pinned quotient, the coefficient matrices are neither uniformly
    # low rank nor simultaneously reducible by a fixed invariant-block
    # decomposition: each generated algebra is the complete matrix algebra.
    fixed = derive_reduction()
    if tuple(map(len, fixed.components)) != (10, 10, 10, 8):
        raise AssertionError("pinned component sizes changed")
    algebra_payload = []
    for component in fixed.components:
        matrices = component_matrices(fixed.quadratic, component)
        dimension = algebra_dimension(matrices)
        size = len(component)
        if dimension != size * size:
            raise AssertionError("a pinned coefficient algebra is not full")
        witness = first_full_rank_combination(matrices)
        witness_matrix = sum(
            (
                coefficient * matrix
                for coefficient, matrix in zip(witness, matrices)
            ),
            np.zeros((size, size), dtype=np.int64),
        )
        full_rank = rank_mod(witness_matrix, 3)
        if full_rank != size:
            raise AssertionError("full-rank witness replay failed")
        algebra_payload.append(
            {
                "component_size": size,
                "algebra_dimension": dimension,
                "full_rank": full_rank,
                "full_rank_multiplier": list(witness),
            }
        )

    quotient_states = 1 << 18
    central_values = 2
    original_per_central = (1 << 20) + (1 << 18)
    contracted_per_central = (1 << 19) + (1 << 18)
    original_total = (
        quotient_states * central_values * original_per_central
    )
    contracted_total = (
        quotient_states * central_values * contracted_per_central
    )
    if original_total != int(global_result["join_rows_total"]):
        raise AssertionError("baseline principal-work count changed")
    two_list_optimum = min(
        (1 << width) + (1 << (37 - width))
        for width in range(38)
    )
    if contracted_per_central != two_list_optimum:
        raise AssertionError("the 19/18 split is not two-list optimal")

    whole_slice = int(global_result["whole_weight_39_supports"])
    if whole_slice % 2:
        raise AssertionError("the characteristic-two slice is not even")

    return {
        "case": 26,
        "block": case.block,
        "q_index": case.index,
        "reflection": {
            "cell_map": "j -> 40-j",
            "negative_lag_equations": 10,
            "positive_lag_equations": 10,
            "noncentral_reflected_pairs": 38,
            "central_fixed_cells": [
                list(keys[int(index)]) for index in pairs[central]
            ],
            "action_on_pair_state": "y_i -> y_i xor p_i (noncentral)",
            "free_on_every_quotient_fiber": True,
        },
        "quotient": {
            "dimension": 18,
            "states": quotient_states,
            "L_pairs": len(left_pairs),
            "S_pairs": len(right_pairs),
            "L_projection_rank": left_rank,
            "L_projection_with_offset_rank": left_augmented_rank,
            "L_zero_parity_pattern_present": False,
            "L_dual_checks": dual_payload,
            "weight_39_supports": whole_slice,
            "reflection_orbit_representatives": whole_slice // 2,
        },
        "contracted_join": {
            "fixed_orientation": "one odd noncentral L-pair y_i = 0",
            "free_L_variables": 19,
            "free_S_variables": 18,
            "central_values": central_values,
            "rows_per_quotient_per_central_before": original_per_central,
            "rows_per_quotient_per_central_after": contracted_per_central,
            "principal_rows_before": original_total,
            "principal_rows_after": contracted_total,
            "principal_rows_saved": original_total - contracted_total,
            "fraction_saved": "2/5",
            "optimal_among_two_table_full_enumeration_joins": True,
            "hash_entries": 1 << 18,
            "hash_memory_increase": 0,
        },
        "walsh_audit": {
            "S_to_L_rank": rank_mod(right_to_left, 2),
            "dual_kernel_dimension": 20 - rank_mod(right_to_left, 2),
            "distinct_quotient_frequencies": 1 << 18,
            "characters_per_frequency": 1 << 2,
            "sparse_frequency_contraction": False,
        },
        "tensor_audit": {
            "S_quotient_vertices": 18,
            "S_quotient_edges": s_edges,
            "S_quotient_primal_graph": "K_18",
            "treewidth_lower_bound": 17,
        },
        "pinned_quadratic_audit": {
            "component_sizes": list(map(len, fixed.components)),
            "components": algebra_payload,
        },
        "scope": (
            "Exact modular-six census contraction only; no whole census, "
            "integer exclusion, BS(84,83), or H(668) is claimed."
        ),
    }


def verify_artifact_hashes() -> None:
    """Check the frozen artifact and exact-input hashes."""

    payload = json.loads(HASHES.read_text())
    if payload.get("algorithm") != "sha256":
        raise AssertionError("artifact hash algorithm changed")
    for relative, expected in payload["files"].items():
        path = (HERE / relative).resolve()
        actual = sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"artifact hash mismatch: {relative}")


def main() -> None:
    verify_artifact_hashes()
    result = derive()
    expected = json.loads(EXPECTED.read_text())
    if result != expected:
        raise AssertionError("derived result differs from frozen certificate")
    print(json.dumps({"status": "PASS", **result}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
