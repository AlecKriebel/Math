#!/usr/bin/env python3
"""Exact verifier for the weighted common-source lemmas and barriers."""

from __future__ import annotations

from fractions import Fraction as Q
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "local_row_energy_counterexample.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def mm(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
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


def d5_roots() -> list[tuple[int, ...]]:
    roots = []
    for i, j in itertools.combinations(range(5), 2):
        for first, second in itertools.product((-1, 1), repeat=2):
            point = [0] * 5
            point[i] = first
            point[j] = second
            roots.append(tuple(point))
    return roots


def gram_from_raw(roots: list[tuple[int, ...]]) -> list[list[Q]]:
    return [
        [
            sum((left[k] * right[k] for k in range(5)), 0) / Q(2)
            for right in roots
        ]
        for left in roots
    ]


def sparse_d5_weights() -> list[Q]:
    weights = [Q(0)] * 40
    for index in (9, 11, 16, 17, 26, 27, 28, 30):
        weights[index] = Q(1, 10)
    for index in (12, 13, 14, 15):
        weights[index] = Q(1, 20)
    return weights


def verify_matrix_identities() -> dict[str, object]:
    gram = gram_from_raw(d5_roots())
    weights = sparse_d5_weights()
    size = len(gram)
    require(size == 40, "wrong D5 cardinality")
    require(sum(weights) == 1, "D5 weights do not sum to one")
    require(
        sum(value > 0 for value in weights) == 12,
        "wrong D5 support size",
    )
    require(
        max(
            gram[i][j]
            for i in range(size)
            for j in range(i)
        )
        <= Q(1, 2),
        "D5 kissing inequality failed",
    )

    gp = [
        sum((gram[i][j] * weights[j] for j in range(size)), Q(0))
        for i in range(size)
    ]
    require(gp == [Q(0)] * size, "D5 weighted centering failed")
    pg = [
        [weights[i] * gram[i][j] for j in range(size)]
        for i in range(size)
    ]
    gpg = mm(gram, pg)
    require(
        gpg == [[entry / 5 for entry in row] for row in gram],
        "D5 weighted isotropy failed",
    )

    distance = [
        [2 * (1 - gram[i][j]) for j in range(size)]
        for i in range(size)
    ]
    require(
        all(distance[i][i] == 0 for i in range(size)),
        "distance diagonal is nonzero",
    )
    require(
        all(
            1 <= distance[i][j] <= 4
            for i in range(size)
            for j in range(size)
            if i != j
        ),
        "distance entry is outside [1,4]",
    )
    dp = [
        sum((distance[i][j] * weights[j] for j in range(size)), Q(0))
        for i in range(size)
    ]
    require(dp == [Q(2)] * size, "Dp identity failed")
    pd = [
        [weights[i] * distance[i][j] for j in range(size)]
        for i in range(size)
    ]
    dpd = mm(distance, pd)
    expected_dpd = [
        [Q(24, 5) - Q(2, 5) * distance[i][j] for j in range(size)]
        for i in range(size)
    ]
    require(dpd == expected_dpd, "DPD identity failed")

    # Similarity-free verification of the transition polynomial.
    transition = [
        [distance[i][j] * weights[j] / 2 for j in range(size)]
        for i in range(size)
    ]
    transition_square = mm(transition, transition)
    expected_square = [
        [
            Q(6, 5) * weights[j] - transition[i][j] / 5
            for j in range(size)
        ]
        for i in range(size)
    ]
    require(
        transition_square == expected_square,
        "transition quadratic identity failed",
    )
    require(
        all(sum(row, Q(0)) == 1 for row in transition),
        "transition matrix is not stochastic",
    )

    # The rational stress matrix and representative consequences.
    omega = [
        [
            (weights[i] if i == j else Q(0))
            - weights[i] * weights[j]
            - 5 * weights[i] * weights[j] * gram[i][j]
            for j in range(size)
        ]
        for i in range(size)
    ]
    require(
        all(sum(row, Q(0)) == 0 for row in omega),
        "stress row sum failed",
    )
    require(
        all(
            omega[i][i] == weights[i] * (1 - 6 * weights[i])
            for i in range(size)
        ),
        "stress diagonal failed",
    )
    for i, j in itertools.combinations(range(size), 2):
        require(
            (
                weights[i]
                * weights[j]
                * (1 + 5 * gram[i][j]) ** 2
                <= (1 - 6 * weights[i]) * (1 - 6 * weights[j])
            ),
            f"pair stress inequality failed at {(i, j)}",
        )

    # All support sizes 6,...,10 occur via orthogonal simplex blocks.
    simplex_supports = []
    for components in range(1, 6):
        partition = [1] * (components - 1) + [6 - components]
        block_weights = []
        block_gram = []
        labels = []
        for block, dimension in enumerate(partition):
            weight = Q(dimension, 5 * (dimension + 1))
            for _ in range(dimension + 1):
                block_weights.append(weight)
                labels.append((block, dimension))
        for block_i, dimension_i in labels:
            row = []
            seen_in_block = 0
            for block_j, dimension_j in labels:
                if block_i != block_j:
                    row.append(Q(0))
                else:
                    # Diagonal positions are located by the running row
                    # index, so fill below after constructing block data.
                    row.append(Q(-1, dimension_i))
            block_gram.append(row)
        for i in range(len(labels)):
            block_gram[i][i] = Q(1)
        require(
            len(block_weights) == 5 + components,
            "wrong orthogonal-simplex support size",
        )
        require(
            sum(block_weights) == 1,
            "orthogonal-simplex weights do not sum to one",
        )
        block_gp = [
            sum(
                (
                    block_gram[i][j] * block_weights[j]
                    for j in range(len(labels))
                ),
                Q(0),
            )
            for i in range(len(labels))
        ]
        require(
            block_gp == [Q(0)] * len(labels),
            "orthogonal-simplex centering failed",
        )
        block_pg = [
            [
                block_weights[i] * block_gram[i][j]
                for j in range(len(labels))
            ]
            for i in range(len(labels))
        ]
        require(
            mm(block_gram, block_pg)
            == [[entry / 5 for entry in row] for row in block_gram],
            "orthogonal-simplex isotropy failed",
        )
        simplex_supports.append(len(labels))
    require(
        simplex_supports == [6, 7, 8, 9, 10],
        "support-size portfolio is incomplete",
    )

    return {
        "D5_cardinality": size,
        "D5_positive_weight_support": 12,
        "D5_zero_weight_extensions": 28,
        "simplex_union_support_sizes": simplex_supports,
    }


