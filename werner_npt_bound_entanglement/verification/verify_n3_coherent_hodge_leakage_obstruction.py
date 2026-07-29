#!/usr/bin/env python3
"""Exact replay of the coherent-Hodge leakage obstruction.

The checker uses SymPy rational arithmetic.  It verifies:

* orthonormality and full one-site support of the two codewords;
* all 32 mixed-block vanishings (four logical matrix units times
  eight local-transpose parity sectors);
* the complete core/norm tables and the positive normal-block masses;
* the even/odd individual-label tight-frame constants in a canonical
  N-dimensional model, specialized to N=27.
"""

from __future__ import annotations

import itertools

import sympy as sp


N = 27


def index(word: tuple[int, int, int]) -> int:
    return 9 * word[0] + 3 * word[1] + word[2]


def dagger(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.conjugate().T


def hs2(matrix: sp.Matrix) -> sp.Expr:
    return sp.simplify(
        sum(
            sp.conjugate(matrix[i, j]) * matrix[i, j]
            for i in range(matrix.rows)
            for j in range(matrix.cols)
        )
    )


def partial_transpose(matrix: sp.Matrix, site: int) -> sp.Matrix:
    out = sp.zeros(N)
    for row_word in itertools.product(range(3), repeat=3):
        for column_word in itertools.product(range(3), repeat=3):
            new_row = list(row_word)
            new_column = list(column_word)
            new_row[site], new_column[site] = (
                new_column[site],
                new_row[site],
            )
            out[index(row_word), index(column_word)] = matrix[
                index(tuple(new_row)), index(tuple(new_column))
            ]
    return out


def parity_projection(matrix: sp.Matrix, subset: tuple[int, ...]) -> sp.Matrix:
    out = matrix
    chosen = set(subset)
    for site in range(3):
        sign = -1 if site in chosen else 1
        out = (out + sign * partial_transpose(out, site)) / 2
    return out.applyfunc(sp.simplify)


u0 = sp.zeros(N, 1)
u1 = sp.zeros(N, 1)
for j in range(3):
    u0[index((j, j, j))] = 1 / sp.sqrt(3)
for word in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
    u1[index(word)] = 1 / sp.sqrt(3)

U = u0.row_join(u1)
assert dagger(U) * U == sp.eye(2)
P = U * dagger(U)
P_perp = sp.eye(N) - P


def one_site_reduction(matrix: sp.Matrix, site: int) -> sp.Matrix:
    out = sp.zeros(3)
    other = [position for position in range(3) if position != site]
    for row, column in itertools.product(range(3), repeat=2):
        value = 0
        for environment in itertools.product(range(3), repeat=2):
            row_word = [0, 0, 0]
            column_word = [0, 0, 0]
            row_word[site] = row
            column_word[site] = column
            for position, physical_site in enumerate(other):
                row_word[physical_site] = environment[position]
                column_word[physical_site] = environment[position]
            value += matrix[
                index(tuple(row_word)), index(tuple(column_word))
            ]
        out[row, column] = sp.simplify(value)
    return out


for site in range(3):
    assert one_site_reduction(P, site) == 2 * sp.eye(3) / 3

logical_units = {}
for a, b in itertools.product(range(2), repeat=2):
    column_a = U[:, a]
    column_b = U[:, b]
    logical_units[(a, b)] = column_a * dagger(column_b)

X = sp.Matrix([[0, 1], [1, 0]])
J = sp.Matrix([[0, 1], [-1, 0]])


def expected_core_and_norm(
    a: int, b: int, subset: tuple[int, ...]
) -> tuple[sp.Matrix, sp.Rational]:
    cardinality = len(subset)
    zero = sp.zeros(2)
    if a == b:
        unit = sp.zeros(2)
        unit[a, a] = 1
        if cardinality == 0:
            return unit / 2, sp.Rational(1, 2)
        if cardinality == 2:
            return unit / 6, sp.Rational(1, 6)
        return zero, sp.Rational(0)

    if cardinality == 0:
        return X / 4, sp.Rational(1, 4)
    if cardinality == 1:
        sign = 1 if (a, b) == (0, 1) else -1
        return sign * J / 6, sp.Rational(1, 6)
    if cardinality == 2:
        return X / 12, sp.Rational(1, 12)
    return zero, sp.Rational(0)


normal_masses = {}
for a, b in itertools.product(range(2), repeat=2):
    matrix = logical_units[(a, b)]
    for cardinality in range(4):
        for subset in itertools.combinations(range(3), cardinality):
            component = parity_projection(matrix, subset)
            core = (dagger(U) * component * U).applyfunc(sp.simplify)
            expected_core, expected_norm = expected_core_and_norm(
                a, b, subset
            )
            assert core == expected_core
            assert hs2(component) == expected_norm

            mixed_left = (P_perp * component * U).applyfunc(sp.simplify)
            mixed_right = (dagger(U) * component * P_perp).applyfunc(
                sp.simplify
            )
            assert mixed_left == sp.zeros(N, 2)
            assert mixed_right == sp.zeros(2, N)

            normal = (P_perp * component * P_perp).applyfunc(sp.simplify)
            mass = hs2(normal)
            assert sp.simplify(
                mass - (expected_norm - hs2(expected_core))
            ) == 0
            normal_masses[(a, b, cardinality)] = mass

for a in range(2):
    assert normal_masses[(a, a, 0)] == sp.Rational(1, 4)
    assert normal_masses[(a, a, 2)] == sp.Rational(5, 36)
for a, b in ((0, 1), (1, 0)):
    assert normal_masses[(a, b, 0)] == sp.Rational(1, 8)
    assert normal_masses[(a, b, 1)] == sp.Rational(1, 9)
    assert normal_masses[(a, b, 2)] == sp.Rational(5, 72)

# Canonical-basis replay of Theorem 3.1.  By unitary congruence one
# may take U=(e_0,e_1).  The following sums retain exact sqrt(2)
# normalizations of the symmetric/skew matrix bases.
U_canonical = sp.zeros(N, 2)
U_canonical[0, 0] = 1
U_canonical[1, 1] = 1
P_canonical = U_canonical * dagger(U_canonical)
P_canonical_perp = sp.eye(N) - P_canonical

skew_basis = []
symmetric_basis = []
for i in range(N):
    diagonal = sp.zeros(N)
    diagonal[i, i] = 1
    symmetric_basis.append(diagonal)
for i in range(N):
    for j in range(i + 1, N):
        symmetric = sp.zeros(N)
        symmetric[i, j] = symmetric[j, i] = 1 / sp.sqrt(2)
        symmetric_basis.append(symmetric)

        skew = sp.zeros(N)
        skew[i, j] = 1 / sp.sqrt(2)
        skew[j, i] = -1 / sp.sqrt(2)
        skew_basis.append(skew)


def leakage_gram(basis: list[sp.Matrix]) -> sp.Matrix:
    out = sp.zeros(2)
    for matrix in basis:
        leakage = P_canonical_perp * matrix * U_canonical
        out += dagger(leakage) * leakage
    return out.applyfunc(sp.simplify)


target = sp.Rational(N - 2, 2) * sp.eye(2)
assert leakage_gram(skew_basis) == target
assert leakage_gram(symmetric_basis) == target

# The core Parseval constants used in the proof.
skew_core = sp.zeros(2)
for matrix in skew_basis:
    compressed = dagger(U_canonical) * matrix * U_canonical
    skew_core += dagger(compressed) * compressed
assert skew_core == sp.eye(2) / 2

symmetric_core = sp.zeros(2)
for matrix in symmetric_basis:
    compressed = dagger(U_canonical) * matrix * U_canonical
    symmetric_core += dagger(compressed) * compressed
assert symmetric_core == 3 * sp.eye(2) / 2

# Independent one-qutrit replay of the Fierz identity used in (23).
# Tensoring this identity three times gives precisely the weights
# 2^(-3) 3^|R| and the parity sign (-1)^|R|.
local_symmetric = []
local_skew = []
for i in range(3):
    diagonal = sp.zeros(3)
    diagonal[i, i] = 1
    local_symmetric.append(diagonal)
for i in range(3):
    for j in range(i + 1, 3):
        symmetric = sp.zeros(3)
        symmetric[i, j] = symmetric[j, i] = 1 / sp.sqrt(2)
        local_symmetric.append(symmetric)

        skew = sp.zeros(3)
        skew[i, j] = 1 / sp.sqrt(2)
        skew[j, i] = -1 / sp.sqrt(2)
        local_skew.append(skew)

test_matrix = sp.Matrix(
    [
        [1 + sp.I, 2, -sp.I],
        [3 - sp.I, -2, 4 + sp.I],
        [5, 1 - 2 * sp.I, 3],
    ]
)
fierz = sp.zeros(3)
for matrix in local_symmetric:
    fierz += matrix * test_matrix.T * dagger(matrix) / 2
for matrix in local_skew:
    fierz -= 3 * matrix * test_matrix.T * dagger(matrix) / 2
endpoint = test_matrix - sp.trace(test_matrix) * sp.eye(3) / 2
assert fierz.applyfunc(sp.simplify) == endpoint.applyfunc(sp.simplify)

weighted_local_frame = sp.zeros(3)
for matrix in local_symmetric:
    weighted_local_frame += dagger(matrix) * matrix / 2
for matrix in local_skew:
    weighted_local_frame += 3 * dagger(matrix) * matrix / 2
assert weighted_local_frame == 5 * sp.eye(3) / 2
assert sp.Rational(5, 2) ** 3 == sp.Rational(125, 8)
assert (
    sp.Rational(125, 8) - sp.Rational(27, 4)
    == sp.Rational(71, 8)
)
assert (
    sp.Rational(125, 8) - sp.Rational(1, 4)
    == sp.Rational(123, 8)
)

# Exact one-site block-colligation replay, including the parity sign
# in the right mixed and normal blocks.  Tensoring the same algebra
# gives equation (24) of the note.
left_frame = sp.Matrix([[1, 0], [0, 1], [0, 0]])
right_frame = sp.Matrix([[0, 0], [1, 0], [0, 1]])
left_projection = left_frame * dagger(left_frame)
right_projection = right_frame * dagger(right_frame)
singular = sp.diag(2, sp.Rational(1, 2))
coefficient = left_frame * singular * dagger(right_frame)
local_endpoint = (
    coefficient - sp.trace(coefficient) * sp.eye(3) / 2
)

core_sum = sp.zeros(2)
left_sum = sp.zeros(3, 2)
right_sum = sp.zeros(2, 3)
normal_sum = sp.zeros(3)
for basis, weight, parity in (
    (local_symmetric, sp.Rational(1, 2), 1),
    (local_skew, sp.Rational(3, 2), -1),
):
    for matrix in basis:
        core = dagger(left_frame) * matrix * right_frame.conjugate()
        left_leakage = (
            (sp.eye(3) - left_projection)
            * matrix
            * right_frame.conjugate()
        )
        right_leakage = (
            (sp.eye(3) - right_projection)
            * matrix
            * left_frame.conjugate()
        )
        core_sum += weight * core * singular * core.conjugate()
        left_sum += (
            weight
            * left_leakage
            * singular
            * core.conjugate()
        )
        right_sum += (
            parity
            * weight
            * core
            * singular
            * dagger(right_leakage)
        )
        normal_sum += (
            parity
            * weight
            * left_leakage
            * singular
            * dagger(right_leakage)
        )

assert core_sum == dagger(left_frame) * local_endpoint * right_frame
assert left_sum == (
    (sp.eye(3) - left_projection) * local_endpoint * right_frame
)
assert right_sum == (
    dagger(left_frame)
    * local_endpoint
    * (sp.eye(3) - right_projection)
)
assert normal_sum == (
    (sp.eye(3) - left_projection)
    * local_endpoint
    * (sp.eye(3) - right_projection)
)

print(
    "verified full-support simultaneous parity-leakage zero, "
    "positive normal blocks, even/odd 25/2 tight frames, and the "
    "signed/weighted local Fierz block identities"
)
