#!/usr/bin/env python3
"""Exact finite diagnostics for the note; Python 3.9+, standard library only.

These tests do not prove infinitude, an asymptotic prime mean, or atomlessness.
No assert statements are used, so Python -O cannot disable the checks.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from math import gcd, isqrt


def factors(n):
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def phi(n):
    ans = n
    for q in factors(n):
        ans = ans // q * (q - 1)
    return ans


def mobius(n):
    qs = factors(n)
    if any(n % (q * q) == 0 for q in qs):
        return 0
    return (-1) ** len(qs)


def primes_to(n):
    return [p for p in range(2, n + 1)
            if all(p % d for d in range(2, isqrt(p) + 1))]


def order(a, p):
    d = p - 1
    for q in factors(d):
        while d % q == 0 and pow(a, d // q, p) == 1:
            d //= q
    return d


def clipped(t):
    return max(F(0), min(F(1), 2 * t - 1))


def calculate():
    checks = 0

    def require(test, message):
        nonlocal checks
        checks += 1
        if not test:
            raise RuntimeError(message)

    rows = []
    graph_primes = []
    graph_points = 0
    admissible = [p for p in primes_to(1000) if p % 4 == 3]
    thresholds = [F(0), F(1, 4), F(1, 2), F(3, 4), F(7, 8), F(1)]
    for p in admissible:
        n = p - 1
        ds = [d for d in range(1, n + 1) if n % d == 0]
        multipliers = [(u * u + 1) % p for u in range(p)]
        require(0 not in multipliers, "vanishing multiplier on admissible prime")
        orders = [order(a, p) for a in multipliers]
        for a, d in zip(multipliers, orders):
            require(n % d == 0 and pow(a, d, p) == 1, "invalid fiber order")
            for q in factors(d):
                require(pow(a, d // q, p) != 1, "fiber order not minimal")
        primitive = orders.count(n)
        theta = F(phi(n), n)
        w = 2 ** len(factors(n))
        require((F(primitive, p) - theta) ** 2 * p <= theta ** 2 * (w - 1) ** 2,
                "primitive-value character estimate failed")
        require(w ** 4 <= 64 ** 4 * n, "squarefree-divisor crude bound failed")
        histogram = Counter({1: p})
        for d in orders:
            histogram[d] += p - 1
        require(sum(histogram.values()) == p * p, "point mass not normalized")
        require(histogram[1] == 2 * p - 1, "fixed-point count failed")
        for x in thresholds + [F(p - 1, p)]:
            cdf = F(sum(v for d, v in histogram.items() if F(d, p) <= x), p * p)
            if F(1, 2) <= x < 1 and p * (1 - x) > 1:
                require(cdf == 1 - F((p - 1) * primitive, p * p),
                        "eventual point CDF formula failed")
            if x in (0, 1, F(p - 1, p)):
                require(cdf == (0 if x == 0 else 1), "CDF endpoint failed")
        moment = sum(F(v, p * p) * clipped(F(d, p)) for d, v in histogram.items())
        require(moment == F((p - 2) * (p - 1) * primitive, p ** 3),
                "continuous-test moment failed")
        roots = {}
        for d in ds:
            roots[d] = sum(pow(a, d, p) == 1 for a in multipliers)
            subgroup = [a for a in range(1, p) if pow(a, d, p) == 1]
            require(len(subgroup) == d, "subgroup cardinality failed")
            eta_sum = 0
            for a in subgroup:
                b = (a - 1) % p
                eta_sum += 0 if b == 0 else (1 if pow(b, n // 2, p) == 1 else -1)
            require(roots[d] == d + eta_sum, "quadratic preimage formula failed")
            count_fixed = sum(v for e, v in histogram.items() if d % e == 0)
            require(count_fixed == p + (p - 1) * roots[d], "iterate fixed points failed")
        for d in ds:
            recovered = sum(mobius(d // e) * roots[e] for e in ds if d % e == 0)
            require(recovered == orders.count(d), "Mobius order recovery failed")

        if p <= 47:
            graph_primes.append(p)
            image = {}
            for u in range(p):
                for v in range(p):
                    image[(u, v)] = (u, (u * u + 1) * v % p)
            require(len(set(image.values())) == p * p, "orbit graph not a permutation")
            seen = set()
            graph_hist = Counter()
            for z in image:
                if z in seen:
                    continue
                path = []
                local = set()
                t = z
                while t not in local and t not in seen:
                    path.append(t)
                    local.add(t)
                    t = image[t]
                require(t == z, "transient or merged affine orbit")
                length = len(path)
                for u, v in path:
                    require(length == (1 if v == 0 else orders[u]),
                            "raw orbit disagrees with fiber order")
                seen.update(path)
                graph_hist[length] += length
            require(len(seen) == p * p and graph_hist == histogram,
                    "raw orbit histogram failed")
            graph_points += len(seen)
        rows.append({"p": p, "primitive_parameters": primitive,
                     "theta": str(theta), "moment": str(moment),
                     "cdf_three_quarters": str(F(sum(v for d, v in histogram.items()
                                                       if 4 * d <= 3 * p), p * p))})

    bad = [5, 13, 17, 29, 37, 41]
    for p in bad:
        zeros = [u for u in range(p) if (u * u + 1) % p == 0]
        require(len(zeros) == 2, "bad-prime roots missing")
        for u in zeros:
            require((u, (u * u + 1) * 0 % p) == (u, (u * u + 1) * 1 % p),
                    "bad-prime collision absent")
    # At p=3,x=3/4 the eventual condition fails and every point is counted.
    first = rows[0]
    require(first["p"] == 3 and first["cdf_three_quarters"] == "1",
            "small-prime moving-boundary control failed")
    # The elementary coefficient-series bound used in the analytic proof.
    for n in range(1, 10001):
        require(2 * phi(n) ** 2 >= n, "totient lower bound failed")
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return {"status": "PASS", "scope": "Exact finite diagnostics only; not an asymptotic proof",
            "admissible_prime_bound": 1000, "admissible_primes": len(admissible),
            "raw_graph_primes": graph_primes, "raw_graph_points": graph_points,
            "bad_reduction_primes": bad, "totient_bound_maximum": 10000,
            "exact_checks": checks, "prime_rows_sha256": hashlib.sha256(encoded).hexdigest(),
            "prime_rows": rows}


if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2, sort_keys=True))
