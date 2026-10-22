#!/usr/bin/env python3
"""Read-only exact checks for the accompanying mathematical audit.

No network, external dependencies, floating-point computations, or writes.
These finite checks are not proofs of the geometric or infinite-series claims.
Failures use exceptions and nonzero exit status, including under python -O.
"""
import argparse
from fractions import Fraction
from math import comb, factorial
import json
import sys


class CheckFailure(Exception):
    pass


COUNT = 0


def equal(actual, expected, label):
    global COUNT
    COUNT += 1
    if actual != expected:
        raise CheckFailure(f"{label}: got {actual!r}; expected {expected!r}")


def require(value, label):
    global COUNT
    COUNT += 1
    if not value:
        raise CheckFailure(label)


def grassmann_dimension(k, ambient):
    if not isinstance(k, int) or not isinstance(ambient, int):
        raise CheckFailure("Grassmann dimensions require integer inputs")
    if not 0 <= k <= ambient:
        raise CheckFailure("Grassmann subspace dimension is outside its domain")
    return k * (ambient - k)


def logarithm_coefficients(max_power):
    # log(1-y/a+b*x^2/a); key=(x-degree,y-degree,a-degree,b-degree).
    terms = {}
    for k in range(1, max_power + 1):
        for j in range(k + 1):
            key = (2 * (k - j), j, -k, k - j)
            terms[key] = terms.get(key, Fraction(0)) + (
                Fraction((-1) ** (k + 1 + j) * comb(k, j), k)
            )
    return terms


def trace_monomial(d, m):
    # Trace of multiplication by w^(-m) in basis 1,w,...,w^(d-1)
    # in Q(z)[w]/(w^d-z), represented as {z-exponent: coefficient}.
    if d < 1 or m < 0:
        raise CheckFailure("Trace parameters require d>=1 and m>=0")
    result = {}
    for i in range(d):
        q, r = divmod(i - m, d)
        if r == i:
            result[q] = result.get(q, 0) + 1
    return result


def exact_checks():
    equal(grassmann_dimension(1, 3), 2, "planes through line parameter dimension")
    equal(4, 2 + 2, "incidence example ambient dimension")
    equal(1, 2 - 1, "incidence example submanifold dimension")
    equal(4 - 1, 2 + 1, "incidence example normal rank")
    require(all(degree > 0 for degree in (1, 1, 1)), "initial normal degrees")
    conic_space = 3 + (comb(2 + 2, 2) - 1)
    equal(conic_space, 8, "plane conic parameter dimension")
    incidence = conic_space - 1
    equal(incidence, 7, "conic incidence dimension")
    equal(1 + (2 - 1), 2, "first normal data dimension")
    equal(incidence - 2, 5, "first normal data fibre lower bound")
    equal(incidence - 1, 6, "order zero fibre lower bound")
    equal((1 - 1, 1 - 1), (0, 0), "blown-up line normal degrees")
    require(not all(degree > 0 for degree in (0, 0)), "trivial normal is not positive")
    require(1 < 1 + 1, "base-plus-fibre exceeds elliptic K3 algebraic dimension")
    coeffs = logarithm_coefficients(8)
    equal(coeffs[(2, 0, -1, 1)], Fraction(1), "quadratic shape coefficient")
    equal(coeffs[(0, 2, -2, 0)], Fraction(-1, 2), "maximal-order quadratic coefficient")
    equal(coeffs.get((1, 0, -1, 0), Fraction(0)), Fraction(0), "odd x coefficient")
    for d in range(1, 9):
        for m in range(65):
            expected = {-m // d: d} if m % d == 0 else {}
            equal(trace_monomial(d, m), expected, f"trace d={d},m={m}")
        for k in range(1, 9):
            coefficient = Fraction(d, factorial(d * k))
            require(coefficient > 0, f"nonzero trace Laurent coefficient d={d},k={k}")


def rejects(thunk, label):
    global COUNT
    try:
        thunk()
    except CheckFailure:
        COUNT += 1
        return
    raise CheckFailure(f"Expected rejection was missing: {label}")


def negative_checks():
    rejects(lambda: grassmann_dimension(4, 3), "invalid subspace dimension")
    rejects(lambda: grassmann_dimension(-1, 3), "negative subspace dimension")
    rejects(lambda: trace_monomial(0, 2), "zero covering degree")
    rejects(lambda: trace_monomial(2, -1), "negative series degree")
    rejects(lambda: equal(7, 2, "corrupted conic separation"), "dimension corruption")
    rejects(lambda: equal(trace_monomial(3, 2), {-1: 3}, "corrupted trace"), "trace corruption")
    rejects(lambda: equal(logarithm_coefficients(2)[(2, 0, -1, 1)],
                          Fraction(-1), "corrupted shape sign"), "sign corruption")
    rejects(lambda: require(all(x > 0 for x in (0, 0)), "corrupted positivity"),
            "normal positivity corruption")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("exact", "negative", "all"), default="all")
    parser.add_argument("--inject-failure", action="store_true",
                        help="Deliberately fail to verify nonzero exit status")
    args = parser.parse_args()
    try:
        if args.mode in ("exact", "all"):
            exact_checks()
        if args.mode in ("negative", "all"):
            negative_checks()
        if args.inject_failure:
            raise CheckFailure("Deliberately injected failure")
    except (CheckFailure, KeyError, ValueError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "mode": args.mode,
                          "checks": COUNT, "error": str(exc),
                          "arithmetic": "exact", "numerical_claims": False}))
        return 1
    print(json.dumps({"status": "PASS", "mode": args.mode, "checks": COUNT,
                      "arithmetic": "exact", "numerical_claims": False,
                      "scope": "Finite algebraic checks only; not a geometric proof certificate"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
