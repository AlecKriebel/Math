#!/usr/bin/env python3
"""Exact rank-two matrix checks, not a computation of CM K2 or a proof of it.

The proof uses ideals over an imaginary quadratic field. These checks specialize
its formal matrix identities to integral matrices to catch orientation, inverse,
coset and omitted-branch mistakes. All arithmetic is exact.
"""
from fractions import Fraction as F
from random import Random
import json
from pathlib import Path

def mat(a, b, c, d):
    return (F(a), F(b), F(c), F(d))

def mul(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)

def inv(x):
    a, b, c, d = x
    e = a * d - b * c
    if not e:
        raise AssertionError()
    return (d / e, -b / e, -c / e, a / e)

def conj(g, x):
    return mul(mul(inv(g), x), g)

def lower(x):
    return mat(1, 0, x, 1)

def upper(x):
    return mat(1, x, 0, 1)

def member(x, N):
    a, b, c, d = x
    return all((z.denominator == 1 for z in x)) and a * d - b * c == 1 and (c % N == 0) and ((d - 1) % N == 0)

def trans(gamma, reps, N):
    output = []
    for t, h in enumerate(reps):
        choices = []
        for s, k in enumerate(reps):
            tau = mul(mul(inv(k), gamma), h)
            if member(tau, N):
                choices.append((s, tau))
        if not len(choices) == 1:
            raise AssertionError((N, t, choices))
        output.append(choices[0])
    if not len({s for s, _ in output}) == len(reps):
        raise AssertionError()
    return output
rng = Random(177730005572)
counts = {'samples': 0, 'bad_coset_equations': 0, 'first_degeneracy_conjugations': 0, 'higher_depth_intertwinings': 0, 'good_coset_equations': 0, 'missing_branch_conjugations': 0}
for q in [2, 3, 5, 7]:
    for M0 in [5, 11, 13]:
        if M0 % q == 0:
            continue
        for depth in [1, 2, 3]:
            M = M0 * q ** (depth - 1)
            N = M * q
            alpha = mat(1, 0, 0, q)
            beta = mat(q, 0, 0, 1)
            reps = [mat(1, 0, N * t, q) for t in range(q)]
            ks = [lower(M * t) for t in range(q)]
            lower_reps = [conj(alpha, h) for h in reps]
            for _ in range(25):
                gamma = mat(1, 0, 0, 1)
                for __ in range(4):
                    gamma = mul(mul(gamma, upper(rng.randrange(-9, 10))), lower(N * rng.randrange(-9, 10)))
                if not member(gamma, N):
                    raise AssertionError()
                gamma_M = conj(alpha, gamma)
                if not member(gamma_M, M):
                    raise AssertionError()
                tr = trans(gamma, reps, N)
                counts['samples'] += 1
                for t, (s, tau) in enumerate(tr):
                    if not tau == mul(mul(inv(ks[s]), gamma_M), ks[t]):
                        raise AssertionError()
                    if not conj(alpha, tau) == mul(mul(inv(lower_reps[s]), gamma_M), lower_reps[t]):
                        raise AssertionError()
                    counts['bad_coset_equations'] += 1
                    counts['first_degeneracy_conjugations'] += 1
                if depth > 1:
                    if not trans(gamma_M, lower_reps, M) == [(s, conj(alpha, tau)) for s, tau in tr]:
                        raise AssertionError()
                    counts['higher_depth_intertwinings'] += 1
                else:
                    b = -pow(M, -1, q) % q
                    w = mat(1 + b * M, b, M, 1)
                    delta = mul(mul(inv(beta), w), alpha)
                    if not all((z.denominator == 1 for z in delta)):
                        raise AssertionError()
                    if not (delta[2] % M == 0 and (delta[3] - q) % M == 0):
                        raise AssertionError()
                    h_inf = mul(beta, delta)
                    if not h_inf == mul(w, alpha):
                        raise AssertionError()
                    all_reps = lower_reps + [h_inf]
                    good = trans(gamma_M, all_reps, M)
                    if not good[:-1] == [(s, conj(alpha, tau)) for s, tau in tr]:
                        raise AssertionError()
                    if not good[-1] == (q, conj(delta, gamma)):
                        raise AssertionError()
                    counts['good_coset_equations'] += q + 1
                    counts['missing_branch_conjugations'] += 1
result = {'status': 'PASS', 'arithmetic': 'exact rational matrices', 'counts': counts, 'scope': 'Checks formal matrix/coset identities only; no CM arithmetic or K2 computation.'}
p = Path(__file__).with_name('MATRIX_CHECK_RESULTS.json')
p.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
