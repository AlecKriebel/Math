#!/usr/bin/env python3
"""Exact small-d characteristic-polynomial tests, not a Lean verification.

Expands det(t I-W) by the complete permutation formula; does not use the
Cayley-Hamilton / coefficient-cancellation route of the new Lean source.
Shares ONLY Gaussian-rational and basic matrix arithmetic with the other new
preflight. No numerical roots, floating-point comparisons, or solver verdicts.
The dimension sample cannot establish the all-dimensional theorem.
"""
from __future__ import annotations
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import argparse
import hashlib
import json
from model_bridge_preflight import G, Z, ONE, I, Checks, mm, ident, scale


def padd(a, b):
    out = [Z] * max(len(a), len(b))
    for i, c in enumerate(a): out[i] = out[i] + c
    for i, c in enumerate(b): out[i] = out[i] + c
    while len(out) > 1 and out[-1] == Z: out.pop()
    return out


def pmul(a, b):
    out = [Z] * (len(a) + len(b) - 1)
    for i, c in enumerate(a):
        for j, e in enumerate(b): out[i+j] = out[i+j] + c*e
    while len(out) > 1 and out[-1] == Z: out.pop()
    return out


def determinant_polynomial(W):
    n = len(W)
    if n == 0 or any(len(row) != n for row in W):
        raise ValueError('A nonempty square matrix is required')
    result = [Z]
    for permutation in permutations(range(n)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(n) for j in range(i+1, n))
        term = [G((-1)**inversions)]
        for i, j in enumerate(permutation):
            term = pmul(term, [-W[i][j], G(int(i == j))])
        result = padd(result, term)
    return result


def msub(A, B):
    return [[a-b for a,b in zip(r,s)] for r,s in zip(A,B)]


def evaluate_polynomial(coefficients, W):
    out = scale(0, W)
    for c in reversed(coefficients):
        out = [[x+y for x,y in zip(r,s)] for r,s in zip(mm(out,W), scale(c,ident(len(W))))]
    return out


def run():
    C = Checks()
    for n in range(1, 8):
        # All weights nonzero, most nonunit and non-real. Product need not be one.
        weights = [G(F(j+2, j+1), F((-1)**j*(j+1), j+3)) for j in range(n)]
        W = [[weights[j] if i == (j+1) % n else Z for j in range(n)] for i in range(n)]
        product = ONE
        for w in weights: product = product*w
        C.truth(f'd={n}: genuinely nonunit weights', any(w.normsq() != 1 for w in weights))
        got = determinant_polynomial(W)
        expected = [-product] + [Z]*(n-1) + [ONE]
        C.equal(f'd={n}: complete permutation determinant', got, expected)
        C.equal(f'd={n}: direct polynomial evaluation', evaluate_polynomial(got,W), scale(0,W))
        C.reject(f'd={n}: wrong determinant constant sign', [product]+expected[1:], got)
        C.reject(f'd={n}: assume product one for arbitrary weights', [-ONE]+expected[1:], got)
        power = ident(n)
        prefix = ONE
        for k in range(n):
            for i in range(n):
                C.equal(f'd={n}: orbit power {k} coordinate {i}', power[i][0], prefix if i == k else Z)
            prefix = prefix*weights[k]
            power = mm(W,power)
        C.equal(f'd={n}: full cycle power', power, scale(product,ident(n)))
        if n >= 3:
            reversed_shift = [[weights[j] if i == (j-1)%n else Z for j in range(n)] for i in range(n)]
            C.reject(f'd={n}: reversed orbit convention', reversed_shift[1][0], W[1][0])
        # Specialize independently to product-one phases; this is not an assumption above.
        phase = [I**j for j in range(n-1)]
        p = ONE
        for w in phase: p=p*w
        phase.append(ONE/p)
        V = [[phase[j] if i==(j+1)%n else Z for j in range(n)] for i in range(n)]
        C.equal(f'd={n}: phase product-one characteristic polynomial',
                determinant_polynomial(V), [-ONE]+[Z]*(n-1)+[ONE])
    if len(C.checks) != len(set(C.checks)) or len(C.controls) != len(set(C.controls)):
        raise AssertionError('Duplicate check names')
    return {'status':'exact_sample_tests_passed_NOT_LEAN', 'kernel_checked':False,
            'universal_characteristic_polynomial_proved':False,
            'independent_agent_review':False,
            'route':'full permutation determinant versus written Cayley-Hamilton route',
            'dimensions':list(range(1,8)), 'assertions':len(C.checks),
            'negative_controls':len(C.controls), 'checks':C.checks, 'controls':C.controls}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    start=datetime.now(timezone.utc)
    result=run()
    result.update(started_utc=start.isoformat(),finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  arithmetic_dependency_sha256=hashlib.sha256(Path(__file__).with_name('model_bridge_preflight.py').read_bytes()).hexdigest())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(f"{result['assertions']} exact assertions, {result['negative_controls']} negative controls passed; kernel_checked=false")

if __name__=='__main__': main()
