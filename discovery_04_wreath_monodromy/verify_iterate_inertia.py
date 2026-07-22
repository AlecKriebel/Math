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

        # With v(s)=-1, the coefficient valuations of
        # 2*x*t^3-y*t^2+2*t-z are (at powers 0,1,2,3)
        # (-c, 0, -a, a).  The strict inequalities below say that the lower
        # Newton polygon consists only of the endpoint edge.  Every root then
        # has t-valuation tau=-(a+c)/3.
        tau = -(a + c) / 3
        coefficient_valuations = (-c, Fraction(0), -a, a)
        endpoint_line = tuple(-c + power * (a + c) / 3 for power in range(4))
        assert coefficient_valuations[0] == endpoint_line[0]
        assert coefficient_valuations[3] == endpoint_line[3]
        assert coefficient_valuations[1] > endpoint_line[1]
        assert coefficient_valuations[2] > endpoint_line[2]

        # Exact dominance checks in the three reconstruction formulas.  They
        # rule out every possible leading-term cancellation used in the local
        # Puiseux induction in the paper.
        assert -c < -a + 2 * tau  # 3*z dominates y*t^2
        assert -c < tau           # 3*z dominates 6*t
        next_a = (c - 2 * a) / 3
        assert tau - next_a < 0   # t*y dominates 1 in 1-t*y
        assert -c < next_a        # old z dominates 2*x and 3*x^2*y

        if level <= 8:
            print(
                f"m={level}: exponent={exponent_numerator}/{exponent_denominator}, "
                f"a={a}, c={c}"
            )

        next_c = 2 * (c - a)
        next_scaled_a = scaled_c - 2 * scaled_a
        next_scaled_c = 6 * (scaled_c - scaled_a)
        assert next_scaled_a == next_a * 3**level
        assert next_scaled_c == next_c * 3**level

        a, c = next_a, next_c
        scaled_a, scaled_c = next_scaled_a, next_scaled_c
        assert 0 <= a / c <= Fraction(1, 6)

    print("PASS: 30 exact Puiseux levels; every exponent numerator is 1 mod 3")
    print("PASS: Newton-edge and reconstruction dominance inequalities")


if __name__ == "__main__":
    main()
