#!/usr/bin/env python3
"""Reduce the L2 secondary problem to its active real biform.

The component coordinates are quotiented as

    z = (c14+c15) + i(c16-c17),
    w = (c4+c5, c6-c7, c8, c9, c10, c11),
    d = c18+i c19.

We use the gauge c5=c7=0 and split z symmetrically between the two
representatives.  After both Lyapunov--Schmidt eliminations, the
secondary minimum is, for fixed w, quadratic in

    m=(Re(z)Re(d), Re(z)Im(d), Im(z)Re(d), Im(z)Im(d)).

This script reconstructs its exact 4 by 4 Gram matrix.  The sole Gram
ambiguity is the Segre relation m0*m3-m1*m2=0; by default its
coefficient is split equally.

This remains discovery code until positivity is certified uniformly in
w.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SECONDARY_PATH = HERE / "analyze_n3_boundary_secondary_ls.py"
SPEC = importlib.util.spec_from_file_location("secondary", SECONDARY_PATH)
secondary = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(secondary)


def component_coefficients(w, z=(0, 0), d=(0, 0)):
    """Return the canonical 27 component coordinates."""

    assert len(w) == 6 and len(z) == 2 and len(d) == 2
    output = [Fraction(0) for _ in range(27)]
    output[4] = Fraction(w[0])
    output[6] = Fraction(w[1])
    output[8:12] = [Fraction(value) for value in w[2:]]
    output[14] = Fraction(z[0], 2)
    output[15] = Fraction(z[0], 2)
    output[16] = Fraction(z[1], 2)
    output[17] = Fraction(-z[1], 2)
    output[18] = Fraction(d[0])
    output[19] = Fraction(d[1])
    return output


def eliminate_positive(w, z=(0, 0), d=(0, 0)):
    """Eliminate the constant positive-Hessian block exactly."""

    coefficients = component_coefficients(w, z, d)
    *_, variable_count, polynomial = secondary.build_problem(
        2, coefficients
    )
    constant, linear, matrix = secondary.quadratic_data(
        variable_count, polynomial
    )
    normal_count = 28
    assert variable_count == normal_count + 149
    diagonal = [
        matrix[normal_count + index][normal_count + index]
        for index in range(149)
    ]
    assert all(value > 0 for value in diagonal)
    assert all(
        matrix[normal_count + row][normal_count + column]
        == (diagonal[row] if row == column else 0)
        for row in range(149)
        for column in range(149)
    )

    reduced_matrix = [
        [
            matrix[row][column]
            - sum(
                matrix[row][normal_count + index]
                * matrix[column][normal_count + index]
                / diagonal[index]
                for index in range(149)
            )
            for column in range(normal_count)
        ]
        for row in range(normal_count)
    ]
    reduced_linear = [
        linear[row]
        - sum(
            matrix[row][normal_count + index]
            * linear[normal_count + index]
            / diagonal[index]
            for index in range(149)
        )
        for row in range(normal_count)
    ]
    reduced_constant = constant - Fraction(1, 4) * sum(
        linear[normal_count + index] ** 2 / diagonal[index]
        for index in range(149)
    )
    return reduced_constant, reduced_linear, reduced_matrix


def eliminate_to_core(w):
    """Return the exact two-dimensional core for z=1.

    The result is ``(K,L,C)`` in

        h^T K h + h^T L d + d^T C d,

    where h and d are real two-vectors.
    """

    retained = (0, 1)
    eliminated = tuple(range(2, 16))
    outputs = []
    reference_core = None
    for d in ((1, 0), (0, 1), (1, 1)):
        constant, linear, matrix = eliminate_positive(w, (1, 0), d)
        block = [
            [matrix[row][column] for column in eliminated]
            for row in eliminated
        ]
        coupling = [
            [matrix[row][column] for column in eliminated]
            for row in retained
        ]
        eliminated_linear = [linear[index] for index in eliminated]
        retained_linear = [linear[index] for index in retained]
        solved_coupling = [
            secondary.exact_ldl_solve(block, row)[0]
            for row in coupling
        ]
        solved_linear = secondary.exact_ldl_solve(
            block, eliminated_linear
        )[0]
        core = [
            [
                matrix[row][column]
                - sum(
                    coupling[first][index]
                    * solved_coupling[second][index]
                    for index in range(len(eliminated))
                )
                for second, column in enumerate(retained)
            ]
            for first, row in enumerate(retained)
        ]
        if reference_core is None:
            reference_core = core
        else:
            assert core == reference_core
        core_linear = [
            retained_linear[first]
            - sum(
                coupling[first][index] * solved_linear[index]
                for index in range(len(eliminated))
            )
            for first in range(2)
        ]
        core_constant = constant - Fraction(1, 4) * sum(
            eliminated_linear[index] * solved_linear[index]
            for index in range(len(eliminated))
        )

        # The twelve genuinely qutrit normal directions are uncoupled
        # and have zero linear term.  They therefore cannot lower the
        # Schur minimum.
        assert all(linear[index] == 0 for index in range(16, 28))
        assert all(
            matrix[row][column] == 0
            for row in range(16)
            for column in range(16, 28)
        )
        outputs.append((core_linear, core_constant))

    assert reference_core is not None
    first_linear, first_constant = outputs[0]
    second_linear, second_constant = outputs[1]
    summed_linear, summed_constant = outputs[2]
    assert summed_linear == [
        first_linear[index] + second_linear[index]
        for index in range(2)
    ]
    cross_constant = (
        summed_constant - first_constant - second_constant
    ) / 2
    linear_map = [
        [first_linear[row], second_linear[row]]
        for row in range(2)
    ]
    constant_matrix = [
        [first_constant, cross_constant],
        [cross_constant, second_constant],
    ]
    return reference_core, linear_map, constant_matrix


def predicted_core(w):
    """Closed quadratic formula for the exact core matrices."""

    w = tuple(Fraction(value) for value in w)
    t = Fraction(5, 4) * (
        w[0] ** 2
        + w[1] ** 2
        + 2 * sum(value**2 for value in w[2:])
    )
    x = Fraction(1, 4) * (
        w[0] ** 2
        - w[1] ** 2
        + 4 * w[2] * w[4]
        - 4 * w[3] * w[5]
    )
    imaginary_eta = (
        Fraction(1, 2) * w[0] * w[1]
        + w[2] * w[5]
        + w[3] * w[4]
    )
    k = [
        [(t + x) / 2, imaginary_eta / 2],
        [imaginary_eta / 2, (t - x) / 2],
    ]
    ell = [
        [x + t / 5, -imaginary_eta],
        [imaginary_eta, x - t / 5],
    ]
    j_k_j = [
        [k[0][0], -k[0][1]],
        [-k[1][0], k[1][1]],
    ]
    return k, ell, j_k_j


def gaussian_multiply(first, second):
    return (
        first[0] * second[0] - first[1] * second[1],
        first[0] * second[1] + first[1] * second[0],
    )


def secondary_formula(w, z, d):
    """Evaluate the closed exact secondary minimum."""

    w = tuple(Fraction(value) for value in w)
    z = tuple(Fraction(value) for value in z)
    d = tuple(Fraction(value) for value in d)
    xi = (w[0], w[1])
    beta = (w[2], w[3])
    chi = (w[4], w[5])
    xi_square = gaussian_multiply(xi, xi)
    beta_chi = gaussian_multiply(beta, chi)
    eta = (
        xi_square[0] / 4 + beta_chi[0],
        xi_square[1] / 4 + beta_chi[1],
    )
    t = Fraction(5, 4) * (
        w[0] ** 2
        + w[1] ** 2
        + 2 * sum(value**2 for value in w[2:])
    )
    if t == 0:
        return Fraction(0)
    eta_norm_squared = eta[0] ** 2 + eta[1] ** 2
    delta = t**2 - eta_norm_squared
    zd = gaussian_multiply(z, d)
    zd_square = gaussian_multiply(zd, zd)
    real_eta_zd_square = (
        eta[0] * zd_square[0] - eta[1] * zd_square[1]
    )
    norm_product = (
        (z[0] ** 2 + z[1] ** 2)
        * (d[0] ** 2 + d[1] ** 2)
    )
    return (
        4
        * t
        / (25 * delta)
        * (
            (3 * t**2 - 5 * eta_norm_squared) * norm_product
            + 2 * t * real_eta_zd_square
        )
    )


def fixed_w_gram(w):
    """Return the exact 4 by 4 Gram matrix for one fixed generic w."""

    z_basis = ((1, 0), (0, 1), (1, 1))
    d_basis = z_basis
    constants = {}
    for z_number, z in enumerate(z_basis):
        for d_number, d in enumerate(d_basis):
            constant, linear, matrix = eliminate_positive(w, z, d)
            solution, pivots = secondary.exact_ldl_solve(matrix, linear)
            assert all(value > 0 for value in pivots)
            constants[z_number, d_number] = (
                constant
                - Fraction(1, 4)
                * sum(
                    value * solution_value
                    for value, solution_value in zip(linear, solution)
                )
            )

    # Coefficients in (z0^2,z0*z1,z1^2) times
    # (d0^2,d0*d1,d1^2).
    coefficient = [
        [Fraction(0) for _ in range(3)] for _ in range(3)
    ]
    coefficient[0][0] = constants[0, 0]
    coefficient[0][2] = constants[0, 1]
    coefficient[2][0] = constants[1, 0]
    coefficient[2][2] = constants[1, 1]
    coefficient[1][0] = (
        constants[2, 0] - coefficient[0][0] - coefficient[2][0]
    )
    coefficient[1][2] = (
        constants[2, 1] - coefficient[0][2] - coefficient[2][2]
    )
    coefficient[0][1] = (
        constants[0, 2] - coefficient[0][0] - coefficient[0][2]
    )
    coefficient[2][1] = (
        constants[1, 2] - coefficient[2][0] - coefficient[2][2]
    )
    coefficient[1][1] = constants[2, 2] - sum(
        sum(row) for row in coefficient
    )

    size = 4
    gram = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    # m=(z0*d0,z0*d1,z1*d0,z1*d1).  Split the unique Segre
    # ambiguity equally between m0*m3 and m1*m2.
    gram[0][0] = coefficient[0][0]
    gram[0][1] = gram[1][0] = coefficient[0][1] / 2
    gram[1][1] = coefficient[0][2]
    gram[0][2] = gram[2][0] = coefficient[1][0] / 2
    gram[1][3] = gram[3][1] = coefficient[1][2] / 2
    gram[2][2] = coefficient[2][0]
    gram[2][3] = gram[3][2] = coefficient[2][1] / 2
    gram[3][3] = coefficient[2][2]
    gram[0][3] = gram[3][0] = coefficient[1][1] / 4
    gram[1][2] = gram[2][1] = coefficient[1][1] / 4

    return gram, coefficient


def exact_ldl(matrix):
    """Unpivoted exact LDL, used only on generic positive matrices."""

    size = len(matrix)
    lower = [
        [Fraction(int(row == column)) for column in range(size)]
        for row in range(size)
    ]
    pivots = []
    for column in range(size):
        pivot = matrix[column][column] - sum(
            lower[column][index] ** 2 * pivots[index]
            for index in range(column)
        )
        pivots.append(pivot)
        if pivot == 0:
            continue
        for row in range(column + 1, size):
            lower[row][column] = (
                matrix[row][column]
                - sum(
                    lower[row][index]
                    * lower[column][index]
                    * pivots[index]
                    for index in range(column)
                )
            ) / pivot
    return pivots


def main():
    w = (1, -2, 3, 1, -1, 2)
    exact_core = eliminate_to_core(w)
    closed_core = predicted_core(w)
    assert exact_core == closed_core
    print("exact two-dimensional core")
    for name, matrix in zip(("K", "L", "C"), exact_core):
        print(name, matrix)
    gram, coefficient = fixed_w_gram(w)
    print("w", w)
    print("biform coefficients")
    for row in coefficient:
        print(*row)
    pivots = exact_ldl(gram)
    print("Gram size", len(gram))
    print("LDL pivots")
    print(*pivots)
    assert all(value > 0 for value in pivots)


if __name__ == "__main__":
    main()
