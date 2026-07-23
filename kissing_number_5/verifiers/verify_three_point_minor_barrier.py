#!/usr/bin/env python3
"""Exact verification of a 41-vertex trianglewise-PSD pseudo-Gram object."""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations

try:
    from verifiers.verify_four_point_wedge import (
        N,
        NODES,
        ORDERED_COUNTS,
        zonal_values,
    )
except ModuleNotFoundError:  # Direct execution from the repository root.
    from verify_four_point_wedge import (
        N,
        NODES,
        ORDERED_COUNTS,
        zonal_values,
    )


# A 4-regular girth-six graph on 0,...,40.
DEEP_EDGES = frozenset(
    {
        (0, 2), (0, 3), (0, 14), (0, 30),
        (1, 12), (1, 27), (1, 28), (1, 36),
        (2, 17), (2, 19), (2, 20),
        (3, 15), (3, 16), (3, 25),
        (4, 5), (4, 6), (4, 20), (4, 25),
        (5, 7), (5, 33), (5, 37),
        (6, 11), (6, 24), (6, 30),
        (7, 29), (7, 34), (7, 40),
        (8, 10), (8, 12), (8, 24), (8, 32),
        (9, 14), (9, 21), (9, 27), (9, 32),
        (10, 15), (10, 20), (10, 34),
        (11, 16), (11, 27), (11, 34),
        (12, 25), (12, 31),
        (13, 31), (13, 34), (13, 38), (13, 39),
        (14, 22), (14, 38),
        (15, 23), (15, 36),
        (16, 18), (16, 37),
        (17, 24), (17, 26), (17, 33),
        (18, 29), (18, 35), (18, 39),
        (19, 21), (19, 23), (19, 37),
        (20, 28),
        (21, 29), (21, 31),
        (22, 24), (22, 28), (22, 37),
        (23, 35), (23, 40),
        (25, 26),
        (26, 38), (26, 40),
        (27, 33),
        (28, 39),
        (29, 36),
        (30, 31), (30, 35),
        (32, 39), (32, 40),
        (33, 35),
        (36, 38),
    }
)

HEAVY_EDGES = frozenset(
    {
        (0, 2), (1, 12), (3, 15), (4, 5),
        (6, 11), (7, 29), (8, 10), (9, 14),
        (13, 31), (16, 18), (17, 24), (19, 21),
        (20, 28), (22, 37), (23, 35), (25, 26),
    }
)

# Extra high edges beyond all distance-two pairs of DEEP_EDGES.
EXTRA_HIGH = frozenset(
    {
        (0, 1), (1, 19), (2, 11), (2, 36), (3, 13), (3, 32),
        (4, 18), (5, 8), (5, 39), (6, 40), (7, 14), (7, 30),
        (8, 38), (9, 15), (10, 33), (10, 37), (12, 14),
        (13, 23), (15, 31), (16, 17), (16, 20), (17, 29),
        (18, 24), (19, 25), (20, 35), (21, 24), (21, 26),
        (22, 29), (22, 34), (25, 39), (26, 28), (28, 30),
        (31, 40), (32, 36),
    }
)

# A conflict-free 132-edge class for the value -9/20.
MIDDLE_45 = frozenset(
    {
        (0, 7), (0, 10), (0, 13), (0, 18), (0, 21), (0, 24),
        (0, 33),
        (1, 10), (1, 13), (1, 14), (1, 18), (1, 21), (1, 37),
        (2, 6), (2, 9), (2, 16), (2, 34), (2, 35), (2, 39), (2, 40),
        (3, 17), (3, 19), (3, 20), (3, 31), (3, 38), (3, 39), (3, 40),
        (4, 8), (4, 9), (4, 15), (4, 17), (4, 29), (4, 35),
        (5, 11), (5, 12), (5, 21), (5, 23), (5, 24), (5, 26), (5, 28),
        (6, 7), (6, 10), (6, 12), (6, 13), (6, 32), (6, 36),
        (7, 15), (7, 16), (7, 17), (7, 20), (7, 22),
        (8, 14), (8, 18), (8, 21), (8, 30), (8, 37),
        (9, 18), (9, 23), (9, 24), (9, 28),
        (10, 22), (10, 31), (10, 38), (10, 39),
        (11, 15), (11, 20), (11, 22), (11, 31), (11, 38),
        (12, 15), (12, 19), (12, 29), (12, 34), (12, 40),
        (13, 17), (13, 20), (13, 22), (13, 25),
        (14, 16), (14, 17), (14, 20), (14, 35),
        (15, 24), (15, 26), (15, 33),
        (16, 21), (16, 30), (16, 32), (16, 33),
        (17, 23), (17, 36),
        (18, 25), (18, 38),
        (19, 26), (19, 28), (19, 30), (19, 32), (19, 36),
        (20, 32),
        (21, 34), (21, 40),
        (22, 23), (22, 30), (22, 33),
        (23, 25), (23, 29), (23, 31),
        (24, 25), (24, 39),
        (25, 28), (25, 36),
        (26, 34), (26, 35), (26, 39),
        (28, 34), (28, 35), (28, 38),
        (29, 32), (29, 33), (29, 37),
        (30, 34), (30, 39), (30, 40),
        (31, 32), (31, 36), (31, 37),
        (33, 38),
        (34, 37),
        (35, 36), (35, 37),
        (36, 40),
        (37, 38),
    }
)

