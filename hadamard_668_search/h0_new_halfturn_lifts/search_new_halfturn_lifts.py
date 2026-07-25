#!/usr/bin/env python3
"""Bounded half-turn lift search for the three exact h0-p00-p02 profiles.

This program deliberately works only in the two lowest nonzero weight
shells of each profile's antisymmetric first-lift code.  It reconstructs
the affine/eigenspace algebra from the pinned profile IDs, enumerates the
complete antisymmetric code, and (unless ``--census-only`` is passed)
exhausts every symmetric second-digit slice in the selected shells.

The calculation is a profile-level lift audit, not an unrestricted LP(333)
search and not a construction of H(668).
"""

from __future__ import annotations

import argparse
from collections import Counter
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
MINIMAL_ROOT = SEARCH_ROOT / "h0_minimal_anti_code"
PHASE_ROOT = SEARCH_ROOT / "phase_second_digit"
sys.path.insert(0, str(HALFTURN_ROOT))
sys.path.insert(0, str(MINIMAL_ROOT))
sys.path.insert(0, str(PHASE_ROOT))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_h0_halfturn_twists as halfturn  # noqa: E402
import verify_h0_minimal_anti_code as minimal  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
from halfturn_profile_catalog import (  # noqa: E402
    profiles_from_strict_aggregate,
)
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    first_digit_equations,
    matrix_rank,
    profiles_from_ids,
)
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
)
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
)


