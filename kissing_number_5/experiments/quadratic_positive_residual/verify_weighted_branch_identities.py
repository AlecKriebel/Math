#!/usr/bin/env python3
"""Exact D5 counterexamples and weighted Gram-identity verification."""

from __future__ import annotations

from fractions import Fraction as Q
import itertools
import json


class VerificationError(Exception):
    """Raised when an exact weighted-branch check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def matrix_multiply(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                Q(0),
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matrix_add(*terms: tuple[Q, list[list[Q]]]) -> list[list[Q]]:
    size = len(terms[0][1])
    return [
        [
            sum((scale * matrix[i][j] for scale, matrix in terms), Q(0))
            for j in range(size)
        ]
        for i in range(size)
    ]


def d5_gram() -> tuple[list[tuple[int, int, int, int]], list[list[Q]]]:
    roots = [
        (i, j, first, second)
        for i in range(5)
        for j in range(i + 1, 5)
        for first, second in itertools.product((-1, 1), repeat=2)
    ]
    gram = []
    for i, j, first, second in roots:
        row = []
        for k, ell, third, fourth in roots:
            numerator = (
                (first if i == k else second if j == k else 0) * third
                + (first if i == ell else second if j == ell else 0) * fourth
            )
            row.append(Q(numerator, 2))
        gram.append(row)
    require(len(roots) == 40, "D5 root enumeration must have size 40")
    return roots, gram


def weights(
    roots: list[tuple[int, int, int, int]], delta: Q
) -> list[Q]:
    plus = {(0, 1), (2, 3)}
    minus = {(0, 2), (1, 3)}
    answer = []
    for i, j, _, _ in roots:
        value = Q(1, 40)
        if (i, j) in plus:
            value += delta
        if (i, j) in minus:
            value -= delta
        answer.append(value)
    return answer


def sparse_twelve_weights() -> list[Q]:
    heavy = {8, 10, 13, 15, 24, 26, 29, 31}
    light = {16, 17, 18, 19}
    return [
        Q(1, 10) if index in heavy else Q(1, 20) if index in light else Q(0)
        for index in range(40)
    ]


def verify_design(
    gram: list[list[Q]], p: list[Q]
) -> dict[str, object]:
    size = len(gram)
    require(len(p) == size, "weight vector has wrong length")
    require(sum(p) == 1, "weights do not sum to one")
    require(all(value >= 0 for value in p), "weights must be nonnegative")
    gp = [
        sum((gram[i][j] * p[j] for j in range(size)), Q(0))
        for i in range(size)
    ]
    require(gp == [Q(0)] * size, "weighted first moment is nonzero")
    pg = [[p[i] * gram[i][j] for j in range(size)] for i in range(size)]
    gpg = matrix_multiply(gram, pg)
    require(
        gpg == [[value / 5 for value in row] for row in gram],
        "weighted second-moment Gram identity failed",
    )

    identity = [
        [Q(1) if i == j else Q(0) for j in range(size)]
        for i in range(size)
    ]
    ones = [[Q(1) for _ in range(size)] for _ in range(size)]
    b = matrix_add((Q(1), identity), (Q(1), ones), (Q(-2), gram))
    diagonal_p = [
        [p[i] if i == j else Q(0) for j in range(size)]
        for i in range(size)
    ]
    bp = [
        sum((b[i][j] * p[j] for j in range(size)), Q(0))
        for i in range(size)
    ]
    require(bp == [1 + value for value in p], "Bp=1+p identity failed")
    bpb = matrix_multiply(matrix_multiply(b, diagonal_p), b)
    pb = matrix_multiply(diagonal_p, b)
    bp_matrix = matrix_multiply(b, diagonal_p)
    right = matrix_add(
        (Q(1), pb),
        (Q(1), bp_matrix),
        (Q(-1), diagonal_p),
        (Q(2, 5), identity),
        (Q(7, 5), ones),
        (Q(-2, 5), b),
    )
    require(bpb == right, "weighted B P B identity failed")
    return {
        "support": sum(value > 0 for value in p),
        "distinct_weights": sorted({str(value) for value in p}),
        "maximum_weight": str(max(p)),
    }


def verify() -> dict[str, object]:
    simplex_gram = [
        [Q(1) if i == j else -Q(1, 5) for j in range(6)]
        for i in range(6)
    ]
    simplex = verify_design(simplex_gram, [Q(1, 6)] * 6)
    require(simplex["support"] == 6, "simplex support is not six")
    require(simplex["maximum_weight"] == "1/6", "simplex weight is wrong")

    roots, gram = d5_gram()
    require(
        max(
            gram[i][j]
            for i in range(40)
            for j in range(40)
            if i != j
        )
        == Q(1, 2),
        "D5 Gram matrix violates the claimed kissing threshold",
    )
    full = verify_design(gram, weights(roots, Q(1, 200)))
    sparse = verify_design(gram, weights(roots, Q(1, 40)))
    sparse_twelve = verify_design(gram, sparse_twelve_weights())
    require(
        full
        == {
            "support": 40,
            "distinct_weights": ["1/40", "1/50", "3/100"],
            "maximum_weight": "3/100",
        },
        "full-support D5 weighting audit failed",
    )
    require(sparse["support"] == 32, "32-support D5 weighting audit failed")
    require(
        sparse_twelve
        == {
            "support": 12,
            "distinct_weights": ["0", "1/10", "1/20"],
            "maximum_weight": "1/10",
        },
        "12-support D5 weighting audit failed",
    )

    # Universal constants from the variance and depth arguments.
    require(Q(1, 6) < Q(1, 5), "maximum-weight comparison failed")
    require(
        (Q(1, 5) - Q(1, 50)) / (2 * (1 - Q(1, 50)))
        == Q(9, 98),
        "universal deep-mass constant is wrong",
    )
    uniform_41 = Q(1, 41)
    require(
        (1 - 6 * uniform_41) / 12 == Q(35, 492),
        "uniform one-fifth-deep-mass constant is wrong",
    )
    return {
        "status": "PASS",
        "sharp_regular_simplex": simplex,
        "full_support_nonuniform_D5": full,
        "sparse_support_D5": sparse,
        "twelve_support_D5": sparse_twelve,
        "universal_maximum_weight": "1/6",
        "universal_deep_mass": "9/98",
        "one_fifth_deep_mass_at_uniform_41": "35/492",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