# Counts of unordered vertex triples, indexed by the sorted triple of edge
# class indices.  The induced fixed-N three-point measure gives such a class
# mass 6 times this count divided by N.
EXPECTED_TRIPLE_COUNTS = (
    ((0, 1, 5), 96),
    ((0, 2, 3), 22),
    ((0, 2, 4), 60),
    ((0, 2, 5), 130),
    ((0, 3, 3), 15),
    ((0, 3, 4), 14),
    ((0, 3, 5), 48),
    ((0, 4, 4), 74),
    ((0, 4, 5), 165),
    ((1, 1, 5), 150),
    ((1, 2, 3), 67),
    ((1, 2, 4), 253),
    ((1, 2, 5), 524),
    ((1, 3, 3), 53),
    ((1, 3, 4), 76),
    ((1, 3, 5), 157),
    ((1, 4, 4), 324),
    ((1, 4, 5), 724),
    ((2, 2, 3), 42),
    ((2, 2, 4), 168),
    ((2, 2, 5), 534),
    ((2, 3, 3), 77),
    ((2, 3, 4), 164),
    ((2, 3, 5), 353),
    ((2, 4, 4), 521),
    ((2, 4, 5), 1437),
    ((2, 5, 5), 52),
    ((3, 3, 3), 10),
    ((3, 3, 4), 151),
    ((3, 3, 5), 181),
    ((3, 4, 4), 19),
    ((3, 4, 5), 323),
    ((3, 5, 5), 266),
    ((4, 4, 4), 416),
    ((4, 4, 5), 1290),
    ((4, 5, 5), 940),
    ((5, 5, 5), 764),
)


def adjacency(edges):
    result = [set() for _ in range(N)]
    for i, j in edges:
        assert 0 <= i < j < N
        result[i].add(j)
        result[j].add(i)
    return result


