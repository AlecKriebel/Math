#!/usr/bin/env python3
"""Exact finite sanity checks; NOT a machine verification of the theorem."""

import argparse
import json
from fractions import Fraction as Q


def c(j):
    return Q(1, 2 ** abs(j))


def g(real, imag=0):
    return Q(real), Q(imag)


ZERO = g(0)


def plus(a, b):
    return a[0] + b[0], a[1] + b[1]


def times(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def abs2(a):
    return a[0] ** 2 + a[1] ** 2


def inverse(a):
    return a[0] / abs2(a), -a[1] / abs2(a)


# A sequence entry has key (integer shift coordinate, fibre coordinate).
def shift(x, n):
    return {(j - n, t): value for (j, t), value in x.items()}


def scale(lam, x):
    return {key: times(lam, value) for key, value in x.items()}


def add(x, y):
    return {key: plus(x.get(key, ZERO), y.get(key, ZERO)) for key in x.keys() | y.keys()}


def norm2(x):
    return sum((c(j) * abs2(value) for (j, _), value in x.items()), Q(0))


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def check_indices_and_conjugacy():
    x = {(-2, 0): g(3, 1), (1, 1): g(-2, 4)}
    check(shift(x, 3) == {(-5, 0): g(3, 1), (-2, 1): g(-2, 4)}, "shift sign")
    check(shift(shift(x, -11), 11) == x, "finite-support inverse")
    # p=1: D(a)_j=a_j/c_j and B(a)_{j-1}=(c_{j-1}/c_j)a_j.
    a = {-4: Q(2, 3), 0: Q(-5), 3: Q(7, 11)}
    ba = {j - 1: c(j - 1) / c(j) * value for j, value in a.items()}
    dba = {j: value / c(j) for j, value in ba.items()}
    sda = {j - 1: value / c(j) for j, value in a.items()}
    check(dba == sda, "D B = S D")
    check(sum(c(j) * abs(value / c(j)) for j, value in a.items())
          == sum(abs(value) for value in a.values()), "D isometry, p=1")


def check_bounded_distortion():
    # W has three atoms of mass 1. h_j(t)=c_j*d_j(t); m_j=3*c_j.
    # At j=0, h_0=1. Other fibres cycle (1/2,1,3/2), so K=2 works.
    def density(j, t):
        return Q(1) if j == 0 else (Q(1, 2), Q(1), Q(3, 2))[(t + j) % 3]

    for j in range(-7, 8):
        check(sum(c(j) * density(j, t) for t in range(3)) == 3 * c(j), "fibre mass")
        for mask in range(8):
            subset = [t for t in range(3) if mask & (1 << t)]
            mu_j = sum((c(j) * density(j, t) for t in subset), Q(0))
            check(c(j) * len(subset) / 2 <= mu_j <= 2 * c(j) * len(subset), "BD subset")
    x = {(j, t): g(j + t, j - 2 * t) for j in range(-7, 8) for t in range(3)}
    original = sum(c(j) * density(j, t) * abs2(value) for (j, t), value in x.items())
    check(norm2(x) / 2 <= original <= 2 * norm2(x), "BD norm comparison, p=2")


def check_perturbation():
    a = {(-2, 0): g(1, 2), (0, 1): g(-3, 1), (1, 0): g(2)}
    b = {(-1, 1): g(2, -1), (0, 0): g(3, 4), (2, 1): g(-1, 2)}
    lam, n, epsilon = g(3, 4), 40, Q(1, 1000)
    perturbation = scale(inverse(lam), shift(b, -n))
    z = add(a, perturbation)
    az = scale(lam, shift(z, n))
    aa = scale(lam, shift(a, n))
    check(az == add(aa, b), "A(a + lambda^-1 R_n b) = A(a) + b")
    check(norm2(perturbation) < epsilon ** 2, "small input perturbation")
    check(norm2(aa) < epsilon ** 2, "small output error")


def check_tail_examples():
    checked = 0
    for p in (1, 2):
        for radius in (0, 1, 3, 7):
            indices = range(-radius, radius + 1)
            for epsilon in (Q(1, 10), Q(1, 1000)):
                n = radius + 1
                while sum(c(j + n) for j in indices) >= epsilon ** p:
                    n += 1
                forward = sum(c(j + n) for j in indices)
                backward = sum(c(j - n) for j in indices)
                factor = sum((Q(2) ** (-j) for j in indices), Q(0))
                check(forward == backward == Q(2) ** (-n) * factor, "geometric tail formula")
                check(forward < epsilon ** p, "two small tails for |lambda|=1")
                checked += 1
            # For c_j=1 both sums equal |F|. Their scaled product is |F|^(2/p).
            # Test representative moduli without taking inexact p-th roots.
            mass = Q(2 * radius + 1)
            for modulus in (Q(1, 4), Q(1), Q(7)):
                check(not (mass / modulus ** p < 1 and mass * modulus ** p < 1),
                      "constant-weight obstruction for epsilon=1")
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print a JSON result")
    args = parser.parse_args()
    checks = [check_indices_and_conjugacy, check_bounded_distortion, check_perturbation,
              check_tail_examples]
    for test in checks:
        test()
    result = {"status": "passed", "arithmetic": "exact rational, including complex components",
              "checks": [test.__name__ for test in checks],
              "scope": "Finite sanity checks only; not machine verification of the theorem."}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("PASS: all four groups of exact finite sanity checks.")
        print(result["scope"])


if __name__ == "__main__":
    main()
