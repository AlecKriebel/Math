#!/usr/bin/env python3
"""Enumerate rank-five K7 extensions of the 51 explicit K6 atoms.

Discovery only.  The search may change the K6 marginal: the K6 atoms are
used merely as positive-definite five-vector bases for generating exact K7
Gram patterns.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATH = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
K6_PATH = HERE.parent / "direct_k6_triangle_extension.json"
VALUES = (-4, -3, -2, -1, 0, 1, 2)
VALUE_INDEX = {value: index for index, value in enumerate(VALUES)}
PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}
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
            # adj[row,column] is cofactor[column,row].
            minor = [
                [
                    matrix[i][j]
                    for j in range(size)
                    if j != row
                ]
                for i in range(size)
                if i != column
            ]
            answer[row][column] = (
                (-1 if (row + column) % 2 else 1) * determinant(minor)
            )
    return answer


def scaled_gram6(edges: tuple[int, ...]) -> list[list[int]]:
    matrix = [[4 if i == j else 0 for j in range(6)] for i in range(6)]
    for (i, j), color in zip(PAIRS6, edges, strict=True):
        matrix[i][j] = VALUES[color]
        matrix[j][i] = VALUES[color]
    return matrix


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = json.loads(SOURCE_PATH.read_text())
    k6 = json.loads(K6_PATH.read_text())
    triple_index = {
        tuple(triple): index
        for index, triple in enumerate(source["triple_orbits"])
    }
    features: dict[tuple[int, ...], tuple[int, ...]] = {}
    candidate_count = 0

    for atom_index, atom in enumerate(k6["atoms"]):
        base_edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        gram = scaled_gram6(base_edges)
        choice = None
        for omitted in range(6):
            indices = [index for index in range(6) if index != omitted]
            base = [[gram[i][j] for j in indices] for i in indices]
            base_determinant = determinant(base)
            if base_determinant > 0:
                choice = omitted, indices, base, base_determinant
                break
        assert choice is not None
        omitted, indices, base, base_determinant = choice
        adj = adjugate(base)
        omitted_correlations = [gram[index][omitted] for index in indices]

        for color_vector in itertools.product(range(7), repeat=5):
            values = [VALUES[color] for color in color_vector]
            squared_norm_numerator = sum(
                values[i] * adj[i][j] * values[j]
                for i in range(5)
                for j in range(5)
            )
            if squared_norm_numerator != 4 * base_determinant:
                continue
            omitted_numerator = sum(
                omitted_correlations[i] * adj[i][j] * values[j]
                for i in range(5)
                for j in range(5)
            )
            if omitted_numerator % base_determinant:
                continue
            omitted_value = omitted_numerator // base_determinant
            if omitted_value not in VALUE_INDEX:
                continue

            new_colors = [None] * 6
            for index, color in zip(indices, color_vector, strict=True):
                new_colors[index] = color
            new_colors[omitted] = VALUE_INDEX[omitted_value]
            edges = [0] * 21
            for pair, color in zip(PAIRS6, base_edges, strict=True):
                edges[PAIR_INDEX7[pair]] = color
            for index, color in enumerate(new_colors):
                assert color is not None
                edges[PAIR_INDEX7[(index, 6)]] = color
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
            "# source_k6_atoms=51 "
            f"rank_five_labeled={candidate_count} "
            f"distinct_triangle_count_vectors={len(features)}\n"
        )
        for feature, edges in sorted(features.items()):
            handle.write(",".join(map(str, (*edges, *feature))) + "\n")


if __name__ == "__main__":
    main()
