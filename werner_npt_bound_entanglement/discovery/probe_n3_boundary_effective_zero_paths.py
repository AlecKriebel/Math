#!/usr/bin/env python3
"""Probe exact higher-order paths on the effective-quartic zero variety.

For a kernel vector k, the order-t^2 positive-Hessian correction is

    p_j(k) = -ell_j(k)/(2 h_j).

This script inserts z(t)=t k+t^2 p(k) into the exact polar Stiefel chart
and computes Q3 coefficient-by-coefficient with Gaussian-rational
arithmetic.  It is intended to identify the first unresolved order on
the common-zero variety of the effective quartic SOS.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import importlib.util
import os
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


effective = load(
    "effective_quartic", "build_n3_boundary_effective_quartic.py"
)
zero_analysis = load(
    "effective_zeros", "analyze_n3_boundary_effective_zero_variety.py"
)
boundary = effective.boundary
EFFECTIVE_DATA = None

Polynomial = effective.Polynomial
Frame = effective.Frame
MatrixSeries = effective.MatrixSeries
ZERO = effective.ZERO


def truncate(polynomial: Polynomial, order: int) -> Polynomial:
    return {
        monomial: coefficient
        for monomial, coefficient in polynomial.items()
        if len(monomial) <= order
    }


def multiply(first: Polynomial, second: Polynomial, order: int):
    return truncate(effective.pmultiply(first, second), order)


def matrix_identity():
    return [
        [effective.polynomial_constant(1 if i == j else 0) for j in range(2)]
        for i in range(2)
    ]


def matrix_multiply(first, second, order):
    return [
        [
            sum_polynomials(
                *(
                    multiply(first[i][k], second[k][j], order)
                    for k in range(2)
                )
            )
            for j in range(2)
        ]
        for i in range(2)
    ]


def sum_polynomials(*polynomials):
    output = {}
    for polynomial in polynomials:
        output = effective.padd(output, polynomial)
    return output


def frame_sum(*frames):
    output = {}
    for frame in frames:
        for key, value in frame.items():
            effective.frame_add(output, key, value)
    return output


def frame_multiply(frame, matrix, order):
    output = {}
    for (row, first), value in frame.items():
        for second in range(2):
            term = multiply(value, matrix[first][second], order)
            effective.frame_add(output, (row, second), term)
    return output


def coordinate_frame(coordinates_by_degree, side):
    frame = {}
    for degree, coordinates in coordinates_by_degree.items():
        monomial = (0,) * degree
        for coordinate, rational in coordinates.items():
            source = boundary.COORDINATES[coordinate][side]
            for key, value in source.items():
                coefficient = effective.gmul(
                    (rational, Fraction(0)),
                    effective.gaussian(value),
                )
                effective.frame_add(
                    frame,
                    key,
                    {monomial: coefficient},
                )
    return frame


def inverse_square_root(gram, order):
    output = matrix_identity()
    power = matrix_identity()
    coefficient = Fraction(1)
    for index in range(1, order // 2 + 1):
        power = matrix_multiply(power, gram, order)
        coefficient *= -Fraction(2 * index - 1, 2 * index)
        for i in range(2):
            for j in range(2):
                output[i][j] = effective.padd(
                    output[i][j],
                    effective.pscale(power[i][j], coefficient),
                )
    return output


def polar_frame(base_strings, variation, order):
    base = effective.base_frame(base_strings)
    gram = effective.gram(variation)
    inverse = inverse_square_root(gram, order)
    return frame_multiply(frame_sum(base, variation), inverse, order)


def partial_trace(matrix: MatrixSeries, traced):
    output = {}
    kept = tuple(index for index in range(3) if index not in traced)
    for (row, column), polynomial in matrix.items():
        if not all(row[index] == column[index] for index in traced):
            continue
        key = (
            tuple(row[index] for index in kept),
            tuple(column[index] for index in kept),
        )
        effective.matrix_add(output, key, polynomial)
    return output


def norm_squared(matrix, order):
    output = {}
    for polynomial in matrix.values():
        output = effective.padd(
            output,
            multiply(effective.pconjugate(polynomial), polynomial, order),
        )
    return output


def q_series(kernel_values, order):
    global EFFECTIVE_DATA
    if EFFECTIVE_DATA is None:
        EFFECTIVE_DATA = effective.build()
    kernel, pivots, forms, _ = EFFECTIVE_DATA
    hessian = boundary.hessian()

    first_order = defaultdict(Fraction)
    for variable, value in kernel_values.items():
        for coordinate, coefficient in kernel[variable].items():
            first_order[coordinate] += value * coefficient

    second_order = {}
    for pivot, form in zip(pivots, forms):
        ell = sum(
            coefficient
            * kernel_values.get(first, 0)
            * kernel_values.get(second, 0)
            for (first, second), coefficient in form.items()
        )
        value = -ell / (2 * hessian[pivot][pivot])
        if value:
            second_order[pivot] = value

    left_variation = coordinate_frame(
        {1: first_order, 2: second_order}, 0
    )
    right_variation = coordinate_frame(
        {1: first_order, 2: second_order}, 1
    )
    left = polar_frame(boundary.U0, left_variation, order)
    right = polar_frame(boundary.V0, right_variation, order)
    matrix = effective.outer(left, right)

    q = {}
    for mask in range(8):
        traced = tuple(index for index in range(3) if (mask >> index) & 1)
        reduced = partial_trace(matrix, traced)
        contribution = effective.pscale(
            norm_squared(reduced, order),
            Fraction(-1, 2) ** len(traced),
        )
        q = effective.padd(q, contribution)
    coefficients = []
    for degree in range(order + 1):
        real, imaginary = q.get((0,) * degree, ZERO)
        assert imaginary == 0
        coefficients.append(real)
    return tuple(coefficients), dict(first_order), second_order


def evaluate_quartic(polynomial, values):
    return sum(
        coefficient
        * product(values.get(index, 0) for index in monomial)
        for monomial, coefficient in polynomial.items()
    )


def product(values):
    output = Fraction(1)
    for value in values:
        output *= value
    return output


def main():
    dimension, _, _, equations = zero_analysis.reconstruct()
    maximum = zero_analysis.maximum_coordinate_subspace(
        dimension, equations
    )
    global EFFECTIVE_DATA
    EFFECTIVE_DATA = effective.build()
    _, _, _, effective_quartic = EFFECTIVE_DATA
    print("coordinate zero subspace", maximum)
    random.seed(20260729)
    first_nonzero_profile = defaultdict(int)
    for sample in range(int(os.environ.get("N3_ZERO_PATH_SAMPLES", "3"))):
        values = {
            index: Fraction(random.randint(-2, 2))
            for index in maximum
        }
        values = {index: value for index, value in values.items() if value}
        assert evaluate_quartic(effective_quartic, values) == 0
        coefficients, first, second = q_series(values, 12)
        first_nonzero = next(
            (
                (degree, value)
                for degree, value in enumerate(coefficients)
                if value
            ),
            None,
        )
        first_nonzero_profile[
            None if first_nonzero is None else first_nonzero[0]
        ] += 1
        print(
            "sample",
            sample,
            "kernel support",
            len(values),
            "first-order support",
            len(first),
            "second-order support",
            len(second),
            "first nonzero",
            first_nonzero,
        )
    print("first nonzero order profile", dict(first_nonzero_profile))

    print("four exact zero components: LS-corrected higher-order probes")
    for component_number, rows in enumerate(
        zero_analysis.effective_zero_component_rows()
    ):
        directions = zero_analysis.nullspace_directions(rows)
        profile = defaultdict(int)
        for sample in range(3):
            values = defaultdict(Fraction)
            for direction in directions:
                coefficient = Fraction(random.randint(-2, 2))
                for index, value in direction.items():
                    values[index] += coefficient * value
            values = {
                index: value for index, value in values.items() if value
            }
            assert evaluate_quartic(effective_quartic, values) == 0
            coefficients, _, _ = q_series(values, 10)
            first_nonzero = next(
                (
                    (degree, value)
                    for degree, value in enumerate(coefficients)
                    if value
                ),
                None,
            )
            profile[
                None if first_nonzero is None else first_nonzero[0]
            ] += 1
            print(
                " component",
                component_number,
                "sample",
                sample,
                "first nonzero",
                first_nonzero,
            )
        print(" component", component_number, "profile", dict(profile))


if __name__ == "__main__":
    main()