def determinant(matrix):
    """Exact determinant by fraction-preserving Gaussian elimination."""

    a = [row[:] for row in matrix]
    answer = Q(1)
    for column in range(len(a)):
        pivot = next(
            (row for row in range(column, len(a)) if a[row][column]),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            a[pivot], a[column] = a[column], a[pivot]
            answer = -answer
        pivot_value = a[column][column]
        answer *= pivot_value
        for row in range(column + 1, len(a)):
            ratio = a[row][column] / pivot_value
            for col in range(column + 1, len(a)):
                a[row][col] -= ratio * a[column][col]
    return answer


def transverse_q(k, u, v, t):
    """Polynomialized normalized transverse Gegenbauer kernel on S^3."""

    if k == 0:
        return Q(1)
    w = t - u * v
    if k == 1:
        return w
    radial_product = (1 - u * u) * (1 - v * v)
    q0, q1 = Q(1), w
    for degree in range(1, k):
        q0, q1 = (
            q1,
            (
                2 * (degree + 1) * w * q1
                - degree * radial_product * q0
            )
            / (degree + 2),
        )
    return q1


def z_matrix(k, radial_degree, u, v, t):
    q = transverse_q(k, u, v, t)
    return [
        [q * u**i * v**j for j in range(radial_degree + 1)]
        for i in range(radial_degree + 1)
    ]


def add_scaled(target, source, scale=Q(1)):
    for i in range(len(target)):
        for j in range(len(target)):
            target[i][j] += scale * source[i][j]


def all_principal_minors(matrix):
    minors = []
    for size in range(1, len(matrix) + 1):
        for indices in combinations(range(len(matrix)), size):
            minors.append(
                (
                    indices,
                    determinant(
                        [[matrix[i][j] for j in indices] for i in indices]
                    ),
                )
            )
    return minors


def build_labels():
    all_pairs = set(combinations(range(N), 2))
    deep_adjacency = adjacency(DEEP_EDGES)
    distance_two = set()
    for neighbors in deep_adjacency:
        distance_two.update(combinations(sorted(neighbors), 2))
    high = frozenset(distance_two | EXTRA_HIGH)
    remaining = sorted(all_pairs - DEEP_EDGES - MIDDLE_45 - high)
    middle_10 = frozenset(remaining[:65])
    middle_095 = frozenset(remaining[65:])
    classes = (
        HEAVY_EDGES,
        DEEP_EDGES - HEAVY_EDGES,
        MIDDLE_45,
        middle_10,
        middle_095,
        high,
    )
    labels = {}
    types = {}
    assert len(NODES) == len(classes)
    for edge_type, (node, edges) in enumerate(zip(NODES, classes)):
        for edge in edges:
            labels[edge] = node
            types[edge] = edge_type
    return classes, labels, types, distance_two


def gram(vertices, labels):
    return [
        [
            Q(1)
            if i == j
            else labels[tuple(sorted((vertices[i], vertices[j])))]
            for j in range(len(vertices))
        ]
        for i in range(len(vertices))
    ]


def canonical_k4_pattern(vertices, types):
    return min(
        tuple(
            types[tuple(sorted((order[i], order[j])))]
            for i, j in combinations(range(4), 2)
        )
        for order in permutations(vertices)
    )


def verify():
    classes, labels, types, distance_two = build_labels()
    assert [len(edges) for edges in classes] == [16, 66, 132, 65, 261, 280]
    assert [2 * len(edges) for edges in classes] == list(ORDERED_COUNTS)
    assert len(labels) == N * (N - 1) // 2

    deep_adjacency = adjacency(DEEP_EDGES)
    assert all(len(neighbors) == 4 for neighbors in deep_adjacency)
    assert len(distance_two) == 246
    assert not (distance_two & DEEP_EDGES)
    assert max(
        len(deep_adjacency[i] & deep_adjacency[j])
        for i, j in combinations(range(N), 2)
    ) == 1

    # No cycle of length five: an edge's endpoints cannot have a common
    # distance-two vertex.
    distance_two_adjacency = adjacency(distance_two)
    assert all(
        not (distance_two_adjacency[i] & distance_two_adjacency[j])
        for i, j in DEEP_EDGES
    )

    # The heavy class is a matching.
    heavy_degrees = [
        sum(vertex in edge for edge in HEAVY_EDGES) for vertex in range(N)
    ]
    assert sorted(heavy_degrees) == [0] * 9 + [1] * 32

    # Neither the high graph nor the -9/20 graph gives the endpoints of a
    # deep edge a common neighbor.  These are exactly the remaining forbidden
    # triangle patterns after distance-two pairs have been made high.
    high_adjacency = adjacency(classes[-1])
    middle_adjacency = adjacency(MIDDLE_45)
    assert all(not (high_adjacency[i] & high_adjacency[j])
               for i, j in DEEP_EDGES)
    assert all(not (middle_adjacency[i] & middle_adjacency[j])
               for i, j in DEEP_EDGES)
    high_degrees = [
        sum(vertex in edge for edge in classes[-1]) for vertex in range(N)
    ]
    assert sorted(high_degrees) == [12] + [13] * 12 + [14] * 28

    # Pfender's inequality holds separately in every row.
    row_values = []
    for vertex in range(N):
        row_values.append(
            sum(
                (
                    2 * labels[edge] ** 2 - 1
                    for edge in DEEP_EDGES
                    if vertex in edge
                ),
                Q(0),
            )
        )
    assert set(row_values) == {Q(542, 625), Q(17657, 20000)}
    assert max(row_values) < 1

    # Every 3-by-3 principal submatrix is positive definite.
    triple_values = []
    triple_counts = Counter()
    for vertices in combinations(range(N), 3):
        triple_values.append((determinant(gram(vertices, labels)), vertices))
        triple_counts[
            tuple(
                sorted(
                    types[tuple(sorted(edge))]
                    for edge in combinations(vertices, 2)
                )
            )
        ] += 1
    triple_minimum = min(triple_values)
    assert triple_minimum == (Q(34771, 400000), (0, 1, 33))
    assert tuple(sorted(triple_counts.items())) == EXPECTED_TRIPLE_COUNTS

    # Aggregate the labeled triples into the exact fixed-N
    # Bachoc--Vallentin measure.  With the normalization used here, alpha is
    # the ordered pair distribution divided by N, and a sorted triple orbit
    # with n unordered occurrences has mass 6n/N.
    alpha = [Q(count, N) for count in ORDERED_COUNTS]
    triple_types = [triple for triple, _ in EXPECTED_TRIPLE_COUNTS]
    nu = [Q(6 * count, N) for _, count in EXPECTED_TRIPLE_COUNTS]
    assert sum(alpha) == N - 1
    assert sum(nu) == (N - 1) * (N - 2)
    for edge_type in range(len(NODES)):
        marginal = sum(
            weight * triple.count(edge_type) / 3
            for triple, weight in zip(triple_types, nu)
        )
        assert marginal == (N - 2) * alpha[edge_type]

    def harmonic_matrix(total_degree, harmonic_degree):
        radial_degree = total_degree - harmonic_degree
        matrix = [
            [Q(0) for _ in range(radial_degree + 1)]
            for _ in range(radial_degree + 1)
        ]
        add_scaled(
            matrix,
            z_matrix(
                harmonic_degree, radial_degree, Q(1), Q(1), Q(1)
            ),
        )
        for node, weight in zip(NODES, alpha):
            add_scaled(
                matrix,
                z_matrix(
                    harmonic_degree, radial_degree, Q(1), node, node
                ),
                weight,
            )
            add_scaled(
                matrix,
                z_matrix(
                    harmonic_degree, radial_degree, node, Q(1), node
                ),
                weight,
            )
            add_scaled(
                matrix,
                z_matrix(
                    harmonic_degree, radial_degree, node, node, Q(1)
                ),
                weight,
            )
        for triple, weight in zip(triple_types, nu):
            values = tuple(NODES[index] for index in triple)
            orbit = sorted(set(permutations(values)))
            for u, v, t in orbit:
                add_scaled(
                    matrix,
                    z_matrix(
                        harmonic_degree, radial_degree, u, v, t
                    ),
                    weight / len(orbit),
                )
        assert all(
            matrix[i][j] == matrix[j][i]
            for i in range(len(matrix))
            for j in range(len(matrix))
        )
        return matrix

    # All blocks at total degree zero and one pass.  At total degree two the
    # k=0 and k=1 blocks still pass, but the scalar k=2 block is negative.
    first_failing_bv_block = None
    for total_degree in range(3):
        for harmonic_degree in range(total_degree + 1):
            matrix = harmonic_matrix(total_degree, harmonic_degree)
            minors = all_principal_minors(matrix)
            failures = [
                (value, indices) for indices, value in minors if value < 0
            ]
            if failures and first_failing_bv_block is None:
                first_failing_bv_block = (
                    total_degree,
                    harmonic_degree,
                    len(matrix),
                    min(failures),
                )
    assert first_failing_bv_block == (
        2,
        2,
        1,
        (Q(-306927942881, 16400000000), (0,)),
    )

    # The first obstruction occurs at order four.
    quadruple_minimum = None
    negative_quadruples = 0
    zero_quadruples = 0
    negative_patterns = Counter()
    for vertices in combinations(range(N), 4):
        value = determinant(gram(vertices, labels))
        if quadruple_minimum is None or (value, vertices) < quadruple_minimum:
            quadruple_minimum = (value, vertices)
        if value == 0:
            zero_quadruples += 1
        if value < 0:
            negative_quadruples += 1
            negative_patterns[canonical_k4_pattern(vertices, types)] += 1
    assert quadruple_minimum == (Q(-2436203, 3125000), (0, 2, 7, 34))
    assert negative_quadruples == 10670
    assert zero_quadruples == 0
    assert len(negative_patterns) == 192

    # Repeat the exact two-point moment check for this labeled realization.
    values = [zonal_values(node, 103) for node in NODES]
    moments = [
        Q(N)
        + sum(
            ORDERED_COUNTS[i] * values[i][degree]
            for i in range(len(NODES))
        )
        for degree in range(1, 104)
    ]
    moment_minimum = min(
        (value, degree) for degree, value in enumerate(moments, 1)
    )
    assert moment_minimum == (Q(30261, 16000), 2)
    q_minimum = Q(15351, 40000)
    assert min(1 - node * node for node in NODES) == q_minimum
    assert q_minimum**3 > Q(4, 17) ** 2
    assert 1054**2 < 104**3

    return {
        "pair_classes": tuple(map(len, classes)),
        "distance_two_pairs": len(distance_two),
        "maximum_pfender_row": max(row_values),
        "minimum_3_by_3": triple_minimum,
        "triple_orbit_count": len(triple_counts),
        "first_failing_bv_block": first_failing_bv_block,
        "minimum_4_by_4": quadruple_minimum,
        "negative_4_by_4_count": negative_quadruples,
        "negative_4_by_4_pattern_count": len(negative_patterns),
        "minimum_moment_unnormalized": moment_minimum[0],
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
