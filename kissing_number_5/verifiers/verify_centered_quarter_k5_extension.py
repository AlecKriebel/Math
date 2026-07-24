#!/usr/bin/env python3
"""Verify the exact local Gram-PSD K5 extension of the centered witness."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


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
PERMUTATIONS = {
    size: tuple(itertools.permutations(range(size))) for size in range(1, 6)
}


def determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    answer = 0
    for permutation in PERMUTATIONS[size]:
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        product = 1
        for i in range(size):
            product *= matrix[i][permutation[i]]
        answer += (-1 if inversions % 2 else 1) * product
    return answer


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


def scaled_gram(edges: tuple[int, ...], values: list[int]) -> list[list[int]]:
    matrix = [[4 if i == j else 0 for j in range(5)] for i in range(5)]
    for color, (i, j) in zip(edges, EDGE_POSITIONS):
        matrix[i][j] = values[color]
        matrix[j][i] = values[color]
    return matrix


def gram_psd(matrix: list[list[int]]) -> tuple[bool, dict[int, int]]:
    minima: dict[int, int] = {}
    for size in range(1, 6):
        determinants = []
        for indices in itertools.combinations(range(5), size):
            principal = [
                [matrix[i][j] for j in indices] for i in indices
            ]
            determinants.append(determinant(principal))
        minima[size] = min(determinants)
        if minima[size] < 0:
            return False, minima
    return True, minima


def verify(
    source_path: Path,
    extension_path: Path,
    enumeration_path: Path | None = None,
) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    extension = json.loads(extension_path.read_text())
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert extension["schema"] == (
        "kissing5.centered_quarter_k5_extension.v1"
    )
    assert extension["status"] == (
        "exact symmetric local Gram-PSD K5 extension; not a code and "
        "not a five-point Lasserre certificate"
    )
    assert extension["normalization"] == (
        "atom weights sum to 1; expected count of each triangle type "
        "among the ten faces is nu/156, so the uniform face marginal "
        "is nu/1560"
    )
    assert extension["source_certificate"] == source_path.name
    assert extension["source_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert extension["edge_order"] == [
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
    ]
    assert extension["discovery_enumeration_header"] == (
        "# feasible_labeled_k5=12087822 "
        "distinct_triangle_count_vectors=105930"
    )
    assert extension["feasible_labeled_k5_count_in_discovery"] == 12087822
    assert extension["distinct_triangle_count_vectors_in_discovery"] == 105930
    if enumeration_path is not None:
        enumeration_bytes = enumeration_path.read_bytes()
        assert extension["discovery_enumeration_sha256"] == hashlib.sha256(
            enumeration_bytes
        ).hexdigest()
        assert enumeration_bytes.splitlines()[0].decode() == extension[
            "discovery_enumeration_header"
        ]

    grid = [Q(value) for value in source["grid"]]
    scaled_values = [int(4 * value) for value in grid]
    assert all(Q(value, 4) == node for value, node in zip(scaled_values, grid))
    assert max(grid) == Q(1, 2)
    triples = [tuple(item) for item in source["triple_orbits"]]
    triple_index = {triple: index for index, triple in enumerate(triples)}
    alpha = [Q(value) for value in source["alpha"]]
    nu = [Q(value) for value in source["nu"]]
    assert len(triples) == 51
    assert sum(alpha) == 40
    assert sum(nu) == 1560

    atoms = extension["atoms"]
    assert len(atoms) == extension["positive_atom_count"] == 51
    weights = [Q(atom["weight"]) for atom in atoms]
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    triangle_count_marginal = [Q(0)] * len(triples)
    edge_count_marginal = [Q(0)] * len(grid)
    principal_minima: dict[int, int | None] = {
        size: None for size in range(1, 6)
    }
    for atom, weight in zip(atoms, weights):
        edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_12_13_14_23_24_34"
            ]
        )
        assert len(edges) == 10
        assert all(0 <= color < len(grid) for color in edges)
        faces = triangle_types(edges)
        assert all(face in triple_index for face in faces)
        feature = tuple(sorted(triple_index[face] for face in faces))
        assert feature == tuple(atom["triangle_orbit_indices"])

        matrix = scaled_gram(edges, scaled_values)
        assert all(matrix[index][index] == 4 for index in range(5))
        assert all(
            matrix[i][j] <= 2
            for i in range(5)
            for j in range(i + 1, 5)
        )
        is_psd, minima = gram_psd(matrix)
        assert is_psd
        for size, value in minima.items():
            old = principal_minima[size]
            principal_minima[size] = value if old is None else min(old, value)

        for index in feature:
            triangle_count_marginal[index] += weight
        for color in edges:
            edge_count_marginal[color] += weight

    assert all(
        observed == target / 156
        for observed, target in zip(triangle_count_marginal, nu)
    )
    assert all(
        observed == target / 4
        for observed, target in zip(edge_count_marginal, alpha)
    )
    assert principal_minima == {1: 4, 2: 0, 3: 0, 4: 0, 5: 0}

    return {
        "status": "PASS",
        "scope": (
            "symmetric local Gram-PSD K5 extension; not a code and not "
            "a five-point Lasserre PSD certificate"
        ),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "discovery_enumeration_hash": (
            "checked" if enumeration_path is not None else "not required"
        ),
        "positive_extension_atoms": len(atoms),
        "minimum_scaled_principal_determinants_by_order": principal_minima,
        "uniform_triangle_face_marginal": "exact nu/1560",
        "uniform_pair_edge_marginal": "exact alpha/40",
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    report = verify(
        root / "certificates" / "centered_quarter_bv_pseudodistribution.json",
        root / "certificates" / "centered_quarter_k5_extension.json",
        root
        / "experiments"
        / "centered_atomic_bv_barrier"
        / "results"
        / "k5_triangle_vectors.csv",
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
