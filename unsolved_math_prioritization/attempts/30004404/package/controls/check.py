#!/usr/bin/env python3
"""Exact finite controls for the metabelian-filling obstruction.

Not a verifier of the imported topological classification, a proof assistant,
or an exhaustive knot/slope search. Python standard library only.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json


def reduce_word(word):
    stack = []
    for letter in word:
        assert letter in (-2, -1, 1, 2)
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def inverse_word(word):
    return tuple(-letter for letter in reversed(word))


def commutator_word(a, b):
    return reduce_word(a + b + inverse_word(a) + inverse_word(b))


x, y = (1,), (2,)
c = commutator_word(x, y)
d = reduce_word(x + c + inverse_word(x))
w = commutator_word(c, d)
word_text = ''.join({1: 'x', -1: 'X', 2: 'y', -2: 'Y'}[v] for v in w)
assert word_text == 'xyXYxxyXYXyxxYXX'
assert len(w) == 16
assert all(w[i] != -w[i+1] for i in range(len(w)-1))
assert reduce_word(w + inverse_word(w)) == ()
assert commutator_word(x, x) == ()  # cancellation negative control
assert reduce_word((1, 2, -2, -1)) == ()

A = ((2, 1), (1, 1))
AI = ((1, -1), (-1, 2))
I = ((1, 0), (0, 1))


def mm(a, b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def mv(a, v):
    return tuple(sum(a[i][k]*v[k] for k in range(2)) for i in range(2))


@lru_cache(None)
def power(n):
    if n == 0:
        return I
    if n > 0:
        return mm(A, power(n-1))
    return mm(AI, power(n+1))


assert mm(A, AI) == mm(AI, A) == I
assert A[0][0]*A[1][1]-A[0][1]*A[1][0] == 1
assert A[0][0]+A[1][1] == 3
E = ((0, 0), 0)


def mul(a, b):
    v, n = a
    u, m = b
    au = mv(power(n), u)
    return ((v[0]+au[0], v[1]+au[1]), n+m)


def inv(a):
    v, n = a
    av = mv(power(-n), v)
    return ((-av[0], -av[1]), -n)


def comm(a, b):
    return mul(mul(mul(a, b), inv(a)), inv(b))


def evaluate(word, a, b):
    values = {1: a, -1: inv(a), 2: b, -2: inv(b)}
    out = E
    for letter in word:
        out = mul(out, values[letter])
    return out


# These are bounded model checks only; §3 of PROOF.md proves the universal law.
elements = [((u, v), n) for u, v, n in product(range(-2, 3), range(-2, 3), range(-3, 4))]
for a in elements:
    assert mul(a, inv(a)) == mul(inv(a), a) == E
    assert mul(E, a) == mul(a, E) == a
pairs = 0
noncommuting_pairs = 0
for a in elements:
    for b in elements:
        ab = comm(a, b)
        assert ab[1] == 0
        aba = mul(mul(a, ab), inv(a))
        assert comm(ab, aba) == E
        assert evaluate(w, a, b) == E
        noncommuting_pairs += ab != E
        pairs += 1
assert noncommuting_pairs > 0
# A model erroneously made abelian would fail this control.
t, u = ((0, 0), 1), ((1, 0), 0)
assert comm(t, u) == ((1, 1), 0)
assert evaluate(c, t, u) != E
# A model with x/y exchanged is not used to prove the law.
assert evaluate((1,), t, u) == t
assert evaluate((2,), t, u) == u

bases = [(2, 3, 7), (2, 4, 5), (3, 3, 4)]
chi = [sum((Fraction(1, v) for v in b), Fraction(-1)) for b in bases]
assert chi == [Fraction(-1, 42), Fraction(-1, 20), Fraction(-1, 12)]
assert all(v < 0 for v in chi)
# Boundary and opposite-sign controls reject conflating all Seifert bases.
assert sum((Fraction(1, v) for v in (2, 3, 6)), Fraction(-1)) == 0
assert sum((Fraction(1, v) for v in (2, 3, 5)), Fraction(-1)) == Fraction(1, 30)
exceptional = set(range(-4, 5))
toroidal = {0, -4, 4}
small_seifert = {-3, -2, -1, 1, 2, 3}
assert toroidal.isdisjoint(small_seifert)
assert toroidal | small_seifert == exceptional
assert 0 in exceptional

print(json.dumps({
    'result': 'PASS',
    'free_reduced_witness': word_text,
    'free_reduced_length': len(w),
    'model': 'Z^2 semidirect_A Z, A=[[2,1],[1,1]]',
    'element_box': {'vector_coordinates': [-2, 2], 'exponent': [-3, 3]},
    'elements': len(elements),
    'ordered_pairs': pairs,
    'noncommuting_ordered_pairs': noncommuting_pairs,
    'witness_evaluations_equal_identity': pairs,
    'orbifold_euler_characteristics': [str(v) for v in chi],
    'exceptional_rational_slopes_from_cited_classification': sorted(exceptional),
    'limits': ['Not a topology classification check', 'Not formal proof verification',
               'No finite search proves the all-slope assertion',
               'Universal algebraic argument is in PROOF.md']
}, sort_keys=True, indent=2))
