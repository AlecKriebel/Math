"""Exact data for the fixed 12-point weighted D5 support.

This module intentionally uses only Python integers and fractions so it can be
imported by a small exact verifier without NumPy or a solver.
"""

from fractions import Fraction


ROOTS = (
    (-1, 0, 0, 1, 0),
    (1, 0, 0, 1, 0),
    (0, -1, -1, 0, 0),
    (0, -1, 1, 0, 0),
    (0, 1, 0, 0, -1),
    (0, 1, 0, 0, 1),
    (0, 0, -1, -1, 0),
    (0, 0, 1, -1, 0),
    (-1, 0, 0, 0, -1),
    (-1, 0, 0, 0, 1),
    (1, 0, 0, 0, -1),
    (1, 0, 0, 0, 1),
)

WEIGHTS = (
    Fraction(1, 10),
    Fraction(1, 10),
    Fraction(1, 10),
    Fraction(1, 10),
    Fraction(1, 10),
    Fraction(1, 10),
    Fraction(1, 10),
    Fraction(1, 10),
    Fraction(1, 20),
    Fraction(1, 20),
    Fraction(1, 20),
    Fraction(1, 20),
)


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def all_d5_roots():
    roots = []
    for i in range(5):
        for j in range(i + 1, 5):
            for si in (-1, 1):
                for sj in (-1, 1):
                    row = [0] * 5
                    row[i] = si
                    row[j] = sj
                    roots.append(tuple(row))
    return tuple(roots)


def completion_roots():
    support = set(ROOTS)
    return tuple(r for r in all_d5_roots() if r not in support)
