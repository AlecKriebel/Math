#!/usr/bin/env python3
"""Exact all-threshold audit of the 120-vector golden family.

For a nonantipodal inner-product value ``t``, an admissible set contains no
pair with inner product below ``t``; its threshold graph joins pairs with
inner product exactly ``t``.  This script eliminates all seven possible
values.  Five values are handled by explicit colorings of the full relation
graph.  At the remaining values 0 and 8, every maximal admissible set is
enumerated by Bron--Kerbosch and its threshold graph is colored by complete
DSATUR backtracking.

All coordinates and comparisons are exact in Z[sqrt(5)].  No optional
package or external solver is used.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
from typing import Sequence


Quadratic = tuple[int, int]  # a+b*sqrt(5)
Point = tuple[Quadratic, Quadratic, Quadratic, Quadratic]


def qmul(x: Quadratic, y: Quadratic) -> Quadratic:
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def qsub(x: Quadratic, y: Quadratic) -> Quadratic:
    return (x[0] - y[0], x[1] - y[1])


def qsign(x: Quadratic) -> int:
    """Exact sign in the positive real embedding of Q(sqrt(5))."""
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    comparison = a * a - 5 * b * b
    assert comparison != 0  # 5 is not a rational square.
    return (1 if a > 0 else -1) * ((comparison > 0) - (comparison < 0))


def qdot(x: Point, y: Point) -> Quadratic:
    rational = 0
    radical = 0
    for a, b in zip(x, y):
        product = qmul(a, b)
        rational += product[0]
        radical += product[1]
    return (rational, radical)


def negate(x: Point) -> Point:
    return tuple((-a, -b) for a, b in x)  # type: ignore[return-value]


def permutation_parity(permutation: Sequence[int]) -> int:
    return sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    ) % 2


def golden_vectors_scaled_by_four() -> list[Point]:
    points: list[Point] = []
    zero = (0, 0)
    for coordinate in range(4):
        for sign in (-1, 1):
            point = [zero] * 4
            point[coordinate] = (4 * sign, 0)
            points.append(tuple(point))  # type: ignore[arg-type]
    for signs in itertools.product((-1, 1), repeat=4):
        points.append(tuple((2 * sign, 0) for sign in signs))  # type: ignore[arg-type]

    base: Point = ((0, 0), (2, 0), (1, 1), (-1, 1))
    for permutation in itertools.permutations(range(4)):
        if permutation_parity(permutation):
            continue
        permuted = tuple(base[permutation[i]] for i in range(4))
        nonzero = [i for i, value in enumerate(permuted) if value != zero]
        for signs in itertools.product((-1, 1), repeat=3):
            point = list(permuted)
            for coordinate, sign in zip(nonzero, signs):
                a, b = point[coordinate]
                point[coordinate] = (sign * a, sign * b)
            points.append(tuple(point))  # type: ignore[arg-type]

    answer = sorted(set(points))
    assert len(answer) == 120
    assert {qdot(point, point) for point in answer} == {(16, 0)}
    return answer


def canonical_lines(points: Sequence[Point]) -> list[Point]:
    seen: set[Point] = set()
    lines: list[Point] = []
    for point in points:
        if point in seen:
            continue
        opposite = negate(point)
        assert opposite in points
        seen.update((point, opposite))
        lines.append(max(point, opposite))
    assert len(lines) == 60
    return lines


# Ordered from the smallest to largest nonantipodal value in the positive
# embedding 2<sqrt(5)<3.
THRESHOLDS: list[Quadratic] = [
    (-4, -4),
    (-8, 0),
    (4, -4),
    (0, 0),
    (-4, 4),
    (8, 0),
    (4, 4),
]


# Colors the projective |dot|=4+4sqrt(5) relation, and therefore both full
# oriented relation graphs at its positive and negative values.
ALPHA_LINE_COLORING = [
    3, 4, 3, 0, 0, 1, 3, 3, 0, 4, 3, 3, 1, 1, 3, 3, 2, 4, 2, 3,
    2, 4, 0, 0, 0, 4, 2, 1, 2, 1, 2, 4, 1, 4, 1, 1, 0, 4, 1, 0,
    0, 2, 2, 4, 2, 4, 4, 3, 1, 4, 1, 3, 0, 0, 2, 3, 2, 1, 2, 0,
]


# Colors the projective |dot|=4sqrt(5)-4 relation, and therefore both signs
# of that relation on all 120 oriented vectors.
BETA_LINE_COLORING = [
    3, 1, 4, 3, 4, 3, 4, 2, 3, 1, 3, 3, 2, 3, 0, 2, 3, 1, 3, 0,
    0, 1, 2, 2, 4, 1, 4, 2, 4, 0, 0, 1, 0, 1, 4, 4, 4, 1, 2, 0,
    0, 2, 0, 1, 2, 1, 1, 2, 3, 1, 0, 0, 3, 2, 2, 4, 3, 4, 4, 0,
]


# Colors the full oriented dot=-8 relation.  Unlike the preceding two
# certificates, this coloring does not descend to antipodal lines.
NEGATIVE_EIGHT_ORIENTED_COLORING = [
    3, 2, 2, 4, 4, 3, 1, 4, 2, 2, 2, 4, 4, 3, 3, 3, 4, 3, 1, 3,
    1, 2, 4, 0, 2, 0, 1, 0, 4, 0, 1, 1, 4, 2, 3, 3, 3, 3, 4, 3,
    2, 2, 4, 3, 3, 2, 0, 4, 2, 2, 3, 1, 3, 4, 2, 2, 4, 4, 2, 3,
    1, 4, 1, 3, 1, 3, 2, 2, 4, 4, 3, 1, 3, 1, 1, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 1, 0, 2, 4, 2, 2, 3, 1, 3, 4, 3, 1, 1, 4, 0,
    2, 0, 4, 0, 1, 4, 2, 2, 0, 4, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0,
]


def dot_table(points: Sequence[Point]) -> list[list[Quadratic]]:
    table = [[(16, 0)] * len(points) for _ in points]
    for i in range(len(points)):
        for j in range(i):
            table[i][j] = table[j][i] = qdot(points[i], points[j])
    return table


def relation_masks(table: Sequence[Sequence[Quadratic]], target: Quadratic) -> list[int]:
    return [
        sum(1 << j for j in range(len(table)) if j != i and table[i][j] == target)
        for i in range(len(table))
    ]


def compatibility_masks(
    table: Sequence[Sequence[Quadratic]], threshold: Quadratic
) -> list[int]:
    return [
        sum(
            1 << j
            for j in range(len(table))
            if j != i and qsign(qsub(table[i][j], threshold)) >= 0
        )
        for i in range(len(table))
    ]


def projective_point_colors(
    points: Sequence[Point], lines: Sequence[Point], line_colors: Sequence[int]
) -> list[int]:
    assert len(lines) == len(line_colors) == 60
    color_by_line = {line: line_colors[i] for i, line in enumerate(lines)}
    return [color_by_line[max(point, negate(point))] for point in points]


def verify_relation_coloring(
    masks: Sequence[int], colors: Sequence[int], color_count: int = 5
) -> None:
    assert len(masks) == len(colors)
    assert set(colors) <= set(range(color_count))
    for i, neighbors in enumerate(masks):
        while neighbors:
            bit = neighbors & -neighbors
            j = bit.bit_length() - 1
            assert colors[i] != colors[j]
            neighbors ^= bit


def exact_k_coloring(adjacency: Sequence[set[int]], k: int) -> list[int] | None:
    """Complete deterministic DSATUR backtracking."""
    colors = [-1] * len(adjacency)

    def search(colored: int, used: int) -> bool:
        if colored == len(adjacency):
            return True
        vertex = max(
            (v for v in range(len(adjacency)) if colors[v] < 0),
            key=lambda v: (
                len({colors[w] for w in adjacency[v] if colors[w] >= 0}),
                sum(colors[w] < 0 for w in adjacency[v]),
                len(adjacency[v]),
                v,
            ),
        )
        forbidden = {colors[w] for w in adjacency[vertex] if colors[w] >= 0}
        choices = [color for color in range(used) if color not in forbidden]
        if used < k and used not in forbidden:
            choices.append(used)
        for color in choices:
            colors[vertex] = color
            if search(colored + 1, max(used, color + 1)):
                return True
            colors[vertex] = -1
        return False

    if not search(0, 0):
        return None
    assert max(colors, default=-1) < k
    assert all(colors[i] != colors[j] for i in range(len(colors)) for j in adjacency[i])
    return colors


def maximal_cliques(adjacency_masks: Sequence[int]) -> list[tuple[int, ...]]:
    """Enumerate every maximal clique exactly by Bron--Kerbosch with pivoting."""
    n = len(adjacency_masks)
    answer: list[tuple[int, ...]] = []

    def search(chosen: tuple[int, ...], candidates: int, excluded: int) -> None:
        nonlocal answer
        if not candidates and not excluded:
            answer.append(tuple(sorted(chosen)))
            return
        possible_pivots = candidates | excluded
        if possible_pivots:
            pivot = max(
                (v for v in range(n) if (possible_pivots >> v) & 1),
                key=lambda v: (candidates & adjacency_masks[v]).bit_count(),
            )
            extensions = candidates & ~adjacency_masks[pivot]
        else:
            extensions = candidates
        while extensions:
            bit = extensions & -extensions
            vertex = bit.bit_length() - 1
            search(
                chosen + (vertex,),
                candidates & adjacency_masks[vertex],
                excluded & adjacency_masks[vertex],
            )
            candidates ^= bit
            excluded |= bit
            extensions ^= bit

    search((), (1 << n) - 1, 0)
    answer.sort()
    assert len(answer) == len(set(answer))
    return answer


def clique_digest(cliques: Sequence[tuple[int, ...]]) -> str:
    encoding = ";".join(",".join(map(str, clique)) for clique in cliques).encode()
    return hashlib.sha256(encoding).hexdigest()


def induced_adjacency(vertices: Sequence[int], relation: Sequence[int]) -> list[set[int]]:
    local_index = {vertex: i for i, vertex in enumerate(vertices)}
    answer = [set() for _ in vertices]
    for i, vertex in enumerate(vertices):
        neighbors = relation[vertex]
        for other, j in local_index.items():
            if (neighbors >> other) & 1:
                answer[i].add(j)
    return answer


def audit_constrained_threshold(
    table: Sequence[Sequence[Quadratic]],
    threshold: Quadratic,
    expected_sizes: collections.Counter[int],
    expected_chromatic: collections.Counter[int],
    expected_digest: str,
) -> tuple[int, collections.Counter[int], collections.Counter[int]]:
    compatibility = compatibility_masks(table, threshold)
    relation = relation_masks(table, threshold)
    cliques = maximal_cliques(compatibility)
    assert collections.Counter(map(len, cliques)) == expected_sizes
    assert clique_digest(cliques) == expected_digest

    chromatic = collections.Counter()
    all_vertices = (1 << len(table)) - 1
    for clique in cliques:
        clique_mask = sum(1 << vertex for vertex in clique)
        # Independent direct checks of admissibility and maximality.
        for vertex in clique:
            assert (clique_mask ^ (1 << vertex)) & ~compatibility[vertex] == 0
        outside = all_vertices ^ clique_mask
        while outside:
            bit = outside & -outside
            vertex = bit.bit_length() - 1
            assert clique_mask & ~compatibility[vertex]
            outside ^= bit

        adjacency = induced_adjacency(clique, relation)
        coloring = None
        for k in range(1, 5):
            coloring = exact_k_coloring(adjacency, k)
            if coloring is not None:
                chromatic[k] += 1
                break
        assert coloring is not None

    assert chromatic == expected_chromatic
    return len(cliques), collections.Counter(map(len, cliques)), chromatic


def verify() -> None:
    points = golden_vectors_scaled_by_four()
    lines = canonical_lines(points)
    table = dot_table(points)

    assert all(qsign(qsub(second, first)) > 0 for first, second in zip(THRESHOLDS, THRESHOLDS[1:]))
    nonantipodal_spectrum = {
        table[i][j]
        for i in range(len(points))
        for j in range(i)
        if points[j] != negate(points[i])
    }
    assert nonantipodal_spectrum == set(THRESHOLDS)

    relation_edge_counts = {}
    relation_degrees = {}
    for threshold in THRESHOLDS:
        relation = relation_masks(table, threshold)
        relation_edge_counts[threshold] = sum(mask.bit_count() for mask in relation) // 2
        relation_degrees[threshold] = {mask.bit_count() for mask in relation}
    assert relation_edge_counts == {
        (-4, -4): 720,
        (-8, 0): 1200,
        (4, -4): 720,
        (0, 0): 1800,
        (-4, 4): 720,
        (8, 0): 1200,
        (4, 4): 720,
    }
    assert relation_degrees == {
        (-4, -4): {12},
        (-8, 0): {20},
        (4, -4): {12},
        (0, 0): {30},
        (-4, 4): {12},
        (8, 0): {20},
        (4, 4): {12},
    }

    alpha_colors = projective_point_colors(points, lines, ALPHA_LINE_COLORING)
    beta_colors = projective_point_colors(points, lines, BETA_LINE_COLORING)
    for threshold in ((-4, -4), (4, 4)):
        verify_relation_coloring(relation_masks(table, threshold), alpha_colors)
    for threshold in ((4, -4), (-4, 4)):
        verify_relation_coloring(relation_masks(table, threshold), beta_colors)
    verify_relation_coloring(
        relation_masks(table, (-8, 0)), NEGATIVE_EIGHT_ORIENTED_COLORING
    )

    zero_result = audit_constrained_threshold(
        table,
        (0, 0),
        collections.Counter({20: 28800, 17: 1200}),
        collections.Counter({4: 20400, 3: 9600}),
        "5ea861917eac9194187f318d6a8532176c5910f5a72dd375b1583d696a025e9a",
    )
    eight_result = audit_constrained_threshold(
        table,
        (8, 0),
        collections.Counter({7: 4560, 8: 600}),
        collections.Counter({3: 3120, 4: 2040}),
        "4df9a77b669f57950df62644be0272a3f4574d4ee3ab5c45ac2f052b6406b117",
    )

    print("H4 golden all-threshold exact audit passed")
    print("thresholds=" + repr(THRESHOLDS))
    print("full_relation_five_colored=[(-4,-4),(-8,0),(4,-4),(-4,4),(4,4)]")
    print(
        "threshold=(0,0) maximal_admissible_sets="
        f"{zero_result[0]} sizes={dict(zero_result[1])} chi={dict(zero_result[2])}"
    )
    print(
        "threshold=(8,0) maximal_admissible_sets="
        f"{eight_result[0]} sizes={dict(eight_result[1])} chi={dict(eight_result[2])}"
    )
    print("non_5_colorable_admissible_threshold_graphs=0")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="run the exact audit (default)")
    return parser.parse_args()


def main() -> None:
    parse_args()
    verify()


if __name__ == "__main__":
    main()
