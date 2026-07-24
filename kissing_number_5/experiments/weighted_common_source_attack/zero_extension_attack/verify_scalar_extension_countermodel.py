#!/usr/bin/env python3
"""Verify an exact rank-11 countermodel to scalar zero-extension tests."""

from __future__ import annotations

from fractions import Fraction as Q
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "scalar_extension_countermodel.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rational_rank(matrix: list[list[int]]) -> int:
    work = [[Q(entry) for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, rows)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        value = work[rank][column]
        work[rank] = [entry / value for entry in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[rank], strict=True
                )
            ]
        rank += 1
    return rank


def d5_roots() -> list[tuple[int, ...]]:
    roots = []
    for i, j in itertools.combinations(range(5), 2):
        for first, second in itertools.product((-1, 1), repeat=2):
            point = [0] * 5
            point[i] = first
            point[j] = second
            roots.append(tuple(point))
    return roots


def verify_sparse_support(weight_units: list[int]) -> list[list[Q]]:
    indices = (9, 11, 16, 17, 26, 27, 28, 30, 12, 13, 14, 15)
    roots = d5_roots()
    selected = [roots[index] for index in indices]
    weights = [Q(unit, 20) for unit in weight_units]
    require(sum(weights) == 1, "support weights do not sum to one")
    for coordinate in range(5):
        require(
            sum(
                (
                    weight * point[coordinate]
                    for weight, point in zip(
                        weights, selected, strict=True
                    )
                ),
                Q(0),
            )
            == 0,
            "sparse D5 support is not centered",
        )
    for first in range(5):
        for second in range(5):
            covariance = sum(
                (
                    weight
                    * point[first]
                    * point[second]
                    / 2
                    for weight, point in zip(
                        weights, selected, strict=True
                    )
                ),
                Q(0),
            )
            expected = Q(1, 5) if first == second else Q(0)
            require(
                covariance == expected,
                "sparse D5 support is not isotropic",
            )
    return [
        [
            Q(
                sum(
                    left[coordinate] * right[coordinate]
                    for coordinate in range(5)
                ),
                2,
            )
            for right in selected
        ]
        for left in selected
    ]


def verify(certificate_path: Path = CERTIFICATE) -> dict[str, object]:
    data = json.loads(certificate_path.read_text())
    require(
        data["schema"]
        == "weighted-common-source.scalar-zero-extension-countermodel.v1",
        "wrong certificate schema",
    )
    require(
        data["status"]
        == "EXACT SCALAR RELAXATION COUNTERMODEL; NOT A GRAM MATRIX",
        "wrong scope status",
    )
    weight_units = data["support_weight_units_over_20"]
    require(
        weight_units == [2] * 8 + [1] * 4,
        "unexpected support weights",
    )
    support_gram = verify_sparse_support(weight_units)

    decode = {"+": 1, "0": 0, "-": -1}
    profiles = [
        [decode[character] for character in profile]
        for profile in data["profiles"]
    ]
    require(len(profiles) == 29, "wrong number of formal zero points")
    require(
        len({tuple(profile) for profile in profiles}) == 29,
        "duplicate formal zero point",
    )
    require(
        all(len(profile) == 12 for profile in profiles),
        "wrong height-profile length",
    )

    for profile in profiles:
        positive_units = sum(
            unit
            for unit, symbol in zip(
                weight_units, profile, strict=True
            )
            if symbol == 1
        )
        negative_units = sum(
            unit
            for unit, symbol in zip(
                weight_units, profile, strict=True
            )
            if symbol == -1
        )
        require(
            positive_units == negative_units == 8,
            "weighted mean or second moment failed",
        )
        weighted_mean = Q(1, 2) * Q(
            positive_units - negative_units, 20
        )
        weighted_second_moment = Q(1, 4) * Q(
            positive_units + negative_units, 20
        )
        require(weighted_mean == 0, "formal zero point is not centered")
        require(
            weighted_second_moment == Q(1, 5),
            "formal zero point has wrong second moment",
        )
        require(
            Q(negative_units, 20) >= Q(19, 147),
            "negative strict-tail mass failed",
        )
        require(
            Q(positive_units, 20) >= Q(1, 4),
            "positive strict-tail mass failed",
        )
        heights = [Q(symbol, 2) for symbol in profile]
        for first, second in itertools.combinations(range(12), 2):
            support_inner = support_gram[first][second]
            first_height = heights[first]
            second_height = heights[second]
            determinant = (
                1
                + 2
                * support_inner
                * first_height
                * second_height
                - support_inner**2
                - first_height**2
                - second_height**2
            )
            require(
                determinant >= 0,
                "support-support-zero Gram determinant failed",
            )

    largest_weighted_symbol_dot = None
    for left, right in itertools.combinations(profiles, 2):
        dot_units = sum(
            (
                unit * first * second
                for unit, first, second in zip(
                    weight_units, left, right, strict=True
                )
            ),
            0,
        )
        if (
            largest_weighted_symbol_dot is None
            or dot_units > largest_weighted_symbol_dot
        ):
            largest_weighted_symbol_dot = dot_units
        weighted_cross_moment = Q(dot_units, 80)
        require(
            weighted_cross_moment <= Q(1, 10),
            "pairwise weighted cross-moment kissing bound failed",
        )
        formal_inner = 5 * weighted_cross_moment
        for first_height, second_height in zip(
            left, right, strict=True
        ):
            first_height = Q(first_height, 2)
            second_height = Q(second_height, 2)
            determinant = (
                1
                + 2
                * formal_inner
                * first_height
                * second_height
                - formal_inner**2
                - first_height**2
                - second_height**2
            )
            require(
                determinant >= 0,
                "support-zero-zero Gram determinant failed",
            )

    rank = rational_rank(profiles)
    require(rank == data["claimed_profile_rank"], "claimed rank is false")
    require(rank == 7 > 5, "countermodel did not expose the rank gap")
    require(
        largest_weighted_symbol_dot == 8,
        "unexpected maximum weighted profile dot product",
    )

    # The exact projection-membership equality is <= 1/25 for every
    # profile and is equality precisely on the actual support column space.
    weights = [Q(unit, 20) for unit in weight_units]
    projection_energies = []
    for profile in profiles:
        heights = [Q(symbol, 2) for symbol in profile]
        energy = sum(
            (
                weights[i]
                * heights[i]
                * support_gram[i][j]
                * weights[j]
                * heights[j]
                for i in range(12)
                for j in range(12)
            ),
            Q(0),
        )
        require(
            energy <= Q(1, 25),
            "projection energy exceeds its exact upper bound",
        )
        projection_energies.append(energy)
    equality_profiles = sum(
        energy == Q(1, 25) for energy in projection_energies
    )
    require(
        equality_profiles == 2,
        "unexpected number of realized ternary profiles",
    )
    return {
        "status": "PASS",
        "scope": data["status"],
        "actual_D5_support_size": 12,
        "formal_zero_points": len(profiles),
        "formal_total_size": 12 + len(profiles),
        "maximum_formal_zero_inner_product": "1/2",
        "all_relevant_3_by_3_Gram_determinants": "nonnegative",
        "profile_rank": rank,
        "required_rank": 5,
        "profiles_passing_projection_equality": equality_profiles,
        "profiles_failing_projection_equality": len(profiles)
        - equality_profiles,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
