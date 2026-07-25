#!/usr/bin/env python3
"""Discover and exactly reconstruct K4/K5 local extensions of the repaired witness."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
from scipy.sparse import csc_matrix


ROOT = Path(__file__).resolve().parents[3]
SOURCE = (
    ROOT
    / "experiments"
    / "centered_integer_degree_moments"
    / "repaired_pair_triple_local_3.json"
)
ENUMERATION = (
    ROOT
    / "experiments"
    / "centered_atomic_bv_barrier"
    / "results"
    / "k5_triangle_vectors.csv"
)
OUTPUT = Path(__file__).resolve().parent / "repaired_local_k4_k5_extension.json"
K4_EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
K5_EDGES = (
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def solve_square(matrix: list[list[Q]], target: list[Q]) -> list[Q]:
    size = len(matrix)
    assert size == len(target) and all(len(row) == size for row in matrix)
    work = [row[:] + [rhs] for row, rhs in zip(matrix, target)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [value / scale for value in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(work[row], work[column])
            ]
    return [work[row][-1] for row in range(size)]


def determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    result = 0
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        product = math.prod(matrix[i][permutation[i]] for i in range(size))
        result += (-1 if inversions % 2 else 1) * product
    return result


def triangle_types(
    vertex_count: int,
    edge_positions: tuple[tuple[int, int], ...],
    edges: tuple[int, ...],
) -> tuple[tuple[int, int, int], ...]:
    edge = {pair: color for pair, color in zip(edge_positions, edges)}
    return tuple(
        tuple(sorted((edge[(i, j)], edge[(i, k)], edge[(j, k)])))
        for i in range(vertex_count)
        for j in range(i + 1, vertex_count)
        for k in range(j + 1, vertex_count)
    )


def exact_sparse_solution(
    matrix: csc_matrix | np.ndarray,
    target_exact: list[Q],
) -> tuple[tuple[int, ...], list[Q]]:
    target = np.asarray([float(value) for value in target_exact])
    result = linprog(
        np.zeros(matrix.shape[1]),
        A_eq=matrix,
        b_eq=target,
        bounds=(0, None),
        method="highs",
    )
    assert result.success, result.message
    active = tuple(int(index) for index in np.flatnonzero(result.x > 1.0e-9))
    assert len(active) == matrix.shape[0] - 1
    active_matrix = (
        matrix[:, list(active)].toarray()
        if isinstance(matrix, csc_matrix)
        else matrix[:, list(active)]
    )
    assert np.linalg.matrix_rank(active_matrix) == len(active)
    _q, _r, row_permutation = qr(
        active_matrix.T, mode="economic", pivoting=True
    )
    rows = tuple(int(index) for index in row_permutation[: len(active)])
    exact_matrix = [
        [Q(int(active_matrix[row, column])) for column in range(len(active))]
        for row in rows
    ]
    weights = solve_square(
        exact_matrix,
        [target_exact[row] for row in rows],
    )
    assert all(weight > 0 for weight in weights)
    assert all(
        sum(
            Q(int(active_matrix[row, column])) * weight
            for column, weight in enumerate(weights)
        )
        == target_exact[row]
        for row in range(len(target_exact))
    )
    return active, weights


def main() -> None:
    source_bytes = SOURCE.read_bytes()
    source = json.loads(source_bytes)
    triples = tuple(tuple(row) for row in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    nu = [Q(value) for value in source["nu"]]
    scaled_nodes = tuple(int(4 * Q(value)) for value in source["grid"])

    k4_representatives: dict[tuple[int, ...], tuple[int, ...]] = {}
    feasible_labeled_k4 = 0
    for edges in itertools.product(range(7), repeat=6):
        faces = triangle_types(4, K4_EDGES, edges)
        if any(face not in triple_index for face in faces):
            continue
        gram = [[4 if i == j else 0 for j in range(4)] for i in range(4)]
        for color, (i, j) in zip(edges, K4_EDGES):
            gram[i][j] = gram[j][i] = scaled_nodes[color]
        if determinant(gram) < 0:
            continue
        feasible_labeled_k4 += 1
        counts = [0] * len(triples)
        for face in faces:
            counts[triple_index[face]] += 1
        k4_representatives.setdefault(tuple(counts), edges)
    k4_features = tuple(k4_representatives)
    k4_matrix = np.asarray([[1, *counts] for counts in k4_features]).T
    k4_target = [Q(1), *(value / 390 for value in nu)]
    k4_active, k4_weights = exact_sparse_solution(k4_matrix, k4_target)

    enumeration_bytes = ENUMERATION.read_bytes()
    lines = enumeration_bytes.decode().splitlines()
    assert lines[0] == (
        "# feasible_labeled_k5=12087822 "
        "distinct_triangle_count_vectors=105930"
    )
    k5_representatives: list[tuple[int, ...]] = []
    k5_features: list[tuple[int, ...]] = []
    row_indices: list[int] = []
    column_indices: list[int] = []
    coefficients: list[float] = []
    for column, line in enumerate(lines[1:]):
        fields = line.split(",")
        edges = tuple(map(int, fields[1:]))
        faces = triangle_types(5, K5_EDGES, edges)
        counts = [0] * len(triples)
        for face in faces:
            counts[triple_index[face]] += 1
        reconstructed_key = 0
        for index in sorted(triple_index[face] for face in faces):
            reconstructed_key = (reconstructed_key << 6) | index
        assert reconstructed_key == int(fields[0])
        k5_representatives.append(edges)
        k5_features.append(tuple(counts))
        row_indices.append(0)
        column_indices.append(column)
        coefficients.append(1.0)
        for index, count in enumerate(counts):
            if count:
                row_indices.append(1 + index)
                column_indices.append(column)
                coefficients.append(float(count))
    assert len(k5_features) == 105930
    k5_matrix = csc_matrix(
        (coefficients, (row_indices, column_indices)),
        shape=(1 + len(triples), len(k5_features)),
    )
    k5_target = [Q(1), *(value / 156 for value in nu)]
    k5_active, k5_weights = exact_sparse_solution(k5_matrix, k5_target)

    certificate = {
        "schema": "kissing5.repaired_centered_local_k4_k5_extension.v1",
        "status": (
            "exact separate symmetric local K4 and K5 Gram-PSD extensions "
            "of one repaired pair/triple witness; not a code or a mutually "
            "consistent hierarchy"
        ),
        "source_certificate": SOURCE.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "grid_numerators_over_four": list(scaled_nodes),
        "k4": {
            "normalization": "expected face counts equal nu/390",
            "feasible_labeled_count": feasible_labeled_k4,
            "distinct_triangle_count_vectors": len(k4_features),
            "positive_atom_count": len(k4_active),
            "atoms": [
                {
                    "edge_color_indices_01_02_03_12_13_23": list(
                        k4_representatives[k4_features[column]]
                    ),
                    "weight": qstr(weight),
                }
                for column, weight in zip(k4_active, k4_weights)
            ],
        },
        "k5": {
            "normalization": "expected triangle counts equal nu/156",
            "discovery_enumeration_sha256": hashlib.sha256(
                enumeration_bytes
            ).hexdigest(),
            "distinct_triangle_count_vectors": len(k5_features),
            "positive_atom_count": len(k5_active),
            "atoms": [
                {
                    "edge_color_indices_01_02_03_04_12_13_14_23_24_34": list(
                        k5_representatives[column]
                    ),
                    "weight": qstr(weight),
                }
                for column, weight in zip(k5_active, k5_weights)
            ],
        },
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)
    print(hashlib.sha256(OUTPUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
