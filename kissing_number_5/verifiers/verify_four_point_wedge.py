#!/usr/bin/env python3
"""Exact audit of the four-point wedge inequalities and a barrier witness.

Only Python's standard library is used.  The labeled complete graph produced
below is not asserted to be a Gram matrix.  It is a pseudo-incidence object
which satisfies all inequalities whose center has two negative incident
labels, while deliberately failing some other three-point PSD constraints.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations


N = 41
NODES = (
    Q(-157, 200),
    Q(-39, 50),
    Q(-9, 20),
    Q(-1, 10),
    Q(-19, 200),
    Q(99, 200),
)
ORDERED_COUNTS = (32, 132, 264, 130, 522, 560)

# A 4-regular graph of girth at least five on vertices 0,...,40.
LOW_EDGES = frozenset(
    {
        (0, 8), (0, 19), (0, 20), (0, 27),
        (1, 2), (1, 14), (1, 20), (1, 32),
        (2, 9), (2, 16), (2, 40),
        (3, 18), (3, 24), (3, 34), (3, 38),
        (4, 28), (4, 33), (4, 34), (4, 35),
        (5, 14), (5, 16), (5, 17), (5, 18),
        (6, 8), (6, 10), (6, 32), (6, 35),
        (7, 15), (7, 19), (7, 32), (7, 34),
        (8, 13), (8, 36),
        (9, 12), (9, 17), (9, 25),
        (10, 31), (10, 37), (10, 38),
        (11, 13), (11, 21), (11, 27), (11, 29),
        (12, 19), (12, 31), (12, 39),
        (13, 30), (13, 31),
        (14, 26), (14, 31),
        (15, 16), (15, 23), (15, 30),
        (16, 21),
        (17, 27), (17, 33),
        (18, 36), (18, 37),
        (19, 40),
        (20, 33), (20, 37),
        (21, 24), (21, 25),
        (22, 24), (22, 26), (22, 27), (22, 39),
        (23, 29), (23, 37), (23, 39),
        (24, 35),
        (25, 30), (25, 32),
        (26, 29), (26, 34),
        (28, 29), (28, 30), (28, 38),
        (33, 36),
        (35, 40),
        (36, 40),
        (38, 39),
    }
)

# Sixteen vertex-disjoint LOW_EDGES receive the deeper of the two labels.
HEAVY_EDGES = frozenset(
    {
        (0, 8), (1, 2), (3, 18), (4, 28),
        (5, 14), (6, 10), (7, 15), (9, 12),
        (11, 13), (16, 21), (17, 27), (19, 40),
        (20, 33), (22, 24), (23, 29), (25, 30),
    }
)

# A proper 3-coloring of LOW_EDGES.
COLORS = (
    0, 0, 1, 2, 0, 2, 0, 0, 1, 2, 1, 1, 0, 0,
    1, 2, 0, 0, 1, 1, 1, 2, 1, 1, 0, 0, 2, 2,
    2, 0, 1, 2, 1, 2, 1, 1, 0, 0, 0, 2, 2,
)

# Added to all distance-two pairs to form the 280-edge high graph.
EXTRA_HIGH = frozenset(
    {
        (0, 2), (0, 30), (1, 3), (1, 11), (2, 29),
        (3, 11), (4, 15), (4, 19), (5, 19), (5, 24),
        (6, 21), (6, 28), (7, 10), (7, 18), (8, 24),
        (8, 37), (9, 13), (9, 14), (10, 17), (12, 15),
        (12, 18), (13, 22), (14, 25), (16, 22), (16, 33),
        (17, 21), (20, 26), (20, 38), (23, 25), (23, 27),
        (26, 35), (31, 34), (32, 36), (39, 40),
    }
)


def zonal_values(t: Q, degree: int) -> list[Q]:
    """Normalized dimension-five Gegenbauer values P_0,...,P_degree."""

    if degree == 0:
        return [Q(1)]
    values = [Q(1), t]
    for k in range(2, degree + 1):
        values.append(
            (
                (2 * k + 1) * t * values[-1]
                - (k - 1) * values[-2]
            )
            / (k + 2)
        )
    return values


def adjacency(edges: set[tuple[int, int]] | frozenset[tuple[int, int]]):
    result = [set() for _ in range(N)]
    for i, j in edges:
        assert 0 <= i < j < N
        result[i].add(j)
        result[j].add(i)
    return result


def build_classes():
    """Construct the six edge classes deterministically from the certificate."""

    all_pairs = set(combinations(range(N), 2))
    low_adjacency = adjacency(LOW_EDGES)
    distance_two = set()
    for neighbors in low_adjacency:
        distance_two.update(combinations(sorted(neighbors), 2))

    middle_candidates = [
        edge
        for edge in sorted(all_pairs)
        if COLORS[edge[0]] == COLORS[edge[1]]
        and edge not in LOW_EDGES
        and edge not in distance_two
    ]
    middle_45 = frozenset(middle_candidates[:132])
    high = frozenset(distance_two | EXTRA_HIGH)
    remaining = sorted(all_pairs - LOW_EDGES - high - middle_45)
    middle_10 = frozenset(remaining[:65])
    middle_095 = frozenset(remaining[65:])
    return (
        HEAVY_EDGES,
        LOW_EDGES - HEAVY_EDGES,
        middle_45,
        middle_10,
        middle_095,
        high,
    ), distance_two, middle_candidates


def verify() -> dict[str, object]:
    """Run all exact arithmetic and finite incidence checks."""

    classes, distance_two, middle_candidates = build_classes()

    # Pair counts and an exact complete-graph partition.
    assert [len(edges) for edges in classes] == [16, 66, 132, 65, 261, 280]
    assert [2 * len(edges) for edges in classes] == list(ORDERED_COUNTS)
    assert sum(ORDERED_COUNTS) == N * (N - 1)
    assert len(set().union(*classes)) == N * (N - 1) // 2
    assert sum(map(len, classes)) == N * (N - 1) // 2

    # The full deep graph is 4-regular, triangle-free, and square-free.
    low_adjacency = adjacency(LOW_EDGES)
    assert all(len(neighbors) == 4 for neighbors in low_adjacency)
    assert all(COLORS[i] != COLORS[j] for i, j in LOW_EDGES)
    assert len(distance_two) == N * 6 == 246
    assert not (distance_two & LOW_EDGES)
    assert max(
        len(low_adjacency[i] & low_adjacency[j])
        for i, j in combinations(range(N), 2)
    ) == 1

    # The heavy graph is a matching and the high graph contains every
    # distance-two pair.  Its degrees are exactly 14^27,13^14.
    assert HEAVY_EDGES <= LOW_EDGES
    heavy_degrees = [
        sum(vertex in edge for edge in HEAVY_EDGES) for vertex in range(N)
    ]
    assert sorted(heavy_degrees) == [0] * 9 + [1] * 32
    assert len(middle_candidates) == 138
    high = classes[-1]
    assert distance_two <= high
    high_degrees = [sum(vertex in edge for edge in high) for vertex in range(N)]
    assert sorted(high_degrees) == [13] * 14 + [14] * 27

    # Pfender's row generator, checked row by row.  Its support is precisely
    # LOW_EDGES for these labels.
    labels = {}
    for node, edges in zip(NODES, classes, strict=True):
        for edge in edges:
            labels[edge] = node
    row_values = []
    for vertex in range(N):
        row_values.append(
            sum(
                (
                    2 * labels[edge] ** 2 - 1
                    for edge in LOW_EDGES
                    if vertex in edge
                ),
                Q(0),
            )
        )
    assert set(row_values) == {Q(542, 625), Q(17657, 20000)}
    assert max(row_values) < 1
    assert sum(row_values, Q(0)) == Q(4507, 125)

    # Every negative-centered wedge, including every mixed-depth wedge, has a
    # PSD 3-by-3 Gram minor.  The exact minimum is positive.
    negative_center_minimum = None
    negative_center_argmin = None
    for center in range(N):
        others = [vertex for vertex in range(N) if vertex != center]
        for y, z in combinations(others, 2):
            u = labels[tuple(sorted((center, y)))]
            v = labels[tuple(sorted((center, z)))]
            if u >= 0 or v >= 0:
                continue
            w = labels[tuple(sorted((y, z)))]
            determinant = 1 + 2 * u * v * w - u * u - v * v - w * w
            if negative_center_minimum is None or determinant < negative_center_minimum:
                negative_center_minimum = determinant
                negative_center_argmin = (center, y, z, u, v, w)
    assert negative_center_minimum == Q(161, 1600)

    # At depth 9/20 the only nontrivial common-center bound used here is 15.
    cumulative_45 = set(LOW_EDGES | classes[2])
    cumulative_adjacency = adjacency(cumulative_45)
    maximum_common_45 = max(
        len(cumulative_adjacency[i] & cumulative_adjacency[j])
        for i, j in combinations(range(N), 2)
    )
    assert maximum_common_45 == 8

    # This is intentionally not a full three-point witness.  Record an exact
    # failing minor so that its scope cannot silently expand.
    failing_labels = (
        labels[(0, 1)],
        labels[(0, 2)],
        labels[(1, 2)],
    )
    assert failing_labels == (Q(99, 200), Q(99, 200), Q(-157, 200))
    failing_determinant = (
        1
        + 2 * failing_labels[0] * failing_labels[1] * failing_labels[2]
        - sum(value * value for value in failing_labels)
    )
    assert failing_determinant == Q(-1963857, 4000000)

    # Exact two-point Gegenbauer positivity.
    check_degree = 103
    values = [zonal_values(node, check_degree) for node in NODES]
    moments_unnormalized = [
        Q(N)
        + sum(
            ORDERED_COUNTS[i] * values[i][degree]
            for i in range(len(NODES))
        )
        for degree in range(1, check_degree + 1)
    ]
    moment_minimum = min(
        (value, degree)
        for degree, value in enumerate(moments_unnormalized, 1)
    )
    assert moment_minimum == (Q(30261, 16000), 2)

    # All 1-t_i^2 are at least 15351/40000 and hence have inverse
    # three-halves power <17/4.  Combined with the analytic constant <31/5
    # from the two-point barrier gives an off-diagonal tail <1054/k^(3/2).
    q_minimum = Q(15351, 40000)
    assert min(1 - node * node for node in NODES) == q_minimum
    assert q_minimum**3 > Q(4, 17) ** 2
    assert Q(31, 5) * Q(17, 4) * (N - 1) == 1054
    assert 1054**2 < 104**3

    return {
        "pair_classes": tuple(map(len, classes)),
        "distance_two_pairs": len(distance_two),
        "maximum_common_at_9_over_20": maximum_common_45,
        "maximum_pfender_row": max(row_values),
        "negative_center_minimum": negative_center_minimum,
        "negative_center_argmin": negative_center_argmin,
        "failing_triple_determinant": failing_determinant,
        "minimum_moment_unnormalized": moment_minimum[0],
        "minimum_moment_degree": moment_minimum[1],
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
