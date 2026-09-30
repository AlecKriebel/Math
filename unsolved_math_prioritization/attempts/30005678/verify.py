#!/usr/bin/env python3
"""Exact diagnostic checks, not a proof of the all-category 2-Segal criterion."""
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
counts = {}

def check(category, assertion):
    if not assertion:
        raise AssertionError(category)
    counts[category] = counts.get(category, 0) + 1

def reduce_word(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)

def inverse(word):
    return tuple(-x for x in reversed(word))

def multiply(*words):
    return reduce_word(x for w in words for x in w)

def substitute(word, images):
    return multiply(*(images[x] if x > 0 else inverse(images[-x]) for x in word))

def power(word, k):
    return multiply(*([word if k >= 0 else inverse(word)] * abs(k)))

def reduced_words(rank, max_length):
    yield ()
    current = [()]
    alphabet = tuple(range(1, rank + 1)) + tuple(range(-1, -rank - 1, -1))
    for _ in range(max_length):
        current = [w + (a,) for w in current for a in alphabet if not w or w[-1] != -a]
        yield from current

# a=1, b=2, c=3. This is a noncommutative reduced-word calculation.
a, b, c = (1,), (2,), (3,)
comm = multiply(c, a, inverse(c), inverse(a))
qA = {1: (), 2: b, 3: c}
qC = {1: (), 2: (), 3: c}
word_cases = 0
for k in (-3, -2, -1, 1, 2, 3):
    u = power(comm, k)
    alpha = {1: a, 2: multiply(b, u), 3: c}
    beta = {1: a, 2: multiply(b, inverse(u)), 3: c}
    check('free_group', alpha[2] == (2,) + u)
    check('free_group', any(abs(x) == 3 for x in alpha[2]))
    check('free_group', substitute(alpha[2], qA) == b)
    check('free_group', substitute(alpha[2], qC) == ())
    check('normal_closure_certificate', multiply(alpha[2], inverse(u)) == b)
    # u lies in the normal closure of a; this identity is the certificate.
    check('normal_closure_certificate', substitute(u, qA) == ())
    for w in reduced_words(3, 3):
        word_cases += 1
        check('inverse_automorphism', substitute(substitute(w, alpha), beta) == w)
        check('inverse_automorphism', substitute(substitute(w, beta), alpha) == w)
        check('quotient_map', substitute(substitute(w, alpha), qA) == substitute(w, qA))
        check('quotient_map', substitute(substitute(w, alpha), qC) == substitute(w, qC))

# The two embeddings are exact homomorphisms on F(a,d), with d encoded as 2.
v0 = {1: a, 2: b}
v1 = {1: a, 2: multiply(b, comm)}
q_source = {1: (), 2: b}
for w in reduced_words(2, 4):
    check('flag_quotients', substitute(substitute(w, v0), qA) == substitute(w, q_source))
    check('flag_quotients', substitute(substitute(w, v1), qA) == substitute(w, q_source))
    check('flag_quotients', substitute(substitute(w, v0), qC) == ())
    check('flag_quotients', substitute(substitute(w, v1), qC) == ())
check('missing_lift', v1[2] == (2, 3, 1, -3, -1))
check('missing_lift', not all(abs(x) in (1, 2) for x in v1[2]))
check('abelianization_warning', [sum((x > 0) - (x < 0) for x in v1[2] if abs(x) == j) for j in (1, 2, 3)] == [0, 1, 0])

# Positive comparison: pointed finite sets, with the basepoint suppressed.
def subsets(s):
    s = tuple(s)
    return [frozenset(a) for k in range(len(s)+1) for a in combinations(s, k)]
set_intervals = 0
for n in range(7):
    universe = frozenset(range(n))
    for A in subsets(universe):
        quotient = universe - A
        Cs = [C for C in subsets(universe) if A <= C]
        images = [C-A for C in Cs]
        check('pointed_set_intervals', len(set(images)) == len(Cs))
        check('pointed_set_intervals', set(images) == set(subsets(quotient)))
        for C in Cs:
            set_intervals += 1
            check('pointed_set_intervals', A | (C-A) == C)

# All triangulations and flips for polygons with 3 through 8 vertices.
@lru_cache(None)
def triangulations(vertices):
    if len(vertices) < 3:
        return (frozenset(),)
    out = []
    for k in range(1, len(vertices)-1):
        tri = tuple(sorted((vertices[0], vertices[k], vertices[-1])))
        for L in triangulations(vertices[:k+1]):
            for R in triangulations(vertices[k:]):
                out.append(L | R | {tri})
    return tuple(out)

def edges(T):
    return frozenset(tuple(sorted(e)) for t in T for e in combinations(t, 2))

def neighbors(T):
    out = set()
    for t, s in combinations(T, 2):
        common = set(t) & set(s)
        if len(common) != 2:
            continue
        other = (set(t) | set(s)) - common
        new = frozenset(tuple(sorted(other | {x})) for x in common)
        out.add((T-{t,s}) | new)
    return out

polygon_counts = {}
for n in range(3, 9):
    Ts = set(triangulations(tuple(range(n))))
    fan = frozenset((0, k, k+1) for k in range(1, n-1))
    check('polygon', fan in Ts)
    reached, todo = {fan}, [fan]
    while todo:
        T = todo.pop()
        for U in neighbors(T):
            check('flip', U in Ts)
            check('flip', T in neighbors(U))
            if U not in reached:
                reached.add(U)
                todo.append(U)
    check('polygon', reached == Ts)
    for T in Ts:
        check('polygon', len(T) == n-2)
        check('polygon', len(neighbors(T)) == n-3)
        if T != fan:
            old = {e for e in edges(T) if 0 in e}
            check('fan_increasing_flip', any(old < {e for e in edges(U) if 0 in e} for U in neighbors(T)))
    polygon_counts[str(n)] = len(Ts)

print(json.dumps({
    'status': 'PASS',
    'artifact_sha256': sha256((HERE/'PARTIAL_RESULT.md').read_bytes()).hexdigest(),
    'verifier_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    'assertions': sum(counts.values()),
    'assertions_by_kind': counts,
    'automorphism_word_cases': word_cases,
    'pointed_set_interval_cases': set_intervals,
    'triangulation_counts_by_number_of_vertices': polygon_counts,
    'limitations': 'Finite exact diagnostics only; no exhaustive category classification, general homotopy proof, or priority certificate.'
}, indent=2, sort_keys=True))
