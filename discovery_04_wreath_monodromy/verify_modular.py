#!/usr/bin/env python3
"""Dependency-free finite-field certificate for the wreath-product result.

The specialization P(r,-3) has Frobenius cycle types (9), (2,1^7), and
(2^4,1) at the three displayed good primes.  The paper's elementary group
lemma shows that a subgroup of S3 wr S3 with these types is the full wreath
product.  This script checks multiplication, squarefreeness, and
irreducibility without a CAS or third-party package.
"""

from __future__ import annotations

from functools import reduce


# Coefficients are stored from constant term upward.
F = [
    17172300267,
    599887620,
    223986114,
    -15697056,
    9515052,
    -4580568,
    216612,
    33952,
    -256,
    -384,
]


CERTIFICATES = {
    # 6 times one irreducible factor of degree 9.
    13: (
        6,
        [[3, -1, -2, -4, -2, -3, 1, -5, 5, 1]],
        (9,),
    ),
    # 43 times seven linear factors and one irreducible quadratic.
    61: (
        43,
        [
            [18, 1],
            [29, 1],
            [-26, 1],
            [-19, 1],
            [-12, 1],
            [-9, 1],
            [-2, 1],
            [-16, -19, 1],
        ],
        (2, 1, 1, 1, 1, 1, 1, 1),
    ),
    # 15 times one linear factor and four irreducible quadratics.
    19: (
        15,
        [
            [4, 1],
            [-2, 5, 1],
            [-4, 9, 1],
            [-1, -6, 1],
            [3, -5, 1],
        ],
        (2, 2, 2, 2, 1),
    ),
}


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def normalized(poly: list[int], prime: int) -> list[int]:
    return trim([coefficient % prime for coefficient in poly])


def add(left: list[int], right: list[int], prime: int) -> list[int]:
    size = max(len(left), len(right))
    result = [0] * size
    for i in range(size):
        result[i] = (
            (left[i] if i < len(left) else 0)
            + (right[i] if i < len(right) else 0)
        ) % prime
    return trim(result)


def subtract(left: list[int], right: list[int], prime: int) -> list[int]:
    return add(left, [(-value) % prime for value in right], prime)


def multiply(left: list[int], right: list[int], prime: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % prime
    return trim(result)


def divide_with_remainder(
    dividend: list[int], divisor: list[int], prime: int
) -> tuple[list[int], list[int]]:
    dividend = normalized(dividend[:], prime)
    divisor = normalized(divisor[:], prime)
    assert divisor != [0]
    if len(dividend) < len(divisor):
        return [0], dividend
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    inverse_lead = pow(divisor[-1], -1, prime)
    while dividend != [0] and len(dividend) >= len(divisor):
        shift = len(dividend) - len(divisor)
        coefficient = dividend[-1] * inverse_lead % prime
        quotient[shift] = coefficient
        for i, value in enumerate(divisor):
            dividend[i + shift] = (dividend[i + shift] - coefficient * value) % prime
        trim(dividend)
    return trim(quotient), dividend


def remainder(dividend: list[int], divisor: list[int], prime: int) -> list[int]:
    return divide_with_remainder(dividend, divisor, prime)[1]


def monic(poly: list[int], prime: int) -> list[int]:
    poly = normalized(poly, prime)
    inverse = pow(poly[-1], -1, prime)
    return [(value * inverse) % prime for value in poly]


def gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    left, right = normalized(left, prime), normalized(right, prime)
    while right != [0]:
        left, right = right, remainder(left, right, prime)
    return monic(left, prime)


def power_mod(base: list[int], exponent: int, modulus: list[int], prime: int) -> list[int]:
    result = [1]
    base = remainder(base, modulus, prime)
    while exponent:
        if exponent & 1:
            result = remainder(multiply(result, base, prime), modulus, prime)
        base = remainder(multiply(base, base, prime), modulus, prime)
        exponent >>= 1
    return result


def prime_divisors(number: int) -> list[int]:
    result = []
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            result.append(divisor)
            while number % divisor == 0:
                number //= divisor
        divisor += 1
    if number > 1:
        result.append(number)
    return result


def irreducible(poly: list[int], prime: int) -> bool:
    """Rabin's exact irreducibility test over F_prime."""
    poly = monic(poly, prime)
    degree = len(poly) - 1
    if degree == 1:
        return True
    variable = [0, 1]
    for divisor in prime_divisors(degree):
        power = power_mod(variable, prime ** (degree // divisor), poly, prime)
        if gcd(subtract(power, variable, prime), poly, prime) != [1]:
            return False
    final_power = power_mod(variable, prime**degree, poly, prime)
    return remainder(subtract(final_power, variable, prime), poly, prime) == [0]


def derivative(poly: list[int], prime: int) -> list[int]:
    return trim([(i * poly[i]) % prime for i in range(1, len(poly))] or [0])


def check_certificate(prime: int) -> tuple[int, ...]:
    unit, factors, expected_pattern = CERTIFICATES[prime]
    product = reduce(lambda left, right: multiply(left, right, prime), factors, [unit])
    assert normalized(product, prime) == normalized(F, prime)
    assert all(irreducible(factor, prime) for factor in factors)
    assert gcd(normalized(F, prime), derivative(F, prime), prime) == [1]
    pattern = tuple(sorted((len(factor) - 1 for factor in factors), reverse=True))
    assert pattern == expected_pattern
    return pattern


def main() -> None:
    for prime in (13, 61, 19):
        pattern = check_certificate(prime)
        print(f"PASS p={prime}: squarefree irreducible degrees {pattern}")
    print("PASS Frobenius types: (9), (2,1^7), (2^4,1)")
    print("The wreath-product group lemma now forces order 6^3*6 = 1296.")


if __name__ == "__main__":
    main()
