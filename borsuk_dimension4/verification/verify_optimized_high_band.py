#!/usr/bin/env python3
"""Exact verifier for notes/route_c_optimized_high_band.md.

The script uses only integers and fractions.  It checks the rational band,
the sharp defect extremizer, the algebraic elimination, a Sturm root count,
and the exact upper bracket proving the scalar-method barrier.
"""

from fractions import Fraction as Q
from itertools import permutations


# Polynomials are coefficient lists in ascending order.
def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def padd(left, right):
    out = [0] * max(len(left), len(right))
    for i in range(len(out)):
        out[i] = (left[i] if i < len(left) else 0) + (
            right[i] if i < len(right) else 0
        )
    return trim(out)


def pneg(poly):
    return [-coefficient for coefficient in poly]


def pscale(poly, scalar):
    return trim([scalar * coefficient for coefficient in poly])


def pmul(left, right):
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return trim(out)


def ppow(poly, exponent):
    out = [1]
    for _ in range(exponent):
        out = pmul(out, poly)
    return out


def peval(poly, value):
    return sum(Q(coefficient) * value**i for i, coefficient in enumerate(poly))


# A polynomial in t is a list whose entries are polynomials in x.
def btadd(left, right):
    out = [[0] for _ in range(max(len(left), len(right)))]
    for i in range(len(out)):
        out[i] = padd(
            left[i] if i < len(left) else [0],
            right[i] if i < len(right) else [0],
        )
    while len(out) > 1 and out[-1] == [0]:
        out.pop()
    return out


