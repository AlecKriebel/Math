#!/usr/bin/env python3
"""Exact quadratic-class fiber-twist census for the pinned h=0 profile.

For each channel choose an orientation ``epsilon`` and a function
``f:F_3 -> F_3``.  On the opposite class pair ``j,j+6`` impose

    W_(j+6)(s,q) = W_j(s, epsilon*q + f(j mod 3)).

Every function on F_3 is represented by a unique polynomial of degree at
most two, hence the name of the family.  There are

    (2*3^3)^2 = 2916

channel-paired constructions.  The constant functions are the old global
S3 twists, while the affine functions are the smaller class-shear theorem
in ``verify_h0_affine_class_twists.py``.

All dimension-nine systems are exhausted directly.  Three exceptional
nonidentity systems are reduced by the six exact zero-polar combinations of
the second-digit quadrics.  The resulting dimensions are nine, fifteen,
and fifteen.  The dimension-nine exception is exhausted directly; each
dimension-fifteen exception is exhausted by an exact three-block quadratic
enumerator.  Every second-digit survivor is replayed at digit three and
against the exact row-margin catalog.

This is a structured-family obstruction for one profile, not an LP(333) or
H(668).
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "quadratic_class_twists_certificate.json"
SEARCH_ROOT = HERE.parent
HALFTURN_ROOT = SEARCH_ROOT / "h0_halfturn_twists"
PHASE_ROOT = SEARCH_ROOT / "phase_second_digit"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HALFTURN_ROOT))
sys.path.insert(0, str(PHASE_ROOT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_h0_affine_class_twists as affine  # noqa: E402
import verify_h0_halfturn_twists as halfturn  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
from verify_lp333_order3_labeled_jet import actual_word  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    first_digit_equations,
    matrix_rank,
    profiles_from_ids,
)
from verify_lp333_order3_phase_transfer import row_sum_catalog  # noqa: E402
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
)


MODULUS = 3
PARAMETERS = tuple(
    (orientation,) + shifts
    for orientation in (1, 2)
    for shifts in product(range(3), repeat=3)
)
IDENTITY = (1, 0, 0, 0)
ACTIVE_SECOND_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))
EXCEPTIONAL_DIMENSION_21 = (
    ((1, 0, 0, 1), (1, 2, 2, 1)),
    ((1, 0, 0, 2), (1, 1, 1, 2)),
)
EXCEPTIONAL_DIMENSION_15 = (
    (2, 2, 0, 2),
    (2, 1, 2, 2),
)
EXPECTED_RECORDS_SHA256 = (
    "fd206c20369202d649f28b35b74d8f17e0ab4e18951702ab32d9a927e163758e"
)
EXPECTED_SURVIVORS_SHA256 = (
    "0c3b0a40ad1882011dd284e28238be0f73bedfb2b7778f10597b4ed61c6a2f5e"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return sha256(payload).hexdigest()


def periodic_permutation(
    parameters: Sequence[int], class_index: int
) -> tuple[int, int, int]:
    """Return ``q -> epsilon*q+f(j mod 3)``."""

    if (
        len(parameters) != 4
        or int(parameters[0]) % MODULUS not in (1, 2)
        or not 0 <= class_index < 6
    ):
        raise ValueError("invalid quadratic-class parameters")
    orientation = int(parameters[0]) % MODULUS
    shifts = tuple(int(value) % MODULUS for value in parameters[1:])
    permutation = tuple(
        (
            orientation * quotient
            + shifts[class_index % MODULUS]
        )
        % MODULUS
        for quotient in range(MODULUS)
    )
    if set(permutation) != set(range(MODULUS)):
        raise AssertionError("a periodic affine rule is not a permutation")
    return permutation  # type: ignore[return-value]


def quadratic_class_system(
    parameters_a: Sequence[int],
    parameters_b: Sequence[int],
) -> tuple[
    tuple[tuple[tuple[int, int, int], ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[int, ...] | None,
    tuple[tuple[int, ...], ...] | None,
]:
    """Construct the exact first-digit system for one paired family."""

    profiles = profiles_from_ids(
        halfturn.PROFILE_IDS_A,
        halfturn.PROFILE_IDS_B,
    )
    coordinates = active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    rows = list(augmented_system(first_digit_equations(profiles)))
    for channel, parameters in enumerate((parameters_a, parameters_b)):
        for class_index in range(6):
            opposite = class_index + 6
            if profiles[channel][class_index] != profiles[channel][opposite]:
                raise AssertionError("the pinned profile lost its half-turn")
            permutation = periodic_permutation(parameters, class_index)
            for residue, count in enumerate(
                profiles[channel][class_index]
            ):
                if count not in (1, 2):
                    continue
                trit_slope, trit_offset = (
                    halfturn.permutation_affine_action(count, permutation)
                )
                row = [0] * (len(coordinates) + 1)
                row[
                    coordinate_index[(channel, opposite, residue)]
                ] = 1
                row[
                    coordinate_index[(channel, class_index, residue)]
                ] = -trit_slope % MODULUS
                row[-1] = trit_offset
                rows.append(tuple(row))

    normalized_rows = tuple(rows)
    origin = canonical_solution(normalized_rows, len(coordinates))
    if origin is None:
        return profiles, normalized_rows, None, None
    basis = second.nullspace_basis(
        tuple(row[:-1] for row in normalized_rows),
        columns=len(coordinates),
    )
    return profiles, normalized_rows, origin, basis


def compose_basis(
    outer: Sequence[Sequence[int]],
    inner: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Compose row-vector bases over F_3."""

    return tuple(
        tuple(
            sum(
                int(inner_row[index]) * int(outer[index][coordinate])
                for index in range(len(outer))
            )
            % MODULUS
            for coordinate in range(len(outer[0]))
        )
        for inner_row in inner
    )


