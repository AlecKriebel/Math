#!/usr/bin/env python3
"""Exact no-go certificate for the quadratic mixed-support dual ansatz.

On the canonical [4,1] x [4,1] x [3,2] highest-weight multiplicity carrier,
this script constructs all fourteen effective real/site-symmetric corrections

    PT_A(C_s^dagger T C_s),

and an exact rational PSD separator H.  It verifies

    Tr(H K_a) = 0  for every correction K_a,
    Tr(H Q) = -44943/4096000 < 0.

Thus no linear combination of these corrections can make Q positive
semidefinite.  Only dependency-free integer and Fraction arithmetic is used.
"""

from fractions import Fraction as F
from itertools import permutations
import sys

sys.path.insert(0, "verification")
import agent_dth_block_census as census
import agent_dth_cross_carrier_twirling as twirl


EFFECTIVE_MONOMIALS = (
    (0, 0, 0),
    (0, 0, 1),
    (0, 0, 2),
    (0, 0, 4),
    (0, 1, 2),
    (0, 2, 2),
    (0, 2, 3),
    (0, 2, 4),
    (0, 4, 4),
    (0, 5, 5),
    (2, 2, 2),
    (2, 2, 3),
    (2, 2, 4),
    (2, 3, 4),
)

REAL_BASIS, PHASES = twirl.target_local_basis()
MONOMIAL_TERMS = {
    word: tuple(sorted(set(permutations(word)))) for word in EFFECTIVE_MONOMIALS
}


