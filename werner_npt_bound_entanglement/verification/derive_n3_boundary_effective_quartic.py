#!/usr/bin/env python3
"""Independent exact derivation of the canonical-boundary effective quartic.

This module starts only from the definition

    Q3(C)=sum_S (-1/2)^|S| ||Tr_S C||_2^2

and the explicitly stated polar Stiefel chart around

    C0=|000><110|+|001><111|.

It reconstructs, with Gaussian-rational arithmetic:

* the complete 204-dimensional constrained Hessian;
* its 55-dimensional kernel and 149-dimensional positive complement;
* the raw quartic on the kernel;
* every mixed-cubic form coupling the kernel to a positive pivot; and
* the Lyapunov--Schmidt effective quartic.

No discovery module or third-party package is imported.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product


D = 3
N = 3
STRINGS = list(product(range(D), repeat=N))
U0 = [(0, 0, 0), (0, 0, 1)]
V0 = [(1, 1, 0), (1, 1, 1)]

Gaussian = tuple[Fraction, Fraction]
String = tuple[int, int, int]
Unit = tuple[String, String]
ScalarFrame = dict[tuple[String, int], Gaussian]
ScalarMatrix = dict[Unit, Gaussian]
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Gaussian]
PolynomialFrame = dict[tuple[String, int], Polynomial]
PolynomialMatrix = dict[Unit, Polynomial]

ZERO: Gaussian = (Fraction(0), Fraction(0))
ONE: Gaussian = (Fraction(1), Fraction(0))
I: Gaussian = (Fraction(0), Fraction(1))


def gadd(first: Gaussian, second: Gaussian) -> Gaussian:
    return (first[0] + second[0], first[1] + second[1])


def gneg(value: Gaussian) -> Gaussian:
    return (-value[0], -value[1])


def gmul(first: Gaussian, second: Gaussian) -> Gaussian:
    return (
        first[0] * second[0] - first[1] * second[1],
        first[0] * second[1] + first[1] * second[0],
    )


def gscale(value: Gaussian, scalar: Fraction) -> Gaussian:
    return (scalar * value[0], scalar * value[1])


def gconjugate(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def scalar_add(output, key, value: Gaussian) -> None:
    output[key] = gadd(output.get(key, ZERO), value)
    if output[key] == ZERO:
        del output[key]


def scalar_frame_sum(*frames: ScalarFrame) -> ScalarFrame:
    output = {}
    for frame in frames:
        for key, value in frame.items():
            scalar_add(output, key, value)
    return output


def scalar_matrix_sum(*matrices: ScalarMatrix) -> ScalarMatrix:
    output = {}
    for matrix in matrices:
        for key, value in matrix.items():
            scalar_add(output, key, value)
    return output


def scalar_gram(frame: ScalarFrame):
    output = [[ZERO for _ in range(2)] for _ in range(2)]
    for (row, first), x in frame.items():
        for (other_row, second), y in frame.items():
            if row == other_row:
                output[first][second] = gadd(
                    output[first][second],
                    gmul(gconjugate(x), y),
                )
    return output


def scalar_multiply_right(frame: ScalarFrame, matrix):
    output = {}
    for (row, first), value in frame.items():
        for second in range(2):
            scalar_add(
                output,
                (row, second),
                gmul(value, matrix[first][second]),
            )
    return output


def scalar_outer(first: ScalarFrame, second: ScalarFrame) -> ScalarMatrix:
    output = {}
    for (row, logical), x in first.items():
        for (column, other_logical), y in second.items():
            if logical == other_logical:
                scalar_add(
                    output,
                    (row, column),
                    gmul(x, gconjugate(y)),
                )
    return output


def scalar_partial_trace(matrix: ScalarMatrix, traced):
    output = {}
    kept = tuple(index for index in range(N) if index not in traced)
    for (row, column), value in matrix.items():
        if not all(row[index] == column[index] for index in traced):
            continue
        key = (
            tuple(row[index] for index in kept),
            tuple(column[index] for index in kept),
        )
        scalar_add(output, key, value)
    return output


def scalar_pairing(first: ScalarMatrix, second: ScalarMatrix) -> Gaussian:
    answer = ZERO
    for size in range(N + 1):
        for traced in combinations(range(N), size):
            first_reduced = scalar_partial_trace(first, traced)
            second_reduced = scalar_partial_trace(second, traced)
            value = ZERO
            for key in set(first_reduced) & set(second_reduced):
                value = gadd(
                    value,
                    gmul(
                        gconjugate(first_reduced[key]),
                        second_reduced[key],
                    ),
                )
            answer = gadd(
                answer,
                gscale(value, Fraction(-1, 2) ** size),
            )
    return answer


def base_frame(strings) -> ScalarFrame:
    return {(strings[0], 0): ONE, (strings[1], 1): ONE}


def coordinate_list():
    coordinates = []
    labels = []
    for side, frame in (("U", U0), ("V", V0)):
        for row in STRINGS:
            if row in frame:
                continue
            for column in range(2):
                for phase, name in ((ONE, "real"), (I, "imag")):
                    left = {}
                    right = {}
                    (left if side == "U" else right)[row, column] = phase
                    coordinates.append((left, right))
                    labels.append((side, row, column, name))

    logical = (
        ((I, ZERO), (ZERO, ZERO)),
        ((ZERO, ZERO), (ZERO, I)),
        ((ZERO, ONE), (gneg(ONE), ZERO)),
        ((ZERO, I), (I, ZERO)),
    )
    for number, generator in enumerate(logical):
        left = {}
        for row in range(2):
            for column in range(2):
                if generator[row][column] != ZERO:
                    left[U0[row], column] = generator[row][column]
        coordinates.append((left, {}))
        labels.append(("logical", number))
    return coordinates, labels


COORDINATES, LABELS = coordinate_list()
LEFT_BASE = base_frame(U0)
RIGHT_BASE = base_frame(V0)
BASE = scalar_outer(LEFT_BASE, RIGHT_BASE)


def quadratic_coefficient(indices) -> Fraction:
    left = {}
    right = {}
    for index in indices:
        left = scalar_frame_sum(left, COORDINATES[index][0])
        right = scalar_frame_sum(right, COORDINATES[index][1])
    left_gram = scalar_gram(left)
    right_gram = scalar_gram(right)

    first = scalar_matrix_sum(
        scalar_outer(left, RIGHT_BASE),
        scalar_outer(LEFT_BASE, right),
    )
    left_normalization = [
        [
            gscale(left_gram[row][column], Fraction(-1, 2))
            for column in range(2)
        ]
        for row in range(2)
    ]
    right_normalization = [
        [
            gscale(right_gram[row][column], Fraction(-1, 2))
            for column in range(2)
        ]
        for row in range(2)
    ]
    second = scalar_matrix_sum(
        scalar_outer(
            scalar_multiply_right(LEFT_BASE, left_normalization),
            RIGHT_BASE,
        ),
        scalar_outer(
            LEFT_BASE,
            scalar_multiply_right(RIGHT_BASE, right_normalization),
        ),
        scalar_outer(left, right),
    )
    first_value = scalar_pairing(first, first)
    cross_value = scalar_pairing(BASE, second)
    assert first_value[1] == 0
    return first_value[0] + 2 * cross_value[0]


def derive_hessian():
    dimension = len(COORDINATES)
    diagonal = [quadratic_coefficient((index,)) for index in range(dimension)]
    matrix = [
        [Fraction(0) for _ in range(dimension)]
        for _ in range(dimension)
    ]
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


def connected_components(matrix):
    adjacency = [[] for _ in matrix]
    for first in range(len(matrix)):
        for second in range(first):
            if matrix[first][second]:
                adjacency[first].append(second)
                adjacency[second].append(first)
    output = []
    seen = set()
    for start in range(len(matrix)):
        if start in seen:
            continue
        component = []
        stack = [start]
        seen.add(start)
        while stack:
            current = stack.pop()
            component.append(current)
            for other in adjacency[current]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        output.append(component)
    return output


def derive_kernel_and_pivots(hessian):
    components = connected_components(hessian)
    kernel = []
    pivots = []
    for component in components:
        pivot = max(component, key=lambda index: hessian[index][index])
        pivot_value = hessian[pivot][pivot]
        assert pivot_value > 0
        for first in component:
            for second in component:
                assert (
                    pivot_value * hessian[first][second]
                    == hessian[first][pivot] * hessian[pivot][second]
                )
        pivots.append(pivot)
        for index in component:
            if index != pivot:
                kernel.append(
                    {
                        index: Fraction(1),
                        pivot: -hessian[pivot][index] / pivot_value,
                    }
                )
    assert len(pivots) == 149
    assert len(kernel) == 55
    return kernel, pivots


def polynomial_constant(value: Gaussian) -> Polynomial:
    return {} if value == ZERO else {(): value}


def polynomial_variable(index: int, coefficient: Gaussian) -> Polynomial:
    return {} if coefficient == ZERO else {(index,): coefficient}


def padd(first: Polynomial, second: Polynomial) -> Polynomial:
    output = dict(first)
    for monomial, coefficient in second.items():
        output[monomial] = gadd(output.get(monomial, ZERO), coefficient)
        if output[monomial] == ZERO:
            del output[monomial]
    return output


def pscale(polynomial: Polynomial, scalar: Fraction) -> Polynomial:
    return {
        monomial: gscale(coefficient, scalar)
        for monomial, coefficient in polynomial.items()
        if gscale(coefficient, scalar) != ZERO
    }


def pmultiply(first: Polynomial, second: Polynomial) -> Polynomial:
    output = {}
    for first_monomial, first_coefficient in first.items():
        for second_monomial, second_coefficient in second.items():
            monomial = tuple(sorted(first_monomial + second_monomial))
            coefficient = gmul(first_coefficient, second_coefficient)
            output[monomial] = gadd(
                output.get(monomial, ZERO), coefficient
            )
            if output[monomial] == ZERO:
                del output[monomial]
    return output


def pconjugate(polynomial: Polynomial) -> Polynomial:
    return {
        monomial: gconjugate(coefficient)
        for monomial, coefficient in polynomial.items()
    }


def polynomial_add(output, key, value: Polynomial) -> None:
    output[key] = padd(output.get(key, {}), value)
    if not output[key]:
        del output[key]


def polynomial_frame_sum(*frames: PolynomialFrame) -> PolynomialFrame:
    output = {}
    for frame in frames:
        for key, value in frame.items():
            polynomial_add(output, key, value)
    return output


def polynomial_matrix_sum(*matrices: PolynomialMatrix) -> PolynomialMatrix:
    output = {}
    for matrix in matrices:
        for key, value in matrix.items():
            polynomial_add(output, key, value)
    return output


def polynomial_base_frame(strings) -> PolynomialFrame:
    return {
        (strings[0], 0): polynomial_constant(ONE),
        (strings[1], 1): polynomial_constant(ONE),
    }


def kernel_frames(kernel):
    left = {}
    right = {}
    for variable, direction in enumerate(kernel):
        for coordinate, rational in direction.items():
            for key, value in COORDINATES[coordinate][0].items():
                polynomial_add(
                    left,
                    key,
                    polynomial_variable(
                        variable, gscale(value, rational)
                    ),
                )
            for key, value in COORDINATES[coordinate][1].items():
                polynomial_add(
                    right,
                    key,
                    polynomial_variable(
                        variable, gscale(value, rational)
                    ),
                )
    return left, right


def fixed_frames(coordinate):
    return (
        {
            key: polynomial_constant(value)
            for key, value in COORDINATES[coordinate][0].items()
        },
        {
            key: polynomial_constant(value)
            for key, value in COORDINATES[coordinate][1].items()
        },
    )


def polynomial_gram(frame: PolynomialFrame):
    output = [[{} for _ in range(2)] for _ in range(2)]
    for (row, first), x in frame.items():
        for (other_row, second), y in frame.items():
            if row == other_row:
                output[first][second] = padd(
                    output[first][second],
                    pmultiply(pconjugate(x), y),
                )
    return output


def polynomial_gram_derivative(kernel, fixed):
    output = [[{} for _ in range(2)] for _ in range(2)]
    for (row, first), x in fixed.items():
        for (other_row, second), y in kernel.items():
            if row == other_row:
                output[first][second] = padd(
                    output[first][second],
                    pmultiply(pconjugate(x), y),
                )
    for (row, first), x in kernel.items():
        for (other_row, second), y in fixed.items():
            if row == other_row:
                output[first][second] = padd(
                    output[first][second],
                    pmultiply(pconjugate(x), y),
                )
    return output


def polynomial_matrix2_multiply(first, second):
    return [
        [
            sum_polynomials(
                *(
                    pmultiply(first[row][middle], second[middle][column])
                    for middle in range(2)
                )
            )
            for column in range(2)
        ]
        for row in range(2)
    ]


def sum_polynomials(*polynomials):
    output = {}
    for polynomial in polynomials:
        output = padd(output, polynomial)
    return output


def polynomial_multiply_right(frame, matrix):
    output = {}
    for (row, first), value in frame.items():
        for second in range(2):
            polynomial_add(
                output,
                (row, second),
                pmultiply(value, matrix[first][second]),
            )
    return output


def polynomial_outer(first, second):
    output = {}
    for (row, logical), x in first.items():
        for (column, other_logical), y in second.items():
            if logical == other_logical:
                polynomial_add(
                    output,
                    (row, column),
                    pmultiply(x, pconjugate(y)),
                )
    return output


def polynomial_partial_trace(matrix, traced):
    output = {}
    kept = tuple(index for index in range(N) if index not in traced)
    for (row, column), value in matrix.items():
        if not all(row[index] == column[index] for index in traced):
            continue
        key = (
            tuple(row[index] for index in kept),
            tuple(column[index] for index in kept),
        )
        polynomial_add(output, key, value)
    return output


def polynomial_pairing(first, second):
    answer = {}
    for size in range(N + 1):
        for traced in combinations(range(N), size):
            first_reduced = polynomial_partial_trace(first, traced)
            second_reduced = polynomial_partial_trace(second, traced)
            value = {}
            for key in set(first_reduced) & set(second_reduced):
                value = padd(
                    value,
                    pmultiply(
                        pconjugate(first_reduced[key]),
                        second_reduced[key],
                    ),
                )
            answer = padd(
                answer,
                pscale(value, Fraction(-1, 2) ** size),
            )
    return answer


def twice_real(polynomial):
    return {
        monomial: 2 * coefficient[0]
        for monomial, coefficient in polynomial.items()
        if coefficient[0]
    }


def real_part(polynomial):
    return {
        monomial: coefficient[0]
        for monomial, coefficient in polynomial.items()
        if coefficient[0]
    }


def add_real(output, polynomial, scale=Fraction(1)):
    for monomial, coefficient in polynomial.items():
        output[monomial] += scale * coefficient
        if not output[monomial]:
            del output[monomial]


def scaled_frame(frame, scalar):
    return {
        key: pscale(value, scalar)
        for key, value in frame.items()
        if pscale(value, scalar)
    }


def derive_quartics(hessian, kernel, pivots):
    left_zero = polynomial_base_frame(U0)
    right_zero = polynomial_base_frame(V0)
    left_one, right_one = kernel_frames(kernel)
    left_gram = polynomial_gram(left_one)
    right_gram = polynomial_gram(right_one)
    left_gram_square = polynomial_matrix2_multiply(left_gram, left_gram)
    right_gram_square = polynomial_matrix2_multiply(
        right_gram, right_gram
    )
    left_two = scaled_frame(
        polynomial_multiply_right(left_zero, left_gram),
        Fraction(-1, 2),
    )
    right_two = scaled_frame(
        polynomial_multiply_right(right_zero, right_gram),
        Fraction(-1, 2),
    )
    left_three = scaled_frame(
        polynomial_multiply_right(left_one, left_gram),
        Fraction(-1, 2),
    )
    right_three = scaled_frame(
        polynomial_multiply_right(right_one, right_gram),
        Fraction(-1, 2),
    )
    left_four = scaled_frame(
        polynomial_multiply_right(left_zero, left_gram_square),
        Fraction(3, 8),
    )
    right_four = scaled_frame(
        polynomial_multiply_right(right_zero, right_gram_square),
        Fraction(3, 8),
    )

    matrices = [
        polynomial_outer(left_zero, right_zero),
        polynomial_matrix_sum(
            polynomial_outer(left_one, right_zero),
            polynomial_outer(left_zero, right_one),
        ),
        polynomial_matrix_sum(
            polynomial_outer(left_two, right_zero),
            polynomial_outer(left_one, right_one),
            polynomial_outer(left_zero, right_two),
        ),
        polynomial_matrix_sum(
            polynomial_outer(left_three, right_zero),
            polynomial_outer(left_two, right_one),
            polynomial_outer(left_one, right_two),
            polynomial_outer(left_zero, right_three),
        ),
        polynomial_matrix_sum(
            polynomial_outer(left_four, right_zero),
            polynomial_outer(left_three, right_one),
            polynomial_outer(left_two, right_two),
            polynomial_outer(left_one, right_three),
            polynomial_outer(left_zero, right_four),
        ),
    ]

    raw = defaultdict(Fraction)
    add_real(
        raw,
        twice_real(polynomial_pairing(matrices[0], matrices[4])),
    )
    add_real(
        raw,
        twice_real(polynomial_pairing(matrices[1], matrices[3])),
    )
    add_real(
        raw,
        real_part(polynomial_pairing(matrices[2], matrices[2])),
    )

    forms = []
    for pivot in pivots:
        left_fixed, right_fixed = fixed_frames(pivot)
        left_gram_derivative = polynomial_gram_derivative(
            left_one, left_fixed
        )
        right_gram_derivative = polynomial_gram_derivative(
            right_one, right_fixed
        )
        derivative_left_two = scaled_frame(
            polynomial_multiply_right(left_zero, left_gram_derivative),
            Fraction(-1, 2),
        )
        derivative_right_two = scaled_frame(
            polynomial_multiply_right(right_zero, right_gram_derivative),
            Fraction(-1, 2),
        )
        derivative_left_three = scaled_frame(
            polynomial_frame_sum(
                polynomial_multiply_right(left_fixed, left_gram),
                polynomial_multiply_right(
                    left_one, left_gram_derivative
                ),
            ),
            Fraction(-1, 2),
        )
        derivative_right_three = scaled_frame(
            polynomial_frame_sum(
                polynomial_multiply_right(right_fixed, right_gram),
                polynomial_multiply_right(
                    right_one, right_gram_derivative
                ),
            ),
            Fraction(-1, 2),
        )
        derivative_one = polynomial_matrix_sum(
            polynomial_outer(left_fixed, right_zero),
            polynomial_outer(left_zero, right_fixed),
        )
        derivative_two = polynomial_matrix_sum(
            polynomial_outer(derivative_left_two, right_zero),
            polynomial_outer(left_fixed, right_one),
            polynomial_outer(left_one, right_fixed),
            polynomial_outer(left_zero, derivative_right_two),
        )
        derivative_three = polynomial_matrix_sum(
            polynomial_outer(derivative_left_three, right_zero),
            polynomial_outer(derivative_left_two, right_one),
            polynomial_outer(left_two, right_fixed),
            polynomial_outer(left_fixed, right_two),
            polynomial_outer(left_one, derivative_right_two),
            polynomial_outer(left_zero, derivative_right_three),
        )
        value = sum_polynomials(
            polynomial_pairing(matrices[0], derivative_three),
            polynomial_pairing(derivative_one, matrices[2]),
            polynomial_pairing(matrices[1], derivative_two),
        )
        forms.append(twice_real(value))

    effective = defaultdict(Fraction)
    add_real(effective, raw)
    for pivot, form in zip(pivots, forms):
        square = defaultdict(Fraction)
        for first_monomial, first_coefficient in form.items():
            for second_monomial, second_coefficient in form.items():
                square[
                    tuple(sorted(first_monomial + second_monomial))
                ] += first_coefficient * second_coefficient
        add_real(
            effective,
            square,
            -Fraction(1, 4) / hessian[pivot][pivot],
        )
    return dict(raw), forms, dict(effective)


def derive():
    assert scalar_pairing(BASE, BASE) == ZERO
    hessian = derive_hessian()
    kernel, pivots = derive_kernel_and_pivots(hessian)
    raw, forms, effective = derive_quartics(
        hessian, kernel, pivots
    )
    return hessian, kernel, pivots, raw, forms, effective


if __name__ == "__main__":
    result = derive()
    print(
        "derived exact chart data:",
        len(result[0]),
        "Hessian coordinates,",
        len(result[1]),
        "kernel coordinates,",
        len(result[2]),
        "positive pivots,",
        len(result[3]),
        "raw quartic terms,",
        sum(map(len, result[4])),
        "mixed terms, and",
        len(result[5]),
        "effective quartic terms",
    )
