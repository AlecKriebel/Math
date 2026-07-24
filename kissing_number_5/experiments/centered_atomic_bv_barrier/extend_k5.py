#!/usr/bin/env python3
"""Find and exactly reconstruct a local Gram-PSD K5 extension.

``enumerate_k5.cpp`` writes one representative for every triangle-count
vector attained by a quarter-grid K5 Gram matrix.  This discovery script
solves the resulting marginal LP, selects a sparse floating solution, and
then reconstructs its weights with exact rational Gaussian elimination.
The certificate is checked by a separate standard-library verifier.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
from scipy.sparse import csc_matrix

from rationalize import qstr, solve_square


EDGE_POSITIONS = (
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


def triangle_types(edges: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    edge = {
        pair: color for pair, color in zip(EDGE_POSITIONS, edges)
    }
    return tuple(
        tuple(sorted((edge[(i, j)], edge[(i, k)], edge[(j, k)])))
        for i in range(5)
        for j in range(i + 1, 5)
        for k in range(j + 1, 5)
    )


def parse_enumeration(
    path: Path,
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]], str]:
    lines = path.read_text().splitlines()
    assert lines
    header = lines[0]
    assert header == (
        "# feasible_labeled_k5=12087822 "
        "distinct_triangle_count_vectors=105930"
    )
    representatives: list[tuple[int, ...]] = []
    features: list[tuple[int, ...]] = []
    for line in lines[1:]:
        fields = line.split(",")
        assert len(fields) == 11
        stored_key = int(fields[0])
        edges = tuple(map(int, fields[1:]))
        assert len(edges) == 10
        assert all(0 <= color < 7 for color in edges)
        feature = tuple(
            sorted(triple_index[face] for face in triangle_types(edges))
        )
        reconstructed_key = 0
        for index in feature:
            reconstructed_key = (reconstructed_key << 6) | index
        assert reconstructed_key == stored_key
        representatives.append(edges)
        features.append(feature)
    assert len(features) == 105930
    assert len(set(features)) == len(features)
    return representatives, features, header


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: extend_k5.py ENUMERATION.csv")
    enumeration_path = Path(sys.argv[1]).resolve()
    root = Path(__file__).resolve().parents[2]
    source_path = (
        root / "certificates" / "centered_quarter_bv_pseudodistribution.json"
    )
    output_path = (
        root / "certificates" / "centered_quarter_k5_extension.json"
    )
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    nu = tuple(Q(value) for value in source["nu"])

    representatives, features, header = parse_enumeration(
        enumeration_path, triple_index
    )
    row_indices: list[int] = []
    column_indices: list[int] = []
    coefficients: list[float] = []
    for column, feature in enumerate(features):
        row_indices.append(0)
        column_indices.append(column)
        coefficients.append(1.0)
        counts = [0] * len(triples)
        for index in feature:
            counts[index] += 1
        for index, count in enumerate(counts):
            if count:
                row_indices.append(1 + index)
                column_indices.append(column)
                coefficients.append(float(count))
    matrix = csc_matrix(
        (coefficients, (row_indices, column_indices)),
        shape=(1 + len(triples), len(features)),
    )
    target = np.array([1.0] + [float(value / 156) for value in nu])
    result = linprog(
        np.zeros(len(features)),
        A_eq=matrix,
        b_eq=target,
        bounds=(0, None),
        method="highs",
    )
    assert result.success, result.message
    active_columns = tuple(
        int(index) for index in np.flatnonzero(result.x > 10**-9)
    )
    assert len(active_columns) == len(triples)

    active_matrix = matrix[:, list(active_columns)].toarray()
    assert np.linalg.matrix_rank(active_matrix) == len(active_columns)
    _q, _r, row_permutation = qr(
        active_matrix.T, mode="economic", pivoting=True
    )
    independent_rows = tuple(
        int(index) for index in row_permutation[: len(active_columns)]
    )
    exact_target_all = [Q(1)] + [value / 156 for value in nu]
    exact_matrix = [
        [
            Q(int(active_matrix[row, local_column]))
            for local_column in range(len(active_columns))
        ]
        for row in independent_rows
    ]
    exact_target = [exact_target_all[row] for row in independent_rows]
    weights = solve_square(exact_matrix, exact_target)
    assert all(weight > 0 for weight in weights)

    exact_columns: list[list[int]] = []
    for column in active_columns:
        counts = [0] * len(triples)
        for index in features[column]:
            counts[index] += 1
        exact_columns.append([1] + counts)
    assert all(
        sum(
            column[row] * weight
            for column, weight in zip(exact_columns, weights)
        )
        == exact_target_all[row]
        for row in range(1 + len(triples))
    )

    atoms = [
        {
            "edge_color_indices_01_02_03_04_12_13_14_23_24_34": list(
                representatives[column]
            ),
            "triangle_orbit_indices": list(features[column]),
            "weight": qstr(weight),
        }
        for column, weight in zip(active_columns, weights)
    ]
    enumeration_bytes = enumeration_path.read_bytes()
    certificate = {
        "schema": "kissing5.centered_quarter_k5_extension.v1",
        "status": (
            "exact symmetric local Gram-PSD K5 extension; not a code and "
            "not a five-point Lasserre certificate"
        ),
        "source_certificate": source_path.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "discovery_enumeration_header": header,
        "discovery_enumeration_sha256": hashlib.sha256(
            enumeration_bytes
        ).hexdigest(),
        "edge_order": [
            "01",
            "02",
            "03",
            "04",
            "12",
            "13",
            "14",
            "23",
            "24",
            "34",
        ],
        "normalization": (
            "atom weights sum to 1; expected count of each triangle type "
            "among the ten faces is nu/156, so the uniform face marginal "
            "is nu/1560"
        ),
        "feasible_labeled_k5_count_in_discovery": 12087822,
        "distinct_triangle_count_vectors_in_discovery": 105930,
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
