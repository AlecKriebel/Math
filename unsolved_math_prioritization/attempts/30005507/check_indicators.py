#!/usr/bin/env python3
"""Exact, bounded checks for OWR-13750328-012. Standard library only.

Enumerates compatible presentations of index-two extensions of Q8, not
isomorphism classes and not arbitrary blocks. Characters of the solvable
C3-semidirect-product model are computed in Z[zeta_3], without floats.
"""
from itertools import product
from collections import Counter
import json
from pathlib import Path

D = tuple(product(range(4), range(2)))
one = (0, 0)

def mul(x, y):
    a, b = x
    c, d = y
    return ((a + (-1)**b * c + 2*b*d) % 4, (b+d) % 2)

def power(x, n):
    y = one
    for _ in range(n):
        y = mul(y, x)
    return y

def inverse(x):
    return next(y for y in D if mul(x, y) == one)

def character(k, x):
    a, b = x
    if k < 4:
        r, s = divmod(k, 2)
        return (-1)**(r*a+s*b)
    return 2 if x == one else -2 if x == (2, 0) else 0

def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def times(a, b):
    x, y = a
    z, w = b
    return (x*z-y*w, x*w+y*z-y*w)

def conjugate(a):
    return (a[0]-a[1], -a[1])

def scale(n, a):
    return (n*a[0], n*a[1])

def total(seq):
    result = (0, 0)
    for z in seq:
        result = add(result, z)
    return result

roots = ((1, 0), (0, 1), (-1, -1))
autos = []
for i, j in product(D, repeat=2):
    if power(i, 2) != (2, 0) or power(j, 2) != (2, 0):
        continue
    alpha = {x: mul(power(i, x[0]), power(j, x[1])) for x in D}
    if len(set(alpha.values())) == 8 and all(
        alpha[mul(x, y)] == mul(alpha[x], alpha[y]) for x, y in product(D, repeat=2)
    ):
        autos.append(alpha)
assert len(autos) == 24
assert all(mul(mul(x, y), z) == mul(x, mul(y, z)) for x, y, z in product(D, repeat=3))
assert [sum(character(k, mul(x, x)) for x in D)//8 for k in range(5)] == [1, 1, 1, 1, -1]

records = []
for ai, alpha in enumerate(autos):
    ainv = {y: x for x, y in alpha.items()}
    for s in D:
        if alpha[s] != s or any(
            alpha[alpha[x]] != mul(mul(s, x), inverse(s)) for x in D
        ):
            continue

        E = tuple(product(D, range(2)))
        def emul(x, y):
            d, b = x
            f, c = y
            out = mul(d, alpha[f] if b else f)
            return (mul(out, s) if b*c else out, (b+c) % 2)

        assert all(emul(emul(x, y), z) == emul(x, emul(y, z))
                   for x, y, z in product(E, repeat=3))
        assert all(any(emul(x, y) == (one, 0) == emul(y, x) for y in E) for x in E)
        square = [emul(x, x)[0] for x in E if x[1] == 1]
        sums = [sum(character(k, d) for d in square) for k in range(5)]
        assert all(v % 8 == 0 for v in sums)
        gow = [v//8 for v in sums]
        assert all(v in (-1, 0, 1) for v in gow)
        assert all((gow[k] != 0) == all(character(k, alpha[d]) == character(k, d) for d in D)
                   for k in range(5))
        assert sum(character(k, one)*gow[k] for k in range(5)) == square.count(one)
        # Pointwise Fourier inversion of the coset-square counting function.
        assert all(sum(gow[k]*character(k, d) for k in range(5)) == square.count(d) for d in D)

        G = tuple(product(range(3), E))
        def gmul(x, y):
            a, e = x
            b, f = y
            return ((a + (-1)**e[1]*b) % 3, emul(e, f))

        def psi(k, x):
            a, (d, b) = x
            if b:
                return (0, 0)
            return add(scale(character(k, d), roots[a]),
                       scale(character(k, ainv[d]), roots[-a % 3]))

        assert all(total(times(psi(k, x), conjugate(psi(l, x))) for x in G)
                   == (len(G) if k == l else 0, 0) for k, l in product(range(5), repeat=2))
        model_sums = [total(psi(k, gmul(x, x)) for x in G) for k in range(5)]
        assert model_sums == [(len(G)*g, 0) for g in gow]
        records.append({"automorphism_index": ai, "t_square": list(s),
                        "gow": gow, "outside_involutions": square.count(one)})

# The numerical obstruction in Attempt 3 uses D=Q8 x Q8 and E=D x C2.
pairs = tuple(product(range(5), repeat=2))
degrees = [character(a, one)*character(b, one) for a, b in pairs]
correct = [(-1)**((a == 4)+(b == 4)) for a, b in pairs]
alternate = correct.copy()
for pair in ((0, 4), (1, 4)):
    alternate[pairs.index(pair)] = 1
alternate[pairs.index((4, 4))] = -1
assert sum(d*v for d, v in zip(degrees, correct)) == 4
assert sum(d*v for d, v in zip(degrees, alternate)) == 4
assert all(v == 1 for d, v in zip(degrees, alternate) if d == 1)

def distribution(values):
    return {str(d): {str(e): sum(dd == d and ee == e for dd, ee in zip(degrees, values))
                     for e in (-1, 0, 1)} for d in sorted(set(degrees))}

result = {"status": "all exact assertions passed",
          "scope": "Compatible Q8 extension presentations and their solvable model blocks only; no arbitrary-block test.",
          "automorphisms": len(autos), "compatible_presentations": len(records),
          "model_character_indicator_checks": 5*len(records),
          "model_character_inner_product_checks": 25*len(records),
          "indicator_vectors": [{"vector": list(v), "presentations": n}
                                 for v, n in sorted(Counter(tuple(r['gow']) for r in records).items())],
          "numerical_obstruction": {"correct": distribution(correct), "alternate": distribution(alternate),
                                    "common_degree_weighted_sum": 4},
          "records": records}

if __name__ == "__main__":
    out = Path(__file__).with_name("exact_results.json")
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, indent=2))
