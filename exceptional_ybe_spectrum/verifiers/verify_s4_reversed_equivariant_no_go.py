#!/usr/bin/env python3
"""Exact no-go certificate for the S4-equivariant (3,2,3) branch.

All residual arithmetic is performed in

    Z[s, i] / (s^2 - 3)

after multiplying each local commutant generator by 24.  For each of
the five half-rank signatures up to complementation, a fixed list of
real-rational matrix coordinates spans the constant polynomial 1.
Consequently the shifted cubic residual cannot vanish.
"""

from __future__ import annotations

import itertools

import numpy as np
import sympy as sp


SCALE = 24

# Coordinates refer to the real-rational component of
# SCALE^3 times the 108 by 108 shifted cubic residual.
COORDINATE_CERTIFICATES = {
    (0, 0, 0, 1, 2): (
        (94, 64),
        (93, 107),
        (89, 89),
        (88, 84),
        (92, 60),
        (94, 43),
        (94, 60),
        (54, 28),
    ),
    (0, 0, 0, 2, 1): (
        (93, 107),
        (94, 64),
        (93, 79),
        (89, 89),
        (102, 103),
        (96, 51),
        (93, 2),
        (60, 42),
    ),
    (0, 1, 1, 0, 2): (
        (100, 100),
        (89, 89),
        (92, 92),
        (96, 60),
        (106, 99),
        (66, 89),
        (88, 107),
        (89, 3),
        (106, 43),
        (72, 18),
    ),
    (0, 1, 1, 1, 1): (
        (2, 0),
        (3, 22),
        (4, 1),
        (5, 26),
        (5, 31),
        (6, 90),
        (8, 3),
        (8, 5),
        (8, 38),
        (8, 39),
        (8, 46),
        (8, 92),
        (10, 40),
        (11, 105),
        (13, 7),
        (15, 20),
        (15, 32),
        (15, 51),
        (15, 104),
        (16, 46),
        (16, 64),
        (16, 75),
        (16, 99),
        (17, 29),
        (17, 62),
        (37, 1),
        (38, 32),
        (40, 10),
        (40, 40),
        (41, 78),
        (41, 79),
        (44, 42),
        (47, 38),
        (47, 48),
        (47, 56),
        (49, 97),
        (50, 14),
        (50, 54),
        (50, 86),
        (51, 17),
        (51, 68),
        (51, 87),
        (52, 18),
        (54, 51),
        (55, 67),
        (55, 68),
        (55, 103),
        (58, 60),
        (59, 17),
        (59, 64),
        (59, 70),
        (59, 75),
        (59, 101),
        (61, 55),
        (61, 61),
        (62, 57),
        (63, 16),
        (68, 80),
        (70, 82),
    ),
    (0, 1, 1, 2, 0): (
        (106, 64),
        (97, 64),
        (75, 80),
        (100, 46),
        (89, 83),
        (66, 31),
        (106, 89),
        (96, 46),
        (102, 102),
        (75, 104),
    ),
}


def parity(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inversions % 2 else 1


def exact_s4_data():
    permutations = list(itertools.permutations(range(4)))
    matchings = [
        frozenset((frozenset((0, 1)), frozenset((2, 3)))),
        frozenset((frozenset((0, 2)), frozenset((1, 3)))),
        frozenset((frozenset((0, 3)), frozenset((1, 2)))),
    ]
    basis_three = sp.Matrix(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, -1, -1]]
    )
    basis_two = sp.Matrix([[1, 0], [0, 1], [-1, -1]])
    metric = sp.kronecker_product(
        basis_three.T * basis_three,
        basis_two.T * basis_two,
        basis_three.T * basis_three,
    )
    metric_inverse = metric.inv()

    representations = []
    inverse_representations = []
    outer_representations = []
    characters = []
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
            representation_three,
            representation_two,
            representation_three,
        )
        representations.append(representation)
        inverse_representations.append(representation.inv())
        outer_representations.append(
            sp.kronecker_product(
                representation_three, representation_three
            )
        )
        character_three = sum(
            permutation[index] == index for index in range(4)
        ) - 1
        character_two = sp.trace(permutation_three) - 1
        characters.append(
            (
                1,
                parity(permutation),
                character_two,
                character_three,
                parity(permutation) * character_three,
            )
        )

    dimensions = (1, 1, 2, 3, 3)
    central = []
    outer = []
    for character_index, dimension in enumerate(dimensions):
        central.append(
            sum(
                (
                    sp.Rational(
                        dimension * characters[index][character_index],
                        24,
                    )
                    * representations[index]
                    for index in range(24)
                ),
                sp.zeros(18),
            )
        )
        outer.append(
            sum(
                (
                    sp.Rational(
                        dimension * characters[index][character_index],
                        24,
                    )
                    * outer_representations[index]
                    for index in range(24)
                ),
                sp.zeros(9),
            )
        )

    def embed_outer(matrix):
        embedded = sp.zeros(18)
        for left, middle, right in itertools.product(
            range(3), range(2), range(3)
        ):
            source = (left * 2 + middle) * 3 + right
            for new_left, new_right in itertools.product(
                range(3), repeat=2
            ):
                target = (new_left * 2 + middle) * 3 + new_right
                embedded[target, source] = matrix[
                    3 * new_left + new_right,
                    3 * left + right,
                ]
        return embedded

    low = (
        central[2] * embed_outer(outer[0]),
        central[3] * embed_outer(outer[3]),
        central[4] * embed_outer(outer[3]),
    )

    def adjoint(matrix):
        return metric_inverse * matrix.conjugate().T * metric

    def averaged_elementary(row, column):
        elementary = sp.zeros(18)
        elementary[row, column] = 1
        return sum(
            (
                representation
                * elementary
                * representation_inverse
                for representation, representation_inverse in zip(
                    representations, inverse_representations
                )
            ),
            sp.zeros(18),
        ) / 24

    sources = ((0, 3), (1, 0), (1, 0))
    normalizations = (sp.Integer(8), 24 * sp.sqrt(3), 8 * sp.sqrt(3))
    paulis = []
    for central_projector, low_projector, source, normalization in zip(
        central[2:], low, sources, normalizations
    ):
        high_projector = central_projector - low_projector
        step = (
            normalization
            * high_projector
            * averaged_elementary(*source)
            * low_projector
        )
        assert sp.simplify(adjoint(step) * step - low_projector) == sp.zeros(18)
        assert sp.simplify(step * adjoint(step) - high_projector) == sp.zeros(18)
        paulis.append(
            (
                sp.simplify(step + adjoint(step)),
                sp.simplify(-sp.I * (step - adjoint(step))),
                sp.simplify(high_projector - low_projector),
            )
        )

    return metric, tuple(central), tuple(paulis)


