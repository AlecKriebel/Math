#!/usr/bin/env python3
"""Exact finite diagnostics for the candidate sign rotation; not an ordinal proof."""
from fractions import Fraction
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import json

BASE = Path(__file__).resolve().parent
MAX_LENGTH = 8

def words(max_length):
    yield ''
    for n in range(1, max_length + 1):
        yield from (''.join(p) for p in product('-+', repeat=n))

def value(s):
    """Independent finite-surreal rational evaluation by initial sign run."""
    if not s:
        return Fraction(0)
    k = 0
    while k < len(s) and s[k] == s[0]:
        k += 1
    v = Fraction(k if s[0] == '+' else -k)
    for j in range(k, len(s)):
        v += Fraction(1 if s[j] == '+' else -1, 2 ** (j - k + 1))
    return v

def prefix(s, t):
    return len(s) < len(t) and t.startswith(s)

def prefixes(s):
    return {s[:i] for i in range(len(s))}

def f(s, a):
    if s == a:
        return ''
    if not s.startswith(a):
        return '+' + s
    assert s[len(a)] == '+'
    return '+' + a + s[len(a) + 1:]

def inv(z, a):
    if not z:
        return a
    assert z[0] == '+'
    w = z[1:]
    if w.startswith(a):
        return a + '+' + w[len(a):]
    return w

def branch(s, a):
    if s == a:
        return 'minimum'
    return 'B' if s.startswith(a) else 'A'

W = list(words(MAX_LENGTH))
V = {s: value(s) for s in W}
results = []
for alpha in range(MAX_LENGTH + 1):
    a = '-' * alpha
    S = [s for s in W if V[s] >= V[a]]
    F = {s: f(s, a) for s in S}
    FV = {s: value(F[s]) for s in S}
    assert len(set(F.values())) == len(S)
    prefix_identity_count = inverse_source_count = inverse_target_count = 0
    pair_count = right_implication_count = right_equivalence_away_minimum_count = nonminimum_prefix_count = 0
    pair_cases = {}
    for s in S:
        assert inv(F[s], a) == s
        inverse_source_count += 1
        assert prefixes(F[s]) == ({''} | {F[v] for v in prefixes(s) if v != a}) if s != a else not prefixes(F[s])
        prefix_identity_count += 1
        assert prefixes(F[s]) <= set(F.values())
    for z in W:
        if value(z) >= 0:
            s = inv(z, a)
            assert value(s) >= V[a]
            assert f(s, a) == z
            inverse_target_count += 1
    for s in S:
        for t in S:
            pair_count += 1
            key = branch(s, a) + '/' + branch(t, a)
            pair_cases[key] = pair_cases.get(key, 0) + 1
            assert (V[s] < V[t]) == (FV[s] < FV[t])
            sr = prefix(s, t) and V[s] > V[t]
            fr = prefix(F[s], F[t]) and FV[s] > FV[t]
            assert not fr or sr, (alpha, s, t, F[s], F[t], 'new right predecessor')
            right_implication_count += 1
            if t != a:
                assert sr == fr
                right_equivalence_away_minimum_count += 1
            else:
                assert not fr
            if s != a and t != a:
                assert prefix(s, t) == prefix(F[s], F[t])
                nonminimum_prefix_count += 1
    results.append(dict(alpha=alpha, source_nodes=len(S), image_nodes=len(set(F.values())), ordered_pairs=pair_count,
                        inverse_source_checks=inverse_source_count, inverse_target_checks=inverse_target_count,
                        prefix_identity_checks=prefix_identity_count, right_relation_implication_checks=right_implication_count,
                        right_relation_equivalence_except_child_minimum_checks=right_equivalence_away_minimum_count,
                        nonminimum_prefix_equivalence_checks=nonminimum_prefix_count, pair_cases=pair_cases, passed=True))
output = dict(completed_utc=datetime.now(timezone.utc).isoformat(), max_source_length=MAX_LENGTH,
              max_tested_finite_alpha=MAX_LENGTH, arithmetic='exact fractions',
              scope='Finite sign sequences only. Diagnostic evidence, not proof for arbitrary ordinals.',
              total_source_nodes=sum(r['source_nodes'] for r in results),
              total_ordered_pairs=sum(r['ordered_pairs'] for r in results),
              all_passed=True, results=results)
(BASE / 'finite_sign_checks.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps({k:output[k] for k in ['completed_utc','total_source_nodes','total_ordered_pairs','all_passed','scope']}, indent=2))
