#!/usr/bin/env python3
"""Verify the exact L2/L3 order-six core certificate.

The symbolic core uses a tiny rational polynomial implementation.  It
verifies the two-by-two Schur identity as a polynomial identity in six
variables.  Three additional Gaussian-rational spot checks compare the
closed formula with the complete 177-variable Lyapunov--Schmidt
elimination.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVATION = (
    ROOT / "discovery" / "analyze_n3_boundary_l2_reduced_form.py"
)
SPEC = importlib.util.spec_from_file_location("l2_reduced", DERIVATION)
l2_reduced = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(l2_reduced)


Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]
ZERO_EXPONENT = (0,) * 6


def constant(value) -> Polynomial:
    value = Fraction(value)
    return {} if value == 0 else {ZERO_EXPONENT: value}


def variable(index) -> Polynomial:
    exponent = tuple(int(position == index) for position in range(6))
    return {exponent: Fraction(1)}


def add(first: Polynomial, second: Polynomial) -> Polynomial:
    output = dict(first)
    for exponent, coefficient in second.items():
        output[exponent] = output.get(exponent, Fraction(0)) + coefficient
        if output[exponent] == 0:
            del output[exponent]
    return output


def scale(polynomial: Polynomial, scalar) -> Polynomial:
    scalar = Fraction(scalar)
    return {
        exponent: scalar * coefficient
        for exponent, coefficient in polynomial.items()
        if scalar * coefficient
    }


def subtract(first: Polynomial, second: Polynomial) -> Polynomial:
    return add(first, scale(second, -1))


def multiply(first: Polynomial, second: Polynomial) -> Polynomial:
    output = {}
    for first_exponent, first_coefficient in first.items():
        for second_exponent, second_coefficient in second.items():
            exponent = tuple(
                first_power + second_power
                for first_power, second_power in zip(
                    first_exponent, second_exponent
                )
            )
            output[exponent] = (
                output.get(exponent, Fraction(0))
                + first_coefficient * second_coefficient
            )
            if output[exponent] == 0:
                del output[exponent]
    return output


def total(*polynomials):
    output = {}
    for polynomial in polynomials:
        output = add(output, polynomial)
    return output


def matrix_multiply(first, second):
    return [
        [
            total(
                *(
                    multiply(first[row][middle], second[middle][column])
                    for middle in range(len(second))
                )
            )
            for column in range(len(second[0]))
        ]
        for row in range(len(first))
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matrix_subtract(first, second):
    return [
        [
            subtract(first[row][column], second[row][column])
            for column in range(len(first[0]))
        ]
        for row in range(len(first))
    ]


def matrix_scale(matrix, scalar):
    return [
        [scale(value, scalar) for value in row]
        for row in matrix
    ]


def matrix_multiply_polynomial(matrix, polynomial):
    return [
        [multiply(value, polynomial) for value in row]
        for row in matrix
    ]


def assert_zero_matrix(matrix):
    assert all(not value for row in matrix for value in row)


def verify_symbolic_core():
    w = [variable(index) for index in range(6)]
    squares = [multiply(value, value) for value in w]
    t = scale(
        total(
            squares[0],
            squares[1],
            scale(squares[2], 2),
            scale(squares[3], 2),
            scale(squares[4], 2),
            scale(squares[5], 2),
        ),
        Fraction(5, 4),
    )
    x = scale(
        total(
            squares[0],
            scale(squares[1], -1),
            scale(multiply(w[2], w[4]), 4),
            scale(multiply(w[3], w[5]), -4),
        ),
        Fraction(1, 4),
    )
    y = total(
        scale(multiply(w[0], w[1]), Fraction(1, 2)),
        multiply(w[2], w[5]),
        multiply(w[3], w[4]),
    )
    eta_norm_squared = add(multiply(x, x), multiply(y, y))
    delta = subtract(multiply(t, t), eta_norm_squared)

    k = [
        [scale(add(t, x), Fraction(1, 2)), scale(y, Fraction(1, 2))],
        [scale(y, Fraction(1, 2)), scale(subtract(t, x), Fraction(1, 2))],
    ]
    ell = [
        [add(x, scale(t, Fraction(1, 5))), scale(y, -1)],
        [y, subtract(x, scale(t, Fraction(1, 5)))],
    ]
    c = [[k[0][0], scale(k[0][1], -1)],
         [scale(k[1][0], -1), k[1][1]]]

    determinant = subtract(
        multiply(k[0][0], k[1][1]),
        multiply(k[0][1], k[1][0]),
    )
    assert not subtract(scale(determinant, 4), delta)

    adjugate = [
        [k[1][1], scale(k[0][1], -1)],
        [scale(k[1][0], -1), k[0][0]],
    ]
    # 4 det(K) H = 4 det(K) C - L^T adj(K) L.
    left = matrix_subtract(
        matrix_multiply_polynomial(c, scale(determinant, 4)),
        matrix_multiply(
            matrix_multiply(transpose(ell), adjugate), ell
        ),
    )
    common = scale(t, Fraction(4, 25))
    three_t_squared_minus_five_eta_squared = subtract(
        scale(multiply(t, t), 3),
        scale(eta_norm_squared, 5),
    )
    right = matrix_multiply_polynomial(
        [
            [
                add(
                    three_t_squared_minus_five_eta_squared,
                    scale(multiply(t, x), 2),
                ),
                scale(multiply(t, y), -2),
            ],
            [
                scale(multiply(t, y), -2),
                subtract(
                    three_t_squared_minus_five_eta_squared,
                    scale(multiply(t, x), 2),
                ),
            ],
        ],
        common,
    )
    assert_zero_matrix(matrix_subtract(left, right))

    # Check t/5 = |xi|^2/4+(|beta|^2+|chi|^2)/2,
    # the scalar used in the triangle/AM--GM certificate.
    triangle_majorant = total(
        scale(add(squares[0], squares[1]), Fraction(1, 4)),
        scale(
            total(squares[2], squares[3], squares[4], squares[5]),
            Fraction(1, 2),
        ),
    )
    assert not subtract(scale(t, Fraction(1, 5)), triangle_majorant)


def full_secondary_minimum(w, z, d):
    constant_term, linear, matrix = l2_reduced.eliminate_positive(
        w, z, d
    )
    solution, pivots = l2_reduced.secondary.exact_ldl_solve(
        matrix, linear
    )
    assert all(pivot > 0 for pivot in pivots)
    return constant_term - Fraction(1, 4) * sum(
        value * solution_value
        for value, solution_value in zip(linear, solution)
    )


def verify_full_exact_samples():
    samples = (
        ((1, -2, 3, 1, -1, 2), (2, -3), (4, 1)),
        ((1, 2, 3, 4, 5, 6), (-2, 1), (3, -4)),
        ((2, -1, 1, 3, -2, 1), (1, 2), (-1, 3)),
    )
    expected = (
        Fraction(7174965, 1492),
        Fraction(292811631, 21038),
        Fraction(1391005, 1488),
    )
    for sample, expected_value in zip(samples, expected):
        direct = full_secondary_minimum(*sample)
        closed = l2_reduced.secondary_formula(*sample)
        assert direct == closed == expected_value


def main():
    verify_symbolic_core()
    verify_full_exact_samples()
    print("verified exact L2/L3 secondary core and full LS samples")


if __name__ == "__main__":
    main()
