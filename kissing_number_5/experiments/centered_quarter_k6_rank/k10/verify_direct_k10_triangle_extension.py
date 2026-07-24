#!/usr/bin/env python3
"""Exact verifier for the direct rank-five K10 triangle-marginal mixture."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATH = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
K9_PATH = HERE.parent / "k9" / "direct_k9_triangle_extension.json"
CERTIFICATE_PATH = HERE / "direct_k10_triangle_extension.json"
PAIRS10 = tuple(itertools.combinations(range(10), 2))
PAIR_INDEX10 = {pair: index for index, pair in enumerate(PAIRS10)}
EDGE_KEY = (
    "edge_color_indices_01_02_03_04_05_06_07_08_09_12_13_14_15_16_"
    "17_18_19_23_24_25_26_27_28_29_34_35_36_37_38_39_45_46_47_"
    "48_49_56_57_58_59_67_68_69_78_79_89"
)


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
    matrix = [[4 if i == j else 0 for j in range(10)] for i in range(10)]
    for (i, j), color in zip(PAIRS10, edges, strict=True):
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
            for indices in itertools.combinations(range(10), size)
        ]
        for size in range(1, 11)
    }


def triangle_feature(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    result = []
    for i, j, k in itertools.combinations(range(10), 3):
        colors = tuple(
            sorted(
                (
                    edges[PAIR_INDEX10[(i, j)]],
                    edges[PAIR_INDEX10[(i, k)]],
                    edges[PAIR_INDEX10[(j, k)]],
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
        "kissing5.centered_quarter_direct_k10_triangle_extension.v1"
    )
    assert certificate["source_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["source_sha256"] == (
        "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
    )
    assert certificate["generation_k9_sha256"] == hashlib.sha256(
        K9_PATH.read_bytes()
    ).hexdigest()
    assert certificate["generation_k9_sha256"] == (
        "b0ead73d99ea050a002a36bfd78f549348d37d19244c147228bee26ad692b148"
    )
    assert certificate["grid"] == source["grid"]

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
    minimum_principal = {size: None for size in range(1, 11)}
    minimum_positive_fifth = None
    distinct_features = set()
    for atom, weight in zip(atoms, weights, strict=True):
        edges = tuple(atom[EDGE_KEY])
        assert len(edges) == 45
        assert all(0 <= color < 7 for color in edges)
        matrix = gram(edges, scaled_values)
        minors = principal_determinants(matrix)
        assert all(value >= 0 for values in minors.values() for value in values)
        assert all(
            value == 0
            for size in (6, 7, 8, 9, 10)
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
        assert len(feature) == 120
        distinct_features.add(feature)
        for index in feature:
            triangle_counts[index] += weight
        for color in edges:
            edge_counts[color] += weight

    assert len(distinct_features) == 51
    nu = [Q(value) for value in source["nu"]]
    alpha = [Q(value) for value in source["alpha"]]
    assert all(
        observed == target / 13
        for observed, target in zip(triangle_counts, nu, strict=True)
    )
    assert all(
        observed == Q(9) * target / 8
        for observed, target in zip(edge_counts, alpha, strict=True)
    )

    return {
        "status": "PASS",
        "scope": (
            "symmetric local rank-five Gram-PSD K10 triangle marginal; "
            "not a code"
        ),
        "positive_atoms": len(atoms),
        "distinct_triangle_count_vectors": len(distinct_features),
        "uniform_triangle_face_marginal": "exact nu/1560",
        "uniform_pair_edge_marginal": "exact alpha/40",
        "minimum_scaled_principal_determinants": minimum_principal,
        "minimum_positive_scaled_fifth_minor": minimum_positive_fifth,
        "all_sixth_through_tenth_order_principal_determinants": 0,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
