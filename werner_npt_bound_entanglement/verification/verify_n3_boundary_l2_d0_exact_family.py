#!/usr/bin/env python3
"""Verify the adjugate exact-zero family on the L2/L3 d=0 branch."""

from __future__ import annotations

import sympy as sp


def adjugate2(matrix):
    return sp.Matrix(
        [
            [matrix[1, 1], -matrix[0, 1]],
            [-matrix[1, 0], matrix[0, 0]],
        ]
    )


def assert_zero(matrix):
    assert all(sp.expand(value) == 0 for value in matrix)


def main():
    # The c variables are formal conjugates of the b variables.  None
    # of the identities requires treating them as algebraically
    # dependent.
    b00, b01, b10, b11 = sp.symbols("b00 b01 b10 b11")
    c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11")
    s = sp.symbols("s", real=True)
    identity = sp.eye(2)
    b = sp.Matrix([[b00, b01], [b10, b11]])
    b_dagger = sp.Matrix([[c00, c10], [c01, c11]])

    d = b - sp.trace(b) * identity
    d_dagger = b_dagger - sp.trace(b_dagger) * identity
    assert_zero(d + adjugate2(b))
    assert_zero(d_dagger + adjugate2(b_dagger))

    m = b_dagger * b
    assert_zero(d * d_dagger - adjugate2(m))
    assert_zero(
        (identity + s**2 * m)
        * (identity + s**2 * adjugate2(m))
        - (
            1 + s**2 * sp.trace(m) + s**4 * sp.det(m)
        )
        * identity
    )

    # The two-copy factor after the scalar-compatible polar
    # normalizations has these site-two blocks.
    e00 = s * d
    e01 = identity
    e10 = s**2 * b * d
    e11 = s * b
    assert_zero(e00 - e11 + s * sp.trace(b) * identity)
    assert_zero(e10 + s**2 * sp.det(b) * identity)
    assert_zero(e01 - identity)

    # Therefore every off-diagonal block and the diagonal difference
    # is scalar on site three, exactly the vanishing of the
    # fully-traceless two-qubit projection.
    print("verified exact d=0 adjugate zero family")


if __name__ == "__main__":
    main()
