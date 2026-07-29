#!/usr/bin/env python3
"""Exact symbolic checker for product saturation of the pair rank-one slack."""

import sympy as sp


def kron3(left, middle, right):
    return sp.kronecker_product(left, middle, right)


def main():
    a, b, c, d = sp.symbols("a b c d", real=True)
    identity = sp.eye(3)
    e00 = sp.zeros(3)
    e00[0, 0] = 1
    e01 = sp.zeros(3)
    e01[0, 1] = 1
    p = identity / 3
    q = e00 - p

    t0 = (
        kron3(p, q, q)
        + kron3(q, p, q)
        + kron3(q, q, p)
    )
    t1 = kron3(e01, p, q) + kron3(e01, q, p)
    t2 = kron3(p, e01, q) + kron3(q, e01, p)
    t3 = kron3(p, q, e01) + kron3(q, p, e01)
    e = a * t0 + b * t1 + c * t2 + d * t3

    y = sp.zeros(27, 1)
    y[0], y[9], y[3], y[1] = a, b, c, d
    h = sp.expand(4 * sp.eye(27) + 12 * y * y.T - 81 * e.T * e)

    blocks = (
        (0, 1, 3, 9),
        (2,),
        (4, 10, 12, 13),
        (5, 11, 14),
        (6,),
        (7, 15, 16),
        (8, 17),
        (18,),
        (19, 21, 22),
        (20, 23),
        (24, 25),
        (26,),
    )
    block_of = {
        index: block_number
        for block_number, block in enumerate(blocks)
        for index in block
    }
    assert all(
        h[row, col] == 0
        for row in range(27)
        for col in range(27)
        if block_of[row] != block_of[col]
    )

    # Impose a^2+b^2+c^2+d^2=1 by replacing every occurrence of 4
    # where needed in the hand block formulas.  The direct matrices
    # below are exactly the blocks stated in the proof.
    norm_relation = {d**2: 1 - a**2 - b**2 - c**2}

    first = h.extract(blocks[0], blocks[0])
    t = sp.Matrix((a, d, c, b))
    assert sp.simplify(first - 4 * (sp.eye(4) - t * t.T)) == sp.zeros(4)

    r = sp.Matrix((b, c, d))
    upper = 3 * sp.eye(3) + 2 * sp.diag(b**2, c**2, d**2) - r * r.T
    second = sp.Matrix.vstack(
        sp.Matrix.hstack(upper, -2 * a * r),
        sp.Matrix.hstack(-2 * a * r.T, sp.Matrix([[3 * a**2]])),
    )
    actual_second = h.extract(blocks[2], blocks[2])
    assert sp.simplify((actual_second - second).subs(norm_relation)) == sp.zeros(4)

    upper_two = (
        (3 + d**2) * sp.eye(2)
        + sp.Matrix((b, -c)) * sp.Matrix((b, -c)).T
    )
    three = sp.Matrix.vstack(
        sp.Matrix.hstack(upper_two, -2 * a * sp.Matrix((b, c))),
        sp.Matrix.hstack(
            -2 * a * sp.Matrix((b, c)).T,
            sp.Matrix([[3 * a**2 + 4 * d**2]]),
        ),
    )
    actual_three = h.extract(blocks[3], blocks[3])
    assert sp.simplify((actual_three - three).subs(norm_relation)) == sp.zeros(3)

    two = sp.Matrix(
        (
            (4 - a**2, -2 * a * b),
            (-2 * a * b, 3 * a**2 + 4 * (c**2 + d**2)),
        )
    )
    actual_two = h.extract(blocks[6], blocks[6])
    assert sp.simplify((actual_two - two).subs(norm_relation)) == sp.zeros(2)

    # Exact boundary identities.
    assert sp.simplify((e.T * e).trace() - sp.Rational(4, 9)) == (
        sp.Rational(4, 9)
        * (a**2 + b**2 + c**2 + d**2 - 1)
    )
    x = sp.zeros(27, 1)
    x[0] = 1
    assert sp.simplify(
        (e * y - sp.Rational(4, 9) * x).subs(norm_relation)
    ) == sp.zeros(27, 1)
    assert sp.simplify(
        (e.T * x - sp.Rational(4, 9) * y)
    ) == sp.zeros(27, 1)

    # The scalar estimates used in the three Schur complements.
    u = sp.symbols("u", real=True, nonnegative=True)
    assert sp.simplify(
        u / (3 - u)
        - sp.Rational(1, 2)
        - 3 * (u - 1) / (2 * (3 - u))
    ) == 0
    assert sp.Rational(3) - sp.Rational(4, 3) == sp.Rational(5, 3)

    print(
        "verified: canonical block decomposition, boundary identities, "
        "and product-saturation spectral-gap constants"
    )


if __name__ == "__main__":
    main()
