#!/usr/bin/env python3
"""Independent exact controls for the finite and Laurent-module calculations.

No numerical test here establishes duality, knot realization or classification.
Uses the standard library. Does not import the submitted verifier.
"""
from itertools import product
import json

counts = {}
def check(condition, category):
    assert condition, category
    counts[category] = counts.get(category, 0) + 1

# Construct A as permutations, with composition defined independently.
identity = tuple(range(7))
a = (0, 2, 4, 6, 1, 3, 5)
b = (1, 2, 3, 4, 5, 6, 0)
def compose(p, q):
    return tuple(p[q[i]] for i in range(7))
group, frontier = {identity}, [identity]
while frontier:
    p = frontier.pop()
    for g in (a, b):
        q = compose(g, p)
        if q not in group:
            group.add(q)
            frontier.append(q)
check(len(group) == 21, 'permutation_group')
check(len({p for p in group if p[0] == 0}) == 3, 'permutation_group')

# Quotient by the diagonal: choose the representative with final coordinate 0.
def quotient(v):
    return tuple(x - v[-1] for x in v[:-1])
def lift(v):
    return tuple(v) + (0,)
def permute(p, v):
    out = [0] * 7
    for i, x in enumerate(v):
        out[p[i]] = x
    return tuple(out)
def act(p, v):
    return quotient(permute(p, lift(v)))
basis = [tuple(int(i == j) for i in range(6)) for j in range(6)]
for p, q in product(group, repeat=2):
    for e in basis:
        check(act(p, act(q, e)) == act(compose(p, q), e), 'quotient_representation')
for v in product((-1, 0, 1), repeat=7):
    check((quotient(v) == (0,) * 6) == (len(set(v)) == 1), 'primitive_diagonal_kernel')
    # The sum modulo 7 is well-defined on this quotient and invariant under A.
    for p in (a, b):
        check(sum(quotient(permute(p, v))) % 7 == sum(quotient(v)) % 7,
              'quotient_coinvariant_control')

# B=C3 semidirect Z in normal form a^i t^n, with t a t^-1=a^-1.
def bmul(x, y):
    i, n = x
    j, m = y
    return ((i + (-1 if n % 2 else 1) * j) % 3, n + m)
def binv(x):
    i, n = x
    return (((-1 if n % 2 else 1) * -i) % 3, -n)
window = [(i, n) for i in range(3) for n in range(-4, 5)]
for x in window:
    check(bmul(x, binv(x)) == bmul(binv(x), x) == (0, 0), 'semidirect_normal_form')
    for y in window:
        for z in window:
            check(bmul(bmul(x, y), z) == bmul(x, bmul(y, z)), 'semidirect_normal_form')

# In each regular B block, N_C t^n spans R^C as a Laurent module.
# Left T-orbits are labelled by the representative a^((-1)^n i).
def t_coset(x):
    i, n = x
    return ((-1 if n % 2 else 1) * i) % 3
for x in window:
    for k in range(-4, 5):
        check(t_coset(bmul((0, k), x)) == t_coset(x), 'T_coinvariant_labels')
for n in range(-10, 11):
    norm = {(i, n) for i in range(3)}
    shifted = {bmul((0, 1), x) for x in norm}
    check(shifted == {(i, n + 1) for i in range(3)}, 'C_invariant_shift')
    counts_by_coset = tuple(sum(t_coset(x) == j for x in norm) for j in range(3))
    check(counts_by_coset == (1, 1, 1), 'restriction_diagonal')

# Laurent polynomials in a five-term window: (t-1) kills the total coefficient;
# restriction of an invariant representative has that total in every T-orbit.
for coeffs in product((-1, 0, 1), repeat=5):
    total = sum(coeffs)
    restricted = [0, 0, 0]
    for n, coefficient in zip(range(-2, 3), coeffs):
        for i in range(3):
            restricted[t_coset((i, n))] += coefficient
    check(restricted == [total] * 3, 'restriction_diagonal')
    check((restricted == [0] * 3) == (total == 0), 'restriction_injectivity_control')
    difference = [-coeffs[0]] + [coeffs[i - 1] - coeffs[i] for i in range(1, 5)] + [coeffs[-1]]
    check(sum(difference) == 0, 'Laurent_difference')

print(json.dumps({
    'status': 'PASS',
    'exact_assertions': sum(counts.values()),
    'categories': counts,
    'limits': ['Finite and finite-support arithmetic only',
               'No computational proof of group cohomology or Poincare duality',
               'No exterior realization or complete 2-type comparison'],
}, indent=2))
