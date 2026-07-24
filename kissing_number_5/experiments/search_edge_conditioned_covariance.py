#!/usr/bin/env python3
"""Test four-point extendibility via edge-conditioned degree covariance.

Discovery code only.  It enumerates all Gram-PSD colored K4 types on the
local five-node support, imposes their triangle marginals, and separates the
five edge-conditioned covariance PSD blocks.
"""

from fractions import Fraction as Q
from itertools import combinations_with_replacement, permutations, product

import numpy as np
from scipy.optimize import linprog

from verifiers.verify_local_hybrid_degree4_rank_color_clique import (
    load_certificate,
)


VERTICES = tuple(range(4))
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
PERMUTATIONS = tuple(permutations(VERTICES))


def determinant(matrix):
    matrix = [list(row) for row in matrix]
    size = len(matrix)
    answer = Q(1)
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            matrix[column], matrix[pivot] = (
                matrix[pivot],
                matrix[column],
            )
            answer = -answer
        pivot_value = matrix[column][column]
        answer *= pivot_value
        for row in range(column + 1, size):
            scale = matrix[row][column] / pivot_value
            for other in range(column + 1, size):
                matrix[row][other] -= scale * matrix[column][other]
    return answer


def transform(pattern, permutation):
    transformed = []
    for first, second in EDGES:
        image = tuple(sorted((permutation[first], permutation[second])))
        transformed.append(pattern[EDGE_INDEX[image]])
    return tuple(transformed)


def canonical(pattern):
    return min(
        transform(pattern, permutation) for permutation in PERMUTATIONS
    )


def triangle_faces(pattern):
    answer = []
    for face in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
        first, second, third = face
        answer.append(
            tuple(
                sorted(
                    (
                        pattern[
                            EDGE_INDEX[tuple(sorted((first, second)))]
                        ],
                        pattern[
                            EDGE_INDEX[tuple(sorted((first, third)))]
                        ],
                        pattern[
                            EDGE_INDEX[tuple(sorted((second, third)))]
                        ],
                    )
                )
            )
        )
    return tuple(answer)


def gram_matrix(pattern, nodes):
    matrix = [
        [Q(int(first == second)) for second in VERTICES]
        for first in VERTICES
    ]
    for color, (first, second) in zip(pattern, EDGES):
        matrix[first][second] = nodes[color]
        matrix[second][first] = nodes[color]
    return matrix


def feasible_triangle_types(nodes):
    answer = []
    for triple in combinations_with_replacement(range(len(nodes)), 3):
        u, v, t = (nodes[index] for index in triple)
        if 1 + 2 * u * v * t - u * u - v * v - t * t >= 0:
            answer.append(triple)
    return tuple(answer)


def feasible_four_types(nodes, triangle_types):
    representatives = {}
    triangle_type_set = set(triangle_types)
    for pattern in product(range(len(nodes)), repeat=len(EDGES)):
        if any(
            face not in triangle_type_set for face in triangle_faces(pattern)
        ):
            continue
        if determinant(gram_matrix(pattern, nodes)) < 0:
            continue
        representative = canonical(pattern)
        representatives.setdefault(representative, representative)
    return tuple(sorted(representatives))


def profile_categories(color_count):
    return tuple(
        combinations_with_replacement(range(color_count), 2)
    )


def edge_profile_second_coefficients(pattern, color_count):
    """Distinct-third-vertex contribution to sum_e n(e)n(e)^T."""

    categories = profile_categories(color_count)
    category_index = {
        category: index for index, category in enumerate(categories)
    }
    blocks = [
        [
            [0 for _ in categories] for _ in categories
        ]
        for _ in range(color_count)
    ]
    for edge_index, (first, second) in enumerate(EDGES):
        anchor_color = pattern[edge_index]
        remaining = [
            vertex
            for vertex in VERTICES
            if vertex not in {first, second}
        ]
        profile_indices = []
        for vertex in remaining:
            first_color = pattern[
                EDGE_INDEX[tuple(sorted((first, vertex)))]
            ]
            second_color = pattern[
                EDGE_INDEX[tuple(sorted((second, vertex)))]
            ]
            profile_indices.append(
                category_index[tuple(sorted((first_color, second_color)))]
            )
        alpha, beta = profile_indices
        if alpha == beta:
            blocks[anchor_color][alpha][alpha] += 2
        else:
            blocks[anchor_color][alpha][beta] += 1
            blocks[anchor_color][beta][alpha] += 1
    return blocks


