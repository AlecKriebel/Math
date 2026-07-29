#!/usr/bin/env python3
"""Exact checks for the identity-amplification codimension-two no-go.

The human proof is in
notes/no_rank_six_subspace_of_d8_amplification.md.  This script verifies:

1. the three-term operator-Schmidt expansion of the exact amplified H;
2. the Bell-basis low-rank pencil and its six real rank-at-most-two lines;
3. generation of the full M_4 algebra on the two active qubits;
4. an exact rank-four invariant-subspace calibration at m=2.

The verifier realizes m=2 explicitly.  The all-m extension in the human
proof uses only rank(B_tilde tensor I_m)=m rank(B_tilde), together with
the verified fact that every nonzero pencil element has rank at least two.
"""

from __future__ import annotations

import itertools

import sympy as sp


I = sp.I
SQRT2 = sp.sqrt(2)
ID2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -I], [I, 0]])
Z = sp.diag(1, -1)
J = -I * Y


def kron(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.ones(1, 1)
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def published_h4() -> sp.Matrix:
    return (
        -kron(Z, ID2, Z, Z) / sp.sqrt(6)
        - kron(Z, ID2, J, J) / sp.sqrt(6)
        - kron(J, ID2, Z, J) / sp.sqrt(6)
        + kron(J, ID2, J, Z) / sp.sqrt(6)
        - kron(X, ID2, X, X) / sp.sqrt(3)
    )


def reorder_amplification(h4: sp.Matrix) -> sp.Matrix:
    """Reorder (site4,site4,spectator2,spectator2) into two 8-sites."""

    h8 = sp.zeros(64)
    for a1, b1, a2, b2, c1, c2 in itertools.product(range(2), repeat=6):
        row = ((2 * a1 + b1) * 2 + c1) * 8 + ((2 * a2 + b2) * 2 + c2)
        for ap1, bp1, ap2, bp2 in itertools.product(range(2), repeat=4):
            column = (
                ((2 * ap1 + bp1) * 2 + c1) * 8
                + ((2 * ap2 + bp2) * 2 + c2)
            )
            old_row = (2 * a1 + b1) * 4 + (2 * a2 + b2)
            old_column = (2 * ap1 + bp1) * 4 + (2 * ap2 + bp2)
            h8[row, column] = h4[old_row, old_column]
    return h8


def coefficients() -> tuple[list[sp.Matrix], list[sp.Matrix]]:
    active_identity = kron(ID2, ID2)
    a_ops = [
        kron(X, ID2, ID2),
        kron(Y, ID2, ID2),
        kron(Z, ID2, ID2),
    ]
    b_ops = [
        -kron(X, X, ID2) / sp.sqrt(3),
        kron(Z, Y, ID2) / sp.sqrt(6)
        - kron(Y, Z, ID2) / sp.sqrt(6),
        kron(Y, Y, ID2) / sp.sqrt(6)
        - kron(Z, Z, ID2) / sp.sqrt(6),
    ]
    assert active_identity.shape == (4, 4)
    return a_ops, b_ops


def check_schmidt_expansion() -> tuple[sp.Matrix, list[sp.Matrix], list[sp.Matrix]]:
    h4 = published_h4()
    h8 = reorder_amplification(h4)
    a_ops, b_ops = coefficients()
    reconstructed = sum(
        (sp.kronecker_product(a, b) for a, b in zip(a_ops, b_ops)),
        sp.zeros(64),
    )
    assert is_zero(h8 - reconstructed)
    assert is_zero(h8.H - h8)
    assert is_zero(h8 * h8 - sp.eye(64))
    return h8, a_ops, b_ops


def bell_basis() -> sp.Matrix:
    return sp.Matrix.hstack(
        sp.Matrix([1, 0, 0, 1]) / SQRT2,
        sp.Matrix([0, 1, 1, 0]) / SQRT2,
        sp.Matrix([1, 0, 0, -1]) / SQRT2,
        sp.Matrix([0, 1, -1, 0]) / SQRT2,
    )


def check_low_rank_pencil() -> tuple[sp.Expr, sp.Expr, list[tuple[sp.Expr, ...]]]:
    bx = -kron(X, X) / sp.sqrt(3)
    by = (kron(Z, Y) - kron(Y, Z)) / sp.sqrt(6)
    bz = (kron(Y, Y) - kron(Z, Z)) / sp.sqrt(6)
    x, y, z = sp.symbols("x y z", real=True)
    unitary = bell_basis()
    transformed = sp.simplify(
        unitary.H * (x * bz + y * by + z * bx) * unitary
    )
    expected = sp.Matrix(
        [
            [-z / sp.sqrt(3) - sp.sqrt(sp.Rational(2, 3)) * x, 0, 0, 0],
            [0, -z / sp.sqrt(3) + sp.sqrt(sp.Rational(2, 3)) * x, 0, 0],
            [0, 0, z / sp.sqrt(3), -I * sp.sqrt(sp.Rational(2, 3)) * y],
            [0, 0, I * sp.sqrt(sp.Rational(2, 3)) * y, z / sp.sqrt(3)],
        ]
    )
    assert is_zero(transformed - expected)

    det_plus = sp.factor(transformed[:2, :2].det())
    det_minus = sp.factor(transformed[2:, 2:].det())
    assert sp.simplify(det_plus - (z**2 - 2 * x**2) / 3) == 0
    assert sp.simplify(det_minus - (z**2 - 2 * y**2) / 3) == 0

    lines = [
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, SQRT2),
        (1, -1, SQRT2),
        (1, 1, -SQRT2),
        (1, -1, -SQRT2),
    ]
    for point in lines:
        specialization = transformed.subs(dict(zip((x, y, z), point)))
        assert specialization.rank() == 2

    # The first block has rank zero iff x=z=0; the second has rank zero
    # iff y=z=0.  If neither is zero, total rank <=2 iff each determinant
    # vanishes, which gives exactly the final four projective lines.
    assert transformed[:2, :2].subs({x: 0, z: 0}) == sp.zeros(2)
    assert transformed[2:, 2:].subs({y: 0, z: 0}) == sp.zeros(2)

    # Formula (4) also proves that a rank-at-most-one pencil element is
    # zero: if one 2x2 block vanishes, the other nonzero block has rank
    # two; otherwise the two nonzero blocks contribute at least one each.
    return det_plus, det_minus, lines


