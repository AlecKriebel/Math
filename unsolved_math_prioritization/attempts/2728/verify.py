#!/usr/bin/env python3
"""Finite exact accounting controls, not geometric realization certificates."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import itertools

checks = {}
def ck(name, value):
    assert value, name
    checks[name] = "PASS"

def exponent(word):
    return sum(1 if x > 0 else -1 for x in word)

def permutation(n, word):
    p = list(range(n))
    for x in word:
        k = abs(x)-1
        p[k], p[k+1] = p[k+1], p[k]
    return tuple(p)

def band(i, j):
    conjugator = list(range(j-1, i, -1))
    return conjugator + [i] + [-x for x in reversed(conjugator)]

for n in range(2, 7):
    for i in range(1, n):
        for j in range(i+1, n+1):
            w = band(i, j)
            expected = list(range(n))
            expected[i-1], expected[j-1] = expected[j-1], expected[i-1]
            ck(f"band_exponent_{n}_{i}_{j}", exponent(w) == 1)
            ck(f"band_permutation_{n}_{i}_{j}", permutation(n,w) == tuple(expected))
            inverse = [-x for x in reversed(w)]
            ck(f"inverse_band_exponent_{n}_{i}_{j}", exponent(inverse) == -1)
            ck(f"band_inverse_cancellation_{n}_{i}_{j}",
               exponent(w+inverse) == 0 and permutation(n,w+inverse) == tuple(range(n)))

for N in range(33):
    word = [1]*3 + [1,-1]*N
    positive, negative, strands = 3+N, N, 2
    chi = strands-positive-negative
    sl = exponent(word)-strands
    ck(f"trefoil_word_control_{N}",
       exponent(word) == 3 and sl == 1 and chi == -1-2*N
       and -1-chi == 2*negative)

for n in range(2, 7):
    for positive, negative in ((3,0),(4,1),(10,4),(7,5)):
        chi = n-positive-negative
        sl = positive-negative-n
        ck(f"band_gap_{n}_{positive}_{negative}", -chi-sl == 2*negative)
        ck(f"positive_stabilization_{n}_{positive}_{negative}",
           (n+1)-(positive+1)-negative == chi and
           (positive+1)-negative-(n+1) == sl)
        ck(f"negative_stabilization_{n}_{positive}_{negative}",
           (n+1)-positive-(negative+1) == chi and
           positive-(negative+1)-(n+1) == sl-2)

ck("negative_stabilized_trefoil",
   3-3-1 == -1 and 3-1-3 == -1 and Fraction(1-(-1),2) == 1)

# Abstract signed counts only: no surface or foliation realization is inferred.
for ep, hp, m in itertools.product(range(1,5), range(5), range(4)):
    em = hm = m
    chi = ep+em-hp-hm
    sl = -(ep-em)+(hp-hm)
    ck(f"balanced_negative_counts_{ep}_{hp}_{m}", sl == -chi)
ck("explicit_nonzero_balanced_negative_counts",
   2+1-3-1 == -1 and -(2-1)+(3-1) == 1)

# Scalar endpoint squeeze: a diagnostic of the necessary equality, not
# computation of any knot Floer invariant or smooth slice genus.
for g in range(9):
    admissible = [(tau, g4) for tau in range(-g,g+1) for g4 in range(g+1)
                  if 2*g-1 <= 2*tau-1 <= 2*g4-1 <= 2*g-1]
    ck(f"sharp_knot_squeeze_{g}", admissible == [(g,g)])

root=Path(__file__).resolve().parent
receipt={
    "problem_id":2728,
    "status":"PASS",
    "assertions":len(checks),
    "obstruction_sha256":hashlib.sha256((root/"OBSTRUCTION.md").read_bytes()).hexdigest(),
    "verifier_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope":"Exact finite braid exponent/permutation, Euler characteristic, "
            "stabilization and signed-count controls. No geometric realization, "
            "transverse isotopy algorithm, or full solution is certified.",
    "checks":checks
}
print(json.dumps(receipt,indent=2,sort_keys=True))
