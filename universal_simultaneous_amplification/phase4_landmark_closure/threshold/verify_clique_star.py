#!/usr/bin/env python3
"""Exact certificates for the separated unequal-clique-star reduction."""

from __future__ import annotations

from fractions import Fraction as F


def add(poly: dict[int, int], exponent: int, coefficient: int) -> None:
    poly[exponent] = poly.get(exponent, 0) + coefficient
    if poly[exponent] == 0:
        del poly[exponent]


def certificate_polynomials(c: int, l: int) -> tuple[dict[int, int], dict[int, int]]:
    """Return D from its original expression and its positive decomposition."""
    original: dict[int, int] = {}
    add(original, c, c * (l - 1))
    add(original, 1, -c * (l - 1))
    add(original, c + 1, -(c - 1) * l)
    add(original, c + l, c - 1)
    add(original, 0, (c - 1) * (l - 1))

    decomposed: dict[int, int] = {}
    # (l-1)(r^c-cr+c-1)
    add(decomposed, c, l - 1)
    add(decomposed, 1, -c * (l - 1))
    add(decomposed, 0, (c - 1) * (l - 1))
    # +(c-1)r^c(r^l-lr+l-1)
    add(decomposed, c + l, c - 1)
    add(decomposed, c + 1, -(c - 1) * l)
    add(decomposed, c, (c - 1) * (l - 1))
    return original, decomposed


def a_bd(size: int, r: F) -> F:
    return (r - 1) * r ** (size - 1) / (r**size - 1)


def b_bd(size: int, r: F) -> F:
    return (r - 1) / (r**size - 1)


def a_db(size: int, r: F) -> F:
    return F(size - 1, size) * (r - 1) * r ** (size - 2) / (r ** (size - 1) - 1)


def b_db(size: int, r: F) -> F:
    return F(size - 1, size) * (r - 1) / (r ** (size - 1) - 1)


def gammas(c: int, l: int, r: F, z: F) -> tuple[F, F]:
    # Bd: source-normalized cross rates.
    A_bd = r * a_bd(c, r) / (r * a_bd(c, r) + b_bd(l, r) / z)
    B_bd = (r * a_bd(l, r) / z) / (r * a_bd(l, r) / z + b_bd(c, r))
    gamma_bd = (1 - A_bd) / B_bd
    x_bd = z * (r**l - 1) / (r**l * (r**c - 1))
    assert gamma_bd == (1 + x_bd) / (1 + r ** (c + l) * x_bd)

    # dB: target normalization and the 1/r reverse-invasion defense factor.
    A_db = (r * a_db(c, r) / z) / (r * a_db(c, r) / z + b_db(l, r) / r)
    B_db = (r * a_db(l, r)) / (r * a_db(l, r) + b_db(c, r) / (r * z))
    gamma_db = (1 - A_db) / B_db
    x_db = b_db(c, r) / (z * r**l * b_db(l, r))
    assert gamma_db == (1 + x_db) / (1 + r ** (c + l) * x_db)
    return gamma_bd, gamma_db


def main() -> None:
    checks = 0
    for c in range(2, 13):
        for l in range(2, 9):
            original, decomposed = certificate_polynomials(c, l)
            assert original == decomposed
            for r in (F(101, 100), F(11, 10), F(6, 5), F(3, 2), F(2), F(5)):
                for z in (F(1, 3), F(1), F(7, 5), F(4)):
                    gamma_bd, gamma_db = gammas(c, l, r, z)
                    baseline = 1 - 1 / r
                    bd_delta = a_bd(l, r) * (1 - gamma_bd) - baseline
                    assert (bd_delta > 0) == (z > 1)

                    numerator = (c - 1) * (r ** (c + 1) * (l - r ** (l - 1)) - (l - 1))
                    denominator = c * (l - 1) * r * (r ** (c - 1) - 1)
                    Z = numerator / denominator
                    assert Z < 1
                    db_delta = a_db(l, r) * (1 - gamma_db) - baseline
                    assert (db_delta > 0) == (z < Z)
                    assert not (bd_delta > 0 and db_delta > 0)
                    checks += 1
    print(f"PASS exact unequal-clique-star certificates checks={checks}")


if __name__ == "__main__":
    main()

