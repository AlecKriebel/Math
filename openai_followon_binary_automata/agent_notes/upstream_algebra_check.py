"""Independent finite-diagram falsification checks of the upstream algebra.

This checks every width-one diagram, all relevant width-one corners, products,
nested pairs and transport contexts. Width-two checks are seeded samples, while
all width-two diagrams are enumerated to identify the idempotents. These are
finite sanity checks, not proofs of the uniform exponential theorem.
"""
import itertools
import json
import random
from functools import lru_cache


def check_width(m, sampled_contexts=0, seed=129):
    full = (1 << (m * m)) - 1
    identity = sum(1 << (i * m + i) for i in range(m))

    @lru_cache(None)
    def relcomp(a, b):
        return sum(1 << (i * m + k) for i in range(m) for k in range(m)
                   if any((a >> (i * m + j)) & (b >> (j * m + k)) & 1
                          for j in range(m)))

    @lru_cache(None)
    def star(a):
        r = a | identity
        for _ in range(m):
            r |= relcomp(r, r)
        return r

    def chain(*rels):
        r = identity
        for a in rels:
            r = relcomp(r, a)
        return r

    def comp(a, b):
        F, B, L, R = a
        f, bb, l, rr = b
        join = star(relcomp(l, R))
        return (chain(F, join, f), chain(bb, star(relcomp(R, l)), B),
                L | chain(F, join, l, B), rr | chain(bb, R, join, f))

    @lru_cache(None)
    def classes(e):
        out = set()
        for sign in range(2):
            K = star(relcomp(e[2 + sign], e[3 - sign]))
            P = chain(K, e[sign], K)
            for i in range(m):
                if (P >> (i * m + i)) & 1:
                    C = frozenset(j for j in range(m)
                                  if (P >> (i * m + j)) & (P >> (j * m + i)) & 1)
                    out.add((sign, C))
        return frozenset(out)

    def missing(e, z):
        out = set()
        for sign, C in classes(e):
            K = star(relcomp(e[2 + sign], e[3 - sign]))
            U = chain(K, z[sign], K)
            if all(not ((U >> (i * m + i)) & 1) for i in C):
                out.add((sign, C))
        return frozenset(out)

    def included(a, b):
        return all((x & ~y) == 0 for x, y in zip(a, b))

    def incorn(e, z):
        return comp(e, z) == z == comp(z, e)

    def idem_power(a):
        seen = set()
        z = a
        while comp(z, z) != z:
            assert z not in seen, ("power orbit failed", a)
            seen.add(z)
            z = comp(z, a)
        return z

    diagrams = list(itertools.product(range(full + 1), repeat=4))
    idems = [e for e in diagrams if comp(e, e) == e]
    counters = {"diagrams": len(diagrams), "idempotents": len(idems),
                "corners": 0, "missing_products": 0, "nested_pairs": 0,
                "transport_contexts": 0, "transport_budgets": 0}
    rng = random.Random(seed)
    if m == 1:
        corner_pairs = [(e, z) for e in idems for z in diagrams if incorn(e, z)]
    else:
        corner_pairs = [(e := rng.choice(idems), comp(comp(e, rng.choice(diagrams)), e))
                        for _ in range(10000)]
    for e, z in corner_pairs:
        assert incorn(e, z)
        assert missing(e, e) == frozenset()
        assert missing(e, z) or included(e, z), ("empty-loss inclusion", e, z)
        counters["corners"] += 1
        candidates = diagrams if m == 1 else [rng.choice(diagrams) for _ in range(3)]
        for a in candidates:
            w = comp(comp(e, a), e)
            assert missing(e, comp(z, w)) <= missing(e, z) | missing(e, w)
            counters["missing_products"] += 1
        d = idem_power(z)
        assert incorn(e, d)
        for sign, D in classes(d):
            old = [(s, C) for s, C in classes(e) if s == sign and C <= D]
            assert any(c not in missing(e, d) for c in old) or len(old) >= 2, (
                "nested containment", e, d, sign, sorted(D))
        counters["nested_pairs"] += 1
    if m == 1:
        triples = itertools.product(idems, diagrams, diagrams)
    else:
        triples = ((rng.choice(idems), rng.choice(diagrams), rng.choice(diagrams))
                   for _ in range(sampled_contexts))
    for e, u, v in triples:
        d = comp(comp(u, e), v)
        if comp(d, d) != d:
            continue
        counters["transport_contexts"] += 1
        Cs = list(classes(e))
        budgets = [frozenset(Cs[i] for i in range(len(Cs)) if (bits >> i) & 1)
                   for bits in range(1 << len(Cs))]
        raw = diagrams if m == 1 else [rng.choice(diagrams) for _ in range(100)]
        replacements = set(comp(comp(e, a), e) for a in raw)
        for J in budgets:
            union = frozenset()
            for z in replacements:
                w = comp(comp(u, z), v)
                if missing(e, z) <= J and incorn(d, w):
                    union |= missing(d, w)
            assert len(union) <= 2 * len(J), ("common transport", e, d, u, v, J, union)
            counters["transport_budgets"] += 1
    return counters


if __name__ == "__main__":
    result = {"scope": "exhaustive width one and seeded width two falsification",
              "seed": 129, "width_1": check_width(1),
              "width_2": check_width(2, sampled_contexts=2000)}
    print(json.dumps(result, indent=2, sort_keys=True))
