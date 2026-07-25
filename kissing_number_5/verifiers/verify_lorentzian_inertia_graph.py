#!/usr/bin/env python3
"""Exact checks for the Lorentzian rank/sign investigation.

The certificate deliberately is *not* a 41-point kissing code.  It gives
an exact order-41 matrix satisfying the tempting rank, inertia, sign, entry
interval, graph-degree, and oriented-matroid surrogates while failing the
essential PSD lift ``(A + J)/2 >= 0``.

Only Python's standard library is used.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT / "certificates" / "lorentzian_rank6_interval_countermodel.json"
)


def determinant(matrix: list[list[int]]) -> int:
    """Exact determinant by fraction-free Bareiss elimination."""

    n = len(matrix)
    assert all(len(row) == n for row in matrix)
    if n == 0:
        return 1
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for column in range(n - 1):
        pivot = next(
            (row for row in range(column, n) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        pivot_value = work[column][column]
        for row in range(column + 1, n):
            for other_column in range(column + 1, n):
                numerator = (
                    work[row][other_column] * pivot_value
                    - work[row][column] * work[column][other_column]
                )
                assert numerator % previous == 0
                work[row][other_column] = numerator // previous
            work[row][column] = 0
        previous = pivot_value
    return sign * work[-1][-1]


def rational_rank(matrix: list[list[int | Fraction]]) -> int:
    """Rank over Q by a small, transparent Gaussian elimination."""

    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(
                    work[row], work[rank], strict=True
                )
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def stereographic_integer_points(
    denominator: int, numerators: list[list[int]]
) -> tuple[list[tuple[int, ...]], list[int]]:
    """Return homogeneous integer representatives v_i/D_i on S^4."""

    points: list[tuple[int, ...]] = []
    row_denominators: list[int] = []
    denominator_squared = denominator * denominator
    for parameters in numerators:
        assert len(parameters) == 4
        norm_squared = sum(value * value for value in parameters)
        row_denominator = denominator_squared + norm_squared
        point = tuple(
            [2 * denominator * value for value in parameters]
            + [denominator_squared - norm_squared]
        )
        assert sum(value * value for value in point) == row_denominator**2
        points.append(point)
        row_denominators.append(row_denominator)
    return points, row_denominators


def inner_numerator(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def cofactor_null_vector(rows: list[tuple[int, ...]]) -> tuple[int, ...]:
    """A normal to four rows in Q^5, using signed 4-by-4 minors."""

    assert len(rows) == 4
    assert all(len(row) == 5 for row in rows)
    return tuple(
        (-1) ** column
        * determinant(
            [
                [
                    rows[row][other_column]
                    for other_column in range(5)
                    if other_column != column
                ]
                for row in range(4)
            ]
        )
        for column in range(5)
    )


def circuit_coefficients(
    support: list[int],
    points: list[tuple[int, ...]],
    denominators: list[int],
) -> tuple[int, ...]:
    """Integer-scaled coefficients of the unique dependence on six points."""

    assert len(support) == 6
    columns = [points[index] for index in support]
    beta = []
    for removed in range(6):
        square = [
            [
                columns[column][row]
                for column in range(6)
                if column != removed
            ]
            for row in range(5)
        ]
        beta.append((-1) ** removed * determinant(square))

    # beta is a dependence among the homogeneous integer numerators.
    for coordinate in range(5):
        assert (
            sum(
                beta[position] * points[index][coordinate]
                for position, index in enumerate(support)
            )
            == 0
        )

    # Since y_i=v_i/D_i, alpha_i=beta_i D_i is a dependence
    # among the rational unit vectors.
    alpha = tuple(
        beta[position] * denominators[index]
        for position, index in enumerate(support)
    )
    if all(value < 0 for value in alpha):
        alpha = tuple(-value for value in alpha)
    assert all(value > 0 for value in alpha)
    return alpha


def verify_depth(
    points: list[tuple[int, ...]],
) -> tuple[int, tuple[int, ...], int, int]:
    """Enumerate central hyperplanes and return exact open Tukey depth.

    Every four points are checked to be independent, and every hyperplane
    they span is checked to contain exactly those four points.  In this
    central general position, rotating a hyperplane until it first acquires
    four boundary points cannot increase its smaller open side.  Hence this
    finite enumeration covers every open origin hemisphere.
    """

    minimum = len(points)
    witness: tuple[int, ...] | None = None
    witness_positive = 0
    witness_negative = 0
    for support in itertools.combinations(range(len(points)), 4):
        normal = cofactor_null_vector([points[index] for index in support])
        assert any(normal)
        signs = [
            sum(a * b for a, b in zip(normal, point, strict=True))
            for point in points
        ]
        zero_indices = tuple(
            index for index, value in enumerate(signs) if value == 0
        )
        assert zero_indices == support
        positive = sum(value > 0 for value in signs)
        negative = sum(value < 0 for value in signs)
        current = min(positive, negative)
        if current < minimum:
            minimum = current
            witness = support
            witness_positive = positive
            witness_negative = negative
    assert witness is not None
    return minimum, witness, witness_positive, witness_negative


def fraction_pair(pair: Iterable[int]) -> Fraction:
    numerator, denominator = pair
    return Fraction(numerator, denominator)


def verify_d5_calibration() -> dict[str, object]:
    """Check the spectral normalization on the exact 40-root D5 code."""

    roots = []
    for first_coordinate, second_coordinate in itertools.combinations(
        range(5), 2
    ):
        for first_sign in (-1, 1):
            for second_sign in (-1, 1):
                root = [0] * 5
                root[first_coordinate] = first_sign
                root[second_coordinate] = second_sign
                roots.append(tuple(root))
    assert len(roots) == 40

    # Normalized roots are root/sqrt(2), so A_ij=root_i.root_j-1.
    a_matrix = [
        [
            inner_numerator(left, right) - 1
            for right in roots
        ]
        for left in roots
    ]
    w_matrix = [
        [
            (1 if row == column else 0) - a_matrix[row][column]
            for column in range(40)
        ]
        for row in range(40)
    ]
    assert all(a_matrix[index][index] == 1 for index in range(40))
    assert all(
        a_matrix[left][right] <= 0
        for left, right in itertools.combinations(range(40), 2)
    )
    row_sums = [sum(row) for row in w_matrix]
    assert row_sums == [41] * 40

    trace_w_squared = sum(
        w_matrix[row][column] * w_matrix[column][row]
        for row in range(40)
        for column in range(40)
    )
    trace_w_cubed = sum(
        w_matrix[first][second]
        * w_matrix[second][third]
        * w_matrix[third][first]
        for first in range(40)
        for second in range(40)
        for third in range(40)
    )
    assert trace_w_squared == 41**2 + 34 + 5 * 15**2 == 2840
    assert trace_w_cubed == 41**3 + 34 - 5 * 15**3 == 52080
    return {
        "D5_W_Perron_root": 41,
        "D5_W_spectrum": "41^1, 1^34, (-15)^5",
        "D5_trace_W_squared": trace_w_squared,
        "D5_trace_W_cubed": trace_w_cubed,
    }


def verify(*, check_depth: bool = True) -> dict[str, object]:
    data = json.loads(CERTIFICATE.read_text())
    assert data["schema"] == (
        "kissing5.lorentzian_rank6_interval_countermodel.v1"
    )
    q = int(data["stereographic_denominator"])
    points, denominators = stereographic_integer_points(
        q, data["stereographic_numerators"]
    )
    number = len(points)
    assert number == 41
    assert all(len(point) == 5 for point in points)

    lower = fraction_pair(data["claimed_inner_product_interval"]["lower"])
    upper = fraction_pair(data["claimed_inner_product_interval"]["upper"])
    scale = fraction_pair(data["scale_s"])
    assert lower == 4 * scale - 3 == Fraction(-9, 10)
    assert upper == scale == Fraction(21, 40)
    critical_shift = scale / (1 - scale)
    assert critical_shift == Fraction(21, 19)

    minimum_inner: Fraction | None = None
    maximum_inner: Fraction | None = None
    minimum_pair: tuple[int, int] | None = None
    maximum_pair: tuple[int, int] | None = None
    negative_pseudo_degrees = [0] * number
    contact_edges = 0
    total_w_weight = Fraction(0)
    for left, right in itertools.combinations(range(number), 2):
        numerator = inner_numerator(points[left], points[right])
        denominator = denominators[left] * denominators[right]
        value = Fraction(numerator, denominator)
        assert lower < value < upper
        if minimum_inner is None or value < minimum_inner:
            minimum_inner = value
            minimum_pair = (left, right)
        if maximum_inner is None or value > maximum_inner:
            maximum_inner = value
            maximum_pair = (left, right)

        # H=(A+J)/2=(20K-J)/19 is negative exactly when K<1/20.
        if 20 * numerator < denominator:
            negative_pseudo_degrees[left] += 1
            negative_pseudo_degrees[right] += 1

        # H_ij=1/2 exactly when K_ij=21/40.
        if 40 * numerator == 21 * denominator:
            contact_edges += 1

        # A=(40K-21J)/19 has all off-diagonal entries in [-3,0).
        a_numerator = 40 * numerator - 21 * denominator
        assert -57 * denominator < a_numerator < 0
        total_w_weight += 2 * Fraction(-a_numerator, 19 * denominator)

        # The pseudo-Gram H has every scalar entry in [-1,1/2).
        h_numerator = 20 * numerator - denominator
        assert -19 * denominator < h_numerator
        assert 2 * h_numerator < 19 * denominator

    assert minimum_inner is not None and maximum_inner is not None
    assert maximum_inner > Fraction(1, 2)
    assert contact_edges == 0
    assert min(negative_pseudo_degrees) == int(
        data["claimed_minimum_negative_pseudo_inner_product_degree"]
    )
    all_ones_w_rayleigh = total_w_weight / number
    assert all_ones_w_rayleigh > 46

    # Positive row rescaling does not change coordinate or affine rank.
    coordinate_matrix = [
        [points[column][row] for column in range(number)]
        for row in range(5)
    ]
    affine_matrix = coordinate_matrix + [denominators]
    coordinate_rank = rational_rank(coordinate_matrix)
    affine_rank = rational_rank(affine_matrix)
    assert coordinate_rank == 5
    assert affine_rank == 6

    # Consequently K=Y^T Y has rank 5 and 1 is outside its range.  Both
    # A=(K-sJ)/(1-s) and H=(20K-J)/19 have inertia (5,1,35) and rank 6:
    # in a basis splitting range(K) from its kernel, subtracting a positive
    # multiple of J with 1 outside range(K) creates exactly one negative
    # direction and raises rank by one.
    a_rank = 6
    a_inertia = (5, 1, 35)
    h_rank = 6
    h_inertia = (5, 1, 35)

    circuit_summaries = []
    seen: set[int] = set()
    for support in data["disjoint_positive_circuit_supports_zero_based"]:
        assert not seen.intersection(support)
        seen.update(support)
        alpha = circuit_coefficients(support, points, denominators)
        circuit_summaries.append(
            {
                "support": support,
                "all_coefficients_strictly_positive": True,
                "minimum_coefficient_bit_length": min(alpha).bit_length(),
                "maximum_coefficient_bit_length": max(alpha).bit_length(),
            }
        )

    # A concrete exact negative vector for H.  A positive Y-circuit alpha
    # has K alpha=0 and sum(alpha)>0, so
    # alpha^T H alpha=-(sum alpha)^2/19<0.
    first_support = data["disjoint_positive_circuit_supports_zero_based"][0]
    first_alpha = circuit_coefficients(
        first_support, points, denominators
    )
    negative_h_quadratic_numerator = -(sum(first_alpha) ** 2)
    negative_h_quadratic_denominator = 19
    assert negative_h_quadratic_numerator < 0

    # The failure is already visible on one exact 3-by-3 principal minor.
    bad_triple = (22, 28, 37)
    bad_h_entries = []
    for left, right in itertools.combinations(bad_triple, 2):
        k_value = Fraction(
            inner_numerator(points[left], points[right]),
            denominators[left] * denominators[right],
        )
        bad_h_entries.append((20 * k_value - 1) / 19)
    h_12, h_13, h_23 = bad_h_entries
    bad_h_determinant = (
        1
        + 2 * h_12 * h_13 * h_23
        - h_12 * h_12
        - h_13 * h_13
        - h_23 * h_23
    )
    assert bad_h_determinant < 0

    if check_depth:
        depth, depth_support, positive, negative = verify_depth(points)
        assert depth == 14
    else:
        depth = None
        depth_support = None
        positive = None
        negative = None

    return {
        "status": "PASS",
        "number_of_points": number,
        "coordinate_rank": coordinate_rank,
        "affine_rank": affine_rank,
        "minimum_inner_product": str(minimum_inner),
        "minimum_pair": minimum_pair,
        "maximum_inner_product": str(maximum_inner),
        "maximum_pair": maximum_pair,
        "scale_s": str(scale),
        "circuit_critical_rank_one_shift": str(critical_shift),
        "A_rank": a_rank,
        "A_inertia_positive_negative_zero": a_inertia,
        "H_rank": h_rank,
        "H_inertia_positive_negative_zero": h_inertia,
        "contact_edges": contact_edges,
        "minimum_negative_pseudo_inner_product_degree": min(
            negative_pseudo_degrees
        ),
        "maximum_negative_pseudo_inner_product_degree": max(
            negative_pseudo_degrees
        ),
        "all_ones_W_rayleigh_quotient_strict_lower_bound": 46,
        "disjoint_positive_direction_circuits": circuit_summaries,
        "negative_H_circuit_witness": "-(sum(alpha))^2/19 < 0",
        "negative_H_3x3_minor_support": bad_triple,
        "negative_H_3x3_determinant": str(bad_h_determinant),
        "open_hemisphere_depth": depth,
        "depth_witness_support": depth_support,
        "depth_witness_positive_negative": (positive, negative),
        "scope": (
            "Exact countermodel to weakened Lorentzian/graph surrogates; "
            "H is indefinite and this is not a kissing code."
        ),
        "D5_calibration": verify_d5_calibration(),
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
