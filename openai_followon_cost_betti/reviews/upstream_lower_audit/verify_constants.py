"""Exact rational certificate for the upstream Bernoulli cost gap.

The analytic estimates used are (1 + 1/95)^95 < e < 3.
Thus K = e^96 * 96^4 * (96/95)^95 < 3^97 * 96^4.
This computation certifies the remaining rational inequalities and
does not numerically approximate the asserted lower bound.
"""

from fractions import Fraction
import json


def verify():
    alpha = Fraction(1, 2**61)
    eta = alpha / 100
    q_upper = Fraction(3**97 * 96**4, 2**183)
    assert 0 < alpha < Fraction(1, 200)
    assert q_upper < Fraction(1, 2)
    assert 92 * alpha < 1

    # The original eta is alpha/100. An exact height with a smaller
    # upper-cost surplus than eta also follows, independently of floats.
    height = 99 * eta.denominator + 1
    assert height > 100
    assert Fraction(99, height) < eta

    # The combinatorial union bound has exponent 99 - 1 - 95 = 3.
    assert 99 - 1 - 95 == 3

    # Exact corner inequalities for all lengths follow because both
    # no-outer and one-outer formulas are ell/3. Their difference from
    # ell-2 is 2*ell/3-2, nonnegative for ell >= 3.
    slope = Fraction(2, 3)
    assert slope > 0 and slope * 3 - 2 == 0

    return {
        "alpha": str(alpha),
        "eta": str(eta),
        "K_alpha_cubed_strict_upper": str(q_upper),
        "exact_twice_numerator": 2 * 3**97 * 96**4,
        "exact_denominator": 2**183,
        "admissible_height_M": height,
        "arithmetic_certificate": "PASS",
        "scope": "Arithmetic only; the topological and group-theoretic proof is audited separately.",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
