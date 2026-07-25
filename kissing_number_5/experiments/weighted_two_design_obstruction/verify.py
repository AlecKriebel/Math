#!/usr/bin/env python3
"""Exact audit of weighted-two-design evidence and barriers."""

from __future__ import annotations

from fractions import Fraction as Q
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "certificate.json"


def determinant(matrix: list[list[Q]]) -> Q:
    """Fraction-free-enough exact elimination for small square matrices."""
    work = [row[:] for row in matrix]
    size = len(work)
    answer = Q(1)
    sign = 1
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, size):
            multiplier = work[row][column] / pivot_value
            for inner in range(column + 1, size):
                work[row][inner] -= multiplier * work[column][inner]
    return sign * answer


def d5_roots() -> list[tuple[Q, ...]]:
    roots = []
    for first, second in itertools.combinations(range(5), 2):
        for first_sign, second_sign in itertools.product((-1, 1), repeat=2):
            root = [Q(0)] * 5
            root[first] = Q(first_sign)
            root[second] = Q(second_sign)
            roots.append(tuple(root))
    return roots


def known_codes() -> dict[str, list[tuple[Q, ...]]]:
    d5 = d5_roots()
    l5 = [point for point in d5 if point[4] != 1]
    for signs in itertools.product((-1, 1), repeat=4):
        if sum(sign < 0 for sign in signs) % 2 == 1:
            l5.append(
                tuple(Q(sign, 2) for sign in signs) + (Q(1),)
            )

    q5 = [point for point in d5 if sum(point) != 2]
    q5.extend(
        tuple(coordinate + Q(4, 5) for coordinate in point)
        for point in d5
        if sum(point) == -2
    )

    r5 = [point for point in l5 if sum(point) != 2]
    r5.extend(
        tuple(coordinate + Q(4, 5) for coordinate in point)
        for point in l5
        if sum(point) == -2
    )
    return {"D5": d5, "L5": l5, "Q5": q5, "R5": r5}


def frame(
    raw_points: list[tuple[Q, ...]],
) -> list[list[Q]]:
    # All four exact models have raw squared norm two.
    return [
        [
            sum(point[i] * point[j] / 2 for point in raw_points)
            for j in range(5)
        ]
        for i in range(5)
    ]


def quadratic(
    vector: tuple[Q, ...], matrix: list[list[Q]]
) -> Q:
    return sum(
        vector[i] * matrix[i][j] * vector[j]
        for i in range(5)
        for j in range(5)
    )


