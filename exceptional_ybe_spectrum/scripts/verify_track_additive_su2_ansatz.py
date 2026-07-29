#!/usr/bin/env python3
"""Exact rejection certificate for the SU(2)-equivariant (2,3,2) ansatz."""

from __future__ import annotations

import sympy as sp


def kron3(left, middle, right):
    return sp.kronecker_product(left, middle, right)


def main():
    imaginary = sp.I
    half = sp.Rational(1, 2)

    # Spin-1/2 generators.
    sx = sp.Matrix([[0, half], [half, 0]])
    sy = sp.Matrix([[0, -imaginary * half], [imaginary * half, 0]])
    sz = sp.diag(half, -half)

    # Spin-1 generators in the m=1,0,-1 basis.
    root_two = sp.sqrt(2)
    raising = sp.Matrix(
        [[0, root_two, 0], [0, 0, root_two], [0, 0, 0]]
    )
    lowering = raising.T
    spin_one_x = (raising + lowering) / 2
    spin_one_y = (raising - lowering) / (2 * imaginary)
    spin_one_z = sp.diag(1, 0, -1)

    identity_two = sp.eye(2)
    identity_three = sp.eye(3)

    # Total-spin Casimir on V_{1/2} tensor V_1 tensor V_{1/2}.
    casimir = sp.zeros(12)
    for outer, middle in zip(
        (sx, sy, sz), (spin_one_x, spin_one_y, spin_one_z)
    ):
        total = (
            kron3(outer, identity_three, identity_two)
            + kron3(identity_two, middle, identity_two)
            + kron3(identity_two, identity_three, outer)
        )
        casimir += total * total

    # Eigenvalues of the Casimir are 0,2,6. This polynomial is -1 on
    # total spins 0 and 2, and +1 on the two total-spin-1 copies.
    h = (
        -sp.eye(12)
        + sp.Rational(3, 2) * casimir
        - sp.Rational(1, 4) * casimir * casimir
    )
    assert h * h == sp.eye(12)
    assert sp.trace(h) == 0

    h1 = sp.kronecker_product(h, sp.eye(6))
    h2 = sp.kronecker_product(sp.eye(6), h)
    residual = (
        h1 * h2 * h1
        - h2 * h1 * h2
        - sp.Rational(1, 3) * (h1 - h2)
    )

    nonzero = [
        (row, column, sp.simplify(residual[row, column]))
        for row in range(72)
        for column in range(72)
        if residual[row, column] != 0
    ]
    assert len(nonzero) == 644
    assert residual[1, 1] == sp.Rational(13, 8)

    print("H^2 = I_12: PASS")
    print("Tr(H) = 0: PASS")
    print("Cubic-relation residual nonzero entries:", len(nonzero))
    print("Exact rejection certificate: residual[1,1] =", residual[1, 1])
    print("The complementary equivariant involution -H has residual -D.")
    print("All assertions passed (exact SymPy arithmetic).")


if __name__ == "__main__":
    main()
