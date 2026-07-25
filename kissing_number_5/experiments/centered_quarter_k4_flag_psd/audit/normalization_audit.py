#!/usr/bin/env python3
"""Exact normalization audit for the ordered- and unordered-edge flag blocks.

The audit uses the genuine 40-point D5 spherical code.  All coordinates are
stored as integer vectors whose actual Gram matrix is one half of the integer
dot-product matrix, so every check below is exact over ``Fraction``.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

from experiments.centered_quarter_k4_flag_psd.search import (
    EDGES,
    EDGE_INDEX,
    canonical,
    face_types,
)


def d5_roots() -> tuple[tuple[int, ...], ...]:
    roots = []
    for i, j in itertools.combinations(range(5), 2):
        for first in (-1, 1):
            for second in (-1, 1):
                vector = [0] * 5
                vector[i] = first
                vector[j] = second
                roots.append(tuple(vector))
    assert len(roots) == 40
    return tuple(roots)


def dot(first: tuple[int, ...], second: tuple[int, ...]) -> Q:
    return Q(sum(a * b for a, b in zip(first, second)), 2)


def outer_add(
    target: list[list[Q]], vector: list[Q], scale: Q = Q(1)
) -> None:
    for i, first in enumerate(vector):
        for j, second in enumerate(vector):
            target[i][j] += scale * first * second


def zero_matrix(size: int) -> list[list[Q]]:
    return [[Q(0) for _ in range(size)] for _ in range(size)]


def matrix_equal(
    first: list[list[Q]], second: list[list[Q]]
) -> bool:
    return first == second


def matvec(matrix: list[list[Q]], vector: list[Q]) -> list[Q]:
    return [
        sum((entry * value for entry, value in zip(row, vector)), Q(0))
        for row in matrix
    ]


def profile_coefficients(
    pattern: tuple[int, ...],
    color_count: int,
    categories: tuple[tuple[int, int], ...],
    ordered: bool,
) -> list[list[list[int]]]:
    category_index = {
        category: index for index, category in enumerate(categories)
    }
    blocks = [
        [[0 for _ in categories] for _ in categories]
        for _ in range(color_count)
    ]
    bases = (
        tuple(itertools.permutations(range(4), 2))
        if ordered
        else EDGES
    )
    for i, j in bases:
        base_color = pattern[EDGE_INDEX[tuple(sorted((i, j)))]]
        remaining = [vertex for vertex in range(4) if vertex not in (i, j)]
        profiles = []
        for vertex in remaining:
            profile = (
                pattern[EDGE_INDEX[tuple(sorted((i, vertex)))]],
                pattern[EDGE_INDEX[tuple(sorted((j, vertex)))]],
            )
            if not ordered:
                profile = tuple(sorted(profile))
            profiles.append(category_index[profile])
        first, second = profiles
        blocks[base_color][first][second] += 1
        blocks[base_color][second][first] += 1
    return blocks


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    source = json.loads(
        (root / "certificates/centered_quarter_bv_pseudodistribution.json")
        .read_text()
    )
    grid = tuple(Q(value) for value in source["grid"])
    color_index = {value: index for index, value in enumerate(grid)}
    triple_orbits = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {
        triple: index for index, triple in enumerate(triple_orbits)
    }

    roots = d5_roots()
    size = len(roots)
    assert all(
        sum(root[coordinate] for root in roots) == 0
        for coordinate in range(5)
    )
    colors = [
        [
            None if i == j else color_index[dot(roots[i], roots[j])]
            for j in range(size)
        ]
        for i in range(size)
    ]

    ordered_pair_counts = [0] * len(grid)
    for i in range(size):
        for j in range(size):
            if i != j:
                ordered_pair_counts[colors[i][j]] += 1
    alpha = [Q(count, size) for count in ordered_pair_counts]
    assert sum(alpha) == size - 1
    assert 1 + sum(value * mass for value, mass in zip(grid, alpha)) == 0

    triangle_counts: Counter[tuple[int, int, int]] = Counter()
    for i, j, k in itertools.permutations(range(size), 3):
        orbit = tuple(sorted((colors[i][j], colors[i][k], colors[j][k])))
        triangle_counts[orbit] += 1
    assert set(triangle_counts) <= set(triple_orbits)
    nu = [
        Q(triangle_counts.get(orbit, 0), size)
        for orbit in triple_orbits
    ]
    assert sum(nu) == (size - 1) * (size - 2)

    # Exact pair marginal from the sorted triangle-orbit convention.
    recovered_pair = [Q(0) for _ in grid]
    for triple, mass in zip(triple_orbits, nu):
        for color in triple:
            recovered_pair[color] += mass / 3
    assert recovered_pair == [(size - 2) * mass for mass in alpha]

    four_counts: Counter[tuple[int, ...]] = Counter()
    for subset in itertools.combinations(range(size), 4):
        pattern = tuple(colors[subset[i]][subset[j]] for i, j in EDGES)
        four_counts[canonical(pattern)] += 1
    number_four_sets = Q(size * (size - 1) * (size - 2) * (size - 3), 24)
    k4 = {
        pattern: Q(count, number_four_sets)
        for pattern, count in four_counts.items()
    }
    assert sum(k4.values()) == 1

    # Exact K4 -> K3 face marginal.
    recovered_faces = [Q(0) for _ in triple_orbits]
    for pattern, mass in k4.items():
        for face in face_types(pattern):
            recovered_faces[triple_index[face]] += mass
    face_factor = Q(4, (size - 1) * (size - 2))
    assert recovered_faces == [face_factor * mass for mass in nu]

    audit_results = {}
    for ordered in (False, True):
        categories = tuple(
            itertools.product(range(len(grid)), repeat=2)
            if ordered
            else itertools.combinations_with_replacement(
                range(len(grid)), 2
            )
        )
        category_index = {
            category: index for index, category in enumerate(categories)
        }

        # Direct moment matrices averaged by 1/N.
        direct = [
            zero_matrix(len(categories) + 1) for _ in grid
        ]
        bases = (
            tuple(itertools.permutations(range(size), 2))
            if ordered
            else tuple(itertools.combinations(range(size), 2))
        )
        for i, j in bases:
            q = colors[i][j]
            counts = [Q(0) for _ in categories]
            for k in range(size):
                if k in (i, j):
                    continue
                profile = (colors[i][k], colors[j][k])
                if not ordered:
                    profile = tuple(sorted(profile))
                counts[category_index[profile]] += 1
            outer_add(direct[q], counts + [Q(1)], Q(1, size))

        # First moments reconstructed only from the sorted K3 masses.
        first = [
            [Q(0) for _ in categories] for _ in grid
        ]
        for triple, mass in zip(triple_orbits, nu):
            triangle_edges = {
                (0, 1): triple[0],
                (0, 2): triple[1],
                (1, 2): triple[2],
            }
            if ordered:
                for i, j in itertools.permutations(range(3), 2):
                    k = next(
                        vertex
                        for vertex in range(3)
                        if vertex not in (i, j)
                    )
                    q = triangle_edges[tuple(sorted((i, j)))]
                    profile = (
                        triangle_edges[tuple(sorted((i, k)))],
                        triangle_edges[tuple(sorted((j, k)))],
                    )
                    first[q][category_index[profile]] += mass / 6
            else:
                for position, q in enumerate(triple):
                    profile = tuple(
                        sorted(
                            triple[index]
                            for index in range(3)
                            if index != position
                        )
                    )
                    first[q][category_index[profile]] += mass / 6

        # Distinct-extension second moments reconstructed only from K4.
        distinct = [
            zero_matrix(len(categories)) for _ in grid
        ]
        flag_factor = number_four_sets / size
        for pattern, mass in k4.items():
            blocks = profile_coefficients(
                pattern, len(grid), categories, ordered
            )
            for q in range(len(grid)):
                for row in range(len(categories)):
                    for column in range(len(categories)):
                        distinct[q][row][column] += (
                            flag_factor * mass * blocks[q][row][column]
                        )

        reconstructed = [
            zero_matrix(len(categories) + 1) for _ in grid
        ]
        for q in range(len(grid)):
            bottom = alpha[q] if ordered else alpha[q] / 2
            for row in range(len(categories)):
                reconstructed[q][row][row] += first[q][row]
                for column in range(len(categories)):
                    reconstructed[q][row][column] += distinct[q][row][column]
                reconstructed[q][row][-1] = first[q][row]
                reconstructed[q][-1][row] = first[q][row]
            reconstructed[q][-1][-1] = bottom
            assert matrix_equal(reconstructed[q], direct[q])

            # Every genuine centered code has these three pointwise kernels.
            if ordered:
                kernels = (
                    [Q(1) for _ in categories] + [Q(-(size - 2))],
                    [grid[first_color] for first_color, _ in categories]
                    + [1 + grid[q]],
                    [grid[second_color] for _, second_color in categories]
                    + [1 + grid[q]],
                )
            else:
                # Forgetting the orientation of the base edge also forgets
                # which endpoint supplies which coordinate.  Only the sum of
                # the two endpoint identities remains a pointwise identity.
                kernels = (
                    [Q(1) for _ in categories] + [Q(-(size - 2))],
                    [
                        grid[first_color] + grid[second_color]
                        for first_color, second_color in categories
                    ]
                    + [2 * (1 + grid[q])],
                )
            assert all(
                matvec(direct[q], vector)
                == [Q(0) for _ in range(len(categories) + 1)]
                for vector in kernels
            )

        label = "ordered" if ordered else "unordered"
        audit_results[label] = {
            "base_normalization": (
                "alpha_q" if ordered else "alpha_q/2"
            ),
            "base_count": sum(
                ordered_pair_counts
                if ordered
                else [count // 2 for count in ordered_pair_counts]
            ),
            "extension_profile_count": len(categories),
            "flag_factor": str(flag_factor),
            "all_exact_moment_blocks_match": True,
            "centered_kernel_count": len(kernels),
            "all_centered_kernels_hold": True,
        }

    # K3 -> K4 pointwise centering, checked directly on every ordered triple.
    checked_ordered_triples = 0
    for i, j, k in itertools.permutations(range(size), 3):
        for center, other_one, other_two in (
            (i, j, k),
            (j, i, k),
            (k, i, j),
        ):
            left = sum(
                (
                    dot(roots[center], roots[extension])
                    for extension in range(size)
                    if extension not in (i, j, k)
                ),
                Q(0),
            )
            right = (
                -1
                - dot(roots[center], roots[other_one])
                - dot(roots[center], roots[other_two])
            )
            assert left == right
        checked_ordered_triples += 1

    summary = {
        "schema": "kissing5.ordered_edge_flag_normalization_audit.v1",
        "status": "exact audit on the genuine D5 code",
        "code_size": size,
        "dimension": 5,
        "grid": [str(value) for value in grid],
        "ordered_pair_count": sum(ordered_pair_counts),
        "unordered_pair_count": sum(ordered_pair_counts) // 2,
        "ordered_triple_count": size * (size - 1) * (size - 2),
        "unordered_four_set_count": int(number_four_sets),
        "distinct_k4_orbits_in_d5": len(k4),
        "ordered_triples_checked_for_pointwise_centering": (
            checked_ordered_triples
        ),
        "audit": audit_results,
    }
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    output = Path(__file__).resolve().parent / "results/d5_normalization_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(encoded)
    print(encoded, end="")
    print("sha256=" + hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
