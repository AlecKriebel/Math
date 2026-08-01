#!/usr/bin/env python3
"""Exact audit of the signed 60-line golden configuration.

This file is deliberately self-contained.  Coordinates are represented in
``Z[sqrt(5)]`` as pairs ``(a,b)`` meaning ``a+b*sqrt(5)``; the geometric
vectors have merely been multiplied by four.

The key certificate is not a search over 2^60 switchings.  Put both
orientations of every line into one 120-vertex graph and join two oriented
vectors precisely when their dot product is -8.  The explicit five-coloring
below colors this entire antipodal two-cover.  Every switched 60-line graph,
and every vertex-deleted graph satisfying the longer-edge constraints, is an
induced subgraph of that one five-colored graph.

No optional packages or external SAT solver are used.
"""

from __future__ import annotations

import argparse
import collections
import itertools
from typing import Iterable, Sequence


Quadratic = tuple[int, int]  # a+b*sqrt(5)
Point = tuple[Quadratic, Quadratic, Quadratic, Quadratic]
Matrix = list[list[int]]


def qmul(x: Quadratic, y: Quadratic) -> Quadratic:
    """Multiply exactly in Z[sqrt(5)]."""
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def qsign(x: Quadratic) -> int:
    """Sign in the real embedding sqrt(5)>0, using integer arithmetic."""
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    comparison = a * a - 5 * b * b
    if comparison == 0:
        # This cannot occur nontrivially because 5 is not a rational square.
        raise AssertionError("unexpected zero in Q(sqrt(5))")
    return (1 if a > 0 else -1) * ((comparison > 0) - (comparison < 0))


def qdot(x: Point, y: Point) -> Quadratic:
    answer = (0, 0)
    for a, b in zip(x, y):
        product = qmul(a, b)
        answer = (answer[0] + product[0], answer[1] + product[1])
    return answer


def negate(x: Point) -> Point:
    return tuple((-a, -b) for a, b in x)  # type: ignore[return-value]


def permutation_parity(permutation: Sequence[int]) -> int:
    return sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    ) % 2


def golden_vectors_scaled_by_four() -> list[Point]:
    """Construct the 120 oriented vectors in a deterministic exact order."""
    points: list[Point] = []
    zero = (0, 0)

    # Four times the eight vectors +/-e_i.
    for coordinate in range(4):
        for sign in (-1, 1):
            point = [zero] * 4
            point[coordinate] = (4 * sign, 0)
            points.append(tuple(point))  # type: ignore[arg-type]

    # Four times all sixteen vectors (1/2)(+/-1,+/-1,+/-1,+/-1).
    for signs in itertools.product((-1, 1), repeat=4):
        points.append(tuple((2 * sign, 0) for sign in signs))  # type: ignore[arg-type]

    # Four times (0,1/2,phi/2,1/(2phi)), where
    # 2 phi=1+sqrt(5) and 2/phi=sqrt(5)-1.
    base: Point = ((0, 0), (2, 0), (1, 1), (-1, 1))
    even_permutations = [
        permutation
        for permutation in itertools.permutations(range(4))
        if permutation_parity(permutation) == 0
    ]
    assert len(even_permutations) == 12
    for permutation in even_permutations:
        permuted = tuple(base[permutation[i]] for i in range(4))
        nonzero = [i for i, value in enumerate(permuted) if value != zero]
        assert len(nonzero) == 3
        for signs in itertools.product((-1, 1), repeat=3):
            point = list(permuted)
            for coordinate, sign in zip(nonzero, signs):
                a, b = point[coordinate]
                point[coordinate] = (sign * a, sign * b)
            points.append(tuple(point))  # type: ignore[arg-type]

    answer = sorted(set(points))
    assert len(answer) == 120
    return answer


def canonical_lines(points: Sequence[Point]) -> list[Point]:
    """The same deterministic 60-line ordering used by route_a_orbit_search."""
    point_set = set(points)
    seen: set[Point] = set()
    lines: list[Point] = []
    for point in points:
        if point in seen:
            continue
        opposite = negate(point)
        assert opposite in point_set
        seen.update((point, opposite))
        lines.append(max(point, opposite))
    assert len(lines) == 60 and len(seen) == 120
    return lines


