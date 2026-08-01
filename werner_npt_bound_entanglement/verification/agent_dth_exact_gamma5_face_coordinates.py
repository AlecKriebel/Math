#!/usr/bin/env python3
"""Exact rational charts for the reduced rank-751 Gamma5 DTH face.

After partial transpose of the final ``z`` replica the local module is

    V^tensor4 tensor conjugate(V).

The first four replicas still obey the two pair antisymmetries, pair exchange,
and first Pluecker equation.  On that exact 772-dimensional global support,
the remaining coupled DTH equation is

    D5 = d0^tensor3 + d2^tensor3,

where ``d0`` contracts the contravariant fifth slot with the second slot and
retains slots (1,3,4), while ``d2`` contracts it with the fourth slot and
retains (3,1,2) (one-based labels).  This module constructs the exact kernel
of D5 in every local Schur block and returns its rational restriction chart.

The construction uses only rational arithmetic.  To avoid forming a
19683-by-n contraction matrix, it computes D5^T D5 as four tensor products
of small local Gram matrices; over QQ its kernel is exactly ker(D5).
"""

from __future__ import annotations

from functools import lru_cache
from itertools import permutations, product
import importlib.util
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


LAST = import_file(
    "dth_gamma5_face_bridge", HERE / "agent_dth_last_crossing_exact.py"
)
BRIDGE = LAST.bridge
LAST_MULTS = LAST.LAST_MULTS
LOCAL_BASES = LAST.last_highest_weight_bases()


def sympy_matrix(rows):
    return sp.Matrix([
        [sp.Rational(value.numerator, value.denominator) for value in row]
        for row in rows
    ])


def transposition(first, second):
    output = list(range(5))
    output[first], output[second] = output[second], output[first]
    return tuple(output)


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


@lru_cache(None)
def local_gram(shape_index):
    basis = LOCAL_BASES[shape_index]
    return sympy_matrix([
        [BRIDGE.dot(left, right) for right in basis]
        for left in basis
    ])


@lru_cache(None)
def local_representation(shape_index, permutation):
    """Coordinate action of a permutation of the first four covariant slots."""
    assert permutation[4] == 4
    basis = LOCAL_BASES[shape_index]
    restriction = sympy_matrix(
        BRIDGE.restriction_block(
            BRIDGE.permutation_operator(permutation), basis
        )
    )
    return local_gram(shape_index).inv() * restriction


@lru_cache(None)
def local_delta(shape_index, which):
    """Return d0 or d2 from a target multiplicity space to three qutrits."""
    assert which in (0, 2)
    basis = LOCAL_BASES[shape_index]
    output = sp.zeros(27, len(basis))
    for column, vector in enumerate(basis):
        for word_index, value in vector.items():
            word = BRIDGE.WORDS[word_index]
            if which == 0:
                if word[4] != word[1]:
                    continue
                retained = (word[0], word[2], word[3])
            else:
                if word[4] != word[3]:
                    continue
                # This cyclic order identifies the two contraction codomains.
                retained = (word[2], word[0], word[1])
            row = 9 * retained[0] + 3 * retained[1] + retained[2]
            output[row, column] += sp.Rational(
                value.numerator, value.denominator
            )
    return output


def kron3(matrices):
    return sp.kronecker_product(*matrices)


