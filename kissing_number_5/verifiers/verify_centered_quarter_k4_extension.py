#!/usr/bin/env python3
"""Verify the exact local Gram-PSD K4 extension of the centered witness."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


EDGE_POSITIONS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PERMUTATIONS = {
    size: tuple(itertools.permutations(range(size))) for size in range(1, 5)
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


def face_types(edges: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    a, b, c, d, e, f = edges
    return (
        tuple(sorted((a, b, d))),
        tuple(sorted((a, c, e))),
        tuple(sorted((b, c, f))),
        tuple(sorted((d, e, f))),
    )


def scaled_gram(edges: tuple[int, ...], values: list[int]) -> list[list[int]]:
    matrix = [[4 if i == j else 0 for j in range(4)] for i in range(4)]
    for color, (i, j) in zip(edges, EDGE_POSITIONS):
        matrix[i][j] = values[color]
        matrix[j][i] = values[color]
    return matrix


def gram_psd(matrix: list[list[int]]) -> bool:
    for size in range(1, 5):
        for indices in itertools.combinations(range(4), size):
            principal = [
                [matrix[i][j] for j in indices] for i in indices
            ]
            if determinant(principal) < 0:
                return False
    return True


def verify(source_path: Path, extension_path: Path) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    extension = json.loads(extension_path.read_text())
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert extension["schema"] == (
        "kissing5.centered_quarter_k4_extension.v1"
    )
    assert extension["source_certificate"] == source_path.name
    assert extension["source_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()

    grid = [Q(value) for value in source["grid"]]
    scaled_values = [int(4 * value) for value in grid]
    assert all(Q(value, 4) == node for value, node in zip(scaled_values, grid))
    triples = [tuple(item) for item in source["triple_orbits"]]
    triple_index = {triple: index for index, triple in enumerate(triples)}
    alpha = [Q(value) for value in source["alpha"]]
    nu = [Q(value) for value in source["nu"]]
    assert len(triples) == 51

    feasible_labeled = 0
    face_vectors: set[tuple[int, ...]] = set()
    for edges in itertools.product(range(len(grid)), repeat=6):
        faces = face_types(edges)
        if any(face not in triple_index for face in faces):
            continue
        matrix = scaled_gram(edges, scaled_values)
        if not gram_psd(matrix):
            continue
        feasible_labeled += 1
        face_vectors.add(
            tuple(sorted(triple_index[face] for face in faces))
        )
    assert feasible_labeled == extension["feasible_labeled_k4_count"]
    assert len(face_vectors) == extension["distinct_face_count_vectors"]
    assert feasible_labeled == 25808
    assert len(face_vectors) == 1375

    atoms = extension["atoms"]
    assert len(atoms) == extension["positive_atom_count"] == 51
    weights = [Q(atom["weight"]) for atom in atoms]
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    face_marginal = [Q(0)] * len(triples)
    edge_marginal = [Q(0)] * len(grid)
    minimum_determinant: int | None = None
    for atom, weight in zip(atoms, weights):
        edges = tuple(atom["edge_color_indices_01_02_03_12_13_23"])
        assert len(edges) == 6
        assert all(0 <= color < len(grid) for color in edges)
        faces = face_types(edges)
        assert all(face in triple_index for face in faces)
        feature = tuple(sorted(triple_index[face] for face in faces))
        assert feature == tuple(atom["face_triple_orbit_indices"])
        assert feature in face_vectors

        matrix = scaled_gram(edges, scaled_values)
        assert gram_psd(matrix)
        full_determinant = determinant(matrix)
        assert full_determinant == atom[
            "scaled_gram_determinant_numerator_over_4_pow_4"
        ]
        assert full_determinant >= 0
        minimum_determinant = (
            full_determinant
            if minimum_determinant is None
            else min(minimum_determinant, full_determinant)
        )
        for index in feature:
            face_marginal[index] += weight
        for color in edges:
            edge_marginal[color] += weight

    assert all(
        observed == target / 390
        for observed, target in zip(face_marginal, nu)
    )
    assert all(
        observed == Q(3, 20) * target
        for observed, target in zip(edge_marginal, alpha)
    )
    assert minimum_determinant == 0

    return {
        "status": "PASS",
        "scope": (
            "symmetric local Gram-PSD K4 extension; not a code and not "
            "a four-point Lasserre PSD certificate"
        ),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "feasible_labeled_k4_patterns": feasible_labeled,
        "distinct_face_count_vectors": len(face_vectors),
        "positive_extension_atoms": len(atoms),
        "minimum_scaled_gram_determinant": minimum_determinant,
        "triangle_face_marginal": "exact",
        "pair_edge_marginal": "exact",
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    report = verify(
        root / "certificates" / "centered_quarter_bv_pseudodistribution.json",
        root / "certificates" / "centered_quarter_k4_extension.json",
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
