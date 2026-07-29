#!/usr/bin/env python3
"""Exact checker for the large-Haar-slack critical-data obstruction.

This is a dependency-free rational verifier.  It checks one exact
member, delta=1/16, and the polynomial identities that hold for the
whole parameter family.  It also reconstructs the genuine balanced
qutrit code's common-origin Pluecker moments.
"""

from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations
from math import factorial


D = 3
delta = Q(1, 16)
q = -delta
g = (1 - 8 * delta) / 9
gamma = 2 * delta / 3
t = 15 * g / 16
m = delta / (1 + 2 * delta)


# Sector, endpoint, Haar-sum, marginal-floor, and refinement identities.
w0 = Q(0)
w1 = Q(0)
w2 = 2 * (1 + delta) / 3
w3 = (1 - 2 * delta) / 3
assert all(value >= 0 for value in (w0, w1, w2, w3))
assert w0 + w1 + w2 + w3 == 1
assert -w0 / 8 + w1 / 4 - w2 / 2 + w3 == q
assert 3 * g == Q(1, 3) - 3 * w1 / 4 - 8 * delta / 3
assert -w2 / 3 + w3 == g
assert w0 <= Q(2, 27)
assert w2 < Q(3, 4) < Q(24, 31)
assert g > 0
assert m < Q(1, 3)
assert delta < Q(1, 8)


def pair(first: int, second: int) -> int:
    return D * first + second


# The local form h = gamma L + t P_0 in the matrix-unit basis.
def k_entry(r: int, a: int, s: int, b: int) -> Q:
    hs = Q((r == s) and (a == b))
    traces = Q((r == a) and (s == b))
    return gamma * (hs - traces / 2) + t * (hs - traces / 3)


# Stationarity at rho=I/3.
for r in range(D):
    for a in range(D):
        left = sum(k_entry(r, a, s, s) for s in range(D))
        right = q * Q(r == a) / 3
        assert left == right


# Scalar/traceless spectra of h and G=h-qN.
h_scalar = -delta / 3
h_traceless = gamma + t
g_scalar = h_scalar + delta / 3
g_traceless = h_traceless + delta / 3
assert g_scalar == 0
assert g_traceless == delta + t > 0
trace_g = g_scalar + 8 * g_traceless
assert trace_g + 8 * q == Q(15, 2) * g
assert 8 * t == Q(15, 2) * g


# Quantitative isotropy estimate, squared to remain rational.
assert t * t <= Q(360 * 360 * 15) * g


# Inverted block Gram:
# beta_(a,r),(b,s) =
#   (gamma+2t/3) delta_ar delta_bs + (2t/15) delta_rs delta_ab.
def beta(a: int, r: int, b: int, s: int) -> Q:
    return (
        (gamma + 2 * t / 3) * Q((a == r) and (b == s))
        + 2 * t / 15 * Q((r == s) and (a == b))
    )


# Forward coefficient map exactly recovers h.
for r in range(D):
    for a in range(D):
        for s in range(D):
            for b in range(D):
                forward = (
                    Q(r == s) * sum(beta(a, p, b, p) for p in range(D))
                    - beta(a, r, b, s) / 2
                )
                assert forward == k_entry(r, a, s, b)


# beta is a positive combination of I_9 and |vec I><vec I|.
identity_coefficient = 2 * t / 15
rank_one_coefficient = gamma + 2 * t / 3
assert identity_coefficient > 0
assert rank_one_coefficient > 0


# Exact Frobenius distance from gamma |vec I><vec I|.
distance_squared = Q(0)
for a in range(D):
    for r in range(D):
        for b in range(D):
            for s in range(D):
                target = gamma * Q((a == r) and (b == s))
                distance_squared += (beta(a, r, b, s) - target) ** 2
assert distance_squared == Q(352, 75) * t * t
assert distance_squared <= Q(4752 * 4752 * 15) * g


# Genuine balanced qutrit code:
# k=0: 000,111,222; k=1: 012,120,201.
support = {
    (0, 0, 0, 0),
    (1, 1, 1, 0),
    (2, 2, 2, 0),
    (0, 1, 2, 1),
    (1, 2, 0, 1),
    (2, 0, 1, 1),
}


