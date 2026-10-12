#!/usr/bin/env python3
"""Independent finite controls for the Willerton tournament argument.

Standard library only. No author modules are imported. Chords are encoded as
cyclic words: +j is the tail of arrow j and -j its head. Polynomial controls
use Temperley--Lieb multiplication, rather than the author's state-sum DSU.
These controls supplement the all-diagram written proof; they are not a proof
of invariance of the imported Polyak--Viro formula.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import hashlib
import json
import random

checks = Counter()
def check(ok, label):
    assert ok, label
    checks[label] += 1

def relabel(word):
    ids = {}
    ans = []
    for x in word:
        ids.setdefault(abs(x), len(ids) + 1)
        ans.append(ids[abs(x)] * (1 if x > 0 else -1))
    return tuple(ans)

def orbit(word):
    word = tuple(word)
    return {relabel(word[k:] + word[:k]) for k in range(len(word))}

# Direct clockwise reading of the pictures in PV1994, p.448, equation (5).
P = (-1, -2, 3, 1, -3, 2)
T = (-1, 2, -3, 1, -2, 3)
OP, OT = orbit(P), orbit(T)
OP_REFLECTED = orbit(tuple(reversed(P)))

def coefficient(word):
    w = relabel(word)
    return Q(1, 2) if w in OP else Q(1) if w in OT else Q(0)

def arrow_edge(word, a, b):
    """Determine orientation from the four-letter interlacement word."""
    w = [x for x in word if abs(x) in (a, b)]
    k = w.index(a)
    w = w[k:] + w[:k]
    if w == [a, b, -a, -b]:
        return 1
    if w == [a, -b, -a, b]:
        return -1
    return 0

def probability(edges):
    # There are precisely two cyclic tournaments on three labelled vertices.
    allowed = sum(all(e == 0 or e == c for e, c in zip(edges, cyc))
                  for cyc in ((1, -1, 1), (-1, 1, -1)))
    return Q(allowed, 2 ** edges.count(0))

local_counts = Counter()
for word in permutations((1, -1, 2, -2, 3, -3)):
    es = [arrow_edge(word, a, b) for a, b in ((1, 2), (1, 3), (2, 3))]
    c, prob = coefficient(word), probability(es)
    local_counts[str(c)] += 1
    check(c <= prob, 'all_six_endpoint_orders')
    if c:
        check(c == prob, 'positive_pattern_exact_probability')
    if relabel(word) in OP_REFLECTED:
        check(prob == Q(1, 2), 'reflected_path_exact_probability')
    for a, b in combinations((1, 2, 3), 2):
        check(arrow_edge(word, a, b) == -arrow_edge(word, b, a),
              'orientation_antisymmetry')
    for signs in product((-1, 1), repeat=3):
        signed = c * signs[0] * signs[1] * signs[2]
        check(abs(signed) <= prob, 'all_crossing_signs')
    rev = tuple(reversed(word))
    check([arrow_edge(rev, a, b) for a, b in ((1, 2), (1, 3), (2, 3))]
          == [-e for e in es], 'circle_orientation_reversal')
    for k in range(6):
        check(coefficient(word[k:] + word[:k]) == c, 'basepoint_independence')

for word, expected in ((P, 1), (T, 3)):
    w = relabel(word)
    aut = sum(relabel(word[k:] + word[:k]) == w for k in range(6))
    check(aut == expected, 'cyclic_automorphism_orders')
    check(len(orbit(word)) * aut == 6, 'orbit_stabilizer')

def upper(n):
    return Q(n * (n*n - (1 if n % 2 else 4)), 24)

tournaments = 0
for n in range(7):
    pairs = list(combinations(range(n), 2))
    maximum = 0
    for bits in product((0, 1), repeat=len(pairs)):
        wins = [set() for _ in range(n)]
        for (i, j), b in zip(pairs, bits):
            wins[i if b else j].add(j if b else i)
        degrees = [len(w) for w in wins]
        cyclic = sum(all(len(wins[i] & set(S)) == 1 for i in S)
                     for S in combinations(range(n), 3))
        maximum = max(maximum, cyclic)
        check(cyclic == comb(n, 3) - sum(comb(d, 2) for d in degrees),
              'all_tournaments_degree_count')
        square_formula = Q(n*(n*n-1), 24) - sum(
            (Q(d)-Q(n-1, 2))**2 for d in degrees)/2
        check(cyclic == square_formula, 'all_tournaments_square_identity')
        check(cyclic <= upper(n), 'all_tournaments_sharp_bound')
        tournaments += 1
    check(maximum == upper(n), 'small_tournament_bound_attainment')

# Laurent polynomials in A for the bracket, represented by integer dictionaries.
def add(p, q):
    r = Counter(p)
    r.update(q)
    return {k: v for k, v in r.items() if v}

def mul(p, q):
    r = Counter()
    for i, a in p.items():
        for j, b in q.items():
            r[i+j] += a*b
    return {k: v for k, v in r.items() if v}

DELTA = {2: -1, -2: -1}
def reduce_tl(word):
    word = list(word)
    loops = 0
    while True:
        for i in range(len(word)-1):
            if word[i] == word[i+1]:
                del word[i]
                loops += 1
                break
        else:
            for i in range(len(word)-2):
                if word[i] == word[i+2]:
                    del word[i+1:i+3]
                    break
            else:
                return tuple(word), loops

def jones(strands, braid):
    assert strands in (2, 3)
    element = {(): {0: 1}}
    for g in braid:
        sign = 1 if g > 0 else -1
        new = {}
        for word, p in element.items():
            new[word] = add(new.get(word, {}), mul(p, {sign: 1}))
            red, loops = reduce_tl(word + (abs(g),))
            q = mul(p, {-sign: 1})
            for _ in range(loops):
                q = mul(q, DELTA)
            new[red] = add(new.get(red, {}), q)
        element = new
    bracket = {}
    for word, p in element.items():
        # Closure trace: tr(1)=delta^(m-1), tr(e_i)=delta^(m-2),
        # and tr(e1e2)=tr(e2e1)=1 in TL_3.
        loops = strands-1 if not word else strands-2 if len(word)==1 else 0
        for _ in range(loops):
            p = mul(p, DELTA)
        bracket = add(bracket, p)
    w = sum(1 if g>0 else -1 for g in braid)
    normalized = mul(bracket, {-3*w: 1 if w % 2 == 0 else -1})
    check(all(k % 4 == 0 for k in normalized), 'integral_Jones_exponents')
    return {-k//4: v for k, v in normalized.items()}

def braid_word(strands, braid):
    # Trace the closed braid directly, one top-to-bottom strand at a time.
    seen, word, p = set(), [], 0
    while p not in seen:
        seen.add(p)
        for i, g in enumerate(braid):
            k = abs(g)-1
            if p not in (k, k+1):
                continue
            over = (p == k) == (g > 0)
            word.append((i+1) * (1 if over else -1))
            p = 2*k+1-p
    return tuple(word) if len(seen) == strands else None

def arrow_sum(word, braid):
    result = Q(0)
    for S in combinations(range(1, len(braid)+1), 3):
        signs = 1
        for i in S:
            signs *= 1 if braid[i-1]>0 else -1
        result += signs * coefficient(tuple(x for x in word if abs(x) in S))
    return result

rng = random.Random(300094)
examples = [(2, (1,)*3, 1), (2, (-1,)*3, -1), (2, (1,)*5, 5),
            (3, (1,-2,1,-2), 0), (3, (1,2)*4, 10), (3, (1,2)*5, 20)]
for m in (2, 3):
    for _ in range(70):
        braid = tuple(rng.choice((-1, 1))*rng.randrange(1,m)
                      for _ in range(rng.randrange(1,16)))
        if braid_word(m, braid) is not None:
            examples.append((m, braid, None))
calibrations = []
for m, braid, known in examples:
    word = braid_word(m, braid)
    polynomial = jones(m, braid)
    check(sum(polynomial.values()) == 1, 'Jones_at_one')
    check(sum(k*v for k, v in polynomial.items()) == 0, 'Jones_first_derivative')
    v3 = -Q(sum(k**3*v for k, v in polynomial.items()), 36)
    check(v3 == arrow_sum(word, braid), 'independent_Temperley_Lieb_calibration')
    check(v3 == arrow_sum(tuple(reversed(word)), braid),
          'classical_reflected_path_identity')
    check(abs(v3) <= upper(len(braid)), 'classical_bound')
    if known is not None:
        check(v3 == known, 'known_normalizations')
        calibrations.append({'strands':m, 'braid':braid, 'v3':str(v3),
                             'Jones':dict(sorted(polynomial.items()))})

here = Path(__file__).resolve().parent
snapshot_sha = hashlib.sha256((here/'author_replay'/'CANDIDATE.md').read_bytes()).hexdigest()
check(snapshot_sha == 'fc2be9794873073e6482e8dfe93ccfd6c5d6f8674c2058ba0a8fc900d906d698',
      'frozen_candidate_hash')
print(json.dumps({'status':'PASS', 'exact_assertions':sum(checks.values()),
    'checks':dict(sorted(checks.items())), 'endpoint_orders':720,
    'coefficient_frequencies':dict(sorted(local_counts.items())),
    'tournaments':tournaments, 'classical_calibrations':len(examples),
    'known_examples':calibrations, 'candidate_sha256':snapshot_sha,
    'limitation':'Finite controls supplement, and do not replace, the written proof or imported knot-invariant identity.'},
    indent=2, sort_keys=True))