@lru_cache(None)
def pair_pluecker_coordinates(shapes):
    """Exact raw-coordinate basis of the Gamma5 pair/Pluecker support."""
    shapes = tuple(shapes)
    dimensions = tuple(LAST_MULTS[shape] for shape in shapes)
    size = dimensions[0] * dimensions[1] * dimensions[2]
    identity = sp.eye(size)

    def global_representation(permutation):
        return kron3(tuple(
            local_representation(shape, permutation) for shape in shapes
        ))

    p12 = (identity - global_representation(transposition(0, 1))) / 2
    p34 = (identity - global_representation(transposition(2, 3))) / 2
    ppair = (identity + global_representation((2, 3, 0, 1, 4))) / 2
    a4 = sp.zeros(size)
    for permutation in permutations(range(4)):
        lifted = tuple(permutation) + (4,)
        a4 += (sp.Rational(permutation_sign(permutation), 24)
               * global_representation(lifted))
    projector = p12 * p34 * ppair * (identity - a4)
    # The joint antisymmetrizer p12*p34 commutes with pair exchange, while
    # a4 is central in the first-four-replica group algebra.  Thus the three
    # factors p12*p34, ppair, and (I-a4) are commuting idempotents, so their
    # product is an exact idempotent and its rank is its trace.  A modularly
    # independent set of that many columns therefore spans its rational
    # image.  This avoids a prohibitively expensive rational RREF in the
    # 512 block.
    exact_trace = sp.trace(projector)
    assert sp.denom(exact_trace) == 1
    rank = int(exact_trace)
    pivots = independent_column_indices(projector, rank)
    return projector[:, list(pivots)]


@lru_cache(None)
def delta_gram(shapes):
    """Small exact matrix D5^T D5 on the raw tensor multiplicity block."""
    shapes = tuple(shapes)
    d0 = tuple(local_delta(shape, 0) for shape in shapes)
    d2 = tuple(local_delta(shape, 2) for shape in shapes)
    return (
        kron3(tuple(left.T * right for left, right in zip(d0, d0)))
        + kron3(tuple(left.T * right for left, right in zip(d0, d2)))
        + kron3(tuple(left.T * right for left, right in zip(d2, d0)))
        + kron3(tuple(left.T * right for left, right in zip(d2, d2)))
    )


@lru_cache(None)
def gamma5_face_coordinates(shapes):
    """Return exact ``(K5,G5,E5)`` for one ordered Gamma5 block.

    ``K5`` is a raw-coordinate basis of the constrained vector space,
    ``G5`` is the nonorthogonal highest-weight Gram matrix, and ``E5=G5*K5``
    is the restriction-range chart.  Every supported rational symmetric
    block is uniquely ``E5*A*E5.T``.
    """
    shapes = tuple(shapes)
    source = pair_pluecker_coordinates(shapes)
    constrained_gram = source.T * delta_gram(shapes) * source
    kernel = constrained_gram.nullspace()
    if kernel:
        physical = source * sp.Matrix.hstack(*kernel)
    else:
        physical = sp.zeros(source.rows, 0)
    gram = kron3(tuple(local_gram(shape) for shape in shapes))
    restriction = gram * physical
    assert physical.rank() == physical.cols
    assert restriction.rank() == restriction.cols
    # D5^T D5 is positive semidefinite over RR, hence equality of kernels.
    assert delta_gram(shapes) * physical == sp.zeros(physical.rows,
                                                     physical.cols)
    return physical, gram, restriction


