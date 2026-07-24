#!/usr/bin/env python3
"""Exact verifier for the continuous rank-five Farkas counterexample."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import itertools
import json
import math


def determinant(matrix: list[list[Q]]) -> Q:
    work = [row[:] for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, len(work)):
            multiplier = work[row][column] / pivot_value
            for other in range(column + 1, len(work)):
                work[row][other] -= multiplier * work[column][other]
    return answer


def matrix_rank(matrix: list[list[Q]]) -> int:
    work = [row[:] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def inverse_two(matrix: list[list[Q]]) -> list[list[Q]]:
    determinant_value = matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2
    return [
        [matrix[1][1] / determinant_value, -matrix[0][1] / determinant_value],
        [-matrix[1][0] / determinant_value, matrix[0][0] / determinant_value],
    ]


def schur_complement(
    matrix: list[list[Q]], base_size: int
) -> list[list[Q]]:
    base = [row[:base_size] for row in matrix[:base_size]]
    cross = [row[base_size:] for row in matrix[:base_size]]
    tail = [row[base_size:] for row in matrix[base_size:]]
    inverse = inverse_two(base)
    answer = [row[:] for row in tail]
    for i in range(len(tail)):
        for j in range(len(tail)):
            correction = sum(
                cross[a][i] * inverse[a][b] * cross[b][j]
                for a in range(base_size)
                for b in range(base_size)
            )
            answer[i][j] -= correction
    return answer


def gram_matrix() -> list[list[Q]]:
    return [
        [1, Q(-3, 4), Q(1, 4), Q(-1, 4), Q(-1, 4), Q(-1, 4), Q(-1, 4)],
        [Q(-3, 4), 1, Q(1, 4), Q(-1, 4), Q(-1, 4), Q(-1, 4), Q(-1, 4)],
        [Q(1, 4), Q(1, 4), 1, 0, Q(-2, 3), Q(-2, 3), Q(-2, 3)],
        [Q(-1, 4), Q(-1, 4), 0, 1, Q(1, 3), Q(1, 3), Q(1, 3)],
        [Q(-1, 4), Q(-1, 4), Q(-2, 3), Q(1, 3), 1, Q(1, 3), Q(1, 3)],
        [Q(-1, 4), Q(-1, 4), Q(-2, 3), Q(1, 3), Q(1, 3), 1, Q(1, 3)],
        [Q(-1, 4), Q(-1, 4), Q(-2, 3), Q(1, 3), Q(1, 3), Q(1, 3), 1],
    ]


def verify() -> dict[str, object]:
    gram = [[Q(value) for value in row] for row in gram_matrix()]
    assert all(gram[i][j] == gram[j][i] for i in range(7) for j in range(7))
    assert all(gram[index][index] == 1 for index in range(7))
    assert max(
        gram[i][j] for i in range(7) for j in range(i + 1, 7)
    ) <= Q(1, 2)

    principal_minor_summary = {}
    for size in range(1, 8):
        values = []
        for indices in itertools.combinations(range(7), size):
            minor = [[gram[i][j] for j in indices] for i in indices]
            values.append(determinant(minor))
        assert all(value >= 0 for value in values)
        principal_minor_summary[size] = {
            "minimum": str(min(values)),
            "maximum": str(max(values)),
            "zeros": sum(value == 0 for value in values),
        }
    assert matrix_rank(gram) == 5
    assert all(
        determinant([[gram[i][j] for j in indices] for i in indices]) == 0
        for indices in itertools.combinations(range(7), 6)
    )

    schur = schur_complement(gram, 2)
    tetrahedron_duplicated = [
        [Q(1) if first == second else Q(-1, 3) for second in (0, 0, 1, 2, 3)]
        for first in (0, 0, 1, 2, 3)
    ]
    assert schur == [
        [value / 2 for value in row] for row in tetrahedron_duplicated
    ]
    assert matrix_rank(schur) == 3

    base_first, base_second = 0, 1
    depth_vertices = [
        vertex
        for vertex in range(2, 7)
        if gram[base_first][vertex] + gram[base_second][vertex] < 0
    ]
    common_vertices = [
        vertex
        for vertex in range(2, 7)
        if gram[base_first][vertex] >= Q(1, 4)
        and gram[base_second][vertex] >= Q(1, 4)
    ]
    exact_155 = [
        vertex
        for vertex in common_vertices
        if gram[base_first][vertex] == Q(1, 4)
        and gram[base_second][vertex] == Q(1, 4)
    ]
    assert depth_vertices == [3, 4, 5, 6]
    assert common_vertices == exact_155 == [2]
    depth = len(depth_vertices)
    common = len(common_vertices)
    exact = len(exact_155)
    atom_value = (
        common - exact - 2109 * math.comb(depth, 4) * common
    )
    assert atom_value == -2109

    # The distinguished base is the only -3/4 off-diagonal entry.
    minus_three_quarters = [
        (i, j)
        for i in range(7)
        for j in range(i + 1, 7)
        if gram[i][j] == Q(-3, 4)
    ]
    assert minus_three_quarters == [(0, 1)]

    # Exact factorization of the representing-state coefficient.
    for global_depth in range(7, 40):
        left = Q(
            math.comb(global_depth, 4) - math.comb(7, 4), 273
        )
        right = Q(
            (global_depth - 7)
            * (global_depth + 4)
            * (global_depth**2 - 3 * global_depth + 30),
            6552,
        )
        assert left == right >= 0

    return {
        "status": "PASS",
        "rank": 5,
        "maximum_off_diagonal": str(
            max(
                gram[i][j]
                for i in range(7)
                for j in range(i + 1, 7)
            )
        ),
        "principal_minors": principal_minor_summary,
        "schur_complement_rank": matrix_rank(schur),
        "depth_count": depth,
        "common_count": common,
        "exact_155_count": exact,
        "farkas_atom_value": atom_value,
        "off_grid_inner_products": sorted(
            str(value)
            for value in {
                gram[i][j]
                for i in range(7)
                for j in range(i + 1, 7)
                if gram[i][j] not in {
                    Q(-1),
                    Q(-3, 4),
                    Q(-1, 2),
                    Q(-1, 4),
                    Q(0),
                    Q(1, 4),
                    Q(1, 2),
                }
            }
        ),
        "conclusion": (
            "rank-five PSD does not imply the finite-pool atom sign"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
