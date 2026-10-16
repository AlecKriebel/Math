#!/usr/bin/env python3
"""Fresh exact audit. Checks finite algebra only, never source/topology claims."""
from fractions import Fraction
from itertools import permutations
from pathlib import Path
from datetime import datetime, timezone
import json

def reduce_word(w):
    r = []
    for a in w:
        if r and r[-1] == -a:
            r.pop()
        else:
            r.append(a)
    return tuple(r)

def inv(w):
    return tuple((-a for a in reversed(w)))

def subst(w, phi):
    return reduce_word((a for letter in w for a in (phi[letter - 1] if letter > 0 else inv(phi[-letter - 1]))))

def compose(phi, psi):
    return tuple((subst(w, phi) for w in psi))
identity = tuple(((i,) for i in range(1, 4)))

def sigma(i, inverse=False):
    phi = list(identity)
    if not inverse:
        phi[i - 1] = (i, i + 1, -i)
        phi[i] = (i,)
    else:
        phi[i - 1] = (i + 1,)
        phi[i] = (-(i + 1), i, i + 1)
    return tuple(phi)
a, b = (sigma(1), sigma(2))
ai, bi = (sigma(1, True), sigma(2, True))
if not compose(a, ai) == identity == compose(ai, a):
    raise AssertionError('Exact audit check failed at original checker line 25')
if not compose(b, bi) == identity == compose(bi, b):
    raise AssertionError('Exact audit check failed at original checker line 26')
if not compose(compose(a, b), a) == compose(compose(b, a), b):
    raise AssertionError('Exact audit check failed at original checker line 27')
A, B = (compose(a, a), compose(b, b))
Ai, Bi = (compose(ai, ai), compose(bi, bi))
beta = compose(compose(compose(A, B), Ai), Bi)
beta_inv = compose(compose(compose(B, A), Bi), Ai)
if not compose(beta, beta_inv) == identity:
    raise AssertionError('Exact audit check failed at original checker line 31')

def normalized_conjugator(image, j):
    w = list(image)
    prefix = []
    while len(w) > 1 and w[0] == -w[-1]:
        prefix.append(w[0])
        w = w[1:-1]
    if not w == [j]:
        raise AssertionError('Exact audit check failed at original checker line 37')
    exp = sum((1 if a == j else -1 if a == -j else 0 for a in prefix))
    normalize = (-j,) * exp if exp >= 0 else (j,) * -exp
    return reduce_word(tuple(prefix) + normalize)
conjugators = [normalized_conjugator(beta[j - 1], j) for j in range(1, 4)]
submitted = [(1, 2, -1, 3, 1, -2, -1, -3), (-3, -1, 3, 1), (-3, -1, 3, 1, -2, -1, -3, 1, 3, 1, 2, -1)]
if not conjugators == submitted:
    raise AssertionError('Exact audit check failed at original checker line 43')
for j, c in enumerate(conjugators, 1):
    if not reduce_word(c + (j,) + inv(c)) == beta[j - 1]:
        raise AssertionError('Exact audit check failed at original checker line 45')
    if not sum((1 if a == j else -1 if a == -j else 0 for a in c)) == 0:
        raise AssertionError('Exact audit check failed at original checker line 46')

def poly_add(p, q):
    r = p.copy()
    for mon, c in q.items():
        r[mon] = r.get(mon, Fraction(0)) + c
    return {m: c for m, c in r.items() if c}

def poly_mul(p, q, degree=2):
    r = {}
    for m, c in p.items():
        for n, d in q.items():
            if len(m + n) <= degree:
                r[m + n] = r.get(m + n, Fraction(0)) + c * d
    return {m: c for m, c in r.items() if c}

def magnus(w, degree=2):
    result = {(): Fraction(1)}
    for a in w:
        i = abs(a)
        term = {(): Fraction(1), (i,): Fraction(1 if a > 0 else -1)}
        if a < 0:
            for d in range(2, degree + 1):
                term[(i,) * d] = Fraction((-1) ** d)
        result = poly_mul(result, term, degree)
    return result
expected = [{(): Fraction(1), (2, 3): Fraction(1), (3, 2): Fraction(-1)}, {(): Fraction(1), (1, 3): Fraction(-1), (3, 1): Fraction(1)}, {(): Fraction(1), (1, 2): Fraction(1), (2, 1): Fraction(-1)}]
if not [magnus(c) for c in conjugators] == expected:
    raise AssertionError('Exact audit check failed at original checker line 70')
if not magnus(inv(conjugators[2]))[1, 2] == -1:
    raise AssertionError('Exact audit check failed at original checker line 71')
if not compose(A, B) != compose(B, A):
    raise AssertionError('Exact audit check failed at original checker line 72')
for omitted in (1, 2, 3):
    for j, w in enumerate(beta, 1):
        if j != omitted:
            if not reduce_word((a for a in w if abs(a) != omitted)) == (j,):
                raise AssertionError('Exact audit check failed at original checker line 75')
    for j, c in enumerate(conjugators, 1):
        if j != omitted:
            if not reduce_word((a for a in c if abs(a) != omitted)) == ():
                raise AssertionError('Exact audit check failed at original checker line 77')
