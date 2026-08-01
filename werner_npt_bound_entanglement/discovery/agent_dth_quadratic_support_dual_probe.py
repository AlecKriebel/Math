#!/usr/bin/env python3
"""Numerical probe of the invariant quadratic support-ideal dual.

This is discovery code, not a verifier.  It imports the exact highest-weight
carrier construction and builds the fourteen effective real, site-symmetric
quadratic support corrections on a selected carrier.  CVXPY then searches for
a common correction and prints the separating dual density.
"""

from fractions import Fraction as F
from itertools import permutations
import sys

import cvxpy as cp
import numpy as np

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


def local_entry(basis_index, row, column):
    row_index = twirl.TARGET_INDEX[row]
    column_index = twirl.TARGET_INDEX[column]
    coefficient = REAL_BASIS[basis_index].get((row_index, column_index), 0)
    return coefficient * (1j ** PHASES[basis_index])


def raw_target_entry(monomial, row, column):
    row_digits = tuple(state_digits(state) for state in row)
    column_digits = tuple(state_digits(state) for state in column)
    value = 0j
    for term in MONOMIAL_TERMS[monomial]:
        product_value = 1 + 0j
        for site, basis_index in enumerate(term):
            local_row = tuple(word[site] for word in row_digits)
            local_column = tuple(word[site] for word in column_digits)
            product_value *= local_entry(basis_index, local_row, local_column)
            if not product_value:
                break
        value += product_value
    assert abs(value.imag) < 1e-10
    return int(round(value.real))


def wedge_target_entry(monomial, row, column):
    """Matrix entry between unnormalized canonical spectator wedges."""
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
            # Trace(PT(|v_j><v_i|) C^dagger T C).
            column = census.support_pt_column(wedge_basis[j], wedge_basis[i])
            value = F(0)
            for (pair_row, other_row, first_pair, pair_column, z), x in column.items():
                p, q = first_pair
                if z == p:
                    other_column, sign = q, 1
                elif z == q:
                    other_column, sign = p, -1
                else:
                    continue
                value += x * sign * wedge_target_entry(
                    monomial,
                    (pair_column, other_column),
                    (pair_row, other_row),
                )
            matrix[i][j] = value
    assert matrix == [list(row) for row in zip(*matrix)]
    return matrix


def carrier_matrices(shapes):
    bases = {shape: census.specht_basis(shape) for shape in census.PARTITIONS}
    _, _, size, inertia, good_basis = census.block_data(shapes, bases)
    wedge_basis = [census.wedge_coordinates(vector) for vector in good_basis]
    witness = [
        [census.inner(good_basis[i], census.lifted_O0(good_basis[j]))
         for j in range(size)]
        for i in range(size)
    ]
    corrections = [
        correction_matrix(wedge_basis, monomial)
        for monomial in EFFECTIVE_MONOMIALS
    ]
    return inertia, witness, corrections


def main():
    shapes = ((4, 1), (4, 1), (3, 2))
    inertia, witness_exact, corrections_exact = carrier_matrices(shapes)
    witness = np.array(witness_exact, dtype=float)
    corrections = [np.array(matrix, dtype=float) for matrix in corrections_exact]
    size = len(witness)

    coefficients = cp.Variable(len(corrections))
    gamma = cp.Variable()
    corrected = witness - sum(
        coefficients[index] * matrix for index, matrix in enumerate(corrections)
    )
    constraint = corrected - gamma * np.eye(size) >> 0
    problem = cp.Problem(cp.Maximize(gamma), [constraint])
    problem.solve(solver="CLARABEL")

    print("carrier", shapes, "inertia", inertia)
    print("status", problem.status, "best gamma", problem.value)
    print("coefficients", coefficients.value)
    print("corrected eigenvalues", np.linalg.eigvalsh(corrected.value))
    dual = constraint.dual_value
    print("dual eigenvalues", np.linalg.eigvalsh(dual))
    print("dual trace", np.trace(dual))
    print("dual witness pairing", np.trace(dual @ witness))
    print("dual correction pairings")
    print(np.array([np.trace(dual @ matrix) for matrix in corrections]))
    np.set_printoptions(linewidth=200, precision=12, suppress=True)
    print("dual matrix")
    print(dual)


if __name__ == "__main__":
    main()