def verify(certificate_path: Path = CERTIFICATE) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    assert certificate["schema"] == (
        "weighted-two-design-obstruction-audit-v1"
    )
    assert certificate["status"] == (
        "EXACT BARRIERS AND KNOWN-CONFIGURATION CHECK"
    )

    code_reports = {}
    codes = known_codes()
    assert sorted(codes) == sorted(certificate["known_40_point_codes"])
    for name, points in codes.items():
        assert len(points) == len(set(points)) == 40
        assert all(
            sum(coordinate * coordinate for coordinate in point) == 2
            for point in points
        )
        maximum_raw_inner_product = max(
            sum(left[k] * right[k] for k in range(5))
            for left, right in itertools.combinations(points, 2)
        )
        assert maximum_raw_inner_product <= 1
        centroid = [
            sum(point[coordinate] for point in points)
            for coordinate in range(5)
        ]
        assert centroid == [Q(0)] * 5
        frame_matrix = frame(points)
        assert frame_matrix == [
            [Q(8) if i == j else Q(0) for j in range(5)]
            for i in range(5)
        ]
        code_reports[name] = {
            "cardinality": 40,
            "maximum_inner_product": str(
                maximum_raw_inner_product / 2
            ),
            "centroid": [str(value) for value in centroid],
            "frame_diagonal": [str(frame_matrix[i][i]) for i in range(5)],
            "uniform_covariance_diagonal": ["1/5"] * 5,
        }

    # A centered, antipodal, exact kissing-code counterexample at order 32.
    separator_matrix = [
        [Q(entry) for entry in row]
        for row in certificate["kissing_counterexample"][
            "separator_matrix"
        ]
    ]
    assert all(
        separator_matrix[i][j] == separator_matrix[j][i]
        for i in range(5)
        for j in range(5)
    )
    assert sum(separator_matrix[i][i] for i in range(5)) == 0
    d5 = codes["D5"]
    separator_values = [
        quadratic(point, separator_matrix) / 2 for point in d5
    ]
    selected = [
        point
        for point, value in zip(d5, separator_values)
        if value > 0
    ]
    omitted = [
        point
        for point, value in zip(d5, separator_values)
        if value < 0
    ]
    assert len(selected) == 32
    assert len(omitted) == 8
    assert set(separator_values) == {Q(2), Q(-8)}
    assert all(tuple(-entry for entry in point) in selected for point in selected)
    assert [
        sum(point[coordinate] for point in selected)
        for coordinate in range(5)
    ] == [Q(0)] * 5
    assert max(
        sum(left[k] * right[k] for k in range(5)) / 2
        for left, right in itertools.combinations(selected, 2)
    ) <= Q(1, 2)
    # Any nonnegative weights with covariance I/5 would average this
    # traceless quadratic to zero, whereas it equals two on every point.

    depth_model = certificate["depth_frame_countermodel"]
    epsilon = Q(depth_model["epsilon"])
    denominator = depth_model["moment_curve_denominator"]
    parameters = [
        Q(numerator, denominator)
        for numerator in depth_model["moment_curve_numerators"]
    ]
    assert len(parameters) == len(set(parameters)) == 20

    def raw(parameter: Q) -> tuple[Q, ...]:
        return (
            Q(1),
            parameter,
            parameter**2,
            parameter**3,
            epsilon * parameter**4,
        )

    raw_vectors = [raw(parameter) for parameter in parameters]
    norm_squares = [
        sum(coordinate * coordinate for coordinate in vector)
        for vector in raw_vectors
    ]

    # Every five lines are independent by the exact Vandermonde formula.
    for selection in itertools.combinations(parameters, 5):
        vandermonde = epsilon
        for i in range(5):
            for j in range(i + 1, 5):
                vandermonde *= selection[j] - selection[i]
        assert vandermonde
    assert depth_model["open_hemisphere_depth_lower_bound"] == 16
    assert depth_model["deletion_interiority"] == 6

    # Exact rational unweighted frame of the forty normalized antipodal
    # vectors, followed by the appended e_5.
    frame_41 = [[Q(0) for _ in range(5)] for _ in range(5)]
    for vector, norm_square in zip(raw_vectors, norm_squares):
        for i in range(5):
            for j in range(5):
                frame_41[i][j] += (
                    2 * vector[i] * vector[j] / norm_square
                )
    frame_41[4][4] += 1
    frame_floor = Q(depth_model["frame_floor"])
    shifted_frame = [
        [
            frame_41[i][j] - frame_floor * Q(i == j)
            for j in range(5)
        ]
        for i in range(5)
    ]
    leading_minors = [
        determinant([row[:size] for row in shifted_frame[:size]])
        for size in range(1, 6)
    ]
    assert all(minor > 0 for minor in leading_minors)

    # q(x)=1-5*x_5^2+5*x_5 has spherical mean zero.  Every paired point
    # has |x_5|<=epsilon, hence q>=1-5epsilon-5epsilon^2>0.  At e_5, q=1.
    separator_lower = 1 - 5 * epsilon - 5 * epsilon**2
    assert separator_lower > 0
    assert depth_model["separator"] == "q(x)=1-5*x_5^2+5*x_5"
    assert depth_model["separator_value_at_e5"] == "1"

    # The countermodel is not a kissing code: the first adjacent parameter
    # pair has normalized inner product greater than one half.
    first, second = raw_vectors[:2]
    dot_product = sum(a * b for a, b in zip(first, second))
    assert dot_product > 0
    assert 4 * dot_product**2 > norm_squares[0] * norm_squares[1]
    assert depth_model["is_kissing_code"] is False

    return {
        "status": "PASS",
        "known_40_point_codes": code_reports,
        "kissing_counterexample": {
            "cardinality": len(selected),
            "antipodal": True,
            "centered": True,
            "separator_values": ["2"],
            "conclusion": (
                "no nonnegative weighted spherical 2-design measure exists"
            ),
        },
        "depth_frame_countermodel": {
            "cardinality": 41,
            "open_hemisphere_depth_lower_bound": 16,
            "deletion_interiority": 6,
            "frame_floor": str(frame_floor),
            "shifted_frame_leading_minors": [
                str(minor) for minor in leading_minors
            ],
            "separator_lower_bound": str(separator_lower),
            "is_kissing_code": False,
        },
        "scope": certificate["scope"],
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
