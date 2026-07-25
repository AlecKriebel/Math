#!/usr/bin/env python3
"""Exact verifier for an out-of-catalog K7 dual counteratom."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

from experiments.root_triangle_k7_overlap.verify_exact_catalog_dual import (
    PAIRS7,
    PAIR_INDEX7,
    atom_projection,
    make_projector,
    rational_rank,
    require,
)


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
COUNTERATOM = HERE / "catalog_dual_counteratom.json"
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
CATALOG = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "k7"
    / "results"
    / "direct_k7_from_51.csv"
)


def determinant(matrix):
    size = len(matrix)
    work = [[Q(value) for value in row] for row in matrix]
    answer = Q(1)
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, size):
            scale = work[row][column] / pivot_value
            for entry in range(column + 1, size):
                work[row][entry] -= scale * work[column][entry]
    return answer


def gram(edges):
    matrix = [
        [4 if row == column else 0 for column in range(7)]
        for row in range(7)
    ]
    for (first, second), color in zip(PAIRS7, edges):
        value = color - 4
        matrix[first][second] = value
        matrix[second][first] = value
    return tuple(tuple(row) for row in matrix)


def verify():
    data = json.loads(COUNTERATOM.read_text())
    dual_path = ROOT / data["dual_certificate"]
    require(
        hashlib.sha256(dual_path.read_bytes()).hexdigest()
        == data["dual_certificate_sha256"],
        "dual certificate hash mismatch",
    )
    dual = json.loads(dual_path.read_text())
    factor = tuple(tuple(map(int, row)) for row in dual["factor_B"])
    multiplier = tuple(map(int, dual["triangle_dual_Y"]))
    edges = tuple(
        data[
            "edge_color_indices_01_02_03_04_05_06_12_13_14_15_16_23_24_25_26_34_35_36_45_46_56"
        ]
    )
    require(
        len(edges) == 21 and all(0 <= color <= 6 for color in edges),
        "invalid edge colors",
    )

    matrix = gram(edges)
    require(rational_rank(matrix) == 5, "counteratom rank is not five")
    for size in range(1, 8):
        for subset in itertools.combinations(range(7), size):
            principal = tuple(
                tuple(matrix[first][second] for second in subset)
                for first in subset
            )
            require(
                determinant(principal) >= 0,
                f"negative principal minor on {subset}",
            )

    source = json.loads(SOURCE.read_text())
    triple_index = {
        tuple(triple): index
        for index, triple in enumerate(source["triple_orbits"])
    }
    counts = [0] * 51
    for vertices in itertools.combinations(range(7), 3):
        colors = tuple(
            sorted(
                edges[PAIR_INDEX7[tuple(sorted(pair))]]
                for pair in itertools.combinations(vertices, 2)
            )
        )
        counts[triple_index[colors]] += 1
    require(
        [[index, count] for index, count in enumerate(counts) if count]
        == data["triangle_count_nonzero_entries"],
        "triangle counts mismatch",
    )

    projection = atom_projection(edges, make_projector(factor))
    require(
        projection == data["sum_of_squares_projection"],
        "sum-of-squares projection mismatch",
    )
    slack = (
        multiplier[0]
        + sum(
            multiplier[1 + triangle] * counts[triangle]
            for triangle in range(51)
        )
        - projection
    )
    require(slack == data["dual_slack"], "stored dual slack mismatch")
    require(slack < 0, "counteratom slack is not negative")

    catalog_edges = {
        tuple(map(int, line.split(",")))[:21]
        for line in CATALOG.read_text().splitlines()[1:]
    }
    require(edges not in catalog_edges, "counteratom is already in catalog")

    print(
        json.dumps(
            {
                "status": "PASS",
                "rank": 5,
                "PSD": "PASS",
                "catalog_membership": "absent",
                "dual_slack": slack,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    verify()
