#!/usr/bin/env python3
"""Exact checks for Turns 1--3. Python standard library only.

The all-n and all-jet proofs are in the written turns. This checks their
algebraic certificates and small controls, not an infinite topology claim.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import permutations
from math import gcd, factorial
import json


def clean(f):
    return {e: Q(c) for e, c in f.items() if c}


def add(*fs):
    out = defaultdict(Q)
    for f in fs:
        for e, c in f.items():
            out[e] += c
    return clean(out)


def scale(c, f):
    return clean({e: c * a for e, a in f.items()})


def mul(f, g):
    out = defaultdict(Q)
    for (a, b), c in f.items():
        for (d, e), h in g.items():
            out[a + d, b + e] += c * h
    return clean(out)


ONE = {(0, 0): Q(1)}
X, Y, Z = {(1, 0): Q(1)}, {(0, 1): Q(1)}, {(-1, -1): Q(1)}


def power(f, n):
    assert n >= 0
    out = ONE
    for _ in range(n):
        out = mul(out, f)
    return out


def orbit(a, b):
    exps = {(s * (p[0] - p[2]), s * (p[1] - p[2]))
            for p in permutations((a, b, 0)) for s in (-1, 1)}
    return {e: Q(1) for e in exps}


def specialize(f):
    out = defaultdict(Q)
    for (a, b), c in f.items():
        out[a] += c
    return {a: c for a, c in out.items() if c}


def residue(f, n):
    return sum(c for (a, b), c in f.items() if a % n == b % n == 0)


def evaluate(f, x, y):
    return sum(c * Q(x) ** a * Q(y) ** b for (a, b), c in f.items())


def dilation(f, p):
    return {(p * a, p * b): c for (a, b), c in f.items()}


def jet(f, J):
    return {(i, j): sum(c * a ** i * b ** j for (a, b), c in f.items())
            / (factorial(i) * factorial(j))
            for i in range(J + 1) for j in range(J + 1 - i)}


def main():
    checks = 0

    def check(b):
        nonlocal checks
        assert b
        checks += 1

    a = add(X, Y, Z)
    b = add(mul(X, Y), mul(X, Z), mul(Y, Z))
    u, v = add(a, b), mul(a, b)
    D = add(power(u, 2), scale(-4, v))
    Dprod = mul(mul(power(add(X, scale(-1, ONE)), 2),
                    power(add(Y, scale(-1, ONE)), 2)),
                power(add(Z, scale(-1, ONE)), 2))
    check(D == Dprod)
    check(not specialize(D))
    check(evaluate(D, 2, 3) == Q(25, 9))
    check(all(c == 0 for c in jet(D, 5).values()))
    check(jet(D, 6)[2, 4] == 1)
    check(jet(D, 6)[3, 3] == 2)
    check(jet(D, 6)[4, 2] == 1)

    F = add(orbit(1, 0), scale(-1, orbit(2, 1)))
    check(bool(F))
    check(F[2, 1] == -1)
    check(all(gcd(abs(i), abs(j)) == 1 for i, j in F))
    check(sum(F.values()) == 0)
    for n in range(1, 21):
        check(residue(F, n) == 0)

    H = add(scale(2, orbit(2, 1)), scale(-2, orbit(3, 1)),
            orbit(4, 1), scale(-1, orbit(5, 1)), orbit(5, 2))
    factored = scale(-1, mul(mul(D, add(u, scale(2, ONE))),
                            add(v, scale(2, u), scale(-3, ONE))))
    check(H == factored)
    check(len(H) == 54)
    check(H[5, 1] == -1)
    check(not specialize(H))
    check(evaluate(H, 2, 3) == Q(-354725, 162))
    check(all(gcd(abs(i), abs(j)) == 1 for i, j in H))
    check(sum(H.values()) == 0)
    for n in range(1, 31):
        check(residue(H, n) == 0)
    for p in range(1, 9):
        Hp = dilation(H, p)
        check(not specialize(Hp))
        check(all(gcd(abs(i), abs(j)) == p for i, j in Hp))
        for n in range(1, 31):
            check(residue(Hp, n) == 0)

    for J in range(0, 13):
        L = J // 2 + 2
        coeffs = []
        for p in range(1, L + 1):
            den = 1
            for q in range(1, L + 1):
                if q != p:
                    den *= p * p - q * q
            coeffs.append(Q(1, den))
        HJ = add(*(scale(c, dilation(H, p))
                   for p, c in enumerate(coeffs, 1)))
        check(bool(HJ))
        check(not specialize(HJ))
        check(len(HJ) == 54 * L)
        for d in range(L - 1):
            check(sum(c * p ** (2 * d) for p, c in enumerate(coeffs, 1)) == 0)
        for c in jet(HJ, J).values():
            check(c == 0)
        for n in range(1, 21):
            check(residue(HJ, n) == 0)

    print(json.dumps({"status": "PASS", "exact_assertions": checks,
                      "joint_kernel_terms": len(H),
                      "joint_kernel_value_at_2_3": str(evaluate(H, 2, 3)),
                      "finite_jet_controls": list(range(13)),
                      "scope": "Laurent algebra, not knot realization or full target"},
                     indent=2))


if __name__ == "__main__":
    main()
