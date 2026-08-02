#!/usr/bin/env python3
"""Exact constants for universal_vertex_acute_s3.md.

The geometric arguments remain in the note.  This dependency-free checker
verifies the quadratic-surd endpoints, the tetrahedral counterexamples, the
sharp support Gram inverse, the regular-support polar-cell calculation, and
the rational bounds used by the core-coloring and distorted-support
arguments.
"""

from __future__ import annotations

from fractions import Fraction as Q


Pair = tuple[Q, Q]  # a+b*sqrt(d), with d passed separately


def add(x: Pair, y: Pair) -> Pair:
    return (x[0] + y[0], x[1] + y[1])


def subtract(x: Pair, y: Pair) -> Pair:
    return (x[0] - y[0], x[1] - y[1])


def multiply(x: Pair, y: Pair, d: int) -> Pair:
    return (x[0] * y[0] + d * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def sign(x: Pair, d: int) -> int:
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    comparison = a * a - d * b * b
    assert comparison != 0
    return (1 if a > 0 else -1) * ((comparison > 0) - (comparison < 0))


def matrix_multiply(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(a))), Q(0)) for j in range(len(a))]
        for i in range(len(a))
    ]


Polynomial = tuple[Q, ...]  # coefficients in ascending order


def polynomial_add(a: Polynomial, b: Polynomial) -> Polynomial:
    degree = max(len(a), len(b))
    return tuple(
        (a[i] if i < len(a) else Q(0)) + (b[i] if i < len(b) else Q(0))
        for i in range(degree)
    )


def polynomial_scale(a: Polynomial, scalar: Q) -> Polynomial:
    return tuple(scalar * coefficient for coefficient in a)


def polynomial_multiply(a: Polynomial, b: Polynomial) -> Polynomial:
    result = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return tuple(result)


def rational_dot(x: tuple[Q, ...], y: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(x, y)), Q(0))


def verify_closest_cap_and_high_regime() -> None:
    c = Q(1, 2)
    closest_cap_sq = c + (1 - c) / 4
    assert closest_cap_sq == Q(5, 8)

    # H=(1+sqrt(3))/4 is the exact solution of
    # H-(1-H)/sqrt(3)=1/2.
    h_sq: Pair = (Q(1, 4), Q(1, 4))
    one_minus_h: Pair = (Q(3, 4), Q(-1, 4))
    inverse_sqrt_three: Pair = (Q(0), Q(1, 3))
    endpoint = subtract(h_sq, multiply(one_minus_h, inverse_sqrt_three, 3))
    assert endpoint == (Q(1, 2), Q(0))
    assert sign(subtract(h_sq, (closest_cap_sq, Q(0))), 3) > 0


