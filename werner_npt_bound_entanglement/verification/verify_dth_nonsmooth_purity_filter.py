#!/usr/bin/env python3
"""Exact audit of the nonsmooth DTH purity threshold."""

from fractions import Fraction as F


def objective(x):
    return 2 * (x * x + 2 * (F(1, 4) - x) ** 2 + x * x / 10)


def main():
    minimizer = F(5, 31)
    assert F(1, 8) < minimizer < F(1, 6)
    assert objective(minimizer) == F(11, 124)
    assert 32 * F(11, 124) - 1 == F(57, 31)

    # Complete the square exactly at the two interval endpoints.
    for endpoint in (F(1, 8), F(1, 6)):
        assert objective(endpoint) >= objective(minimizer)

    print("exact nonsmooth DTH purity filter passed")
    print("spectral minimum: 11/124 at lambda_1=5/31")
    print("local-purity threshold: 57/31")


if __name__ == "__main__":
    main()
