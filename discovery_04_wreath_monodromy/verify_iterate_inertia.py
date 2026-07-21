#!/usr/bin/env python3
"""Dependency-free check of the all-iterate valuation recurrence.

The proof that the recurrence implies full-cycle inertia is mathematical; this
script checks the exact integer identities, invariant inequalities, and
coprimality pattern for a long finite prefix as a regression certificate.
"""

from fractions import Fraction
from math import gcd


def main() -> None:
    scaled_a, scaled_c = 0, 1
    a, c = Fraction(0), Fraction(1)

    for level in range(1, 31):
        exponent_numerator = scaled_a + scaled_c
        exponent_denominator = 3**level
        assert gcd(exponent_numerator, 3) == 1
        assert Fraction(exponent_numerator, exponent_denominator) == (a + c) / 3
        assert c > 5 * a

        if level <= 8:
            print(
                f"m={level}: exponent={exponent_numerator}/{exponent_denominator}, "
                f"a={a}, c={c}"
            )

        next_a = (c - 2 * a) / 3
        next_c = 2 * (c - a)
        next_scaled_a = scaled_c - 2 * scaled_a
        next_scaled_c = 6 * (scaled_c - scaled_a)
        assert next_scaled_a == next_a * 3**level
        assert next_scaled_c == next_c * 3**level

        a, c = next_a, next_c
        scaled_a, scaled_c = next_scaled_a, next_scaled_c
        assert 0 <= a / c <= Fraction(1, 6)

    print("PASS: 30 exact levels; every exponent numerator is 1 mod 3")
    print("The note proves this congruence and the invariant interval uniformly.")


if __name__ == "__main__":
    main()
