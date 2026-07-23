#!/usr/bin/env python3
"""Exact checks for proofs/rank_kernel_barriers.md.

All matrices have integer entries after harmless scaling.  The verifier uses
only Python's standard library and exact Fraction Gaussian elimination.
"""

from fractions import Fraction
from itertools import combinations, product


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    rows = len(a)
    middle = len(b)
    columns = len(b[0])
    return [
        [
            sum(a[i][k] * b[k][j] for k in range(middle))
            for j in range(columns)
        ]
        for i in range(rows)
    ]


def add_scaled_identity(a: list[list[int]], scalar: int) -> list[list[int]]:
    return [
        [value + (scalar if i == j else 0) for j, value in enumerate(row)]
        for i, row in enumerate(a)
    ]


def exact_rank(a: list[list[int]]) -> int:
    matrix = [[Fraction(value) for value in row] for row in a]
    rows = len(matrix)
    columns = len(matrix[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if matrix[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(rows):
            if row == rank or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def finite_field_matrices() -> tuple[list[tuple[int, int]], list[list[int]], list[list[int]]]:
    vertices = list(product(range(7), repeat=2))
    size = len(vertices)
    line_graph = [[0] * size for _ in range(size)]
    complement = [[0] * size for _ in range(size)]
    for i, (x1, y1) in enumerate(vertices):
        for j, (x2, y2) in enumerate(vertices):
            if i == j:
                continue
            adjacent_line = (
                x1 == x2
                or y1 == y2
                or (x1 + y1 - x2 - y2) % 7 == 0
            )
            line_graph[i][j] = int(adjacent_line)
            complement[i][j] = int(not adjacent_line)
    return vertices, line_graph, complement


def verify_finite_field_counterexample() -> dict[str, object]:
    vertices, line_graph, adjacency = finite_field_matrices()
    assert all(sum(row) == 18 for row in line_graph)
    assert all(sum(row) == 30 for row in adjacency)

    # Exact minimal-polynomial identity:
    # (A - 30 I)(A - 2 I)(A + 5 I) = 0.
    factor1 = add_scaled_identity(adjacency, -30)
    factor2 = add_scaled_identity(adjacency, -2)
    factor3 = add_scaled_identity(adjacency, 5)
    zero = matmul(matmul(factor1, factor2), factor3)
    assert all(value == 0 for row in zero for value in row)
    assert exact_rank(adjacency) == 49

    # Work with 2M = 2I-A to stay integral.
    twice_m = [
        [2 * int(i == j) - adjacency[i][j] for j in range(49)]
        for i in range(49)
    ]
    assert exact_rank(twice_m) == 19

    deleted = {
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (1, 0),
        (1, 2),
    }
    retained_indices = [i for i, vertex in enumerate(vertices) if vertex not in deleted]
    assert len(retained_indices) == 41
    principal = [
        [twice_m[i][j] for j in retained_indices]
        for i in retained_indices
    ]
    principal_rank = exact_rank(principal)
    assert principal_rank <= 19

    clique = {(0, 0), (1, 1), (2, 4), (3, 2)}
    clique_indices = [vertices.index(vertex) for vertex in clique]
    assert all(adjacency[i][j] == 1 for i, j in combinations(clique_indices, 2))
    # The quadratic form for M, not 2M, on the clique indicator is -2.
    quadratic_twice_m = sum(
        twice_m[i][j] for i in clique_indices for j in clique_indices
    )
    assert quadratic_twice_m == -4

    # 10(M+3J/10)=5(2M)+3J is PSD by the proved spectrum; its
    # exact rank gives an independent algebraic check of the claimed nullity.
    scaled_r = [
        [5 * twice_m[i][j] + 3 for j in range(49)]
        for i in range(49)
    ]
    assert exact_rank(scaled_r) == 19

    return {
        "full_order": 49,
        "full_rank_M": exact_rank(twice_m),
        "principal_order": 41,
        "principal_rank_M": principal_rank,
        "clique_quadratic_form_M": Fraction(quadratic_twice_m, 2),
        "rank_M_plus_3J_over_10": exact_rank(scaled_r),
    }


def d_roots(dimension: int) -> list[tuple[int, ...]]:
    roots: list[tuple[int, ...]] = []
    for i, j in combinations(range(dimension), 2):
        for sign_i, sign_j in product((-1, 1), repeat=2):
            root = [0] * dimension
            root[i] = sign_i
            root[j] = sign_j
            roots.append(tuple(root))
    return roots


def verify_d6_kernel() -> dict[str, object]:
    roots = d_roots(6)
    assert len(roots) == 60
    # If q = r.s, then g=q/2 and 4p(g)=(q+2)(q-1).
    four_k = [
        [
            (sum(a * b for a, b in zip(r, s, strict=True)) + 2)
            * (sum(a * b for a, b in zip(r, s, strict=True)) - 1)
            for s in roots
        ]
        for r in roots
    ]
    assert all(four_k[i][i] == 4 for i in range(60))
    assert all(
        four_k[i][j] <= 0
        for i in range(60)
        for j in range(60)
        if i != j
    )
    rank = exact_rank(four_k)
    assert rank == 27

    # The spectrum of 4K is -80^1, 16^5, 8^15, 20^6, 0^33.
    trace = sum(four_k[i][i] for i in range(60))
    square = matmul(four_k, four_k)
    trace_square = sum(square[i][i] for i in range(60))
    assert trace == -80 + 5 * 16 + 15 * 8 + 6 * 20
    assert trace_square == 80**2 + 5 * 16**2 + 15 * 8**2 + 6 * 20**2

    return {
        "order": 60,
        "rank": rank,
        "trace_4K": trace,
        "trace_square_4K": trace_square,
        "claimed_spectrum_4K": {
            "-80": 1,
            "16": 5,
            "8": 15,
            "20": 6,
            "0": 33,
        },
    }


def main() -> None:
    print("finite_field:", verify_finite_field_counterexample())
    print("d6_kernel:", verify_d6_kernel())
    print("status: PASS")


if __name__ == "__main__":
    main()
