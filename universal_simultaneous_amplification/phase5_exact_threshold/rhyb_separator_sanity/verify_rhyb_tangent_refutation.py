#!/usr/bin/env python3
"""Exact refutation of the R_hyb affine tangent by a stored weak-cut witness."""

from __future__ import annotations

import sympy as sp


def main():
    r = sp.symbols("r", positive=True)
    polynomial = r**6 - 8*r**5 + 22*r**4 - 30*r**3 + 21*r**2 - 6*r + 1
    lo = sp.Rational(1502856912, 10**9)
    hi = sp.Rational(1502856913, 10**9)
    assert polynomial.subs(r, lo) > 0 > polynomial.subs(r, hi)
    assert sp.Poly(polynomial, r).count_roots(lo, hi) == 1

    order_a, order_b = 2, 20
    order = order_a + order_b
    sigma = sp.Rational(19, 137)

    def bd_complete(size: int):
        return sp.factor((1 - 1/r) / (1 - r**(-size)))

    def db_complete(size: int):
        return sp.factor(
            sp.Rational(size - 1, size) * (1 - 1/r) / (1 - r**(1-size))
        )

    z_ba = sigma * r**order_b * (r**order_a - 1) / (r**order_b - 1)
    z_bb = sigma**(-1) * r**order_a * (r**order_b - 1) / (r**order_a - 1)
    z_da = (
        sigma**(-1)
        * sp.Rational(order_a * (order_b - 1), order_b * (order_a - 1))
        * r**order_b
        * (r**(order_a - 1) - 1)
        / (r**(order_b - 1) - 1)
    )
    z_db = (
        sigma
        * sp.Rational(order_b * (order_a - 1), order_a * (order_b - 1))
        * r**order_a
        * (r**(order_b - 1) - 1)
        / (r**(order_a - 1) - 1)
    )
    rho_b = (
        sp.Rational(order_a, order) * bd_complete(order_a) * z_ba / (1 + z_ba)
        + sp.Rational(order_b, order) * bd_complete(order_b) * z_bb / (1 + z_bb)
    )
    rho_d = (
        sp.Rational(order_a, order) * db_complete(order_a) * z_da / (1 + z_da)
        + sp.Rational(order_b, order) * db_complete(order_b) * z_db / (1 + z_db)
    )
    x = sp.factor(rho_b / bd_complete(order))
    y = sp.factor(rho_d / db_complete(order))
    score = sp.factor(y - 1 + (r - 1) * (x - 1))
    numerator, denominator = map(sp.factor, sp.together(score).as_numer_denom())

    assert denominator.subs(r, lo) > 0 and denominator.subs(r, hi) > 0
    assert numerator.subs(r, lo) > 0 and numerator.subs(r, hi) > 0
    # A Sturm count proves that the score numerator has no zero in the
    # isolating interval of R_hyb, so the positive endpoint sign persists.
    assert sp.Poly(numerator, r).count_roots(lo, hi) == 0

    root = sp.RootOf(polynomial, 0)
    assert lo < root < hi
    assert sp.N(score.subs(r, root), 30) > 0

    # The hybrid tangent is uniquely forced by annihilating the leaf vector.
    q = sp.symbols("q")
    leaf_separator = -1 + q / (r - 1)
    assert sp.solve(leaf_separator, q) == [r - 1]

    print(f"R_hyb~{sp.N(root, 22)}")
    print(f"stored weak-cut tangent score~{sp.N(score.subs(r, root), 22)}")
    print("PASS: exact R_hyb root isolation")
    print("PASS: exact positive stored-witness tangent score")
    print("REFUTED: universal affine separator D+(R_hyb-1)B<=0")
    print("OPEN: nonlinear endpoint disjunction / compactness theorem")


if __name__ == "__main__":
    main()
