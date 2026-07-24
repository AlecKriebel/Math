#!/usr/bin/env python3
"""Enumerate rank-five K8 extensions of the 51 explicit K7 atoms.

Discovery only.  The stored K7 atoms are used as rank-five bases for exact
Schur/range generation; the resulting mixture is allowed to change the K7
marginal.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATH = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
K7_PATH = HERE.parent / "k7" / "direct_k7_triangle_extension.json"
VALUES = (-4, -3, -2, -1, 0, 1, 2)
VALUE_INDEX = {value: index for index, value in enumerate(VALUES)}
PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIRS8 = tuple(itertools.combinations(range(8), 2))
PAIR_INDEX8 = {pair: index for index, pair in enumerate(PAIRS8)}
PERMUTATIONS = {
    size: tuple(itertools.permutations(range(size))) for size in range(1, 6)
}


def determinant(matrix: list[list[int]]) -> int:
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


def adjugate(matrix: list[list[int]]) -> list[list[int]]:
    size = len(matrix)
    answer = [[0] * size for _ in range(size)]
    for row in range(size):
        for column in range(size):
            minor = [
                [matrix[i][j] for j in range(size) if j != row]
                for i in range(size)
                if i != column
            ]
            answer[row][column] = (
                (-1 if (row + column) % 2 else 1) * determinant(minor)
            )
    return answer


def scaled_gram7(edges: tuple[int, ...]) -> list[list[int]]:
    matrix = [[4 if i == j else 0 for j in range(7)] for i in range(7)]
    for (i, j), color in zip(PAIRS7, edges, strict=True):
        matrix[i][j] = VALUES[color]
        matrix[j][i] = VALUES[color]
    return matrix


def triangle_feature(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    result = []
    for i, j, k in itertools.combinations(range(8), 3):
        colors = tuple(
            sorted(
                (
                    edges[PAIR_INDEX8[(i, j)]],
                    edges[PAIR_INDEX8[(i, k)]],
                    edges[PAIR_INDEX8[(j, k)]],
                )
            )
        )
        result.append(triple_index[colors])
    return tuple(sorted(result))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = json.loads(SOURCE_PATH.read_text())
    k7 = json.loads(K7_PATH.read_text())
    triple_index = {
        tuple(triple): index
        for index, triple in enumerate(source["triple_orbits"])
    }
    features: dict[tuple[int, ...], tuple[int, ...]] = {}
    candidate_count = 0

    edge_key = (
        "edge_color_indices_01_02_03_04_05_06_12_13_14_15_16_"
        "23_24_25_26_34_35_36_45_46_56"
    )
    for atom_index, atom in enumerate(k7["atoms"]):
        base_edges = tuple(atom[edge_key])
        gram = scaled_gram7(base_edges)
        choice = None
        for indices in itertools.combinations(range(7), 5):
            base = [[gram[i][j] for j in indices] for i in indices]
            base_determinant = determinant(base)
            if base_determinant > 0:
                omitted = tuple(index for index in range(7) if index not in indices)
                choice = indices, omitted, base, base_determinant
                break
        assert choice is not None
        indices, omitted, base, base_determinant = choice
        adj = adjugate(base)
        omitted_correlations = [
            [gram[index][vertex] for index in indices] for vertex in omitted
        ]

        for color_vector in itertools.product(range(7), repeat=5):
            values = [VALUES[color] for color in color_vector]
            squared_norm_numerator = sum(
                values[i] * adj[i][j] * values[j]
                for i in range(5)
                for j in range(5)
            )
            if squared_norm_numerator != 4 * base_determinant:
                continue
            forced_colors = []
            for correlations in omitted_correlations:
                numerator = sum(
                    correlations[i] * adj[i][j] * values[j]
                    for i in range(5)
                    for j in range(5)
                )
                if numerator % base_determinant:
                    break
                forced_value = numerator // base_determinant
                if forced_value not in VALUE_INDEX:
                    break
                forced_colors.append(VALUE_INDEX[forced_value])
            if len(forced_colors) != len(omitted):
                continue

            new_colors: list[int | None] = [None] * 7
            for index, color in zip(indices, color_vector, strict=True):
                new_colors[index] = color
            for index, color in zip(omitted, forced_colors, strict=True):
                new_colors[index] = color
            edges = [0] * 28
            for pair, color in zip(PAIRS7, base_edges, strict=True):
                edges[PAIR_INDEX8[pair]] = color
            for index, color in enumerate(new_colors):
                assert color is not None
                edges[PAIR_INDEX8[(index, 7)]] = color
            edges_tuple = tuple(edges)
            feature = triangle_feature(edges_tuple, triple_index)
            features.setdefault(feature, edges_tuple)
            candidate_count += 1
        print(
            f"base={atom_index + 1} candidates={candidate_count} "
            f"features={len(features)}",
            flush=True,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(
            "# source_k7_atoms=51 "
            f"rank_five_labeled={candidate_count} "
            f"distinct_triangle_count_vectors={len(features)}\n"
        )
        for feature, edges in sorted(features.items()):
            handle.write(",".join(map(str, (*edges, *feature))) + "\n")


if __name__ == "__main__":
    main()