q = ((4,), (4, 5), (5, -4))
phi = tuple((reduce_word(q[i] + (i + 1,) + inv(q[i])) for i in range(3)))
for c, expected_poly in zip(conjugators, expected):
    if not magnus(subst(c, phi)) == expected_poly:
        raise AssertionError('Exact audit check failed at original checker line 81')
for c in conjugators:
    if not magnus((4, 5) + c + (-5, -4)) == magnus(c):
        raise AssertionError('Exact audit check failed at original checker line 82')


# Supplemental unrestricted whisker check, added after inspecting the historical
# audit: the mathematical proof is that beta acts identically modulo Gamma_3.
beta5=beta+((4,),(5,))
whiskers=[(1,), (2,), (3,), (4,), (5,), (1,2), (4,1,-4), (3,5,1,-5), (2,-1,3)]
for whisker in whiskers:
    factor=reduce_word(subst(whisker,beta5)+inv(whisker))
    if magnus(factor)!={():Fraction(1)}:
        raise AssertionError('Whisker factor changed degree <= 2')
    for c in conjugators:
        changed=reduce_word(subst(whisker,beta5)+c+inv(whisker))
        if magnus(changed)!=magnus(c):
            raise AssertionError('Full whisker change modified degree-two longitude')
third_order=reduce_word(subst((1,),beta5)+(-1,))
if magnus(third_order,3)=={():Fraction(1)}:
    raise AssertionError('Whisker degree-three negative control was trivial')

def det(matrix):
    n = len(matrix)
    value = Fraction(0)
    for p in permutations(range(n)):
        parity = sum((p[i] > p[j] for i in range(n) for j in range(i + 1, n)))
        product = Fraction((-1) ** parity)
        for i, j in enumerate(p):
            product *= matrix[i][j]
        value += product
    return value
if not det([[2, 0, 0], [0, 2, 0], [2, 2, -4]]) == -16:
    raise AssertionError('Exact audit check failed at original checker line 95')
if not det([[1, 1], [1, 1]]) == -24:
    raise AssertionError('Exact audit check failed at original checker line 96')
for z in range(-7, 8):
    if not det([[1, 0, 0, 0], [1, 1, 1, 0], [1, -1, 1, 0], [1, z, z * z, 1]]) == 2:
        raise AssertionError('Exact audit check failed at original checker line 98')
for z in range(-6, 7):
    r, s, t, u, v = (Fraction(z, 3), Fraction(z + 1, 5), Fraction(2 * z - 3, 7), Fraction(z - 4, 11), Fraction(z + 3, 13))
    mat = [[1, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0], [1, -1, 1, 0, 0, 0], [1, r, r * r, 0, 0, 1], [1, s, s * s, 1, 5, u], [1, t, t * t, 5, 1, v]]
    if not det(mat) == -48:
        raise AssertionError('Exact audit check failed at original checker line 103')
    if not det([row[:5] + [0] for row in mat]) == 0:
        raise AssertionError('Exact audit check failed at original checker line 104')
terms = {3: 1, 2: -1, 0: 1, -2: -1, -3: 1}
a2 = sum((Fraction(c * e * (e - 1), 2) for e, c in terms.items()))
if not (sum(terms.values()) == 1 and a2 == 5):
    raise AssertionError('Exact audit check failed at original checker line 110')

def laurent_mul(p, q):
    r = {}
    for i, a in p.items():
        for j, b in q.items():
            r[i + j] = r.get(i + j, 0) + a * b
    return {k: v for k, v in r.items() if v}
normalized = {e + 3: c for e, c in terms.items()}
if not laurent_mul(normalized, laurent_mul({0: 1, 3: -1}, {0: 1, 4: -1})) == laurent_mul({0: 1, 1: -1}, {0: 1, 12: -1}):
    raise AssertionError('Exact audit check failed at original checker line 118')
if not Fraction((3 * 3 - 1) * (4 * 4 - 1), 24) == a2:
    raise AssertionError('Exact audit check failed at original checker line 119')
output = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS', 'python': 'standard-library exact integer/Fraction arithmetic', 'scope': 'finite free-word/Artin/Magnus/determinant/Alexander arithmetic only', 'topological_or_source_theorems_machine_certified': False, 'beta_images': [list(w) for w in beta], 'derived_normalized_conjugators': [list(w) for w in conjugators], 'magnus_degree_two': [{','.join(map(str, m)): str(c) for m, c in p.items()} for p in expected], 'determinants': {'slice': -16, 'span': 2, 'component_pair': -24, 'six_rows': -48}, 'torus_a2': str(a2), 'negative_controls': ['A and B do not commute', 'inverse triple coefficient changes sign', 'zero w column destroys six-row determinant', 'conjugated meridian/longitude basing preserves degree-two leading term']}
path = Path(__file__).with_name('CHECK_RESULT.json')
path.write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps(output, indent=2))
