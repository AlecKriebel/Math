#!/usr/bin/env python3
"""Standard-library exact verifier for the repaired local K4/K5 extensions."""

from __future__ import annotations

from fractions import Fraction as Q
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
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


def determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    answer = 0
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        product = math.prod(matrix[i][permutation[i]] for i in range(size))
        answer += (-1 if inversions % 2 else 1) * product
    return answer


def gram_is_psd(
    vertex_count: int,
    edge_positions: tuple[tuple[int, int], ...],
    edges: tuple[int, ...],
    scaled_nodes: tuple[int, ...],
) -> bool:
    matrix = [
        [4 if i == j else 0 for j in range(vertex_count)]
        for i in range(vertex_count)
    ]
    for color, (i, j) in zip(edges, edge_positions):
        matrix[i][j] = matrix[j][i] = scaled_nodes[color]
    for size in range(1, vertex_count + 1):
        for subset in itertools.combinations(range(vertex_count), size):
            principal = [[matrix[i][j] for j in subset] for i in subset]
            if determinant(principal) < 0:
                return False
    return True


def triangle_counts(
    vertex_count: int,
    edge_positions: tuple[tuple[int, int], ...],
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> list[int]:
    edge = {pair: color for pair, color in zip(edge_positions, edges)}
    counts = [0] * len(triple_index)
    for i in range(vertex_count):
        for j in range(i + 1, vertex_count):
            for k in range(j + 1, vertex_count):
                face = tuple(
                    sorted((edge[(i, j)], edge[(i, k)], edge[(j, k)]))
                )
                assert face in triple_index
                counts[triple_index[face]] += 1
    return counts


def verify(certificate_path: Path, source_path: Path) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    assert certificate["schema"] == (
        "kissing5.repaired_centered_local_k4_k5_extension.v1"
    )
    assert certificate["source_certificate"] == source_path.name
    assert certificate["source_sha256"] == hashlib.sha256(source_bytes).hexdigest()
    scaled_nodes = tuple(certificate["grid_numerators_over_four"])
    assert scaled_nodes == (-4, -3, -2, -1, 0, 1, 2)
    assert tuple(Q(value) for value in source["grid"]) == tuple(
        Q(value, 4) for value in scaled_nodes
    )
    triples = tuple(tuple(row) for row in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    nu = [Q(value) for value in source["nu"]]

    summaries: dict[str, object] = {}
    specifications = (
        (
            "k4",
            4,
            K4_EDGES,
            "edge_color_indices_01_02_03_12_13_23",
            Q(390),
        ),
        (
            "k5",
            5,
            K5_EDGES,
            "edge_color_indices_01_02_03_04_12_13_14_23_24_34",
            Q(156),
        ),
    )
    for name, vertex_count, edge_positions, edge_key, divisor in specifications:
        section = certificate[name]
        atoms = section["atoms"]
        assert len(atoms) == section["positive_atom_count"] == 51
        weights = [Q(atom["weight"]) for atom in atoms]
        edges = [tuple(atom[edge_key]) for atom in atoms]
        assert all(weight > 0 for weight in weights)
        assert sum(weights) == 1
        assert len(set(edges)) == len(edges)
        assert all(
            len(edge_row) == len(edge_positions)
            and all(0 <= color < 7 for color in edge_row)
            for edge_row in edges
        )
        assert all(
            gram_is_psd(vertex_count, edge_positions, edge_row, scaled_nodes)
            for edge_row in edges
        )
        counts = [
            triangle_counts(
                vertex_count,
                edge_positions,
                edge_row,
                triple_index,
            )
            for edge_row in edges
        ]
        observed = [
            sum(weight * row[index] for weight, row in zip(weights, counts))
            for index in range(len(triples))
        ]
        assert observed == [value / divisor for value in nu]
        summaries[name] = {
            "positive_atoms": len(atoms),
            "minimum_weight": str(min(weights)),
            "all_principal_minors_nonnegative": True,
            "exact_triangle_marginal": True,
        }

    return {
        "status": "PASS",
        "scope": (
            "separate exact local K4/K5 extensions of one repaired witness; "
            "not cross-level consistency and not a global code"
        ),
        **summaries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).resolve().parent / "repaired_local_k4_k5_extension.json",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=(
            ROOT
            / "experiments"
            / "centered_integer_degree_moments"
            / "repaired_pair_triple_local_3.json"
        ),
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate, args.source), indent=2))


if __name__ == "__main__":
    main()
