#!/usr/bin/env python3
"""Find and exactly reconstruct a local Gram-PSD K4 extension.

The linear program is discovery-only.  Once a 51-column basis is selected,
the stored weights are solved from the rational triangle marginal by exact
Gaussian elimination and checked against every marginal row.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog

from rationalize import qstr, solve_square


EDGE_POSITIONS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
DETERMINANT_PERMUTATIONS = tuple(itertools.permutations(range(4)))


def determinant_4(matrix: list[list[int]]) -> int:
    answer = 0
    for permutation in DETERMINANT_PERMUTATIONS:
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(4)
            for j in range(i + 1, 4)
        )
        product = 1
        for i in range(4):
            product *= matrix[i][permutation[i]]
        answer += (-1 if inversions % 2 else 1) * product
    return answer


def face_types(edges: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    a, b, c, d, e, f = edges
    return (
        tuple(sorted((a, b, d))),
        tuple(sorted((a, c, e))),
        tuple(sorted((b, c, f))),
        tuple(sorted((d, e, f))),
    )


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    source_path = (
        root / "certificates" / "centered_quarter_bv_pseudodistribution.json"
    )
    output_path = (
        root / "certificates" / "centered_quarter_k4_extension.json"
    )
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    nodes = tuple(Q(value) for value in source["grid"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    nu = tuple(Q(value) for value in source["nu"])
    scaled_nodes = tuple(int(4 * node) for node in nodes)

    representatives: dict[tuple[int, ...], tuple[int, ...]] = {}
    determinant_by_feature: dict[tuple[int, ...], int] = {}
    feasible_labeled_count = 0
    for edges in itertools.product(range(len(nodes)), repeat=6):
        faces = face_types(edges)
        if any(face not in triple_index for face in faces):
            continue
        matrix = [[4 if i == j else 0 for j in range(4)] for i in range(4)]
        for color, (i, j) in zip(edges, EDGE_POSITIONS):
            matrix[i][j] = scaled_nodes[color]
            matrix[j][i] = scaled_nodes[color]
        determinant = determinant_4(matrix)
        if determinant < 0:
            continue
        feasible_labeled_count += 1
        feature = tuple(sorted(triple_index[face] for face in faces))
        representatives.setdefault(feature, edges)
        determinant_by_feature.setdefault(feature, determinant)

    features = tuple(representatives)
    row_count = 1 + len(triples)
    matrix = np.zeros((row_count, len(features)))
    matrix[0, :] = 1
    for column, feature in enumerate(features):
        for index in feature:
            matrix[1 + index, column] += 1
    target_float = np.array([1.0] + [float(value / 390) for value in nu])
    result = linprog(
        np.zeros(len(features)),
        A_eq=matrix,
        b_eq=target_float,
        bounds=(0, None),
        method="highs",
    )
    assert result.success
    active_columns = tuple(
        int(index) for index in np.flatnonzero(result.x > 10**-9)
    )
    assert len(active_columns) == len(triples)
    active_matrix = matrix[:, list(active_columns)]
    assert np.linalg.matrix_rank(active_matrix) == len(active_columns)

    _q, _r, row_permutation = qr(
        active_matrix.T, mode="economic", pivoting=True
    )
    independent_rows = tuple(
        int(index) for index in row_permutation[: len(active_columns)]
    )
    exact_matrix = [
        [
            Q(int(matrix[row, column]))
            for column in active_columns
        ]
        for row in independent_rows
    ]
    exact_target_all = [Q(1)] + [value / 390 for value in nu]
    exact_target = [exact_target_all[row] for row in independent_rows]
    weights = solve_square(exact_matrix, exact_target)
    assert all(weight > 0 for weight in weights)
    assert all(
        sum(
            Q(int(matrix[row, column])) * weight
            for column, weight in zip(active_columns, weights)
        )
        == exact_target_all[row]
        for row in range(row_count)
    )

    atoms = []
    for column, weight in zip(active_columns, weights):
        feature = features[column]
        edges = representatives[feature]
        atoms.append(
            {
                "edge_color_indices_01_02_03_12_13_23": list(edges),
                "face_triple_orbit_indices": list(feature),
                "scaled_gram_determinant_numerator_over_4_pow_4": (
                    determinant_by_feature[feature]
                ),
                "weight": qstr(weight),
            }
        )
    certificate = {
        "schema": "kissing5.centered_quarter_k4_extension.v1",
        "status": (
            "exact symmetric local Gram-PSD K4 extension; not a code and "
            "not a four-point Lasserre certificate"
        ),
        "source_certificate": source_path.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "edge_order": ["01", "02", "03", "12", "13", "23"],
        "normalization": (
            "atom weights sum to 1; expected count of each triangle face "
            "type is nu/390, so the uniform face marginal is nu/1560"
        ),
        "feasible_labeled_k4_count": feasible_labeled_count,
        "distinct_face_count_vectors": len(features),
        "positive_atom_count": len(atoms),
        "atoms": atoms,
    }
    output_path.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    )
    print(output_path)
    print(hashlib.sha256(output_path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
