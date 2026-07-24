#!/usr/bin/env python3
"""Exact standard-library audit of the shifted-W sign-rank barrier."""

from __future__ import annotations

from fractions import Fraction as Q
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "sign_rank_counterexample.json"


def canonical_projective_points() -> list[tuple[int, int, int, int]]:
    """Canonical representatives of the points of PG(3,3)."""
    points: set[tuple[int, int, int, int]] = set()
    for vector in itertools.product(range(3), repeat=4):
        if vector == (0, 0, 0, 0):
            continue
        first = next(value for value in vector if value)
        inverse = 1 if first == 1 else 2
        points.add(tuple(inverse * value % 3 for value in vector))
    return sorted(points)


def symplectic_product(
    first: tuple[int, int, int, int],
    second: tuple[int, int, int, int],
) -> int:
    return (
        first[0] * second[1]
        - first[1] * second[0]
        + first[2] * second[3]
        - first[3] * second[2]
    ) % 3


def adjacency_matrix(
    points: list[tuple[int, int, int, int]],
) -> list[list[int]]:
    return [
        [
            int(i != j and symplectic_product(first, second) == 0)
            for j, second in enumerate(points)
        ]
        for i, first in enumerate(points)
    ]


def matrix_product(
    first: list[list[int]], second: list[list[int]]
) -> list[list[int]]:
    return [
        [
            sum(first[i][k] * second[k][j] for k in range(len(second)))
            for j in range(len(second[0]))
        ]
        for i in range(len(first))
    ]


