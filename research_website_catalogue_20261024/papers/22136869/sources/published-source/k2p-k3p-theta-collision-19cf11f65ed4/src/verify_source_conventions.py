#!/usr/bin/env python3
"""Exact rational check of the source paper's K2P conventions."""
from fractions import Fraction as F
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def k2p(c: F, g: F) -> list[F]:
    return [F(1), c, g, c]


NAME = "ACGT"
ADD = [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]


def sun(a, b, c, d, e, f, delta, x, y, z):
    require(F(0) < delta < F(1), "inheritance parameter must lie in (0,1)")
    return a[x] * b[y] * c[z] * (
        delta * d[z] * f[y] + (1 - delta) * e[z] * f[ADD[y][z]]
    )


def main() -> None:
    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10 or newer is required")

    a, b, c, d, e, f = [
        k2p(F(1, 3), F(2, 5)),
        k2p(F(2, 7), F(3, 7)),
        k2p(F(1, 4), F(5, 9)),
        k2p(F(3, 8), F(4, 9)),
        k2p(F(2, 9), F(1, 2)),
        k2p(F(5, 11), F(3, 10)),
    ]
    delta = F(2, 5)
    checks = {
        (0, 2, 2): b[2] * c[2] * (delta * d[2] * f[2] + (1 - delta) * e[2]),
        (1, 1, 0): a[1] * b[1] * f[1],
        (2, 0, 2): a[2] * c[2] * (delta * d[2] + (1 - delta) * e[2] * f[2]),
        (2, 2, 0): a[2] * b[2] * f[2],
        (3, 1, 2): a[1] * b[1] * c[2] * f[1] * (delta * d[2] + (1 - delta) * e[2]),
    }
    for labels, expected in checks.items():
        require(sun(a, b, c, d, e, f, delta, *labels) == expected,
                f"source coordinate mismatch at {labels}")

    # Reproduce favorable-order Q factorization numerically exactly by identity.
    coords = {
        (x, y, z): sun(a, b, c, d, e, f, delta, x, y, z)
        if x ^ y ^ z == 0 else F(0)
        for x in range(4) for y in range(4) for z in range(4)
    }
    invariant = (
        coords[0, 2, 2] * coords[2, 0, 2] * coords[1, 1, 0] ** 2
        - coords[0, 0, 0] * coords[2, 2, 0] * coords[3, 1, 2] ** 2
    )
    positive = (
        a[2] * b[2] * c[2] ** 2 * d[2] * e[2]
        * a[1] ** 2 * b[1] ** 2 * f[1] ** 2
        * delta * (1 - delta) * (1 - f[2]) ** 2
    )
    require(invariant == positive, "favorable-order Q factorization")
    require(invariant > 0, "favorable-order Q must be strictly positive")
    print("[source conventions] PASS  A,C,G,T order; C+G=T; K2P a_C=a_T")
    print("[source conventions] PASS  five explicit Lemma 4.1 coordinates and favorable-order Q factorization")


if __name__ == "__main__":
    main()
