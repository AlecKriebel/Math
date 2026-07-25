#!/usr/bin/env python3
"""Exact *geometrically centered* H1/H2 congruence checks.

This verifier uses only the Python standard library.  It deliberately takes
raw unordered pair counts and raw unordered-triple H2 numerator products,
rather than trusting precomputed aggregate residues.

It enforces A=sum(a*m_a)=-82.  Do not use its specialized residues for the
noncentered r12 endpoint; use verify_general_quarter_grid_moments.py there.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Iterable, Mapping


COLORS = tuple(range(-4, 3))
PAIR_TOTAL = 41 * 40 // 2
UNORDERED_TRIPLE_TOTAL = 41 * 40 * 39 // 6
H2_NUMERATOR = {color: 5 * color * color - 16 for color in COLORS}
H2_V_SCALE = 14336
H2_D_SCALE = 12845056


def validate_pair_counts(counts: Mapping[int, int]) -> None:
    if set(counts) != set(COLORS):
        raise ValueError(f"pair colors must be exactly {COLORS}")
    if any(
        not isinstance(counts[color], int) or counts[color] < 0
        for color in COLORS
    ):
        raise ValueError("pair multiplicities must be nonnegative integers")
    if sum(counts.values()) != PAIR_TOTAL:
        raise ValueError(f"pair multiplicities must sum to {PAIR_TOTAL}")


def h1_from_raw_pair_counts(
    counts: Mapping[int, int],
) -> tuple[int, int]:
    """Return Q and X, checking exact centering and X == 2 (mod 10)."""

    validate_pair_counts(counts)
    centered_sum = sum(color * counts[color] for color in COLORS)
    if centered_sum != -82:
        raise ValueError("pair counts fail exact centering sum -82")
    q = sum(color * color * counts[color] for color in COLORS)
    if q % 2:
        raise AssertionError("a^2 == a (mod 2) and centering force Q even")
    x = 5 * q - 11808
    if x % 10 != 2:
        raise AssertionError("H1 X must be 2 modulo 10")
    return q, x


def h2_from_raw_data(
    counts: Mapping[int, int],
    unordered_triple_products: Iterable[int],
) -> tuple[int, int, int, int]:
    """Return S,R,X2,Y2 from raw pair and unordered-triple data."""

    validate_pair_counts(counts)
    centered_sum = sum(color * counts[color] for color in COLORS)
    if centered_sum != -82:
        raise ValueError("pair counts fail exact centering sum -82")
    products = tuple(unordered_triple_products)
    if len(products) != UNORDERED_TRIPLE_TOTAL:
        raise ValueError(
            "need one H2 numerator product for each of "
            f"{UNORDERED_TRIPLE_TOTAL} unordered vertex triples"
        )
    if any(not isinstance(value, int) for value in products):
        raise ValueError("triple numerator products must be integers")
    # Every b_a is 4 modulo 5, so every product of three b_a values is
    # 4^3 == 4 modulo 5.  Check the raw data rather than assuming this.
    if any(value % 5 != 4 for value in products):
        raise ValueError("a raw H2 triple numerator product is not 4 mod 5")

    s = sum(
        counts[color] * H2_NUMERATOR[color] ** 2
        for color in COLORS
    )
    q = sum(color * color * counts[color] for color in COLORS)
    x1 = 5 * q - 11_808
    r = 6 * sum(products)
    x = 7 * s - 1_133_568
    y = 49 * r - 36_288 * s + 4_933_287_936

    # Pointwise, b_a^2 == 16 + 15a (mod 30).  Pair total 820 and
    # exact centering sum -82 therefore force S == 10 (mod 30).
    if s % 30 != 10:
        raise AssertionError("S must be 10 modulo 30")
    if r % 30:
        raise AssertionError("R must be 0 modulo 30")
    if x % 210 != 82:
        raise AssertionError("H2 X2 must be 82 modulo 210")
    if (x - 21 * x1 - 40) % 2100:
        raise AssertionError("joint H1/H2 X-moment congruence failed")
    if y % 210 != 66:
        raise AssertionError("H2 Y2 must be 66 modulo 210")
    if (y - 10 * x - 2) % 49:
        raise AssertionError("H2 joint residue modulo 49 failed")

    t2 = Fraction(41) + Fraction(s, 2048)
    t3 = Fraction(41) + Fraction(3 * s, 2048) + Fraction(r, 262144)
    variance = t2 - Fraction(41**2, 14)
    centered = (
        t3
        - Fraction(3 * 41, 14) * t2
        + Fraction(2 * 41**3, 14**2)
    )
    if H2_V_SCALE * variance != x:
        raise AssertionError("H2 X2 affine scaling failed")
    if H2_D_SCALE * centered != y:
        raise AssertionError("H2 Y2 affine scaling failed")
    analytic = 144 * variance**3 - 182 * centered**2
    integer = 576 * x**3 - 13 * y**2
    if integer != 4 * H2_V_SCALE**3 * analytic:
        raise AssertionError("H2 sharp-rank scaling failed")
    return s, r, x, y


def synthetic_pair_counts() -> dict[int, int]:
    counts = dict.fromkeys(COLORS, 0)
    counts[-4] = 280
    counts[0] = 21
    counts[2] = 519
    return counts


def expect_value_error(action, text: str) -> None:
    try:
        action()
    except ValueError:
        return
    raise AssertionError(f"tamper case was not rejected: {text}")


def self_test() -> None:
    # Exhaust the only parity identity used by the H1 proof.
    for parities in product((0, 1), repeat=len(COLORS)):
        linear = sum(
            color * parity
            for color, parity in zip(COLORS, parities)
        ) % 2
        quadratic = sum(
            color * color * parity
            for color, parity in zip(COLORS, parities)
        ) % 2
        if linear != quadratic:
            raise AssertionError("H1 parity identity failed")
    for color in COLORS:
        numerator = H2_NUMERATOR[color]
        if (numerator * numerator - 16 - 15 * color) % 30:
            raise AssertionError("H2 pointwise square congruence failed")
        if (
            numerator * numerator
            - 15 * color * color
            + 150 * color
            - 256
        ) % 300:
            raise AssertionError("H1/H2 pointwise joint congruence failed")

    counts = synthetic_pair_counts()
    _, h1_x = h1_from_raw_pair_counts(counts)
    if h1_x != 20972:
        raise AssertionError("unexpected H1 control value")

    # 64 is an actual H2 numerator product (4*4*4) and is 4 modulo 5.
    products = [64] * UNORDERED_TRIPLE_TOTAL
    _, _, h2_x, h2_y = h2_from_raw_data(counts, products)
    if h2_x % 210 != 82 or h2_y % 210 != 66:
        raise AssertionError("unexpected H2 control residues")

    wrong_total = counts.copy()
    wrong_total[0] -= 1
    expect_value_error(
        lambda: h1_from_raw_pair_counts(wrong_total),
        "wrong pair total",
    )
    noncentered = dict.fromkeys(COLORS, 0)
    noncentered[0] = PAIR_TOTAL
    expect_value_error(
        lambda: h1_from_raw_pair_counts(noncentered),
        "noncentered pair counts",
    )
    expect_value_error(
        lambda: h2_from_raw_data(
            noncentered,
            [64] * UNORDERED_TRIPLE_TOTAL,
        ),
        "noncentered H2 pair counts",
    )
    fractional = counts.copy()
    fractional[0] -= 0.5
    fractional[1] += 0.5
    expect_value_error(
        lambda: h1_from_raw_pair_counts(fractional),
        "fractional pair count",
    )
    expect_value_error(
        lambda: h2_from_raw_data(counts, products[:-1]),
        "missing unordered triple",
    )
    corrupted_products = products.copy()
    corrupted_products[0] = 65
    expect_value_error(
        lambda: h2_from_raw_data(counts, corrupted_products),
        "bad triple residue",
    )
    fractional_products = products.copy()
    fractional_products[0] = 64.5
    expect_value_error(
        lambda: h2_from_raw_data(counts, fractional_products),
        "fractional triple product",
    )


def main() -> None:
    self_test()
    print(
        "PASS: raw H1/H2 empirical congruences and seven tamper cases verified"
    )


if __name__ == "__main__":
    main()