# Certificate for the lexicographically sorted output of
# golden_vectors_scaled_by_four().  Color labels are 0,...,4.
ORIENTED_NEGATIVE8_FIVE_COLORING = [
    3, 2, 2, 4, 4, 3, 1, 4, 2, 2, 2, 4, 4, 3, 3, 3, 4, 3, 1, 3,
    1, 2, 4, 0, 2, 0, 1, 0, 4, 0, 1, 1, 4, 2, 3, 3, 3, 3, 4, 3,
    2, 2, 4, 3, 3, 2, 0, 4, 2, 2, 3, 1, 3, 4, 2, 2, 4, 4, 2, 3,
    1, 4, 1, 3, 1, 3, 2, 2, 4, 4, 3, 1, 3, 1, 1, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 1, 0, 2, 4, 2, 2, 3, 1, 3, 4, 3, 1, 1, 4, 0,
    2, 0, 4, 0, 1, 4, 2, 2, 0, 4, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0,
]


# Independent upper-bound certificate for the unsigned 60-line |dot|=8
# graph.  Its lower bound is checked spectrally below.
UNSIGNED_LINE_SIX_COLORING = [
    2, 5, 3, 4, 5, 1, 4, 1, 0, 3, 4, 0, 0, 5, 0, 3, 5, 4, 1, 1,
    3, 1, 3, 2, 4, 0, 0, 5, 1, 3, 2, 5, 4, 1, 2, 0, 3, 3, 4, 5,
    1, 0, 4, 2, 5, 0, 4, 2, 3, 2, 2, 5, 2, 1, 4, 5, 3, 1, 2, 0,
]


def adjacency_from_relation(
    points: Sequence[Point], relation: Iterable[Quadratic]
) -> list[set[int]]:
    targets = set(relation)
    adjacency = [set() for _ in points]
    for i in range(len(points)):
        for j in range(i):
            if qdot(points[i], points[j]) in targets:
                adjacency[i].add(j)
                adjacency[j].add(i)
    return adjacency


def edge_count(adjacency: Sequence[set[int]]) -> int:
    return sum(map(len, adjacency)) // 2


def verify_coloring(adjacency: Sequence[set[int]], colors: Sequence[int], k: int) -> None:
    assert len(colors) == len(adjacency)
    assert set(colors) <= set(range(k))
    assert all(colors[i] != colors[j] for i in range(len(adjacency)) for j in adjacency[i])


def find_clique(adjacency: Sequence[set[int]], target: int) -> tuple[int, ...] | None:
    masks = [sum(1 << w for w in neighbors) for neighbors in adjacency]

    def search(chosen: tuple[int, ...], candidates: int) -> tuple[int, ...] | None:
        need = target - len(chosen)
        if need == 0:
            return chosen
        while candidates.bit_count() >= need:
            bit = candidates & -candidates
            vertex = bit.bit_length() - 1
            candidates ^= bit
            answer = search(chosen + (vertex,), candidates & masks[vertex])
            if answer is not None:
                return answer
        return None

    return search((), (1 << len(adjacency)) - 1)


def adjacency_matrix(adjacency: Sequence[set[int]]) -> Matrix:
    return [
        [int(j in adjacency[i]) for j in range(len(adjacency))]
        for i in range(len(adjacency))
    ]


def signed_relation_matrix(lines: Sequence[Point]) -> Matrix:
    answer = [[0] * len(lines) for _ in lines]
    for i in range(len(lines)):
        for j in range(i):
            value = qdot(lines[i], lines[j])
            if value in ((8, 0), (-8, 0)):
                answer[i][j] = answer[j][i] = 1 if value == (8, 0) else -1
    return answer


def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    answer = [[0] * n for _ in range(n)]
    for i, row in enumerate(a):
        for k, value in enumerate(row):
            if value:
                for j, other in enumerate(b[k]):
                    answer[i][j] += value * other
    return answer


def matrix_shift(a: Matrix, scalar: int) -> Matrix:
    """Return a+scalar*I."""
    answer = [row[:] for row in a]
    for i in range(len(a)):
        answer[i][i] += scalar
    return answer


def zero_matrix(a: Matrix) -> bool:
    return all(value == 0 for row in a for value in row)


def connected(adjacency: Sequence[set[int]]) -> bool:
    reached = {0}
    boundary = [0]
    while boundary:
        vertex = boundary.pop()
        for neighbor in adjacency[vertex] - reached:
            reached.add(neighbor)
            boundary.append(neighbor)
    return len(reached) == len(adjacency)


