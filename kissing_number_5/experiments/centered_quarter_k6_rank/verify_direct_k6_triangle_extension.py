#!/usr/bin/env python3
"""Exact standard-library verifier for the direct rank-five K6 extension."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
CERTIFICATE_PATH = Path(__file__).with_name("direct_k6_triangle_extension.json")
PAIRS6 = tuple((i, j) for i in range(6) for j in range(i + 1, 6))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
PERMUTATIONS = {
    size: tuple(itertools.permutations(range(size))) for size in range(1, 7)
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


def gram(edges: tuple[int, ...], values: tuple[int, ...]):
    matrix = [[4 if i == j else 0 for j in range(6)] for i in range(6)]
    for (i, j), color in zip(PAIRS6, edges, strict=True):
        matrix[i][j] = values[color]
        matrix[j][i] = values[color]
    return tuple(tuple(row) for row in matrix)


def principal_determinants(
    matrix: tuple[tuple[int, ...], ...]
) -> dict[int, list[int]]:
    result = {}
    for size in range(1, 7):
        result[size] = [
            determinant(
                tuple(
                    tuple(matrix[i][j] for j in indices) for i in indices
                )
            )
            for indices in itertools.combinations(range(6), size)
        ]
    return result


def triangle_indices(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    result = []
    for i in range(6):
        for j in range(i + 1, 6):
            for k in range(j + 1, 6):
                colors = tuple(
                    sorted(
                        (
                            edges[PAIR_INDEX6[(i, j)]],
                            edges[PAIR_INDEX6[(i, k)]],
                            edges[PAIR_INDEX6[(j, k)]],
                        )
                    )
                )
                result.append(triple_index[colors])
    return tuple(sorted(result))


def verify(
    source_path: Path = SOURCE_PATH,
    certificate_path: Path = CERTIFICATE_PATH,
) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    certificate = json.loads(certificate_path.read_text())
    assert certificate["schema"] == (
        "kissing5.centered_quarter_direct_k6_triangle_extension.v1"
    )
    assert (ROOT / certificate["source_certificate"]).resolve() == (
        source_path.resolve()
    )
    assert certificate["source_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["grid"] == source["grid"]
    grid = tuple(Q(value) for value in source["grid"])
    scaled_values = tuple(int(4 * value) for value in grid)
    assert all(Q(value, 4) == node for value, node in zip(scaled_values, grid))
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    assert len(triples) == len(triple_index) == 51

    atoms = certificate["atoms"]
    assert len(atoms) == certificate["positive_atom_count"] == 51
    weights = [Q(atom["weight"]) for atom in atoms]
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    triangle_counts = [Q(0)] * 51
    edge_counts = [Q(0)] * 7
    minimum_principal = {size: None for size in range(1, 7)}
    minimum_positive_fifth_minor = None
    distinct_features = set()
    for atom, weight in zip(atoms, weights, strict=True):
        edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        assert len(edges) == 15
        assert all(0 <= color < 7 for color in edges)
        matrix = gram(edges, scaled_values)
        minors = principal_determinants(matrix)
        assert all(value >= 0 for values in minors.values() for value in values)
        assert minors[6] == [0]
        positive_fifth = [value for value in minors[5] if value > 0]
        assert positive_fifth
        local_minimum = min(positive_fifth)
        minimum_positive_fifth_minor = (
            local_minimum
            if minimum_positive_fifth_minor is None
            else min(minimum_positive_fifth_minor, local_minimum)
        )
        for size, values in minors.items():
            local = min(values)
            old = minimum_principal[size]
            minimum_principal[size] = local if old is None else min(old, local)

        feature = triangle_indices(edges, triple_index)
        assert feature == tuple(atom["triangle_orbit_indices"])
        assert len(feature) == 20
        distinct_features.add(feature)
        for index in feature:
            triangle_counts[index] += weight
        for color in edges:
            edge_counts[color] += weight

    assert len(distinct_features) == 51
    nu = [Q(value) for value in source["nu"]]
    alpha = [Q(value) for value in source["alpha"]]
    assert all(
        observed == target / 78
        for observed, target in zip(triangle_counts, nu, strict=True)
    )
    assert all(
        observed == 3 * target / 8
        for observed, target in zip(edge_counts, alpha, strict=True)
    )
    assert minimum_principal[6] == 0
    assert minimum_positive_fifth_minor is not None

    return {
        "status": "PASS",
        "scope": (
            "symmetric local rank-five Gram-PSD K6 triangle marginal; "
            "not a code"
        ),
        "positive_atoms": len(atoms),
        "distinct_triangle_count_vectors": len(distinct_features),
        "uniform_triangle_face_marginal": "exact nu/1560",
        "uniform_pair_edge_marginal": "exact alpha/40",
        "minimum_scaled_principal_determinants": minimum_principal,
        "minimum_positive_scaled_fifth_minor": minimum_positive_fifth_minor,
        "all_full_determinants": 0,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE_PATH)
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE_PATH)
    arguments = parser.parse_args()
    print(
        json.dumps(
            verify(arguments.source, arguments.certificate),
            indent=2,
            sort_keys=True,
        )
    )
