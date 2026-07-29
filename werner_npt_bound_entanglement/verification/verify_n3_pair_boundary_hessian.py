#!/usr/bin/env python3
"""Exact audit of the pair-sector deficit at the canonical boundary zero.

The verifier imports only the standard-library polar-chart construction
used by ``derive_n3_boundary_effective_quartic.py``.  It replaces the
quadratic pairing by

    (2/3)<C,D> - <Pi_2 C, Pi_2 D>

and reconstructs all 204 by 204 Hessian entries over Q.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import importlib.util
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
DERIVATION = HERE / "derive_n3_boundary_effective_quartic.py"


def load_derivation():
    spec = importlib.util.spec_from_file_location("n3_derivation", DERIVATION)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


derive = load_derivation()
F = Fraction


def local_pair(first, second, traceless):
    """Matrix-unit kernel of the local scalar/traceless projection."""

    a, b = first
    c, d = second
    scalar = F(1, 3) if a == b and c == d else F(0)
    identity = F(1) if a == c and b == d else F(0)
    return identity - scalar if traceless else scalar


def unit_pair_sector(first, second):
    """Return <E_first, Pi_2 E_second> exactly."""

    row, column = first
    other_row, other_column = second
    answer = F(0)
    for scalar_site in range(3):
        term = F(1)
        for site in range(3):
            term *= local_pair(
                (row[site], column[site]),
                (other_row[site], other_column[site]),
                traceless=site != scalar_site,
            )
        answer += term
    return answer


def deficit_pairing(first, second):
    """Gaussian-rational polarization of (2/3)||C||^2-||Pi_2 C||^2."""

    answer = derive.ZERO
    for first_unit, first_value in first.items():
        for second_unit, second_value in second.items():
            identity = F(1) if first_unit == second_unit else F(0)
            kernel = F(2, 3) * identity - unit_pair_sector(
                first_unit, second_unit
            )
            answer = derive.gadd(
                answer,
                derive.gscale(
                    derive.gmul(
                        derive.gconjugate(first_value), second_value
                    ),
                    kernel,
                ),
            )
    return answer


def chart_terms(indices):
    """First and second polar-chart coefficients in one direction."""

    left = {}
    right = {}
    for index in indices:
        left = derive.scalar_frame_sum(
            left, derive.COORDINATES[index][0]
        )
        right = derive.scalar_frame_sum(
            right, derive.COORDINATES[index][1]
        )
    left_gram = derive.scalar_gram(left)
    right_gram = derive.scalar_gram(right)

    first = derive.scalar_matrix_sum(
        derive.scalar_outer(left, derive.RIGHT_BASE),
        derive.scalar_outer(derive.LEFT_BASE, right),
    )
    left_normalization = [
        [
            derive.gscale(left_gram[row][column], F(-1, 2))
            for column in range(2)
        ]
        for row in range(2)
    ]
    right_normalization = [
        [
            derive.gscale(right_gram[row][column], F(-1, 2))
            for column in range(2)
        ]
        for row in range(2)
    ]
    second = derive.scalar_matrix_sum(
        derive.scalar_outer(
            derive.scalar_multiply_right(
                derive.LEFT_BASE, left_normalization
            ),
            derive.RIGHT_BASE,
        ),
        derive.scalar_outer(
            derive.LEFT_BASE,
            derive.scalar_multiply_right(
                derive.RIGHT_BASE, right_normalization
            ),
        ),
        derive.scalar_outer(left, right),
    )
    return first, second


def quadratic_coefficient(indices):
    first, second = chart_terms(indices)
    first_value = deficit_pairing(first, first)
    cross_value = deficit_pairing(derive.BASE, second)
    assert first_value[1] == 0
    return first_value[0] + 2 * cross_value[0]


def linear_coefficient(index):
    first, _ = chart_terms((index,))
    value = deficit_pairing(derive.BASE, first)
    return 2 * value[0]


def derive_hessian():
    dimension = len(derive.COORDINATES)
    diagonal = [quadratic_coefficient((index,)) for index in range(dimension)]
    matrix = [[F(0) for _ in range(dimension)] for _ in range(dimension)]
    for index, value in enumerate(diagonal):
        matrix[index][index] = value
    for first in range(dimension):
        for second in range(first):
            value = (
                quadratic_coefficient((first, second))
                - diagonal[first]
                - diagonal[second]
            ) / 2
            matrix[first][second] = matrix[second][first] = value
    return matrix


def rref(rows, dimension):
    work = []
    for sparse in rows:
        row = [
            F(sparse.get(index, 0)) if isinstance(sparse, dict)
            else F(sparse[index])
            for index in range(dimension)
        ]
        if any(row):
            work.append(row)
    pivot_row = 0
    for column in range(dimension):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row]
                )
            ]
        pivot_row += 1
    return work[:pivot_row]


def nullspace(matrix, dimension=None):
    if dimension is None:
        dimension = len(matrix)
    reduced = rref(matrix, dimension)
    pivots = [
        next(index for index, value in enumerate(row) if value)
        for row in reduced
    ]
    output = []
    for free in range(dimension):
        if free in pivots:
            continue
        vector = {free: F(1)}
        for row, pivot in zip(reduced, pivots):
            if row[free]:
                vector[pivot] = -row[free]
        output.append(vector)
    return output


def intersection(first, second, dimension):
    """Basis of the intersection of two rational row spaces."""

    first_basis = rref(first, dimension)
    second_basis = rref(second, dimension)
    first_annihilator = nullspace(first_basis, dimension)
    second_annihilator = nullspace(second_basis, dimension)
    return nullspace(
        rref(first_annihilator + second_annihilator, dimension),
        dimension,
    )


def positive_rank(block):
    """Exact symmetric elimination; fail immediately if not PSD."""

    matrix = [row[:] for row in block]
    rank = 0
    while matrix:
        pivot = next(
            (index for index in range(len(matrix)) if matrix[index][index] > 0),
            None,
        )
        if pivot is None:
            assert all(value == 0 for row in matrix for value in row)
            break
        assert all(matrix[index][index] >= 0 for index in range(len(matrix)))
        if pivot:
            matrix[0], matrix[pivot] = matrix[pivot], matrix[0]
            for row in matrix:
                row[0], row[pivot] = row[pivot], row[0]
        value = matrix[0][0]
        column = [matrix[index][0] for index in range(1, len(matrix))]
        matrix = [
            [
                matrix[row + 1][column_index + 1]
                - column[row] * column[column_index] / value
                for column_index in range(len(column))
            ]
            for row in range(len(column))
        ]
        rank += 1
    return rank


def chart_index(label):
    return derive.LABELS.index(label)


def local_plane_graph_directions():
    """Move the common third-site plane span{|0>,|1>} inside C^3."""

    output = []
    for logical in range(2):
        for phase in ("real", "imag"):
            output.append(
                {
                    chart_index(("U", (0, 0, 2), logical, phase)): F(1),
                    chart_index(("V", (1, 1, 2), logical, phase)): F(1),
                }
            )
    return output


def genuine_third_site_opening_indices():
    """Coordinates that open, rather than move, the deficient local planes."""

    output = set()
    for index, label in enumerate(derive.LABELS):
        side = label[0]
        if side not in ("U", "V") or not isinstance(label[1], tuple):
            continue
        row = label[1]
        if row[2] != 2:
            continue
        base_environment = (0, 0) if side == "U" else (1, 1)
        if row[:2] != base_environment:
            output.add(index)
    return output


def factorized_zero_directions():
    """Tangent to |a><b| on sites 0,1 tensor P_W at the base."""

    output = []
    for first_two in product(range(3), repeat=2):
        if first_two == (0, 0):
            continue
        for phase in ("real", "imag"):
            output.append(
                {
                    chart_index(
                        ("U", first_two + (logical,), logical, phase)
                    ): F(1)
                    for logical in range(2)
                }
            )
    for first_two in product(range(3), repeat=2):
        if first_two == (1, 1):
            continue
        for phase in ("real", "imag"):
            output.append(
                {
                    chart_index(
                        ("V", first_two + (logical,), logical, phase)
                    ): F(1)
                    for logical in range(2)
                }
            )
    output.extend(local_plane_graph_directions())
    output.append(
        {
            chart_index(("logical", 0)): F(1),
            chart_index(("logical", 1)): F(1),
        }
    )
    assert len(output) == 37
    return output


def load_spinflip_directions():
    path = HERE / "verify_n3_boundary_spinflip_tangent.py"
    spec = importlib.util.spec_from_file_location("n3_spinflip", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.spinflip_chart_directions()


def matrix_vector(matrix, vector):
    return [
        sum(
            (matrix[row][column] * vector.get(column, 0)
             for column in range(len(matrix))),
            F(0),
        )
        for row in range(len(matrix))
    ]


def main():
    # The base is an exact equality point and is critical in the full chart.
    assert deficit_pairing(derive.BASE, derive.BASE) == derive.ZERO
    assert all(
        linear_coefficient(index) == 0
        for index in range(len(derive.COORDINATES))
    )

    hessian = derive_hessian()
    components = derive.connected_components(hessian)
    profile = Counter()
    total_rank = 0
    for component in components:
        block = [
            [hessian[row][column] for column in component]
            for row in component
        ]
        rank = positive_rank(block)
        total_rank += rank
        profile[
            (
                len(component),
                rank,
                tuple(sorted({hessian[index][index] for index in component})),
            )
        ] += 1

    expected = Counter(
        {
            (1, 1, (F(1, 3),)): 48,
            (1, 1, (F(2, 3),)): 48,
            (1, 1, (F(2, 9),)): 8,
            (1, 1, (F(4, 3),)): 2,
            (2, 1, (F(1, 3),)): 21,
            (2, 1, (F(2, 3),)): 4,
            (2, 1, (F(2, 9),)): 4,
            (2, 2, (F(2, 9),)): 8,
            (4, 2, (F(2, 9),)): 4,
            (4, 3, (F(2, 9),)): 2,
        }
    )
    assert profile == expected
    assert total_rank == 165

    kernel = nullspace(hessian)
    assert len(kernel) == 39
    assert all(
        all(value == 0 for value in matrix_vector(hessian, vector))
        for vector in kernel
    )

    # A zero-Hessian direction can leak the left frame out of the fixed
    # third-site qubit only through the four coordinates induced by moving
    # that qubit plane itself.
    leakage = {
        index
        for index, label in enumerate(derive.LABELS)
        if (
            label[0] == "U"
            and isinstance(label[1], tuple)
            and label[1][2] == 2
        )
    }
    graph_leakage = {
        chart_index(("U", (0, 0, 2), logical, phase))
        for logical in range(2)
        for phase in ("real", "imag")
    }
    assert len(leakage) == 36
    assert len(graph_leakage) == 4
    assert all(
        all(
            index in graph_leakage or vector.get(index, 0) == 0
            for index in leakage
        )
        for vector in kernel
    )
    restricted = [
        {index: vector.get(index, 0) for index in graph_leakage
         if vector.get(index, 0)}
        for vector in kernel
    ]
    assert len(rref(restricted, len(derive.COORDINATES))) == 4

    graph = local_plane_graph_directions()
    assert len(rref(graph, len(derive.COORDINATES))) == 4
    assert all(
        all(value == 0 for value in matrix_vector(hessian, direction))
        for direction in graph
    )

    # The entire flat space is already generated, to first order, by the
    # two known exact-zero mechanisms.  The full Q3-zero tangents each
    # have dimension 37; imposing the pair-deficit Hessian leaves
    # dimensions 21 and 35, and their sum is the complete 39D kernel.
    factorized = factorized_zero_directions()
    spinflip = load_spinflip_directions()
    dimension = len(derive.COORDINATES)
    assert len(rref(factorized, dimension)) == 37
    assert len(rref(spinflip, dimension)) == 37
    factorized_flat = intersection(factorized, kernel, dimension)
    spinflip_flat = intersection(spinflip, kernel, dimension)
    assert len(factorized_flat) == 21
    assert len(spinflip_flat) == 35
    assert len(rref(factorized_flat + spinflip_flat, dimension)) == 39
    assert len(rref(kernel + factorized_flat + spinflip_flat, dimension)) == 39

    # At site three the base left and right support reductions are both
    # diag(1,1,0).  In a polar-frame direction, the t^2 coefficient of
    # their determinants is the squared norm of the local-|2> leakage
    # after removing the common-plane graph motions.  These are exactly
    # the following 64 real coordinates.  Every one is an isolated
    # Hessian block, with coefficient at least 2/9.  Thus the pair
    # deficit controls the determinant opening of both missing qutrit
    # directions to second order, with sharp constant 2/9.
    opening = genuine_third_site_opening_indices()
    assert len(opening) == 64
    assert all(
        all(
            column == index or hessian[index][column] == 0
            for column in range(dimension)
        )
        for index in opening
    )
    opening_diagonal = {hessian[index][index] for index in opening}
    assert opening_diagonal == {F(2, 9), F(1, 3), F(2, 3)}
    assert min(opening_diagonal) == F(2, 9)

    print(
        "verified exact pair-boundary Hessian:",
        "dimension 204, rank 165, nullity 39, PSD;",
        "36 left support-leakage coordinates,",
        "only the 4 common-plane graph directions survive in the kernel;",
        "flat space = span of 21D factor and 35D spin-flip flat tangents;",
        "sharp second-order support-determinant constant 2/9",
    )


if __name__ == "__main__":
    main()
