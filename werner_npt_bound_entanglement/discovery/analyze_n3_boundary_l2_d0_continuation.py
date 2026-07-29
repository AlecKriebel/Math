#!/usr/bin/env python3
"""Continue a generic d=0 direction on L2 beyond order six.

This exact discovery calculation solves the positive-definite
177-variable secondary problem and inserts its unique minimizer into
the polar Stiefel series.  It then reports higher Taylor coefficients
of Q3 with all later chart coefficients set to zero.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import importlib.util
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
SECONDARY_PATH = HERE / "analyze_n3_boundary_secondary_ls.py"
SPEC = importlib.util.spec_from_file_location("secondary", SECONDARY_PATH)
secondary = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(secondary)


def optimized_series(coefficients, order):
    kernel, pivots, mixed_forms, _ = secondary.primary_data()
    hessian = secondary.boundary.hessian()
    rows = secondary.zero_analysis.effective_zero_component_rows()[2]
    component_basis = secondary.zero_analysis.nullspace_directions(rows)

    kernel_values = defaultdict(Fraction)
    for coefficient, direction in zip(coefficients, component_basis):
        for index, value in direction.items():
            kernel_values[index] += Fraction(coefficient) * value
    kernel_values = {
        index: value for index, value in kernel_values.items() if value
    }

    first_original = defaultdict(Fraction)
    for variable_index, value in kernel_values.items():
        for coordinate, coefficient in kernel[variable_index].items():
            first_original[coordinate] += value * coefficient

    second_positive = {}
    for pivot, form in zip(pivots, mixed_forms):
        ell = sum(
            coefficient
            * kernel_values.get(first, 0)
            * kernel_values.get(second, 0)
            for (first, second), coefficient in form.items()
        )
        value = -ell / (2 * hessian[pivot][pivot])
        if value:
            second_positive[pivot] = value

    *_, variable_count, polynomial = secondary.build_problem(
        2, coefficients
    )
    constant, linear, matrix = secondary.quadratic_data(
        variable_count, polynomial
    )
    solved_linear, pivots_ldl = secondary.exact_ldl_solve(matrix, linear)
    assert all(value > 0 for value in pivots_ldl)
    minimizer = [-value / 2 for value in solved_linear]
    minimum = (
        constant
        + sum(
            linear[index] * minimizer[index]
            for index in range(variable_count)
        )
        + sum(
            matrix[row][column] * minimizer[row] * minimizer[column]
            for row in range(variable_count)
            for column in range(variable_count)
        )
    )

    normal_kernel = secondary.component_complement(rows)
    second_original = defaultdict(Fraction, second_positive)
    for value, kernel_coordinate in zip(
        minimizer[: len(normal_kernel)], normal_kernel
    ):
        for coordinate, coefficient in kernel[kernel_coordinate].items():
            second_original[coordinate] += value * coefficient
    third_original = {
        pivot: minimizer[len(normal_kernel) + number]
        for number, pivot in enumerate(pivots)
        if minimizer[len(normal_kernel) + number]
    }

    left_one, right_one = secondary.coordinate_frame(first_original, [])
    left_two, right_two = secondary.coordinate_frame(second_original, [])
    left_three, right_three = secondary.coordinate_frame(third_original, [])
    blank = {}
    left_series = secondary.polar_frame_series(
        secondary.boundary.U0,
        [blank, left_one, left_two, left_three],
        order=order,
    )
    right_series = secondary.polar_frame_series(
        secondary.boundary.V0,
        [blank, right_one, right_two, right_three],
        order=order,
    )
    return (
        minimum,
        left_series,
        right_series,
        (left_one, left_two, left_three),
        (right_one, right_two, right_three),
    )


def canonical_coefficients(z, w):
    coefficients = [Fraction(0) for _ in range(27)]
    coefficients[4] = Fraction(w[0])
    coefficients[6] = Fraction(w[1])
    coefficients[8:12] = [Fraction(value) for value in w[2:]]
    coefficients[14] = Fraction(z[0], 2)
    coefficients[15] = Fraction(z[0], 2)
    coefficients[16] = Fraction(z[1], 2)
    coefficients[17] = Fraction(-z[1], 2)
    return coefficients


def main():
    order = int(os.environ.get("N3_D0_ORDER", "12"))
    coefficients = canonical_coefficients(
        z=(1, 0),
        w=(1, -2, 3, 1, -1, 2),
    )
    minimum, left_series, right_series, _, _ = optimized_series(
        coefficients, order
    )
    print("secondary minimum", minimum)
    for degree in range(4, order + 1):
        polynomial = secondary.q_polynomial_at_order(
            left_series, right_series, degree
        )
        print(
            "degree",
            degree,
            "coefficient",
            polynomial.get((), Fraction(0)),
        )


if __name__ == "__main__":
    main()
