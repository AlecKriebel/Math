#!/usr/bin/env python3
"""Exact verifier for a trianglewise-PSD barrier passing degree-2 BV."""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations

try:
    from verifiers.verify_three_point_minor_barrier import (
        DEEP_EDGES,
        HEAVY_EDGES,
        N,
        NODES,
        ORDERED_COUNTS,
        add_scaled,
        adjacency,
        all_principal_minors,
        determinant,
        gram,
        transverse_q,
        z_matrix,
        zonal_values,
    )
except ModuleNotFoundError:  # Direct execution from the repository root.
    from verify_three_point_minor_barrier import (
        DEEP_EDGES,
        HEAVY_EDGES,
        N,
        NODES,
        ORDERED_COUNTS,
        add_scaled,
        adjacency,
        all_principal_minors,
        determinant,
        gram,
        transverse_q,
        z_matrix,
        zonal_values,
    )


MIDDLE_45 = frozenset(
    {
        (0, 10), (0, 12), (0, 13), (0, 26), (0, 27), (0, 28),
        (1, 2), (1, 6), (1, 10), (1, 13), (1, 14), (1, 16),
        (1, 21), (1, 35), (1, 40), (2, 6), (2, 8), (2, 15),
        (2, 16), (2, 22), (2, 34), (2, 39), (3, 5), (3, 9),
        (3, 20), (3, 24), (3, 29), (3, 35), (3, 40), (4, 8),
        (4, 15), (4, 19), (4, 22), (4, 27), (4, 29), (4, 38),
        (4, 39), (5, 12), (5, 21), (5, 23), (5, 28), (5, 32),
        (5, 36), (6, 9), (6, 13), (6, 23), (6, 26), (7, 8),
        (7, 9), (7, 19), (7, 25), (7, 38), (7, 39), (8, 14),
        (8, 26), (8, 27), (9, 10), (9, 13), (9, 18), (9, 28),
        (10, 17), (10, 29), (10, 37), (10, 38), (11, 15),
        (11, 19), (11, 20), (11, 25), (11, 38), (11, 40),
        (12, 15), (12, 22), (12, 39), (13, 23), (13, 25),
        (13, 29), (14, 16), (14, 31), (14, 33), (14, 39),
        (15, 21), (15, 33), (15, 39), (16, 26), (16, 30),
        (16, 32), (16, 33), (17, 23), (17, 28), (17, 29),
        (17, 31), (17, 32), (18, 19), (18, 22), (18, 25),
        (18, 31), (18, 34), (18, 40), (19, 24), (19, 30),
        (19, 38), (20, 24), (20, 30), (20, 36), (21, 22),
        (21, 34), (21, 39), (22, 27), (22, 34), (23, 27),
        (23, 28), (24, 35), (24, 36), (25, 28), (25, 33),
        (25, 37), (26, 27), (27, 29), (27, 31), (28, 31),
        (30, 32), (30, 34), (30, 38), (31, 36), (31, 37),
        (31, 40), (32, 36), (33, 34), (33, 39), (33, 40),
        (35, 37), (37, 40),
    }
)

MIDDLE_10 = frozenset(
    {
        (0, 7), (1, 3), (1, 18), (1, 30), (2, 25), (2, 31),
        (3, 21), (3, 28), (5, 13), (5, 14), (5, 18), (5, 24),
        (6, 10), (6, 28), (6, 29), (6, 39), (7, 20), (7, 22),
        (7, 31), (8, 13), (9, 12), (9, 17), (9, 23), (9, 34),
        (10, 26), (10, 35), (11, 12), (11, 17), (11, 22),
        (11, 36), (12, 14), (12, 20), (13, 16), (13, 24),
        (13, 27), (13, 35), (14, 19), (14, 20), (14, 29),
        (14, 34), (15, 31), (15, 37), (16, 17), (16, 38),
        (19, 25), (19, 26), (20, 23), (20, 32), (20, 35),
        (21, 25), (22, 25), (23, 39), (24, 25), (25, 35),
        (26, 29), (27, 39), (28, 29), (28, 33), (28, 38),
        (28, 40), (29, 30), (32, 35), (33, 38), (35, 36),
        (37, 38),
    }
)