def btmul(left, right):
    out = [[0] for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = padd(out[i + j], pmul(a, b))
    while len(out) > 1 and out[-1] == [0]:
        out.pop()
    return out


def btscale(poly_t, poly_x):
    return [pmul(coefficient, poly_x) for coefficient in poly_t]


def sign(value):
    return 1 if value > 0 else -1 if value < 0 else 0


def verify_sharp_defect_family() -> None:
    # In Lemma 1, W <= 1/727 gives |lambda_i-1/5| < 3/40 and hence
    # lambda_i > 1/8.  This is the exact comparison needed for x+y>1/4.
    assert Q(2, 727) < Q(9, 1600)
    assert Q(1, 5) - Q(3, 40) == Q(1, 8)
    assert Q(1, 727) < Q(1, 15)
    # This is exactly (3d)^2 < 3d/5 at the largest allowed d, so the
    # maximizer u=3d lies in the permitted interval.
    endpoint_delta = Q(1, 727)
    assert (3 * endpoint_delta) ** 2 < Q(3, 5) * endpoint_delta

    # Coefficients in the indeterminate d.
    low_weight = [Q(1, 5), -3]
    high_weight = [Q(1, 5), 2]
    assert padd(pscale(low_weight, 2), pscale(high_weight, 3)) == [1]

    # W = 1/2(2(-3d)^2 + 3(2d)^2) = 15d^2.
    weight_defect = pscale(
        padd(pscale(pmul([0, -3], [0, -3]), 2),
             pscale(pmul([0, 2], [0, 2]), 3)),
        Q(1, 2),
    )
    assert weight_defect == [0, 0, 15]

    # With alpha = 25d/(1-15d), the low-weight row is x*alpha = 5d,
    # and the weighted edge cost is d(1-15d).
    denominator = [1, -15]
    assert pscale(low_weight, 5) == denominator
    edge_cost = pmul([0, 1], denominator)
    assert padd(weight_defect, edge_cost) == [0, 1]

    # For a single edge of weight one, P Alpha P has exact eigenvectors
    # with eigenvalues -1 and 3/5.
    projection = [
        [Q(4, 5) if i == j else Q(-1, 5) for j in range(5)]
        for i in range(5)
    ]
    alpha = [[Q(0) for _ in range(5)] for _ in range(5)]
    alpha[0][1] = alpha[1][0] = Q(1)

    def matmul(left, right):
        return [
            [sum(left[i][k] * right[k][j] for k in range(5)) for j in range(5)]
            for i in range(5)
        ]

    compressed = matmul(matmul(projection, alpha), projection)

    def matvec(matrix, vector):
        return [sum(matrix[i][j] * vector[j] for j in range(5)) for i in range(5)]

    negative_vector = [1, -1, 0, 0, 0]
    positive_vector = [3, 3, -2, -2, -2]
    assert matvec(compressed, negative_vector) == [-1, 1, 0, 0, 0]
    assert matvec(compressed, positive_vector) == pscale(positive_vector, Q(3, 5))


def verify_rational_band() -> None:
    delta = Q(1, 728)
    total = 25 * delta / (1 - 15 * delta)
    sigma_minus = total
    sigma_plus = Q(3, 5) * total
    assert total == Q(25, 713)
    assert sigma_plus == Q(15, 713)

    a = sigma_minus / (1 - sigma_minus)
    b = 3 + 5 * a
    slack = 1 / (1 - sigma_minus) - 1 / (1 + sigma_plus)
    center = Q(7, 17)
    assert a == Q(25, 688)
    assert b == Q(2189, 688)
    assert slack == Q(3565, 62608)
    assert center < b / 2

    rational_part = (b + 2 * center) / 5 + slack * center + Q(2, 5) * center**2
    radical_sq = 2 * b * center
    radical_coefficient = Q(2, 5)
    target = Q(1, 4) / (1 + sigma_plus)
    assert rational_part == Q(5766141, 6462040)
    assert radical_sq == Q(15323, 5848)
    assert target == Q(713, 2912)

    left = rational_part - target
    assert left == Q(117149693, 180937120)
    assert left > 0
    square_margin = radical_coefficient**2 * radical_sq - left**2
    assert square_margin == Q(186180822731, 6547648278778880)
    assert square_margin > 0


def build_elimination_polynomials():
    # L=(1-x)(5+3x), c=L+20x+2tL.
    ell = [5, -2, -3]
    c = [padd(ell, [0, 20]), pscale(ell, 2)]
    anchor_factor = pmul([3, 2], [5, 3])
    derivative_rhs = pmul(pmul([3, 2], [1, -1]), ppow([5, 3], 2))

    # D=2t c^2-(3+2x)(1-x)(5+3x)^2.
    derivative_poly = btadd(
        btmul([[0], [2]], btmul(c, c)),
        [pneg(derivative_rhs)],
    )

    # E0 and E from equations (30).
    threshold_core = btscale(c, anchor_factor)
    threshold_core = btadd(
        threshold_core,
        btmul([[0], [2]], btscale(c, ell)),
    )
    threshold_core = btadd(
        threshold_core,
        [pscale(pmul(anchor_factor, ell), -2)],
    )
    threshold_core = btadd(
        threshold_core,
        btmul([[0], [0, 40]], c),
    )
    threshold_core = btadd(
        threshold_core,
        btmul([[0], [0], [2]], btscale(c, ell)),
    )
    threshold_poly = btadd(
        btscale(threshold_core, pscale([5, 3], 4)),
        btscale(c, pscale(ell, -25)),
    )

    assert len(derivative_poly) == 4
    assert len(threshold_poly) == 4
    return derivative_poly, threshold_poly


def sylvester_resultant_cubics(first, second):
    rows = []
    for shift in range(3):
        rows.append([
            [0] if j < shift or j >= shift + 4 else first[3 - (j - shift)]
            for j in range(6)
        ])
    for shift in range(3):
        rows.append([
            [0] if j < shift or j >= shift + 4 else second[3 - (j - shift)]
            for j in range(6)
        ])

    determinant = [0]
    for permutation in permutations(range(6)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(6)
            for j in range(i + 1, 6)
        )
        term = [1]
        for row in range(6):
            term = pmul(term, rows[row][permutation[row]])
        determinant = padd(determinant, pscale(term, -1 if inversions % 2 else 1))
    return determinant


H_POLY = [
    -190625,
    5046875,
    11336875,
    -7724125,
    -22203875,
    1329277,
    15615705,
    12827745,
    3918240,
    500580,
    23328,
]

K_POLY = [
    -61,
    49525,
    -3800875,
    41036875,
    3469325000,
    -87853600000,
    129195000000,
    23578200000000,
    -453330000000000,
    3786750000000000,
    -12150000000000000,
]


def verify_resultant_and_substitution() -> None:
    derivative_poly, threshold_poly = build_elimination_polynomials()
    resultant = sylvester_resultant_cubics(derivative_poly, threshold_poly)
    expected = pscale(
        pmul(
            pmul(
                pmul(ppow([-1, 1], 6), [3, 2]),
                ppow([5, 3], 10),
            ),
            H_POLY,
        ),
        2560,
    )
    assert resultant == expected

    # Substitute x=25d/(1-15d), clearing the tenth-power denominator.
    numerator = [0, 25]
    denominator = [1, -15]
    substituted = [0]
    degree = len(H_POLY) - 1
    for i, coefficient in enumerate(H_POLY):
        term = pmul(ppow(numerator, i), ppow(denominator, degree - i))
        substituted = padd(substituted, pscale(term, coefficient))
    assert substituted == pscale(K_POLY, 3125)


def polynomial_divmod(dividend, divisor):
    dividend = [Q(value) for value in trim(dividend)]
    divisor = [Q(value) for value in trim(divisor)]
    quotient = [Q(0)] * max(1, len(dividend) - len(divisor) + 1)
    while len(dividend) >= len(divisor) and not (
        len(dividend) == 1 and dividend[0] == 0
    ):
        shift = len(dividend) - len(divisor)
        factor = dividend[-1] / divisor[-1]
        quotient[shift] = factor
        for j, coefficient in enumerate(divisor):
            dividend[j + shift] -= factor * coefficient
        dividend = trim(dividend)
    return trim(quotient), trim(dividend)


def derivative(poly):
    return trim([Q(i) * poly[i] for i in range(1, len(poly))] or [Q(0)])


def sign_changes(signs):
    nonzero = [item for item in signs if item]
    return sum(left != right for left, right in zip(nonzero, nonzero[1:]))


def sturm_sequence(poly):
    sequence = [[Q(value) for value in poly], derivative(poly)]
    while True:
        _, remainder = polynomial_divmod(sequence[-2], sequence[-1])
        remainder = trim([-value for value in remainder])
        if len(remainder) == 1 and remainder[0] == 0:
            break
        sequence.append(remainder)
    return sequence


def verify_root_count_and_bracket() -> None:
    sequence = sturm_sequence(H_POLY)
    assert [len(poly) - 1 for poly in sequence] == list(range(10, -1, -1))

    signs_at_zero = [sign(poly[0]) for poly in sequence]
    signs_at_infinity = [sign(poly[-1]) for poly in sequence]
    assert sign_changes(signs_at_zero) - sign_changes(signs_at_infinity) == 1

    lower_total = Q(25, 713)
    upper_total = Q(25, 712)
    signs_at_lower = [sign(peval(poly, lower_total)) for poly in sequence]
    signs_at_upper = [sign(peval(poly, upper_total)) for poly in sequence]
    assert sign_changes(signs_at_lower) - sign_changes(signs_at_upper) == 1

    assert peval(K_POLY, Q(1, 728)) == Q(
        -62651547670389194403421,
        2552077471698829010599936,
    )
    assert peval(K_POLY, Q(1, 727)) == Q(
        2053339764513756372448918336,
        41242416955341131537413053649,
    )

    # No root modulo 7, hence no rational root over Q.
    coefficients_mod_7 = [coefficient % 7 for coefficient in K_POLY]
    assert coefficients_mod_7 == [2, 0, 6, 5, 1, 2, 3, 2, 3, 5, 2]
    values_mod_7 = [
        sum(coefficient * pow(value, i, 7)
            for i, coefficient in enumerate(coefficients_mod_7)) % 7
        for value in range(7)
    ]
    assert values_mod_7 == [2, 3, 6, 6, 1, 4, 3]


def verify_upper_barrier() -> None:
    # At delta=1/727, T=25/712.  Bracket the unique minimizing t using
    # the squared derivative equation t(2+5q+4t)^2=2B.
    total = Q(25, 712)
    sigma_plus = Q(3, 5) * total
    b = (3 + 2 * total) / (1 - total)
    slack = 1 / (1 - total) - 1 / (1 + sigma_plus)
    lower_t = Q(20583, 50000)
    upper_t = Q(41167, 100000)
    assert total < Q(1, 6)
    assert b < 4
    assert upper_t < Q(1, 2)

    def derivative_polynomial(center):
        return center * (2 + 5 * slack + 4 * center) ** 2 - 2 * b

    assert derivative_polynomial(lower_t) < 0
    assert derivative_polynomial(upper_t) > 0

    # On this bracket, the rational part of rho is increasing and the
    # radical is at most its value at upper_t.
    rational_lower = b / 5 + (Q(2, 5) + slack) * lower_t + Q(2, 5) * lower_t**2
    target = Q(1, 4) / (1 + sigma_plus)
    left = rational_lower - target
    assert left > 0
    square_margin = left**2 - Q(4, 25) * (2 * b * upper_t)
    assert square_margin == Q(
        462920369845229531253847921,
        9744113421914062500000000000000,
    )
    assert square_margin > 0


if __name__ == "__main__":
    verify_sharp_defect_family()
    verify_rational_band()
    verify_resultant_and_substitution()
    verify_root_count_and_bracket()
    verify_upper_barrier()
    print("optimized high-radius band: exact checks passed")