def zero_polar_slice(
    profiles: Sequence[Sequence[Sequence[int]]],
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
) -> tuple[
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    dict[str, object],
]:
    """Impose all affine combinations whose quadratic polar part vanishes."""

    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles),
        origin,
        basis,
    )
    variables = len(basis)
    flattened = tuple(
        tuple(
            int(polars[equation][left][right]) % MODULUS
            for left in range(variables)
            for right in range(left, variables)
        )
        for equation in ACTIVE_SECOND_ROWS
    )
    transposed = tuple(
        tuple(
            flattened[equation][coordinate]
            for equation in range(len(ACTIVE_SECOND_ROWS))
        )
        for coordinate in range(len(flattened[0]))
    )
    zero_polar_combinations = second.nullspace_basis(
        transposed,
        columns=len(ACTIVE_SECOND_ROWS),
    )
    if len(zero_polar_combinations) != 6:
        raise AssertionError("the exceptional polar nullity changed")

    affine_rows = []
    for coefficients in zero_polar_combinations:
        linear = tuple(
            sum(
                int(coefficients[row])
                * int(linears[ACTIVE_SECOND_ROWS[row]][column])
                for row in range(len(ACTIVE_SECOND_ROWS))
            )
            % MODULUS
            for column in range(variables)
        )
        constant = sum(
            int(coefficients[row])
            * int(constants[ACTIVE_SECOND_ROWS[row]])
            for row in range(len(ACTIVE_SECOND_ROWS))
        ) % MODULUS
        affine_rows.append(linear + ((-constant) % MODULUS,))
    affine_rows = tuple(affine_rows)
    coefficient_rank = matrix_rank(
        tuple(row[:-1] for row in affine_rows)
    )
    augmented_rank = matrix_rank(affine_rows)
    if (coefficient_rank, augmented_rank) != (6, 6):
        raise AssertionError("the six hidden affine equations changed rank")

    inner_origin = canonical_solution(affine_rows, variables)
    if inner_origin is None:
        raise AssertionError("a hidden affine slice became inconsistent")
    inner_basis = second.nullspace_basis(
        tuple(row[:-1] for row in affine_rows),
        columns=variables,
    )
    placement_origin = second.lift_affine_point(
        origin, basis, inner_origin
    )
    placement_basis = compose_basis(basis, inner_basis)
    if matrix_rank(placement_basis) != variables - 6:
        raise AssertionError("the composed exceptional basis lost rank")
    return placement_origin, placement_basis, {
        "polar_span_rank": len(ACTIVE_SECOND_ROWS) - 6,
        "zero_polar_combinations": 6,
        "affine_rank": 6,
        "reduced_dimension": len(placement_basis),
    }


def ordinary_quadratic_value(
    constant: int,
    linear: Sequence[int],
    polar: Sequence[Sequence[int]],
    point: Sequence[int],
) -> int:
    """Evaluate the audited polar convention directly over F_3."""

    value = int(constant)
    for left in range(len(point)):
        value += int(linear[left]) * int(point[left])
        value += (
            2
            * int(polar[left][left])
            * int(point[left])
            * int(point[left])
        )
        for right in range(left + 1, len(point)):
            value += (
                int(polar[left][right])
                * int(point[left])
                * int(point[right])
            )
    return value % MODULUS