def verify() -> None:
    points = golden_vectors_scaled_by_four()
    point_index = {point: i for i, point in enumerate(points)}
    assert len(point_index) == 120
    assert {qdot(point, point) for point in points} == {(16, 0)}
    assert all(negate(point) in point_index for point in points)

    full_spectrum = collections.Counter(
        qdot(points[i], points[j])
        for i in range(len(points))
        for j in range(i)
    )
    assert full_spectrum == collections.Counter(
        {
            (-16, 0): 60,
            (-4, -4): 720,
            (-8, 0): 1200,
            (4, -4): 720,
            (0, 0): 1800,
            (-4, 4): 720,
            (8, 0): 1200,
            (4, 4): 720,
        }
    )
    # -(4+4sqrt(5)) is strictly below -8, while 4-4sqrt(5)>-8.
    assert qsign((4, -4)) < 0
    assert qsign((12, -4)) > 0

    oriented = adjacency_from_relation(points, [(-8, 0)])
    assert edge_count(oriented) == 1200
    assert {len(neighbors) for neighbors in oriented} == {20}
    assert collections.Counter(ORIENTED_NEGATIVE8_FIVE_COLORING) == {
        0: 24,
        1: 24,
        2: 24,
        3: 24,
        4: 24,
    }
    verify_coloring(oriented, ORIENTED_NEGATIVE8_FIVE_COLORING, 5)

    # The antipodal color pairs give a compact regularity check on the
    # certificate: every unordered pair of distinct colors labels six lines.
    antipodal_color_pairs = collections.Counter()
    for i, point in enumerate(points):
        j = point_index[negate(point)]
        assert ORIENTED_NEGATIVE8_FIVE_COLORING[i] != ORIENTED_NEGATIVE8_FIVE_COLORING[j]
        if i < j:
            antipodal_color_pairs[
                tuple(
                    sorted(
                        (
                            ORIENTED_NEGATIVE8_FIVE_COLORING[i],
                            ORIENTED_NEGATIVE8_FIVE_COLORING[j],
                        )
                    )
                )
            ] += 1
    assert antipodal_color_pairs == collections.Counter(
        {pair: 6 for pair in itertools.combinations(range(5), 2)}
    )

    lines = canonical_lines(points)
    unsigned = adjacency_from_relation(lines, [(8, 0), (-8, 0)])
    assert edge_count(unsigned) == 600
    assert {len(neighbors) for neighbors in unsigned} == {20}
    assert connected(unsigned)
    verify_coloring(unsigned, UNSIGNED_LINE_SIX_COLORING, 6)
    assert find_clique(unsigned, 4) is not None
    assert find_clique(unsigned, 5) is None

    # Exact spectral certificates.  Since the matrices are real symmetric,
    # these annihilating polynomials locate every eigenvalue at a real root.
    # Connectivity makes the 20-eigenspace of the regular unsigned graph
    # one-dimensional; trace(A)=0 and trace(A^2)=1200 then give the stated
    # multiplicities.  In particular lambda_min(A)=-4, and Hoffman's bound
    # gives alpha<=60*4/(20+4)=10 and chi>=6.
    a = adjacency_matrix(unsigned)
    unsigned_polynomial = matrix_multiply(
        matrix_multiply(matrix_multiply(a, matrix_shift(a, 4)), matrix_shift(a, -5)),
        matrix_shift(a, -20),
    )
    assert zero_matrix(unsigned_polynomial)

    signed = signed_relation_matrix(lines)
    signed_polynomial = matrix_multiply(
        matrix_multiply(signed, matrix_shift(signed, 5)), matrix_shift(signed, -10)
    )
    assert zero_matrix(signed_polynomial)
    assert sum(signed[i][j] * signed[j][i] for i in range(60) for j in range(60)) == 1200

    longer = adjacency_from_relation(lines, [(4, 4), (-4, -4)])
    assert edge_count(longer) == 360
    assert {len(neighbors) for neighbors in longer} == {12}

    print("exact signed golden-line audit passed")
    print("field=Q(sqrt(5)); coordinates_scaled_by_four=true")
    print("oriented_vectors=120 negative_8_edges=1200 degree=20")
    print("oriented_negative_8_color_class_sizes=[24,24,24,24,24]")
    print("all_2^60_switchings_five_colorable=true")
    print("all_vertex_deleted_long_edge_compatible_subsets_five_colorable=true")
    print("unsigned_lines=60 abs_8_edges=600 degree=20 clique_number=4")
    print("unsigned_spectrum={20^1,5^16,0^18,(-4)^25} chromatic_number=6")
    print("signed_spectrum={10^8,0^36,(-5)^16}")
    print("long_abs_relation_edges=360 degree=12")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="run the exact audit (default)")
    return parser.parse_args()


def main() -> None:
    parse_args()
    verify()


if __name__ == "__main__":
    main()
