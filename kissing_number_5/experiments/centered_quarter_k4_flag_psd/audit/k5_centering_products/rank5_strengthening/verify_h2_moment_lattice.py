#!/usr/bin/env python3
"""Dependency-free exact verifier for the H2 quarter-grid moment lattice."""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping


COLORS = tuple(range(-4, 3))
B = {color: 5 * color * color - 16 for color in COLORS}
V_SCALE = 14336
D_SCALE = 12845056


def invariants(
    counts: Mapping[int, int],
    ordered_triple_numerator_sum: int,
) -> tuple[int, int, int, int]:
    """Return S,R,X2,Y2 after checking the empirical divisibility data."""

    if set(counts) != set(COLORS):
        raise ValueError(f"counts must have exactly the colors {COLORS}")
    if any(not isinstance(counts[color], int) or counts[color] < 0 for color in COLORS):
        raise ValueError("pair counts must be nonnegative integers")
    if sum(counts.values()) != 820:
        raise ValueError("41 points have exactly 820 unordered pairs")
    if sum(color * counts[color] for color in COLORS) != -82:
        raise ValueError("centered quarter-grid pair counts must sum to -82")
    if not isinstance(ordered_triple_numerator_sum, int):
        raise ValueError("R must be an integer")
    if ordered_triple_numerator_sum % 30:
        raise ValueError("an empirical R must be divisible by 30")
    s = sum(counts[color] * B[color] ** 2 for color in COLORS)
    q = sum(counts[color] * color * color for color in COLORS)
    x1 = 5 * q - 11_808
    r = ordered_triple_numerator_sum
    x = 7 * s - 1_133_568
    y = 49 * r - 36_288 * s + 4_933_287_936
    if y != 49 * r - 5_184 * x - 943_128_576:
        raise AssertionError("the two exact Y2 forms disagree")
    if s % 30 != 10:
        raise AssertionError("S must be 10 modulo 30")
    if x % 210 != 82:
        raise AssertionError("X2 must be 82 modulo 210")
    if (x - 21 * x1 - 40) % 2100:
        raise AssertionError("joint H1/H2 X-moment congruence failed")
    if y % 210 != 66:
        raise AssertionError("Y2 must be 66 modulo 210")
    if (y - 10 * x - 2) % 49:
        raise AssertionError("joint X2/Y2 congruence failed")
    return s, r, x, y


def centered_moments(s: int, r: int) -> tuple[Fraction, Fraction]:
    t2 = Fraction(41) + Fraction(s, 2048)
    t3 = Fraction(41) + Fraction(3 * s, 2048) + Fraction(r, 262144)
    v = t2 - Fraction(41 * 41, 14)
    d = (
        t3
        - Fraction(3 * 41, 14) * t2
        + Fraction(2 * 41**3, 14**2)
    )
    return v, d


def verify_exact_scaling(s: int, r: int) -> None:
    v, d = centered_moments(s, r)
    x = 7 * s - 1_133_568
    y = 49 * r - 36_288 * s + 4_933_287_936
    if V_SCALE * v != x:
        raise AssertionError((V_SCALE * v, x))
    if D_SCALE * d != y:
        raise AssertionError((D_SCALE * d, y))
    analytic_residual = 144 * v**3 - 182 * d**2
    integer_residual = 576 * x**3 - 13 * y**2
    if integer_residual != 4 * V_SCALE**3 * analytic_residual:
        raise AssertionError("sharp-rank scaling identity failed")


def main() -> None:
    assert tuple(B[color] for color in COLORS) == (
        64,
        29,
        4,
        -11,
        -16,
        -11,
        4,
    )
    counts = dict.fromkeys(COLORS, 0)
    counts[-4] = 280
    counts[0] = 21
    counts[2] = 519
    s, r, x, y = invariants(counts, 0)
    verify_exact_scaling(s, r)
    print(
        "verified H2 lattice:",
        f"X2={x} == 82 (mod 210),",
        f"Y2={y} == 66 (mod 210)",
    )


if __name__ == "__main__":
    main()
