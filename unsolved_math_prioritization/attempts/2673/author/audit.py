#!/usr/bin/env python3
"""Exact arithmetic safeguards, not a proof of universal knot quantifiers."""
import argparse
from fractions import Fraction
import hashlib
import json
from math import gcd, isqrt
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def factor(n):
    require(type(n) is int and n >= 1, "positive integer required")
    out = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def prime_power_or_one(n):
    return len(factor(n)) <= 1


def power_of_two(n):
    return n > 0 and n & (n - 1) == 0


def four_odd_prime_power(n):
    if n % 4:
        return False
    fs = factor(n // 4)
    return len(fs) == 1 and next(iter(fs)) != 2


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def divide_monic(a, b):
    a = list(a)
    require(b[-1] == 1, "divisor must be monic")
    q = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and a != [0]:
        c, d = a[-1], len(a) - len(b)
        q[d] += c
        for i, v in enumerate(b):
            a[d + i] -= c * v
        trim(a)
    require(a == [0], "polynomial division was not exact")
    return trim(q)


def cyclotomics(limit):
    polys = {}
    for n in range(1, limit + 1):
        p = [-1] + [0] * (n - 1) + [1]
        for d in divisors(n)[:-1]:
            p = divide_monic(p, polys[d])
        polys[n] = p
    return polys


def evaluate(poly, x):
    v = 0
    for c in reversed(poly):
        v = v * x + c
    return v


def slope(obj):
    require(type(obj) is dict and set(obj) == {"p", "q"}, "exactly p and q required")
    p, q = obj["p"], obj["q"]
    require(type(p) is int and type(q) is int, "integer numerator and denominator required")
    require(p != 0 and q > 0, "nonzero numerator and positive denominator required")
    require(abs(p) <= 100000 and q <= 100000, "input exceeds audit limit")
    require(gcd(abs(p), q) == 1, "slope must already be reduced")
    return p, q


def trefoil_witness(p, q):
    """alpha/pi as a Fraction, or None, from exact filling congruences."""
    m = p - 6 * q
    if m == 0:
        return None
    d = abs(m)
    for k in range(d + 1):
        alpha = Fraction(k, d)
        if Fraction(1, 6) < alpha < Fraction(5, 6):
            phase = m * alpha + q
            if phase.denominator == 1 and phase.numerator % 2 == 0:
                return alpha
    return None


def torus_obstruction(p, q):
    """One positive torus-knot obstruction for abs(p)/q, using imported SZ."""
    p = abs(p)
    upper = p // q + 2
    for a in range(2, isqrt(upper) + 1):
        for b in range(a + 1, upper // a + 1):
            if gcd(a, b) != 1:
                continue
            distance = abs(p - a * b * q)
            if distance == 1 or (distance == 0 and a == 2):
                return [a, b]
    return None


def classify(obj):
    p, q = slope(obj)
    n, r = abs(p), Fraction(abs(p), q)
    automatic_nd = prime_power_or_one(n // gcd(n, 2))
    published = (r <= 2 or (r < 5 and automatic_nd)
                 or (r < 7 and (power_of_two(n) or four_odd_prime_power(n))))
    forbidden = torus_obstruction(p, q)
    preprint = r <= 8 and (automatic_nd or four_odd_prime_power(n)) and forbidden is None
    require(not (published and forbidden), "contradictory positive and negative classifications")
    return {"p": p, "q": q, "published_input_corollary": published,
            "conditional_preprint_corollary": preprint,
            "torus_obstruction": forbidden,
            "unresolved_by_this_audit": not published and forbidden is None,
            "meaning": "partial sufficient tests; never a complete classification"}


def strict_json(s):
    def pairs(kvs):
        d = {}
        for k, v in kvs:
            require(k not in d, "duplicate JSON key")
            d[k] = v
        return d
    return json.loads(s, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError("nonfinite JSON")))


def self_test():
    polys = cyclotomics(128)
    cyclo_checks = 0
    for n, poly in polys.items():
        fs = factor(n)
        expected = 0 if n == 1 else (next(iter(fs)) if len(fs) == 1 else 1)
        require(evaluate(poly, 1) == expected, "cyclotomic value at 1 mismatch")
        cyclo_checks += 1
        if n > 2 and n % 2 == 0 and len(factor(n // 2)) == 1 and n // 2 % 2:
            prime = next(iter(factor(n // 2)))
            require(evaluate(poly, -1) == prime, "twice-odd-prime-power evaluation mismatch")
            cyclo_checks += 1
    require(polys[12] == [1, 0, -1, 0, 1], "Phi12 mismatch")
    require(polys[15] == [1, -1, 0, 1, -1, 1, 0, -1, 1], "Phi15 mismatch")
    for d in [12, 15]:
        require(evaluate(polys[d], 1) == evaluate(polys[d], -1) == 1, "residual obstruction mismatch")

    arithmetic_checks = 0
    for p in range(1, 1025):
        if four_odd_prime_power(p):
            ell = next(iter(factor(p // 4)))
            for d in divisors(p // 2):
                if d == 1 or prime_power_or_one(d):
                    continue
                fs = factor(d // 2)
                require(d % 2 == 0 and len(fs) == 1 and ell in fs,
                        "unaccounted cyclotomic order")
                arithmetic_checks += 1

    trefoil_checks = 0
    slope_checks = 0
    positive_count = 0
    forbidden_count = 0
    for p in range(-120, 121):
        if p == 0:
            continue
        for q in range(1, 41):
            if gcd(abs(p), q) != 1:
                continue
            witness = trefoil_witness(p, q)
            require((witness is not None) == (abs(p - 6 * q) >= 2), "trefoil iff mismatch")
            if witness is not None:
                phase = (p - 6 * q) * witness + q
                require(Fraction(1, 6) < witness < Fraction(5, 6), "endpoint representation")
                require(phase.denominator == 1 and phase.numerator % 2 == 0, "filling failure")
            trefoil_checks += 1
            result = classify({"p": p, "q": q})
            mirror = classify({"p": -p, "q": q})
            for key in ["published_input_corollary", "conditional_preprint_corollary", "torus_obstruction"]:
                require(result[key] == mirror[key], "mirror asymmetry")
            slope_checks += 1
            positive_count += result["published_input_corollary"]
            forbidden_count += result["torus_obstruction"] is not None

    dets = [abs(sum(c * ((-1) ** i) for i, c in enumerate(poly))) for poly in
            [[1, -1, 1, -1, 1], [1, -1, 1, -1, 1, -1, 1], [1, -1, 0, 1, 0, -1, 1]]]
    require(dets == [5, 7, 3], "low-genus determinant mismatch")
    for p, q in [(12, 5), (20, 3), (28, 5), (36, 7)]:
        require(classify({"p": p, "q": q})["published_input_corollary"], "Theorem A example failed")
    for p, q in [(15, 4), (24, 5)]:
        require(classify({"p": p, "q": q})["unresolved_by_this_audit"], "residual case misclassified")
    density_checks = 0
    for n in range(3, 101, 2):
        p, q = 6 * n + 2, n
        require(gcd(p, q) == 1, "density slope not reduced")
        require(trefoil_witness(p, q) == Fraction(1, 2), "density witness mismatch")
        require(trefoil_witness(6 * n + 1, n) is None, "density forbidden family mismatch")
        density_checks += 1
    require(trefoil_witness(6, 1) is None, "limit slope incorrectly accepted")
    return {"status": "passed", "scope": "finite arithmetic safeguards only",
            "cyclotomic_checks": cyclo_checks, "numerator_divisor_checks": arithmetic_checks,
            "trefoil_checks": trefoil_checks, "slope_checks": slope_checks,
            "published_positive_in_grid": positive_count, "torus_obstructions_in_grid": forbidden_count,
            "low_genus_determinants": dets, "density_sequence_checks": density_checks}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slope-json")
    args = ap.parse_args()
    try:
        result = classify(strict_json(args.slope_json)) if args.slope_json is not None else self_test()
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as e:
        print("REJECTED: " + str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
