#!/usr/bin/env python3
"""Resumable exact constructor for the 24-profile LP(333) zero gate.

This is a finite theory-led search, not a 666-sign brute force search.  It
uses the local-global theorem in ``LP333_ORDER3_PROFILE_CRT.md``:

* exact four-coordinate aggregate target;
* normalized profile energy 54;
* six opposite-pair local conditions;
* the primitive-nine ``3(1-omega)`` ideal on all nonzero parts;
* all thirteen characteristic-37 logarithmic transfer coefficients; and
* the six exact reversal-independent equations ``D_j=0``.

Those modular conditions force the exact profile correlation ``D_t=0`` by
the CRT norm gap.  Any CP-SAT survivor is therefore replayed immediately by
``verify_lp333_order3_profile_crt_candidate.py``, which has no solver
dependency and checks the full exact correlation word.

The runner is resumable through deterministic prefix cubes.  A timed-out
cube is replaced by its ten children and the queue is saved atomically.
Survivors are enumerated, replayed, and emitted with their symmetry orbits;
finding one never halts the queue.  CP-SAT always uses one worker.  Its
``max_memory_in_mb`` setting is recorded as an advisory solver parameter,
not misrepresented as a hard process-RSS limit.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import time
from typing import Any, Optional, Sequence

import ortools
from ortools.sat.python import cp_model

from verify_lp333_order3_char37_transfer import (
    CLASS_OF,
    CLASSES,
    PROFILES,
    TRANSFER_MATRIX,
    pair_signature,
    profile_norm,
    row_sum_targets,
    signed_profile_integer,
)
from verify_lp333_order3_profile9 import profile_correlation_table
from verify_lp333_order3_profile9_shards import PROFILE9_SHARD_WITNESSES
from verify_lp333_order3_profile_crt_candidate import (
    audit_profile_crt_candidate,
    require_exact_int,
    strict_json_loads,
)
from verify_lp333_order3_profile_zero_symmetry import (
    CONJUGATE_PROFILE_IDS,
    EXPECTED_FORMAL_TARGET_ORBITS,
    orbit_partition,
    transform_assignment,
    transform_target,
)


Target = tuple[int, int, int, int]
Identifiers = tuple[int, ...]
Prefix = tuple[int, ...]

SCHEMA = "hadamard668.lp333-order3-profile-crt-search.v5"
CANDIDATE_SCHEMA = "hadamard668.lp333-order3-profile-crt-survivors.v5"
CLASS_COUNT = 12
PROFILE_STATE_COUNT = 10
DEFAULT_TOTAL_TIME_SECONDS = 60.0
DEFAULT_CUBE_TIME_SECONDS = 15.0
DEFAULT_MAX_MEMORY_MIB = 4096
MAX_MEMORY_MIB = 4096
DEFAULT_SEED = 668
CAUCHY_NORM_BOUND = 167**2
TIGHT_CORRELATION_COORDINATE_BOUND = 192
CORRELATION_COORDINATE_BOUND = TIGHT_CORRELATION_COORDINATE_BOUND
QUARTET_ASSIGNMENT_COUNT = 3334
QUARTET_COARSE_STATE_COUNT = 1409
MAX_NORM_NINE_PROFILES = 3

SEMANTIC_SOURCE_DEPENDENCIES = (
    "search_lp333_order3_profile_crt.py",
    "verify_lp333_order3_profile_crt_candidate.py",
    "verify_lp333_order3_char37_transfer.py",
    "verify_lp333_order3_profile9.py",
    "verify_lp333_order3_profile9_shards.py",
    "verify_lp333_order3_profile_crt.py",
    "verify_lp333_order3_profile_endpoint_shell.py",
    "verify_lp333_order3_profile_penultimate_shell.py",
    "verify_lp333_order3_profile_shell_four.cpp",
    "verify_lp333_order3_profile_zero_symmetry.py",
    "verify_lp333_order3_prime167_split.py",
)

# Complete one opposite-pair quartet before moving to the next.  Prefix
# cubes therefore expose the local mod-three obstruction early.
VARIABLE_ORDER: tuple[tuple[int, int], ...] = tuple(
    item
    for pair_index in range(6)
    for item in (
        (0, pair_index),
        (0, pair_index + 6),
        (1, pair_index),
        (1, pair_index + 6),
    )
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def audit_correlation_coordinate_bound() -> dict[str, int]:
    """Certify that the model's coordinate box contains the Cauchy disk.

    For ``z=a+b*omega`` one has

        4 Norm(z) = (2a-b)^2 + 3b^2
                  = (2b-a)^2 + 3a^2.

    Hence ``Norm(z)<=167^2`` implies ``|a|,|b|<=192``.  The model uses this
    sharp integral coordinate box exactly.
    """

    if (
        3 * (TIGHT_CORRELATION_COORDINATE_BOUND + 1) ** 2
        <= 4 * CAUCHY_NORM_BOUND
    ):
        raise AssertionError("the claimed tight coordinate bound is too small")
    if (
        3 * TIGHT_CORRELATION_COORDINATE_BOUND**2
        > 4 * CAUCHY_NORM_BOUND
    ):
        raise AssertionError("the tight coordinate bound was not maximal")
    if CORRELATION_COORDINATE_BOUND < TIGHT_CORRELATION_COORDINATE_BOUND:
        raise AssertionError("the CP-SAT coordinate domain cuts the Cauchy disk")
    return {
        "cauchy_norm_bound": CAUCHY_NORM_BOUND,
        "tight_coordinate_bound": TIGHT_CORRELATION_COORDINATE_BOUND,
        "model_coordinate_bound": CORRELATION_COORDINATE_BOUND,
    }


def e_conjugate(value: tuple[int, int]) -> tuple[int, int]:
    return value[0] - value[1], -value[1]


def e_multiply(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def _equality_literal(
    model: cp_model.CpModel,
    left: cp_model.IntVar,
    right: cp_model.IntVar,
    name: str,
) -> cp_model.IntVar:
    equal = model.new_bool_var(name)
    model.add(left == right).only_enforce_if(equal)
    model.add(left != right).only_enforce_if(equal.negated())
    return equal


def add_lexicographic_less_or_equal(
    model: cp_model.CpModel,
    left: Sequence[cp_model.IntVar],
    right: Sequence[cp_model.IntVar],
    name: str,
) -> None:
    """Add the exact integer-vector condition ``left <=lex right``."""

    if len(left) != len(right):
        raise ValueError("lexicographic vectors must have equal length")
    if not left:
        return
    prefix_equal = model.new_bool_var(f"{name}_prefix_0")
    model.add(prefix_equal == 1)
    for index, (left_value, right_value) in enumerate(zip(left, right)):
        model.add(left_value <= right_value).only_enforce_if(prefix_equal)
        if index + 1 == len(left):
            break
        equal = _equality_literal(
            model, left_value, right_value, f"{name}_equal_{index}"
        )
        next_prefix = model.new_bool_var(f"{name}_prefix_{index + 1}")
        model.add(next_prefix <= prefix_equal)
        model.add(next_prefix <= equal)
        model.add(next_prefix >= prefix_equal + equal - 1)
        prefix_equal = next_prefix


def target_stabilizer_elements(
    target: Sequence[int],
) -> tuple[tuple[int, bool, bool], ...]:
    """Return every nonidentity formal symmetry fixing one target."""

    normalized = tuple(
        require_exact_int(value, f"target[{index}]")
        for index, value in enumerate(target)
    )
    if len(normalized) != 4:
        raise ValueError("the aggregate target must have four coordinates")
    result = tuple(
        (rotation, bool(star_a), bool(star_b))
        for rotation in range(6)
        for star_a in range(2)
        for star_b in range(2)
        if (rotation, star_a, star_b) != (0, 0, 0)
        and transform_target(normalized, bool(star_a), bool(star_b))
        == normalized
    )
    # Every target has the C6 rotation subgroup.  At most one of the two
    # stars fixes a catalog target, as certified by the symmetry verifier.
    if len(result) not in (5, 11):
        raise AssertionError("the fixed-target stabilizer order changed")
    return result


@dataclass
class ProfileCRTModel:
    model: cp_model.CpModel
    identifiers: tuple[
        tuple[cp_model.IntVar, ...], tuple[cp_model.IntVar, ...]
    ]
    coefficient_real: tuple[
        tuple[cp_model.IntVar, ...], tuple[cp_model.IntVar, ...]
    ]
    coefficient_omega: tuple[
        tuple[cp_model.IntVar, ...], tuple[cp_model.IntVar, ...]
    ]
    correlation_real: tuple[Any, ...]
    correlation_omega: tuple[Any, ...]
    quartet_states: tuple[cp_model.IntVar, ...]
    target: Target
    transfer_equations: int
    ideal_parts: int
    exact_zero_equations: int
    symmetry_elements: tuple[tuple[int, bool, bool], ...]


def _allowed_profile_rows(
    channel: int, class_index: int
) -> tuple[tuple[int, int, int, int, int], ...]:
    return tuple(
        (
            profile_id,
            *signed_profile_integer(channel, class_index, profile_id),
            profile_norm(profile_id),
            int(profile_norm(profile_id) == 9),
        )
        for profile_id in range(PROFILE_STATE_COUNT)
    )


def _product_rows(
    channel: int, left_index: int, right_index: int
) -> tuple[tuple[int, int, int, int], ...]:
    result = []
    for left_id in range(PROFILE_STATE_COUNT):
        left = signed_profile_integer(channel, left_index, left_id)
        for right_id in range(PROFILE_STATE_COUNT):
            right = signed_profile_integer(channel, right_index, right_id)
            product = e_multiply(left, e_conjugate(right))
            result.append((left_id, right_id, product[0], product[1]))
    return tuple(result)


@lru_cache(maxsize=None)
def quartet_allowed_rows(
    pair_index: int,
) -> tuple[tuple[int, ...], ...]:
    """Return the exact local quartet table.

    Columns are the four profile IDs, a canonical coarse-state ID, the four
    aggregate increments, and the energy increment.  The opposite-pair
    signature equality leaves exactly 3,334 of the 10,000 ID quartets and
    these collapse to exactly 1,409 coarse states.
    """

    if not 0 <= pair_index < 6:
        raise ValueError("quartet index must lie in 0,...,5")
    raw: list[tuple[int, ...]] = []
    for a_left in range(PROFILE_STATE_COUNT):
        for a_right in range(PROFILE_STATE_COUNT):
            signature = pair_signature(a_left, a_right)
            for b_left in range(PROFILE_STATE_COUNT):
                for b_right in range(PROFILE_STATE_COUNT):
                    if pair_signature(b_left, b_right) != signature:
                        continue
                    ids = (a_left, a_right, b_left, b_right)
                    values = (
                        signed_profile_integer(0, pair_index, a_left),
                        signed_profile_integer(
                            0, pair_index + 6, a_right
                        ),
                        signed_profile_integer(1, pair_index, b_left),
                        signed_profile_integer(
                            1, pair_index + 6, b_right
                        ),
                    )
                    coarse = (
                        values[0][0] + values[1][0],
                        values[0][1] + values[1][1],
                        values[2][0] + values[3][0],
                        values[2][1] + values[3][1],
                        sum(profile_norm(value) for value in ids),
                    )
                    raw.append((*ids, *coarse))
    coarse_states = tuple(sorted({row[4:] for row in raw}))
    if len(raw) != QUARTET_ASSIGNMENT_COUNT:
        raise AssertionError("the 3,334-state quartet census changed")
    if len(coarse_states) != QUARTET_COARSE_STATE_COUNT:
        raise AssertionError("the 1,409-state coarse quartet census changed")
    coarse_ids = {state: index for index, state in enumerate(coarse_states)}
    return tuple(
        (*row[:4], coarse_ids[row[4:]], *row[4:])
        for row in raw
    )


@lru_cache(maxsize=None)
def quartet_coarse_states(
    pair_index: int,
) -> tuple[tuple[int, int, int, int, int], ...]:
    rows = quartet_allowed_rows(pair_index)
    result = tuple(sorted({tuple(row[5:]) for row in rows}))
    if len(result) != QUARTET_COARSE_STATE_COUNT:
        raise AssertionError("quartet coarse-state extraction changed")
    return result  # type: ignore[return-value]


@lru_cache(maxsize=1)
def audit_quartet_state_census() -> dict[str, int]:
    """Audit the one- and two-layer coarse state spaces without a solve."""

    rows = quartet_allowed_rows(0)
    multiplicities = []
    for pair_index in range(2):
        counts: dict[tuple[int, ...], int] = {}
        for row in quartet_allowed_rows(pair_index):
            state = tuple(row[5:])
            counts[state] = counts.get(state, 0) + 1
        multiplicities.append(counts)
    first = quartet_coarse_states(0)
    second = quartet_coarse_states(1)
    two_layer_states = {
        tuple(left[index] + right[index] for index in range(5))
        for left in first
        for right in second
        if left[4] + right[4] <= 54
    }
    two_layer_prefixes = sum(
        multiplicities[0][left] * multiplicities[1][right]
        for left in first
        for right in second
        if left[4] + right[4] <= 54
    )
    if len(two_layer_states) != 96_104:
        raise AssertionError("the 96,104-state two-layer census changed")
    if two_layer_prefixes != 10_934_035:
        raise AssertionError("the two-layer quartet-prefix census changed")
    return {
        "quartet_assignments": len(rows),
        "quartet_coarse_states": len(first),
        "two_layer_energy_bounded_states": len(two_layer_states),
        "two_layer_energy_bounded_prefixes": two_layer_prefixes,
    }


def _sum_bounds(weights: Sequence[int], value_bound: int) -> int:
    return sum(abs(value) for value in weights) * value_bound


def build_profile_crt_model(
    target: Sequence[int],
    prefix: Sequence[int] = (),
    *,
    enforce_crt: bool = True,
    break_rotation_symmetry: bool = True,
) -> ProfileCRTModel:
    """Build one exact target/prefix cube.

    The historical switch name ``enforce_crt`` now enables the exact six-part
    zero gate as well as its redundant CRT cuts.  Setting it to false retains
    aggregate, energy, and local constraints and exposes the exact correlation
    variables; that mode is used only for arithmetic self-tests.
    """

    audit_correlation_coordinate_bound()
    normalized_target = tuple(
        require_exact_int(value, f"target[{index}]")
        for index, value in enumerate(target)
    )
    if len(normalized_target) != 4:
        raise ValueError("the aggregate target must have four coordinates")
    if normalized_target not in set(row_sum_targets()):
        raise ValueError("the target is not one of the 22 aggregate shards")
    normalized_prefix = tuple(
        require_exact_int(value, f"prefix[{index}]")
        for index, value in enumerate(prefix)
    )
    if len(normalized_prefix) > len(VARIABLE_ORDER):
        raise ValueError("a prefix fixes more than 24 variables")
    if any(not 0 <= value < PROFILE_STATE_COUNT for value in normalized_prefix):
        raise ValueError("a prefix value lies outside 0,...,9")

    model = cp_model.CpModel()
    identifiers: list[list[cp_model.IntVar]] = [[], []]
    coefficients_real: list[list[cp_model.IntVar]] = [[], []]
    coefficients_omega: list[list[cp_model.IntVar]] = [[], []]
    norms: list[list[cp_model.IntVar]] = [[], []]
    norm_nine_flags: list[list[cp_model.IntVar]] = [[], []]
    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            profile_id = model.new_int_var(
                0, PROFILE_STATE_COUNT - 1, f"p_{channel}_{class_index}"
            )
            real = model.new_int_var(-3, 3, f"z_real_{channel}_{class_index}")
            omega = model.new_int_var(
                -3, 3, f"z_omega_{channel}_{class_index}"
            )
            norm = model.new_int_var(0, 9, f"norm_{channel}_{class_index}")
            norm_nine = model.new_bool_var(
                f"norm_nine_{channel}_{class_index}"
            )
            model.add_allowed_assignments(
                [profile_id, real, omega, norm, norm_nine],
                _allowed_profile_rows(channel, class_index),
            )
            identifiers[channel].append(profile_id)
            coefficients_real[channel].append(real)
            coefficients_omega[channel].append(omega)
            norms[channel].append(norm)
            norm_nine_flags[channel].append(norm_nine)

    id_words = (
        tuple(identifiers[0]),
        tuple(identifiers[1]),
    )
    real_words = (
        tuple(coefficients_real[0]),
        tuple(coefficients_real[1]),
    )
    omega_words = (
        tuple(coefficients_omega[0]),
        tuple(coefficients_omega[1]),
    )
    norm_words = (tuple(norms[0]), tuple(norms[1]))
    norm_nine_words = (
        tuple(norm_nine_flags[0]),
        tuple(norm_nine_flags[1]),
    )

    for channel in range(2):
        model.add(sum(real_words[channel]) == normalized_target[2 * channel])
        model.add(
            sum(omega_words[channel]) == normalized_target[2 * channel + 1]
        )
    model.add(sum(norm_words[0]) + sum(norm_words[1]) == 54)
    # The six-, five-, and four-norm-nine endpoint shells are excluded
    # exactly by the local modulo-nine and symmetry certificates in
    # verify_lp333_order3_profile_endpoint_shell.py and
    # verify_lp333_order3_profile_penultimate_shell.py, and by the streaming
    # affine-modulo-nine certificate in
    # verify_lp333_order3_profile_shell_four.cpp.
    model.add(
        sum(norm_nine_words[0]) + sum(norm_nine_words[1])
        <= MAX_NORM_NINE_PROFILES
    )

    # Exact opposite-pair quartet tables.  Besides enforcing the local
    # primitive-nine signature, each table maps its four IDs to one of 1,409
    # aggregate/energy states.  Layered cumulative variables expose these
    # coarse states to propagation without materializing a multi-million-edge
    # MDD.
    quartet_states: list[cp_model.IntVar] = []
    quartet_increments: list[tuple[cp_model.IntVar, ...]] = []
    for pair_index in range(6):
        rows = quartet_allowed_rows(pair_index)
        coarse_state = model.new_int_var(
            0,
            QUARTET_COARSE_STATE_COUNT - 1,
            f"quartet_coarse_state_{pair_index}",
        )
        increment_variables = []
        for coordinate in range(5):
            values = tuple(row[5 + coordinate] for row in rows)
            increment_variables.append(
                model.new_int_var(
                    min(values),
                    max(values),
                    f"quartet_increment_{pair_index}_{coordinate}",
                )
            )
        model.add_allowed_assignments(
            [
                id_words[0][pair_index],
                id_words[0][pair_index + 6],
                id_words[1][pair_index],
                id_words[1][pair_index + 6],
                coarse_state,
                *increment_variables,
            ],
            rows,
        )
        quartet_states.append(coarse_state)
        quartet_increments.append(tuple(increment_variables))

    final_state = (
        normalized_target[0],
        normalized_target[1],
        normalized_target[2],
        normalized_target[3],
        54,
    )
    cumulative: list[list[Any]] = [[0, 0, 0, 0, 0]]
    for pair_index in range(6):
        next_state = []
        for coordinate in range(5):
            remaining_states = [
                quartet_coarse_states(index)
                for index in range(pair_index + 1, 6)
            ]
            remaining_min = sum(
                min(state[coordinate] for state in states)
                for states in remaining_states
            )
            remaining_max = sum(
                max(state[coordinate] for state in states)
                for states in remaining_states
            )
            prefix_states = [
                quartet_coarse_states(index)
                for index in range(pair_index + 1)
            ]
            prefix_min = sum(
                min(state[coordinate] for state in states)
                for states in prefix_states
            )
            prefix_max = sum(
                max(state[coordinate] for state in states)
                for states in prefix_states
            )
            lower = max(
                prefix_min, final_state[coordinate] - remaining_max
            )
            upper = min(
                prefix_max, final_state[coordinate] - remaining_min
            )
            value = model.new_int_var(
                lower,
                upper,
                f"quartet_prefix_{pair_index + 1}_{coordinate}",
            )
            model.add(
                value
                == cumulative[-1][coordinate]
                + quartet_increments[pair_index][coordinate]
            )
            next_state.append(value)
        cumulative.append(next_state)
    for coordinate, target_value in enumerate(final_state):
        model.add(cumulative[-1][coordinate] == target_value)

    # One product table for each unordered pair of class variables.  Reverse
    # orientation is obtained by exact Eisenstein conjugation.
    pair_products: dict[
        tuple[int, int, int], tuple[cp_model.IntVar, cp_model.IntVar]
    ] = {}
    for channel in range(2):
        for left_index in range(CLASS_COUNT):
            for right_index in range(left_index + 1, CLASS_COUNT):
                rows = _product_rows(channel, left_index, right_index)
                real_values = tuple(row[2] for row in rows)
                omega_values = tuple(row[3] for row in rows)
                product_real = model.new_int_var(
                    min(real_values),
                    max(real_values),
                    f"product_real_{channel}_{left_index}_{right_index}",
                )
                product_omega = model.new_int_var(
                    min(omega_values),
                    max(omega_values),
                    f"product_omega_{channel}_{left_index}_{right_index}",
                )
                model.add_allowed_assignments(
                    [
                        id_words[channel][left_index],
                        id_words[channel][right_index],
                        product_real,
                        product_omega,
                    ],
                    rows,
                )
                pair_products[(channel, left_index, right_index)] = (
                    product_real,
                    product_omega,
                )

    def oriented_product(
        channel: int, left_index: int, right_index: int
    ) -> tuple[Any, Any]:
        if left_index == right_index:
            return norm_words[channel][left_index], 0
        if left_index <= right_index:
            return pair_products[(channel, left_index, right_index)]
        real, omega = pair_products[(channel, right_index, left_index)]
        return real - omega, -omega

    correlation_real: list[Any] = [0]
    correlation_omega: list[Any] = [0]
    zero_coefficients = (-1, 2)
    for part_index, part in enumerate(CLASSES):
        lag = part[0]
        real_terms: list[Any] = []
        omega_terms: list[Any] = []
        for channel in range(2):
            zero = zero_coefficients[channel]
            for right_column in range(37):
                left_column = (right_column + lag) % 37
                if left_column == 0:
                    right_index = CLASS_OF[right_column]
                    right_real = real_words[channel][right_index]
                    right_omega = omega_words[channel][right_index]
                    real_terms.append(zero * (right_real - right_omega))
                    omega_terms.append(-zero * right_omega)
                elif right_column == 0:
                    left_index = CLASS_OF[left_column]
                    real_terms.append(
                        zero * real_words[channel][left_index]
                    )
                    omega_terms.append(
                        zero * omega_words[channel][left_index]
                    )
                else:
                    left_index = CLASS_OF[left_column]
                    right_index = CLASS_OF[right_column]
                    product_real, product_omega = oriented_product(
                        channel, left_index, right_index
                    )
                    real_terms.append(product_real)
                    omega_terms.append(product_omega)
        real_value = model.new_int_var(
            -CORRELATION_COORDINATE_BOUND,
            CORRELATION_COORDINATE_BOUND,
            f"D_real_{part_index}",
        )
        omega_value = model.new_int_var(
            -CORRELATION_COORDINATE_BOUND,
            CORRELATION_COORDINATE_BOUND,
            f"D_omega_{part_index}",
        )
        model.add(real_value == sum(real_terms))
        model.add(omega_value == sum(omega_terms))
        correlation_real.append(real_value)
        correlation_omega.append(omega_value)

    ideal_parts = 0
    transfer_equations = 0
    exact_zero_equations = 0
    if enforce_crt:
        # Reversal gives D_{j+6}=conjugate(D_j), so these six Eisenstein
        # equations are the complete exact zero gate.
        for part_index in range(1, 7):
            model.add(correlation_real[part_index] == 0)
            model.add(correlation_omega[part_index] == 0)
            exact_zero_equations += 2

        # D_t in 3(1-omega)Z[omega] on every nonzero class.
        ideal_quotient_bound = CORRELATION_COORDINATE_BOUND // 3 + 1
        for part_index in range(1, 13):
            real_third = model.new_int_var(
                -ideal_quotient_bound,
                ideal_quotient_bound,
                f"ideal_real_third_{part_index}",
            )
            omega_third = model.new_int_var(
                -ideal_quotient_bound,
                ideal_quotient_bound,
                f"ideal_omega_third_{part_index}",
            )
            lambda_quotient = model.new_int_var(
                -ideal_quotient_bound,
                ideal_quotient_bound,
                f"ideal_lambda_quotient_{part_index}",
            )
            model.add(correlation_real[part_index] == 3 * real_third)
            model.add(correlation_omega[part_index] == 3 * omega_third)
            model.add(real_third + omega_third == 3 * lambda_quotient)
            ideal_parts += 1

        # The exact logarithmic transfer matrix maps the 13 invariant
        # correlation parts to all 13 characteristic-37 coefficients.
        # Symmetric integer representatives keep the quotient bounds tight.
        for transfer_index, row in enumerate(TRANSFER_MATRIX):
            weights = tuple(
                value if value <= 18 else value - 37 for value in row
            )
            bound = _sum_bounds(
                weights, CORRELATION_COORDINATE_BOUND
            )
            quotient_bound = bound // 37 + 1
            for coordinate_name, values in (
                ("real", correlation_real),
                ("omega", correlation_omega),
            ):
                quotient = model.new_int_var(
                    -quotient_bound,
                    quotient_bound,
                    f"transfer_{coordinate_name}_{transfer_index}",
                )
                model.add(
                    sum(
                        weight * value
                        for weight, value in zip(weights, values)
                    )
                    == 37 * quotient
                )
                transfer_equations += 1

    symmetry_elements: tuple[tuple[int, bool, bool], ...] = ()
    if break_rotation_symmetry:
        flat = tuple(id_words[0]) + tuple(id_words[1])
        symmetry_elements = target_stabilizer_elements(normalized_target)
        for rotation, star_a, star_b in symmetry_elements:
            image_variables = []
            for channel, use_star in enumerate((star_a, star_b)):
                offset = (
                    2 * rotation + (6 if use_star else 0)
                ) % CLASS_COUNT
                for class_index in range(CLASS_COUNT):
                    source = id_words[channel][
                        (class_index + offset) % CLASS_COUNT
                    ]
                    if use_star:
                        mapped = model.new_int_var(
                            0,
                            PROFILE_STATE_COUNT - 1,
                            (
                                f"symmetry_{rotation}_{int(star_a)}_"
                                f"{int(star_b)}_{channel}_{class_index}"
                            ),
                        )
                        model.add_element(
                            source, CONJUGATE_PROFILE_IDS, mapped
                        )
                        image_variables.append(mapped)
                    else:
                        image_variables.append(source)
            add_lexicographic_less_or_equal(
                model,
                flat,
                tuple(image_variables),
                (
                    f"target_stabilizer_{rotation}_{int(star_a)}_"
                    f"{int(star_b)}"
                ),
            )

    ordered_variables = tuple(
        id_words[channel][class_index]
        for channel, class_index in VARIABLE_ORDER
    )
    for depth, value in enumerate(normalized_prefix):
        model.add(ordered_variables[depth] == value)
    model.add_decision_strategy(
        ordered_variables,
        cp_model.CHOOSE_FIRST,
        cp_model.SELECT_MIN_VALUE,
    )

    validation_error = model.validate()
    if validation_error:
        raise RuntimeError(f"invalid CP-SAT model: {validation_error}")
    return ProfileCRTModel(
        model=model,
        identifiers=id_words,
        coefficient_real=real_words,
        coefficient_omega=omega_words,
        correlation_real=tuple(correlation_real),
        correlation_omega=tuple(correlation_omega),
        quartet_states=tuple(quartet_states),
        target=normalized_target,  # type: ignore[arg-type]
        transfer_equations=transfer_equations,
        ideal_parts=ideal_parts,
        exact_zero_equations=exact_zero_equations,
        symmetry_elements=symmetry_elements,
    )


def configure_solver(
    *, time_limit: float, max_memory_mib: int, seed: int = DEFAULT_SEED
) -> cp_model.CpSolver:
    if time_limit <= 0:
        raise ValueError("the solver time limit must be positive")
    if not 1 <= max_memory_mib <= MAX_MEMORY_MIB:
        raise ValueError("the solver memory limit must lie in [1,4096] MiB")
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(time_limit)
    solver.parameters.num_search_workers = 1
    solver.parameters.max_memory_in_mb = int(max_memory_mib)
    solver.parameters.random_seed = int(seed)
    solver.parameters.randomize_search = False
    solver.parameters.search_branching = cp_model.FIXED_SEARCH
    return solver


def extract_assignment(
    solver: cp_model.CpSolver, bundle: ProfileCRTModel
) -> tuple[Identifiers, Identifiers]:
    return tuple(
        tuple(solver.value(value) for value in channel)
        for channel in bundle.identifiers
    )  # type: ignore[return-value]


def extract_correlation(
    solver: cp_model.CpSolver, bundle: ProfileCRTModel
) -> tuple[tuple[int, int], ...]:
    return tuple(
        (
            int(value_real)
            if isinstance(value_real, int)
            else solver.value(value_real),
            int(value_omega)
            if isinstance(value_omega, int)
            else solver.value(value_omega),
        )
        for value_real, value_omega in zip(
            bundle.correlation_real, bundle.correlation_omega
        )
    )


def target_modes() -> dict[str, tuple[int, ...]]:
    targets = row_sum_targets()
    formal = tuple(
        targets.index(orbit[0]) for orbit in EXPECTED_FORMAL_TARGET_ORBITS
    )
    lift_orbits = orbit_partition(targets, False, True)
    lift = tuple(targets.index(orbit[0]) for orbit in lift_orbits)
    return {
        "formal": formal,
        "lift": lift,
        "all": tuple(range(len(targets))),
    }


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


@lru_cache(maxsize=1)
def semantic_manifest() -> dict[str, Any]:
    """Return the source-, dependency-, table-, and solver-pinned semantics."""

    directory = Path(__file__).resolve().parent
    source_hashes = {}
    for name in SEMANTIC_SOURCE_DEPENDENCIES:
        path = directory / name
        if not path.is_file():
            raise FileNotFoundError(f"semantic dependency is missing: {path}")
        source_hashes[name] = _file_sha256(path)
    table_signature = {
        "profiles": PROFILES,
        "classes": CLASSES,
        "transfer_matrix": TRANSFER_MATRIX,
        "targets": row_sum_targets(),
        "profile_rows": tuple(
            _allowed_profile_rows(channel, class_index)
            for channel in range(2)
            for class_index in range(CLASS_COUNT)
        ),
        "quartet_rows": tuple(
            quartet_allowed_rows(pair_index) for pair_index in range(6)
        ),
        "off_diagonal_product_rows": tuple(
            _product_rows(channel, left_index, right_index)
            for channel in range(2)
            for left_index in range(CLASS_COUNT)
            for right_index in range(left_index + 1, CLASS_COUNT)
        ),
        "conjugate_profile_ids": CONJUGATE_PROFILE_IDS,
    }
    return {
        "schema": SCHEMA,
        "ortools_version": ortools.__version__,
        "semantic_source_sha256": source_hashes,
        "table_sha256": compact_hash(table_signature),
        "quartet_census": {
            "assignments": QUARTET_ASSIGNMENT_COUNT,
            "coarse_states": QUARTET_COARSE_STATE_COUNT,
        },
    }


@lru_cache(maxsize=1)
def semantic_fingerprint() -> str:
    return compact_hash(semantic_manifest())


def model_fingerprint(
    target_indices: Sequence[int], break_rotation_symmetry: bool
) -> str:
    selected = tuple(
        require_exact_int(value, f"target_indices[{index}]")
        for index, value in enumerate(target_indices)
    )
    payload = {
        "schema": SCHEMA,
        "semantic_fingerprint": semantic_fingerprint(),
        "selected_target_indices": selected,
        "variable_order": VARIABLE_ORDER,
        "break_rotation_symmetry": bool(break_rotation_symmetry),
        "correlation_coordinate_bound": CORRELATION_COORDINATE_BOUND,
        "mathematical_layers": (
            "aggregate",
            "energy54",
            "norm9_top_three_shell_exclusions",
            "quartet3334_coarse1409",
            "target_stabilizer_lex",
            "primitive9_lambda3",
            "characteristic37_transfer13",
            "six_exact_reversal_independent_correlations",
        ),
    }
    return compact_hash(payload)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_checkpoint(
    target_indices: Sequence[int], break_rotation_symmetry: bool
) -> dict[str, Any]:
    selected = tuple(
        require_exact_int(value, f"target_indices[{index}]")
        for index, value in enumerate(target_indices)
    )
    if not selected or len(set(selected)) != len(selected):
        raise ValueError("target indices must be nonempty and distinct")
    if any(not 0 <= value < len(row_sum_targets()) for value in selected):
        raise ValueError("target indices must lie in 0,...,21")
    return {
        "schema": SCHEMA,
        "created_utc": _utc_now(),
        "updated_utc": _utc_now(),
        "ortools_version": ortools.__version__,
        "semantic_manifest": semantic_manifest(),
        "semantic_fingerprint": semantic_fingerprint(),
        "model_fingerprint": model_fingerprint(
            selected, break_rotation_symmetry
        ),
        "selected_target_indices": selected,
        "break_rotation_symmetry": bool(break_rotation_symmetry),
        "variable_order": VARIABLE_ORDER,
        "pending_cubes": [
            {"target_index": target_index, "prefix": ()}
            for target_index in selected
        ],
        "infeasible_cubes": 0,
        "split_cubes": 0,
        "solver_calls": 0,
        "solver_wall_time_seconds": 0.0,
        "candidates": [],
        "candidate_sha256": [],
        "status": "in_progress",
    }


def save_checkpoint(path: Path, checkpoint: dict[str, Any]) -> None:
    checkpoint["updated_utc"] = _utc_now()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(checkpoint, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _checkpoint_integer(
    checkpoint: dict[str, Any], key: str, *, minimum: int = 0
) -> int:
    if key not in checkpoint:
        raise ValueError(f"checkpoint is missing {key!r}")
    value = require_exact_int(checkpoint[key], f"checkpoint.{key}")
    if value < minimum:
        raise ValueError(f"checkpoint.{key} must be at least {minimum}")
    return value


def _validate_checkpoint_payload(
    checkpoint: object,
    target_indices: Sequence[int],
    break_rotation_symmetry: bool,
) -> dict[str, Any]:
    if not isinstance(checkpoint, dict):
        raise ValueError("checkpoint JSON must be an object")
    expected_indices = tuple(
        require_exact_int(value, f"target_indices[{index}]")
        for index, value in enumerate(target_indices)
    )
    if checkpoint.get("schema") != SCHEMA:
        raise ValueError("checkpoint schema mismatch")
    if checkpoint.get("semantic_fingerprint") != semantic_fingerprint():
        raise ValueError(
            "checkpoint source/dependency/table/OR-Tools semantics mismatch; "
            "use a new path"
        )
    stored_manifest = checkpoint.get("semantic_manifest")
    if compact_hash(stored_manifest) != semantic_fingerprint():
        raise ValueError("checkpoint semantic manifest is inconsistent")
    expected_model = model_fingerprint(
        expected_indices, break_rotation_symmetry
    )
    if checkpoint.get("model_fingerprint") != expected_model:
        raise ValueError(
            "checkpoint mathematical configuration mismatch; use a new path"
        )
    selected_raw = checkpoint.get("selected_target_indices")
    if not isinstance(selected_raw, list):
        raise ValueError("checkpoint.selected_target_indices must be an array")
    selected = tuple(
        require_exact_int(value, f"selected_target_indices[{index}]")
        for index, value in enumerate(selected_raw)
    )
    if selected != expected_indices:
        raise ValueError("checkpoint selected target indices changed")
    if type(checkpoint.get("break_rotation_symmetry")) is not bool:
        raise ValueError("checkpoint symmetry flag must be Boolean")
    if checkpoint["break_rotation_symmetry"] != break_rotation_symmetry:
        raise ValueError("checkpoint symmetry flag changed")
    if checkpoint.get("ortools_version") != ortools.__version__:
        raise ValueError("checkpoint OR-Tools version changed")
    order_raw = checkpoint.get("variable_order")
    if not isinstance(order_raw, list):
        raise ValueError("checkpoint.variable_order must be an array")
    normalized_order = []
    for index, item in enumerate(order_raw):
        if not isinstance(item, list) or len(item) != 2:
            raise ValueError("checkpoint variable-order entry is malformed")
        normalized_order.append(
            (
                require_exact_int(item[0], f"variable_order[{index}][0]"),
                require_exact_int(item[1], f"variable_order[{index}][1]"),
            )
        )
    if tuple(normalized_order) != VARIABLE_ORDER:
        raise ValueError("checkpoint variable order changed")

    pending = checkpoint.get("pending_cubes")
    if not isinstance(pending, list):
        raise ValueError("checkpoint.pending_cubes must be an array")
    normalized_pending = []
    for cube_index, cube in enumerate(pending):
        if not isinstance(cube, dict):
            raise ValueError(f"pending_cubes[{cube_index}] must be an object")
        target_index = require_exact_int(
            cube.get("target_index"),
            f"pending_cubes[{cube_index}].target_index",
        )
        if target_index not in selected:
            raise ValueError("a pending cube uses an unselected target")
        prefix_raw = cube.get("prefix")
        if not isinstance(prefix_raw, list):
            raise ValueError("a pending cube prefix must be an array")
        prefix = tuple(
            require_exact_int(
                value, f"pending_cubes[{cube_index}].prefix[{index}]"
            )
            for index, value in enumerate(prefix_raw)
        )
        if len(prefix) > len(VARIABLE_ORDER) or any(
            not 0 <= value < PROFILE_STATE_COUNT for value in prefix
        ):
            raise ValueError("a pending cube prefix is outside the search tree")
        normalized_pending.append(
            {"target_index": target_index, "prefix": prefix}
        )
    checkpoint["pending_cubes"] = normalized_pending

    for key in ("infeasible_cubes", "split_cubes", "solver_calls"):
        _checkpoint_integer(checkpoint, key)
    wall = checkpoint.get("solver_wall_time_seconds")
    if type(wall) not in (int, float) or not math.isfinite(wall) or wall < 0:
        raise ValueError("checkpoint solver wall time must be finite")
    candidates = checkpoint.get("candidates")
    hashes = checkpoint.get("candidate_sha256")
    if not isinstance(candidates, list) or not isinstance(hashes, list):
        raise ValueError("checkpoint candidate catalogs must be arrays")
    if any(not isinstance(value, str) for value in hashes):
        raise ValueError("candidate hashes must be strings")
    if any(
        len(value) != 64
        or any(
            character not in "0123456789abcdef" for character in value
        )
        for value in hashes
    ):
        raise ValueError("candidate hashes must be lowercase SHA-256 values")
    if len(set(hashes)) != len(hashes):
        raise ValueError("candidate hashes must be unique")
    if len(candidates) != len(hashes):
        raise ValueError("candidate records and hashes have different lengths")
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            raise ValueError(f"candidates[{index}] must be an object")
        target_index = require_exact_int(
            candidate.get("target_index"),
            f"candidates[{index}].target_index",
        )
        if target_index not in selected:
            raise ValueError("a candidate uses an unselected target")
        normalized_fields = {}
        for field, expected_length in (
            ("target", 4),
            ("profiles_a", 12),
            ("profiles_b", 12),
        ):
            values = candidate.get(field)
            if not isinstance(values, list):
                raise ValueError(
                    f"candidates[{index}].{field} must be an array"
                )
            normalized = tuple(
                require_exact_int(
                    value,
                    f"candidates[{index}].{field}[{value_index}]",
                )
                for value_index, value in enumerate(values)
            )
            if len(normalized) != expected_length:
                raise ValueError(f"candidate {field} has the wrong length")
            normalized_fields[field] = normalized
        if any(
            not 0 <= value < PROFILE_STATE_COUNT
            for field in ("profiles_a", "profiles_b")
            for value in normalized_fields[field]
        ):
            raise ValueError("a candidate profile ID lies outside 0,...,9")
        if normalized_fields["target"] != row_sum_targets()[target_index]:
            raise ValueError("a candidate target/index pair disagrees")
        candidate_hash = compact_hash(
            (
                normalized_fields["target"],
                normalized_fields["profiles_a"],
                normalized_fields["profiles_b"],
            )
        )
        if candidate.get("survivor_sha256") != candidate_hash:
            raise ValueError("a candidate survivor hash is invalid")
        if hashes[index] != candidate_hash:
            raise ValueError("candidate hash catalog order is invalid")
    return checkpoint


def load_or_create_checkpoint(
    path: Path,
    target_indices: Sequence[int],
    break_rotation_symmetry: bool,
) -> dict[str, Any]:
    if not path.exists():
        checkpoint = new_checkpoint(
            target_indices, break_rotation_symmetry
        )
        save_checkpoint(path, checkpoint)
        return checkpoint
    checkpoint = strict_json_loads(path.read_text(encoding="utf-8"))
    return _validate_checkpoint_payload(
        checkpoint, target_indices, break_rotation_symmetry
    )


def split_cube(cube: dict[str, Any]) -> list[dict[str, Any]]:
    prefix_raw = cube.get("prefix")
    if not isinstance(prefix_raw, (list, tuple)):
        raise ValueError("cube prefix must be an array")
    prefix = tuple(
        require_exact_int(value, f"cube.prefix[{index}]")
        for index, value in enumerate(prefix_raw)
    )
    if len(prefix) >= len(VARIABLE_ORDER):
        return []
    target_index = require_exact_int(cube.get("target_index"), "cube.target_index")
    return [
        {
            "target_index": target_index,
            "prefix": prefix + (value,),
        }
        for value in range(PROFILE_STATE_COUNT)
    ]


def add_assignment_nogood(
    model: cp_model.CpModel,
    identifiers: tuple[
        tuple[cp_model.IntVar, ...], tuple[cp_model.IntVar, ...]
    ],
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
    name: str,
) -> None:
    """Exclude one complete 24-ID assignment exactly."""

    values = tuple(identifiers_a) + tuple(identifiers_b)
    if len(values) != 24:
        raise ValueError("a no-good assignment must contain 24 profile IDs")
    literals = []
    for index, (variable, value) in enumerate(
        zip(identifiers[0] + identifiers[1], values)
    ):
        normalized = require_exact_int(value, f"nogood[{index}]")
        if not 0 <= normalized < PROFILE_STATE_COUNT:
            raise ValueError("a no-good profile ID is outside 0,...,9")
        literal = model.new_bool_var(f"{name}_equal_{index}")
        model.add(variable == normalized).only_enforce_if(literal)
        model.add(variable != normalized).only_enforce_if(literal.negated())
        literals.append(literal)
    model.add(sum(literals) <= len(literals) - 1)


def _orbit_records(
    target: Target,
    identifiers_a: Identifiers,
    identifiers_b: Identifiers,
    *,
    include_star_a: bool,
    include_star_b: bool,
) -> list[dict[str, Any]]:
    targets = row_sum_targets()
    records: dict[
        tuple[Target, Identifiers, Identifiers], dict[str, Any]
    ] = {}
    for rotation in range(6):
        for star_a in range(2 if include_star_a else 1):
            for star_b in range(2 if include_star_b else 1):
                image_a, image_b = transform_assignment(
                    identifiers_a,
                    identifiers_b,
                    rotation,
                    bool(star_a),
                    bool(star_b),
                )
                image_target = transform_target(
                    target, bool(star_a), bool(star_b)
                )
                if image_target not in targets:
                    raise AssertionError("a survivor orbit left the target catalog")
                replay = audit_profile_crt_candidate(
                    image_target, image_a, image_b
                )
                key = (image_target, image_a, image_b)
                records[key] = {
                    "target_index": targets.index(image_target),
                    "target": image_target,
                    "profiles_a": image_a,
                    "profiles_b": image_b,
                    "exact_replay_sha256": replay["certificate_sha256"],
                }
    return [records[key] for key in sorted(records)]


def survivor_record(
    target_index: int,
    target: Target,
    identifiers_a: Identifiers,
    identifiers_b: Identifiers,
    prefix: Prefix,
    solver_status: str,
) -> tuple[str, dict[str, Any]]:
    replay = audit_profile_crt_candidate(target, identifiers_a, identifiers_b)
    survivor_hash = compact_hash((target, identifiers_a, identifiers_b))
    record = {
        "survivor_sha256": survivor_hash,
        "target_index": target_index,
        "target": target,
        "profiles_a": identifiers_a,
        "profiles_b": identifiers_b,
        "prefix": prefix,
        "solver_status": solver_status,
        "exact_replay": replay,
        "formal_profile_orbit": _orbit_records(
            target,
            identifiers_a,
            identifiers_b,
            include_star_a=True,
            include_star_b=True,
        ),
        "lift_compatible_orbit": _orbit_records(
            target,
            identifiers_a,
            identifiers_b,
            include_star_a=False,
            include_star_b=True,
        ),
        "lift_status": "profile_zero_gate_only",
    }
    return survivor_hash, record


def save_survivor_catalog(
    path: Path, checkpoint: dict[str, Any]
) -> None:
    payload = {
        "schema": CANDIDATE_SCHEMA,
        "updated_utc": _utc_now(),
        "semantic_fingerprint": semantic_fingerprint(),
        "survivors": checkpoint["candidates"],
        "status": (
            "detached_profile_zero_replay_only; "
            "no labelled lift, LP(333), or H(668)"
        ),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def run_checkpoint(
    checkpoint_path: Path,
    *,
    target_indices: Sequence[int],
    total_time_seconds: float,
    cube_time_seconds: float,
    max_memory_mib: int,
    break_rotation_symmetry: bool,
    candidate_path: Optional[Path] = None,
) -> dict[str, Any]:
    """Advance a deterministic cube queue for a bounded wall-clock budget."""

    if total_time_seconds <= 0 or cube_time_seconds <= 0:
        raise ValueError("time limits must be positive")
    if not 1 <= max_memory_mib <= MAX_MEMORY_MIB:
        raise ValueError("max memory must lie in [1,4096] MiB")
    checkpoint = load_or_create_checkpoint(
        checkpoint_path, target_indices, break_rotation_symmetry
    )
    targets = row_sum_targets()
    started = time.monotonic()
    while checkpoint["pending_cubes"]:
        elapsed = time.monotonic() - started
        remaining = total_time_seconds - elapsed
        if remaining <= 0.05:
            break
        cube = checkpoint["pending_cubes"].pop(0)
        target_index = require_exact_int(
            cube["target_index"], "cube.target_index"
        )
        prefix = tuple(
            require_exact_int(value, f"cube.prefix[{index}]")
            for index, value in enumerate(cube["prefix"])
        )
        bundle = build_profile_crt_model(
            targets[target_index],
            prefix,
            enforce_crt=True,
            break_rotation_symmetry=break_rotation_symmetry,
        )
        # Persisted survivors are exact no-goods.  This prevents the same
        # witness from reappearing after a timed-out parent cube is split.
        for candidate_index, candidate in enumerate(checkpoint["candidates"]):
            if candidate["target_index"] != target_index:
                continue
            add_assignment_nogood(
                bundle.model,
                bundle.identifiers,
                candidate["profiles_a"],
                candidate["profiles_b"],
                f"persisted_survivor_{candidate_index}",
            )
        cube_deadline = min(
            started + total_time_seconds, time.monotonic() + cube_time_seconds
        )
        cube_complete = False
        while True:
            remaining = min(
                started + total_time_seconds - time.monotonic(),
                cube_deadline - time.monotonic(),
            )
            if remaining <= 0.05:
                break
            solver = configure_solver(
                time_limit=remaining,
                max_memory_mib=max_memory_mib,
            )
            status = solver.solve(bundle.model)
            checkpoint["solver_calls"] += 1
            checkpoint["solver_wall_time_seconds"] += solver.wall_time
            status_name = solver.status_name(status)

            if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
                identifiers_a, identifiers_b = extract_assignment(
                    solver, bundle
                )
                survivor_hash, candidate = survivor_record(
                    target_index,
                    targets[target_index],
                    identifiers_a,
                    identifiers_b,
                    prefix,
                    status_name,
                )
                if survivor_hash not in checkpoint["candidate_sha256"]:
                    checkpoint["candidate_sha256"].append(survivor_hash)
                    checkpoint["candidates"].append(candidate)
                    if candidate_path is not None:
                        save_survivor_catalog(candidate_path, checkpoint)
                add_assignment_nogood(
                    bundle.model,
                    bundle.identifiers,
                    identifiers_a,
                    identifiers_b,
                    f"current_survivor_{survivor_hash[:16]}",
                )
                continue
            if status == cp_model.INFEASIBLE:
                checkpoint["infeasible_cubes"] += 1
                cube_complete = True
                break
            if status == cp_model.UNKNOWN:
                break
            raise RuntimeError(f"unexpected CP-SAT status: {status_name}")

        if not cube_complete:
            children = split_cube(cube)
            if not children:
                checkpoint["pending_cubes"].insert(0, cube)
                checkpoint["status"] = "fully_fixed_cube_timed_out"
                save_checkpoint(checkpoint_path, checkpoint)
                break
            checkpoint["pending_cubes"] = (
                children + checkpoint["pending_cubes"]
            )
            checkpoint["split_cubes"] += 1
        save_checkpoint(checkpoint_path, checkpoint)

    if not checkpoint["pending_cubes"]:
        checkpoint["status"] = (
            "cp_sat_queue_exhausted_with_replayed_survivors"
            if checkpoint["candidates"]
            else "cp_sat_queue_exhausted_no_survivor_no_proof_certificate"
        )
    elif checkpoint["candidates"]:
        checkpoint["status"] = "in_progress_with_replayed_survivors"
    else:
        checkpoint["status"] = "in_progress"
    checkpoint["last_run_wall_seconds"] = time.monotonic() - started
    checkpoint["last_run_max_memory_mib"] = max_memory_mib
    checkpoint["last_run_workers"] = 1
    checkpoint["memory_parameter_is_hard_rss_limit"] = False
    save_checkpoint(checkpoint_path, checkpoint)
    if candidate_path is not None and checkpoint["candidates"]:
        save_survivor_catalog(candidate_path, checkpoint)
    return checkpoint


def run_self_test(max_memory_mib: int = 512) -> dict[str, Any]:
    """Cross-check the CP correlation layer on a pinned exact fixture."""

    quartet_census = audit_quartet_state_census()
    target, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
    bundle = build_profile_crt_model(
        target,
        enforce_crt=False,
        break_rotation_symmetry=False,
    )
    for channel, identifiers in enumerate((identifiers_a, identifiers_b)):
        for class_index, value in enumerate(identifiers):
            bundle.model.add(
                bundle.identifiers[channel][class_index] == value
            )
    solver = configure_solver(
        time_limit=10.0, max_memory_mib=min(max_memory_mib, 512)
    )
    status = solver.solve(bundle.model)
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        raise AssertionError("the fixed arithmetic fixture became infeasible")
    model_table = extract_correlation(solver, bundle)
    exact_table = profile_correlation_table(identifiers_a, identifiers_b)
    if model_table != exact_table:
        raise AssertionError(
            f"CP correlation table differs: {model_table} != {exact_table}"
        )

    full = build_profile_crt_model(
        target,
        enforce_crt=True,
        break_rotation_symmetry=False,
    )
    for channel, identifiers in enumerate((identifiers_a, identifiers_b)):
        for class_index, value in enumerate(identifiers):
            full.model.add(full.identifiers[channel][class_index] == value)
    full_solver = configure_solver(
        time_limit=10.0, max_memory_mib=min(max_memory_mib, 512)
    )
    full_status = full_solver.solve(full.model)
    if full_status != cp_model.INFEASIBLE:
        raise AssertionError(
            "the known transfer-failing fixture passed the full CRT model"
        )
    if full.exact_zero_equations != 12:
        raise AssertionError("the six exact Eisenstein equations changed")
    return {
        "fixture_target": target,
        "correlation_parts_checked": len(model_table),
        "model_matches_exact_replay": True,
        "known_bad_fixture_full_status": full_solver.status_name(full_status),
        "exact_zero_scalar_equations": full.exact_zero_equations,
        "correlation_coordinate_bound": CORRELATION_COORDINATE_BOUND,
        "semantic_fingerprint": semantic_fingerprint(),
        **quartet_census,
        "solver_workers": 1,
        "solver_memory_limit_mib": min(max_memory_mib, 512),
        "solver_memory_parameter_is_hard_rss_limit": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("output/lp333_order3_profile_crt_checkpoint.json"),
    )
    parser.add_argument("--candidate", type=Path)
    parser.add_argument(
        "--target-mode",
        choices=("formal", "lift", "all"),
        default="formal",
        help=(
            "formal=7 profile-equation orbit representatives; "
            "lift=12 representatives preserving the canonical zero words; "
            "all=22 targets"
        ),
    )
    parser.add_argument(
        "--target-index",
        action="append",
        type=int,
        help="override target mode with one or more indices in 0,...,21",
    )
    parser.add_argument(
        "--time-limit",
        type=float,
        default=DEFAULT_TOTAL_TIME_SECONDS,
        help="total wall-clock budget for this invocation (default: 60)",
    )
    parser.add_argument(
        "--cube-time-limit",
        type=float,
        default=DEFAULT_CUBE_TIME_SECONDS,
        help="per-cube CP-SAT budget before exact subdivision (default: 15)",
    )
    parser.add_argument(
        "--max-memory-mb",
        type=int,
        default=DEFAULT_MAX_MEMORY_MIB,
        help=(
            "CP-SAT advisory max_memory_in_mb parameter, at most 4096; "
            "this is not a hard process-RSS limit"
        ),
    )
    parser.add_argument(
        "--no-target-stabilizer-symmetry",
        "--no-rotation-symmetry",
        dest="no_target_stabilizer_symmetry",
        action="store_true",
        help="disable the exact fixed-target formal stabilizer lex leader",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run a fixed exact arithmetic cross-check and exit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.self_test:
        result = run_self_test(args.max_memory_mb)
        print(
            "correlation_parts_checked="
            f"{result['correlation_parts_checked']}"
        )
        print(
            "known_bad_fixture_full_status="
            f"{result['known_bad_fixture_full_status']}"
        )
        print("PASS: CP-SAT correlation layer matches exact replay")
        return

    modes = target_modes()
    if args.target_index:
        target_indices = tuple(dict.fromkeys(args.target_index))
        if any(not 0 <= value < 22 for value in target_indices):
            raise ValueError("target indices must lie in 0,...,21")
    else:
        target_indices = modes[args.target_mode]
    result = run_checkpoint(
        args.checkpoint,
        target_indices=target_indices,
        total_time_seconds=args.time_limit,
        cube_time_seconds=args.cube_time_limit,
        max_memory_mib=args.max_memory_mb,
        break_rotation_symmetry=not args.no_target_stabilizer_symmetry,
        candidate_path=args.candidate,
    )
    print(f"status={result['status']}")
    print(f"selected_target_indices={result['selected_target_indices']}")
    print(f"solver_calls={result['solver_calls']}")
    print(f"infeasible_cubes={result['infeasible_cubes']}")
    print(f"split_cubes={result['split_cubes']}")
    print(f"pending_cubes={len(result['pending_cubes'])}")
    print(f"candidate_count={len(result['candidates'])}")
    print(
        "solver_wall_time_seconds="
        f"{result['solver_wall_time_seconds']:.6f}"
    )
    print(f"checkpoint={args.checkpoint}")
    if result["candidates"]:
        print("PASS: candidate survived dependency-free exact replay")
        print("STATUS: profile zero gate only; no labelled lift or H(668)")
    else:
        print("STATUS: bounded resumable search checkpointed; no candidate")


if __name__ == "__main__":
    main()
