#!/usr/bin/env python3
"""Exact certificate for the noncentral S4-equivariant (2,3,2) branch."""

from __future__ import annotations

import itertools
import math

import numpy as np
import sympy as sp


def parity(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inversions % 2 else 1


def build_exact_paulis():
    """Return the metric and two exact multiplicity-space Pauli triples."""
    permutations = list(itertools.permutations(range(4)))
    matchings = [
        frozenset((frozenset((0, 1)), frozenset((2, 3)))),
        frozenset((frozenset((0, 2)), frozenset((1, 3)))),
        frozenset((frozenset((0, 3)), frozenset((1, 2)))),
    ]

    basis_two = sp.Matrix([[1, 0], [0, 1], [-1, -1]])
    basis_three = sp.Matrix(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, -1, -1]]
    )
    metric_two = basis_two.T * basis_two
    metric_three = basis_three.T * basis_three
    metric = sp.kronecker_product(
        metric_two, metric_three, metric_two
    )
    metric_inverse = metric.inv()

    representations = []
    standard = sp.zeros(12)
    twisted = sp.zeros(12)
    trivial_aa = sp.zeros(4)
    sign_aa = sp.zeros(4)
    for permutation in permutations:
        permutation_four = sp.zeros(4)
        for index in range(4):
            permutation_four[permutation[index], index] = 1
        representation_three = (
            permutation_four * basis_three
        )[:3, :]

        permutation_three = sp.zeros(3)
        for index, matching in enumerate(matchings):
            image = frozenset(
                frozenset(permutation[element] for element in pair)
                for pair in matching
            )
            permutation_three[matchings.index(image), index] = 1
        representation_two = (
            permutation_three * basis_two
        )[:2, :]

        representation = sp.kronecker_product(
            representation_two,
            representation_three,
            representation_two,
        )
        representations.append(representation)
        character = sum(
            permutation[index] == index for index in range(4)
        ) - 1
        standard += sp.Rational(character, 8) * representation
        twisted += (
            sp.Rational(parity(permutation) * character, 8)
            * representation
        )
        aa_representation = sp.kronecker_product(
            representation_two, representation_two
        )
        trivial_aa += aa_representation / 24
        sign_aa += parity(permutation) * aa_representation / 24

    def embed_aa(matrix):
        embedded = sp.zeros(12)
        for left in range(2):
            for middle in range(3):
                for right in range(2):
                    source = (left * 3 + middle) * 2 + right
                    for new_left in range(2):
                        for new_right in range(2):
                            target = (
                                (new_left * 3 + middle) * 2 + new_right
                            )
                            embedded[target, source] = matrix[
                                2 * new_left + new_right,
                                2 * left + right,
                            ]
        return embedded

    standard_low = embed_aa(trivial_aa)
    twisted_low = embed_aa(sign_aa)
    standard_high = standard - standard_low
    twisted_high = twisted - twisted_low

    def adjoint(matrix):
        return metric_inverse * matrix.conjugate().T * metric

    # A fixed elementary matrix has nonzero averaged intertwiners in both
    # isotypic components.  Their squared norms are 1/1296 and 1/144.
    elementary = sp.zeros(12)
    elementary[0, 1] = 1
    averaged = sum(
        (
            representation
            * elementary
            * representation.inv()
            for representation in representations
        ),
        sp.zeros(12),
    ) / 24
    standard_step = 36 * standard_high * averaged * standard_low
    twisted_step = 12 * twisted_high * averaged * twisted_low

    def pauli_triple(step, low, high):
        return (
            step + adjoint(step),
            -sp.I * (step - adjoint(step)),
            high - low,
        )

    paulis = (
        pauli_triple(standard_step, standard_low, standard_high),
        pauli_triple(twisted_step, twisted_low, twisted_high),
    )
    return metric, standard, twisted, paulis


def gaussian_matmul(first, second):
    """Multiply Gaussian-integer matrices represented by real/imag pairs."""
    first_real, first_imaginary = first
    second_real, second_imaginary = second
    return (
        first_real @ second_real - first_imaginary @ second_imaginary,
        first_real @ second_imaginary + first_imaginary @ second_real,
    )


def gaussian_subtract(first, second):
    return first[0] - second[0], first[1] - second[1]