EXTRA_HIGH = frozenset(
    {
        (0, 5), (0, 29), (0, 34), (2, 32), (2, 36), (3, 32),
        (4, 13), (4, 14), (4, 21), (6, 19), (7, 14), (8, 35),
        (10, 21), (10, 30), (11, 23), (11, 26), (12, 18),
        (12, 23), (12, 37), (13, 33), (14, 23), (15, 22),
        (17, 34), (17, 39), (20, 38), (20, 40), (21, 26),
        (22, 35), (24, 29), (25, 29), (25, 39), (26, 30),
        (30, 37), (35, 38),
    }
)


def build_labels():
    all_pairs = set(combinations(range(N), 2))
    deep_adjacency = adjacency(DEEP_EDGES)
    distance_two = set()
    for neighbors in deep_adjacency:
        distance_two.update(combinations(sorted(neighbors), 2))
    high = frozenset(distance_two | EXTRA_HIGH)
    used = DEEP_EDGES | MIDDLE_45 | MIDDLE_10 | high
    middle_095 = frozenset(all_pairs - used)
    classes = (
        HEAVY_EDGES,
        DEEP_EDGES - HEAVY_EDGES,
        MIDDLE_45,
        MIDDLE_10,
        middle_095,
        high,
    )
    labels = {}
    types = {}
    for edge_type, (node, edges) in enumerate(zip(NODES, classes)):
        for edge in edges:
            assert edge not in labels
            labels[edge] = node
            types[edge] = edge_type
    return classes, labels, types, distance_two


def triple_measure(types):
    counts = Counter()
    for vertices in combinations(range(N), 3):
        counts[
            tuple(
                sorted(
                    types[tuple(sorted(edge))]
                    for edge in combinations(vertices, 2)
                )
            )
        ] += 1
    triples = sorted(counts)
    nu = [Q(6 * counts[triple], N) for triple in triples]
    return counts, triples, nu


def harmonic_matrix(total_degree, harmonic_degree, triples, nu):
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
    alpha = [Q(count, N) for count in ORDERED_COUNTS]
    for node, weight in zip(NODES, alpha):
        add_scaled(
            matrix,
            z_matrix(harmonic_degree, radial_degree, Q(1), node, node),
            weight,
        )
        add_scaled(
            matrix,
            z_matrix(harmonic_degree, radial_degree, node, Q(1), node),
            weight,
        )
        add_scaled(
            matrix,
            z_matrix(harmonic_degree, radial_degree, node, node, Q(1)),
            weight,
        )
    for triple, weight in zip(triples, nu):
        values = tuple(NODES[index] for index in triple)
        orbit = sorted(set(permutations(values)))
        for u, v, t in orbit:
            add_scaled(
                matrix,
                z_matrix(harmonic_degree, radial_degree, u, v, t),
                weight / len(orbit),
            )
    return matrix