def matrix_rank(matrix: list[list[Q | int]]) -> int:
    work = [[Q(value) for value in row] for row in matrix]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, row_count)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    entry - multiplier * pivot_entry
                    for entry, pivot_entry in zip(
                        work[row], work[rank]
                    )
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def verify(certificate_path: Path = CERTIFICATE) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    assert certificate["schema"] == (
        "w-shift-sign-rank-counterexample-v1"
    )
    assert certificate["status"] == (
        "EXACT COUNTEREXAMPLE WITH COMMON-SOURCE SEPARATOR"
    )

    points = canonical_projective_points()
    assert len(points) == certificate["projective_point_count"] == 40
    assert all(next(value for value in point if value) == 1 for point in points)
    assert all(symplectic_product(point, point) == 0 for point in points)

    adjacency = adjacency_matrix(points)
    assert all(adjacency[i][i] == 0 for i in range(40))
    assert all(
        adjacency[i][j] == adjacency[j][i]
        for i in range(40)
        for j in range(40)
    )
    degrees = [sum(row) for row in adjacency]
    assert degrees == [12] * 40

    common_neighbors = matrix_product(adjacency, adjacency)
    for i in range(40):
        for j in range(40):
            expected = (
                12
                if i == j
                else 2
                if adjacency[i][j]
                else 4
            )
            assert common_neighbors[i][j] == expected

    # The checked SRG relation is A^2 = 8I - 2A + 4J.
    assert common_neighbors == [
        [
            8 * int(i == j) - 2 * adjacency[i][j] + 4
            for j in range(40)
        ]
        for i in range(40)
    ]
    edge_count = sum(degrees) // 2
    assert edge_count == certificate["gq_edge_count"] == 240

    # On constants A has eigenvalue 12.  On its orthogonal complement the
    # checked relation becomes (A-2I)(A+4I)=0.  Trace A=0 and dimension 39
    # give multiplicities 24 and 15, respectively.
    positive_nonprincipal_multiplicity = 24
    negative_multiplicity = 15
    assert positive_nonprincipal_multiplicity + negative_multiplicity == 39
    assert (
        12
        + 2 * positive_nonprincipal_multiplicity
        - 4 * negative_multiplicity
        == 0
    )

    order = 41
    w = [[0 for _ in range(order)] for _ in range(order)]
    for i in range(40):
        for j in range(40):
            w[i][j] = 2 * adjacency[i][j]
    m = [
        [w[i][j] - 4 * int(i == j) for j in range(order)]
        for i in range(order)
    ]
    assert all(w[i][i] == 0 for i in range(order))
    assert all(
        0 <= w[i][j] <= Q(9, 4)
        for i in range(order)
        for j in range(order)
        if i != j
    )
    assert all(m[i][i] == -4 for i in range(order))
    assert matrix_rank(m) == certificate["m_rank"] == 17

    expected_spectrum = {
        "20": 1,
        "0": 24,
        "-12": 15,
        "-4": 1,
    }
    assert certificate["m_spectrum"] == expected_spectrum
    assert certificate["m_positive_inertia"] == 1
    assert certificate["m_negative_inertia"] == 16
    assert certificate["m_nullity"] == 24
    assert 17 < (order + 1) // 2

    # This fake also obeys the stronger rank-one domination M <= (6/5)J.
    q_matrix = [
        [Q(6, 5) - m[i][j] for j in range(order)]
        for i in range(order)
    ]
    assert matrix_rank(q_matrix) == certificate["q_rank"] == 17

    # On the sum-zero subspace of the first 40 coordinates, Q=-M has
    # eigenvalues 0 and 12.  On vectors (c*1_40,z), its quadratic form is
    # 1120 c^2 + 96 c z + (26/5) z^2.  The two exact Sylvester pivots below
    # prove positivity on that complementary plane.
    constant_plane_first_minor = Q(1120)
    constant_plane_determinant = (
        Q(1120) * Q(26, 5) - Q(48) ** 2
    )
    assert constant_plane_first_minor > 0
    assert constant_plane_determinant == 3520 > 0

    # Common-source separator.  If W arose from a spherical-code Gram
    # matrix G, W=2 would force g in {0,-1/2}, while W=0 would force
    # g in {1/2,-1}.  Let e count the -1/2 edge pairs and a the antipodal
    # (-1) nonedge pairs.  Antipodes form a matching, so a<=20.  The
    # degree-two harmonic Gram matrix then has the displayed maximum
    # trace square, attained formally at e=0,a=20.
    nonedge_count = order * (order - 1) // 2 - edge_count
    assert (
        nonedge_count
        == certificate["total_nonedge_count_after_isolate"]
        == 580
    )
    h2_trace_square_upper = (
        41
        + 2
        * (
            Q(edge_count, 16)
            + Q(nonedge_count - 20, 256)
            + 20
        )
    )
    h2_rank_trace_lower = Q(41 * 41, 14)
    separator_gap = h2_rank_trace_lower - h2_trace_square_upper
    assert h2_trace_square_upper == Q(
        certificate["common_source_h2_trace_square_upper_bound"]
    )
    assert h2_rank_trace_lower == Q(
        certificate["rank_14_h2_trace_square_lower_bound"]
    )
    assert separator_gap == Q(certificate["exact_separator_gap"])
    assert h2_trace_square_upper == Q(923, 8)
    assert h2_rank_trace_lower == Q(1681, 14)
    assert separator_gap == Q(263, 56) > 0

    return {
        "status": "PASS",
        "construction": "W(3,3) point graph plus one isolate",
        "matrix_order": order,
        "w_off_diagonal_values": [0, 2],
        "m_rank": matrix_rank(m),
        "m_inertia": [1, 16, 24],
        "rank_half_bound_refuted_by": (order + 1) // 2 - matrix_rank(m),
        "rank_one_domination": {
            "statement": "M <= (6/5)J",
            "q_rank": matrix_rank(q_matrix),
            "constant_plane_determinant": str(
                constant_plane_determinant
            ),
        },
        "common_source_separator": {
            "h2_trace_square_upper": str(h2_trace_square_upper),
            "h2_rank_trace_lower": str(h2_rank_trace_lower),
            "gap": str(separator_gap),
        },
        "scope": certificate["scope"],
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
