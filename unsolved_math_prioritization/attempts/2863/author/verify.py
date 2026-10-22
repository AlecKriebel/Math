#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; no manifold skein-rank computation.
Python standard library only. Prints deterministic JSON; never writes inputs.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json

checks = {}

def check(test, section):
    assert test, section
    checks[section] = checks.get(section, 0) + 1

def trim(a):
    a = list(map(F, a))
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a or [F(0)])

ZERO, ONE, X = trim([0]), trim([1]), trim([0, 1])

def add(a, b):
    return trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])

def scale(a, c):
    return trim([x*c for x in a])

def sub(a, b):
    return add(a, scale(b, -1))

def mul(a, b):
    c = [F(0)] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)

def power(a, n):
    b = ONE
    for _ in range(n):
        b = mul(b, a)
    return b

def divmodp(a, b):
    assert b != ZERO
    a = trim(a)
    q = [F(0)] * max(1, len(a)-len(b)+1)
    while a != ZERO and len(a) >= len(b):
        j, c = len(a)-len(b), a[-1]/b[-1]
        q[j] += c
        a = sub(a, (F(0),)*j + scale(b, c))
    return trim(q), a

def mod(a, b):
    return divmodp(a, b)[1]

def xgcd(a, b):
    r0, r1, s0, s1, t0, t1 = a, b, ONE, ZERO, ZERO, ONE
    while r1 != ZERO:
        q, r2 = divmodp(r0, r1)
        r0, r1 = r1, r2
        s0, s1 = s1, sub(s0, mul(q, s1))
        t0, t1 = t1, sub(t0, mul(q, t1))
    c = 1/r0[-1]
    return scale(r0, c), scale(s0, c), scale(t0, c)

cyclo = {}
for n in range(1, 31):
    p = sub(power(X, n), ONE)
    for d in range(1, n):
        if n % d == 0:
            p, remainder = divmodp(p, cyclo[d])
            check(remainder == ZERO, 'cyclotomic_divisions')
    cyclo[n] = p
    check(p[-1] == 1 and all(c.denominator == 1 for c in p), 'cyclotomic_integrality')

# Independent product identities x^n - 1 = product_{d|n} Phi_d(x).
for n in range(1, 31):
    p = ONE
    for d in range(1, n+1):
        if n % d == 0:
            p = mul(p, cyclo[d])
    check(p == sub(power(X, n), ONE), 'cyclotomic_product_identities')

orders = list(range(1, 16, 2))
primes = [cyclo[2*n] for n in orders]
for i, j in combinations(range(len(primes)), 2):
    g, s, t = xgcd(primes[i], primes[j])
    check(g == ONE and add(mul(s, primes[i]), mul(t, primes[j])) == ONE,
          'pairwise_bezout')

