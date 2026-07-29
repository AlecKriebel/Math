#!/usr/bin/env python3
"""Exact replay of the two-site flip-kernel parity reduction.

This verifier checks:

1. the symbolic Grassmann and determinant parity arithmetic;
2. the non-flip-invariant published d=4 exceptional witness;
3. a balanced, fully standard d=2 limitation projection with odd
   flip-kernel nullity and nonzero exceptional cubic residual.

No floating-point arithmetic or randomness is used.
"""

from __future__ import annotations

from functools import reduce
from itertools import product

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    return reduce(sp.kronecker_product, matrices, sp.Matrix([[1]]))


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def flip_matrix(dimension: int) -> sp.Matrix:
    matrix = sp.zeros(dimension**2)
    for a, b in product(range(dimension), repeat=2):
        matrix[b * dimension + a, a * dimension + b] = 1
    return matrix


def partial_trace(
    matrix: sp.Matrix, dimension: int, traced_leg: int
) -> sp.Matrix:
    result = sp.zeros(dimension)
    if traced_leg == 1:
        for b, d_index in product(range(dimension), repeat=2):
            result[b, d_index] = sum(
                matrix[a * dimension + b, a * dimension + d_index]
                for a in range(dimension)
            )
    elif traced_leg == 2:
        for a, c in product(range(dimension), repeat=2):
            result[a, c] = sum(
                matrix[a * dimension + b, c * dimension + b]
                for b in range(dimension)
            )
    else:
        raise ValueError("traced_leg must be 1 or 2")
    return result


def published_h() -> sp.Matrix:
    identity = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.diag(1, -1)
    j = sp.Matrix([[0, -1], [1, 0]])
    return (
        -tensor(z, identity, z, z) / sp.sqrt(6)
        - tensor(z, identity, j, j) / sp.sqrt(6)
        - tensor(j, identity, z, j) / sp.sqrt(6)
        + tensor(j, identity, j, z) / sp.sqrt(6)
        - tensor(x, identity, x, x) / sp.sqrt(3)
    )


def intersection_basis(*equations: sp.Matrix) -> sp.Matrix:
    stacked = equations[0]
    for equation in equations[1:]:
        stacked = stacked.col_join(equation)
    vectors = stacked.nullspace()
    if not vectors:
        return sp.zeros(stacked.cols, 0)
    return sp.Matrix.hstack(*vectors)


def symbolic_parity_arithmetic() -> None:
    s = sp.symbols("s", integer=True, positive=True)
    d = 2 * s
    rank_projection = d**2 / 2
    symmetric_dimension = d * (d + 1) / 2
    ambient_dimension = d**2

    # Grassmann index:
    # a-b = dim ran(P) + dim Sym^2(V) - dim(V tensor V) = s.
    index = sp.simplify(
        rank_projection + symmetric_dimension - ambient_dimension
    )
    assert index == s

    # det(H)=1 and det(F)=(-1)^s.  The difference between the flip
    # exponent d(d-1)/2 and s is even.
    flip_exponent = sp.expand(d * (d - 1) / 2)
    assert sp.simplify(flip_exponent - s) == 2 * s * (s - 1)
    assert sp.simplify(rank_projection) == 2 * s**2

    # If b is the second kernel summand, nullity=s+2b has parity s.
    b = sp.symbols("b", integer=True, nonnegative=True)
    nullity = s + 2 * b
    assert sp.simplify(nullity - s) == 2 * b


def published_d4_calibration() -> None:
    d = 4
    s = d // 2
    identity = sp.eye(d**2)
    h = published_h()
    projection = (identity - h) / 2
    flip = flip_matrix(d)
    k_matrix = h * flip

    assert h.T.conjugate() == h
    assert h**2 == identity
    assert sp.trace(h) == 0
    assert projection.rank() == d**2 // 2
    assert k_matrix.T.conjugate() * k_matrix == identity
    assert flip * k_matrix * flip == k_matrix.T.conjugate()

    # The calibration is genuinely non-flip-invariant.
    commutator = h * flip - flip * h
    assert commutator.rank() == 8
    assert sp.trace(commutator.T.conjugate() * commutator) == 32

    # Exact spectrum and determinant agreement.
    assert k_matrix**4 == identity
    variable = sp.symbols("x")
    expected = (
        (variable - 1) ** 4
        * (variable + 1) ** 4
        * (variable**2 + 1) ** 4
    )
    assert sp.expand(k_matrix.charpoly(variable).as_expr() - expected) == 0
    assert sp.det(k_matrix) == (-1) ** s == 1

    # Build both summands in the universal kernel decomposition.
    ran_p_sym = intersection_basis(h + identity, flip - identity)
    ker_p_alt = intersection_basis(h - identity, flip + identity)
    combined = ran_p_sym.row_join(ker_p_alt)

    assert ran_p_sym.rank() == 3
    assert ker_p_alt.rank() == 1
    assert combined.rank() == 4
    assert is_zero((k_matrix + identity) * combined)
    assert d**2 - (k_matrix + identity).rank() == 4
    assert ran_p_sym.rank() - ker_p_alt.rank() == s
    assert combined.rank() == s + 2 * ker_p_alt.rank()


def standard_d2_limitation() -> None:
    d = 2
    identity = sp.eye(d)
    identity_square = sp.eye(d**2)
    projection = sp.diag(1, 0, 0, 1)
    h = identity_square - 2 * projection
    flip = flip_matrix(d)
    k_matrix = h * flip

    assert projection.T == projection
    assert projection**2 == projection
    assert projection.rank() == d**2 // 2
    assert partial_trace(projection, d, 1) == identity
    assert partial_trace(projection, d, 2) == identity

    ran_p_sym = intersection_basis(h + identity_square, flip - identity_square)
    ker_p_alt = intersection_basis(h - identity_square, flip + identity_square)
    combined = ran_p_sym.row_join(ker_p_alt)
    assert (ran_p_sym.rank(), ker_p_alt.rank()) == (2, 1)
    assert combined.rank() == 3
    assert is_zero((k_matrix + identity_square) * combined)
    assert d**2 - (k_matrix + identity_square).rank() == 3
    assert sp.det(k_matrix) == -1

    # It is not an exceptional solution.
    p_12 = tensor(projection, identity)
    p_23 = tensor(identity, projection)
    residual = (
        p_12 * p_23 * p_12
        - p_23 * p_12 * p_23
        - sp.Rational(1, 3) * (p_12 - p_23)
    )
    assert sp.trace(residual.T * residual) == sp.Rational(4, 9)


def main() -> None:
    symbolic_parity_arithmetic()
    print("PASS symbolic Grassmann and determinant parity arithmetic")
    published_d4_calibration()
    print("PASS published d=4 non-flip-invariant calibration")
    standard_d2_limitation()
    print("PASS fully standard d=2 odd-nullity limitation model")
    print("All two-site flip parity-reduction checks passed exactly.")


if __name__ == "__main__":
    main()
