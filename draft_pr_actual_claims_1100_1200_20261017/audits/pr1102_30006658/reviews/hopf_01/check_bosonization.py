#!/usr/bin/env python3
"""Exact convention checks, NOT a proof of the infinite-dimensional theorem.

H is the free associative graded algebra on odd x,y and even t, each
primitive. It is an infinite-dimensional, noncommutative super Hopf algebra.
All checked operations are exact; word lengths are only test bounds and
are NEVER quotient relations or truncations of the tested operations.
Only the Python standard library is used.
"""

from itertools import product
from collections import defaultdict
import json

PARITY = {"x": 1, "y": 1, "t": 0}


def parity(word):
    return sum(PARITY[c] for c in word) % 2


def clean(d, p):
    return {k: v % p for k, v in d.items() if v % p}


def delta_h(word, p):
    # Build Delta multiplicatively in the SUPER tensor-product algebra.
    ans = {("", ""): 1}
    for c in word:
        nxt = defaultdict(int)
        for (a, b), q in ans.items():
            nxt[(a + c, b)] += q * (-1) ** (parity(b) * PARITY[c])
            nxt[(a, b + c)] += q
        ans = clean(nxt, p)
    return ans


def antipode_h(word):
    n = len(word)
    crossings = sum(PARITY[word[i]] * PARITY[word[j]]
                    for i in range(n) for j in range(i + 1, n))
    return word[::-1], (-1) ** (n + crossings)


def mul_b(u, v):
    h, i = u
    a, j = v
    return (h + a, (i + j) % 2), (-1) ** (i * parity(a))


def delta_b(u, p):
    h, i = u
    return {((a, (parity(b) + i) % 2), (b, i)): c
            for (a, b), c in delta_h(h, p).items()}


def antipode_b(u):
    h, i = u
    sh, c = antipode_h(h)
    k, d = mul_b(("", (i + parity(h)) % 2), (sh, 0))
    return k, c * d


def mul_tensor(u, v):
    a, c = mul_b(u[0], v[0])
    b, d = mul_b(u[1], v[1])
    return (a, b), c * d


def words(max_length):
    return ["".join(w) for n in range(max_length + 1)
            for w in product("xyt", repeat=n)]


def check(p):
    counts = defaultdict(int)
    basis = [(w, i) for w in words(3) for i in (0, 1)]
    unit = ("", 0)
    for u in basis:
        # Bosonized counit and coassociativity.
        d = delta_b(u, p)
        lco, rco = defaultdict(int), defaultdict(int)
        lc, rc = defaultdict(int), defaultdict(int)
        for (a, b), c in d.items():
            if not a[0]:
                lc[b] += c
            if not b[0]:
                rc[a] += c
            for (aa, ab), q in delta_b(a, p).items():
                lco[(aa, ab, b)] += c * q
            for (ba, bb), q in delta_b(b, p).items():
                rco[(a, ba, bb)] += c * q
        assert clean(lc, p) == {u: 1}
        assert clean(rc, p) == {u: 1}
        assert clean(lco, p) == clean(rco, p)
        counts["coassociativity_and_counits"] += 1

        left, right = defaultdict(int), defaultdict(int)
        for (a, b), c in d.items():
            sa, q = antipode_b(a)
            k, r = mul_b(sa, b)
            left[k] += c * q * r
            sb, q = antipode_b(b)
            k, r = mul_b(a, sb)
            right[k] += c * q * r
        target = {unit: 1} if not u[0] else {}
        assert clean(left, p) == target
        assert clean(right, p) == target
        counts["both_antipode_identities"] += 1

    small = [(w, i) for w in words(2) for i in (0, 1)]
    for u, v in product(small, repeat=2):
        uv, c = mul_b(u, v)
        lhs = clean({k: c * q for k, q in delta_b(uv, p).items()}, p)
        rhs = defaultdict(int)
        for a, q in delta_b(u, p).items():
            for b, r in delta_b(v, p).items():
                k, s = mul_tensor(a, b)
                rhs[k] += q * r * s
        assert lhs == clean(rhs, p)
        counts["bialgebra_multiplicativity"] += 1
        # xH is a graded right ideal; Hx is a graded left ideal.
        if u[0].startswith("x"):
            assert uv[0].startswith("x")
            counts["right_ideal_embedding"] += 1
        if v[0].endswith("x"):
            assert uv[0].endswith("x")
            counts["left_ideal_embedding"] += 1

    tiny = [(w, i) for w in words(1) for i in (0, 1)]
    for u, v, w in product(tiny, repeat=3):
        uv, c = mul_b(u, v)
        lhs, d = mul_b(uv, w)
        vw, e = mul_b(v, w)
        rhs, f = mul_b(u, vw)
        assert lhs == rhs and (c * d - e * f) % p == 0
        counts["associativity"] += 1

    # Forgetting grading is valid in characteristic 2. In odd
    # characteristic this exact example detects a missing super sign.
    dx = delta_h("x", p)
    dy = delta_h("y", p)
    wrong = defaultdict(int)
    for (a, b), q in dx.items():
        for (c, d), r in dy.items():
            wrong[(a + c, b + d)] += q * r  # ordinary tensor product
    mismatch = clean(wrong, p) != delta_h("xy", p)
    assert mismatch == (p != 2)
    counts["ungrading_negative_control"] += 1
    return dict(counts)


if __name__ == "__main__":
    print(json.dumps({"result": "PASS", "fields": {
        str(p): check(p) for p in (2, 3, 5)}}, indent=2, sort_keys=True))
