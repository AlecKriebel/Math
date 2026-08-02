#!/usr/bin/env python3
"""Exact checks for the center-vector and spectral diameter obstruction.

The universal proof is analytic; this checker verifies all sharp scalar and
Gram identities and independently replays the exact unsigned-golden graph
application using the coordinate constructor from its primary certificate.
Only the Python standard library is used.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT))

from borsuk_dimension4.search.h4_signed_subset_search import (
    adjacency_from_relation,
    adjacency_matrix,
    canonical_lines,
    golden_vectors_scaled_by_four,
    matrix_multiply,
    matrix_shift,
    zero_matrix,
)


Matrix = list[list[int]]


def verify_cap_constants() -> None:
    # Extremal four-direction Gram matrix: diagonal 1, off diagonal 1/2.
    gram = [
        [Fraction(1) if i == j else Fraction(1, 2) for j in range(4)]
        for i in range(4)
    ]
    # The sum has squared norm 10 and inner product 5/2 with each vector.
    sum_squared = sum(gram[i][j] for i in range(4) for j in range(4))
    point_sum_products = [sum(gram[i]) for i in range(4)]
    assert sum_squared == 10
    assert point_sum_products == [Fraction(5, 2)] * 4
    assert point_sum_products[0] ** 2 / sum_squared == Fraction(5, 8)

    # The edge-center extremum is 1-2 alpha^2=-1/4.
    alpha_squared = Fraction(5, 8)
    assert 1 - 2 * alpha_squared == Fraction(-1, 4)

    # Caratheodory support sizes m<=4 all give at least 5/8.
    for support_size in range(1, 5):
        lower_bound = Fraction(1, 2) + Fraction(1, 2 * support_size)
        assert lower_bound >= Fraction(5, 8)


def polynomial_in_matrix(a: Matrix) -> Matrix:
    # A(A+4I)(A-5I)(A-20I), evaluated with exact integer arithmetic.
    return matrix_multiply(
        matrix_multiply(
            matrix_multiply(a, matrix_shift(a, 4)),
            matrix_shift(a, -5),
        ),
        matrix_shift(a, -20),
    )


def verify_unsigned_golden_application() -> None:
    roots = golden_vectors_scaled_by_four()
    lines = canonical_lines(roots)
    graph = adjacency_from_relation(lines, [(8, 0), (-8, 0)])
    assert len(graph) == 60
    assert {len(neighbors) for neighbors in graph} == {20}

    adjacency = adjacency_matrix(graph)
    assert sum(adjacency[i][i] for i in range(len(adjacency))) == 0
    assert zero_matrix(polynomial_in_matrix(adjacency))

    # Symmetry makes A diagonalizable; the annihilator confines every
    # eigenvalue to {-4,0,5,20}, so tau>=-4. The constant row sum gives the
    # positive eigenvalue 20, while trace(A)=0 forces a negative eigenvalue;
    # hence tau=-4. The center-vector trace bound would instead require
    # tau<=-k/4=-5.
    degree = 20
    certified_eigenvalue_lower_bound = -4
    required_upper_bound = Fraction(-degree, 4)
    assert Fraction(certified_eigenvalue_lower_bound) > required_upper_bound
    assert degree > -4 * certified_eigenvalue_lower_bound


def main() -> None:
    verify_cap_constants()
    verify_unsigned_golden_application()
    print("rank-four vector five-coloring constants verified")
    print("sharp_cap_cosine_squared=5/8 edge_center_bound=-1/4")
    print("unsigned_golden_degree=20 least_eigenvalue=-4")
    print("diameter_subgraph_necessary_bound=20<=16 contradiction")


if __name__ == "__main__":
    main()
