#!/usr/bin/env python3
"""Exact exhaustive d=6 search in the cyclic Gaussian functional ansatz.

Let u=U_12 and v=U_23 be the standard order-six Gaussian Weyl generators,
so u v = q v u with q=exp(i*pi/3).  This script exhausts every Hermitian
trace-zero involution H=f(U): its six spectral values must be three +1s and
three -1s, giving only binomial(6,3)=20 cases.

The computation takes place in the exact twisted group algebra with basis
u^a v^b, 0<=a,b<6.  It never builds 216 by 216 matrices.
"""

from itertools import combinations

import sympy as sp


ORDER = 6
ONE_THIRD = sp.Rational(1, 3)
Q = (1 + sp.I * sp.sqrt(3)) / 2


def clean(value):
    return sp.simplify(sp.expand_complex(value))


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = clean(result.get(monomial, 0) + coefficient)
    return {
        monomial: coefficient
        for monomial, coefficient in result.items()
        if coefficient != 0
    }


def scale(polynomial, scalar):
    return {
        monomial: clean(scalar * coefficient)
        for monomial, coefficient in polynomial.items()
        if clean(scalar * coefficient) != 0
    }


def multiply(left, right):
    """Multiply using v^b u^c = q^(-bc) u^c v^b."""

    result = {}
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            monomial = ((a + c) % ORDER, (b + d) % ORDER)
            coefficient = x * y * Q ** (-b * c)
            result[monomial] = clean(
                result.get(monomial, 0) + coefficient
            )
    return {
        monomial: coefficient
        for monomial, coefficient in result.items()
        if coefficient != 0
    }


def functional_coefficients(positive_spectrum):
    """Inverse Fourier transform of the selected +/-1 spectral values."""

    values = [
        1 if j in positive_spectrum else -1
        for j in range(ORDER)
    ]
    return [
        clean(
            sum(
                values[j] * Q ** (-j * k)
                for j in range(ORDER)
            )
            / ORDER
        )
        for k in range(ORDER)
    ]


def residual(coefficients):
    h1 = {
        (k, 0): coefficient
        for k, coefficient in enumerate(coefficients)
        if coefficient != 0
    }
    h2 = {
        (0, k): coefficient
        for k, coefficient in enumerate(coefficients)
        if coefficient != 0
    }
    return add(
        multiply(multiply(h1, h2), h1),
        scale(multiply(multiply(h2, h1), h2), -1),
        scale(add(h1, scale(h2, -1)), -ONE_THIRD),
    )


def main():
    survivors = []
    rows = []
    for positive in combinations(range(ORDER), ORDER // 2):
        coefficients = functional_coefficients(set(positive))
        obstruction = residual(coefficients)
        if not obstruction:
            survivors.append(positive)
        first = next(iter(sorted(obstruction.items())), None)
        rows.append((positive, len(obstruction), first))

    assert len(rows) == 20
    assert not survivors

    print("Exact cyclic Gaussian-functional search at d=6")
    print("ansatz: H=f(U), U^6=1, three +1 and three -1 spectral values")
    print("twisted relation: u v = exp(i*pi/3) v u")
    print("cases exhausted: 20")
    print("survivors: 0")
    print()
    print("positive spectral indices | nonzero residual coefficients | first")
    for positive, count, first in rows:
        print(f"{positive} | {count} | {first}")
    print()
    print("[proved within ansatz] no trace-zero Gaussian functional H solves")
    print("the exceptional cubic relation in local dimension six")


if __name__ == "__main__":
    main()