def exact_residual_polynomials(paulis):
    """Extract selected residual coordinates by exact int64 arithmetic.

    Multiplying every Pauli generator by 12 gives Gaussian-integer
    matrices.  The cubic residual multiplied by 12^3=1728 therefore has
    Gaussian-integer coefficient matrices.  The conservative entry bound
    for every triple product is

        72^2 * 16^3 < 22e6,

    far below the signed-int64 limit.
    """
    integer_paulis = []
    for matrix in paulis[0] + paulis[1]:
        real = np.zeros((12, 12), dtype=np.int64)
        imaginary = np.zeros((12, 12), dtype=np.int64)
        for row in range(12):
            for column in range(12):
                entry = sp.expand(12 * matrix[row, column])
                real_part = sp.re(entry)
                imaginary_part = sp.im(entry)
                assert real_part.is_Integer
                assert imaginary_part.is_Integer
                real[row, column] = int(real_part)
                imaginary[row, column] = int(imaginary_part)
        assert np.max(np.abs(real)) <= 16
        assert np.max(np.abs(imaginary)) <= 16
        integer_paulis.append((real, imaginary))

    identity = np.eye(6, dtype=np.int64)
    zero = np.zeros((6, 6), dtype=np.int64)
    left = [
        (
            np.kron(matrix[0], identity),
            np.kron(matrix[1], identity),
        )
        for matrix in integer_paulis
    ]
    right = [
        (
            np.kron(identity, matrix[0]),
            np.kron(identity, matrix[1]),
        )
        for matrix in integer_paulis
    ]

    left_right = [
        [
            gaussian_matmul(left[first], right[middle])
            for middle in range(6)
        ]
        for first in range(6)
    ]
    right_left = [
        [
            gaussian_matmul(right[first], left[middle])
            for middle in range(6)
        ]
        for first in range(6)
    ]
    monomials = list(
        itertools.combinations_with_replacement(range(6), 3)
    )
    coefficients = {
        monomial: (
            np.zeros((72, 72), dtype=np.int64),
            np.zeros((72, 72), dtype=np.int64),
        )
        for monomial in monomials
    }
    for first, middle, last in itertools.product(range(6), repeat=3):
        forward = gaussian_matmul(
            left_right[first][middle], left[last]
        )
        backward = gaussian_matmul(
            right_left[first][middle], right[last]
        )
        contribution = gaussian_subtract(forward, backward)
        target = coefficients[tuple(sorted((first, middle, last)))]
        target[0][:] += contribution[0]
        target[1][:] += contribution[1]
    assert max(
        int(np.max(np.abs(part)))
        for coefficient in coefficients.values()
        for part in coefficient
    ) < 100_000_000

    # The linear term in 1728 times the residual is
    # -(1728/36)(12 H_1 - 12 H_2) = -48(L-R).
    linear = [
        (
            -48 * (left[index][0] - right[index][0]),
            -48 * (left[index][1] - right[index][1]),
        )
        for index in range(6)
    ]
    variables = sp.symbols("x y z u v w", real=True)

    def coordinate_polynomial(row, column, part):
        part_index = 0 if part == "real" else 1
        values = [
            int(coefficients[monomial][part_index][row, column])
            for monomial in monomials
        ]
        values.extend(
            int(linear[index][part_index][row, column])
            for index in range(6)
        )
        assert any(values)
        divisor = 0
        for value in values:
            divisor = math.gcd(divisor, abs(value))
        values = [value // divisor for value in values]
        if next(value for value in values if value) < 0:
            values = [-value for value in values]
        polynomial = sum(
            coefficient
            * variables[first]
            * variables[middle]
            * variables[last]
            for coefficient, (first, middle, last) in zip(
                values, monomials
            )
        ) + sum(
            values[len(monomials) + index] * variables[index]
            for index in range(6)
        )
        return sp.expand(polynomial), divisor

    sparse_locations = [
        (6, 51, "imaginary"),
        (6, 65, "imaginary"),
        (2, 55, "imaginary"),
        (2, 45, "imaginary"),
        (20, 51, "imaginary"),
        (34, 65, "imaginary"),
        (0, 51, "real"),
        (0, 57, "imaginary"),
        (2, 0, "imaginary"),
        (12, 0, "imaginary"),
        (14, 0, "real"),
        (14, 0, "imaginary"),
        (20, 37, "imaginary"),
        (0, 0, "real"),
        (0, 0, "imaginary"),
        (0, 43, "imaginary"),
        (6, 37, "imaginary"),
        (14, 51, "real"),
        (2, 55, "real"),
        (3, 1, "imaginary"),
    ]
    killer_locations = [
        (17, 17, "imaginary"),
        (8, 6, "real"),
        (1, 1, "real"),
    ]
    sparse = [
        coordinate_polynomial(*location)[0]
        for location in sparse_locations
    ]
    killers = [
        coordinate_polynomial(*location)[0]
        for location in killer_locations
    ]
    return variables, sparse, killers


def main():
    metric, standard, twisted, paulis = build_exact_paulis()
    metric_inverse = metric.inv()

    def adjoint(matrix):
        return metric_inverse * matrix.conjugate().T * metric

    assert standard * standard == standard
    assert twisted * twisted == twisted
    assert standard + twisted == sp.eye(12)
    assert standard * twisted == sp.zeros(12)
    assert sp.trace(standard) == 6
    assert sp.trace(twisted) == 6
    for central, triple in zip((standard, twisted), paulis):
        for matrix in triple:
            assert adjoint(matrix) == matrix
            assert matrix * matrix == central
            assert sp.trace(matrix) == 0
        assert triple[0] * triple[1] == sp.I * triple[2]
        assert triple[1] * triple[2] == sp.I * triple[0]
        assert triple[2] * triple[0] == sp.I * triple[1]

    variables, sparse, killers = exact_residual_polynomials(paulis)
    x, y, z, u, v, w = variables
    expected_sparse = [
        v * x * (-w + z),
        u * y * (-w + z),
        -u * v * w - u * v * z + 2 * x * y * z,
        2 * u * v * z - 3 * w * x * y + x * y * z,
        -4 * u * w * y + v * w * x + 3 * v * x * z,
        -u * w * y - 3 * u * y * z + 4 * v * x * z,
        -u * v**2 + u * w * z - u * z**2 + v * x * y,
        (-w + z) * (-u * y + v * x),
        -u * v * z - u * w * y + v * x * z + x * y * z,
        -u * v * z + u * w * y - v * x * z + x * y * z,
        (-w + z) * (u * x - v * y),
        -u * x * y + v * w * z + v * x**2 - v * z**2,
        (-w + z) * (u * y + v * x),
        3 * u * w * x + 5 * u * x * z
        + 5 * v * w * y + 3 * v * y * z,
        5 * u * x * y - 5 * v * w * z
        + 3 * v * x**2 - 3 * v * z**2,
        -11 * u * w * y + 3 * u * y * z
        + 3 * v * w * x + 5 * v * x * z,
        -13 * u * w * y - 3 * u * y * z
        + 3 * v * w * x + 13 * v * x * z,
        3 * u * v**2 + 13 * u * w * z
        + 3 * u * z**2 + 13 * v * x * y,
        -u**2 * x - 2 * u * v * y + v**2 * x
        + x**3 + x * y**2,
        u * v * z - 2 * u * w * y + 2 * v * x * z
        - 3 * w * x * y + 2 * x * y * z,
    ]
    expected_killers = [
        9 * u * v * w - 3 * u * v * z + 24 * v**2 * y
        - 24 * w**2 * y + 9 * w * x * y + 24 * x**2 * y
        - 15 * x * y * z - 8 * y,
        6 * u**3 - 2 * u * v * y + 2 * u * w * z + 2 * u
        - 3 * v**2 * x + 2 * v * x * y - 3 * w**2 * x
        + x * y**2 - x * z**2,
        9 * u**2 * w + 9 * u**2 * z - 9 * v**2 * w
        + 39 * v**2 * z - 9 * w**3 - 21 * w**2 * z
        + 27 * w * x**2 + 9 * w * y**2 - 27 * w * z**2
        + 3 * x**2 * z + 9 * y**2 * z + 9 * z**3 - 16 * z,
    ]
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(sparse, expected_sparse)
    )
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(killers, expected_killers)
    )

    spheres = [
        x**2 + y**2 + z**2 - 1,
        u**2 + v**2 + w**2 - 1,
    ]
    basis = sp.groebner(
        spheres + sparse,
        *variables,
        order="grevlex",
        domain=sp.QQ,
    )
    consequences = [
        u * (v**2 + w**2),
        u * (z - w),
        x * y - u * v,
        w * (w**2 - 1),
        v * (z - w),
        v * (u * y - v * x),
        x * (z**2 - w**2),
    ]
    assert all(
        basis.reduce(consequence)[1] == 0
        for consequence in consequences
    )

    full_basis = sp.groebner(
        spheres + sparse + killers,
        *variables,
        order="grevlex",
        domain=sp.QQ,
    )
    assert len(full_basis.polys) == 1
    assert full_basis.polys[0].as_expr() == 1

    # Independent replay of the human branch argument.
    branch_a = sp.groebner(
        [
            u**2 - 1,
            v,
            w,
            z,
            x * y,
            x**2 + y**2 - 1,
        ],
        *variables,
        order="grevlex",
        domain=sp.QQ,
    )
    assert branch_a.reduce(killers[1] - 8 * u)[1] == 0

    branch_b = sp.groebner(
        [u, w, z, x, v**2 - 1, y**2 - 1],
        *variables,
        order="grevlex",
        domain=sp.QQ,
    )
    assert branch_b.reduce(killers[0] - 16 * y)[1] == 0

    branch_c = sp.groebner(
        [u, v, x, w**2 - 1, y**2 + z**2 - 1],
        *variables,
        order="grevlex",
        domain=sp.QQ,
    )
    assert branch_c.reduce(killers[0] + 32 * y)[1] == 0
    branch_c_endpoints = sp.groebner(
        [u, v, x, y, w**2 - 1, z**2 - 1],
        *variables,
        order="grevlex",
        domain=sp.QQ,
    )
    assert branch_c_endpoints.reduce(
        killers[2] + 36 * w + 28 * z
    )[1] == 0
    assert all(
        -36 * sign_w - 28 * sign_z != 0
        for sign_w in (-1, 1)
        for sign_z in (-1, 1)
    )

    print("Exact S4 multiplicity Pauli triples: verified.")
    print("Selected cubic coordinates: 20 sparse + 3 branch killers.")
    print("Seven branch consequences: exact Groebner reductions to zero.")
    print("Full selected-coordinate ideal with sphere constraints: <1>.")
    print("Human branch replay: A, B, and both C circles excluded exactly.")
    print("Noncentral S4-equivariant rank-six branch: EMPTY.")
    print("All assertions passed (rational/Gaussian-integer arithmetic).")


if __name__ == "__main__":
    main()
