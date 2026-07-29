#!/usr/bin/env python3
"""Exact replay for the overlap-space Kramers parity audit.

The human proof classifies antiunitary symmetries of the canonical generic
two-projection block.  This verifier checks the finite algebra identities,
the exact odd-multiplicity d=6 abstract model, and the cyclic-overlap
defects of the published d=4 witness.
"""

from __future__ import annotations

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def is_zero(matrix: sp.Matrix) -> bool:
    # The witness lives in a small algebraic number field.  DomainMatrix
    # zero tests avoid thousands of separate general-purpose simplify calls.
    return bool(matrix.to_DM(extension=True).is_zero_matrix)


def hs_norm_squared(matrix: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.trace(matrix.conjugate().T * matrix))


def generic_block_audit() -> None:
    c = sp.Rational(1, 3)
    a = sp.sqrt(c * (1 - c))
    p = sp.Matrix([[1, 0], [0, 0]])
    q = sp.Matrix([[c, a], [a, 1 - c]])
    identity = sp.eye(2)

    assert p * p == p
    assert q * q == q
    assert is_zero(p * q * p - q * p * q - c * (p - q))

    complex_structure = (p * q - q * p) / a
    assert complex_structure.conjugate().T == -complex_structure
    assert complex_structure**2 == -identity
    assert p * complex_structure * p == sp.zeros(2)
    assert (
        complex_structure * p * complex_structure.conjugate().T
        == identity - p
    )

    swap = (p + q - identity) / sp.sqrt(c)
    assert swap.conjugate().T * swap == identity
    assert swap**2 == identity
    assert swap * p * swap == q
    assert swap * q * swap == p

    # Exact d=6 abstract three-strand multiplicities.  The displayed
    # 2-by-2 block plus these direct-sum counts is a complete sparse
    # certificate; constructing a dense 216-by-216 matrix adds no logic.
    s = 3
    common_one = s**3
    common_zero = s**3
    generic = 3 * s**3
    total = common_one + common_zero + 2 * generic
    rank_p = common_one + generic
    overlap_trace = common_one + c * generic
    assert total == 216
    assert rank_p == 108
    assert overlap_trace == 54
    assert generic == 81
    assert generic % 2 == 1

    # If u conjugate(u)=-I_k, determinants require (-1)^k=1.
    # The odd k=81 model therefore cannot carry the proposed commuting
    # Kramers antiunitary.
    assert (-1) ** generic == -1


def published_h4() -> sp.Matrix:
    identity_2 = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.diag(1, -1)
    j = sp.Matrix([[0, -1], [1, 0]])
    return (
        -tensor(z, identity_2, z, z) / sp.sqrt(6)
        - tensor(z, identity_2, j, j) / sp.sqrt(6)
        - tensor(j, identity_2, z, j) / sp.sqrt(6)
        + tensor(j, identity_2, j, z) / sp.sqrt(6)
        - tensor(x, identity_2, x, x) / sp.sqrt(3)
    )


def cyclic_rotation(d: int) -> sp.Matrix:
    """L|a,b,c> = |b,c,a>."""
    rotation = sp.zeros(d**3)
    for first in range(d):
        for middle in range(d):
            for last in range(d):
                source = first * d**2 + middle * d + last
                target = middle * d**2 + last * d + first
                rotation[target, source] = 1
    return rotation


def outer_reversal(d: int) -> sp.Matrix:
    reversal = sp.zeros(d**3)
    for first in range(d):
        for middle in range(d):
            for last in range(d):
                source = first * d**2 + middle * d + last
                target = last * d**2 + middle * d + first
                reversal[target, source] = 1
    return reversal


def local_flip(d: int) -> sp.Matrix:
    flip = sp.zeros(d**2)
    for left in range(d):
        for right in range(d):
            flip[right * d + left, left * d + right] = 1
    return flip


def published_witness_audit() -> None:
    d = 4
    c = sp.Rational(1, 3)
    h = published_h4()
    projection = (sp.eye(d**2) - h) / 2
    p = tensor(projection, sp.eye(d))
    q = tensor(sp.eye(d), projection)
    rotation = cyclic_rotation(d)
    r = rotation * p * rotation.T

    assert is_zero(projection**2 - projection)
    assert is_zero(projection.conjugate() - projection)
    assert is_zero(rotation.T * p * rotation - q)

    def common_one(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
        return (
            (left * right * left - c * left) / (1 - c)
        ).applyfunc(sp.simplify)

    e_q = common_one(p, q)
    e_r = common_one(p, r)
    k_q = (p - e_q).applyfunc(sp.simplify)
    k_r = (p - e_r).applyfunc(sp.simplify)

    assert sp.simplify(sp.trace(e_q)) == 8
    assert sp.simplify(sp.trace(e_r)) == 8
    assert sp.simplify(sp.trace(k_q)) == 24
    assert sp.simplify(sp.trace(k_r)) == 24
    assert sp.simplify(sp.trace(k_q * k_r)) == 18
    assert hs_norm_squared(k_q - k_r) == 12

    # W=p L p on ran(p), extended by zero to the full space.
    overlap = p * rotation * p
    left_square = (overlap * overlap.T).applyfunc(sp.simplify)
    right_square = (overlap.T * overlap).applyfunc(sp.simplify)
    assert is_zero(left_square - (c * p + (1 - c) * e_r))
    assert is_zero(right_square - (c * p + (1 - c) * e_q))
    assert hs_norm_squared(left_square - right_square) == sp.Rational(16, 3)

    # Adjoint/flip closure and bare outer reversal both fail exactly.
    flip = local_flip(d)
    opposite = flip * projection * flip
    assert hs_norm_squared(projection - opposite) == 8

    reversal = outer_reversal(d)
    reflected_k = reversal * k_q * reversal
    assert sp.simplify(sp.trace(k_q * reflected_k)) == 9
    assert hs_norm_squared(k_q - reflected_k) == 30


def main() -> None:
    generic_block_audit()
    print("PASS generic block complex structure and antiunitary parity guard")
    print("PASS exact odd k=81 balanced abstract d=6 overlap model")
    published_witness_audit()
    print("PASS exact d=4 cyclic-overlap nonnormality and singular-space defect")
    print("PASS exact d=4 conjugation, adjoint, flip, and reversal audit")
    print("All overlap-space Kramers parity audit checks passed exactly.")


if __name__ == "__main__":
    main()
