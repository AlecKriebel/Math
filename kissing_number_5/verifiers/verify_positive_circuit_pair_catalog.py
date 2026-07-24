#!/usr/bin/env python3
"""Exact verifier for the D5 positive-circuit pair catalog."""

from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from math import gcd, lcm
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "positive_circuit_pair_catalog.json"


def root_system(dimension):
    roots = []
    for first, second in combinations(range(dimension), 2):
        for first_sign, second_sign in product((-1, 1), repeat=2):
            vector = [0] * dimension
            vector[first] = first_sign
            vector[second] = second_sign
            roots.append(tuple(vector))
    return tuple(roots)


def matrix_rank(columns, dimension):
    matrix = [
        [Q(column[row]) for column in columns]
        for row in range(dimension)
    ]
    rank = 0
    for column in range(len(columns)):
        pivot = next(
            (
                row
                for row in range(rank, dimension)
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(dimension):
            if row != rank and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [
                    value - scale * pivot_value
                    for value, pivot_value in zip(
                        matrix[row], matrix[rank]
                    )
                ]
        rank += 1
    return rank


def positive_kernel_vector(columns, dimension):
    """Return normalized positive kernel weights for a minimal circuit."""

    matrix = [
        [Q(column[row]) for column in columns]
        for row in range(dimension)
    ]
    rank = 0
    pivots = []
    for column in range(len(columns)):
        pivot = next(
            (
                row
                for row in range(rank, dimension)
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(dimension):
            if row != rank and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [
                    value - scale * pivot_value
                    for value, pivot_value in zip(
                        matrix[row], matrix[rank]
                    )
                ]
        pivots.append(column)
        rank += 1
    assert rank == len(columns) - 1
    free_columns = [
        column for column in range(len(columns)) if column not in pivots
    ]
    assert len(free_columns) == 1
    free = free_columns[0]
    kernel = [Q(0)] * len(columns)
    kernel[free] = 1
    for row, pivot in enumerate(pivots):
        kernel[pivot] = -matrix[row][free]
    if all(value < 0 for value in kernel):
        kernel = [-value for value in kernel]
    assert all(value > 0 for value in kernel)
    total = sum(kernel)
    kernel = [value / total for value in kernel]
    assert all(
        sum(
            kernel[column] * columns[column][row]
            for column in range(len(columns))
        ) == 0
        for row in range(dimension)
    )
    return tuple(kernel)


def inner(left, right):
    # Integer vectors are sqrt(2) times normalized roots.
    return Q(sum(a * b for a, b in zip(left, right)), 2)


def integer_partitions(total, maximum=None):
    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for rest in integer_partitions(total - first, first):
            yield (first,) + rest


def verify():
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert data["schema"] == "positive-circuit-pair-catalog-v1"
    pair_payload = {"pairs": data["pair_examples"]}
    encoded = json.dumps(
        pair_payload, separators=(",", ":"), sort_keys=False
    ).encode()
    assert hashlib.sha256(encoded).hexdigest() == data[
        "pair_payload_sha256"
    ]

    roots = root_system(5)
    assert len(roots) == 40
    assert all(inner(root, root) == 1 for root in roots)
    assert max(
        inner(roots[first], roots[second])
        for first in range(len(roots))
        for second in range(first)
    ) == Q(1, 2)
    assert matrix_rank(roots, 5) == 5

    expected_pairs = {
        (first, second)
        for first in range(2, 7)
        for second in range(first, 7)
    }
    observed_pairs = set()
    intersection_dimensions = {}
    for item in data["pair_examples"]:
        sizes = tuple(item["sizes"])
        first_indices = tuple(item["first"])
        second_indices = tuple(item["second"])
        assert sizes == (len(first_indices), len(second_indices))
        assert set(first_indices).isdisjoint(second_indices)
        first_columns = tuple(roots[index] for index in first_indices)
        second_columns = tuple(roots[index] for index in second_indices)
        first_weights = positive_kernel_vector(first_columns, 5)
        second_weights = positive_kernel_vector(second_columns, 5)

        cross = [
            [inner(first, second) for second in second_columns]
            for first in first_columns
        ]
        assert max(value for row in cross for value in row) <= Q(1, 2)
        assert all(
            sum(
                cross[row][column] * second_weights[column]
                for column in range(len(second_weights))
            ) == 0
            for row in range(len(first_weights))
        )
        assert all(
            sum(
                first_weights[row] * cross[row][column]
                for row in range(len(first_weights))
            ) == 0
            for column in range(len(second_weights))
        )

        union_rank = matrix_rank(first_columns + second_columns, 5)
        intersection = (
            len(first_indices) - 1
            + len(second_indices) - 1
            - union_rank
        )
        assert intersection >= max(0, sum(sizes) - 7)
        intersection_dimensions[sizes] = intersection
        observed_pairs.add(sizes)
    assert observed_pairs == expected_pairs

    # A nonzero normal u is orthogonal to a D5 root line precisely when
    # either two zero coordinates are used (both signed lines vanish), or
    # two nonzero coordinates have the same absolute value (one line
    # vanishes).  Maximize the number of zero root lines over all possible
    # zero-coordinate counts and partitions of equal absolute values.
    maximum_zero_lines = 0
    for zero_count in range(5):
        for groups in integer_partitions(5 - zero_count):
            zero_lines = zero_count * (zero_count - 1)
            zero_lines += sum(size * (size - 1) // 2 for size in groups)
            maximum_zero_lines = max(maximum_zero_lines, zero_lines)
    assert maximum_zero_lines == 12
    open_hemisphere_minimum = 20 - maximum_zero_lines
    assert open_hemisphere_minimum == data[
        "d5_open_origin_hemisphere_minimum"
    ] == 8

    # Near-counterexample: only the final rank-five requirement fails.
    roots6 = root_system(6)
    near = roots6[:41]
    assert len(near) == data["rank_six_near_counterexample"][
        "cardinality"
    ] == 41
    assert all(inner(root, root) == 1 for root in near)
    assert max(
        inner(near[first], near[second])
        for first in range(len(near))
        for second in range(first)
    ) <= Q(1, 2)
    near_rank = matrix_rank(near, 6)
    assert near_rank == data["rank_six_near_counterexample"][
        "gram_rank"
    ] == 6
    for indices in data["rank_six_near_counterexample"][
        "positive_circuits"
    ]:
        positive_kernel_vector(tuple(near[index] for index in indices), 6)
    assert set(
        data["rank_six_near_counterexample"]["positive_circuits"][0]
    ).isdisjoint(
        data["rank_six_near_counterexample"]["positive_circuits"][1]
    )

    return {
        "status": "PASS",
        "d5_circuit_size_pairs": len(observed_pairs),
        "d5_open_hemisphere_minimum": open_hemisphere_minimum,
        "intersection_dimensions": intersection_dimensions,
        "rank_six_near_counterexample_size": len(near),
        "rank_six_near_counterexample_rank": near_rank,
        "conclusion": "circuit sizes and two kernel vectors alone do not separate",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