def verify_row_counterexample(
    certificate_path: Path = CERTIFICATE,
) -> dict[str, object]:
    data = json.loads(certificate_path.read_text())
    require(
        data["schema"]
        == "weighted-common-source.local-row-energy-counterexample.v1",
        "wrong row-energy certificate schema",
    )
    require(
        data["status"] == "EXACT RATIONAL SPHERICAL CODE COUNTEREXAMPLE",
        "wrong row-energy certificate status",
    )
    points = [
        [Q(coordinate) for coordinate in point]
        for point in data["points"]
    ]
    require(len(points) == 25, "wrong row-energy code cardinality")
    require(
        all(len(point) == 5 for point in points),
        "wrong row-energy code dimension",
    )
    require(
        points[0] == [Q(1), Q(0), Q(0), Q(0), Q(0)],
        "first row-energy point is not e1",
    )
    require(
        all(
            sum((coordinate * coordinate for coordinate in point), Q(0))
            == 1
            for point in points
        ),
        "a row-energy point is not unit",
    )
    products = [
        sum((left[k] * right[k] for k in range(5)), Q(0))
        for left, right in itertools.combinations(points, 2)
    ]
    exact_maximum = max(products)
    require(
        exact_maximum == Q(data["claimed_exact_maximum_inner_product"]),
        "claimed exact maximum inner product is false",
    )
    require(
        exact_maximum < Q(1, 2),
        "row-energy counterexample violates the kissing bound",
    )
    require(
        len({tuple(point) for point in points}) == len(points),
        "row-energy counterexample contains duplicate points",
    )
    row_energy = sum((point[0] ** 2 for point in points), Q(0))
    require(
        row_energy == Q(data["claimed_exact_anchor_row_energy"]),
        "claimed exact row energy is false",
    )
    require(
        row_energy > Q(41, 5),
        "row energy does not exceed 41/5",
    )
    return {
        "cardinality": len(points),
        "maximum_inner_product": str(exact_maximum),
        "anchor_row_energy": str(row_energy),
        "threshold": "41/5",
    }


def verify(certificate_path: Path = CERTIFICATE) -> dict[str, object]:
    negative_tail = (Q(2) - 5 * Q(1, 50)) / (
        15 * (1 - Q(1, 50))
    )
    positive_tail = 4 * (1 - 5 * Q(1, 50)) / (
        15 * (1 - 2 * Q(1, 50))
    )
    require(negative_tail == Q(19, 147), "negative-tail constant failed")
    require(positive_tail == Q(1, 4), "positive-tail constant failed")
    return {
        "status": "PASS",
        "weighted_identities": verify_matrix_identities(),
        "zero_weight_tail_constants": {
            "below_minus_1_over_50": str(negative_tail),
            "above_plus_1_over_50": str(positive_tail),
        },
        "exact_row_counterexample": verify_row_counterexample(
            certificate_path
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
