#!/usr/bin/env python3
"""Exact verifier for the low-harmonic rank/frame-potential barrier.

Only Python's standard library and fractions.Fraction are used.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import itertools
import json
from pathlib import Path


HARMONIC_DIMENSIONS = (1, 5, 14, 30)
EXPECTED_MINIMUM = Q(7796592200083, 800000000000000)


def gegenbauer_5(t: Q, maximum_degree: int = 3) -> list[Q]:
    values = [Q(1)]
    if maximum_degree:
        values.append(t)
    for k in range(2, maximum_degree + 1):
        values.append(
            ((2 * k + 1) * t * values[-1] - (k - 1) * values[-2])
            / (k + 2)
        )
    return values


def determinant(matrix: list[list[Q]]) -> Q:
    work = [row[:] for row in matrix]
    result = Q(1)
    for column in range(len(work)):
        pivot = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result *= pivot_value
        for row in range(column + 1, len(work)):
            multiplier = work[row][column] / pivot_value
            for entry in range(column + 1, len(work)):
                work[row][entry] -= multiplier * work[column][entry]
    return result


def verify(source_path: Path) -> dict[str, object]:
    source = json.loads(source_path.read_text())
    assert (
        source["schema"]
        == "fixed41-bv-fullradial-k16-pseudodistribution-v1"
    )
    assert source["dimension"] == 5
    cardinality = source["cardinality"]
    assert cardinality == 41
    assert Q(source["maximum_inner_product"]) == Q(1, 2)

    nodes = [Q(value) for value in source["grid"]]
    weights = [Q(value) for value in source["alpha"]]
    assert nodes == [
        Q(-1),
        Q(-3, 4),
        Q(-1, 2),
        Q(-1, 4),
        Q(0),
        Q(1, 4),
        Q(1, 2),
    ]
    assert len(weights) == len(nodes)
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == cardinality - 1

    polynomial_values = [gegenbauer_5(node) for node in nodes]
    checked_subsets: list[dict[str, object]] = []
    positive_minors: list[tuple[Q, tuple[int, ...], tuple[int, ...]]] = []

    for mask in range(1, 1 << len(HARMONIC_DIMENSIONS)):
        degrees = tuple(
            degree
            for degree in range(len(HARMONIC_DIMENSIONS))
            if mask & (1 << degree)
        )
        rank_bound = sum(HARMONIC_DIMENSIONS[degree] for degree in degrees)
        if rank_bound >= cardinality:
            continue

        matrix = [
            [
                Q(1)
                + sum(
                    weight
                    * polynomial_values[index][degree_a]
                    * polynomial_values[index][degree_b]
                    for index, weight in enumerate(weights)
                )
                - Q(cardinality, rank_bound)
                for degree_b in degrees
            ]
            for degree_a in degrees
        ]
        minimum_minor: Q | None = None
        for size in range(1, len(degrees) + 1):
            for indices in itertools.combinations(range(len(degrees)), size):
                minor = determinant(
                    [[matrix[i][j] for j in indices] for i in indices]
                )
                assert minor >= 0
                if minor > 0:
                    positive_minors.append((minor, degrees, indices))
                    if minimum_minor is None or minor < minimum_minor:
                        minimum_minor = minor
        checked_subsets.append(
            {
                "degrees": list(degrees),
                "rank_bound": rank_bound,
                "determinant": str(determinant(matrix)),
                "minimum_positive_principal_minor": (
                    None if minimum_minor is None else str(minimum_minor)
                ),
            }
        )

    assert len(checked_subsets) == 11
    global_minimum = min(positive_minors)
    assert global_minimum == (EXPECTED_MINIMUM, (1,), (0,))
    return {
        "status": "PASS",
        "cardinality": cardinality,
        "checked_harmonic_subsets": checked_subsets,
        "minimum_positive_principal_minor": str(global_minimum[0]),
        "minimum_location": {
            "degrees": list(global_minimum[1]),
            "indices": list(global_minimum[2]),
        },
        "conclusion": (
            "the all-harmonic mass-41 witness passes every "
            "low-harmonic rank/frame matrix inequality"
        ),
    }


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=(
            project_root
            / "certificates"
            / "fixed41_bv_fullradial_k16_pseudodistribution.json"
        ),
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.source), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