def independent_row_indices(matrix, expected_rank, prime=1_000_003):
    """Select rationally independent chart rows via a prime-field replay."""
    rows, columns = matrix.rows, matrix.cols
    if not columns:
        return tuple()
    work = [
        [int(sp.numer(matrix[row, column]))
         * pow(int(sp.denom(matrix[row, column])), -1, prime) % prime
         for row in range(rows)]
        for column in range(columns)
    ]
    pivot_row = 0
    pivots = []
    for column in range(rows):
        selected = next(
            (row for row in range(pivot_row, columns) if work[row][column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [value * inverse % prime
                           for value in work[pivot_row]]
        for row in range(columns):
            if row == pivot_row:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    (x - coefficient * y) % prime
                    for x, y in zip(work[row], work[pivot_row])
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == expected_rank:
            break
    assert len(pivots) == expected_rank
    return tuple(pivots)


def independent_column_indices(matrix, expected_rank, prime=1_000_003):
    """Select independent columns, with exact QQ validity certified mod p."""
    rows, columns = matrix.rows, matrix.cols
    echelon = {}
    selected = []
    for column in range(columns):
        vector = {
            row: (int(sp.numer(matrix[row, column]))
                  * pow(int(sp.denom(matrix[row, column])), -1, prime)
                  % prime)
            for row in range(rows) if matrix[row, column]
        }
        while vector:
            pivot = min(vector)
            if pivot not in echelon:
                inverse = pow(vector[pivot], -1, prime)
                vector = {
                    row: value * inverse % prime
                    for row, value in vector.items()
                    if value * inverse % prime
                }
                echelon[pivot] = vector
                selected.append(column)
                break
            coefficient = vector[pivot]
            old = echelon[pivot]
            for row, value in old.items():
                updated = (vector.get(row, 0) - coefficient * value) % prime
                if updated:
                    vector[row] = updated
                elif row in vector:
                    del vector[row]
        if len(selected) == expected_rank:
            break
    assert len(selected) == expected_rank
    return tuple(selected)


@lru_cache(None)
def gamma5_face_chart(shapes):
    """Return an exact restriction-range basis and nonsingular pivot rows."""
    _, _, restriction = gamma5_face_coordinates(tuple(shapes))
    rank = restriction.cols
    if not rank:
        return restriction, tuple()
    # Integral row-LLL improves later exact and floating chart conditioning.
    denominators = [int(sp.denom(value)) for value in restriction]
    common = sp.ilcm(*denominators) if denominators else 1
    integral = (restriction * common).applyfunc(int)
    reduced = integral.T.lll().T
    rows = independent_row_indices(reduced, rank)
    return reduced, rows


def recover_coordinate_matrix(shapes, restriction_matrix):
    basis, rows = gamma5_face_chart(tuple(shapes))
    rank = basis.cols
    if not rank:
        assert restriction_matrix == sp.zeros(restriction_matrix.rows)
        return sp.zeros(0)
    ej = basis[list(rows), :]
    coordinate = ej.inv() * restriction_matrix.extract(rows, rows) * ej.inv().T
    assert restriction_matrix == basis * coordinate * basis.T
    assert coordinate == coordinate.T
    return coordinate


def main():
    support_total = face_total = support_active = face_active = 0
    full_support_total = full_face_total = full_defect_total = 0
    exceptional = []
    maximum_face = 0
    for shapes in product(range(6), repeat=3):
        source = pair_pluecker_coordinates(shapes)
        physical, _, restriction = gamma5_face_coordinates(shapes)
        support_total += source.cols
        face_total += physical.cols
        carrier = 1
        for shape in shapes:
            carrier *= LAST.LAST_IRREP_DIMS[shape]
        full_support_total += carrier * source.cols
        full_face_total += carrier * physical.cols
        full_defect_total += carrier * (source.cols - physical.cols)
        support_active += int(source.cols > 0)
        face_active += int(physical.cols > 0)
        maximum_face = max(maximum_face, physical.cols)
        defect = source.cols - physical.cols
        if defect:
            exceptional.append((shapes, source.cols, physical.cols, defect))
        assert restriction.cols == physical.cols

    assert support_total == 772
    assert face_total == 751
    assert full_support_total == 1_194_102
    assert full_defect_total == 6_552
    assert full_face_total == 1_187_550
    assert len(exceptional) == 19
    assert sum(item[3] for item in exceptional) == 21
    print("exact Gamma5 DTH face-coordinate certificate passed")
    print("reduced pair/Pluecker rank sum / active blocks:",
          support_total, support_active)
    print("reduced D5-kernel rank sum / active blocks:",
          face_total, face_active)
    print("full support / D5 rank / face dimensions:",
          full_support_total, full_defect_total, full_face_total)
    print("maximum face chart rank:", maximum_face)
    print("rank-21 exceptional blocks:")
    for shapes, support, face, defect in exceptional:
        print(" ", "/".join(LAST.LAST_NAMES[s] for s in shapes),
              "support", support, "face", face, "defect", defect)


if __name__ == "__main__":
    main()
