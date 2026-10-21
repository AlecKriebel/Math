#!/usr/bin/env python3
"""Exact arithmetic checks for authored shortcut counterexamples; not a theorem proof."""
from fractions import Fraction
from itertools import permutations
import json


def determinant(a):
    n = len(a)
    total = Fraction(0)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = Fraction((-1) ** inversions)
        for i in range(n):
            term *= a[i][p[i]]
        total += term
    return total


def minor(sequence, rows, columns):
    return [[sequence[j-i] if 0 <= j-i < len(sequence) else Fraction(0)
             for j in columns] for i in rows]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    truncated = [Fraction(1), Fraction(1), Fraction(1)]
    m = minor(truncated, [0,1,2], [1,2,3])
    require(determinant(m) == -1, 'Truncated geometric determinant changed')
    padded = truncated + [Fraction(0)] * 5
    require(all(padded[n] ** 2 >= padded[n-1] * padded[n+1]
                for n in range(1, len(padded)-1)), 'Log-concavity check failed')
    ez2 = [Fraction(1), Fraction(0), Fraction(1)]
    require(determinant(minor(ez2, [0,1], [1,2])) == -1,
            'exp(z^2) determinant changed')
    require(Fraction(1) > Fraction(1,2), 'Polynomial approximation obstruction failed')
    print(json.dumps({
        'truncated_geometric_minor': -1,
        'truncated_geometric_log_concave': True,
        'exp_z2_minor': -1,
        'geometric_violates_polynomial_h2_bound': True,
        'scope': 'Exact examples only; not a verification of the infinite classification.'
    }, indent=2))

if __name__ == '__main__':
    main()
