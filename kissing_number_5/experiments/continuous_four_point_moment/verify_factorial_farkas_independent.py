#!/usr/bin/env python3
"""Independent exact audit of the two K7-pool Farkas rays.

This implementation does not import the primary verifier.  It constructs
adjacency matrices directly from the CSV rows and checks the two dual
identities by elementary integer counting.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
POOL = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "k7"
    / "results"
    / "direct_k7_from_51.csv"
)
SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
POOL_SHA256 = (
    "16cee0b4f7b6b7655990a74f7ffef104c4aef43d5074696cbbb1bcf413d1a623"
)
PAIRS = tuple(itertools.combinations(range(7), 2))


def adjacency(edge_colors: tuple[int, ...]) -> list[list[int]]:
    matrix = [[-1 for _ in range(7)] for _ in range(7)]
    for vertex in range(7):
        matrix[vertex][vertex] = 7
    for color, (first, second) in zip(edge_colors, PAIRS):
        matrix[first][second] = color
        matrix[second][first] = color
    return matrix


def synthetic_adjacency() -> list[list[int]]:
    matrix = [[4 if i != j else 7 for j in range(7)] for i in range(7)]
    for vertex in range(2, 6):
        matrix[0][vertex] = matrix[vertex][0] = 6
        matrix[1][vertex] = matrix[vertex][1] = 6
    for first in (2, 3):
        for second in (4, 5):
            matrix[first][second] = matrix[second][first] = 6
    return matrix


def triangle_types(matrix: list[list[int]]) -> list[tuple[int, int, int]]:
    return [
        tuple(
            sorted(
                (
                    matrix[first][second],
                    matrix[first][third],
                    matrix[second][third],
                )
            )
        )
        for first, second, third in itertools.combinations(range(7), 3)
    ]


def verify() -> dict[str, object]:
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256
    assert hashlib.sha256(POOL.read_bytes()).hexdigest() == POOL_SHA256
    source = json.loads(SOURCE.read_text())
    nodes = tuple(Q(value) for value in source["grid"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])
    triple_index = {triple: index for index, triple in enumerate(triples)}

    lines = POOL.read_text().splitlines()
    records = [
        tuple(int(field) for field in line.split(",")) for line in lines[1:]
    ]
    assert len(records) == 1782

    r1 = (0, 20, -188, 1485, -9724, -65450)
    r2 = (20, -110, 748, -6545, 78540, -1452990)
    for common in range(4):
        assert (
            Q(13, 12) * r1[common] + Q(1, 4) * r2[common]
            == 5 - Q(65, 6) * common
        )

    matrices = []
    maximum_common = 0
    for record in records:
        matrix = adjacency(record[:21])
        matrices.append(matrix)
        stored_faces = tuple(record[21:])
        rebuilt_faces = tuple(
            sorted(triple_index[triple] for triple in triangle_types(matrix))
        )
        assert rebuilt_faces == stored_faces

        edges = common_total = first_row = second_row = 0
        for first, second in PAIRS:
            if matrix[first][second] != 4:
                continue
            edges += 1
            common = sum(
                matrix[first][vertex] == 6
                and matrix[second][vertex] == 6
                for vertex in range(7)
                if vertex not in (first, second)
            )
            maximum_common = max(maximum_common, common)
            common_total += common
            first_row += r1[common]
            second_row += r2[common]
        assert (
            Q(13, 12) * first_row
            + Q(1, 4) * second_row
            == 5 * edges - Q(65, 6) * common_total
        )
    assert maximum_common == 3

    cap_target = (
        5 * Q(21, 40) * alpha[4]
        - Q(65, 6) * Q(7, 312) * nu[triple_index[(4, 6, 6)]]
    )
    assert cap_target == Q(
        -10305950358714927, 1184000000000000
    ) < 0

    matrices.append(synthetic_adjacency())
    joint_column_values = []
    for matrix in matrices:
        local_01 = local_41 = 0
        for first, second in PAIRS:
            if matrix[first][second] != 1:
                continue
            residual = [
                vertex
                for vertex in range(7)
                if vertex not in (first, second)
            ]
            depth = sum(
                nodes[matrix[first][vertex]]
                + nodes[matrix[second][vertex]]
                < 0
                for vertex in residual
            )
            common = sum(
                matrix[first][vertex] >= 5
                and matrix[second][vertex] >= 5
                for vertex in residual
            )
            local_01 += common
            local_41 += math.comb(depth, 4) * common
        face_count = triangle_types(matrix).count((1, 5, 5))
        joint_column_values.append(
            local_01 - 2109 * local_41 - face_count
        )
    assert set(joint_column_values) == {0}

    for common in range(7):
        for depth in range(7, 40 - common):
            assert common * (
                -Q(5, 39)
                + Q(2109, math.comb(39, 5)) * math.comb(depth, 4)
            ) >= 0

    joint_target = -Q(7, 312) * nu[triple_index[(1, 5, 5)]]
    assert joint_target == Q(
        -44522548762943617, 22510800000000000000
    ) < 0
    return {
        "status": "PASS",
        "pool_columns": len(records),
        "cap_farkas_target": cap_target,
        "joint_augmented_columns": len(matrices),
        "joint_farkas_target": joint_target,
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
