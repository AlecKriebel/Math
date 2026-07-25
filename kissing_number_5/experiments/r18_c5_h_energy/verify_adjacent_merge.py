#!/usr/bin/env python3
"""Exact certificate for the adjacent-mass secant inequality.

The checker uses integer polynomial arithmetic throughout.  It constructs a
degree-18 rational surrogate for F, divides out every equality-boundary factor,
converts the resulting four-variable polynomial to the tensor Bernstein basis,
and checks every coefficient against 7/50.  It also proves the rational pi
bracket and the C^3 approximation-error budget used in the accompanying proof.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb, factorial, gcd


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def arctan_alternating_bounds(reciprocal, last_index):
    """Bounds for arctan(1/reciprocal), ending at the given series index."""
    total = Fraction(0)
    for j in range(last_index + 1):
        term = Fraction(1, (2 * j + 1) * reciprocal ** (2 * j + 1))
        total += term if j % 2 == 0 else -term
    next_term = Fraction(
        1,
        (2 * last_index + 3) * reciprocal ** (2 * last_index + 3),
    )
    if last_index % 2 == 0:
        return total - next_term, total
    return total, total + next_term


def verify_pi_bracket():
    # Machin: pi/4 = 4 atan(1/5) - atan(1/239).
    # The tangent calculation is checked exactly:
    # tan(4 atan(1/5))=120/119 and tan(A-B)=1.
    require(2 * 5 * 5 == 50, "unexpected integer arithmetic failure")
    tan_2a = Fraction(2, 5) / (1 - Fraction(1, 25))
    tan_4a = 2 * tan_2a / (1 - tan_2a * tan_2a)
    require(tan_2a == Fraction(5, 12), "wrong double-angle tangent")
    require(tan_4a == Fraction(120, 119), "wrong quadruple-angle tangent")
    tan_difference = (tan_4a - Fraction(1, 239)) / (
        1 + tan_4a * Fraction(1, 239)
    )
    require(tan_difference == 1, "Machin tangent identity failed")

    low_5, high_5 = arctan_alternating_bounds(5, 10)
    low_239, high_239 = arctan_alternating_bounds(239, 2)
    pi_low = 4 * (4 * low_5 - high_239)
    pi_high = 4 * (4 * high_5 - low_239)
    require(pi_low > Fraction(314159, 100000), "pi lower bracket too weak")
    require(pi_high < Fraction(314160, 100000), "pi upper bracket too weak")

    k0 = Fraction(1309, 625)  # 2.0944
    k_low = 2 * pi_low / 3
    k_high = 2 * pi_high / 3
    require(k_high < k0, "chosen rational frequency is not above 2*pi/3")
    require(k0 - k_low < Fraction(1, 150000), "frequency error too large")
    return k0


# Sparse integer polynomials in (s,t,r,u), later reusing r as v.
NVAR = 4
ZERO = (0, 0, 0, 0)


def add_polynomial(p, q, scale=1):
    out = defaultdict(int)
    out.update(p)
    for monomial, coefficient in q.items():
        out[monomial] += scale * coefficient
    return {m: c for m, c in out.items() if c}


def scale_polynomial(p, scale):
    if scale == 0:
        return {}
    return {m: scale * c for m, c in p.items() if c}


def multiply_polynomial(p, q):
    out = defaultdict(int)
    for left, a in p.items():
        for right, b in q.items():
            monomial = tuple(left[i] + right[i] for i in range(NVAR))
            out[monomial] += a * b
    return {m: c for m, c in out.items() if c}


def power_polynomial(p, exponent):
    out = {ZERO: 1}
    base = p
    while exponent:
        if exponent & 1:
            out = multiply_polynomial(out, base)
        exponent >>= 1
        if exponent:
            base = multiply_polynomial(base, base)
    return out


ONE = {ZERO: 1}
S = {(1, 0, 0, 0): 1}
T = {(0, 1, 0, 0): 1}
R = {(0, 0, 1, 0): 1}
U = {(0, 0, 0, 1): 1}


def subtract_polynomial(p, q):
    return add_polynomial(p, q, -1)


def compose_scaled_univariate(coefficients, argument):
    out = {}
    for coefficient in reversed(coefficients):
        out = multiply_polynomial(out, argument)
        if coefficient:
            out = add_polynomial(out, {ZERO: coefficient})
    return out


def scaled_f_coefficients(k0):
    """Integer coefficients of SCALE*f(x)."""
    p, q = k0.numerator, k0.denominator
    scale = 8 * factorial(18) * q**18
    require(scale % 4 == 0, "scale does not represent 3/4")
    coefficients = [0] * 19
    coefficients[0] = 3 * scale // 4
    for j in range(1, 10):
        degree = 2 * j
        multiplier = factorial(18) // factorial(degree)
        coefficients[degree] = (
            (-1 if j % 2 else 1)
            * (3 + 2**degree)
            * p**degree
            * multiplier
            * q ** (18 - degree)
        )
    # The factor 8 is already present in SCALE and cancels the 1/8 in f.
    return scale, coefficients


def divide_monomial_exact(p, powers):
    out = {}
    for monomial, coefficient in p.items():
        require(
            all(monomial[i] >= powers[i] for i in range(NVAR)),
            f"missing equality-boundary factor at {monomial}",
        )
        reduced = tuple(monomial[i] - powers[i] for i in range(NVAR))
        out[reduced] = coefficient
    return out


def divide_one_minus_t_exact(p):
    groups = defaultdict(dict)
    for monomial, coefficient in p.items():
        groups[(monomial[0], monomial[2], monomial[3])][monomial[1]] = coefficient
    out = {}
    for fixed, coefficients in groups.items():
        degree = max(coefficients)
        cumulative = 0
        for j in range(degree + 1):
            cumulative += coefficients.get(j, 0)
            if j < degree and cumulative:
                out[(fixed[0], j, fixed[1], fixed[2])] = cumulative
        require(cumulative == 0, f"polynomial is not divisible by 1-t: {fixed}")
    return out


def substitute_r_equals_one_minus_s_times_v(p):
    rv = multiply_polynomial(subtract_polynomial(ONE, S), R)
    powers_s = [power_polynomial(S, j) for j in range(19)]
    powers_t = [power_polynomial(T, j) for j in range(19)]
    powers_rv = [power_polynomial(rv, j) for j in range(19)]
    powers_u = [power_polynomial(U, j) for j in range(19)]
    out = {}
    for monomial, coefficient in p.items():
        term = {ZERO: coefficient}
        term = multiply_polynomial(term, powers_s[monomial[0]])
        term = multiply_polynomial(term, powers_t[monomial[1]])
        term = multiply_polynomial(term, powers_rv[monomial[2]])
        term = multiply_polynomial(term, powers_u[monomial[3]])
        out = add_polynomial(out, term)
    return out


def lcm(a, b):
    return a // gcd(a, b) * b


def exact_bernstein_numerators(power_coefficients, degrees):
    """Return common-denominator Bernstein numerators."""
    current = power_coefficients
    common_denominator = 1
    for axis, degree in enumerate(degrees):
        axis_denominator = 1
        for j in range(degree + 1):
            axis_denominator = lcm(axis_denominator, comb(degree, j))
        transform = [
            [
                (
                    axis_denominator * comb(i, j) // comb(degree, j)
                    if j <= i
                    else 0
                )
                for j in range(degree + 1)
            ]
            for i in range(degree + 1)
        ]
        groups = defaultdict(dict)
        for monomial, coefficient in current.items():
            fixed = monomial[:axis] + monomial[axis + 1 :]
            groups[fixed][monomial[axis]] = coefficient
        transformed = {}
        for fixed, coefficients in groups.items():
            for i in range(degree + 1):
                value = sum(
                    transform[i][j] * coefficients.get(j, 0)
                    for j in range(i + 1)
                )
                if value:
                    monomial = fixed[:axis] + (i,) + fixed[axis:]
                    transformed[monomial] = value
        current = transformed
        common_denominator *= axis_denominator
    return current, common_denominator


def construct_and_verify_bernstein(k0):
    scale, coefficients = scaled_f_coefficients(k0)

    def scaled_f(argument):
        return compose_scaled_univariate(coefficients, argument)

    def scaled_p(argument):
        return add_polynomial(
            add_polynomial(scaled_f(argument), scaled_f(subtract_polynomial(ONE, argument))),
            {ZERO: -(3 * scale // 4)},
        )

    x = multiply_polynomial(S, T)
    a = multiply_polynomial(R, U)
    c = subtract_polynomial(R, a)

    def scaled_phi(X):
        Y = subtract_polynomial(S, X)
        positive = add_polynomial(
            add_polynomial(scaled_f(add_polynomial(X, R)), scaled_f(add_polynomial(Y, R))),
            add_polynomial(
                scaled_f(subtract_polynomial(subtract_polynomial(ONE, X), a)),
                scaled_f(subtract_polynomial(subtract_polynomial(ONE, Y), c)),
            ),
        )
        return add_polynomial(
            positive,
            add_polynomial(scaled_p(X), scaled_p(Y)),
            -1,
        )

    secant_gap = subtract_polynomial(
        add_polynomial(
            multiply_polynomial(subtract_polynomial(ONE, T), scaled_phi({})),
            multiply_polynomial(T, scaled_phi(S)),
        ),
        scaled_phi(x),
    )

    # Divide D_f by s^2*t*(1-t)*r, then subtract 2.
    quotient = divide_monomial_exact(secant_gap, (2, 1, 1, 0))
    quotient = divide_one_minus_t_exact(quotient)
    quotient = add_polynomial(quotient, {ZERO: -2 * scale})
    cube_polynomial = substitute_r_equals_one_minus_s_times_v(quotient)
    degrees = tuple(max(m[i] for m in cube_polynomial) for i in range(NVAR))
    require(degrees == (15, 15, 15, 16), f"unexpected multidegree {degrees}")

    bernstein, basis_denominator = exact_bernstein_numerators(
        cube_polynomial,
        degrees,
    )
    expected_count = 1
    for degree in degrees:
        expected_count *= degree + 1
    # Zero coefficients are legal, so enumerate the full tensor below.
    minimum_margin = None
    minimum_index = None
    digest = sha256()
    for index in product(*(range(degree + 1) for degree in degrees)):
        value = bernstein.get(index, 0)
        digest.update(str(value).encode("ascii"))
        digest.update(b"\n")
        margin = 50 * value - 7 * scale * basis_denominator
        if minimum_margin is None or margin < minimum_margin:
            minimum_margin = margin
            minimum_index = index
    require(expected_count == 69632, "unexpected Bernstein tensor size")
    require(minimum_margin is not None and minimum_margin > 0, "Bernstein bound < 7/50")
    certificate_digest = digest.hexdigest()
    expected_digest = "5153dc70e2db1f215f2c8e60c39f55e1a5a41960f849bfb315edd2fb6a47b21b"
    require(certificate_digest == expected_digest, "Bernstein tensor digest changed")
    require(minimum_index == (15, 0, 0, 0), "minimum coefficient index changed")
    return {
        "scale": scale,
        "basis_denominator": basis_denominator,
        "minimum_index": minimum_index,
        "minimum_margin": minimum_margin,
        "digest": certificate_digest,
    }


def verify_error_budget(k0):
    # For k=2*pi/3, |k-k0|<delta and k,k0<K.
    delta = Fraction(1, 150000)
    K = Fraction(21, 10)
    frequency_error = delta * (
        Fraction(3, 8) * (3 * K**2 + K**3)
        + (3 * K**2 + 2 * K**3)
    )
    taylor_error = k0**3 * (
        Fraction(3, 8) * k0**17 + (2 * k0) ** 17
    ) / factorial(17)
    c3_error = frequency_error + taylor_error
    require(c3_error < Fraction(1, 800), "C^3 error budget exceeded")
    normalized_operator_error = Fraction(3, 2) * c3_error
    require(
        Fraction(7, 50) - normalized_operator_error > 0,
        "Bernstein margin does not dominate analytic remainder",
    )
    return c3_error


def main():
    k0 = verify_pi_bracket()
    c3_error = verify_error_budget(k0)
    certificate = construct_and_verify_bernstein(k0)
    print("verified: adjacent merge D >= 2*x*y*(a+c)")
    print("C3_error_bound", c3_error)
    print("minimum_Bernstein_index", certificate["minimum_index"])
    print("Bernstein_digest", certificate["digest"])


if __name__ == "__main__":
    main()
