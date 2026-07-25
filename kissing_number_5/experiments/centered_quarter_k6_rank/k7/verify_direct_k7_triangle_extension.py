#!/usr/bin/env python3
"""Exact verifier for the direct rank-five K7 triangle-marginal mixture."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATH = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
K6_PATH = HERE.parent / "direct_k6_triangle_extension.json"
CERTIFICATE_PATH = HERE / "direct_k7_triangle_extension.json"
PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}
PERMUTATIONS = {
    size: tuple(itertools.permutations(range(size))) for size in range(1, 8)
}


def determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    size = len(matrix)
    total = 0
    for permutation in PERMUTATIONS[size]:
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        product = 1
        for i in range(size):
            product *= matrix[i][permutation[i]]
        total += (-1 if inversions % 2 else 1) * product
    return total


def gram(
    edges: tuple[int, ...], scaled_values: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    matrix = [[4 if i == j else 0 for j in range(7)] for i in range(7)]
    for (i, j), color in zip(PAIRS7, edges, strict=True):
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
            for indices in itertools.combinations(range(7), size)
        ]
        for size in range(1, 8)
    }


def triangle_feature(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    result = []
    for i, j, k in itertools.combinations(range(7), 3):
        colors = tuple(
            sorted(
                (
                    edges[PAIR_INDEX7[(i, j)]],
                    edges[PAIR_INDEX7[(i, k)]],
                    edges[PAIR_INDEX7[(j, k)]],
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
        "kissing5.centered_quarter_direct_k7_triangle_extension.v1"
    )
    assert certificate["source_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["source_sha256"] == (
        "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
    )
    assert certificate["generation_k6_sha256"] == hashlib.sha256(
        K6_PATH.read_bytes()
    ).hexdigest()
    assert certificate["generation_k6_sha256"] == (
        "32e629ab5df91cf6e616aa1f7a61af22f853b78ccff50947738b5cab1394d0ba"
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
    minimum_principal = {size: None for size in range(1, 8)}
    minimum_positive_fifth = None
    distinct_features = set()
    for atom, weight in zip(atoms, weights, strict=True):
        edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_05_06_12_13_14_15_16_23_24_25_26_34_35_36_45_46_56"
            ]
        )
        assert len(edges) == 21
        assert all(0 <= color < 7 for color in edges)
        matrix = gram(edges, scaled_values)
        minors = principal_determinants(matrix)
        assert all(value >= 0 for values in minors.values() for value in values)
        assert all(value == 0 for value in minors[6])
        assert minors[7] == [0]
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
        assert len(feature) == 35
        distinct_features.add(feature)
        for index in feature:
            triangle_counts[index] += weight
        for color in edges:
            edge_counts[color] += weight

    assert len(distinct_features) == 51
    nu = [Q(value) for value in source["nu"]]
    alpha = [Q(value) for value in source["alpha"]]
    assert all(
        observed == Q(7) * target / 312
        for observed, target in zip(triangle_counts, nu, strict=True)
    )
    assert all(
        observed == Q(21) * target / 40
        for observed, target in zip(edge_counts, alpha, strict=True)
    )

    return {
        "status": "PASS",
        "scope": (
            "symmetric local rank-five Gram-PSD K7 triangle marginal; "
            "not a code"
        ),
        "positive_atoms": len(atoms),
        "distinct_triangle_count_vectors": len(distinct_features),
        "uniform_triangle_face_marginal": "exact nu/1560",
        "uniform_pair_edge_marginal": "exact alpha/40",
        "minimum_scaled_principal_determinants": minimum_principal,
        "minimum_positive_scaled_fifth_minor": minimum_positive_fifth,
        "all_sixth_and_seventh_order_principal_determinants": 0,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
