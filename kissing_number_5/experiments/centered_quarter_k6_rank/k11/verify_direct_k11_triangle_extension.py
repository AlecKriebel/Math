#!/usr/bin/env python3
"""Exact verifier for the direct rank-five K11 triangle-marginal mixture."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATH = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
K10_PATH = HERE.parent / "k10" / "direct_k10_triangle_extension.json"
CERTIFICATE_PATH = HERE / "direct_k11_triangle_extension.json"
PAIRS11 = tuple(itertools.combinations(range(11), 2))
PAIR_INDEX11 = {pair: index for index, pair in enumerate(PAIRS11)}
EDGE_KEY = "edge_color_indices_lexicographic_pairs_0_to_10"


def determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Exact fraction-free Bareiss determinant."""
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    work = [list(row) for row in matrix]
    sign = 1
    previous_pivot = 1
    for column in range(size - 1):
        pivot_row = next(
            (
                row
                for row in range(column, size)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, size):
            for other_column in range(column + 1, size):
                numerator = (
                    work[row][other_column] * pivot
                    - work[row][column] * work[column][other_column]
                )
                assert numerator % previous_pivot == 0
                work[row][other_column] = numerator // previous_pivot
            work[row][column] = 0
        previous_pivot = pivot
    return sign * work[-1][-1]


def gram(
    edges: tuple[int, ...], scaled_values: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    matrix = [[4 if i == j else 0 for j in range(11)] for i in range(11)]
    for (i, j), color in zip(PAIRS11, edges, strict=True):
        matrix[i][j] = scaled_values[color]
        matrix[j][i] = scaled_values[color]
    return tuple(tuple(row) for row in matrix)


def principal_determinants(
    matrix: tuple[tuple[int, ...], ...]
) -> dict[int, list[int]]:
    return {
        size: [
            determinant(
                tuple(
                    tuple(matrix[i][j] for j in indices) for i in indices
                )
            )
            for indices in itertools.combinations(range(11), size)
        ]
        for size in range(1, 12)
    }


def triangle_feature(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    result = []
    for i, j, k in itertools.combinations(range(11), 3):
        colors = tuple(
            sorted(
                (
                    edges[PAIR_INDEX11[(i, j)]],
                    edges[PAIR_INDEX11[(i, k)]],
                    edges[PAIR_INDEX11[(j, k)]],
                )
            )
        )
        result.append(triple_index[colors])
    return tuple(sorted(result))


def verify() -> dict[str, object]:
    source_bytes = SOURCE_PATH.read_bytes()
    source = json.loads(source_bytes)
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    assert certificate["schema"] == (
        "kissing5.centered_quarter_direct_k11_triangle_extension.v1"
    )
    assert certificate["source_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["source_sha256"] == (
        "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
    )
    assert certificate["generation_k10_sha256"] == hashlib.sha256(
        K10_PATH.read_bytes()
    ).hexdigest()
    assert certificate["generation_k10_sha256"] == (
        "542f3061bfe282d98580955e62e756bfd9646890a45747f0baad8b11f750cc28"
    )
    assert certificate["grid"] == source["grid"]
    assert certificate["edge_order"] == (
        "all pairs (i,j) with 0<=i<j<=10 in Python "
        "itertools.combinations(range(11),2) order"
    )

    grid = tuple(Q(value) for value in source["grid"])
    scaled_values = tuple(int(4 * value) for value in grid)
    assert all(Q(value, 4) == node for value, node in zip(scaled_values, grid))
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    assert len(triple_index) == 51

    atoms = certificate["atoms"]
    weights = [Q(atom["weight"]) for atom in atoms]
    assert len(atoms) == certificate["positive_atom_count"] == 51
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    triangle_counts = [Q(0)] * 51
    edge_counts = [Q(0)] * 7
    minimum_principal = {size: None for size in range(1, 12)}
    minimum_positive_fifth = None
    distinct_features = set()
    for atom, weight in zip(atoms, weights, strict=True):
        edges = tuple(atom[EDGE_KEY])
        assert len(edges) == 55
        assert all(0 <= color < 7 for color in edges)
        matrix = gram(edges, scaled_values)
        minors = principal_determinants(matrix)
        assert all(value >= 0 for values in minors.values() for value in values)
        assert all(
            value == 0
            for size in range(6, 12)
            for value in minors[size]
        )
        positive_fifth = [value for value in minors[5] if value > 0]
        assert positive_fifth
        local_positive = min(positive_fifth)
        minimum_positive_fifth = (
            local_positive
            if minimum_positive_fifth is None
            else min(minimum_positive_fifth, local_positive)
        )
        for size, values in minors.items():
            local = min(values)
            old = minimum_principal[size]
            minimum_principal[size] = local if old is None else min(old, local)

        feature = triangle_feature(edges, triple_index)
        assert feature == tuple(atom["triangle_orbit_indices"])
        assert len(feature) == 165
        distinct_features.add(feature)
        for index in feature:
            triangle_counts[index] += weight
        for color in edges:
            edge_counts[color] += weight

    assert len(distinct_features) == 51
    nu = [Q(value) for value in source["nu"]]
    alpha = [Q(value) for value in source["alpha"]]
    assert all(
        observed == Q(11) * target / 104
        for observed, target in zip(triangle_counts, nu, strict=True)
    )
    assert all(
        observed == Q(11) * target / 8
        for observed, target in zip(edge_counts, alpha, strict=True)
    )

    return {
        "status": "PASS",
        "scope": (
            "symmetric local rank-five Gram-PSD K11 triangle marginal; "
            "not a code"
        ),
        "positive_atoms": len(atoms),
        "distinct_triangle_count_vectors": len(distinct_features),
        "uniform_triangle_face_marginal": "exact nu/1560",
        "uniform_pair_edge_marginal": "exact alpha/40",
        "minimum_scaled_principal_determinants": minimum_principal,
        "minimum_positive_scaled_fifth_minor": minimum_positive_fifth,
        "all_sixth_through_eleventh_order_principal_determinants": 0,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