def exact_components(matrix):
    result = np.zeros((4, matrix.rows, matrix.cols), dtype=np.int64)
    square_root = sp.sqrt(3)
    for row in range(matrix.rows):
        for column in range(matrix.cols):
            entry = sp.expand(SCALE * matrix[row, column])
            for offset, part in (
                (0, sp.re(entry)),
                (2, sp.im(entry)),
            ):
                constant = sp.simplify(part.subs(square_root, 0))
                radical = sp.simplify((part - constant) / square_root)
                assert constant.is_Integer
                assert radical.is_Integer
                result[offset, row, column] = int(constant)
                result[offset + 1, row, column] = int(radical)
    return result


def quadratic_matmul(first, second):
    return (
        first[0] @ second[0] + 3 * (first[1] @ second[1]),
        first[0] @ second[1] + first[1] @ second[0],
    )


def algebra_matmul(first, second):
    real_real = quadratic_matmul(first[:2], second[:2])
    imag_imag = quadratic_matmul(first[2:], second[2:])
    real_imag = quadratic_matmul(first[:2], second[2:])
    imag_real = quadratic_matmul(first[2:], second[:2])
    return np.stack(
        (
            real_real[0] - imag_imag[0],
            real_real[1] - imag_imag[1],
            real_imag[0] + imag_real[0],
            real_imag[1] + imag_real[1],
        )
    )


def local_generators(signature, central, paulis):
    simple_one, simple_sign, *multiplicity_ranks = signature
    fixed = (
        (1 if simple_one else -1) * central[0]
        + (1 if simple_sign else -1) * central[1]
    )
    active = []
    for multiplicity_rank, projector, triple in zip(
        multiplicity_ranks, central[2:], paulis
    ):
        if multiplicity_rank == 0:
            fixed -= projector
        elif multiplicity_rank == 2:
            fixed += projector
        else:
            assert multiplicity_rank == 1
            active.extend(triple)
    return (fixed, *active)


def selected_coordinate_matrix(signature, coordinates, central, paulis):
    """Return selected residual-coordinate coefficients over all monomials."""
    local = [
        exact_components(matrix)
        for matrix in local_generators(signature, central, paulis)
    ]
    count = len(local)
    variable_count = count - 1
    identity_six = np.eye(6, dtype=np.int64)
    left = [
        np.stack(
            tuple(np.kron(component, identity_six) for component in matrix)
        )
        for matrix in local
    ]
    right = [
        np.stack(
            tuple(np.kron(identity_six, component) for component in matrix)
        )
        for matrix in local
    ]
    left_right = [
        [algebra_matmul(left[i], right[j]) for j in range(count)]
        for i in range(count)
    ]
    right_left = [
        [algebra_matmul(right[i], left[j]) for j in range(count)]
        for i in range(count)
    ]

    # Every monomial of total degree at most three occurs after the fixed
    # coefficient x_0=1 is substituted.
    exponents = tuple(
        exponent
        for total_degree in range(4)
        for exponent in itertools.product(range(total_degree + 1), repeat=variable_count)
        if sum(exponent) == total_degree
    )
    # Put the exponent tuples in the same ordinary lexicographic order
    # used by the discovery calculation.
    exponents = tuple(sorted(exponents))
    exponent_index = {
        exponent: index for index, exponent in enumerate(exponents)
    }
    rows = np.zeros(
        (len(coordinates), len(exponents)), dtype=np.int64
    )

    for first, middle, last in itertools.product(range(count), repeat=3):
        exponent = [0] * variable_count
        for index in (first, middle, last):
            if index:
                exponent[index - 1] += 1
        column = exponent_index[tuple(exponent)]
        forward = algebra_matmul(left_right[first][middle], left[last])
        backward = algebra_matmul(right_left[first][middle], right[last])
        for coordinate_index, (row, matrix_column) in enumerate(coordinates):
            rows[coordinate_index, column] += int(
                forward[0, row, matrix_column]
                - backward[0, row, matrix_column]
            )

    linear_factor = SCALE * SCALE // 3
    zero_column = exponent_index[(0,) * variable_count]
    for coordinate_index, (row, matrix_column) in enumerate(coordinates):
        rows[coordinate_index, zero_column] -= linear_factor * int(
            left[0][0, row, matrix_column]
            - right[0][0, row, matrix_column]
        )
    for index in range(1, count):
        exponent = [0] * variable_count
        exponent[index - 1] = 1
        column = exponent_index[tuple(exponent)]
        for coordinate_index, (row, matrix_column) in enumerate(coordinates):
            rows[coordinate_index, column] -= linear_factor * int(
                left[index][0, row, matrix_column]
                - right[index][0, row, matrix_column]
            )

    assert np.max(np.abs(rows)) < 100_000_000
    return exponents, rows


