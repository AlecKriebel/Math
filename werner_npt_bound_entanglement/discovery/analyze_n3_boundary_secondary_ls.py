#!/usr/bin/env python3
"""Build the secondary order-six Lyapunov--Schmidt problem exactly.

Fix a rational generic first-order direction k in one of the four
linear components of {q4_eff=0}.  The order-t^2 positive-Hessian
correction p2(k) is fixed by the first Lyapunov--Schmidt step.  Write

    z(t)=t k+t^2(p2+h)+t^3 r,

where h ranges over a complement to the chosen zero component inside
the 55-dimensional primary kernel, and r ranges over the 149 positive
Hessian pivots.  The coefficient [t^6]Q3 is an exact quadratic
polynomial in (h,r).  This script constructs that polynomial directly
from the polar Stiefel chart, reports its inertia, and exactly evaluates
its Schur minimum when nonsingular.

This is discovery code; a global componentwise formula still has to
retain k symbolically.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
import importlib.util
import os
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

Gaussian = tuple[Fraction, Fraction]
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Gaussian]
Frame = dict[tuple[boundary.String, int], Polynomial]
Matrix = dict[boundary.Unit, Polynomial]

ZERO = effective.ZERO
ONE = effective.ONE
MAX_VARIABLE_DEGREE = 2


def add(first: Polynomial, second: Polynomial) -> Polynomial:
    return effective.padd(first, second)


def scale(polynomial: Polynomial, scalar) -> Polynomial:
    return effective.pscale(polynomial, scalar)


def multiply(first: Polynomial, second: Polynomial) -> Polynomial:
    output = {}
    for first_monomial, first_coefficient in first.items():
        for second_monomial, second_coefficient in second.items():
            monomial = tuple(sorted(first_monomial + second_monomial))
            if len(monomial) > MAX_VARIABLE_DEGREE:
                continue
            coefficient = effective.gmul(
                first_coefficient, second_coefficient
            )
            output[monomial] = effective.gadd(
                output.get(monomial, ZERO), coefficient
            )
            if output[monomial] == ZERO:
                del output[monomial]
    return output


def conjugate(polynomial):
    return effective.pconjugate(polynomial)


def constant(value) -> Polynomial:
    coefficient = value if isinstance(value, tuple) else effective.gaussian(value)
    return {} if coefficient == ZERO else {(): coefficient}


def variable(index, value=1) -> Polynomial:
    coefficient = value if isinstance(value, tuple) else effective.gaussian(value)
    return {} if coefficient == ZERO else {(index,): coefficient}


def sum_polynomials(*polynomials):
    output = {}
    for polynomial in polynomials:
        output = add(output, polynomial)
    return output


def add_entry(output, key, polynomial):
    output[key] = add(output.get(key, {}), polynomial)
    if not output[key]:
        del output[key]


def frame_sum(*frames):
    output = {}
    for frame in frames:
        for key, polynomial in frame.items():
            add_entry(output, key, polynomial)
    return output


def matrix_sum(*matrices):
    output = {}
    for matrix in matrices:
        for key, polynomial in matrix.items():
            add_entry(output, key, polynomial)
    return output


def base_frame(strings):
    return {
        (strings[0], 0): constant(1),
        (strings[1], 1): constant(1),
    }


def coordinate_frame(constants, variables):
    """Build a frame from original chart-coordinate data.

    ``constants`` maps original coordinate to a rational scalar.
    ``variables`` contains pairs (polynomial-variable, original sparse
    direction).
    """

    left = {}
    right = {}
    for coordinate, coefficient in constants.items():
        for side, output in ((0, left), (1, right)):
            for key, value in boundary.COORDINATES[coordinate][side].items():
                gaussian = effective.gmul(
                    (coefficient, Fraction(0)),
                    effective.gaussian(value),
                )
                add_entry(output, key, constant(gaussian))
    for polynomial_variable, direction in variables:
        for coordinate, coefficient in direction.items():
            for side, output in ((0, left), (1, right)):
                for key, value in boundary.COORDINATES[coordinate][side].items():
                    gaussian = effective.gmul(
                        (coefficient, Fraction(0)),
                        effective.gaussian(value),
                    )
                    add_entry(
                        output,
                        key,
                        variable(polynomial_variable, gaussian),
                    )
    return left, right


def frame_inner(first: Frame, second: Frame):
    output = [[{} for _ in range(2)] for _ in range(2)]
    for (row, first_logical), x in first.items():
        for (other_row, second_logical), y in second.items():
            if row == other_row:
                output[first_logical][second_logical] = add(
                    output[first_logical][second_logical],
                    multiply(conjugate(x), y),
                )
    return output


def matrix2_sum(*matrices):
    return [
        [
            sum_polynomials(
                *(matrix[row][column] for matrix in matrices)
            )
            for column in range(2)
        ]
        for row in range(2)
    ]


def matrix2_scale(matrix, scalar):
    return [
        [scale(matrix[row][column], scalar) for column in range(2)]
        for row in range(2)
    ]


def matrix2_multiply(first, second):
    return [
        [
            sum_polynomials(
                *(
                    multiply(first[row][middle], second[middle][column])
                    for middle in range(2)
                )
            )
            for column in range(2)
        ]
        for row in range(2)
    ]


def multiply_right(frame, matrix):
    output = {}
    for (row, first), polynomial in frame.items():
        for second in range(2):
            add_entry(
                output,
                (row, second),
                multiply(polynomial, matrix[first][second]),
            )
    return output


def outer(first, second):
    output = {}
    for (row, logical), x in first.items():
        for (column, other_logical), y in second.items():
            if logical == other_logical:
                add_entry(
                    output,
                    (row, column),
                    multiply(x, conjugate(y)),
                )
    return output


def polar_frame_series(base_strings, variations, order=6):
    """Polar-retract U0+sum_m t^m X_m through the requested order."""

    zero_matrix = [[{} for _ in range(2)] for _ in range(2)]
    gram = [
        [[{} for _ in range(2)] for _ in range(2)]
        for _ in range(order + 1)
    ]
    for degree in range(2, order + 1):
        gram[degree] = matrix2_sum(
            *(
                frame_inner(variations[first], variations[degree - first])
                for first in range(1, degree)
                if first < len(variations)
                and degree - first < len(variations)
                and variations[first]
                and variations[degree - first]
            )
        )

    identity = [
        [constant(1 if row == column else 0) for column in range(2)]
        for row in range(2)
    ]
    # Matrix power series
    #   (I+gram)^(-1/2)=sum_m binom(-1/2,m) gram^m.
    # Since every entry of ``gram`` starts in degree two, only
    # floor(order/2) powers are needed.  This general form agrees with
    # the earlier explicit square/cube implementation through order six
    # and also supports the order-eight continuation.
    powers = [
        [zero_matrix for _ in range(order + 1)]
        for _ in range(order // 2 + 1)
    ]
    powers[0][0] = identity
    for power in range(1, len(powers)):
        for degree in range(order + 1):
            terms = [
                matrix2_multiply(
                    powers[power - 1][first],
                    gram[degree - first],
                )
                for first in range(degree + 1)
                if any(
                    powers[power - 1][first][i][j]
                    for i in range(2)
                    for j in range(2)
                )
                and any(
                    gram[degree - first][i][j]
                    for i in range(2)
                    for j in range(2)
                )
            ]
            if terms:
                powers[power][degree] = matrix2_sum(*terms)

    binomial = [Fraction(1)]
    for power in range(1, len(powers)):
        binomial.append(
            binomial[-1] * Fraction(-(2 * power - 1), 2 * power)
        )
    inverse = [zero_matrix for _ in range(order + 1)]
    for degree in range(order + 1):
        terms = [
            matrix2_scale(powers[power][degree], binomial[power])
            for power in range(len(powers))
            if any(
                powers[power][degree][i][j]
                for i in range(2)
                for j in range(2)
            )
        ]
        if terms:
            inverse[degree] = matrix2_sum(*terms)

    sources = [base_frame(base_strings)] + variations[1:]
    output = []
    for degree in range(order + 1):
        output.append(
            frame_sum(
                *(
                    multiply_right(sources[first], inverse[degree - first])
                    for first in range(degree + 1)
                    if first < len(sources)
                    and sources[first]
                    and any(
                        inverse[degree - first][i][j]
                        for i in range(2)
                        for j in range(2)
                    )
                )
            )
        )
    return output


def partial_trace(matrix, traced):
    output = {}
    kept = tuple(index for index in range(3) if index not in traced)
    for (row, column), polynomial in matrix.items():
        if not all(row[index] == column[index] for index in traced):
            continue
        key = (
            tuple(row[index] for index in kept),
            tuple(column[index] for index in kept),
        )
        add_entry(output, key, polynomial)
    return output


def norm_pair(first, second):
    output = {}
    for key in set(first) & set(second):
        output = add(
            output,
            multiply(conjugate(first[key]), second[key]),
        )
    return output


def q_polynomial_at_order(left_series, right_series, order):
    matrices = []
    for degree in range(order + 1):
        matrices.append(
            matrix_sum(
                *(
                    outer(left_series[first], right_series[degree - first])
                    for first in range(degree + 1)
                )
            )
        )
    output = {}
    for mask in range(8):
        traced = tuple(index for index in range(3) if (mask >> index) & 1)
        reduced = [partial_trace(matrix, traced) for matrix in matrices]
        value = {}
        for first in range(order + 1):
            value = add(
                value,
                norm_pair(reduced[first], reduced[order - first]),
            )
        output = add(
            output,
            scale(value, Fraction(-1, 2) ** len(traced)),
        )
    real = {}
    for monomial, (real_part, imaginary_part) in output.items():
        assert imaginary_part == 0
        if real_part:
            real[monomial] = real_part
    return real


def q6_polynomial(left_series, right_series):
    return q_polynomial_at_order(left_series, right_series, 6)


def component_complement(rows):
    pivots = [
        min(row)
        for row in rows
    ]
    assert len(set(pivots)) == len(rows)
    return pivots


@lru_cache(maxsize=1)
def primary_data():
    return effective.build()


def build_problem(component_number, coefficients_override=None):
    kernel, pivots, mixed_forms, _ = primary_data()
    hessian = boundary.hessian()
    rows = zero_analysis.effective_zero_component_rows()[component_number]
    component_basis = zero_analysis.nullspace_directions(rows)
    encoded_coefficients = os.environ.get("N3_SECONDARY_COEFFICIENTS")
    if coefficients_override is not None:
        coefficients = [Fraction(value) for value in coefficients_override]
        assert len(coefficients) == len(component_basis)
    elif encoded_coefficients:
        coefficients = [
            Fraction(value)
            for value in encoded_coefficients.split(",")
            if value
        ]
        assert len(coefficients) == len(component_basis)
    else:
        coefficients = [
            Fraction(number % 5 - 2)
            for number in range(len(component_basis))
        ]
    kernel_values = defaultdict(Fraction)
    for coefficient, direction in zip(coefficients, component_basis):
        for index, value in direction.items():
            kernel_values[index] += coefficient * value
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

    normal_kernel_coordinates = component_complement(rows)
    variable_directions_second = [
        (number, kernel[kernel_coordinate])
        for number, kernel_coordinate in enumerate(normal_kernel_coordinates)
    ]
    positive_offset = len(variable_directions_second)
    variable_directions_third = [
        (positive_offset + number, {pivot: Fraction(1)})
        for number, pivot in enumerate(pivots)
    ]
    variable_count = positive_offset + len(pivots)

    left_one, right_one = coordinate_frame(first_original, [])
    left_two, right_two = coordinate_frame(
        second_positive, variable_directions_second
    )
    left_three, right_three = coordinate_frame(
        {}, variable_directions_third
    )
    blank = {}
    left_series = polar_frame_series(
        boundary.U0,
        [blank, left_one, left_two, left_three],
    )
    right_series = polar_frame_series(
        boundary.V0,
        [blank, right_one, right_two, right_three],
    )
    polynomial = q6_polynomial(left_series, right_series)
    return (
        kernel_values,
        normal_kernel_coordinates,
        pivots,
        variable_count,
        polynomial,
    )


def quadratic_data(variable_count, polynomial):
    constant_term = polynomial.get((), Fraction(0))
    linear = [Fraction(0) for _ in range(variable_count)]
    matrix = [
        [Fraction(0) for _ in range(variable_count)]
        for _ in range(variable_count)
    ]
    for monomial, coefficient in polynomial.items():
        if not monomial:
            continue
        if len(monomial) == 1:
            linear[monomial[0]] += coefficient
        else:
            first, second = monomial
            if first == second:
                matrix[first][first] += coefficient
            else:
                matrix[first][second] += coefficient / 2
                matrix[second][first] += coefficient / 2
    return constant_term, linear, matrix


def exact_ldl_solve(matrix, right):
    size = len(matrix)
    lower = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    pivots = []
    for first in range(size):
        lower[first][first] = 1
        pivot = matrix[first][first] - sum(
            lower[first][k] ** 2 * pivots[k] for k in range(first)
        )
        assert pivot > 0, (first, pivot)
        pivots.append(pivot)
        for second in range(first + 1, size):
            lower[second][first] = (
                matrix[second][first]
                - sum(
                    lower[second][k] * lower[first][k] * pivots[k]
                    for k in range(first)
                )
            ) / pivot
    forward = []
    for first in range(size):
        forward.append(
            right[first]
            - sum(
                lower[first][k] * forward[k] for k in range(first)
            )
        )
    diagonal = [
        value / pivot for value, pivot in zip(forward, pivots)
    ]
    solution = [Fraction(0) for _ in range(size)]
    for first in range(size - 1, -1, -1):
        solution[first] = diagonal[first] - sum(
            lower[k][first] * solution[k]
            for k in range(first + 1, size)
        )
    assert all(
        sum(matrix[row][column] * solution[column] for column in range(size))
        == right[row]
        for row in range(size)
    )
    return solution, pivots


def main():
    # NumPy is used only for the floating-point discovery report.  The
    # exact builders and LDL solver above intentionally remain
    # dependency-free so the small certificate verifier can import them.
    import numpy as np

    component = int(os.environ.get("N3_SECONDARY_COMPONENT", "1"))
    (
        kernel_values,
        normal_kernel,
        pivots,
        variable_count,
        polynomial,
    ) = build_problem(component)
    print(
        "component",
        component,
        "generic kernel support",
        len(kernel_values),
        "normal kernel directions",
        len(normal_kernel),
        "positive third-order directions",
        len(pivots),
        "quadratic variables",
        variable_count,
        "q6 terms",
        len(polynomial),
        flush=True,
    )
    constant_term, linear, matrix = quadratic_data(
        variable_count, polynomial
    )
    floating = np.asarray(
        [[float(value) for value in row] for row in matrix]
    )
    eigenvalues = np.linalg.eigvalsh(floating)
    print(
        "quadratic inertia",
        int(np.count_nonzero(eigenvalues > 1e-9)),
        int(np.count_nonzero(eigenvalues < -1e-9)),
        int(np.count_nonzero(abs(eigenvalues) <= 1e-9)),
        "min/max",
        eigenvalues[0],
        eigenvalues[-1],
    )
    linear_float = np.asarray([float(value) for value in linear])
    solution = -0.5 * np.linalg.pinv(floating, rcond=1e-11) @ linear_float
    residual = floating @ solution + 0.5 * linear_float
    minimum = (
        float(constant_term)
        + float(np.dot(linear_float, solution))
        + float(solution @ floating @ solution)
    )
    print(
        "constant",
        constant_term,
        "linear norm",
        np.linalg.norm(linear_float),
        "stationarity residual",
        np.linalg.norm(residual),
        "secondary minimum",
        minimum,
    )
    if os.environ.get("N3_SECONDARY_EXACT"):
        exact_solution, exact_pivots = exact_ldl_solve(matrix, linear)
        exact_minimum = constant_term - Fraction(1, 4) * sum(
            value * solution_value
            for value, solution_value in zip(linear, exact_solution)
        )
        print(
            "exact LDL pivots",
            len(exact_pivots),
            "minimum",
            exact_minimum,
            "maximum bit length",
            max(
                max(value.numerator.bit_length(), value.denominator.bit_length())
                for value in exact_pivots + exact_solution
            ),
        )


if __name__ == "__main__":
    main()
