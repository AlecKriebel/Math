#!/usr/bin/env python3
"""Exact Fourier minor for the displayed-tree noncut witness."""

from __future__ import annotations

import sys

import sympy as sp


def main() -> int:
    try:
        p0, p1, p2, p3, u = sp.symbols("p0 p1 p2 p3 u")

        # True quartet split 01|23, flattened across the wrong split 02|13.
        # In the zero-character block use row/column states 00 and CC.
        zero_block = sp.Matrix([
            [1, p1 * p3 * u],
            [p0 * p2 * u, p0 * p1 * p2 * p3],
        ])
        zero_minor = sp.factor(zero_block.det())
        expected = p0 * p1 * p2 * p3 * (1 - u**2)
        if sp.expand(zero_minor - expected) != 0:
            raise RuntimeError(("zero-block determinant", zero_minor))

        # One positive 1x1 entry from each C, G, T character block augments
        # the zero-block determinant to a 5x5 block-diagonal minor.
        nonzero_entries = (p0 * p1, p0 * p1, p0 * p1)
        five_minor = sp.factor(zero_minor * sp.prod(nonzero_entries))
        expected_five = sp.factor(expected * (p0 * p1) ** 3)
        if sp.expand(five_minor - expected_five) != 0:
            raise RuntimeError(("five-minor determinant", five_minor))
        if sp.factor(zero_minor.subs(u, 1)) != 0:
            raise RuntimeError("unit internal multiplier mutation survived")

        print(
            "K3P_DISPLAYED_TREE_MINOR_PASS "
            "zero_minor=p0*p1*p2*p3*(1-u^2) "
            "strict_for_0<p0,p1,p2,p3,u<1"
        )
        return 0
    except (RuntimeError, TypeError, ValueError) as error:
        print(f"K3P_DISPLAYED_TREE_MINOR_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
