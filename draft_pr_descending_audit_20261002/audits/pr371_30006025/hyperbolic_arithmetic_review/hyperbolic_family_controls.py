#!/usr/bin/env python3
"""Independent exact triangle-character controls; no infinite-law certification."""
from fractions import Fraction as Q
from itertools import product
from collections import Counter
import json

counts = Counter()
def ck(value, scope):
    assert value, scope
    counts[scope] += 1

# Q[u,v]/(v^2-u^2+3/4), normalized to v exponent 0 or 1.
def add(p, r):
    out = dict(p)
    for e, c in r.items():
        out[e] = out.get(e, Q(0)) + c
    return {e: c for e, c in out.items() if c}
def neg(p):
    return {e: -c for e, c in p.items()}
def mul(p, r):
    out = {}
    for (i, j), a in p.items():
        for (k, l), b in r.items():
            if j+l == 2:
                out = add(out, {(i+k+2, 0): a*b, (i+k, 0): -Q(3,4)*a*b})
            else:
                out = add(out, {(i+k, j+l): a*b})
    return out
def constant(q):
    return {(0,0): Q(q)} if q else {}
def mm(a, b):
    return [[add(mul(a[i][0], b[0][j]), mul(a[i][1], b[1][j])) for j in range(2)] for i in range(2)]
def trace(a):
    return add(a[0][0], a[1][1])
def determinant(a):
    return add(mul(a[0][0], a[1][1]), neg(mul(a[0][1], a[1][0])))
def inverse(a):
    return [[a[1][1], neg(a[0][1])], [neg(a[1][0]), a[0][0]]]

one, zero = constant(1), {}
I = [[one, zero], [zero, one]]
minus_I = [[constant(-1), zero], [zero, constant(-1)]]
u, v = {(1,0): Q(1)}, {(0,1): Q(1)}
A = [[zero, constant(-1)], [one, zero]]
B = [[constant(Q(1,2)), add(u,v)], [add(neg(u),v), constant(Q(1,2))]]
ck(determinant(A) == one, 'generator_determinant')
ck(determinant(B) == one, 'generator_determinant')
ck(mm(A,A) == minus_I, 'order_two_in_PSL')
ck(mm(mm(B,B),B) == minus_I, 'order_three_in_PSL')
AB = mm(A,B)
ck(trace(AB) == {(1,0): Q(2)}, 'triangle_product_trace')
ck(mm(AB,AB) == [[add(mul(trace(AB), AB[i][j]), neg(I[i][j])) for j in range(2)] for i in range(2)], 'cayley_hamilton')

alphabet = [A, B, inverse(A), inverse(B)]
word_controls = 0
for length in range(6):
    for word in product(range(4), repeat=length):
        w = I
        for letter in word:
            w = mm(w, alphabet[letter])
        ck(determinant(w) == one, 'word_determinant')
        # The character lies in Q[u] for this rotation pair, even though
        # individual entries use v. This is finite corroboration only.
        ck(all(j == 0 for i,j in trace(w)), 'trace_in_character_field')
        word_controls += 1

admissible = []
for N in range(7, 1001):
    characteristic = Q(1)-Q(N,6)
    genus = (Q(2)-characteristic)/2
    is_integer = genus.denominator == 1
    ck(is_integer == (N % 12 == 6), 'cubic_index_genus_parity')
    if is_integer:
        g = int(genus)
        ck(g >= 2 and N == 12*g-6, 'cubic_genus_signature')
        orb_area_over_pi = Q(1,3)-Q(2,N)
        ck(N*orb_area_over_pi == 4*(g-1), 'orientation_preserving_area_index')
        # A reflection triangle has half the orbifold area: confusing
        # those conventions doubles the purported index.
        ck(Q(4*(g-1),1)/(orb_area_over_pi/2) == 2*N, 'reflection_group_negative_control')
        admissible.append(N)

# A deterministic scale a maps rho(t) to rho(t/a)/a. Its t coefficient
# is 1/(2*a^2); for positive a this can equal the source 1/2 only at a=1.
for a in [Q(1,4),Q(1,2),Q(1),Q(3,2),Q(2),Q(3)]:
    ck((Q(1,2)/a**2 == Q(1,2)) == (a == 1), 'scale_density_first_coefficient')
    ck((Q(1,24)/a**4 == Q(1,24)) == (a == 1), 'scale_density_third_coefficient')

print(json.dumps({
    'status': 'PASS',
    'assertions': sum(counts.values()),
    'by_scope': dict(counts),
    'word_controls': word_controls,
    'maximum_word_length': 5,
    'signature_control_range': [7,1000],
    'admissible_cubic_signatures': len(admissible),
    'scope': 'Exact supplementary symbolic triangle-character, index/parity and scaling controls. No finite word search certifies Philippe classification, discreteness, transcendence or an infinite probability law.'
}, indent=2, sort_keys=True))
