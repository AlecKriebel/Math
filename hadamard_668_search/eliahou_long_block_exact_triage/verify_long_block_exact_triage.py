#!/usr/bin/env python3
"""Verify the exact structural triage of Eliahou long cases 2 through 20.

This is a bounded algebraic audit, not a production search.  It rebuilds
the twenty normalized quadratic equations from the authoritative case
definitions, derives the characteristic-two syndrome quotient, recognizes
the conditioned characteristic-three interaction graph, proves exact
work-count bounds, checks the absence of the short-case reflection gauge,
audits the global L/S split, and computes the characteristic-seven Hasse
jet ranks.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
import random
import sys
import time
from typing import Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
CASCADE = SEARCH / "eliahou_cyclotomic_cascade"
sys.path[:0] = [str(JET), str(CASCADE), str(SEARCH)]

import search_char3_local as local  # noqa: E402
import verify_cyclotomic_cascade as cascade  # noqa: E402
import verify_eliahou_antifold42 as antifold  # noqa: E402


CASES = tuple(range(1, 21))
EXPECTED_Q_INDICES = (
    2, 10, 18, 27, 35, 1, 3, 4, 9, 11, 12, 17, 19, 20, 25, 26, 28, 33,
    34, 36,
)
CERTIFICATE = HERE / "LONG_BLOCK_EXACT_TRIAGE.json"
REFERENCE_JOIN_ROWS_PER_SECOND = 67_122_352.0968

EDGE_XOR = (0, 1, 1, 0)
EDGE_EQUAL = (1, 0, 0, 1)
EDGE_ALL = (1, 1, 1, 1)

# These two deterministic 20-dimensional subcubes are only collision-rate
# controls.  They are not used in any proof or exclusion.
COLLISION_PILOTS = (
    {
        "case": 2,
        "block": "L",
        "variables": (
            3, 5, 6, 7, 8, 9, 11, 13, 15, 20,
            21, 22, 23, 24, 28, 29, 30, 31, 35, 37,
        ),
    },
    {
        "case": 2,
        "block": "S",
        "variables": (
            39, 41, 42, 43, 44, 47, 48, 49, 51, 52,
            54, 56, 57, 61, 64, 67, 70, 73, 74, 76,
        ),
    },
)


def compact_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def rank_mod(matrix: np.ndarray, modulus: int) -> int:
    """Exact row rank over a prime field."""

    work = np.asarray(matrix, dtype=np.int64).copy() % modulus
    row = 0
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        pivot = row + int(choices[0])
        work[[row, pivot]] = work[[pivot, row]]
        work[row] = (
            work[row] * pow(int(work[row, column]), -1, modulus)
        ) % modulus
        for other in range(work.shape[0]):
            if other != row and work[other, column]:
                work[other] = (
                    work[other] - work[other, column] * work[row]
                ) % modulus
        row += 1
        if row == work.shape[0]:
            break
    return row


def affine_parameterization(
    matrix: np.ndarray, rhs: np.ndarray
) -> tuple[tuple[int, ...], np.ndarray, np.ndarray]:
    """Return pivots, a particular point, and a row null basis over F2."""

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
        raise ValueError("inconsistent binary affine system")
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
    if not np.array_equal(matrix @ particular & 1, rhs):
        raise AssertionError("binary particular point failed replay")
    if np.any(matrix @ basis.T & 1):
        raise AssertionError("binary null basis failed replay")
    return tuple(pivots), particular, basis


@lru_cache(maxsize=None)
def parity_configurations(size: int, parity: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        bits
        for bits in product((0, 1), repeat=size)
        if sum(bits) % 2 == parity
    )


def interaction_pattern(
    quadratic: np.ndarray,
    left: Sequence[int],
    right: Sequence[int],
) -> tuple[int, int, int, int]:
    """Return edge presence for parity pairs 00,01,10,11.

    An edge is present exactly when the cross-group potential has a nonzero
    mixed difference modulo three, so the potential cannot be absorbed into
    unary terms.
    """

    result = []
    for left_parity in (0, 1):
        for right_parity in (0, 1):
            left_states = parity_configurations(
                len(left), left_parity
            )
            right_states = parity_configurations(
                len(right), right_parity
            )
            left_zero = left_states[0]
            right_zero = right_states[0]
            found = False
            for left_state in left_states[1:]:
                for right_state in right_states[1:]:
                    difference = np.zeros(20, dtype=np.int64)
                    for left_local, left_variable in enumerate(left):
                        for right_local, right_variable in enumerate(right):
                            multiplier = (
                                left_state[left_local]
                                * right_state[right_local]
                                - left_state[left_local]
                                * right_zero[right_local]
                                - left_zero[left_local]
                                * right_state[right_local]
                                + left_zero[left_local]
                                * right_zero[right_local]
                            )
                            difference += (
                                int(multiplier)
                                * quadratic[
                                    :, left_variable, right_variable
                                ]
                            )
                    if np.any(difference % 3):
                        found = True
                        break
                if found:
                    break
            result.append(int(found))
    return tuple(result)  # type: ignore[return-value]


def mod4_lift_interaction_pattern(
    quadratic: np.ndarray,
    left: Sequence[int],
    right: Sequence[int],
) -> tuple[int, int, int, int]:
    """Return the next-bit edge pattern after the mod-2 quotient is fixed."""

    result = []
    for left_parity in (0, 1):
        for right_parity in (0, 1):
            left_states = parity_configurations(
                len(left), left_parity
            )
            right_states = parity_configurations(
                len(right), right_parity
            )
            left_zero = left_states[0]
            right_zero = right_states[0]
            found = False
            for left_state in left_states[1:]:
                for right_state in right_states[1:]:
                    difference = np.zeros(20, dtype=np.int64)
                    for left_local, left_variable in enumerate(left):
                        for right_local, right_variable in enumerate(right):
                            multiplier = (
                                left_state[left_local]
                                * right_state[right_local]
                                - left_state[left_local]
                                * right_zero[right_local]
                                - left_zero[left_local]
                                * right_state[right_local]
                                + left_zero[left_local]
                                * right_zero[right_local]
                            )
                            difference += (
                                int(multiplier)
                                * quadratic[
                                    :, left_variable, right_variable
                                ]
                            )
                    if np.any(difference & 1):
                        raise AssertionError(
                            "a fixed-quotient mixed difference is odd"
                        )
                    if np.any((difference // 2) & 1):
                        found = True
                        break
                if found:
                    break
            result.append(int(found))
    return tuple(result)  # type: ignore[return-value]


def exact_weight_mod2_count(
    linear: np.ndarray, constant: np.ndarray
) -> int:
    """Count weight-39 points in the twenty-equation affine F2 slice.

    This is the character formula

        2^-20 sum_u (-1)^(u.b) K_39(wt(uH);78).

    Gray order makes the complete 2^20 dual sum a small bounded audit.
    """

    affine = np.remainder(linear, 2).astype(np.uint8)
    rhs = np.remainder(-constant, 2).astype(np.uint8)
    if rank_mod(affine, 2) != 20:
        raise AssertionError("the raw characteristic-two rank changed")
    row_masks = tuple(
        sum(int(affine[row, column]) << column for column in range(78))
        for row in range(20)
    )
    rhs_mask = sum(int(rhs[row]) << row for row in range(20))
    krawtchouk = tuple(
        sum(
            (-1) ** j
            * comb(t, j)
            * comb(78 - t, 39 - j)
            for j in range(max(0, 39 - (78 - t)), min(39, t) + 1)
        )
        for t in range(79)
    )
    codeword = 0
    dual_rhs = 0
    previous_gray = 0
    total = krawtchouk[0]
    for integer in range(1, 1 << 20):
        gray = integer ^ (integer >> 1)
        changed = gray ^ previous_gray
        bit = changed.bit_length() - 1
        codeword ^= row_masks[bit]
        dual_rhs ^= (rhs_mask >> bit) & 1
        summand = krawtchouk[codeword.bit_count()]
        total += -summand if dual_rhs else summand
        previous_gray = gray
    if total % (1 << 20):
        raise AssertionError("MacWilliams character sum is not integral")
    result = total >> 20
    if result <= 0:
        raise AssertionError("the characteristic-two slice is empty")
    return result


def exact_dihedral_symmetries(
    keys: Sequence[tuple[str, int]],
    constant: np.ndarray,
    linear: np.ndarray,
    quadratic: np.ndarray,
) -> dict[str, object]:
    """Audit blockwise cell-dihedral maps preserving this support domain."""

    key_index = {key: index for index, key in enumerate(keys)}
    options: dict[str, list[tuple[int, int]]] = {}
    for block in ("L", "S"):
        cells = {cell for key_block, cell in keys if key_block == block}
        block_options = []
        for slope in (1, -1):
            for offset in range(42):
                image = {
                    (slope * cell + offset) % 42 for cell in cells
                }
                if image == cells:
                    block_options.append((slope, offset))
        options[block] = block_options

    exact = []
    for long_map in options["L"]:
        for short_map in options["S"]:
            permutation = []
            for block, cell in keys:
                slope, offset = (
                    long_map if block == "L" else short_map
                )
                permutation.append(
                    key_index[(block, (slope * cell + offset) % 42)]
                )
            permutation_array = np.asarray(permutation, dtype=np.int64)
            lag_signs = []
            valid = True
            for lag in range(20):
                signs = [
                    sign
                    for sign in (1, -1)
                    if (
                        constant[lag] == sign * constant[lag]
                        and np.array_equal(
                            linear[lag, permutation_array],
                            sign * linear[lag],
                        )
                        and np.array_equal(
                            quadratic[lag, permutation_array][
                                :, permutation_array
                            ],
                            sign * quadratic[lag],
                        )
                    )
                ]
                if not signs:
                    valid = False
                    break
                lag_signs.append(signs[0])
            if valid:
                exact.append(
                    {
                        "L": list(long_map),
                        "S": list(short_map),
                        "lag_signs": lag_signs,
                    }
                )
    if options["L"] != [(1, 0)]:
        raise AssertionError("a long support-domain reflection emerged")
    if options["S"] != [(1, 0), (-1, 40)]:
        raise AssertionError("the short support-domain maps changed")
    if len(exact) != 1 or (
        exact[0]["L"] != [1, 0] or exact[0]["S"] != [1, 0]
    ):
        raise AssertionError("a nontrivial within-case reflection emerged")
    return {
        "domain_preserving_blockwise_dihedral_maps": (
            len(options["L"]) * len(options["S"])
        ),
        "exact_polynomial_symmetries": len(exact),
        "nontrivial_exact_symmetries": len(exact) - 1,
        "free_reflection_gauge": False,
    }


def hasse_jet_matrix(contents: Sequence[int]) -> tuple[np.ndarray, ...]:
    """Map the twenty independent lags to seven mod-7 Hasse layers."""

    if len(contents) != 20 or any(content % 7 == 0 for content in contents):
        raise AssertionError("a normalized lag content vanished modulo seven")
    layers = []
    for derivative in range(7):
        layer = np.zeros((6, 20), dtype=np.int64)
        for column, lag in enumerate(range(1, 21)):
            for exponent, coefficient_sign in (
                (lag, 1),
                (42 - lag, -1),
            ):
                if exponent < derivative:
                    continue
                reduced_exponent = exponent - derivative
                quotient, residue = divmod(reduced_exponent, 6)
                layer[residue, column] += (
                    coefficient_sign
                    * int(contents[column])
                    * comb(exponent, derivative)
                    * (-1 if quotient % 2 else 1)
                )
        layers.append(layer % 7)
    return tuple(layers)


def f49_factor_ranks(
    layers: Sequence[np.ndarray],
) -> dict[str, object]:
    """Decompose z^6+1 into its three irreducible quadratic factors."""

    result = {}
    for factor_constant in (1, 2, 4):
        factor_layers = []
        for layer in layers:
            reduced = np.zeros((2, 20), dtype=np.int64)
            for exponent in range(6):
                quotient, residue = divmod(exponent, 2)
                reduced[residue] += (
                    layer[exponent]
                    * pow(-factor_constant, quotient, 7)
                )
            factor_layers.append(reduced % 7)
        result[f"z2_plus_{factor_constant}"] = {
            "layer_ranks": [
                rank_mod(layer, 7) for layer in factor_layers
            ],
            "cumulative_ranks": [
                rank_mod(np.vstack(factor_layers[: stop + 1]), 7)
                for stop in range(7)
            ],
        }
    expected = {
        "z2_plus_1": {
            "layer_ranks": [1, 1, 2, 2, 2, 2, 2],
            "cumulative_ranks": [1, 2, 3, 4, 5, 6, 7],
        },
        "z2_plus_2": {
            "layer_ranks": [2, 2, 2, 2, 2, 2, 2],
            "cumulative_ranks": [2, 4, 6, 8, 10, 12, 14],
        },
        "z2_plus_4": {
            "layer_ranks": [2, 2, 2, 2, 2, 2, 2],
            "cumulative_ranks": [2, 4, 6, 8, 10, 12, 14],
        },
    }
    if result != expected:
        raise AssertionError("the F49 local-factor ranks changed")
    return result


def unrestricted_char7_local_count() -> dict[str, object]:
    """Verify the unrestricted two-polynomial seven-jet branch count."""

    target = 334 % 7
    if target != 5:
        raise AssertionError("the characteristic-seven target changed")

    # In F_49 = F_7[u]/(u^2+1), Norm(a+bu)=a^2+b^2.
    norms = Counter(
        (a * a + b * b) % 7
        for a in range(7)
        for b in range(7)
    )
    self_factor_base = sum(
        left_count * norms[(target - left_norm) % 7]
        for left_norm, left_count in norms.items()
    )
    if self_factor_base != 336:
        raise AssertionError("the self-F49 base count changed")

    # On the swapped pair of F49 factors, a nonzero 2-vector has a
    # 49-point affine dot-product fibre for a nonzero target.
    swapped_factor_base = (49 ** 2 - 1) * 49
    if swapped_factor_base != 117_600:
        raise AssertionError("the swapped-F49 base count changed")
    self_lift_per_layer = 7 ** 3
    swapped_lift_per_layer = 49 ** 3
    total = (
        self_factor_base
        * swapped_factor_base
        * (self_lift_per_layer ** 6)
        * (swapped_lift_per_layer ** 6)
    )
    return {
        "target_mod7": target,
        "singular_target_branch": False,
        "self_F49_base_solutions": self_factor_base,
        "self_F49_lifts_per_higher_jet": self_lift_per_layer,
        "swapped_F49_pair_base_solutions": swapped_factor_base,
        "swapped_F49_pair_lifts_per_higher_jet": swapped_lift_per_layer,
        "higher_jet_layers": 6,
        "unrestricted_PQ_solution_count": str(total),
        "ambient_F7_coefficients": 84,
        "equation_codimension": 21,
        "conclusion": (
            "triangularity repackages the 21 norm constraints; without "
            "the Boolean alphabet it gives no additional contraction"
        ),
    }


def derive_case(case_number: int) -> dict[str, object]:
    case, keys, equations, constant, linear, quadratic = local.arrays(
        case_number
    )
    expected_index = EXPECTED_Q_INDICES[case_number - CASES[0]]
    if (case.block, case.index) != ("L", expected_index):
        raise AssertionError("canonical long-case ordering changed")
    if (
        len(keys) != 78
        or constant.shape != (20,)
        or linear.shape != (20, 78)
        or quadratic.shape != (20, 78, 78)
    ):
        raise AssertionError("long-case integer model dimensions changed")
    if np.any(quadratic & 1):
        raise AssertionError("the characteristic-two layer is not affine")

    affine = np.remainder(linear, 2).astype(np.uint8)
    groups_by_syndrome: dict[tuple[int, ...], list[int]] = {}
    for variable in range(78):
        syndrome = tuple(map(int, affine[:, variable]))
        groups_by_syndrome.setdefault(syndrome, []).append(variable)
    groups = tuple(
        tuple(group) for group in groups_by_syndrome.values()
    )
    quotient_matrix = np.asarray(
        tuple(groups_by_syndrome), dtype=np.uint8
    ).T
    quotient_with_weight = np.vstack(
        (
            quotient_matrix,
            np.ones((1, len(groups)), dtype=np.uint8),
        )
    )
    quotient_rhs = np.append(
        np.remainder(-constant, 2), 1
    ).astype(np.uint8)
    pivots, particular, basis = affine_parameterization(
        quotient_with_weight, quotient_rhs
    )
    quotient_dimension = len(groups) - len(pivots)
    nontrivial = tuple(
        index for index, group in enumerate(groups) if len(group) > 1
    )
    if (
        len(pivots) != 21
        or len(nontrivial) != 19
        or rank_mod(basis[:, nontrivial], 2) != 19
    ):
        raise AssertionError("the long quotient rank profile changed")

    patterns: dict[tuple[int, int], tuple[int, int, int, int]] = {}
    pattern_counts: Counter[tuple[int, int, int, int]] = Counter()
    for left_local, left in enumerate(nontrivial):
        for right_local in range(left_local + 1, len(nontrivial)):
            right = nontrivial[right_local]
            pattern = interaction_pattern(
                quadratic, groups[left], groups[right]
            )
            patterns[(left_local, right_local)] = pattern
            pattern_counts[pattern] += 1
    if not set(pattern_counts) <= {EDGE_XOR, EDGE_EQUAL, EDGE_ALL}:
        raise AssertionError("an unclassified interaction pattern appeared")

    universal = tuple(
        vertex
        for vertex in range(19)
        if all(
            patterns[tuple(sorted((vertex, other)))] == EDGE_ALL
            for other in range(19)
            if other != vertex
        )
    )
    ordinary = tuple(vertex for vertex in range(19) if vertex not in universal)
    if any(len(groups[nontrivial[vertex]]) != 3 for vertex in universal):
        raise AssertionError("a universal vertex is not a mixed triple")
    if any(len(groups[nontrivial[vertex]]) != 2 for vertex in ordinary):
        raise AssertionError("an ordinary vertex is not a reflected pair")

    phases: dict[int, int] = {}
    if ordinary:
        phases[ordinary[0]] = 0
        for vertex in ordinary[1:]:
            pattern = patterns[
                tuple(sorted((ordinary[0], vertex)))
            ]
            if pattern == EDGE_EQUAL:
                phases[vertex] = 0
            elif pattern == EDGE_XOR:
                phases[vertex] = 1
            else:
                raise AssertionError("an ordinary edge is universal")
        for left_index, left in enumerate(ordinary):
            for right in ordinary[left_index + 1:]:
                wanted = (
                    EDGE_EQUAL
                    if phases[left] == phases[right]
                    else EDGE_XOR
                )
                if patterns[(min(left, right), max(left, right))] != wanted:
                    raise AssertionError("the two-clique phase law failed")

    expected_universal = 1 if case_number == 6 else (
        2 if case_number in (1, 14) else 0
    )
    if len(universal) != expected_universal:
        raise AssertionError("the exceptional separator size changed")
    phase_sizes = sorted(Counter(phases.values()).values(), reverse=True)
    if phase_sizes != sorted(
        ((10, 9) if not universal else ((9, 9) if len(universal) == 1 else (9, 8))),
        reverse=True,
    ):
        raise AssertionError("the conditioned clique sizes changed")

    mod4_patterns: Counter[tuple[int, int, int, int]] = Counter()
    for left_local, left in enumerate(nontrivial):
        for right in nontrivial[left_local + 1:]:
            mod4_patterns[
                mod4_lift_interaction_pattern(
                    quadratic, groups[left], groups[right]
                )
            ] += 1
    expected_mod4_patterns = Counter(
        {
            (0, 0, 0, 0): comb(19 - len(universal), 2),
            EDGE_ALL: (
                len(universal) * (19 - len(universal))
                + comb(len(universal), 2)
            ),
        }
    )
    expected_mod4_patterns += Counter()
    if mod4_patterns != +expected_mod4_patterns:
        raise AssertionError("the conditioned mod-4 interaction graph changed")

    separator_states = 4 ** len(universal)
    ordinary_vertices = len(ordinary)
    minimum_component_rows = separator_states * (
        (1 << (ordinary_vertices // 2))
        + (1 << (ordinary_vertices - ordinary_vertices // 2))
    )
    quotient_fiber = 1 << (quotient_dimension - 19)
    gross_component_rows = (
        quotient_fiber
        * (1 << len(universal))
        * separator_states
        * 2
        * (3 ** ordinary_vertices)
    )

    mod2_supports = exact_weight_mod2_count(linear, constant)
    internal_bits = 78 - len(groups)
    feasible_quotient_lower_bound = (
        mod2_supports + (1 << internal_bits) - 1
    ) >> internal_bits
    component_rows_lower_bound = (
        feasible_quotient_lower_bound * minimum_component_rows
    )

    block_indices = {
        block: tuple(
            index
            for index, (key_block, _) in enumerate(keys)
            if key_block == block
        )
        for block in ("L", "S")
    }
    if any(len(indices) != 39 for indices in block_indices.values()):
        raise AssertionError("the long/short variable split changed")
    if np.any(
        quadratic[:, block_indices["L"]][
            :, :, block_indices["S"]
        ]
    ):
        raise AssertionError("a cross-block quadratic term appeared")
    half_cross_edges = {}
    raw_block_edges = {}
    for block, indices in block_indices.items():
        left = indices[:20]
        right = indices[20:]
        half_cross_edges[block] = sum(
            bool(np.any(quadratic[:, i, j] % 6))
            for i in left
            for j in right
        )
        raw_block_edges[block] = sum(
            bool(np.any(quadratic[:, i, j] % 6))
            for offset, i in enumerate(indices)
            for j in indices[offset + 1:]
        )

    contents = tuple(int(equation.content) for equation in equations)
    hasse_layers = hasse_jet_matrix(contents)
    layer_ranks = [rank_mod(layer, 7) for layer in hasse_layers]
    cumulative_ranks = [
        rank_mod(np.vstack(hasse_layers[: stop + 1]), 7)
        for stop in range(7)
    ]
    if layer_ranks != [3, 3, 6, 6, 6, 6, 6]:
        raise AssertionError("the individual Hasse-jet ranks changed")
    if cumulative_ranks != [3, 6, 9, 12, 15, 18, 20]:
        raise AssertionError("the cumulative Hasse-jet ranks changed")
    hasse_increments = [
        cumulative_ranks[0],
        *[
            cumulative_ranks[index] - cumulative_ranks[index - 1]
            for index in range(1, 7)
        ],
    ]
    quadratic_flat = np.remainder(
        quadratic.reshape(20, -1), 7
    ).astype(np.int64)
    quadratic_cumulative_ranks = [
        rank_mod(
            np.remainder(
                np.vstack(hasse_layers[: stop + 1]) @ quadratic_flat,
                7,
            ),
            7,
        )
        for stop in range(7)
    ]
    if quadratic_cumulative_ranks != cumulative_ranks:
        raise AssertionError(
            "a characteristic-seven jet became affine in the support bits"
        )
    mod7_linear_ranks = {
        "whole": rank_mod(linear, 7),
        "L": rank_mod(linear[:, block_indices["L"]], 7),
        "S": rank_mod(linear[:, block_indices["S"]], 7),
    }
    if set(mod7_linear_ranks.values()) != {20}:
        raise AssertionError("a mod-7 linear projection lost rank")
    if sum(bool(np.any(equation % 7)) for equation in quadratic) != 20:
        raise AssertionError("a mod-7 quadratic equation vanished")

    mixed_groups = [
        [list(keys[variable]) for variable in group]
        for group in groups
        if len({keys[variable][0] for variable in group}) > 1
    ]
    model_hasher = hashlib.sha256()
    model_hasher.update(
        json.dumps(keys, separators=(",", ":")).encode("ascii")
    )
    for array in (constant, linear, quadratic):
        model_hasher.update(np.asarray(array, dtype="<i2").tobytes())

    return {
        "case": case_number,
        "q_index": case.index,
        "signature": list(case.signature),
        "variables": 78,
        "block_variables": {"L": 39, "S": 39},
        "model_sha256": model_hasher.hexdigest(),
        "mod2": {
            "raw_rank": rank_mod(affine, 2),
            "syndrome_classes": len(groups),
            "class_size_counts": {
                str(size): count
                for size, count in sorted(Counter(map(len, groups)).items())
            },
            "quotient_rank_with_weight_parity": len(pivots),
            "quotient_dimension": quotient_dimension,
            "quotient_states": str(1 << quotient_dimension),
            "nontrivial_classes": len(nontrivial),
            "nontrivial_parity_projection_rank": rank_mod(
                basis[:, nontrivial], 2
            ),
            "mixed_classes": mixed_groups,
            "particular_sha256": compact_hash(particular.tolist()),
            "basis_sha256": compact_hash(basis.tolist()),
            "exact_weight_39_supports": str(mod2_supports),
        },
        "conditioned_mod3_graph": {
            "vertices": 19,
            "universal_mixed_triple_separator_vertices": len(universal),
            "ordinary_reflected_pair_vertices": ordinary_vertices,
            "phase_sizes_at_zero_parity": phase_sizes,
            "edge_pattern_counts": {
                "".join(map(str, pattern)): count
                for pattern, count in sorted(pattern_counts.items())
            },
            "family": (
                f"K_{len(universal)} join "
                f"(K_a disjoint-union K_{ordinary_vertices}-a)"
                if universal
                else f"K_a disjoint-union K_{ordinary_vertices}-a"
            ),
            "possible_component_sizes": (
                [[19]]
                if universal
                else [[19 - small, small] if small else [19]
                      for small in range(10)]
            ),
            "exact_treewidth_range": [
                len(universal)
                + max(
                    ordinary_vertices // 2,
                    ordinary_vertices - ordinary_vertices // 2,
                )
                - 1,
                18,
            ],
            "separator_domain_states": separator_states,
            "exact_fixed_quotient_mitm": True,
        },
        "conditioned_mod4_lift": {
            "equations": (
                "normalized residual divided by 2, modulo 2, on a "
                "fixed characteristic-two quotient"
            ),
            "edge_pattern_counts": {
                "".join(map(str, pattern)): count
                for pattern, count in sorted(mod4_patterns.items())
            },
            "factor_graph": (
                f"K_{len(universal)} join independent_"
                f"{19 - len(universal)}"
            ),
            "exact_treewidth": len(universal),
            "ordinary_pair_variables": 19 - len(universal),
            "mixed_triple_separator_variables": len(universal),
            "linear_after_conditioning_separator": True,
        },
        "reflection": exact_dihedral_symmetries(
            keys, constant, linear, quadratic
        ),
        "work": {
            "internal_bits_per_quotient": internal_bits,
            "maximum_physical_supports_per_quotient": str(
                1 << internal_bits
            ),
            "feasible_quotients_lower_bound": str(
                feasible_quotient_lower_bound
            ),
            "minimum_component_rows_per_feasible_quotient": str(
                minimum_component_rows
            ),
            "rigorous_component_rows_lower_bound": str(
                component_rows_lower_bound
            ),
            "gross_component_rows_all_quotients": str(
                gross_component_rows
            ),
            "lower_bound_hours_at_reference_short_kernel_rate": (
                component_rows_lower_bound
                / REFERENCE_JOIN_ROWS_PER_SECOND
                / 3600
            ),
            "gross_hours_at_reference_short_kernel_rate": (
                gross_component_rows
                / REFERENCE_JOIN_ROWS_PER_SECOND
                / 3600
            ),
        },
        "global_split": {
            "cross_block_quadratic_terms": 0,
            "raw_block_interaction_edges": raw_block_edges,
            "natural_20_by_19_cross_edges": half_cross_edges,
            "natural_20_by_19_possible_edges": 380,
        },
        "mod7": {
            "identity": "z^42+1=(z^6+1)^7 over F_7",
            "hasse_layer_ranks": layer_ranks,
            "hasse_cumulative_ranks": cumulative_ranks,
            "hasse_incremental_ranks": hasse_increments,
            "residual_branch_reductions": [
                str(7 ** rank) for rank in hasse_increments
            ],
            "F49_factor_ranks": f49_factor_ranks(hasse_layers),
            "quadratic_span_cumulative_ranks": (
                quadratic_cumulative_ranks
            ),
            "full_residual_state_count": str(7 ** 20),
            "full_residual_plus_weight_bits": (
                (40 * (7 ** 20) - 1).bit_length()
            ),
            "linear_ranks": mod7_linear_ranks,
            "quadratic_nonzero_equations": 20,
            "smaller_exact_quotient": False,
            "sequentially_linear_in_boolean_support": False,
        },
    }


def bounded_mod4_rank_control(
    case_number: int, quotient_samples: int = 64
) -> dict[str, object]:
    """Sample exact next-bit ranks on representative affine quotients.

    The interaction-graph classification is exhaustive.  This additional
    control only measures rank/consistency variation; its distributions are
    not promoted to whole-quotient counts.
    """

    case, keys, _, constant, linear, quadratic = local.arrays(case_number)
    affine = np.remainder(linear, 2).astype(np.uint8)
    groups_by_syndrome: dict[tuple[int, ...], list[int]] = {}
    for variable in range(len(keys)):
        groups_by_syndrome.setdefault(
            tuple(map(int, affine[:, variable])), []
        ).append(variable)
    groups = tuple(
        tuple(group) for group in groups_by_syndrome.values()
    )
    quotient_matrix = np.asarray(
        tuple(groups_by_syndrome), dtype=np.uint8
    ).T
    quotient_with_weight = np.vstack(
        (
            quotient_matrix,
            np.ones((1, len(groups)), dtype=np.uint8),
        )
    )
    quotient_rhs = np.append(
        np.remainder(-constant, 2), 1
    ).astype(np.uint8)
    _, particular, basis = affine_parameterization(
        quotient_with_weight, quotient_rhs
    )
    ordinary = tuple(
        group_index
        for group_index, group in enumerate(groups)
        if len(group) == 2
    )
    separators = tuple(
        group_index
        for group_index, group in enumerate(groups)
        if len(group) == 3
    )
    if len(ordinary) + len(separators) != 19:
        raise AssertionError("the mod-4 control group count changed")

    generator = random.Random(668_400 + case_number)
    rank_counts: Counter[int] = Counter()
    solution_counts: Counter[int] = Counter()
    conditioned_systems = 0
    for _ in range(quotient_samples):
        coefficients = np.array(
            [generator.getrandbits(1) for _ in range(len(basis))],
            dtype=np.uint8,
        )
        quotient = particular ^ (
            (coefficients @ basis) & 1
        ).astype(np.uint8)
        base = np.zeros(len(keys), dtype=np.int16)
        for group_index, group in enumerate(groups):
            base[list(group)] = parity_configurations(
                len(group), int(quotient[group_index])
            )[0]

        separator_state_ranges = tuple(
            range(
                len(
                    parity_configurations(
                        len(groups[group_index]),
                        int(quotient[group_index]),
                    )
                )
            )
            for group_index in separators
        )
        for separator_choices in product(*separator_state_ranges):
            point = base.copy()
            for group_index, choice in zip(
                separators, separator_choices
            ):
                point[list(groups[group_index])] = (
                    parity_configurations(
                        len(groups[group_index]),
                        int(quotient[group_index]),
                    )[choice]
                )
            baseline = local.exact_values(
                point, constant, linear, quadratic
            ).astype(np.int64)
            if np.any(baseline & 1):
                raise AssertionError("a quotient point failed mod two")
            columns = []
            for group_index in ordinary:
                alternative = point.copy()
                alternative[list(groups[group_index])] = (
                    parity_configurations(
                        2, int(quotient[group_index])
                    )[1]
                )
                difference = (
                    local.exact_values(
                        alternative, constant, linear, quadratic
                    ).astype(np.int64)
                    - baseline
                )
                if np.any(difference & 1):
                    raise AssertionError(
                        "a fixed-quotient mod-4 difference is odd"
                    )
                columns.append(np.remainder(difference // 2, 2))
            matrix = np.asarray(columns, dtype=np.uint8).T
            rhs = np.remainder(-baseline // 2, 2).astype(np.uint8)
            rank = rank_mod(matrix, 2)
            augmented_rank = rank_mod(
                np.column_stack((matrix, rhs)), 2
            )
            rank_counts[rank] += 1
            if augmented_rank == rank:
                solution_counts[1 << (len(ordinary) - rank)] += 1
            else:
                solution_counts[0] += 1
            conditioned_systems += 1

    return {
        "case": case_number,
        "q_index": case.index,
        "scope": (
            "bounded deterministic rank/consistency sample; graph "
            "classification is exhaustive but these frequencies are not"
        ),
        "quotient_samples": quotient_samples,
        "separator_conditions_per_quotient": 4 ** len(separators),
        "conditioned_linear_systems": conditioned_systems,
        "ordinary_variables": len(ordinary),
        "separator_variables": len(separators),
        "observed_rank_counts": {
            str(rank): count for rank, count in sorted(rank_counts.items())
        },
        "observed_solution_multiplicity_counts": {
            str(count): frequency
            for count, frequency in sorted(solution_counts.items())
        },
    }


def grouped_affine_coordinates(
    case_number: int,
) -> tuple[
    tuple[object, ...],
    tuple[tuple[str, int], ...],
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    int,
]:
    """Return an orientation-aware 57-coordinate affine mod-2 model."""

    case, keys, equations, constant, linear, quadratic = local.arrays(
        case_number
    )
    affine = np.remainder(linear, 2).astype(np.uint8)
    groups_by_syndrome: dict[tuple[int, ...], list[int]] = {}
    for variable in range(len(keys)):
        groups_by_syndrome.setdefault(
            tuple(map(int, affine[:, variable])), []
        ).append(variable)
    groups = tuple(
        tuple(group) for group in groups_by_syndrome.values()
    )
    quotient_matrix = np.asarray(
        tuple(groups_by_syndrome), dtype=np.uint8
    ).T
    quotient_with_weight = np.vstack(
        (
            quotient_matrix,
            np.ones((1, len(groups)), dtype=np.uint8),
        )
    )
    quotient_rhs = np.append(
        np.remainder(-constant, 2), 1
    ).astype(np.uint8)
    _, quotient_particular, quotient_basis = affine_parameterization(
        quotient_with_weight, quotient_rhs
    )
    outer_dimension = len(quotient_basis)
    inner_dimension = sum(len(group) - 1 for group in groups)
    if outer_dimension + inner_dimension != 57:
        raise AssertionError("the affine null dimension changed")

    physical_particular = np.zeros(78, dtype=np.uint8)
    physical_basis = np.zeros((57, 78), dtype=np.uint8)
    inner_coordinate = outer_dimension
    for group_index, group in enumerate(groups):
        last = group[-1]
        physical_particular[last] = quotient_particular[group_index]
        physical_basis[:outer_dimension, last] = (
            quotient_basis[:, group_index]
        )
        for variable in group[:-1]:
            physical_basis[inner_coordinate, variable] = 1
            physical_basis[inner_coordinate, last] = 1
            inner_coordinate += 1
    if inner_coordinate != 57:
        raise AssertionError("failed to allocate the inner coordinates")

    raw_matrix = np.vstack(
        (affine, np.ones((1, 78), dtype=np.uint8))
    )
    raw_rhs = np.append(
        np.remainder(-constant, 2), 1
    ).astype(np.uint8)
    if not np.array_equal(
        raw_matrix @ physical_particular & 1, raw_rhs
    ):
        raise AssertionError("the grouped physical point failed replay")
    if np.any(raw_matrix @ physical_basis.T & 1):
        raise AssertionError("the grouped physical basis failed replay")
    return (
        (case, equations, groups),
        keys,
        constant,
        linear,
        quadratic,
        np.vstack((physical_particular, physical_basis)),
        outer_dimension,
    )


def derive_mod4_anf(
    case_number: int,
) -> tuple[dict[str, object], tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Derive the exact twenty quadratic next-bit forms on 57 coordinates."""

    (
        metadata,
        keys,
        constant,
        linear,
        quadratic,
        affine_payload,
        outer_dimension,
    ) = grouped_affine_coordinates(case_number)
    case = metadata[0]
    physical_particular = affine_payload[0]
    physical_basis = affine_payload[1:]
    if np.any(quadratic & 1):
        raise AssertionError(
            "odd cross coefficients could create cubic next-bit terms"
        )

    coordinate_points = [0]
    coordinate_points.extend(1 << coordinate for coordinate in range(57))
    coordinate_points.extend(
        (1 << left) | (1 << right)
        for left in range(57)
        for right in range(left + 1, 57)
    )
    coordinates = np.zeros(
        (len(coordinate_points), 57), dtype=np.uint8
    )
    for row, mask in enumerate(coordinate_points):
        for coordinate in range(57):
            coordinates[row, coordinate] = (mask >> coordinate) & 1
    physical = (
        physical_particular[np.newaxis, :]
        ^ ((coordinates @ physical_basis) & 1)
    ).astype(np.int16)
    values = (
        constant[np.newaxis, :]
        + physical @ linear.T
        + np.einsum(
            "bi,eij,bj->be", physical, quadratic, physical
        )
        // 2
    )
    if np.any(values & 1):
        raise AssertionError("a parameterized point failed mod two")
    half_values = np.remainder(values // 2, 2).astype(np.uint8).T
    anf_constant = half_values[:, 0]
    anf_linear = (
        half_values[:, 1:58] ^ anf_constant[:, np.newaxis]
    )
    anf_quadratic = np.zeros((20, 57, 57), dtype=np.uint8)
    row = 58
    for left in range(57):
        for right in range(left + 1, 57):
            anf_quadratic[:, left, right] = (
                half_values[:, row]
                ^ half_values[:, 1 + left]
                ^ half_values[:, 1 + right]
                ^ anf_constant
            )
            row += 1
    if row != len(coordinate_points):
        raise AssertionError("the ANF interpolation indexing failed")

    # The degree-two bound is exact, not inferred from these controls:
    # XOR-affine coordinates truncate at degree two modulo four, while all
    # original cross coefficients are even.  Random higher-weight replay
    # guards the implementation of that algebraic identity.
    generator = random.Random(668_440 + case_number)
    for _ in range(128):
        coordinate = np.array(
            [generator.getrandbits(1) for _ in range(57)],
            dtype=np.uint8,
        )
        chosen = (
            physical_particular
            ^ ((coordinate @ physical_basis) & 1)
        ).astype(np.int16)
        direct = np.remainder(
            local.exact_values(
                chosen, constant, linear, quadratic
            )
            // 2,
            2,
        ).astype(np.uint8)
        predicted = anf_constant ^ (
            (anf_linear @ coordinate) & 1
        )
        for left in np.flatnonzero(coordinate):
            predicted ^= (
                anf_quadratic[:, left] @ coordinate
            ) & 1
        if not np.array_equal(direct, predicted):
            raise AssertionError("the quadratic mod-4 ANF failed replay")

    upper_all = np.asarray(
        [
            [
                anf_quadratic[equation, left, right]
                for left in range(57)
                for right in range(left + 1, 57)
            ]
            for equation in range(20)
        ],
        dtype=np.uint8,
    )
    upper_outer = np.asarray(
        [
            [
                anf_quadratic[equation, left, right]
                for left in range(outer_dimension)
                for right in range(left + 1, outer_dimension)
            ]
            for equation in range(20)
        ],
        dtype=np.uint8,
    )
    outer_edges = sum(
        bool(np.any(anf_quadratic[:, left, right]))
        for left in range(outer_dimension)
        for right in range(left + 1, outer_dimension)
    )
    outer_inner_edges = sum(
        bool(np.any(anf_quadratic[:, left, right]))
        for left in range(outer_dimension)
        for right in range(outer_dimension, 57)
    )
    inner_edges = sum(
        bool(np.any(anf_quadratic[:, left, right]))
        for left in range(outer_dimension, 57)
        for right in range(left + 1, 57)
    )
    all_edges = outer_edges + outer_inner_edges + inner_edges
    outer_possible = comb(outer_dimension, 2)
    hasher = hashlib.sha256()
    for array in (anf_constant, anf_linear, anf_quadratic):
        hasher.update(np.asarray(array, dtype=np.uint8).tobytes())

    result = {
        "case": case_number,
        "q_index": case.index,
        "free_coordinates": 57,
        "outer_quotient_coordinates": outer_dimension,
        "inner_orientation_coordinates": 57 - outer_dimension,
        "equations": 20,
        "exact_algebraic_degree": 2,
        "degree_proof": (
            "the raw characteristic-two constraints make every residual "
            "even; XOR substitution modulo four has degree at most two, "
            "and every original quadratic cross coefficient is even"
        ),
        "quadratic_coefficient_row_rank": rank_mod(upper_all, 2),
        "outer_quadratic_coefficient_row_rank": rank_mod(
            upper_outer, 2
        ),
        "quadratic_union_edges": all_edges,
        "outer_quadratic_union_edges": outer_edges,
        "outer_quadratic_possible_edges": outer_possible,
        "outer_quadratic_density": outer_edges / outer_possible,
        "outer_inner_bilinear_union_edges": outer_inner_edges,
        "inner_quadratic_union_edges": inner_edges,
        "anf_sha256": hasher.hexdigest(),
        "exact_low_degree_sat_encoding": (
            "21 affine XOR equations plus 20 quadratic XOR equations "
            "with auxiliary AND variables"
        ),
        "outer_compatibility_warning": (
            "the existential orientation system is quadratic and dense "
            "in the outer quotient; determinant/minor elimination is not "
            "a low-rank linear condition"
        ),
    }
    if (
        result["quadratic_coefficient_row_rank"] != 20
        or result["outer_quadratic_coefficient_row_rank"] != 20
    ):
        raise AssertionError("the mod-4 quadratic equation span changed")
    return result, (anf_constant, anf_linear, anf_quadratic)


def arithmetic_block_specification(
    block: str, index: int, side: str
) -> tuple[object, int]:
    """Rebuild the modulus-14 arithmetic fingerprint used by the cascade."""

    pair_rows = cascade.normalized_pair_rows(
        cascade.q_adjusted_rows(block, index)
    )
    long_cells, short_cells = antifold.available_s_support_cells(
        block, index
    )
    row, cells = (
        (pair_rows[0], long_cells)
        if side == "P"
        else (pair_rows[1], short_cells)
    )
    baseline = cascade.reduce_negacyclic(row, 14)
    option_groups = []
    for residue in range(14):
        states: Counter[tuple[int, int]] = Counter(
            {(0, baseline[residue]): 1}
        )
        for cell in (cell for cell in cells if cell % 14 == residue):
            contribution = (
                (-1 if (cell // 14) % 2 else 1) * row[cell]
            )
            following = states.copy()
            for (weight, value), multiplicity in states.items():
                following[(weight + 1, value - contribution)] += multiplicity
            states = following
        option_groups.append(
            tuple(
                (weight, value, multiplicity)
                for (weight, value), multiplicity in sorted(states.items())
            )
        )
    fingerprint = (side, baseline, tuple(option_groups))
    raw_tuples = 1
    for group in option_groups:
        raw_tuples *= len(group)
    return fingerprint, raw_tuples


def derive_global_split() -> dict[str, object]:
    cases = cascade.canonical_cases()
    if len(cases) != 30:
        raise AssertionError("the canonical case count changed")
    records: dict[tuple[object, ...], dict[str, object]] = {}
    case_fingerprints: dict[tuple[int, str], tuple[object, ...]] = {}
    for case_number, (block, index) in enumerate(cases):
        for side in ("P", "Q"):
            fingerprint, raw_tuples = arithmetic_block_specification(
                block, index, side
            )
            case_fingerprints[(case_number, side)] = fingerprint
            if fingerprint not in records:
                records[fingerprint] = {
                    "side": side,
                    "cases": [],
                    "mod14_raw_coefficient_tuples": raw_tuples,
                }
            records[fingerprint]["cases"].append(case_number)  # type: ignore[index]
    if len(records) != 26:
        raise AssertionError("the 26 arithmetic specifications changed")
    total_mod14_tuples = sum(
        int(record["mod14_raw_coefficient_tuples"])
        for record in records.values()
    )
    if total_mod14_tuples != 328_470_183_936:
        raise AssertionError("the modulus-14 growth total changed")

    open_long_specs = {
        case_fingerprints[(case_number, side)]
        for case_number in CASES
        for side in ("P", "Q")
    }
    open_long_p_specs = {
        case_fingerprints[(case_number, "P")]
        for case_number in CASES
    }
    open_long_q_specs = {
        case_fingerprints[(case_number, "Q")]
        for case_number in CASES
    }
    primary_specs = {
        case_fingerprints[(case_number, side)]
        for case_number in range(2, 21)
        for side in ("P", "Q")
    }
    if (
        len(open_long_specs),
        len(open_long_p_specs),
        len(open_long_q_specs),
        len(primary_specs),
    ) != (19, 18, 1, 18):
        raise AssertionError("the long-case block reuse count changed")

    per_block_states = 1 << 39
    per_case_states = 2 * per_block_states
    unique_open_long_states = len(open_long_specs) * per_block_states
    unique_primary_states = len(primary_specs) * per_block_states
    all_unique_states = len(records) * per_block_states
    reference_rate = REFERENCE_JOIN_ROWS_PER_SECOND

    return {
        "exact_additive_split": "long block contribution + short block contribution",
        "states_per_39_bit_block": str(per_block_states),
        "raw_states_per_case": str(per_case_states),
        "all_30_cases_unique_arithmetic_specs": len(records),
        "all_30_cases_raw_unique_spec_states": str(all_unique_states),
        "cases_2_20_unique_arithmetic_specs": len(primary_specs),
        "cases_2_20_raw_unique_spec_states": str(unique_primary_states),
        "open_cases_1_20_unique_arithmetic_specs": len(open_long_specs),
        "open_cases_1_20_unique_P_specs": len(open_long_p_specs),
        "open_cases_1_20_unique_Q_specs": len(open_long_q_specs),
        "open_cases_1_20_raw_unique_spec_states": str(
            unique_open_long_states
        ),
        "raw_per_case_hours_at_reference_short_kernel_rate": (
            per_case_states / reference_rate / 3600
        ),
        "raw_unique_open_long_hours_at_reference_short_kernel_rate": (
            unique_open_long_states / reference_rate / 3600
        ),
        "minimum_mod6_record_bytes": 16,
        "minimum_mod6_table_tib_per_spec": (
            per_block_states * 16 / (1 << 40)
        ),
        "int16_exact_record_bytes": 48,
        "int16_exact_table_tib_per_spec": (
            per_block_states * 48 / (1 << 40)
        ),
        "minimum_mod6_tib_all_19_open_long_specs": (
            unique_open_long_states * 16 / (1 << 40)
        ),
        "int16_exact_tib_all_19_open_long_specs": (
            unique_open_long_states * 48 / (1 << 40)
        ),
        "four_way_half_states_per_block": str((1 << 20) + (1 << 19)),
        "four_way_half_lists_mib_at_48_bytes_for_both_blocks": (
            2 * ((1 << 20) + (1 << 19)) * 48 / (1 << 20)
        ),
        "four_way_pair_products_per_case": str(per_case_states),
        "four_way_obstruction": (
            "within-block norm cross terms make half contributions "
            "bilinear, so small half lists do not make an additive 4-sum"
        ),
        "mod14_unique_specifications": [
            {
                "side": record["side"],
                "cases": record["cases"],
                "raw_coefficient_tuples": str(
                    record["mod14_raw_coefficient_tuples"]
                ),
            }
            for record in sorted(
                records.values(),
                key=lambda item: (
                    str(item["side"]),
                    tuple(item["cases"]),  # type: ignore[arg-type]
                ),
            )
        ],
        "mod14_total_raw_coefficient_tuples": str(total_mod14_tuples),
    }


def collision_pilot(specification: dict[str, object]) -> dict[str, object]:
    """Enumerate one frozen 2^20 subcube and hash its mod-6 key stream."""

    case_number = int(specification["case"])
    block = str(specification["block"])
    variables = tuple(map(int, specification["variables"]))
    case, keys, _, _, linear, quadratic = local.arrays(case_number)
    if case.block != "L" or len(variables) != 20:
        raise AssertionError("invalid collision-pilot specification")
    if any(keys[variable][0] != block for variable in variables):
        raise AssertionError("collision pilot crossed block boundaries")

    chosen = np.zeros(78, dtype=np.int16)
    values = np.zeros(20, dtype=np.int64)
    weight = 0
    previous_gray = 0
    powers = tuple(6 ** coordinate for coordinate in range(20))
    seen: set[int] = set()
    stream_hash = hashlib.sha256()

    def packed_key() -> int:
        return weight + 40 * sum(
            int(values[coordinate] % 6) * powers[coordinate]
            for coordinate in range(20)
        )

    first = packed_key()
    seen.add(first)
    stream_hash.update(first.to_bytes(8, "little"))
    for integer in range(1, 1 << 20):
        gray = integer ^ (integer >> 1)
        changed = gray ^ previous_gray
        local_bit = changed.bit_length() - 1
        variable = variables[local_bit]
        if chosen[variable] == 0:
            values += (
                linear[:, variable]
                + quadratic[:, variable, :] @ chosen
            )
            chosen[variable] = 1
            weight += 1
        else:
            chosen[variable] = 0
            values -= (
                linear[:, variable]
                + quadratic[:, variable, :] @ chosen
            )
            weight -= 1
        key = packed_key()
        seen.add(key)
        stream_hash.update(key.to_bytes(8, "little"))
        previous_gray = gray
    states = 1 << 20
    return {
        "case": case_number,
        "block": block,
        "subcube_variables": [list(keys[variable]) for variable in variables],
        "states": states,
        "distinct_mod6_weight_keys": len(seen),
        "collisions": states - len(seen),
        "distinct_fraction": len(seen) / states,
        "stream_sha256": stream_hash.hexdigest(),
        "scope": "heuristic collision-rate control only",
    }


def crt42_spectral_audit() -> dict[str, object]:
    """Test the bounded CRT-42 residual alphabet against positivity."""

    # If every normalized residual is zero modulo 2,3,7, then it is zero
    # modulo 42.  Cauchy gives |physical correlation| <= 334; correlations
    # are multiples of four, so |normalized residual| <= 83.
    residual_alphabet = (-42, 0, 42)
    epsilon = [0] * 20
    for even_lag in range(2, 21, 2):
        epsilon[even_lag - 1] = (-1) ** (even_lag // 2)
    normalized = [42 * value for value in epsilon]
    if (
        not any(normalized)
        or any(value not in residual_alphabet for value in normalized)
        or any(value % 42 for value in normalized)
    ):
        raise AssertionError("the CRT-42 control vector is invalid")

    # At theta_m=(2m+1)pi/42,
    #   sum_{j=1}^{10} (-1)^j cos(2j theta_m)
    # is 10 for m=10,31 and -1/2 otherwise.  Physical coefficients are
    # four times the normalized residuals, so the norm spectrum is
    # 334 + 336 times this cosine sum.
    spectrum = []
    for root_index in range(42):
        doubled_cosine_sum = (
            20 if (root_index + 11) % 21 == 0 else -1
        )
        spectrum.append(334 + 168 * doubled_cosine_sum)
    spectrum_counts = Counter(spectrum)
    if spectrum_counts != Counter({166: 40, 3694: 2}):
        raise AssertionError("the exact spectral control changed")
    if min(spectrum) < 0:
        raise AssertionError("the advertised control is not nonnegative")
    return {
        "normalized_residual_bound": 83,
        "crt_modulus": 42,
        "remaining_residual_alphabet": list(residual_alphabet),
        "nonzero_control_normalized_residuals": normalized,
        "nonzero_control_spectrum_counts": {
            str(value): count
            for value, count in sorted(spectrum_counts.items())
        },
        "spectral_nonnegativity_forces_zero": False,
        "jet_exclusion": False,
        "conclusion": (
            "CRT-42 plus the universal bound and norm-spectrum "
            "nonnegativity do not exclude all nonzero residual vectors"
        ),
    }


def case_zero_indexing_audit() -> dict[str, object]:
    """Keep the 79-variable closed boundary case distinct from open L2."""

    case, keys, _, _, linear, _ = local.arrays(0)
    groups: dict[tuple[int, ...], int] = Counter(
        tuple(map(int, column))
        for column in np.remainder(linear, 2).T
    )
    if (
        (case.block, case.index) != ("L", 0)
        or len(keys) != 79
        or Counter(block for block, _ in keys) != Counter({"L": 40, "S": 39})
        or Counter(groups.values()) != Counter({2: 39, 1: 1})
    ):
        raise AssertionError("the 79-variable L0 boundary case changed")
    return {
        "canonical_case": 0,
        "label": "L0",
        "variables": 79,
        "block_variables": {"L": 40, "S": 39},
        "mod2_class_size_counts": {"1": 1, "2": 39},
        "open_long_lane": False,
        "status_source": "../ELIAHOU_ANTIFOLD42.md",
        "status": "existing proof-certified UNSAT",
        "indexing_warning": (
            "the still-open solver-only case is canonical case 1 = L2 "
            "and has 78 variables"
        ),
    }


def derive(run_pilots: bool = True) -> dict[str, object]:
    started = time.monotonic()
    case_results = [derive_case(case_number) for case_number in CASES]
    global_split = derive_global_split()
    mod4_anf_results = [
        derive_mod4_anf(case_number)[0] for case_number in CASES
    ]
    mod4_controls = [
        bounded_mod4_rank_control(case_number)
        for case_number in (1, 2, 6, 14)
    ]
    pilots = (
        [collision_pilot(specification) for specification in COLLISION_PILOTS]
        if run_pilots
        else []
    )
    result: dict[str, object] = {
        "schema": "h668-eliahou-long-block-exact-triage-v1",
        "scope": {
            "open_long_cases": list(CASES),
            "primary_requested_cases": list(range(2, 21)),
            "production_census_run": False,
            "claim": (
                "structural/work classification only; no infeasibility "
                "or Hadamard matrix is claimed"
            ),
        },
        "summary": {
            "ordinary_two_clique_cases": [
                case["case"]
                for case in case_results
                if case["conditioned_mod3_graph"][
                    "universal_mixed_triple_separator_vertices"
                ] == 0
            ],
            "one_triple_separator_cases": [6],
            "two_triple_separator_cases": [1, 14],
            "all_cases_have_free_reflection_gauge": False,
            "all_cases_have_exact_fixed_quotient_mitm": True,
            "any_case_projected_below_two_hours": False,
            "recommended_production_launch": False,
        },
        "closed_boundary_case": case_zero_indexing_audit(),
        "cases": case_results,
        "exact_mod4_anf": mod4_anf_results,
        "bounded_mod4_rank_controls": mod4_controls,
        "global_LS_split": global_split,
        "unrestricted_char7_local_count": (
            unrestricted_char7_local_count()
        ),
        "crt42_spectral_audit": crt42_spectral_audit(),
        "bounded_mod6_collision_pilots": pilots,
        "reference_rate": {
            "join_rows_per_second": REFERENCE_JOIN_ROWS_PER_SECOND,
            "source": "../eliahou_global_quotient_plan/BENCHMARK.json",
            "warning": (
                "runtime figures are arithmetic projections from a "
                "different certified kernel, not production measurements"
            ),
        },
    }
    result["semantic_sha256"] = compact_hash(result)
    result["verification_seconds"] = time.monotonic() - started
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-certificate",
        action="store_true",
        help="replace the frozen certificate with the freshly derived payload",
    )
    parser.add_argument(
        "--skip-pilots",
        action="store_true",
        help="skip the two bounded 2^20 collision controls",
    )
    return parser.parse_args()


def comparable(payload: dict[str, object]) -> dict[str, object]:
    result = dict(payload)
    result.pop("verification_seconds", None)
    return result


def main() -> None:
    args = parse_args()
    result = derive(run_pilots=not args.skip_pilots)
    if args.write_certificate:
        CERTIFICATE.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n"
        )
        print(f"WROTE {CERTIFICATE}")
        return
    if not CERTIFICATE.exists():
        raise FileNotFoundError(
            f"missing {CERTIFICATE}; use --write-certificate once"
        )
    expected = json.loads(CERTIFICATE.read_text())
    if args.skip_pilots:
        expected = dict(expected)
        expected["bounded_mod6_collision_pilots"] = []
        expected["semantic_sha256"] = compact_hash(
            {
                key: value
                for key, value in expected.items()
                if key not in {"semantic_sha256", "verification_seconds"}
            }
        )
        result["semantic_sha256"] = compact_hash(
            {
                key: value
                for key, value in result.items()
                if key not in {"semantic_sha256", "verification_seconds"}
            }
        )
    if comparable(result) != comparable(expected):
        raise AssertionError("derived long-block classification changed")
    print(
        json.dumps(
            {
                "status": "PASS",
                "cases": len(result["cases"]),
                "semantic_sha256": result["semantic_sha256"],
                "verification_seconds": result["verification_seconds"],
                "production_census_run": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
