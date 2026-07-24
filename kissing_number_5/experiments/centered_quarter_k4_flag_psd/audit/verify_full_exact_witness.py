#!/usr/bin/env python3
"""Independent exact verifier for the full-centered K4 flag witness."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from experiments.centered_quarter_k4_flag_psd.audit.rationalize_full_witness import (
    affine_system,
)
from experiments.centered_quarter_k4_flag_psd.audit.search_full_centering import (
    coefficients,
)


def matvec(matrix: list[list[Q]], vector: list[Q]) -> list[Q]:
    return [
        sum((entry * value for entry, value in zip(row, vector)), Q(0))
        for row in matrix
    ]


def independent_columns(vectors: list[list[Q]]) -> list[int]:
    """Return indices of a maximal independent subset of column vectors."""
    if not vectors:
        return []
    row_count = len(vectors[0])
    basis: dict[int, list[Q]] = {}
    chosen = []
    for index, vector in enumerate(vectors):
        work = list(vector)
        for pivot in sorted(basis):
            if work[pivot]:
                factor = work[pivot] / basis[pivot][pivot]
                work = [
                    value - factor * base
                    for value, base in zip(work, basis[pivot])
                ]
        pivot = next(
            (row for row in range(row_count) if work[row]), None
        )
        if pivot is not None:
            basis[pivot] = work
            chosen.append(index)
    return chosen


def independent_rows(matrix: list[list[Q]]) -> list[int]:
    # Treat the rows as the candidate vectors in their column coordinate
    # space.
    return independent_columns([list(row) for row in matrix])


def positive_definite_ldl(matrix: list[list[Q]]) -> list[Q]:
    """Exact unpivoted LDL; succeeds iff all exact pivots are positive."""
    size = len(matrix)
    lower = [[Q(0) for _ in range(size)] for _ in range(size)]
    diagonal = [Q(0) for _ in range(size)]
    for row in range(size):
        lower[row][row] = 1
        pivot = matrix[row][row] - sum(
            (
                lower[row][column]
                * lower[row][column]
                * diagonal[column]
                for column in range(row)
            ),
            Q(0),
        )
        assert pivot > 0
        diagonal[row] = pivot
        for later in range(row + 1, size):
            numerator = matrix[later][row] - sum(
                (
                    lower[later][column]
                    * lower[row][column]
                    * diagonal[column]
                    for column in range(row)
                ),
                Q(0),
            )
            lower[later][row] = numerator / pivot
    return diagonal


def reduced_psd_check(
    matrix: list[list[Q]], kernel_vectors: list[list[Q]]
) -> tuple[int, list[Q]]:
    size = len(matrix)
    assert all(
        matrix[row][column] == matrix[column][row]
        for row in range(size)
        for column in range(size)
    )
    for vector in kernel_vectors:
        assert matvec(matrix, vector) == [Q(0)] * size
    chosen_columns = independent_columns(kernel_vectors)
    independent_kernels = [
        kernel_vectors[index] for index in chosen_columns
    ]
    kernel_matrix = [
        [vector[row] for vector in independent_kernels]
        for row in range(size)
    ]
    pivot_rows = independent_rows(kernel_matrix)
    assert len(pivot_rows) == len(independent_kernels)
    keep = [row for row in range(size) if row not in pivot_rows]
    reduced = [[matrix[row][column] for column in keep] for row in keep]
    pivots = positive_definite_ldl(reduced)
    return len(independent_kernels), pivots


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    audit = Path(__file__).resolve().parent
    source = json.loads(
        (
            root
            / "certificates/centered_quarter_bv_pseudodistribution.json"
        ).read_text()
    )
    certificate_path = audit / "results/full_exact_linear_witness.json"
    certificate = json.loads(certificate_path.read_text())
    data = coefficients(source)
    alpha = [Q(value) for value in certificate["alpha"]]
    nu = [Q(value) for value in certificate["nu"]]
    k4 = [Q(value) for value in certificate["k4"]]
    exact = alpha + nu + k4
    assert min(exact) > 0

    # Rebuild and check all 183 affine rows independently.
    affine, rhs = affine_system(data)
    for row, target in zip(affine, rhs):
        assert sum(
            (
                Q(int(coefficient)) * value
                for coefficient, value in zip(row, exact)
                if coefficient
            ),
            Q(0),
        ) == int(target)

    grid = tuple(Q(value) for value in data["grid"])
    categories = data["categories"]
    triple_count = len(data["triples"])
    orbit_count = len(data["orbits"])
    edge_first6 = np.rint(6 * data["edge_first"]).astype(np.int64)
    vertex_distinct6 = np.rint(
        6 * data["vertex_distinct"]
    ).astype(np.int64)
    edge_flag = [
        np.rint(block).astype(np.int64) for block in data["edge_flag"]
    ]
    assert all(
        np.max(np.abs(6 * data["edge_first"][q] - edge_first6[q]))
        < 1e-12
        for q in range(7)
    )
    assert (
        np.max(
            np.abs(
                6 * data["vertex_distinct"] - vertex_distinct6
            )
        )
        < 1e-12
    )

    # Vertex moment block.
    vertex_second = [[Q(0) for _ in range(7)] for _ in range(7)]
    for first in range(7):
        vertex_second[first][first] += alpha[first]
        for second in range(7):
            vertex_second[first][second] += sum(
                (
                    Q(
                        int(vertex_distinct6[first, second, triple]),
                        6,
                    )
                    * nu[triple]
                    for triple in range(triple_count)
                ),
                Q(0),
            )
    vertex_block = [
        vertex_second[row] + [alpha[row]] for row in range(7)
    ] + [alpha + [Q(1)]]
    vertex_kernels = [
        [Q(1)] * 7 + [Q(-40)],
        list(grid) + [Q(1)],
    ]
    vertex_nullity, vertex_pivots = reduced_psd_check(
        vertex_block, vertex_kernels
    )

    # Ordered-edge moment blocks.
    flag_factor = Q(math.comb(41, 4), 41)
    assert flag_factor == 2470
    edge_reports = []
    for q in range(7):
        first = [
            sum(
                (
                    Q(int(edge_first6[q, category, triple]), 6)
                    * nu[triple]
                    for triple in range(triple_count)
                ),
                Q(0),
            )
            for category in range(len(categories))
        ]
        active = [index for index, value in enumerate(first) if value]
        # No K4 coefficient may reintroduce a structurally absent profile.
        inactive = set(range(len(categories))) - set(active)
        for index in inactive:
            assert all(
                edge_flag[q][index, column, orbit] == 0
                and edge_flag[q][column, index, orbit] == 0
                for column in range(len(categories))
                for orbit in range(orbit_count)
            )

        second = [
            [Q(0) for _ in active] for _ in active
        ]
        for local_row, row in enumerate(active):
            for local_column, column in enumerate(active):
                second[local_row][local_column] = flag_factor * sum(
                    (
                        int(edge_flag[q][row, column, orbit]) * k4[orbit]
                        for orbit in range(orbit_count)
                        if edge_flag[q][row, column, orbit]
                    ),
                    Q(0),
                )
                if row == column:
                    second[local_row][local_column] += first[row]
        active_first = [first[index] for index in active]
        block = [
            second[row] + [active_first[row]]
            for row in range(len(active))
        ] + [active_first + [alpha[q]]]
        kernels = [
            [Q(1)] * len(active) + [Q(-39)],
            [grid[categories[index][0]] for index in active]
            + [1 + grid[q]],
            [grid[categories[index][1]] for index in active]
            + [1 + grid[q]],
        ]
        nullity, pivots = reduced_psd_check(block, kernels)
        edge_reports.append(
            {
                "color": str(grid[q]),
                "active_profiles": len(active),
                "certified_kernel_rank": nullity,
                "positive_reduced_dimension": len(pivots),
                "minimum_ldl_pivot_float": float(min(pivots)),
            }
        )

    # Check all non-deduplicated K3 extension-count and centering equations.
    oriented_mass6 = np.rint(6 * data["oriented_mass"]).astype(np.int64)
    extension_count = np.rint(data["extension_count"]).astype(np.int64)
    extension_sum4 = np.rint(4 * data["extension_sum"]).astype(np.int64)
    for row, oriented in enumerate(data["oriented_types"]):
        base_mass6 = sum(
            (
                int(oriented_mass6[row, triple]) * nu[triple]
                for triple in range(triple_count)
            ),
            Q(0),
        )
        assert 6 * flag_factor * sum(
            (
                int(extension_count[row, orbit]) * k4[orbit]
                for orbit in range(orbit_count)
                if extension_count[row, orbit]
            ),
            Q(0),
        ) == 38 * base_mass6
        first, second, third = oriented
        for center, incident in enumerate(
            ((first, second), (first, third), (second, third))
        ):
            target4 = -4 - 4 * grid[incident[0]] - 4 * grid[incident[1]]
            assert target4.denominator == 1
            assert 6 * flag_factor * sum(
                (
                    int(extension_sum4[row, center, orbit]) * k4[orbit]
                    for orbit in range(orbit_count)
                    if extension_sum4[row, center, orbit]
                ),
                Q(0),
            ) == int(target4) * base_mass6

    summary = {
        "schema": "kissing5.centered_quarter_k4_full_exact_verification.v1",
        "status": (
            "exact positive rational witness for the full K2/K3/K4 "
            "quarter-grid pointwise-centering and ordered-edge PSD relaxation"
        ),
        "certificate": str(certificate_path.relative_to(root)),
        "certificate_sha256": hashlib.sha256(
            certificate_path.read_bytes()
        ).hexdigest(),
        "affine_rows_checked": len(affine),
        "ordered_triangle_types_checked": len(data["oriented_types"]),
        "vertex_kernel_rank": vertex_nullity,
        "vertex_positive_reduced_dimension": len(vertex_pivots),
        "vertex_minimum_ldl_pivot_float": float(min(vertex_pivots)),
        "edge_blocks": edge_reports,
        "scope": (
            "This is a finite-support relaxation witness only.  It is not a "
            "41-point code and does not establish global K5 consistency."
        ),
    }
    output = audit / "results/full_exact_verification.json"
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    output.write_text(encoded)
    print(encoded, end="")
    print("sha256=" + hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