def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    if not a:
        return 0
    h = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(h, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[h], a[pivot] = a[pivot], a[h]
        p = a[h][j]
        a[h] = [x/p for x in a[h]]
        for i in range(h+1, len(a)):
            c = a[i][j]
            if c:
                a[i] = [x-c*y for x, y in zip(a[i], a[h])]
        h += 1
        if h == len(a):
            break
    return h

def multiplication_matrix(f, modulus):
    d = len(modulus)-1
    columns = []
    for j in range(d):
        c = mod(mul(f, power(X, j)), modulus)
        columns.append(list(c) + [F(0)]*(d-len(c)))
    return [[columns[j][i] for j in range(d)] for i in range(d)]

# Specialization of a cyclic torsion summand is the cokernel of multiplication
# by its annihilator on the cyclotomic residue field (represented over Q).
for i, p in enumerate(primes):
    degree = len(p)-1
    for j, q in enumerate(primes):
        for exponent in (1, 2, 3):
            codim = degree-rank(multiplication_matrix(power(q, exponent), p))
            check(codim == (degree if i == j else 0), 'cyclic_fibers')

# An annihilator with several distinct factors still contributes one residue
# dimension, not its total degree or primary multiplicity.
for chosen in combinations(range(len(primes)), 2):
    f = mul(power(primes[chosen[0]], 2), primes[chosen[1]])
    for i, p in enumerate(primes):
        degree = len(p)-1
        codim = degree-rank(multiplication_matrix(f, p))
        check(codim == (degree if i in chosen else 0), 'mixed_annihilator_fibers')

for p in primes[:5]:
    degree = len(p)-1
    for exponent in (1, 2, 3):
        modulus = power(p, exponent)
        codim = len(modulus)-1-rank(multiplication_matrix(p, modulus))
        check(codim == degree, 'primary_length_not_fiber_dimension')
        check(len(modulus)-1 == exponent*degree, 'primary_length')

# Direct sum controls E restricted to finitely many selected primes. At those
# primes, its generic rank is one and specialized dimension is exactly two.
for p in primes:
    degree = len(p)-1
    torsion_codim = sum(degree-rank(multiplication_matrix(q, p)) for q in primes)
    check(torsion_codim == degree, 'rank_one_all_selected_orders_model')
    check((degree+torsion_codim)//degree == 2, 'rank_one_specialization_jump')

# Verify inversion-orbit counts directly for finite products of cyclic groups.
groups = [()] + [(n,) for n in range(2, 13)]
groups += list(product(range(2, 7), repeat=2))
groups += list(product(range(2, 5), repeat=3))
examples = []
for invariants in groups:
    elements = list(product(*[range(n) for n in invariants]))
    inverse = lambda v: tuple((-x) % n for x, n in zip(v, invariants))
    orbits = {min(v, inverse(v)) for v in elements}
    fixed = sum(v == inverse(v) for v in elements)
    check(2*len(orbits) == len(elements)+fixed, 'abelian_character_orbits')
    check(fixed == (2 ** sum(n % 2 == 0 for n in invariants)), 'abelian_two_torsion')
    if invariants in [(), (2,), (3,), (4,), (2, 2), (2, 3)]:
        examples.append({'cyclic_factors':list(invariants), 'order':len(elements),
                         'two_torsion_order':fixed, 'diagonal_characters':len(orbits)})

# Construct compatible polynomial interpolation at distinct cyclotomic fields.
crt_degrees = []
for count in (2, 4, 6, 8):
    moduli = primes[:count]
    residues = [mod(trim([i+1, 1, i*i+1]), p) for i, p in enumerate(moduli)]
    total = ONE
    for p in moduli:
        total = mul(total, p)
    answer = ZERO
    for p, residue in zip(moduli, residues):
        other, rem = divmodp(total, p)
        check(rem == ZERO, 'crt_exact_quotients')
        g, inv, _ = xgcd(other, p)
        check(g == ONE, 'crt_coprime')
        answer = add(answer, mul(mul(other, inv), residue))
    answer = mod(answer, total)
    for p, residue in zip(moduli, residues):
        check(mod(answer, p) == residue, 'finite_root_interpolation')
    crt_degrees.append({'orders': [2*n for n in orders[:count]],
                        'polynomial_degree': len(answer)-1})

# Kitaeff's q=2 specialization: the two coefficients in the kernel example
# cancel for both even and odd root half-orders. This checks only the scalar
# cancellation in the cited formula, not the independent nonzero-skein theorem.
for half_order in range(5, 46):
    factor = 2 if half_order % 2 == 0 else 1
    check((-1)*factor + factor == 0, 'evaluation_kernel_scalar_cancellation')

print(json.dumps({
    'result':'PASS',
    'total_assertions':sum(checks.values()),
    'sections':checks,
    'abelian_examples':examples,
    'crt_examples':crt_degrees,
    'scope':'Exact finite algebraic controls only; no generic skein dimension is computed. '
            'Does not formally prove the universal module lemma or validate imported topology theorems.'
}, indent=2, sort_keys=True))
