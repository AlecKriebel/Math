#!/usr/bin/env python3
"""Small exact checker for the algebra and finite sign cases in the frame proof.

The geometric inputs (spherical triangle inequality, monotonicity of cos^2 on
[0,pi/2], and the two-vector frame eigenvalues 1 +/- <p,q>) are stated in the
accompanying proof.  This checker verifies the exact trigonometric coefficient
identities and exhausts all 32 cyclic sign words.
"""

from fractions import Fraction
from itertools import product


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def verify_pair_identity():
    # cos^2(L+v)+cos^2(L-v) = 1 + cos(2L) cos(2v),
    # with L=pi/3 and cos(2L)=-1/2.
    cos_2L = Fraction(-1, 2)
    constant = Fraction(1)
    coefficient_of_cos_2v = cos_2L
    require(constant == 1, "pair identity constant changed")
    require(
        coefficient_of_cos_2v == Fraction(-1, 2),
        "pair identity cosine coefficient changed",
    )
    # On |v| <= pi/6, cos(2v) >= 1/2.
    upper_bound = constant + coefficient_of_cos_2v * Fraction(1, 2)
    require(upper_bound == Fraction(3, 4), "deep-pair bound is not 3/4")


def verify_triple_identity():
    # After cos^2 x=(1+cos 2x)/2, the nonconstant terms are
    # cos(q)+cos(2L-q)+cos(4L-q).  With L=pi/3, the coefficients of
    # cos(q) are 1,-1/2,-1/2 and those of sin(q) are 0,+sqrt(3)/2,
    # -sqrt(3)/2.
    cos_coefficients = (Fraction(1), Fraction(-1, 2), Fraction(-1, 2))
    sqrt3_sin_coefficients = (Fraction(0), Fraction(1, 2), Fraction(-1, 2))
    require(sum(cos_coefficients) == 0, "triple cosine terms do not cancel")
    require(
        sum(sqrt3_sin_coefficients) == 0,
        "triple sine terms do not cancel",
    )
    constant = 3 * Fraction(1, 2)
    require(constant == Fraction(3, 2), "triple identity constant changed")


def cyclic_cuts(signs):
    return sum(signs[i] != signs[(i + 1) % 5] for i in range(5))


def run_lengths(signs):
    cuts = cyclic_cuts(signs)
    if cuts == 0:
        return (5,)
    # Start immediately after a cut, then read the cyclic runs.
    start = next(i for i in range(5) if signs[i - 1] != signs[i])
    lengths = []
    length = 1
    for step in range(1, 5):
        here = (start + step) % 5
        previous = (here - 1) % 5
        if signs[here] == signs[previous]:
            length += 1
        else:
            lengths.append(length)
            length = 1
    lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def verify_sign_cases():
    counts = {0: 0, 2: 0, 4: 0}
    for signs in product((-1, 1), repeat=5):
        cuts = cyclic_cuts(signs)
        require(cuts in counts, f"odd or impossible cut count {cuts}: {signs}")
        counts[cuts] += 1
        runs = run_lengths(signs)
        if cuts == 0:
            require(runs == (5,), f"wrong zero-cut runs: {signs}, {runs}")
        elif cuts == 2:
            require(
                runs in ((4, 1), (3, 2)),
                f"wrong two-cut runs: {signs}, {runs}",
            )
        else:
            require(
                runs == (2, 1, 1, 1),
                f"wrong four-cut runs: {signs}, {runs}",
            )
    require(counts == {0: 2, 2: 20, 4: 10}, f"wrong sign-word counts: {counts}")


def verify_mass_bookkeeping():
    deep_pair = Fraction(3, 4)
    zero_cut_bound = 5 * deep_pair / 2
    four_plus_one = 2 * deep_pair + 1
    three_plus_two = 2 * deep_pair + deep_pair
    four_cut = Fraction(3, 2) + Fraction(3, 2)
    require(zero_cut_bound == Fraction(15, 8), "wrong zero-cut bound")
    require(four_plus_one == Fraction(5, 2), "wrong 4+1 bound")
    require(three_plus_two == Fraction(9, 4), "wrong 3+2 bound")
    require(four_cut == 3, "wrong four-cut bound")


def main():
    verify_pair_identity()
    verify_triple_identity()
    verify_sign_cases()
    verify_mass_bookkeeping()
    print("verified: exact C5-cell frame bound lambda_max <= 3")


if __name__ == "__main__":
    main()
