"""Finite falsification checks, not a proof of the unrestricted theorem.

The operator lemmas allow arbitrary p and m, unlike the exponential theorem.
We use p=3,m=2 on the nonhomocyclic group Z/27 + Z/9.
"""
from itertools import product
from functools import cache
from pathlib import Path
import datetime
import hashlib
import json
import random

P, M = 3, 2
points = list(product(range(27), range(9)))
index = {x: i for i, x in enumerate(points)}
identity = tuple(range(len(points)))


def add(x, y):
    return ((x[0] + y[0]) % 27, (x[1] + y[1]) % 9)


def scale(k, x):
    return (k * x[0] % 27, k * x[1] % 9)


def operator(a, b, c, d):
    return tuple(index[((3*a*x + 3*b*y) % 27, (c*x + 3*d*y) % 9)]
                 for x, y in points)


ops = [operator(0, 1, 1, 0), operator(1, 1, 2, 1),
       operator(2, 2, 1, 2)]
ops.append(tuple(index[add(points[x], points[y])]
                 for x, y in zip(ops[0], ops[1])))


def compose(a, b):
    return tuple(a[x] for x in b)


@cache
def word(w):
    out = identity
    for letter in reversed(w):
        out = compose(ops[letter], out)
    return out


sections = []
for variant in range(3):
    section = {}
    for x, y in points:
        if x % 3 == y % 3 == 0:
            # Arbitrary, generally nonadditive and nonnormalized roots.
            i = (x//3 + y + variant) % 3
            j = (x + y//3 + 2*variant) % 3
            root = ((x//3 + 9*i) % 27, (y//3 + 3*j) % 9)
            assert scale(3, root) == (x, y)
            section[index[(x, y)]] = index[root]
    sections.append(section)


def compositions(n, k):
    if k == 1:
        if n >= M:
            yield (n,)
        return
    for first in range(M, n - M*(k-1) + 1):
        for rest in compositions(n-first, k-1):
            yield (first,) + rest


def evaluate(w, parts, choices):
    ends = [0]
    for part in parts:
        ends.append(ends[-1]+part)
    out = identity
    for j in range(len(parts)-1, -1, -1):
        out = compose(word(w[ends[j]:ends[j+1]]), out)
        if j:
            out = tuple(sections[choices[j-1]][x] for x in out)
    return out


counts = dict(contraction_points=0, marked_maps=0, additive_pairs=0,
              coefficient_cancellations=0, slot_maps=0, budget_cases=0)
for a, b in product(range(len(ops)), repeat=2):
    output = word((a, b))
    for i, x in enumerate(points):
        assert all(z % 3 == 0 for z in points[output[i]])
        for r in (1, 2, 3):
            torsion = {index[y] for y in points if scale(3**r, y) == (0, 0)}
            p_torsion = {index[scale(3, points[j])] for j in torsion}
            if i in torsion:
                assert output[i] in p_torsion
        counts['contraction_points'] += 1

rng = random.Random(21123)
for n, s in [(4, 1), (5, 1), (6, 1), (6, 2), (7, 2), (8, 2)]:
    for _ in range(8):
        w = tuple(rng.randrange(3) for _ in range(n))
        reference = None
        for parts in compositions(n, s+1):
            for choices in product(range(3), repeat=s):
                result = evaluate(w, parts, choices)
                if reference is None:
                    reference = result
                assert result == reference
                counts['marked_maps'] += 1
        for i, x in enumerate(points):
            assert scale(3**s, points[reference[i]]) == points[word(w)[i]]
            counts['coefficient_cancellations'] += 1
        for i, x in enumerate(points):
            for j, y in enumerate(points):
                k = index[add(x, y)]
                assert points[reference[k]] == add(points[reference[i]], points[reference[j]])
                counts['additive_pairs'] += 1
        # Joint-family slot additivity: operator 3 = operator 0 + operator 1.
        for slot in (0, n//2, n-1):
            outputs = []
            parts = next(compositions(n, s+1))
            for replacement in (0, 1, 3):
                ww = list(w); ww[slot] = replacement
                outputs.append(evaluate(tuple(ww), parts, (0,)*s))
            assert all(points[c] == add(points[a], points[b])
                       for a, b, c in zip(*outputs))
            counts['slot_maps'] += 1


def valuation(n, p):
    value = 0
    while n and n % p == 0:
        n //= p
        value += 1
    return value


primes = [p for p in range(5, 102) if all(p % d for d in range(2, int(p**.5)+1))]
for p in primes:
    m = (p-1)//4
    factorial_valuation = 0
    for j in range(1, 5001):
        factorial_valuation += valuation(j, p)
        assert 4*m*factorial_valuation <= j-1
        assert 4*m*valuation(j, p) <= j-1
        counts['budget_cases'] += 2

out = {'verdict': 'PASS', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'scope': 'Finite checks of abstract operator lemmas and denominator arithmetic only',
       'module': 'Z/27 + Z/9', 'p': P, 'm': M, 'counts': counts,
       'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
