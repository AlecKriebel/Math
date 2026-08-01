#!/usr/bin/env python3
"""Exact rational coordinates for the holomorphic DTH support K.

The corrected five-replica lift is locally covariant on ``(C^3)^tensor 5``.
For an ordered triple of local S_5 shapes this module constructs, entirely
over QQ,

* the raw tensor-product Specht coordinate space;
* the pair-antisymmetric, pair-symmetric, first-Pluecker source projector;
* the combined Omega contraction;
* a column basis ``K`` of the physical constrained vector space; and
* the restriction-range basis ``E = G K``.

Here ``G`` is the Gram matrix of the nonorthogonal integral polytabloid
basis.  If ``A`` is any rational symmetric matrix, then

    h = E A E.T

is the raw highest-weight *restriction matrix* of a Hermitian operator
supported on K.  Conversely every supported restriction matrix has this
form.  This convention is the one consumed directly by the exact local
crossing bridge in ``agent_dth_local_crossing_exact.py``; no orthonormalizing
square roots occur.

SymPy is used only for exact rational matrix arithmetic.  There are no
floating-point rank decisions or external data files.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import permutations, product
import importlib.util
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
BRIDGE_PATH = HERE / "agent_dth_local_crossing_exact.py"
SPEC = importlib.util.spec_from_file_location("dth_exact_bridge", BRIDGE_PATH)
BRIDGE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BRIDGE)


HOL_MULTS = BRIDGE.HOL_MULTS
HOL_SHAPES = BRIDGE.HOL_SHAPES
EXPECTED_UNORDERED_K_DIMS = {
    tuple(HOL_SHAPES.index(shape) for shape in shapes): data[2]
    for shapes, data in BRIDGE.census.EXPECTED.items()
}


def sympy_matrix(rows):
    return sp.Matrix([
        [sp.Rational(value.numerator, value.denominator) for value in row]
        for row in rows
    ])


def transposition(first, second):
    out = list(range(5))
    out[first], out[second] = out[second], out[first]
    return tuple(out)


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


LOCAL_BASES = BRIDGE.holomorphic_highest_weight_bases()


@lru_cache(None)
def local_gram(shape_index):
    basis = LOCAL_BASES[shape_index]
    return sympy_matrix([
        [BRIDGE.dot(left, right) for right in basis]
        for left in basis
    ])


@lru_cache(None)
def local_representation(shape_index, permutation):
    """Coordinate matrix R with P_pi E = E R."""
    basis = LOCAL_BASES[shape_index]
    restriction = sympy_matrix(
        BRIDGE.restriction_block(
            BRIDGE.permutation_operator(permutation), basis
        )
    )
    return local_gram(shape_index).inv() * restriction


@lru_cache(None)
def local_omega(shape_index, first):
    """Raw epsilon contraction, retaining the other bivector pair."""
    assert first in (0, 2)
    basis = LOCAL_BASES[shape_index]
    retained = (2, 3) if first == 0 else (0, 1)
    out = [[sp.Integer(0) for _ in basis] for _ in range(9)]
    for column, vector in enumerate(basis):
        for word_index, value in vector.items():
            word = BRIDGE.WORDS[word_index]
            coefficient = BRIDGE.census.epsilon(
                word[4], word[first], word[first + 1]
            )
            if coefficient:
                row = 3 * word[retained[0]] + word[retained[1]]
                out[row][column] += coefficient * sp.Rational(
                    value.numerator, value.denominator
                )
    return sp.Matrix(out)


def kron3(matrices):
    return sp.kronecker_product(*matrices)


@lru_cache(None)
def hol_k_coordinates(shapes):
    """Return exact ``(K, G, E)`` for one ordered local-shape triple.

    ``K`` contains physical constrained vectors in raw tensor-product Specht
    coordinates, ``G`` is the raw Gram matrix, and ``E=G*K`` contains their
    inner products against the raw basis.  Thus the supported operator chart
    is exactly ``h=E*A*E.T``.
    """
    shapes = tuple(shapes)
    assert len(shapes) == 3 and all(0 <= shape < 5 for shape in shapes)
    dimensions = tuple(HOL_MULTS[shape] for shape in shapes)
    size = dimensions[0] * dimensions[1] * dimensions[2]
    identity = sp.eye(size)

    def global_representation(permutation):
        return kron3(tuple(
            local_representation(shape, permutation) for shape in shapes
        ))

    p12 = (identity - global_representation(transposition(0, 1))) / 2
    p34 = (identity - global_representation(transposition(2, 3))) / 2
    pair_exchange = (2, 3, 0, 1, 4)
    ppair = (identity + global_representation(pair_exchange)) / 2
    a4 = sp.zeros(size)
    for permutation in permutations(range(4)):
        lifted = tuple(permutation) + (4,)
        a4 += (sp.Rational(permutation_sign(permutation), 24)
               * global_representation(lifted))
    source = p12 * p34 * ppair * (identity - a4)

    # Pivot columns are an exact basis of im(source).
    _, pivots = source.rref()
    source_basis = source[:, list(pivots)]

    omega = (
        kron3(tuple(local_omega(shape, 0) for shape in shapes))
        + kron3(tuple(local_omega(shape, 2) for shape in shapes))
    )
    constrained = omega * source_basis
    kernel = constrained.nullspace()
    if kernel:
        kernel_matrix = sp.Matrix.hstack(*kernel)
        physical_basis = source_basis * kernel_matrix
    else:
        physical_basis = sp.zeros(size, 0)

    gram = kron3(tuple(local_gram(shape) for shape in shapes))
    restriction_range = gram * physical_basis
    assert physical_basis.rank() == physical_basis.cols
    assert restriction_range.rank() == restriction_range.cols
    return physical_basis, gram, restriction_range


def expected_k_dimension(shapes):
    return EXPECTED_UNORDERED_K_DIMS[tuple(sorted(shapes))]


def main():
    vector_dimension = 0
    hermitian_dimension = 0
    maximum_denominator = 1
    for shapes in product(range(5), repeat=3):
        physical, gram, restriction = hol_k_coordinates(shapes)
        expected = expected_k_dimension(shapes)
        assert physical.cols == restriction.cols == expected
        assert gram.rows == gram.cols == physical.rows
        vector_dimension += expected
        hermitian_dimension += expected * (expected + 1) // 2
        for value in physical:
            maximum_denominator = max(maximum_denominator, int(sp.denom(value)))

    assert vector_dimension == 768
    assert hermitian_dimension == 4139
    print("exact holomorphic DTH K-coordinate certificate passed")
    print("ordered block vector dimension:", vector_dimension)
    print("real symmetric chart dimension:", hermitian_dimension)
    print("maximum K-coordinate denominator:", maximum_denominator)


if __name__ == "__main__":
    main()
