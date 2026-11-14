#!/usr/bin/env python3
"""Exact independent diagnostics, with no runtime third-party dependencies.

These checks validate finite identities and boundary conventions, not infinite
prime subsequences or historical novelty. Run from any directory.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json


def primes_through(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for n in range(2, int(limit**0.5) + 1):
        if sieve[n]:
            sieve[n*n:limit+1:n] = b"\x00" * ((limit-n*n)//n + 1)
    return [i for i, flag in enumerate(sieve) if flag]


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def mobius(n):
    sign = 1
    d = 2
    while d*d <= n:
        if n % d == 0:
            n //= d
            sign = -sign
            if n % d == 0:
                return 0
        while n % d == 0:
            n //= d
        d += 1
    return -sign if n > 1 else sign


def eta(a, p):
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1)//2, p)
    return -1 if value == p - 1 else 1


def order(a, p):
    value = 1
    for k in range(1, p):
        value = value*a % p
        if value == 1:
            return k
    raise AssertionError("nonzero element must have finite multiplicative order")


def full_graph_periods(p):
    universe = [(u, v) for u in range(p) for v in range(p)]
    forward = {(u, v): (u, (u*u + 1)*v % p) for u, v in universe}
    assert len(set(forward.values())) == p*p
    periods = {}
    cycles = 0
    for start in universe:
        if start in periods:
            continue
        walk = []
        z = start
        while z not in walk:
            assert z not in periods
            walk.append(z)
            z = forward[z]
        assert z == start
        cycles += 1
        for z in walk:
            periods[z] = len(walk)
    return periods, cycles


def continuous_test(period, p):
    t = Fraction(period, p)
    return max(Fraction(0), min(Fraction(1), 2*t - 1))


def check_prime(p, graph=False):
    assert p % 4 == 3
    n = p - 1
    orders = [order((u*u + 1) % p, p) for u in range(p)]
    multiplicities = Counter(orders)
    primitive = multiplicities[n]
    assert primitive % 2 == 0
    assert multiplicities[1] == 1
    point_period_counts = Counter({1: p})
    for k, count in multiplicities.items():
        point_period_counts[k] += n*count
    assert sum(point_period_counts.values()) == p*p
    assert point_period_counts[1] == 2*p - 1

    ds = divisors(n)
    roots = {d: sum(pow((u*u + 1) % p, d, p) == 1
                    for u in range(p)) for d in ds}
    for d in ds:
        geometric = d + sum(eta(a - 1, p) for a in range(1, p)
                            if pow(a, d, p) == 1)
        assert roots[d] == geometric
        recovered = sum(mobius(d//e)*roots[e] for e in divisors(d))
        assert recovered == multiplicities[d]
    assert roots[n] == p

    for x in [Fraction(1, 2), Fraction(3, 4), Fraction(9, 10)]:
        direct = Fraction(sum(count for k, count in point_period_counts.items()
                              if k <= p*x), p*p)
        if n > p*x:
            assert direct == 1 - Fraction(n*primitive, p*p)
    assert Fraction(sum(count for k, count in point_period_counts.items()
                        if k <= n), p*p) == 1
    assert Fraction(sum(count for k, count in point_period_counts.items()
                        if k <= p), p*p) == 1
    assert sum(count for k, count in point_period_counts.items() if k <= 0) == 0
    moment = sum(count*continuous_test(k, p)
                 for k, count in point_period_counts.items()) / (p*p)
    assert moment == Fraction((p - 2)*(p - 1)*primitive, p**3)
    expected_cycles = p + sum(Fraction(n*count, k)
                              for k, count in multiplicities.items())
    assert expected_cycles.denominator == 1
    if graph:
        periods, cycles = full_graph_periods(p)
        assert Counter(periods.values()) == point_period_counts
        assert cycles == expected_cycles
        for (u, v), period in periods.items():
            assert period == (1 if v == 0 else orders[u])
    return {"p": p, "primitive_parameters": primitive,
            "D_half_exact": str(1 - Fraction(n*primitive, p*p)),
            "bounded_continuous_moment_exact": str(moment),
            "periodic_points": p*p, "fixed_points": 2*p - 1,
            "full_graph_checked": graph}


def main():
    out = Path(__file__).resolve().parent
    original = out.parents[1] / "original" / "PROOF.md"
    proof_hash = sha256(original.read_bytes()).hexdigest()
    assert proof_hash == "ba5fc8850a665da5130e3791fb49015c998ed0eee317576712ad3b66bc228c05"
    rows = [check_prime(p, graph=p <= 47)
            for p in primes_through(1000) if p % 4 == 3]
    negative_controls = []
    for p in [5, 13, 17, 29, 37, 41]:
        images = {(u, (u*u + 1)*v % p)
                  for u in range(p) for v in range(p)}
        roots = [u for u in range(p) if (u*u + 1) % p == 0]
        assert len(roots) == 2
        assert len(images) == p*p - 2*(p - 1)
        negative_controls.append({"p": p, "exceptional_lines": 2,
                                  "image_cardinality": len(images),
                                  "is_permutation": False})
    result = {"status": "PASS", "head": "091bdecef6f84154f5d5c205a4b07eeb6391b8f8",
              "proof_sha256": proof_hash,
              "description": "Exact finite identities, raw orbit graph controls, geometric fixed-point counts, Mobius recovery, endpoints, and continuous weak-limit diagnostic.",
              "prime_count": len(rows), "rows": rows,
              "negative_controls": negative_controls,
              "limit_claims_empirically_certified": False}
    (out / "DIAGNOSTICS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "prime_count": len(rows),
                      "full_graph_prime_count": sum(row["full_graph_checked"] for row in rows),
                      "negative_controls": len(negative_controls)}))


if __name__ == "__main__":
    main()