def edge_profile_first_moments(
    triangle_counts, color_count, categories
):
    category_index = {
        category: index for index, category in enumerate(categories)
    }
    first_moments = [
        [0 for _ in categories] for _ in range(color_count)
    ]
    for triple, count in triangle_counts.items():
        for edge_position, anchor_color in enumerate(triple):
            other = tuple(
                sorted(
                    triple[position]
                    for position in range(3)
                    if position != edge_position
                )
            )
            first_moments[anchor_color][category_index[other]] += count
    return first_moments


def rational_direction(vector, denominator=100000):
    pivot = int(np.argmax(np.abs(vector)))
    scaled = vector / vector[pivot]
    answer = tuple(
        Q(float(value)).limit_denominator(denominator)
        for value in scaled
    )
    assert answer[pivot] == 1
    return answer


def quadratic(matrix, vector):
    return sum(
        vector[i] * matrix[i][j] * vector[j]
        for i in range(len(vector))
        for j in range(len(vector))
    )


def main():
    nodes, ordered_counts, triple_counts, _ = load_certificate()
    triangle_types = feasible_triangle_types(nodes)
    four_types = feasible_four_types(nodes, triangle_types)
    print(
        "triangle types",
        len(triangle_types),
        "Gram-PSD K4 orbits",
        len(four_types),
        flush=True,
    )

    face_incidence = [
        [triangle_faces(pattern).count(triple) for pattern in four_types]
        for triple in triangle_types
    ]
    face_targets = [
        38 * triple_counts.get(triple, 0) for triple in triangle_types
    ]
    categories = profile_categories(len(nodes))
    first_moments = edge_profile_first_moments(
        triple_counts, len(nodes), categories
    )
    four_coefficients = [
        edge_profile_second_coefficients(pattern, len(nodes))
        for pattern in four_types
    ]
    covariance_constants = []
    covariance_coefficients = []
    for color in range(len(nodes)):
        edge_count = ordered_counts[color] // 2
        first = first_moments[color]
        constant = [
            [
                (
                    Q(first[row]) if row == column else Q(0)
                )
                - Q(first[row] * first[column], edge_count)
                for column in range(len(categories))
            ]
            for row in range(len(categories))
        ]
        covariance_constants.append(constant)
        covariance_coefficients.append(
            [
                four_coefficients[index][color]
                for index in range(len(four_types))
            ]
        )

    cuts = []
    for color in range(len(nodes)):
        for coordinate in range(len(categories)):
            direction = tuple(
                Q(int(index == coordinate))
                for index in range(len(categories))
            )
            cuts.append((color, direction))

    for round_index in range(100):
        rows = []
        bounds = []
        for color, direction in cuts:
            constant = quadratic(covariance_constants[color], direction)
            coefficient = [
                quadratic(matrix, direction)
                for matrix in covariance_coefficients[color]
            ]
            rows.append([-float(value) for value in coefficient])
            bounds.append(float(constant))
        result = linprog(
            np.zeros(len(four_types)),
            A_ub=np.array(rows),
            b_ub=np.array(bounds),
            A_eq=np.array(face_incidence, dtype=float),
            b_eq=np.array(face_targets, dtype=float),
            bounds=(0, None),
            method="highs",
        )
        print(
            "round",
            round_index,
            "cuts",
            len(cuts),
            "status",
            result.status,
            result.message,
            flush=True,
        )
        if not result.success:
            print("four-point relaxation infeasible", flush=True)
            return

        new_cuts = []
        minima = []
        for color in range(len(nodes)):
            matrix = np.array(covariance_constants[color], dtype=float)
            for value, coefficient in zip(
                result.x, covariance_coefficients[color]
            ):
                matrix += value * np.array(coefficient, dtype=float)
            eigenvalues, eigenvectors = np.linalg.eigh(matrix)
            minima.append(eigenvalues[0])
            if eigenvalues[0] < -1e-7:
                candidate = (
                    color,
                    rational_direction(eigenvectors[:, 0]),
                )
                if candidate not in cuts and candidate not in new_cuts:
                    new_cuts.append(candidate)
        print("minimum eigenvalues", minima, flush=True)
        if not new_cuts:
            if min(minima) >= -1e-7:
                print(
                    "four-point edge-covariance extension found; "
                    "this constraint does not separate the witness",
                    flush=True,
                )
                nonzero = sum(value > 1e-8 for value in result.x)
                print("nonzero K4 orbit weights", nonzero, flush=True)
                return
            raise RuntimeError("rational separation stalled")
        cuts.extend(new_cuts)
    raise RuntimeError("cutting-plane limit reached")


if __name__ == "__main__":
    main()
