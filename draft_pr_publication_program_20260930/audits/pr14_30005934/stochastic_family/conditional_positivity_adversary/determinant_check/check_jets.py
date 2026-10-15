#!/usr/bin/env python3
"""Exact Taylor-jet checks of the symmetric determinant differential identity.

Uses only Python's standard library. No Wishart identity or claimed differential
formula is used to build the left side: expand det(c I + U)^p / det(c I)^p
by the finite generalized-binomial Taylor jet and apply det(-D).
"""

from fractions import Fraction
from itertools import permutations
from math import factorial, prod


def add(left, right):
    result = dict(left)
    for exponent, value in right.items():
        result[exponent] = result.get(exponent, Fraction(0)) + value
        if result[exponent] == 0:
            del result[exponent]
    return result


def scale(poly, scalar):
    return {exponent: value * scalar for exponent, value in poly.items() if value * scalar}


def multiply(left, right, degree):
    result = {}
    for left_exp, left_value in left.items():
        for right_exp, right_value in right.items():
            exponent = tuple(a + b for a, b in zip(left_exp, right_exp))
            if sum(exponent) <= degree:
                result[exponent] = result.get(exponent, Fraction(0)) + left_value * right_value
    return {exponent: value for exponent, value in result.items() if value}


def sign(permutation):
    inversions = sum(permutation[i] > permutation[j] for i in range(len(permutation)) for j in range(i + 1, len(permutation)))
    return (-1) ** inversions


def differential_value(n, alpha, c):
    coordinates = [(i, j) for i in range(n) for j in range(i, n)]
    index = {pair: k for k, pair in enumerate(coordinates)}
    zero = (0,) * len(coordinates)
    determinant = {}
    operator = []
    for permutation in permutations(range(n)):
        term = {zero: Fraction(sign(permutation))}
        derivative = [0] * len(coordinates)
        operator_weight = Fraction((-1) ** n * sign(permutation))
        for i, j in enumerate(permutation):
            coordinate = index[(min(i, j), max(i, j))]
            exponent = list(zero)
            exponent[coordinate] = 1
            entry = {tuple(exponent): Fraction(1)}
            if i == j:
                entry[zero] = c
            else:
                operator_weight /= 2
            term = multiply(term, entry, n)
            derivative[coordinate] += 1
        determinant = add(determinant, term)
        operator.append((tuple(derivative), operator_weight))
    normalized = scale(determinant, Fraction(1, c ** n))
    increment = add(normalized, {zero: Fraction(-1)})
    jet = {zero: Fraction(1)}
    power = {zero: Fraction(1)}
    binomial = Fraction(1)
    p = -alpha / 2
    for k in range(1, n + 1):
        power = multiply(power, increment, n)
        binomial *= (p - k + 1) / k
        jet = add(jet, scale(power, binomial))
    actual = sum(weight * jet.get(exponent, 0) * prod(factorial(entry) for entry in exponent) for exponent, weight in operator)
    expected = Fraction(1, 2 ** n) * prod(alpha - j for j in range(n)) / c ** n
    return actual, expected


def main():
    alphas = [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(3), Fraction(7, 2), Fraction(4), Fraction(5)]
    cs = [Fraction(1), Fraction(3, 2), Fraction(2)]
    checks = 0
    for n in range(1, 5):
        for alpha in alphas:
            for c in cs:
                actual, expected = differential_value(n, alpha, c)
                assert actual == expected, (n, alpha, c, actual, expected)
                checks += 1
        print(f'n={n}: all {len(alphas) * len(cs)} exact rational Taylor-jet checks passed')
    print(f'Total: {checks} checks passed')


if __name__ == '__main__':
    main()
