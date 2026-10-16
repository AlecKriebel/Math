#!/usr/bin/env python3
"""Independent F2 diagnostic for the proposed L/LSZ dictionary.
No source documents are embedded. Finite controls support the written all-index proof.
"""
import json
from pathlib import Path
from itertools import product

ZERO = frozenset()
ONE = frozenset({(0, 0, 0, 0)})

def add(*ps):
    s = set()
    for p in ps:
        s.symmetric_difference_update(p)
    return frozenset(s)

def mon(a, b, i, j):
    if min(a, b, i, j) < 0 or a > 1 or b > 1:
        return ZERO
    return frozenset({(a, b, i, j)})

def mul(p, q):
    r = ZERO
    for t in p:
        for s in q:
            r = add(r, mon(*(t[k] + s[k] for k in range(4))))
    return r

def bracket(p, q):
    r = ZERO
    for a, b, i, j in p:
        for c, d, k, l in q:
            if (a*k + c*i) % 2:
                r = add(r, mon(a+c-1, b+d, i+k-1, j+l))
            if (b*l + d*j) % 2:
                r = add(r, mon(a+c, b+d-1, i+k, j+l-1))
    return r

def g(n, q):
    if q == 1 and n >= 0:
        return mon(0, 1, 0, n)
    if q == 2 and n >= 0:
        return mon(1, 1, 0, n)
    if q == 3 and n >= 1:
        return mon(0, 0, 1, n-1)
    if q == 4 and n >= 1:
        return mon(1, 0, 1, n-1)
    raise ValueError((n, q))

def times(c, p):
    return p if c % 2 else ZERO

def table(m, p, n, q):
    """Separate transcription of the LSZ char2 generator bracket cases."""
    if m == 0:
        return table(n, q, m, p) if n else ZERO
    if n == 0:
        if q == 1:
            if p in (1, 2):
                return times(m, g(m-1, p))
            return times(m-1, g(m-1, p)) if m >= 2 else ZERO
        if q == 2:
            if p == 1:
                return times(m, g(m-1, 2))
            if p == 2:
                return ZERO
            if p == 3:
                return g(0, 1) if m == 1 else add(times(m-1, g(m-1, 4)), g(m-1, 1))
            return g(m-1, 2)
        raise ValueError((m, p, n, q))
    h = m+n-1
    if p == 1:
        return times(m+n, g(h, q)) if q in (1, 2) else times(n-1, g(h, q))
    if p == 2:
        if q == 1:
            return table(n, q, m, p)
        if q == 2:
            return ZERO
        if q == 3:
            return add(g(h, 1), times(n-1, g(h, 4)))
        return g(h, 2)
    if p == 3:
        if q in (1, 2):
            return table(n, q, m, p)
        return ZERO if q == 3 else g(h, 3)
    if q in (1, 2, 3):
        return table(n, q, m, p)
    return ZERO

def need(ok, label):
    if not ok:
        raise RuntimeError(label)

def basis(n):
    if n == 0:
        return {(0,0,0,0), (0,1,0,0), (1,1,0,0)}
    return {(a,b,i,n-i) for a,b in product(range(2), repeat=2)
            for i in range(n+1) if i >= 1 or b == 1}

def run():
    bound = 25
    gens = [(n,q) for n in range(bound+1) for q in range(1,5)
            if n >= 1 or q <= 2]
    counts = {}
    pairs = 0
    for (m,p),(n,q) in product(gens, repeat=2):
        need(bracket(g(m,p),g(n,q)) == table(m,p,n,q), ("bracket",m,p,n,q))
        pairs += 1
    counts["generator_bracket_pairs"] = pairs
    ring = 0
    for m,n in product(range(bound+1), repeat=2):
        for p,q in [(1,1),(1,2),(2,2)]:
            need(mul(g(m,p),g(n,q)) == ZERO, ("relation1",m,n,p,q)); ring += 1
        if n >= 1:
            need(mul(g(m,2),g(n,4)) == ZERO, ("relation2a",m,n)); ring += 1
            need(mul(g(m,2),g(n,3)) == mul(g(m,1),g(n,4)), ("relation2b",m,n)); ring += 1
        if min(m,n) >= 1:
            need(mul(g(m,4),g(n,4)) == ZERO, ("relation3a",m,n)); ring += 1
            for q in (3,4):
                need(mul(g(m,1),g(n,q)) == mul(g(0,1),g(m+n,q)), ("relation3",m,n,q)); ring += 1
        if m >= 2 and n >= 1:
            for q in (3,4):
                need(mul(g(m,3),g(n,q)) == mul(g(1,3),g(m+n-1,q)), ("relation4",m,n,q)); ring += 1
    counts["cup_relation_instances"] = ring
    for n in range(bound+1):
        need(len(basis(n)) == (3 if n == 0 else 4*n+2), ("dimension",n))
        if n == 0:
            mapped = {next(iter(ONE)),next(iter(g(0,1))),next(iter(g(0,2)))}
        else:
            mapped = set(g(n,1) | g(n,2))
            for i in range(1,n+1):
                for q in (3,4):
                    p = mul(mon(0,0,i-1,0),g(n-i+1,q))
                    mapped.update(p)
                    mapped.update(mul(g(0,1),p))
        need(mapped == basis(n), ("basis-bijection",n))
    counts["basis_degrees"] = bound+1
    bs = [t for n in range(9) for t in basis(n)]
    weak = 0
    aug = 0
    for t,s in product(bs,repeat=2):
        p,q=frozenset({t}),frozenset({s})
        need((0,0,0,0) not in bracket(p,q), ("augmentation-bracket",t,s)); aug += 1
        if (t[0] or t[1]) and (s[0] or s[1]):
            need(all(v[0] or v[1] for v in bracket(p,q)), ("weak-closure",t,s)); weak += 1
    counts["augmentation_bracket_pairs_through_degree8"] = aug
    counts["nilpotent_pair_weak_closure_through_degree8"] = weak
    stripping = 0
    for i in range(1,bound+1):
        for j in range(bound+1):
            z=mon(1,0,i,j)
            need(mul(z,z) == ZERO, ("nilpotence",i,j))
            need(bracket(g(1,3),z) == mon(0,0,i,j), ("nilpotent-strip",i,j))
            stripping += 1
    counts["nilpotent_stripping_instances"] = stripping
    return {"status":"pass","coefficient_field":"F2","index_bound":bound,
            "counts":counts,
            "scope":"finite diagnostics, not verification of source proofs or an all-degree Hochschild resolution"}
if __name__ == "__main__":
    r = run()
    print(json.dumps(r,indent=2))
    (Path(__file__).parent/"DIAGNOSTIC_RESULT.json").write_text(json.dumps(r,indent=2)+"\n")