def half_rank_signatures():
    signatures = []
    for simple_one, simple_sign in itertools.product(range(2), repeat=2):
        for ranks in itertools.product(range(3), repeat=3):
            if (
                simple_one
                + simple_sign
                + 2 * ranks[0]
                + 3 * ranks[1]
                + 3 * ranks[2]
                == 9
            ):
                signatures.append((simple_one, simple_sign, *ranks))
    return tuple(signatures)


def main():
    metric, central, paulis = exact_s4_data()
    metric_inverse = metric.inv()

    def adjoint(matrix):
        return metric_inverse * matrix.conjugate().T * metric

    assert sum(central, sp.zeros(18)) == sp.eye(18)
    assert [sp.trace(projector) for projector in central] == [1, 1, 4, 6, 6]
    assert sum(
        1 if multiplicity == 1 else multiplicity * multiplicity
        for multiplicity in (1, 1, 2, 2, 2)
    ) == 14
    for first, projector in enumerate(central):
        assert projector * projector == projector
        for second in range(first):
            assert projector * central[second] == sp.zeros(18)
    for projector, triple in zip(central[2:], paulis):
        for matrix in triple:
            assert adjoint(matrix) == matrix
            assert sp.simplify(matrix * matrix - projector) == sp.zeros(18)
            assert sp.trace(matrix) == 0
        assert sp.simplify(triple[0] * triple[1] - sp.I * triple[2]) == sp.zeros(18)
        assert sp.simplify(triple[1] * triple[2] - sp.I * triple[0]) == sp.zeros(18)
        assert sp.simplify(triple[2] * triple[0] - sp.I * triple[1]) == sp.zeros(18)

    signatures = half_rank_signatures()
    expected_signatures = {
        (0, 0, 0, 1, 2),
        (0, 0, 0, 2, 1),
        (0, 1, 1, 0, 2),
        (0, 1, 1, 1, 1),
        (0, 1, 1, 2, 0),
        (1, 0, 1, 0, 2),
        (1, 0, 1, 1, 1),
        (1, 0, 1, 2, 0),
        (1, 1, 2, 0, 1),
        (1, 1, 2, 1, 0),
    }
    assert set(signatures) == expected_signatures
    assert {
        tuple(1 - value for value in signature[:2])
        + tuple(2 - value for value in signature[2:])
        for signature in COORDINATE_CERTIFICATES
    } | set(COORDINATE_CERTIFICATES) == expected_signatures

    print("Exact decomposition ranks: 1, 1, 4, 6, 6.")
    print("Full equivariant commutant: C + C + M2 + M2 + M2 (dimension 14).")
    print("Balanced signatures: 10, paired into 5 by H -> -H.")

    for signature, coordinates in COORDINATE_CERTIFICATES.items():
        exponents, coefficient_rows = selected_coordinate_matrix(
            signature, coordinates, central, paulis
        )
        domain_matrix = sp.polys.matrices.DomainMatrix.from_list_sympy(
            *coefficient_rows.shape, coefficient_rows.tolist()
        ).to_field()
        row_reduced, _ = domain_matrix.rref()
        reduced_rows = row_reduced.to_Matrix().tolist()
        constant_target = [sp.Integer(1)] + [
            sp.Integer(0) for _ in range(len(exponents) - 1)
        ]
        assert constant_target in reduced_rows
        print(
            "signature",
            signature,
            ":",
            len(coordinates),
            "coordinates span constant 1 among",
            len(exponents),
            "monomials.",
        )

    print("All five complement representatives fail the shifted cubic.")
    print("Complete diagonal-S4-equivariant (3,2,3) half-rank branch: EMPTY.")
    print("All assertions passed (exact Q(sqrt(3), i) arithmetic).")


if __name__ == "__main__":
    main()
