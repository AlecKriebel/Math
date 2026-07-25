#!/usr/bin/env python3
"""Generate exact clique/coloring certificates for all 51 K11 atoms.

The output is proof data, but this generator is discovery code.  The
standalone verifier independently regenerates every geometric candidate and
checks both the clique and coloring certificates.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = HERE.parent / "direct_k11_triangle_extension.json"
VALUES = (-4, -3, -2, -1, 0, 1, 2)
VALUE_SET = frozenset(VALUES)
PAIRS11 = tuple(itertools.combinations(range(11), 2))
EDGE_KEY = "edge_color_indices_lexicographic_pairs_0_to_10"
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
        answer += -product if inversions % 2 else product
    return answer


def adjugate(matrix: list[list[int]]) -> list[list[int]]:
    size = len(matrix)
    return [
        [
            (-1 if (row + column) % 2 else 1)
            * determinant(
                [
                    [
                        matrix[i][j]
                        for j in range(size)
                        if j != row
                    ]
                    for i in range(size)
                    if i != column
                ]
            )
            for column in range(size)
        ]
        for row in range(size)
    ]


def matrix_data(
    edges: tuple[int, ...],
) -> tuple[list[list[int]], int, list[list[int]]]:
    gram = [[4 if i == j else 0 for j in range(11)] for i in range(11)]
    for (first, second), color in zip(PAIRS11, edges, strict=True):
        gram[first][second] = gram[second][first] = VALUES[color]
    base = [row[:5] for row in gram[:5]]
    determinant_base = determinant(base)
    if determinant_base <= 0:
        raise RuntimeError("the first five vertices are not a basis")
    return gram, determinant_base, adjugate(base)


def candidates(
    gram: list[list[int]],
    determinant_base: int,
    adj: list[list[int]],
) -> list[tuple[int, ...]]:
    result = []
    for row in itertools.product(VALUES, repeat=5):
        norm_numerator = sum(
            row[i] * adj[i][j] * row[j]
            for i in range(5)
            for j in range(5)
        )
        if norm_numerator != 4 * determinant_base:
            continue
        for vertex in range(5, 11):
            numerator = sum(
                gram[vertex][i] * adj[i][j] * row[j]
                for i in range(5)
                for j in range(5)
            )
            if (
                numerator % determinant_base
                or numerator // determinant_base not in VALUE_SET
            ):
                break
        else:
            result.append(row)
    return result


def compatibility_graph(
    rows: list[tuple[int, ...]],
    determinant_base: int,
    adj: list[list[int]],
) -> list[int]:
    neighbors = [0] * len(rows)
    for first, row in enumerate(rows):
        for second in range(first):
            other = rows[second]
            numerator = sum(
                row[i] * adj[i][j] * other[j]
                for i in range(5)
                for j in range(5)
            )
            if (
                numerator % determinant_base == 0
                and numerator // determinant_base in VALUE_SET
            ):
                neighbors[first] |= 1 << second
                neighbors[second] |= 1 << first
    return neighbors


def greedy_color_order(
    vertices: int,
    neighbors: list[int],
) -> tuple[list[int], list[int]]:
    order = []
    bounds = []
    color = 0
    remaining = vertices
    while remaining:
        color += 1
        available = remaining
        while available:
            bit = available & -available
            vertex = bit.bit_length() - 1
            order.append(vertex)
            bounds.append(color)
            remaining ^= bit
            available ^= bit
            available &= ~neighbors[vertex]
    return order, bounds


def maximum_clique(neighbors: list[int]) -> list[int]:
    best: list[int] = []

    def expand(vertices: int, chosen: list[int]) -> None:
        nonlocal best
        if not vertices:
            if len(chosen) > len(best):
                best = chosen[:]
            return
        order, bounds = greedy_color_order(vertices, neighbors)
        for index in range(len(order) - 1, -1, -1):
            if len(chosen) + bounds[index] <= len(best):
                return
            vertex = order[index]
            bit = 1 << vertex
            if vertices & bit:
                expand(vertices & neighbors[vertex], chosen + [vertex])
                vertices ^= bit

    expand((1 << len(neighbors)) - 1, [])
    return sorted(best)


def dsatur_coloring(
    neighbors: list[int],
    seed: int | None,
) -> list[int]:
    randomizer = random.Random(seed)
    neighbor_sets = [
        {index for index in range(len(neighbors)) if row >> index & 1}
        for row in neighbors
    ]
    colors = [-1] * len(neighbors)
    saturation = [set() for _ in neighbors]
    for _step in neighbors:
        score = max(
            (len(saturation[vertex]), len(neighbor_sets[vertex]))
            for vertex in range(len(neighbors))
            if colors[vertex] < 0
        )
        choices = [
            vertex
            for vertex in range(len(neighbors))
            if colors[vertex] < 0
            and (len(saturation[vertex]), len(neighbor_sets[vertex])) == score
        ]
        vertex = min(choices) if seed is None else randomizer.choice(choices)
        color = 0
        while color in saturation[vertex]:
            color += 1
        colors[vertex] = color
        for other in neighbor_sets[vertex]:
            if colors[other] < 0:
                saturation[other].add(color)
    return colors


def optimal_coloring(neighbors: list[int], target: int) -> list[int]:
    for seed in [None, *range(1000)]:
        colors = dsatur_coloring(neighbors, seed)
        if max(colors) + 1 == target:
            return colors
    raise RuntimeError(f"failed to find the certified {target}-coloring")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text())
    entries = []
    for atom_index, atom in enumerate(source["atoms"]):
        edges = tuple(atom[EDGE_KEY])
        gram, determinant_base, adj = matrix_data(edges)
        rows = candidates(gram, determinant_base, adj)
        neighbors = compatibility_graph(rows, determinant_base, adj)
        clique = maximum_clique(neighbors)
        colors = optimal_coloring(neighbors, len(clique))
        entries.append(
            {
                "atom_index": atom_index,
                "basis_vertex_indices": [0, 1, 2, 3, 4],
                "basis_determinant": determinant_base,
                "candidate_count": len(rows),
                "maximum_additional_points": len(clique),
                "maximum_total_points": 11 + len(clique),
                "clique_candidate_indices": clique,
                "candidate_colors": colors,
            }
        )
        print(
            atom_index,
            len(rows),
            len(clique),
            11 + len(clique),
            flush=True,
        )
    totals = [entry["maximum_total_points"] for entry in entries]
    certificate = {
        "schema": "kissing5.k11_quarter_grid_maximal_extensions.v1",
        "status": (
            "exact candidate-completeness plus clique/coloring certificates "
            "for the 51 selected K11 atoms"
        ),
        "source_certificate": str(SOURCE.relative_to(ROOT)),
        "source_sha256": (
            "f02f52aed4d843434ef6b16c31d03e6176f0566d0a9fa12d02b50b0ec0aee54a"
        ),
        "grid_scaled_by_four": list(VALUES),
        "candidate_definition": (
            "all unit vectors whose correlations with every one of the "
            "eleven source vertices lie in the seven-value quarter grid"
        ),
        "entries": entries,
        "minimum_maximum_total_points": min(totals),
        "maximum_maximum_total_points": max(totals),
        "atoms_reaching_40": [
            entry["atom_index"]
            for entry in entries
            if entry["maximum_total_points"] == 40
        ],
        "scope_warning": (
            "This excludes a quarter-grid K41 extension containing one of "
            "the 51 selected K11 atoms. It does not classify all K11 atoms "
            "or exclude spherical codes with non-grid inner products."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()