def vectorize(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(matrix).reshape(matrix.rows * matrix.cols, 1)


def algebra_closure(generators: list[sp.Matrix]) -> list[sp.Matrix]:
    """Exact unital algebra closure by repeated right multiplication."""

    dimension = generators[0].rows
    basis = [sp.eye(dimension)]
    rank = 1
    frontier = [sp.eye(dimension)]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            candidate = sp.simplify(current * generator)
            trial = sp.Matrix.hstack(
                *(vectorize(matrix) for matrix in basis + [candidate])
            )
            new_rank = trial.rank()
            if new_rank > rank:
                basis.append(candidate)
                frontier.append(candidate)
                rank = new_rank
    return basis


def check_generated_algebra(a_ops: list[sp.Matrix], b_ops: list[sp.Matrix]) -> int:
    # Remove the spectator c qubit.  The exact algebra must be M_4.
    a_active = [kron(pauli, ID2) for pauli in (X, Y, Z)]
    b_active = [
        -kron(X, X) / sp.sqrt(3),
        (kron(Z, Y) - kron(Y, Z)) / sp.sqrt(6),
        (kron(Y, Y) - kron(Z, Z)) / sp.sqrt(6),
    ]
    closure = algebra_closure(a_active + b_active)
    assert len(closure) == 16

    # Also verify the two simple human-proof extractions.
    ix = sp.simplify(-sp.sqrt(3) * a_active[0] * b_active[0])
    assert ix == kron(ID2, X)
    xy = sp.simplify(
        -sp.sqrt(6) * (a_active[2] * b_active[2] - b_active[2] * a_active[2])
        / (2 * I)
    )
    # Depending on the commutator convention this is +/- X tensor Y.
    assert xy in (kron(X, Y), -kron(X, Y))
    iy = sp.simplify(a_active[0] * xy)
    assert iy in (kron(ID2, Y), -kron(ID2, Y))

    # Guard that the full eight-dimensional coefficients are precisely
    # active operators tensored with the spectator identity.
    for full, active in zip(a_ops, a_active):
        assert full == kron(active, ID2)
    for full, active in zip(b_ops, b_active):
        assert full == kron(active, ID2)
    return len(closure)


def check_rank_four_calibration(h8: sp.Matrix) -> int:
    # Q = I_ab tensor |0><0|_c selects one spectator copy of the d=4
    # witness and must be square-invariant exactly.
    ket0 = sp.Matrix([[1, 0], [0, 0]])
    q = kron(sp.eye(4), ket0)
    pair = sp.kronecker_product(q, q)
    assert q.rank() == 4
    assert q * q == q
    assert is_zero(h8 * pair - pair * h8)
    return q.rank()


def main() -> None:
    h8, a_ops, b_ops = check_schmidt_expansion()
    det_plus, det_minus, lines = check_low_rank_pencil()
    algebra_dimension = check_generated_algebra(a_ops, b_ops)
    calibration_rank = check_rank_four_calibration(h8)
    print("exact identity-amplification checks passed")
    print(f"Bell block determinants: {det_plus}, {det_minus}")
    print(f"real rank-at-most-two pencil lines: {len(lines)}")
    print(f"active generated algebra dimension: {algebra_dimension}")
    print(f"exact invariant calibration rank: {calibration_rank}")
    print("human theorem: no rank-(4m-2) commuting projection for m >= 2")


if __name__ == "__main__":
    main()