def state_digits(state):
    return (state // 9, (state // 3) % 3, state % 3)


def gaussian_mul(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def local_entry(basis_index, row, column):
    row_index = twirl.TARGET_INDEX[row]
    column_index = twirl.TARGET_INDEX[column]
    coefficient = REAL_BASIS[basis_index].get((row_index, column_index), 0)
    phase = ((1, 0), (0, 1))[PHASES[basis_index]]
    return (coefficient * phase[0], coefficient * phase[1])


def raw_target_entry(monomial, row, column):
    row_digits = tuple(state_digits(state) for state in row)
    column_digits = tuple(state_digits(state) for state in column)
    value = (0, 0)
    for term in MONOMIAL_TERMS[monomial]:
        product_value = (1, 0)
        for site, basis_index in enumerate(term):
            local_row = tuple(word[site] for word in row_digits)
            local_column = tuple(word[site] for word in column_digits)
            product_value = gaussian_mul(
                product_value,
                local_entry(basis_index, local_row, local_column),
            )
            if product_value == (0, 0):
                break
        value = (value[0] + product_value[0], value[1] + product_value[1])
    # The selected real/conjugation-invariant monomials have real entries.
    assert value[1] == 0
    return value[0]


def wedge_target_entry(monomial, row, column):
    """Entry between unnormalized canonical spectator-wedge coordinates."""
    (a, b), z = row
    (c, d), y = column
    value = 0
    for first, second, row_sign in ((a, b, 1), (b, a, -1)):
        for third, fourth, column_sign in ((c, d, 1), (d, c, -1)):
            value += row_sign * column_sign * raw_target_entry(
                monomial, (first, second, z), (third, fourth, y)
            )
    return value


def correction_matrix(wedge_basis, monomial):
    size = len(wedge_basis)
    matrix = [[F(0) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            # By self-adjointness of partial transpose,
            # K_ij = Tr(C PT(|v_j><v_i|) C^dagger T).
            column = census.support_pt_column(wedge_basis[j], wedge_basis[i])
            value = F(0)
            for (
                pair_row,
                other_row,
                first_pair,
                pair_column,
                z,
            ), coefficient in column.items():
                p, q = first_pair
                if z == p:
                    other_column, sign = q, 1
                elif z == q:
                    other_column, sign = p, -1
                else:
                    continue
                value += coefficient * sign * wedge_target_entry(
                    monomial,
                    (pair_column, other_column),
                    (pair_row, other_row),
                )
            matrix[i][j] = value
    assert matrix == [list(row) for row in zip(*matrix)]
    return matrix


def matrix_pairing(left, right):
    return sum(
        left[i][j] * right[i][j]
        for i in range(len(left))
        for j in range(len(left))
    )


def matmul(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def ldl_diagonal(matrix):
    work = [row[:] for row in matrix]
    diagonal = []
    for k in range(len(work)):
        pivot = work[k][k]
        assert pivot
        diagonal.append(pivot)
        for i in range(k + 1, len(work)):
            for j in range(k + 1, len(work)):
                work[i][j] -= work[i][k] * work[k][j] / pivot
    return diagonal


def main():
    shapes = ((4, 1), (4, 1), (3, 2))
    bases = {shape: census.specht_basis(shape) for shape in census.PARTITIONS}
    _, _, size, inertia, good_basis = census.block_data(shapes, bases)
    assert size == 7 and inertia == (6, 1, 0)
    wedge_basis = [census.wedge_coordinates(vector) for vector in good_basis]

    witness = [
        [
            census.inner(good_basis[i], census.lifted_O0(good_basis[j]))
            for j in range(size)
        ]
        for i in range(size)
    ]
    corrections = [
        correction_matrix(wedge_basis, monomial)
        for monomial in EFFECTIVE_MONOMIALS
    ]

    # An exact rank-one relation in the correction span.
    r = [3, -6, 5, -2, -4, -7, -14]
    rank_one = [
        [
            -3 * corrections[0][i][j]
            + 11 * corrections[1][i][j]
            - 8 * corrections[2][i][j]
            + 4 * corrections[3][i][j]
            for j in range(size)
        ]
        for i in range(size)
    ]
    assert all(
        rank_one[i][j] == -F(5, 96) * r[i] * r[j]
        for i in range(size)
        for j in range(size)
    )

    # Columns of B are an integer basis of r^perp.
    B = [[0 for _ in range(6)] for _ in range(7)]
    for j in range(1, 7):
        B[j][j - 1] = r[0]
        B[0][j - 1] = -r[j]

    G = [
        [F(3, 128), F(7651, 1440000), -F(40681, 2880000), F(19, 2000), F(3, 1000), -F(1, 500)],
        [F(7651, 1440000), F(13, 2000), -F(17, 2000), F(9, 1000), -F(1, 500), F(1, 1000)],
        [-F(40681, 2880000), -F(17, 2000), F(43, 2000), -F(7, 500), -F(1, 500), F(1, 2000)],
        [F(19, 2000), F(9, 1000), -F(7, 500), F(37, 2000), -F(1, 200), F(3, 2000)],
        [F(3, 1000), -F(1, 500), -F(1, 500), -F(1, 200), F(3, 500), -F(1, 400)],
        [-F(1, 500), F(1, 1000), F(1, 2000), F(3, 2000), -F(1, 400), F(3, 2000)],
    ]

    # Exact positive definiteness of G, hence H=B G B^T >= 0.
    diagonal = ldl_diagonal(G)
    assert diagonal == [
        F(3, 128),
        F(257362199, 48600000000),
        F(15826251843, 2058897592000),
        F(7006171723, 1266100147440),
        F(54168407301, 43788573268750),
        F(137174154077, 866694516816000),
    ]
    assert all(value > 0 for value in diagonal)

    H = matmul(matmul(B, G), transpose(B))
    assert all(sum(H[i][j] * r[j] for j in range(7)) == 0 for i in range(7))
    correction_pairings = [matrix_pairing(H, matrix) for matrix in corrections]
    assert correction_pairings == [F(0)] * len(corrections)
    witness_pairing = matrix_pairing(H, witness)
    assert witness_pairing == -F(44943, 4096000)

    print("exact quadratic support-dual no-go certificate passed")
    print("carrier:", shapes, "dimension", size, "witness inertia", inertia)
    print("effective corrections annihilated:", len(corrections))
    print("separator rank: 6")
    print("separator/witness pairing:", witness_pairing)


if __name__ == "__main__":
    main()
