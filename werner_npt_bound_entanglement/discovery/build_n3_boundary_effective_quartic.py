#!/usr/bin/env python3
"""Build the exact Lyapunov--Schmidt quartic at the nonnormal zero.

The raw kernel quartic is corrected by eliminating the 149 positive
Hessian directions.  All polynomial arithmetic here uses Gaussian
rationals represented as pairs of ``Fraction`` objects.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ANALYZER = HERE / "analyze_n3_unshifted_boundary.py"
SPEC = importlib.util.spec_from_file_location("boundary", ANALYZER)
boundary = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(boundary)

CERTIFICATE = (
    HERE.parent
    / "verification"
    / "certificates"
    / "n3_boundary_flat_quartic_sos.json"
)

Gaussian = tuple[Fraction, Fraction]
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Gaussian]
Frame = dict[tuple[boundary.String, int], Polynomial]
MatrixSeries = dict[boundary.Unit, Polynomial]

ZERO: Gaussian = (Fraction(0), Fraction(0))
ONE: Gaussian = (Fraction(1), Fraction(0))


def gaussian(value) -> Gaussian:
    if isinstance(value, Fraction):
        return (value, Fraction(0))
    if isinstance(value, int):
        return (Fraction(value), Fraction(0))
    return (Fraction(value.real), Fraction(value.imag))


def gadd(first: Gaussian, second: Gaussian) -> Gaussian:
    return (first[0] + second[0], first[1] + second[1])


def gmul(first: Gaussian, second: Gaussian) -> Gaussian:
    return (
        first[0] * second[0] - first[1] * second[1],
        first[0] * second[1] + first[1] * second[0],
    )


def gconjugate(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def polynomial_constant(value) -> Polynomial:
    coefficient = gaussian(value)
    return {} if coefficient == ZERO else {(): coefficient}


def polynomial_variable(index: int, value=1) -> Polynomial:
    coefficient = gaussian(value)
    return {} if coefficient == ZERO else {(index,): coefficient}


def padd(first: Polynomial, second: Polynomial) -> Polynomial:
    output = dict(first)
    for monomial, coefficient in second.items():
        output[monomial] = gadd(output.get(monomial, ZERO), coefficient)
        if output[monomial] == ZERO:
            del output[monomial]
    return output


def pscale(polynomial: Polynomial, scalar) -> Polynomial:
    scalar = gaussian(scalar)
    output = {
        monomial: gmul(coefficient, scalar)
        for monomial, coefficient in polynomial.items()
    }
    return {
        monomial: coefficient
        for monomial, coefficient in output.items()
        if coefficient != ZERO
    }


def pmultiply(first: Polynomial, second: Polynomial) -> Polynomial:
    output: defaultdict[Monomial, Gaussian] = defaultdict(lambda: ZERO)
    for first_monomial, first_coefficient in first.items():
        for second_monomial, second_coefficient in second.items():
            monomial = tuple(sorted(first_monomial + second_monomial))
            output[monomial] = gadd(
                output[monomial],
                gmul(first_coefficient, second_coefficient),
            )
    return {
        monomial: coefficient
        for monomial, coefficient in output.items()
        if coefficient != ZERO
    }


def pconjugate(polynomial: Polynomial) -> Polynomial:
    return {
        monomial: gconjugate(coefficient)
        for monomial, coefficient in polynomial.items()
    }


def frame_add(output: Frame, key, value: Polynomial) -> None:
    output[key] = padd(output.get(key, {}), value)
    if not output[key]:
        del output[key]


def matrix_add(output: MatrixSeries, key, value: Polynomial) -> None:
    output[key] = padd(output.get(key, {}), value)
    if not output[key]:
        del output[key]


def base_frame(strings) -> Frame:
    return {
        (strings[0], 0): polynomial_constant(1),
        (strings[1], 1): polynomial_constant(1),
    }


def kernel_frames(kernel) -> tuple[Frame, Frame]:
    left: Frame = {}
    right: Frame = {}
    for variable, direction in enumerate(kernel):
        for coordinate, rational in direction.items():
            for key, value in boundary.COORDINATES[coordinate][0].items():
                frame_add(
                    left,
                    key,
                    polynomial_variable(variable, rational * value),
                )
            for key, value in boundary.COORDINATES[coordinate][1].items():
                frame_add(
                    right,
                    key,
                    polynomial_variable(variable, rational * value),
                )
    return left, right


def fixed_frames(coordinate: int) -> tuple[Frame, Frame]:
    left = {
        key: polynomial_constant(value)
        for key, value in boundary.COORDINATES[coordinate][0].items()
    }
    right = {
        key: polynomial_constant(value)
        for key, value in boundary.COORDINATES[coordinate][1].items()
    }
    return left, right


def gram(frame: Frame):
    output = [[{} for _ in range(2)] for _ in range(2)]
    for (row, first), x in frame.items():
        for (other_row, second), y in frame.items():
            if row == other_row:
                output[first][second] = padd(
                    output[first][second],
                    pmultiply(pconjugate(x), y),
                )
    return output


def gram_derivative(kernel: Frame, fixed: Frame):
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


def multiply_right(frame: Frame, logical) -> Frame:
    output: Frame = {}
    for (row, first), value in frame.items():
        for second in range(2):
            frame_add(
                output,
                (row, second),
                pmultiply(value, logical[first][second]),
            )
    return output


def outer(first: Frame, second: Frame) -> MatrixSeries:
    output: MatrixSeries = {}
    for (row, logical), x in first.items():
        for (column, other_logical), y in second.items():
            if logical == other_logical:
                matrix_add(
                    output,
                    (row, column),
                    pmultiply(x, pconjugate(y)),
                )
    return output


def matrix_sum(*matrices: MatrixSeries) -> MatrixSeries:
    output: MatrixSeries = {}
    for matrix in matrices:
        for key, value in matrix.items():
            matrix_add(output, key, value)
    return output


def pairing(first: MatrixSeries, second: MatrixSeries) -> Polynomial:
    output: Polynomial = {}
    for first_unit, x in first.items():
        for second_unit, y in second.items():
            coefficient = boundary.unit_pairing(first_unit, second_unit)
            if coefficient:
                output = padd(
                    output,
                    pscale(
                        pmultiply(pconjugate(x), y),
                        coefficient,
                    ),
                )
    return output


def real_twice(polynomial: Polynomial) -> dict[Monomial, Fraction]:
    output = {}
    for monomial, (real, _) in polynomial.items():
        if real:
            output[monomial] = 2 * real
    return output


def add_real(
    output: defaultdict[Monomial, Fraction],
    polynomial: dict[Monomial, Fraction],
    scale=Fraction(1),
) -> None:
    for monomial, coefficient in polynomial.items():
        output[monomial] += scale * coefficient
        if not output[monomial]:
            del output[monomial]


def raw_quartic() -> dict[Monomial, Fraction]:
    certificate = json.loads(CERTIFICATE.read_text())
    assert certificate["format"] == "n3-flat-kernel-rational-face-v2"
    return {
        tuple(indices): Fraction(*coefficient)
        for indices, coefficient in certificate["quartic_terms"]
    }


def build():
    hessian = boundary.hessian()
    components = boundary.connected_components(hessian)
    kernel = boundary.kernel_basis(hessian, components)
    pivots = [
        max(component, key=lambda index: hessian[index][index])
        for component in components
        if hessian[
            max(component, key=lambda index: hessian[index][index])
        ][
            max(component, key=lambda index: hessian[index][index])
        ]
        > 0
    ]
    left_base = base_frame(boundary.U0)
    right_base = base_frame(boundary.V0)
    left_kernel, right_kernel = kernel_frames(kernel)

    left_gram = gram(left_kernel)
    right_gram = gram(right_kernel)
    left_second = {
        key: pscale(value, Fraction(-1, 2))
        for key, value in multiply_right(left_base, left_gram).items()
    }
    right_second = {
        key: pscale(value, Fraction(-1, 2))
        for key, value in multiply_right(right_base, right_gram).items()
    }
    left_third = {
        key: pscale(value, Fraction(-1, 2))
        for key, value in multiply_right(left_kernel, left_gram).items()
    }
    right_third = {
        key: pscale(value, Fraction(-1, 2))
        for key, value in multiply_right(right_kernel, right_gram).items()
    }

    matrix_zero = outer(left_base, right_base)
    matrix_one = matrix_sum(
        outer(left_kernel, right_base),
        outer(left_base, right_kernel),
    )
    matrix_two = matrix_sum(
        outer(left_second, right_base),
        outer(left_kernel, right_kernel),
        outer(left_base, right_second),
    )

    linear_forms = []
    for pivot in pivots:
        left_fixed, right_fixed = fixed_frames(pivot)
        left_gram_derivative = gram_derivative(left_kernel, left_fixed)
        right_gram_derivative = gram_derivative(
            right_kernel, right_fixed
        )
        derivative_left_second = {
            key: pscale(value, Fraction(-1, 2))
            for key, value in multiply_right(
                left_base, left_gram_derivative
            ).items()
        }
        derivative_right_second = {
            key: pscale(value, Fraction(-1, 2))
            for key, value in multiply_right(
                right_base, right_gram_derivative
            ).items()
        }
        derivative_left_third = matrix_sum_frames(
            multiply_right(left_fixed, left_gram),
            multiply_right(left_kernel, left_gram_derivative),
            scale=Fraction(-1, 2),
        )
        derivative_right_third = matrix_sum_frames(
            multiply_right(right_fixed, right_gram),
            multiply_right(right_kernel, right_gram_derivative),
            scale=Fraction(-1, 2),
        )

        derivative_one = matrix_sum(
            outer(left_fixed, right_base),
            outer(left_base, right_fixed),
        )
        derivative_two = matrix_sum(
            outer(derivative_left_second, right_base),
            outer(left_fixed, right_kernel),
            outer(left_kernel, right_fixed),
            outer(left_base, derivative_right_second),
        )
        derivative_three = matrix_sum(
            outer(derivative_left_third, right_base),
            outer(derivative_left_second, right_kernel),
            outer(left_second, right_fixed),
            outer(left_fixed, right_second),
            outer(left_kernel, derivative_right_second),
            outer(left_base, derivative_right_third),
        )
        value = matrix_sum_polynomials(
            pairing(matrix_zero, derivative_three),
            pairing(derivative_one, matrix_two),
            pairing(matrix_one, derivative_two),
        )
        linear_forms.append(real_twice(value))

    effective: defaultdict[Monomial, Fraction] = defaultdict(Fraction)
    add_real(effective, raw_quartic())
    for pivot, form in zip(pivots, linear_forms):
        square: defaultdict[Monomial, Fraction] = defaultdict(Fraction)
        for first_monomial, first_coefficient in form.items():
            for second_monomial, second_coefficient in form.items():
                square[
                    tuple(sorted(first_monomial + second_monomial))
                ] += first_coefficient * second_coefficient
        add_real(
            effective,
            dict(square),
            -Fraction(1, 4) / hessian[pivot][pivot],
        )
    return kernel, pivots, linear_forms, dict(effective)


def matrix_sum_frames(*frames: Frame, scale=Fraction(1)) -> Frame:
    output: Frame = {}
    for frame in frames:
        for key, value in frame.items():
            frame_add(output, key, pscale(value, scale))
    return output


def matrix_sum_polynomials(*polynomials: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for polynomial in polynomials:
        output = padd(output, polynomial)
    return output


def main() -> None:
    _, pivots, forms, effective = build()
    print("positive pivots", len(pivots))
    print("mixed cubic quadratic forms", len(forms))
    print("mixed cubic terms", sum(map(len, forms)))
    print("effective quartic terms", len(effective))
    print(
        "effective coordinate-axis values",
        {
            index: effective.get((index, index, index, index), Fraction(0))
            for index in range(55)
            if effective.get((index, index, index, index), Fraction(0))
        },
    )


if __name__ == "__main__":
    main()