def exhaust_dimension_fifteen(
    profiles: Sequence[Sequence[Sequence[int]]],
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Exhaust 3^15 points with an exact three-block quadratic table."""

    if len(basis) != 15:
        raise ValueError("the three-block enumerator requires dimension 15")
    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles),
        origin,
        basis,
    )
    assignments = tuple(product(range(MODULUS), repeat=5))
    block_size = len(assignments)
    blocks = (range(0, 5), range(5, 10), range(10, 15))

    def within(
        equation: int,
        indices: range,
        point: Sequence[int],
    ) -> int:
        value = int(constants[equation]) if indices.start == 0 else 0
        for local_left, left in enumerate(indices):
            value += int(linears[equation][left]) * int(point[local_left])
            value += (
                2
                * int(polars[equation][left][left])
                * int(point[local_left])
                * int(point[local_left])
            )
            for local_right in range(local_left + 1, 5):
                right = indices.start + local_right
                value += (
                    int(polars[equation][left][right])
                    * int(point[local_left])
                    * int(point[local_right])
                )
        return value % MODULUS

    def cross(
        equation: int,
        left_indices: range,
        right_indices: range,
        left_point: Sequence[int],
        right_point: Sequence[int],
    ) -> int:
        return sum(
            int(polars[equation][left][right])
            * int(left_point[local_left])
            * int(right_point[local_right])
            for local_left, left in enumerate(left_indices)
            for local_right, right in enumerate(right_indices)
        ) % MODULUS

    ab_tables = []
    ac_tables = []
    bc_tables = []
    for equation in ACTIVE_SECOND_ROWS:
        q_a = tuple(
            within(equation, blocks[0], point)
            for point in assignments
        )
        q_b = tuple(
            within(equation, blocks[1], point)
            for point in assignments
        )
        q_c = tuple(
            within(equation, blocks[2], point)
            for point in assignments
        )
        ab_tables.append(tuple(
            (
                q_a[left]
                + q_b[right]
                + cross(
                    equation,
                    blocks[0],
                    blocks[1],
                    assignments[left],
                    assignments[right],
                )
            )
            % MODULUS
            for left in range(block_size)
            for right in range(block_size)
        ))
        ac_tables.append(tuple(
            (
                q_c[right]
                + cross(
                    equation,
                    blocks[0],
                    blocks[2],
                    assignments[left],
                    assignments[right],
                )
            )
            % MODULUS
            for left in range(block_size)
            for right in range(block_size)
        ))
        bc_tables.append(tuple(
            cross(
                equation,
                blocks[1],
                blocks[2],
                assignments[left],
                assignments[right],
            )
            for left in range(block_size)
            for right in range(block_size)
        ))

    survivors = []
    for first in range(block_size):
        first_offset = first * block_size
        for second_index in range(block_size):
            ab_index = first_offset + second_index
            second_offset = second_index * block_size
            for third in range(block_size):
                ac_index = first_offset + third
                bc_index = second_offset + third
                if all(
                    (
                        ab_tables[equation][ab_index]
                        + ac_tables[equation][ac_index]
                        + bc_tables[equation][bc_index]
                    )
                    % MODULUS
                    == 0
                    for equation in range(len(ACTIVE_SECOND_ROWS))
                ):
                    point = (
                        assignments[first]
                        + assignments[second_index]
                        + assignments[third]
                    )
                    # Detached direct evaluation of all eighteen rows.
                    if any(
                        ordinary_quadratic_value(
                            constants[equation],
                            linears[equation],
                            polars[equation],
                            point,
                        )
                        for equation in ACTIVE_SECOND_ROWS
                    ):
                        raise AssertionError(
                            "a block-enumeration survivor failed direct replay"
                        )
                    survivors.append(point)
    return tuple(survivors)


def labelled_aggregate(
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> tuple[int, ...]:
    """Recover the exact 18-coordinate row-margin aggregate."""

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


def replay_exceptional_survivors(
    profiles: Sequence[Sequence[Sequence[int]]],
    parameters: tuple[tuple[int, ...], tuple[int, ...]],
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
    affine_points: Sequence[Sequence[int]],
    catalog: set[tuple[int, ...]],
) -> tuple[dict[str, object], ...]:
    """Replay every structured digit-two survivor exactly."""

    term_data = second.second_digit_term_data(profiles)
    first_equations = first_digit_equations(profiles)
    records = []
    for affine_point in affine_points:
        placement = second.lift_affine_point(
            origin, basis, affine_point
        )
        if second.symbolic_first_digits(
            first_equations, placement
        ) != (0,) * 20:
            raise AssertionError("an exceptional point failed digit one")
        if second.symbolic_second_digits(
            term_data, placement
        ) != (0,) * 20:
            raise AssertionError("an exceptional point failed digit two")
        if second.direct_second_digits(
            profiles, placement
        ) != (0,) * 20:
            raise AssertionError(
                "an exceptional point failed direct digit-two replay"
            )

        displayed = second.displayed_values(profiles, placement)
        digits = tuple(
            second.lambda_digits(value, 12) for value in displayed
        )
        digit_counts = tuple(
            sum(row[digit] != 0 for row in digits)
            for digit in range(12)
        )
        if digit_counts[:3] != (0, 0, 0):
            raise AssertionError("a digit-two survivor lost its prefix")
        if digit_counts[3] == 0:
            raise AssertionError(
                "a quadratic-class survivor unexpectedly reached digit three"
            )

        masks_a, masks_b = second.masks_from_trits(
            profiles, placement
        )
        aggregate = labelled_aggregate(masks_a, masks_b)
        row_margin_member = aggregate in catalog
        if row_margin_member:
            raise AssertionError(
                "a quadratic-class survivor entered the row-margin catalog"
            )
        records.append({
            "parameters_a": parameters[0],
            "parameters_b": parameters[1],
            "affine_coordinates": tuple(affine_point),
            "placement_trits": placement,
            "masks_a": masks_a,
            "masks_b": masks_b,
            "digit_counts": digit_counts,
            "row_margin_aggregate": aggregate,
            "row_margin_member": row_margin_member,
        })
    return tuple(records)


def classify_quadratic_class_twists() -> dict[str, object]:
    """Classify all 54^2 families through the first decisive failed digit."""

    records = []
    outcome_histogram: Counter[str] = Counter()
    global_histogram: Counter[str] = Counter()
    affine_histogram: Counter[str] = Counter()
    dimension_nine_points = 0
    exceptional_survivors = []
    exceptional_metadata = {}
    catalog = set(row_sum_catalog())

    for parameters_a in PARAMETERS:
        for parameters_b in PARAMETERS:
            profiles, rows, origin, basis = quadratic_class_system(
                parameters_a,
                parameters_b,
            )
            coefficient_rank = matrix_rank(
                tuple(row[:-1] for row in rows)
            )
            augmented_rank = matrix_rank(rows)
            is_global = (
                parameters_a[1] == parameters_a[2] == parameters_a[3]
                and parameters_b[1] == parameters_b[2] == parameters_b[3]
            )
            is_affine = (
                (
                    parameters_a[2] - parameters_a[1]
                )
                % MODULUS
                == (
                    parameters_a[3] - parameters_a[2]
                )
                % MODULUS
                and (
                    parameters_b[2] - parameters_b[1]
                )
                % MODULUS
                == (
                    parameters_b[3] - parameters_b[2]
                )
                % MODULUS
            )

            if origin is None:
                if augmented_rank != coefficient_rank + 1:
                    raise AssertionError(
                        "an inconsistent family did not gain one rank"
                    )
                dimension = None
                second_digit_survivors = None
                failed_digit = 1
                outcome = "inconsistent"
            else:
                if basis is None or coefficient_rank != augmented_rank:
                    raise AssertionError("a consistent family lost its basis")
                dimension = len(basis)
                if dimension == 9:
                    second_digit_survivors = (
                        halfturn.exhaust_dimension_nine_second_digit(
                            profiles,
                            origin,
                            basis,
                        )
                    )
                    dimension_nine_points += MODULUS**9
                    if second_digit_survivors:
                        raise AssertionError(
                            "a generic quadratic-class family survived digit two"
                        )
                    failed_digit = 2
                    outcome = "dimension_9"
                elif dimension == 15:
                    if (
                        tuple(parameters_a),
                        tuple(parameters_b),
                    ) != EXCEPTIONAL_DIMENSION_15:
                        raise AssertionError(
                            "the dimension-15 exception moved"
                        )
                    reduced_origin, reduced_basis, metadata = (
                        zero_polar_slice(profiles, origin, basis)
                    )
                    if len(reduced_basis) != 9:
                        raise AssertionError(
                            "the dimension-15 exception did not reduce to nine"
                        )
                    second_digit_survivors = (
                        halfturn.exhaust_dimension_nine_second_digit(
                            profiles,
                            reduced_origin,
                            reduced_basis,
                        )
                    )
                    if second_digit_survivors:
                        raise AssertionError(
                            "the dimension-15 exception survived digit two"
                        )
                    exceptional_metadata["dimension_15"] = metadata
                    failed_digit = 2
                    outcome = "dimension_15"
                elif dimension == 21:
                    parameters = (
                        tuple(parameters_a),
                        tuple(parameters_b),
                    )
                    if parameters == (IDENTITY, IDENTITY):
                        second_digit_survivors = None
                        failed_digit = None
                        outcome = "identity_dimension_21"
                    else:
                        if parameters not in EXCEPTIONAL_DIMENSION_21:
                            raise AssertionError(
                                "a dimension-21 exception moved"
                            )
                        reduced_origin, reduced_basis, metadata = (
                            zero_polar_slice(profiles, origin, basis)
                        )
                        if len(reduced_basis) != 15:
                            raise AssertionError(
                                "a dimension-21 exception did not reduce to 15"
                            )
                        affine_points = exhaust_dimension_fifteen(
                            profiles,
                            reduced_origin,
                            reduced_basis,
                        )
                        if len(affine_points) != 24:
                            raise AssertionError(
                                "an exceptional digit-two count changed"
                            )
                        replayed = replay_exceptional_survivors(
                            profiles,
                            parameters,
                            reduced_origin,
                            reduced_basis,
                            affine_points,
                            catalog,
                        )
                        exceptional_survivors.extend(replayed)
                        exceptional_metadata[str(parameters)] = metadata
                        second_digit_survivors = len(affine_points)
                        failed_digit = 3
                        outcome = "nonidentity_dimension_21"
                else:
                    raise AssertionError(
                        f"unexpected affine dimension {dimension}"
                    )

            outcome_histogram[outcome] += 1
            if is_global:
                global_histogram[outcome] += 1
            if is_affine:
                affine_histogram[outcome] += 1
            records.append({
                "parameters_a": tuple(parameters_a),
                "parameters_b": tuple(parameters_b),
                "coefficient_rank": coefficient_rank,
                "augmented_rank": augmented_rank,
                "dimension": dimension,
                "second_digit_survivors": second_digit_survivors,
                "failed_digit": failed_digit,
                "global_constant_subfamily": is_global,
                "affine_class_subfamily": is_affine,
            })

    expected_outcomes = {
        "inconsistent": 1454,
        "dimension_9": 1458,
        "identity_dimension_21": 1,
        "nonidentity_dimension_21": 2,
        "dimension_15": 1,
    }
    expected_global = {
        "inconsistent": 17,
        "dimension_9": 18,
        "identity_dimension_21": 1,
    }
    expected_affine = {
        "inconsistent": 161,
        "dimension_9": 162,
        "identity_dimension_21": 1,
    }
    expected_non_affine = {
        "inconsistent": 1293,
        "dimension_9": 1296,
        "nonidentity_dimension_21": 2,
        "dimension_15": 1,
    }
    if dict(outcome_histogram) != expected_outcomes:
        raise AssertionError(
            f"quadratic-class outcomes changed: {dict(outcome_histogram)}"
        )
    if dict(global_histogram) != expected_global:
        raise AssertionError(
            f"global-subfamily outcomes changed: {dict(global_histogram)}"
        )
    if dict(affine_histogram) != expected_affine:
        raise AssertionError(
            f"affine-subfamily outcomes changed: {dict(affine_histogram)}"
        )
    non_affine_histogram = Counter(outcome_histogram)
    non_affine_histogram.subtract(affine_histogram)
    non_affine_histogram += Counter()
    if dict(non_affine_histogram) != expected_non_affine:
        raise AssertionError(
            "non-affine-class outcomes changed: "
            f"{dict(non_affine_histogram)}"
        )
    if dimension_nine_points != 1458 * MODULUS**9:
        raise AssertionError("the generic dimension-nine census changed")
    if len(exceptional_survivors) != 48:
        raise AssertionError("the exceptional survivor corpus changed")

    digit_three_histogram = Counter(
        int(record["digit_counts"][3])  # type: ignore[index]
        for record in exceptional_survivors
    )
    expected_digit_three_histogram = {
        8: 2,
        10: 2,
        11: 12,
        12: 6,
        13: 6,
        14: 8,
        15: 6,
        16: 6,
    }
    if dict(sorted(digit_three_histogram.items())) != (
        expected_digit_three_histogram
    ):
        raise AssertionError(
            "the exceptional digit-three histogram changed"
        )

    records_hash = compact_hash(records)
    survivors_hash = compact_hash(exceptional_survivors)
    if EXPECTED_RECORDS_SHA256 and records_hash != EXPECTED_RECORDS_SHA256:
        raise AssertionError(
            f"record hash changed: {records_hash}"
        )
    if (
        EXPECTED_SURVIVORS_SHA256
        and survivors_hash != EXPECTED_SURVIVORS_SHA256
    ):
        raise AssertionError(
            f"survivor hash changed: {survivors_hash}"
        )

    result = {
        "families": len(records),
        "affine_class_subfamily_families": sum(
            bool(record["affine_class_subfamily"]) for record in records
        ),
        "new_non_affine_class_families": sum(
            not bool(record["affine_class_subfamily"])
            for record in records
        ),
        "nonidentity_families_locally_excluded": len(records) - 1,
        "outcome_histogram": expected_outcomes,
        "global_subfamily_histogram": expected_global,
        "affine_subfamily_histogram": expected_affine,
        "new_non_affine_subfamily_histogram": expected_non_affine,
        "generic_dimension_nine_points_exhausted":
            dimension_nine_points,
        "dimension_fifteen_exception_points_exhausted": MODULUS**9,
        "dimension_twenty_one_exception_points_exhausted":
            2 * MODULUS**15,
        "exceptional_digit_two_survivors": len(exceptional_survivors),
        "exceptional_digit_three_survivors": 0,
        "exceptional_row_margin_members": 0,
        "digit_three_residual_histogram":
            expected_digit_three_histogram,
        "exceptional_metadata": exceptional_metadata,
        "records_sha256": records_hash,
        "survivors_sha256": survivors_hash,
        "status": "PASS",
    }
    verify_certificate(result, exceptional_survivors)
    return result


def verify_certificate(
    result: dict[str, object],
    exceptional_survivors: Sequence[dict[str, object]],
) -> None:
    """Replay the explicit compact certificate for the two exceptions."""

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    expected_summary = {
        "families": result["families"],
        "affine_class_subfamily_families":
            result["affine_class_subfamily_families"],
        "new_non_affine_class_families":
            result["new_non_affine_class_families"],
        "nonidentity_families_locally_excluded":
            result["nonidentity_families_locally_excluded"],
        "records_sha256": result["records_sha256"],
        "survivors_sha256": result["survivors_sha256"],
        "exceptional_digit_two_survivors":
            result["exceptional_digit_two_survivors"],
        "exceptional_digit_three_survivors":
            result["exceptional_digit_three_survivors"],
        "exceptional_row_margin_members":
            result["exceptional_row_margin_members"],
    }
    if certificate["summary"] != expected_summary:
        raise AssertionError("the compact certificate summary changed")

    for pinned in certificate["dimension_21_exceptions"]:
        parameters = (
            tuple(pinned["parameters_a"]),
            tuple(pinned["parameters_b"]),
        )
        records = tuple(
            record
            for record in exceptional_survivors
            if (
                tuple(record["parameters_a"]),  # type: ignore[arg-type]
                tuple(record["parameters_b"]),  # type: ignore[arg-type]
            )
            == parameters
        )
        if len(records) != pinned["digit_two_survivors"]:
            raise AssertionError("a pinned exception lost a survivor")
        first = records[0]
        representative = pinned["enumeration_first_representative"]
        checks = {
            "affine_coordinates":
                list(first["affine_coordinates"]),
            "placement_trits":
                list(first["placement_trits"]),
            "masks_a": list(first["masks_a"]),
            "masks_b": list(first["masks_b"]),
            "digit_counts": list(first["digit_counts"]),
            "row_margin_aggregate":
                list(first["row_margin_aggregate"]),
        }
        if representative != checks:
            raise AssertionError(
                "an explicit exceptional representative changed"
            )


def main() -> None:
    result = classify_quadratic_class_twists()
    for key, value in result.items():
        print(f"{key}={value}")
    print("PASS: all quadratic-class fiber twists classified")
    print("STATUS: structured h=0 obstruction only; no LP(333) or H(668)")


if __name__ == "__main__":
    main()
