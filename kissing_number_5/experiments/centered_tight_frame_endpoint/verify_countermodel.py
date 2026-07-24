#!/usr/bin/env python3
"""Exact verifier for the centered-endpoint triangle-PSD countermodel.

Only the Python standard library is used.  Every matrix and polynomial
calculation is in fractions.Fraction arithmetic.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "circulant_triangle_psd_countermodel.json"
Q = Fraction


def determinant(matrix: list[list[Q]]) -> Q:
    work = [row[:] for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        diagonal = work[column][column]
        answer *= diagonal
        for j in range(column + 1, len(work)):
            work[column][j] /= diagonal
        for row in range(column + 1, len(work)):
            multiplier = work[row][column]
            for j in range(column + 1, len(work)):
                work[row][j] -= multiplier * work[column][j]
    return answer


def gegenbauer_value(degree: int, t: Q) -> Q:
    """Dimension-five normalized Gegenbauer polynomial P_degree(t)."""

    if degree == 0:
        return Q(1)
    previous = Q(1)
    current = t
    for k in range(1, degree):
        previous, current = (
            current,
            Q(2 * k + 3, k + 3) * t * current
            - Q(k, k + 3) * previous,
        )
    return current


def main() -> None:
    data = json.loads(CERTIFICATE.read_text())
    assert data["schema"].endswith("countermodel-v1")
    n = data["order"]
    assert n == 41
    distance_values = [Q(value) for value in data["circulant_distance_values"]]
    assert len(distance_values) == (n - 1) // 2

    def distance_class(i: int, j: int) -> int:
        difference = (i - j) % n
        return min(difference, n - difference) - 1

    def entry(i: int, j: int) -> Q:
        return Q(1) if i == j else distance_values[distance_class(i, j)]

    gram = [[entry(i, j) for j in range(n)] for i in range(n)]
    assert all(gram[i][j] == gram[j][i] for i in range(n) for j in range(n))
    assert all(gram[i][i] == 1 for i in range(n))
    assert all(
        gram[i][j] <= Q(1, 2)
        for i in range(n)
        for j in range(n)
        if i != j
    )
    assert all(
        gram[i][j] >= -1
        for i in range(n)
        for j in range(n)
        if i != j
    )

    expected_multiset = sorted(
        value
        for value_text, multiplicity in data["off_diagonal_multiplicities"]
        for value in [Q(value_text)] * multiplicity
    )
    assert len(expected_multiset) == n - 1
    for row in range(n):
        off = sorted(gram[row][j] for j in range(n) if j != row)
        assert off == expected_multiset
        assert sum(off) == -1
        assert sum(value * value for value in off) == Q(36, 5)
        assert sum(gram[row]) == 0
        assert sum(value * value for value in gram[row]) == Q(41, 5)

    # The Lorentzian/nonnegative transform has the exact endpoint diagonal
    # and row moments, although its off-diagonal square identity is absent.
    b = [
        [
            (Q(1) if i == j else Q(0)) + Q(1) - 2 * gram[i][j]
            for j in range(n)
        ]
        for i in range(n)
    ]
    assert all(b[i][i] == 0 for i in range(n))
    assert all(value >= 0 for row in b for value in row)
    assert all(sum(row) == 42 for row in b)
    assert all(sum(value * value for value in row) == Q(364, 5) for row in b)

    # Every principal submatrix of order at most three is PSD.  For a real
    # symmetric 3-by-3 matrix this is equivalent to nonnegative principal
    # minors, and the order-one/two cases follow from |g_ij| <= 1.
    triangle_determinants: list[Q] = []
    for indices in combinations(range(n), 3):
        minor = [[gram[i][j] for j in indices] for i in indices]
        value = determinant(minor)
        triangle_determinants.append(value)
        assert value >= 0
    assert min(triangle_determinants) == 0

    # The matrix is nevertheless not PSD: this exact order-four principal
    # minor is negative.  This is the explicit boundary between what the
    # artifact does and does not certify.
    witness = data["negative_principal_minor_witness"]
    indices = witness["indices_zero_based"]
    minor = [[gram[i][j] for j in indices] for i in indices]
    witness_determinant = determinant(minor)
    assert witness_determinant == Q(witness["determinant"]) == Q(-27, 16)

    # Every ordinary Delsarte all-ones inequality holds.  Degrees through
    # 89 are checked directly.  For the tail, use
    #
    #   P_k(t) = 2 L'_{k+1}(t) / ((k+1)(k+2))
    #
    # and Bernstein's inequality
    #   sqrt(1-t^2)|L'_{k+1}(t)| <= k+1,
    # hence |P_k(t)| <= 2/((k+2)sqrt(1-t^2)).
    exact_harmonic_sums: list[Q] = []
    for degree in range(90):
        value = Q(1) + sum(
            multiplicity * gegenbauer_value(degree, Q(node))
            for node, multiplicity in data["off_diagonal_multiplicities"]
        )
        exact_harmonic_sums.append(value)
        assert value >= 0
    assert exact_harmonic_sums[1] == 0
    assert exact_harmonic_sums[2] == 0
    assert min(exact_harmonic_sums[3:]) > 0

    reciprocal_sqrt_upper_bounds = {
        Q(-4, 5): Q(5, 3),
        Q(-3, 4): Q(8, 5),
        Q(-1, 2): Q(7, 6),
        Q(-7, 20): Q(15, 14),
        Q(-3, 10): Q(21, 20),
        Q(-1, 4): Q(21, 20),
        Q(-3, 20): Q(51, 50),
        Q(-1, 20): Q(501, 500),
        Q(0): Q(1),
        Q(3, 10): Q(21, 20),
        Q(1, 2): Q(7, 6),
    }
    for node, upper in reciprocal_sqrt_upper_bounds.items():
        assert upper * upper * (1 - node * node) >= 1
    weight_sum = sum(
        multiplicity * reciprocal_sqrt_upper_bounds[Q(node)]
        for node, multiplicity in data["off_diagonal_multiplicities"]
    )
    assert weight_sum == Q(
        data["ordinary_harmonic_audit"]["bernstein_derivative_bound_weight_sum"]
    )
    assert 2 * weight_sum == Q(
        data["ordinary_harmonic_audit"][
            "strict_tail_numerator_twice_weight_sum"
        ]
    )
    assert 2 * weight_sum < 92
    # Consequently, for every k >= 90,
    # 1 + sum c_t P_k(t) >= 1 - 2*weight_sum/(k+2) > 0.

    counts = data["degree_counts"]
    assert sum(value < 0 for value in expected_multiset) == counts[
        "strictly_negative"
    ]
    assert sum(value > 0 for value in expected_multiset) == counts[
        "strictly_positive"
    ]
    assert sum(value == 0 for value in expected_multiset) == counts["zero"]
    assert sum(value == Q(1, 2) for value in expected_multiset) == counts[
        "contact_inner_product_one_half"
    ]
    assert sum(value < Q(-1, 300) for value in expected_multiset) == counts[
        "below_minus_one_over_300"
    ]
    assert sum(value > Q(1, 300) for value in expected_multiset) == counts[
        "above_one_over_300"
    ]

    print(
        {
            "order": n,
            "triangle_count": len(triangle_determinants),
            "minimum_triangle_determinant": str(min(triangle_determinants)),
            "negative_order_four_witness": str(witness_determinant),
            "minimum_exact_harmonic_sum_degrees_3_to_89": str(
                min(exact_harmonic_sums[3:])
            ),
            "all_higher_harmonic_sums_strictly_positive": True,
            "row_sum": str(sum(gram[0])),
            "row_square_sum": str(
                sum(value * value for value in gram[0])
            ),
        }
    )


if __name__ == "__main__":
    main()