# Each of the two codewords has local density I/3 at every site.
for site in range(3):
    for logical in range(2):
        counts = [0, 0, 0]
        for entry in support:
            if entry[3] == logical:
                counts[entry[site]] += 1
        assert counts == [1, 1, 1]


Polynomial = dict[tuple[int, int, int], Q]


def minor_polynomials(row_party: int) -> list[Polynomial]:
    """All nonzero 2x2 flattening minors after contracting party 0."""

    other_party = 2 if row_party == 1 else 1
    entries: dict[tuple[int, int], Polynomial] = {}
    for row in range(D):
        for other in range(D):
            for logical in range(2):
                polynomial: defaultdict[tuple[int, int, int], Q] = defaultdict(Q)
                for first in range(D):
                    if row_party == 1:
                        index = (first, row, other, logical)
                    else:
                        index = (first, other, row, logical)
                    if index in support:
                        exponent = [0, 0, 0]
                        exponent[first] = 1
                        polynomial[tuple(exponent)] += 1
                entries[(row, 3 * logical + other)] = dict(polynomial)

    output: list[Polynomial] = []
    for row1, row2 in combinations(range(D), 2):
        for column1, column2 in combinations(range(2 * D), 2):
            polynomial = defaultdict(Q)
            for exponent1, coefficient1 in entries[(row1, column1)].items():
                for exponent2, coefficient2 in entries[(row2, column2)].items():
                    exponent = tuple(
                        left + right
                        for left, right in zip(exponent1, exponent2)
                    )
                    # Each tensor entry has its common factor 1/sqrt(3).
                    polynomial[exponent] += coefficient1 * coefficient2 / 3
            for exponent1, coefficient1 in entries[(row1, column2)].items():
                for exponent2, coefficient2 in entries[(row2, column1)].items():
                    exponent = tuple(
                        left + right
                        for left, right in zip(exponent1, exponent2)
                    )
                    polynomial[exponent] -= coefficient1 * coefficient2 / 3
            cleaned = {
                exponent: coefficient
                for exponent, coefficient in polynomial.items()
                if coefficient
            }
            if cleaned:
                output.append(cleaned)
    return output


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    output = defaultdict(Q)
    for exponent1, coefficient1 in left.items():
        for exponent2, coefficient2 in right.items():
            exponent = tuple(
                first + second
                for first, second in zip(exponent1, exponent2)
            )
            output[exponent] += coefficient1 * coefficient2
    return dict(output)


def haar_square(polynomial: Polynomial) -> Q:
    """E |p(z)|^2 for Haar z in C^3 and holomorphic homogeneous p."""

    output = Q(0)
    for exponent, coefficient in polynomial.items():
        degree = sum(exponent)
        numerator = 2
        for value in exponent:
            numerator *= factorial(value)
        denominator = factorial(degree + 2)
        output += coefficient * coefficient * Q(numerator, denominator)
    return output


left_minors = minor_polynomials(1)
right_minors = minor_polynomials(2)
assert len(left_minors) == len(right_minors) == 12
mean_a = sum((haar_square(poly) for poly in left_minors), Q(0))
mean_b = sum((haar_square(poly) for poly in right_minors), Q(0))
mean_ab = sum(
    (
        haar_square(multiply(left, right))
        for left in left_minors
        for right in right_minors
    ),
    Q(0),
)
assert mean_a == mean_b == Q(5, 36)
assert mean_ab == Q(47, 2430)
assert mean_ab / (mean_a * mean_b) == Q(376, 375)
assert mean_ab >= Q(2, 5) * mean_a * mean_b


# Recorded determinant floors.  The crude inequalities below are enough:
# 0 < m < 1 makes both numerators at most one.
assert mean_a >= m**8 * (1 - m) ** 4 / 79_350
assert mean_b >= m**8 * (1 - m) ** 4 / 79_350
assert mean_ab >= m**16 * (1 - m) ** 8 / 15_741_056_250


print(
    "verified: exact negative large-slack critical data satisfy the "
    "sector, stationary, Hessian, Haar, isotropy, block-Gram, marginal, "
    "and genuine common-pencil-minor constraints at delta=1/16"
)
