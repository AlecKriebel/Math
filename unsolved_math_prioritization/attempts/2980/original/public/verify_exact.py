#!/usr/bin/env python3
"""Exact auxiliary checks for KP-4.104. No geometric classification is asserted.

Python standard library only. Prints JSON; writes only with explicit --output.
Every validation remains active under python -O and -OO.
"""
import argparse
from fractions import Fraction
from functools import reduce
from itertools import combinations, permutations
import json
from math import gcd
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def inverse(word):
    return tuple(-x for x in reversed(word))


def free_reduce(word):
    result = []
    for letter in word:
        if result and result[-1] == -letter:
            result.pop()
        else:
            result.append(letter)
    return tuple(result)


def apply(automorphism, word):
    result = ()
    for letter in word:
        image = automorphism[abs(letter) - 1]
        result = free_reduce(result + (image if letter > 0 else inverse(image)))
    return result


def compose(left, right):
    return tuple(apply(left, word) for word in right)


def braid_generator(i, sign):
    result = [(1,), (2,), (3,)]
    if sign == 1:
        result[i - 1] = (i, i + 1, -i)
        result[i] = (i,)
    else:
        result[i - 1] = (i + 1,)
        result[i] = (-(i + 1), i, i + 1)
    return tuple(result)


def artin(word):
    result = ((1,), (2,), (3,))
    for letter in word:
        result = compose(result, braid_generator(abs(letter), 1 if letter > 0 else -1))
    return result


def conjugate(g, word):
    return g + word + inverse(g)


def determinant(matrix):
    n = len(matrix)
    total = 0
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = (-1) ** inversions
        for i in range(n):
            term *= matrix[i][p[i]]
        total += term
    return total


def determinantal_divisors(matrix):
    divisors = []
    for size in range(1, min(len(matrix), len(matrix[0])) + 1):
        minors = [determinant([[matrix[r][c] for c in cols] for r in rows])
                  for rows in combinations(range(len(matrix)), size)
                  for cols in combinations(range(len(matrix[0])), size)]
        divisors.append(reduce(gcd, minors, 0))
    return divisors


def pfaffian(coeffs):
    a, b, c, d, e, f = coeffs
    return a * f - b * e + c * d


def compute():
    identity = ((1,), (2,), (3,))
    for i in (1, 2):
        require(artin((i, -i)) == identity, "Artin generator inverse failed")
    require(artin((1, 2, 1)) == artin((2, 1, 2)), "Braid relation failed")
    require(artin((1,)) != artin((2,)), "Representation sanity check failed")

    a, b = (1,), (2,)
    p = (a, conjugate((1, 2, 2), a))
    q = (conjugate((1, 1), b), b)
    g = (1, -2, -1)
    z = (1, 2) * 3
    w = (1, 1, 2, 2) * 2
    beta = w + inverse(z)
    require(artin(p[0] + p[1]) == artin(beta), "First product differs from beta")
    require(artin(q[0] + q[1]) == artin(beta), "Second product differs from beta")
    for i in range(2):
        require(artin(conjugate(g, p[i])) == artin(q[i]), "Simultaneous conjugation failed")
        require(sum(1 if x > 0 else -1 for x in p[i]) == 1, "Factor exponent wrong")
    require(artin(conjugate(g, beta)) == artin(beta), "Conjugator does not centralize product")

    smith_samples = []
    for n in range(-100, 101):
        matrix = [[1, 2, 1], [0, 0, 1], [-1, -2, 1], [0, -n, 1]]
        got = determinantal_divisors(matrix)
        require(got == [1, 1, abs(n)], "Determinantal-divisor mismatch at n=" + str(n))
        if n in (-5, -3, -1, 0, 1, 2, 3, 4, 5, 99):
            smith_samples.append({"n": n, "determinantal_divisors": got,
                                  "H1": "Z" if n == 0 else "Z/" + str(abs(n))})
    require(determinantal_divisors([[1, -1], [0, -2]]) == [1, 2], "P lift H1 failed")
    require(determinantal_divisors([[2, 0], [1, 1]]) == [1, 2], "Q lift H1 failed")

    omega0 = (1, 0, 0, 0, 0, 1)
    omega1 = (1, 2, 0, 0, -2, -3)
    pf_samples = []
    for t in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)):
        form = tuple((1 - t) * x + t * y for x, y in zip(omega0, omega1))
        got = pfaffian(form)
        require(got == (1 - 2 * t) ** 2, "Pfaffian identity failed")
        require(form[0] == 1, "Positivity on distinguished plane failed")
        pf_samples.append({"t": str(t), "pfaffian": str(got)})
    require(pfaffian(omega0) == pfaffian(omega1) == 1, "Endpoint nondegeneracy failed")

    degree_samples = []
    for d in range(1, 51):
        genus = (d - 1) * (d - 2) // 2
        chi = 2 - 2 * genus - d
        branches = d * (d - 1)
        require(chi == d - branches == d * (2 - d), "Capping Euler characteristic failed")
        require(2 * genus - 2 == d * d - 3 * d, "Adjunction failed")
        require(2 - 2 * (genus + 1) != 3 * d - d * d, "Stabilization unexpectedly satisfies adjunction")
        if d in (1, 2, 3, 4, 17, 18):
            degree_samples.append({"degree": d, "capped_genus": genus,
                                   "boundary_components": d, "filling_chi": chi,
                                   "full_twist_bands": branches})

    return {
        "status": "PASS",
        "scope": "Auxiliary exact algebra only; no solution of KP-4.104 or geometric isotopy algorithm.",
        "braid_pair": {"P": p, "Q": q, "conjugator": g,
                       "common_product": beta,
                       "simultaneously_conjugate": True,
                       "same_product_verified_by_Artin_action": True,
                       "double_cover_H1_both": "Z/2"},
        "cover_homology": {"integer_parameters_checked": [-100, 100], "samples": smith_samples,
                           "universal_proof": "Eliminate b=0 and a=-2c; the sole remaining relation is n*c=0."},
        "forms": {"coefficient_order": ["12", "13", "14", "23", "24", "34"],
                  "omega0": omega0, "omega1": omega1,
                  "pfaffian_polynomial_in_t": [1, -4, 4], "samples": pf_samples},
        "capping": {"degrees_checked": [1, 50], "samples": degree_samples},
        "limitations": ["Finite checks do not prove a universal theorem; the report provides algebraic proofs.",
                        "No smooth isotopy, complex isotopy, or symplectic non-isotopy is inferred from equal invariants."]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Explicit destination for JSON; otherwise stdout only")
    args = parser.parse_args()
    data = json.dumps(compute(), indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(data, end="")
    else:
        args.output.write_text(data, encoding="utf-8")


if __name__ == "__main__":
    main()
