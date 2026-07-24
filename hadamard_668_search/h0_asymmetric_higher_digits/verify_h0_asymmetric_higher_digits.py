#!/usr/bin/env python3
"""Exact replay of the first asymmetric lift of the h=0 profile.

The exact order-three profile is invariant under the class half-turn
``j -> j+6``.  Its rank-18 first placement layer splits into a 21-dimensional
fixed space and a 15-dimensional anti-fixed space.  This verifier fixes the
first canonical anti direction, solves the six half-turn-odd second-digit
equations, and reconstructs the resulting 15-dimensional affine slice.

The pinned point in that slice is an exact digit-2 witness.  It is neither a
digit-3 witness nor row-margin compatible.  Solver telemetry in the companion
certificate is deliberately treated only as a bounded UNKNOWN observation.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_phase_second_digit as second  # noqa: E402
from verify_lp333_order3_labeled_jet import (  # noqa: E402
    actual_word,
    validate_labelled_certificate,
)
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    first_digit_equations,
    matrix_rank,
    profiles_from_ids,
)
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    row_sum_catalog,
)


CERTIFICATE = HERE / "certificate.json"
PROFILE_IDS_A = (1, 1, 2, 4, 4, 5, 1, 1, 2, 4, 4, 5)
PROFILE_IDS_B = (5, 5, 1, 7, 4, 1, 5, 5, 1, 7, 4, 1)
TARGET = (2, -2, -4, -2)
ANTI_DIRECTION = (1,) + (0,) * 14

ASYMMETRIC_PLACEMENT = (
    0, 2, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 2, 0, 1, 1,
    1, 2, 2, 0, 2, 0, 1, 0, 2, 1, 2, 0, 0, 0, 2, 1, 2, 0,
    2, 1, 0, 2, 2, 1, 2, 0, 0, 0, 2, 1, 2, 0, 2, 1, 0, 2,
)

IDENTITY_CONTROL_PLACEMENT = (
    1, 1, 2, 0, 2, 0, 0, 2, 0, 1, 2, 2, 1, 1, 1, 2, 0, 2,
    0, 0, 2, 0, 1, 2, 2, 1, 1, 1, 2, 1, 0, 0, 2, 0, 1, 1,
    2, 0, 1, 1, 1, 1, 2, 1, 0, 0, 2, 0, 1, 1, 2, 0, 1, 1,
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def halfturn_rows(
    halfturn: Sequence[int],
    sign: int,
) -> tuple[tuple[int, ...], ...]:
    """Return equations ``u_i - sign*u_T(i) = 0`` over F_3."""

    return tuple(
        tuple(
            (
                1
                if column == index
                else -int(sign)
                if column == halfturn[index]
                else 0
            )
            % 3
            for column in range(54)
        )
        for index in range(54)
    )


def combine_basis(
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
            % 3
            for coordinate in range(len(outer[0]))
        )
        for inner_row in inner
    )


def add_vectors(*vectors: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        sum(int(vector[index]) for vector in vectors) % 3
        for index in range(len(vectors[0]))
    )


def scaled_combination(
    basis: Sequence[Sequence[int]],
    coefficients: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        sum(
            int(coefficients[index]) * int(basis[index][coordinate])
            for index in range(len(basis))
        )
        % 3
        for coordinate in range(len(basis[0]))
    )


def labelled_aggregate(
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> tuple[int, ...]:
    """Recover the 18-coordinate row-margin aggregate from labelled masks."""

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


def effective_form_count(
    profiles,
    origin: Sequence[int],
    basis: Sequence[Sequence[int]],
) -> int:
    """Count exact phase forms after composition with one affine slice."""

    forms = set()
    for terms, _ in second.second_digit_term_data(profiles):
        for term in terms:
            constant = (
                int(term.constant)
                + sum(
                    int(coefficient) * int(origin[variable])
                    for variable, coefficient in term.coefficients
                )
            ) % 3
            slopes = tuple(
                sum(
                    int(coefficient) * int(basis[index][variable])
                    for variable, coefficient in term.coefficients
                )
                % 3
                for index in range(len(basis))
            )
            forms.add((constant, slopes))
    return len(forms)


def reconstruct_slice() -> dict[str, object]:
    profiles = profiles_from_ids(PROFILE_IDS_A, PROFILE_IDS_B)
    coordinates = second.active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    halfturn = tuple(
        coordinate_index[(channel, (class_index + 6) % 12, residue)]
        for channel, class_index, residue in coordinates
    )
    if any(halfturn[halfturn[index]] != index for index in range(54)):
        raise AssertionError("the class half-turn stopped being an involution")

    first_rows = augmented_system(first_digit_equations(profiles))
    first_coefficients = tuple(row[:-1] for row in first_rows)
    fixed_basis = second.nullspace_basis(
        first_coefficients + halfturn_rows(halfturn, 1),
        columns=54,
    )
    anti_basis = second.nullspace_basis(
        first_coefficients + halfturn_rows(halfturn, -1),
        columns=54,
    )
    if (len(fixed_basis), len(anti_basis)) != (21, 15):
        raise AssertionError("the half-turn eigenspace dimensions changed")
    if matrix_rank(fixed_basis + anti_basis) != 36:
        raise AssertionError("the eigenspaces no longer span the first layer")

    canonical_origin = canonical_solution(first_rows, 54)
    if canonical_origin is None:
        raise AssertionError("the first placement layer became inconsistent")
    fixed_origin = tuple(
        2
        * (
            int(canonical_origin[index])
            + int(canonical_origin[halfturn[index]])
        )
        % 3
        for index in range(54)
    )

    term_data = second.second_digit_term_data(profiles)
    constants, linears, polars = second.derive_quadratics(
        term_data,
        fixed_origin,
        fixed_basis + anti_basis,
    )

    # For fixed anti coordinate y, the six output-odd equations are linear
    # in the 21 fixed coordinates x:
    #
    #   (B_k y).x = -l_k.y,  k=0,...,5.
    odd_rows = []
    for output in range(6):
        coefficients = tuple(
            sum(
                (
                    int(polars[8 + output][left][21 + right])
                    - int(polars[14 + output][left][21 + right])
                )
                * ANTI_DIRECTION[right]
                for right in range(15)
            )
            % 3
            for left in range(21)
        )
        right_hand_side = -sum(
            (
                int(linears[8 + output][21 + right])
                - int(linears[14 + output][21 + right])
            )
            * ANTI_DIRECTION[right]
            for right in range(15)
        ) % 3
        odd_rows.append(coefficients + (right_hand_side,))
    odd_rows = tuple(odd_rows)
    if (
        matrix_rank(tuple(row[:-1] for row in odd_rows)),
        matrix_rank(odd_rows),
    ) != (6, 6):
        raise AssertionError("the six output-odd rows changed rank")

    fixed_coordinate_origin = canonical_solution(odd_rows, 21)
    if fixed_coordinate_origin is None:
        raise AssertionError("the output-odd slice became inconsistent")
    fixed_coordinate_basis = second.nullspace_basis(
        tuple(row[:-1] for row in odd_rows),
        columns=21,
    )
    if len(fixed_coordinate_basis) != 15:
        raise AssertionError("the asymmetric slice dimension changed")

    placement_origin = add_vectors(
        fixed_origin,
        scaled_combination(anti_basis, ANTI_DIRECTION),
        scaled_combination(fixed_basis, fixed_coordinate_origin),
    )
    placement_basis = combine_basis(
        fixed_basis, fixed_coordinate_basis
    )
    if matrix_rank(placement_basis) != 15:
        raise AssertionError("the physical slice basis lost rank")

    coordinate_rows = tuple(
        tuple(
            placement_basis[index][coordinate] for index in range(15)
        )
        + (
            (
                ASYMMETRIC_PLACEMENT[coordinate]
                - placement_origin[coordinate]
            )
            % 3,
        )
        for coordinate in range(54)
    )
    affine_coordinates = canonical_solution(coordinate_rows, 15)
    if affine_coordinates is None:
        raise AssertionError("the pinned witness left the asymmetric slice")
    if second.lift_affine_point(
        placement_origin, placement_basis, affine_coordinates
    ) != ASYMMETRIC_PLACEMENT:
        raise AssertionError("the pinned asymmetric coordinates failed")

    first = second.symbolic_first_digits(
        first_digit_equations(profiles), ASYMMETRIC_PLACEMENT
    )
    symbolic_second = second.symbolic_second_digits(
        term_data, ASYMMETRIC_PLACEMENT
    )
    direct_second = second.direct_second_digits(
        profiles, ASYMMETRIC_PLACEMENT
    )
    if first != (0,) * 20:
        raise AssertionError("the asymmetric witness failed digit 1")
    if symbolic_second != (0,) * 20 or direct_second != (0,) * 20:
        raise AssertionError("the asymmetric witness failed digit 2")

    values = second.displayed_values(profiles, ASYMMETRIC_PLACEMENT)
    digits = tuple(second.lambda_digits(value, 12) for value in values)
    digit_counts = tuple(
        sum(row[digit] != 0 for row in digits) for digit in range(12)
    )
    if digit_counts[:4] != (0, 0, 0, 13):
        raise AssertionError("the pinned digit prefix changed")
    if all(
        ASYMMETRIC_PLACEMENT[index]
        == ASYMMETRIC_PLACEMENT[halfturn[index]]
        for index in range(54)
    ):
        raise AssertionError("the asymmetric witness became half-turn fixed")

    masks_a, masks_b = second.masks_from_trits(
        profiles, ASYMMETRIC_PLACEMENT
    )
    aggregate = labelled_aggregate(masks_a, masks_b)
    catalog = row_sum_catalog()
    if aggregate in catalog:
        raise AssertionError("the asymmetric witness entered the row catalog")
    try:
        validate_labelled_certificate(aggregate, masks_a, masks_b)
    except ValueError as error:
        row_margin_failure = str(error)
    else:
        raise AssertionError("the asymmetric witness passed row-margin replay")
    if row_margin_failure != "exact zero-column-lag equation failed":
        raise AssertionError("the row-margin failure mode changed")

    # Exact size of the compact A,Q digit-3 model used for the bounded run.
    forms = effective_form_count(
        profiles, placement_origin, placement_basis
    )
    model_variables = 15 + 3 * forms + 2 * 19
    model_constraints = 2 * forms + 2 * 19
    if (forms, model_variables, model_constraints) != (411, 1286, 860):
        raise AssertionError("the compact digit-3 model size changed")

    # Detached replay of the half-turn-fixed diagnostic control.
    if any(
        IDENTITY_CONTROL_PLACEMENT[index]
        != IDENTITY_CONTROL_PLACEMENT[halfturn[index]]
        for index in range(54)
    ):
        raise AssertionError("the identity control lost half-turn symmetry")
    control_first = second.symbolic_first_digits(
        first_digit_equations(profiles), IDENTITY_CONTROL_PLACEMENT
    )
    control_second = second.direct_second_digits(
        profiles, IDENTITY_CONTROL_PLACEMENT
    )
    if control_first != (0,) * 20 or control_second != (0,) * 20:
        raise AssertionError("the identity control lost digit 2")
    control_values = second.displayed_values(
        profiles, IDENTITY_CONTROL_PLACEMENT
    )
    control_digits = tuple(
        second.lambda_digits(value, 12) for value in control_values
    )
    control_counts = tuple(
        sum(row[digit] != 0 for row in control_digits)
        for digit in range(12)
    )
    if control_counts[:4] != (0, 0, 0, 11):
        raise AssertionError("the identity-control prefix changed")

    return {
        "profile_ids_a": PROFILE_IDS_A,
        "profile_ids_b": PROFILE_IDS_B,
        "target": TARGET,
        "first_layer_rank": matrix_rank(first_coefficients),
        "first_layer_nullity": 54 - matrix_rank(first_coefficients),
        "fixed_dimension": len(fixed_basis),
        "anti_dimension": len(anti_basis),
        "odd_slice_rank": matrix_rank(
            tuple(row[:-1] for row in odd_rows)
        ),
        "slice_dimension": len(placement_basis),
        "anti_direction": ANTI_DIRECTION,
        "fixed_basis_sha256": compact_hash(fixed_basis),
        "anti_basis_sha256": compact_hash(anti_basis),
        "placement_origin_sha256": compact_hash(placement_origin),
        "placement_basis_sha256": compact_hash(placement_basis),
        "affine_coordinates": affine_coordinates,
        "affine_coordinates_sha256": compact_hash(affine_coordinates),
        "placement_trits": ASYMMETRIC_PLACEMENT,
        "placement_trits_sha256": compact_hash(ASYMMETRIC_PLACEMENT),
        "displayed_values_sha256": compact_hash(values),
        "lambda_digits_sha256": compact_hash(digits),
        "digit_residual_counts": digit_counts,
        "halfturn_fixed": False,
        "row_margin_aggregate": aggregate,
        "row_margin_catalog_rows": len(catalog),
        "row_margin_catalog_member": False,
        "row_margin_failure": row_margin_failure,
        "compact_digit3_model": {
            "affine_variables": 15,
            "effective_phase_forms": forms,
            "variables": model_variables,
            "constraints": model_constraints,
        },
        "identity_control": {
            "placement_trits_sha256": compact_hash(
                IDENTITY_CONTROL_PLACEMENT
            ),
            "displayed_values_sha256": compact_hash(control_values),
            "lambda_digits_sha256": compact_hash(control_digits),
            "digit_residual_counts": control_counts,
            "halfturn_fixed": True,
        },
    }


def audit() -> dict[str, object]:
    stored = json.loads(CERTIFICATE.read_text())
    reconstructed = reconstruct_slice()

    exact_fields = (
        "profile_ids_a",
        "profile_ids_b",
        "target",
        "first_layer_rank",
        "first_layer_nullity",
        "fixed_dimension",
        "anti_dimension",
        "odd_slice_rank",
        "slice_dimension",
        "anti_direction",
        "fixed_basis_sha256",
        "anti_basis_sha256",
        "placement_origin_sha256",
        "placement_basis_sha256",
        "affine_coordinates",
        "affine_coordinates_sha256",
        "placement_trits",
        "placement_trits_sha256",
        "displayed_values_sha256",
        "lambda_digits_sha256",
        "digit_residual_counts",
        "halfturn_fixed",
        "row_margin_aggregate",
        "row_margin_catalog_rows",
        "row_margin_catalog_member",
        "row_margin_failure",
        "compact_digit3_model",
    )
    for field in exact_fields:
        expected = json.loads(json.dumps(reconstructed[field]))
        if stored[field] != expected:
            raise AssertionError(f"certificate field changed: {field}")

    for field, value in reconstructed["identity_control"].items():
        expected = json.loads(json.dumps(value))
        if stored["identity_control"][field] != expected:
            raise AssertionError(
                f"identity-control certificate field changed: {field}"
            )

    bounded = stored["bounded_digit3_search"]
    if bounded["status"] != "UNKNOWN":
        raise AssertionError("the bounded run must not imply an exclusion")
    if bounded["workers"] > 4 or bounded["peak_rss_bytes"] >= 4 << 30:
        raise AssertionError("the bounded run exceeded its hardware cap")
    if bounded["model"] != stored["compact_digit3_model"]:
        raise AssertionError("the bounded run model metadata changed")

    identity_search = stored["identity_control"]["bounded_digit3_search"]
    if identity_search["status"] != "INTERRUPTED_UNKNOWN":
        raise AssertionError("the identity control scope changed")
    if not identity_search["diagnostic_only"]:
        raise AssertionError("the identity control lost its warning")

    return {
        "schema": stored["schema"],
        "label": stored["label"],
        "first_layer": (
            reconstructed["first_layer_rank"],
            reconstructed["first_layer_nullity"],
        ),
        "halfturn_dimensions": (
            reconstructed["fixed_dimension"],
            reconstructed["anti_dimension"],
        ),
        "asymmetric_slice": (
            reconstructed["odd_slice_rank"],
            reconstructed["slice_dimension"],
        ),
        "zero_digit_prefix": 2,
        "digit_3_nonzero_rows": reconstructed[
            "digit_residual_counts"
        ][3],
        "row_margin_catalog_member": False,
        "bounded_digit3_status": bounded["status"],
        "identity_control_status": identity_search["status"],
        "placement_trits_sha256": reconstructed[
            "placement_trits_sha256"
        ],
    }


def main() -> None:
    result = audit()
    print(json.dumps(result, indent=2))
    print(f"semantic_sha256={compact_hash(result)}")
    print("PASS: asymmetric h=0 digit-2 witness replayed exactly")
    print("NO CLAIM: digit 3 remains UNKNOWN and row margins fail")


if __name__ == "__main__":
    main()