ACTIVE_SECOND_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))
V1_PROFILE_RECORDS = (
    {
        "digest": "0x5b160dfa076231eb",
        "ids_a": (1, 8, 7, 1, 5, 7, 1, 8, 7, 1, 5, 7),
        "ids_b": (5, 7, 2, 6, 8, 5, 5, 7, 2, 6, 8, 5),
        "target": (4, 2, -2, 2),
    },
    {
        "digest": "0xfdb6a5c865468e1f",
        "ids_a": (4, 4, 5, 7, 7, 8, 4, 4, 5, 7, 7, 8),
        "ids_b": (1, 4, 7, 5, 5, 7, 1, 4, 7, 5, 5, 7),
        "target": (4, 2, -2, 2),
    },
    {
        "digest": "0xac3483a00651e7ce",
        "ids_a": (4, 8, 5, 7, 5, 1, 4, 8, 5, 7, 5, 1),
        "ids_b": (4, 1, 1, 5, 2, 4, 4, 1, 1, 5, 2, 4),
        "target": (4, 2, -2, 2),
    },
)
# Backward-compatible name used by the v1 detached verifier.
PROFILE_RECORDS = V1_PROFILE_RECORDS


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def reconstruct_profile(
    ids_a: Sequence[int],
    ids_b: Sequence[int],
) -> dict[str, object]:
    """Reconstruct the first-lift half-turn coordinates and digit-two forms."""

    profiles = profiles_from_ids(tuple(ids_a), tuple(ids_b))
    coordinates = active_trit_coordinates(profiles)
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    variables = len(coordinates)
    involution = tuple(
        coordinate_index[(channel, (class_index + 6) % 12, residue)]
        for channel, class_index, residue in coordinates
    )
    if any(involution[involution[index]] != index for index in range(variables)):
        raise AssertionError("the class half-turn is not an involution")

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
            for column in range(variables)
        )
        for index in range(variables)
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
            for column in range(variables)
        )
        for index in range(variables)
    )
    fixed_basis = second.nullspace_basis(
        coefficient_rows + fixed_rows,
        columns=variables,
    )
    anti_basis = second.nullspace_basis(
        coefficient_rows + anti_rows,
        columns=variables,
    )
    eigenbasis = fixed_basis + anti_basis
    first_dimension = variables - matrix_rank(coefficient_rows)
    if matrix_rank(eigenbasis) != first_dimension:
        raise AssertionError("the two eigenspaces do not span the first lift")

    origin = canonical_solution(first_rows, variables)
    if origin is None:
        raise AssertionError("the first placement digit is inconsistent")
    fixed_origin = tuple(
        2 * (int(origin[index]) + int(origin[involution[index]])) % 3
        for index in range(variables)
    )
    if any(
        (
            sum(row[index] * fixed_origin[index] for index in range(variables))
            - row[-1]
        )
        % 3
        for row in first_rows
    ):
        raise AssertionError("the symmetrized affine origin is invalid")

    term_data = second.second_digit_term_data(profiles)
    constants, linears, polars = second.derive_quadratics(
        term_data,
        fixed_origin,
        eigenbasis,
    )
    fixed_dimension = len(fixed_basis)
    anti_dimension = len(anti_basis)
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
            or any(map(int, linear[:fixed_dimension]))
            or any(
                int(polar[left][right])
                for left in range(fixed_dimension)
                for right in range(fixed_dimension)
            )
            or any(
                int(polar[left][right])
                for left in range(fixed_dimension, first_dimension)
                for right in range(fixed_dimension, first_dimension)
            )
        ):
            raise AssertionError("an odd equation lost bilinear-plus-anti shape")

    return {
        "profiles": profiles,
        "coordinates": coordinates,
        "coordinate_index": coordinate_index,
        "involution": involution,
        "first_rows": first_rows,
        "first_dimension": first_dimension,
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
) -> dict[str, object]:
    """Enumerate the complete natural antisymmetric ternary code."""

    coordinates = data["coordinates"]
    coordinate_index = data["coordinate_index"]
    anti_basis = data["anti_basis"]
    if (
        not isinstance(coordinates, tuple)
        or not isinstance(coordinate_index, dict)
        or not isinstance(anti_basis, tuple)
    ):
        raise AssertionError("profile reconstruction has invalid types")
    pair_coordinates = tuple(
        coordinate for coordinate in coordinates if coordinate[1] < 6
    )
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
    dimension, length = generator.shape
    if matrix_rank(tuple(map(tuple, generator.tolist()))) != dimension:
        raise AssertionError("the anti-code projection is not injective")

    powers = 3 ** np.arange(dimension, dtype=np.int64)
    histogram = np.zeros(length + 1, dtype=np.int64)
    coordinates_by_weight: dict[int, list[tuple[int, ...]]] = {}
    first_two_positive: list[int] = []
    for lower in range(0, 3**dimension, chunk_size):
        numbers = np.arange(
            lower,
            min(lower + chunk_size, 3**dimension),
            dtype=np.int64,
        )
        coefficients = (
            (numbers[:, None] // powers[None, :]) % 3
        ).astype(np.int16)
        words = (coefficients @ generator) % 3
        weights = np.count_nonzero(words, axis=1)
        histogram += np.bincount(weights, minlength=length + 1)
        observed = sorted(
            int(value) for value in np.unique(weights) if int(value) > 0
        )
        for weight in observed:
            if weight not in first_two_positive:
                first_two_positive.append(weight)
                first_two_positive.sort()
                del first_two_positive[2:]
            if weight in first_two_positive:
                coordinates_by_weight.setdefault(weight, []).extend(
                    tuple(map(int, coefficients[index]))
                    for index in np.flatnonzero(weights == weight)
                )
        # A newly discovered lower shell can displace an earlier provisional
        # shell.  Drop it so only the globally two smallest survive.
        for weight in tuple(coordinates_by_weight):
            if weight not in first_two_positive:
                del coordinates_by_weight[weight]

    weight_histogram = {
        weight: int(count)
        for weight, count in enumerate(histogram)
        if int(count)
    }
    if sum(weight_histogram.values()) != 3**dimension:
        raise AssertionError("the anti-code census lost a word")
    shell_weights = tuple(sorted(first_two_positive))
    if len(shell_weights) != 2:
        raise AssertionError("fewer than two positive anti shells were found")
    shell_coordinates = {
        weight: tuple(coordinates_by_weight[weight])
        for weight in shell_weights
    }
    if any(
        len(shell_coordinates[weight]) != weight_histogram[weight]
        for weight in shell_weights
    ):
        raise AssertionError("a selected anti shell was not retained completely")
    return {
        "length": length,
        "dimension": dimension,
        "weight_histogram": weight_histogram,
        "shell_weights": shell_weights,
        "shell_coordinates": shell_coordinates,
        "pair_coordinates": pair_coordinates,
        "generator": generator,
    }


def odd_slice_consistent(
    data: dict[str, object],
    anti_coordinates: Sequence[int],
) -> tuple[bool, int, int | None]:
    """Return consistency, coefficient rank, and affine dimension."""

    fixed_dimension = len(data["fixed_basis"])
    anti_dimension = len(data["anti_basis"])
    minus_forms = data["minus_forms"]
    if not isinstance(minus_forms, tuple):
        raise AssertionError("the reconstructed odd forms have wrong type")
    rows = []
    for _, linear, polar in minus_forms:
        coefficients = tuple(
            sum(
                int(polar[column][fixed_dimension + anti_index])
                * int(anti_coordinates[anti_index])
                for anti_index in range(anti_dimension)
            )
            % 3
            for column in range(fixed_dimension)
        )
        rhs = (
            -sum(
                int(linear[fixed_dimension + anti_index])
                * int(anti_coordinates[anti_index])
                for anti_index in range(anti_dimension)
            )
        ) % 3
        rows.append(coefficients + (rhs,))
    rows_tuple = tuple(rows)
    coefficient_rank = matrix_rank(tuple(row[:-1] for row in rows_tuple))
    augmented_rank = matrix_rank(rows_tuple)
    if augmented_rank != coefficient_rank:
        return False, coefficient_rank, None
    return True, coefficient_rank, fixed_dimension - coefficient_rank


def shell_lift_census(
    data: dict[str, object],
    shell_coordinates: Sequence[Sequence[int]],
    allowed_margin_sums: set[tuple[int, ...]],
) -> dict[str, object]:
    """Exhaust every symmetric slice over one signed anti-weight shell."""

    record_histogram: Counter[str] = Counter()
    odd_rank_histogram: Counter[int] = Counter()
    dimension_histogram: Counter[str] = Counter()
    digit_three_histogram: Counter[int] = Counter()
    digit_two_points = 0
    row_margin_compatible_points = 0
    consistent_slices = 0
    for index, anti_coordinates in enumerate(shell_coordinates):
        consistent, odd_rank, dimension = odd_slice_consistent(
            data, anti_coordinates
        )
        odd_rank_histogram[odd_rank] += 1
        if not consistent:
            dimension_histogram["inconsistent"] += 1
            record = {
                "consistent": False,
                "odd_rank": odd_rank,
                "affine_dimension": None,
                "digit_two_points": 0,
                "row_margin_compatible_points": 0,
                "digit_three_histogram": {},
            }
        else:
            consistent_slices += 1
            if dimension is None:
                raise AssertionError("a consistent slice lost its dimension")
            dimension_histogram[str(dimension)] += 1
            raw_record = minimal.enumerate_slice(
                data,
                anti_coordinates,
                allowed_margin_sums,
            )
            if (
                int(raw_record["odd_rank"]) != odd_rank
                or int(raw_record["affine_dimension"]) != dimension
            ):
                raise AssertionError("the independent odd-system ranks differ")
            record = {"consistent": True, **raw_record}
            digit_two_points += int(record["digit_two_points"])
            row_margin_compatible_points += int(
                record["row_margin_compatible_points"]
            )
            digit_three_histogram.update(
                {
                    int(defect): int(count)
                    for defect, count in record[
                        "digit_three_histogram"
                    ].items()
                }
            )
        record_histogram[
            json.dumps(record, separators=(",", ":"), sort_keys=True)
        ] += 1
        print(
            "slice",
            index + 1,
            "/",
            len(shell_coordinates),
            json.dumps(record, separators=(",", ":"), sort_keys=True),
            flush=True,
        )
    minimum_digit_three_defect = (
        min(digit_three_histogram) if digit_three_histogram else None
    )
    return {
        "signed_anti_words": len(shell_coordinates),
        "consistent_slices": consistent_slices,
        "odd_rank_histogram": dict(sorted(odd_rank_histogram.items())),
        "affine_dimension_histogram": dict(
            sorted(dimension_histogram.items())
        ),
        "digit_two_points": digit_two_points,
        "row_margin_compatible_points": row_margin_compatible_points,
        "digit_three_histogram": dict(sorted(digit_three_histogram.items())),
        "minimum_digit_three_defect": minimum_digit_three_defect,
        "full_digit_three_points": int(digit_three_histogram.get(0, 0)),
        "slice_record_histogram": dict(sorted(record_histogram.items())),
        "anti_coordinate_sha256": compact_hash(tuple(shell_coordinates)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--structure-only",
        action="store_true",
        help="stop after exact-profile and half-turn eigenspace checks",
    )
    mode.add_argument(
        "--census-only",
        action="store_true",
        help="stop after the eigenspace and complete anti-code censuses",
    )
    parser.add_argument(
        "--profile",
        default="all",
        help="one digest from the selected catalog (default: all)",
    )
    parser.add_argument(
        "--aggregate",
        type=Path,
        help=(
            "strict production-v2 aggregate; discovers every half-turn-fixed "
            "h0 profile instead of using the frozen v1 three-profile list"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    catalog = None
    if args.aggregate is None:
        source_records = V1_PROFILE_RECORDS
    else:
        catalog = profiles_from_strict_aggregate(args.aggregate.resolve())
        source_records = catalog["profiles"]
        if not isinstance(source_records, tuple):
            raise AssertionError("the aggregate catalog has wrong types")
    selected = tuple(
        record
        for record in source_records
        if args.profile == "all" or record["digest"] == args.profile
    )
    if not selected:
        raise SystemExit(
            f"profile {args.profile!r} is absent from the selected catalog"
        )
    records = []
    for profile_record in selected:
        data = reconstruct_profile(
            profile_record["ids_a"], profile_record["ids_b"]
        )
        record = {
            **profile_record,
            "first_affine_dimension": data["first_dimension"],
            "fixed_eigenspace_dimension": len(data["fixed_basis"]),
            "anti_eigenspace_dimension": len(data["anti_basis"]),
        }
        if not args.structure_only:
            census = anti_code_census(data)
            record.update({
                "anti_code_parameters": (
                    census["length"],
                    census["dimension"],
                    census["shell_weights"][0],
                ),
                "anti_weight_histogram": census["weight_histogram"],
                "selected_shell_weights": census["shell_weights"],
                "selected_shell_sizes": tuple(
                    len(census["shell_coordinates"][weight])
                    for weight in census["shell_weights"]
                ),
            })
        if not args.census_only and not args.structure_only:
            margin_catalog = catalog_phase_sum_intersection(
                profile_record["ids_a"], profile_record["ids_b"]
            )
            allowed_margin_targets = tuple(
                tuple(
                    coordinate
                    for channel in sums
                    for value in channel
                    for coordinate in value
                )
                for sums, _ in margin_catalog["phase_sum_corpus"]
            )
            allowed_margin_sums = set(allowed_margin_targets)
            if len(allowed_margin_sums) != len(allowed_margin_targets):
                raise AssertionError("the row-margin catalog has duplicates")
            record["exact_row_margin_catalog_size"] = len(
                allowed_margin_sums
            )
            shell_records = {}
            for weight in census["shell_weights"]:
                print(
                    f"BEGIN digest={profile_record['digest']} weight={weight}",
                    flush=True,
                )
                shell_records[str(weight)] = shell_lift_census(
                    data,
                    census["shell_coordinates"][weight],
                    allowed_margin_sums,
                )
            record["shell_records"] = shell_records
        records.append(record)
        print("PROFILE_RESULT " + json.dumps(record, sort_keys=True))
    if args.structure_only:
        schema = "lp333-new-halfturn-lifts-structure-v2"
        scope = (
            "exact profile and half-turn eigenspace reconstruction only; "
            "no anti-code or digit-two enumeration"
        )
    elif args.census_only:
        schema = "lp333-new-halfturn-lifts-census-v2"
        scope = "complete anti-code censuses; no digit-two shell lift yet"
    else:
        schema = "lp333-new-halfturn-lifts-v2"
        scope = (
            "complete two-lowest-anti-weight shell lift for each "
            "selected half-turn profile"
        )
    result = {
        "schema": schema,
        "profile_source": (
            "frozen-v1-three-profile-list"
            if args.aggregate is None
            else "strict-production-v2-aggregate"
        ),
        "profiles": records,
        "scope": scope,
    }
    if args.aggregate is not None:
        if catalog is None:
            raise AssertionError("the aggregate catalog was lost")
        result["aggregate_catalog_counts"] = {
            "all_exact_h0_orbits": catalog["all_exact_h0_orbits"],
            "halfturn_fixed_orbits": catalog["halfturn_fixed_orbits"],
        }
    print(f"semantic_sha256={compact_hash(result)}")
    print("PASS")


if __name__ == "__main__":
    main()