def verify():
    classes, labels, types, distance_two = build_labels()
    assert tuple(map(len, classes)) == (16, 66, 132, 65, 261, 280)
    assert len(labels) == N * (N - 1) // 2
    assert len(distance_two) == 246

    # The negative-wedge incidence conditions are retained.
    deep_adjacency = adjacency(DEEP_EDGES)
    high_adjacency = adjacency(classes[5])
    middle_adjacency = adjacency(MIDDLE_45)
    assert all(len(neighbors) == 4 for neighbors in deep_adjacency)
    assert all(
        not (high_adjacency[i] & high_adjacency[j])
        for i, j in DEEP_EDGES
    )
    assert all(
        not (middle_adjacency[i] & middle_adjacency[j])
        for i, j in DEEP_EDGES
    )

    triple_minimum = min(
        (determinant(gram(vertices, labels)), vertices)
        for vertices in combinations(range(N), 3)
    )
    assert triple_minimum == (Q(34771, 400000), (0, 5, 27))

    counts, triples, nu = triple_measure(types)
    assert len(triples) == 38
    assert sum(nu) == (N - 1) * (N - 2)
    alpha = [Q(count, N) for count in ORDERED_COUNTS]
    for edge_type in range(len(NODES)):
        assert sum(
            weight * triple.count(edge_type) / 3
            for triple, weight in zip(triples, nu)
        ) == (N - 2) * alpha[edge_type]

    # Every fixed-N BV block of total degree at most two is positive
    # definite.
    degree_two_minors = {}
    for harmonic_degree in range(3):
        matrix = harmonic_matrix(2, harmonic_degree, triples, nu)
        minors = all_principal_minors(matrix)
        assert all(value > 0 for _, value in minors)
        degree_two_minors[harmonic_degree] = minors
    k2_scalar = harmonic_matrix(2, 2, triples, nu)[0][0]
    assert k2_scalar == Q(8701609923, 16400000000)

    # The first failed block is total degree three, k=1.  The k=0 block
    # immediately before it is positive definite.
    degree_three_k0 = harmonic_matrix(3, 0, triples, nu)
    assert all(
        value > 0 for _, value in all_principal_minors(degree_three_k0)
    )
    degree_three_k1 = harmonic_matrix(3, 1, triples, nu)
    assert degree_three_k1 == [
        [
            Q(1636251, 205000),
            Q(-172747923, 164000000),
            Q(52884578739, 32800000000),
        ],
        [
            Q(-172747923, 164000000),
            Q(8600664577, 16400000000),
            Q(9151184465761, 3280000000000),
        ],
        [
            Q(52884578739, 32800000000),
            Q(9151184465761, 3280000000000),
            Q(694136547054399, 656000000000000),
        ],
    ]
    failed_minor_12 = (
        degree_three_k1[1][1] * degree_three_k1[2][2]
        - degree_three_k1[1][2] ** 2
    )
    assert failed_minor_12 == Q(
        -38887070757266787904992449,
        5379200000000000000000000,
    )
    full_failed_determinant = determinant(degree_three_k1)
    assert full_failed_determinant == Q(
        -615018788827907136219533721201153,
        8821888000000000000000000000000,
    )

    # A particularly short scalar separator uses f(u)=u-(8/3)u^2.  It is
    # the quadratic form of the k=1 matrix at the vector (0,1,-8/3).
    vector = (Q(0), Q(1), Q(-8, 3))
    weighted_residual_scalar = sum(
        vector[i] * degree_three_k1[i][j] * vector[j]
        for i in range(3)
        for j in range(3)
    )
    assert weighted_residual_scalar == Q(
        -105027064094021, 15375000000000
    )

    # The dominant colored-wedge incidence is exact.  Triangle PSD forbids
    # a deep edge from being completed by two -9/20 edges, so all
    # 4 * 2|MIDDLE_45| = 1056 incident deep-middle wedges appear in one of
    # the six classes below.
    deep_middle_counts = {
        triple: counts[triple]
        for triple in (
            (0, 2, 3), (0, 2, 4), (0, 2, 5),
            (1, 2, 3), (1, 2, 4), (1, 2, 5),
        )
    }
    assert deep_middle_counts == {
        (0, 2, 3): 9,
        (0, 2, 4): 79,
        (0, 2, 5): 118,
        (1, 2, 3): 73,
        (1, 2, 4): 308,
        (1, 2, 5): 469,
    }
    assert sum(deep_middle_counts.values()) == 4 * 2 * len(MIDDLE_45)

    # It remains far from four-locally PSD.
    quadruple_minimum = None
    negative_quadruples = 0
    for vertices in combinations(range(N), 4):
        value = determinant(gram(vertices, labels))
        item = value, vertices
        if quadruple_minimum is None or item < quadruple_minimum:
            quadruple_minimum = item
        negative_quadruples += value < 0
    assert quadruple_minimum == (Q(-712327, 500000), (1, 15, 16, 39))
    assert negative_quadruples == 14608

    # The pair distribution, hence all two-point moment checks, is unchanged.
    values = [zonal_values(node, 103) for node in NODES]
    moments = [
        Q(N)
        + sum(
            ORDERED_COUNTS[i] * values[i][degree]
            for i in range(len(NODES))
        )
        for degree in range(1, 104)
    ]
    assert min((value, degree) for degree, value in enumerate(moments, 1)) == (
        Q(30261, 16000),
        2,
    )

    return {
        "pair_classes": tuple(map(len, classes)),
        "minimum_3_by_3": triple_minimum,
        "triple_orbit_count": len(triples),
        "degree_2_k2_scalar": k2_scalar,
        "degree_3_k1_failed_minor": failed_minor_12,
        "degree_3_weighted_residual_scalar": weighted_residual_scalar,
        "deep_middle_wedge_count": sum(deep_middle_counts.values()),
        "minimum_4_by_4": quadruple_minimum,
        "negative_4_by_4_count": negative_quadruples,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
