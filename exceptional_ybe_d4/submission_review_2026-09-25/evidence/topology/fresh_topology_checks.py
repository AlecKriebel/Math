#!/usr/bin/env python3
"""Independent, exact, standard-library-only checks of Section 9.

This does not import any project verifier.  Two separately encoded computations:
  (1) coefficient of I in the literal GR Pauli braid, times 2**n;
  (2) unreduced Burau over F4 at t satisfying t*t+t+1=0.
For the all-meridians-to-1 triple branched cover, the latter's proposed mod-2
first Betti number is 2*(nullity(B(t)-I)-1); see topology.md for scope/proof.
The Pauli expansion here is exponential in n: this is an audit, NOT the claimed
polynomial-time algorithm.  All coefficient and field arithmetic is exact.
"""
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random


def rotate(z, p):
    a, b = z
    return ((a, b), (-b, a), (-a, -b), (b, -a))[p % 4]


def local_terms(i):
    # Site i starts at qubit 2*(i-1). A Pauli is i**p X**x Z**z.
    s = 2*(i-1)
    z = (1 << (s+1)) | (1 << (s+2))  # I Z Z I
    x = (1 << s) | (1 << (s+2)) | (1 << (s+3))  # X I X X
    return ((0, 0, 0), (0, z, 1), (x, 0, 1), (x, z, 0))


def pauli_braid(word):
    poly = {(0, 0): (1, 0)}
    denominator_power = 0
    for g in word:
        nxt = {}
        for (x, z), a in poly.items():
            for j, (y, w, p) in enumerate(local_terms(abs(g))):
                # r0^-1 = (I-U-V-UV)/2.
                p += (2 if g < 0 and j else 0) + 2*((z & y).bit_count() % 2)
                c = rotate(a, p)
                label = (x ^ y, z ^ w)
                old = nxt.get(label, (0, 0))
                nxt[label] = (old[0]+c[0], old[1]+c[1])
        poly = {k: v for k, v in nxt.items() if v != (0, 0)}
        denominator_power += 1
        while denominator_power and all(a % 2 == b % 2 == 0 for a, b in poly.values()):
            poly = {k: (a//2, b//2) for k, (a, b) in poly.items()}
            denominator_power -= 1
    return poly, denominator_power


def trace_value(n, word):
    poly, k = pauli_braid(word)
    a, b = poly.get((0, 0), (0, 0))
    assert b == 0, (n, word, a, b)
    value = Fraction(a * (2**n), 2**k)
    assert value.denominator == 1, (n, word, value)
    return value.numerator


def fmul(a, b):
    # F4 = F2[t]/(t^2+t+1), integers encode polynomial coefficient bits.
    c = 0
    for j in range(2):
        if b & (1 << j):
            c ^= a << j
    if c & 4:
        c ^= 7
    return c


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def burau(n, word):
    a = identity(n)
    for g in word:
        i = abs(g)-1
        block = ((3, 2), (1, 0)) if g > 0 else ((0, 1), (3, 2))
        for row in a:
            x, y = row[i:i+2]
            row[i] = fmul(x, block[0][0]) ^ fmul(y, block[1][0])
            row[i+1] = fmul(x, block[0][1]) ^ fmul(y, block[1][1])
    return a


def rank(a):
    a = [row[:] for row in a]
    r = 0
    for c in range(len(a[0])):
        pivot = next((j for j in range(r, len(a)) if a[j][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = (0, 1, 3, 2)[a[r][c]]
        a[r] = [fmul(inv, x) for x in a[r]]
        for j in range(len(a)):
            if j != r and a[j][c]:
                z = a[j][c]
                a[j] = [x ^ fmul(z, y) for x, y in zip(a[j], a[r])]
        r += 1
    return r


def components(n, word):
    p = list(range(n))
    for g in word:
        i = abs(g)-1
        p[i], p[i+1] = p[i+1], p[i]
    seen = set()
    c = 0
    for i in range(n):
        if i in seen:
            continue
        c += 1
        while i not in seen:
            seen.add(i)
            i = p[i]
    return c


def cover_data(n, word):
    a = burau(n, word)
    for i in range(n):
        a[i][i] ^= 1
    d = 2*(n-rank(a)-1)
    assert d >= 0 and d % 2 == 0
    c = components(n, word)
    return c, d, 2*((-1)**(c-1))*((-2)**(d//2))


def inverse(word):
    return [-x for x in reversed(word)]


def check_case(n, word):
    actual = trace_value(n, word)
    c, d, expected = cover_data(n, word)
    assert actual == expected, (n, word, actual, expected, c, d)
    return {"n": n, "word": word, "components": c, "d2": d, "J": actual}


def main():
    rng = random.Random(20260925)
    cases = []
    examples = [(1, []), (2, []), (2, [1,1]), (2, [-1,-1]),
                (2, [1,1,1]), (2, [-1,-1,-1]),
                (3, [1,-2]*2), (3, [1,-2]*3)]
    for n, word in examples:
        cases.append(check_case(n, word))
    example_results = cases[:]
    for n in range(1, 8):
        cases.append(check_case(n, []))
    for m in range(-30, 31):
        cases.append(check_case(2, ([1] if m >= 0 else [-1])*abs(m)))
    for n in range(2, 7):
        for _ in range(55):
            length = rng.randrange(0, 45)
            word = [rng.choice((-1,1))*rng.randrange(1,n) for _ in range(length)]
            cases.append(check_case(n, word))
    # Markov stabilization (both signs), reflection, mirror, and split unknot.
    for n in range(2, 6):
        for _ in range(8):
            word = [rng.choice((-1,1))*rng.randrange(1,n) for _ in range(16)]
            base = check_case(n, word)
            for variant_n, variant, factor in (
                (n+1, word+[n], 1), (n+1, word+[-n], 1),
                (n, [(n-abs(g))*(1 if g > 0 else -1) for g in word], 1),
                (n, [-g for g in word], 1), (n+1, word, 2)):
                result = check_case(variant_n, variant)
                assert result["J"] == factor*base["J"]
                cases.append(result)
    # Garside D r_i D^-1 = r_(n-i); kappa cancels in the conjugation.
    garside_count = 0
    for n in range(2, 8):
        delta = [g for end in range(n-1, 0, -1) for g in range(1, end+1)]
        for i in range(1,n):
            assert pauli_braid(delta+[i]+inverse(delta)) == pauli_braid([n-i])
            garside_count += 1
    # Injectivity of all normal-monomial Pauli labels by binary rank, n<=100.
    for n in range(2,101):
        vectors = []
        for i in range(1,n):
            for x,z,_ in local_terms(i)[1:3]:
                vectors.append(x | (z << (2*n)))
        pivots = {}
        for v in vectors:
            while v:
                h = v.bit_length()-1
                if h in pivots:
                    v ^= pivots[h]
                else:
                    pivots[h] = v
                    break
            assert v != 0, n
        assert len(pivots) == 2*n-2
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "check_scope": "fresh exact Pauli traces, F4 Burau cover homology, and Garside conjugacy",
        "random_seed": 20260925,
        "trace_vs_cover_cases": len(cases),
        "garside_generator_checks": garside_count,
        "normal_monomial_label_injectivity_n_range": [2,100],
        "all_passed": True,
        "example_results": example_results,
        "case_digest_sha256": hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "caution": "Bounded tests are evidence, not a replacement for the all-n proofs; the trace expansion used here is exponential in n."
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