def verify_tetrahedral_geometry_and_naive_failure() -> None:
    # Regular tetrahedron numerators; every vector is divided by sqrt(3).
    tetra = [
        (1, 1, 1),
        (1, -1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
    ]

    def integer_dot(x: tuple[int, int, int], y: tuple[int, int, int]) -> int:
        return sum(a * b for a, b in zip(x, y))

    assert {
        Q(integer_dot(tetra[i], tetra[j]), 3)
        for i in range(4)
        for j in range(i)
    } == {Q(-1, 3)}
    assert tuple(sum(tetra[i][j] for i in range(4)) for j in range(3)) == (0, 0, 0)

    # In the Voronoi cell of t_0, u=e_3 and v=-t_3 both occur.  Their
    # inner product is -1/sqrt(3), strictly below -1/3.
    u = (0, 0, 1)
    v_numerator = tuple(-coordinate for coordinate in tetra[3])
    u_scores = [integer_dot(u, vertex) for vertex in tetra]  # common /sqrt(3)
    v_scores = [Q(integer_dot(v_numerator, vertex), 3) for vertex in tetra]
    assert u_scores[0] == max(u_scores)
    assert v_scores[0] == max(v_scores)
    uv_numerator = integer_dot(u, v_numerator)
    assert uv_numerator == -1
    assert Q(uv_numerator * uv_numerator, 3) == Q(1, 3)

    # The guaranteed cap endpoint turns this cell pair into an inner product
    # (5-sqrt(3))/8, which is below 1/2.
    cap_pair: Pair = (Q(5, 8), Q(-1, 8))
    assert sign(subtract(cap_pair, (Q(1, 2), Q(0))), 3) < 0

    # Exact K4 defeating lexicographic nearest-tetra tie-breaking: use the
    # opposite tetrahedron as transverse support at the sharp cap endpoint.
    # All lifted off-diagonal products are 1/2.
    lifted_off_diagonal = Q(5, 8) + Q(3, 8) * Q(-1, 3)
    assert lifted_off_diagonal == Q(1, 2)
    opposite = [tuple(-coordinate for coordinate in vertex) for vertex in tetra]
    lexicographic_colors = []
    for point in opposite:
        scores = [integer_dot(point, vertex) for vertex in tetra]
        maximum = max(scores)
        lexicographic_colors.append(min(i for i, value in enumerate(scores) if value == maximum))
    assert lexicographic_colors == [1, 0, 0, 0]


def verify_tetrahedral_cell_factorization() -> None:
    # D(t,s), viewed as a quadratic in t, has coefficients A(s), B(s), C(s).
    a: Polynomial = (Q(24), Q(-64), Q(16))
    b: Polynomial = (Q(-24), Q(88), Q(-64))
    c: Polynomial = (Q(6), Q(-24), Q(24))
    discriminant = polynomial_add(
        polynomial_multiply(b, b),
        polynomial_scale(polynomial_multiply(a, c), Q(-4)),
    )
    factored = polynomial_scale(
        polynomial_multiply(
            polynomial_multiply((Q(0), Q(1)), (Q(-2), Q(5))),
            (Q(3), Q(-8), Q(8)),
        ),
        Q(64),
    )
    assert discriminant == factored

    # a0=2-sqrt(10)/2 is the smaller zero of 2s^2-8s+3 and lies
    # strictly between 2/5 and 1.  This is the exact breakpoint used in
    # the convex/concave split.
    a0: Pair = (Q(2), Q(-1, 2))
    a0_squared = multiply(a0, a0, 10)
    breakpoint_polynomial = add(
        add((2 * a0_squared[0], 2 * a0_squared[1]), (-8 * a0[0], -8 * a0[1])),
        (Q(3), Q(0)),
    )
    assert breakpoint_polynomial == (Q(0), Q(0))
    assert sign(subtract(a0, (Q(2, 5), Q(0))), 10) > 0
    assert sign(subtract((Q(1), Q(0)), a0), 10) > 0
    assert (-8) ** 2 - 4 * 8 * 3 == -32


def verify_sharp_support_algebra() -> None:
    # Gram matrix of four unit contacts with mutual product 1/2.
    gram = [[Q(1) if i == j else Q(1, 2) for j in range(4)] for i in range(4)]
    inverse = [
        [2 * (Q(1) if i == j else Q(0)) - Q(2, 5) for j in range(4)]
        for i in range(4)
    ]
    assert matrix_multiply(gram, inverse) == [
        [Q(1) if i == j else Q(0) for j in range(4)] for i in range(4)
    ]

    # r is confined by r^2+10r-15<=0, hence
    # R=2sqrt(10)-5.  The rational upper bound R<7/5 is used to get an
    # uncomplicated uniform core margin.
    maximum_r: Pair = (Q(-5), Q(2))
    polynomial = add(
        add(multiply(maximum_r, maximum_r, 10), (Q(0), Q(0))),
        add((Q(10) * maximum_r[0], Q(10) * maximum_r[1]), (Q(-15), Q(0))),
    )
    assert polynomial == (Q(0), Q(0))
    assert sign(subtract((Q(7, 5), Q(0)), maximum_r), 10) > 0

    # 3/sqrt(5)-1 < 5/14.  Together with R<7/5 this yields
    # R(3/sqrt(5)-1)<1/2 and hence every core coordinate s_i>1/2.
    coefficient_gap: Pair = (Q(19, 14), Q(-3, 5))
    assert sign(coefficient_gap, 5) > 0
    assert Q(7, 5) * Q(5, 14) == Q(1, 2)


def verify_regular_support_partition() -> None:
    # Vertices of the cell where coordinate 0 is maximal are uniform
    # distributions on subsets containing 0, transformed by q=4p-1.
    vertices: list[tuple[Q, ...]] = []
    for mask in range(1, 16):
        if not (mask & 1):
            continue
        size = mask.bit_count()
        vertices.append(
            tuple(Q(4, size) - 1 if mask & (1 << j) else Q(-1) for j in range(4))
        )
    assert len(vertices) == 8
    assert all(sum(vertex, Q(0)) == 0 for vertex in vertices)
    assert min(rational_dot(x, y) for x in vertices for y in vertices) == Q(-4, 3)

    # The standard tetrahedron is a tight frame: after division by sqrt(3),
    # its frame operator is (4/3)I.
    tetra = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    frame_numerator = [
        [sum(vertex[i] * vertex[j] for vertex in tetra) for j in range(3)]
        for i in range(3)
    ]
    assert frame_numerator == [[4 if i == j else 0 for j in range(3)] for i in range(3)]

    # H0=(1+sqrt(3))/4 is below 25/36, hence h<5/6.  The derivative
    # polynomial 4h^2-h-2 is still negative at 5/6 and is increasing over
    # the cap-height range.
    h0: Pair = (Q(1, 4), Q(1, 4))
    assert sign(subtract((Q(25, 36), Q(0)), h0), 3) > 0
    assert 4 * Q(5, 6) ** 2 - Q(5, 6) - 2 == Q(-1, 18)
    assert 8 * Q(3, 4) - 1 > 0
    assert sign(subtract((Q(3, 4), Q(0)), h0), 3) > 0

    # The explicit same-cell margin at the sharp endpoint is 1/12.
    h_sq = Q(5, 8)
    c = Q(1, 2)
    margin = (h_sq - c) * (Q(3, 2) - 2 * h_sq) / (1 - h_sq)
    assert margin == Q(1, 12)


def verify_distorted_support_obstruction() -> None:
    h_sq = Q(17, 25)
    c = Q(1, 2)
    alpha_sq = 1 - h_sq
    transverse = [
        (Q(6, 11), Q(9, 11), Q(-2, 11)),
        (Q(-9, 17), Q(-8, 17), Q(-12, 17)),
        (Q(-12, 13), Q(0), Q(-5, 13)),
        (Q(1, 9), Q(-4, 9), Q(8, 9)),
    ]
    assert all(rational_dot(vector, vector) == 1 for vector in transverse)

    weights = tuple(Q(value, 37382) for value in (12364, 10251, 2860, 11907))
    assert sum(weights, Q(0)) == 1
    assert all(weight > 0 for weight in weights)
    assert tuple(
        sum((weights[i] * transverse[i][j] for i in range(4)), Q(0))
        for j in range(3)
    ) == (Q(0), Q(0), Q(0))

    pair_products = [
        rational_dot(transverse[i], transverse[j]) for i in range(4) for j in range(i)
    ]
    assert min(pair_products) == Q(-6, 11)
    threshold_transverse = (c - h_sq) / alpha_sq
    assert threshold_transverse == Q(-9, 16)
    assert min(pair_products) > threshold_transverse
    lifted_minimum = h_sq + alpha_sq * min(pair_products)
    assert lifted_minimum == Q(139, 275) > c

    w1 = (Q(9, 7), Q(-4, 7), Q(-6, 7))
    w2 = (Q(-11, 16), Q(5, 4), Q(9, 16))
    scores1 = tuple(rational_dot(vector, w1) for vector in transverse)
    scores2 = tuple(rational_dot(vector, w2) for vector in transverse)
    assert scores1 == (Q(30, 77), Q(23, 119), Q(-6, 7), Q(-23, 63))
    assert scores2 == (Q(6, 11), Q(-169, 272), Q(87, 208), Q(-19, 144))
    assert scores1[0] > max(scores1[1:]) and scores2[0] > max(scores2[1:])
    assert min(scores1 + scores2) >= -1
    norm1 = rational_dot(w1, w1)
    norm2 = rational_dot(w2, w2)
    assert norm1 == Q(19, 7)
    assert norm2 == Q(301, 128)
    assert rational_dot(w1, w2) == Q(-233, 112)
    polar_radius_sq = ((1 - h_sq) / (h_sq - c)) ** 2
    assert polar_radius_sq == Q(256, 81)
    assert norm1 < polar_radius_sq and norm2 < polar_radius_sq

    # Equation (23) gives these primitive integer quadratics.
    root_polynomials = [(9475, 1400, -602), (153525, 25600, -11008)]
    for norm, polynomial in zip((norm1, norm2), root_polynomials):
        quadratic = norm / (1 - h_sq) + 1 / h_sq
        linear = 1 / h_sq
        constant = c * c / h_sq - 1
        scale = quadratic / polynomial[0]
        assert linear == scale * polynomial[1]
        assert constant == scale * polynomial[2]

    intervals = [
        (Q(18878, 100000), Q(18879, 100000)),
        (Q(19707, 100000), Q(19708, 100000)),
    ]
    for polynomial, (lower, upper) in zip(root_polynomials, intervals):
        evaluate = lambda value: (
            polynomial[0] * value * value + polynomial[1] * value + polynomial[2]
        )
        assert evaluate(lower) < 0 < evaluate(upper)
        assert lower > h_sq - c

    # Positive terms use the upper endpoints and the negative product uses
    # the lower endpoints, giving a rigorous upper interval bound for Phi.
    (lower1, upper1), (lower2, upper2) = intervals
    negative_coefficient = Q(25, 8) * Q(233, 112)
    product_upper = (
        Q(25, 17) * (c + upper1) * (c + upper2)
        - negative_coefficient * lower1 * lower2
    )
    product_lower = (
        Q(25, 17) * (c + lower1) * (c + lower2)
        - negative_coefficient * upper1 * upper2
    )
    assert Q(23, 50) < product_lower < product_upper < Q(93, 200) < c


def verify_gnomonic_constants() -> None:
    # At the universally guaranteed cap, ||z||^2<=h^{-2}-1=3/5.
    h_sq = Q(5, 8)
    assert 1 / h_sq - 1 == Q(3, 5)


if __name__ == "__main__":
    verify_closest_cap_and_high_regime()
    verify_tetrahedral_geometry_and_naive_failure()
    verify_tetrahedral_cell_factorization()
    verify_sharp_support_algebra()
    verify_regular_support_partition()
    verify_distorted_support_obstruction()
    verify_gnomonic_constants()
    print("universal vertex acute-S3 constants: exact checks passed")
