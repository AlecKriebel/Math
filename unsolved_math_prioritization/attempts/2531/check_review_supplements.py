#!/usr/bin/env python3
"""Independent finite controls for frozen 2531 claims; not new theorem research."""
import itertools
import json
import random

counts = {}
def check(label, truth):
    assert truth, label
    counts[label] = counts.get(label, 0) + 1

# An infinite-line restricted base, with an unrestricted step conjugator.
# Its resulting cocycle has finite support, but is not a restricted coboundary.
P = list(itertools.permutations(range(3)))
def compose(a, b):
    return tuple(a[b[i]] for i in range(3))
pi = {p: i for i, p in enumerate(P)}
table = [[pi[compose(a, b)] for b in P] for a in P]
inv = [next(j for j in range(6) if table[i][j] == table[j][i] == 0)
       for i in range(6)]
one = (0, 0)
def mul(a, b):
    return (table[a[0]][b[0]], table[a[1]][b[1]])
def inverse(a):
    return (inv[a[0]], inv[a[1]])
def conjugate(a, b):
    return mul(mul(a, b), inverse(a))
def get(f, y):
    return f.get(y, one)
def step(y):
    return (1, 3) if y >= 0 else one
def clean(f):
    return {y: a for y, a in f.items() if a != one}
def cocycle(h, y):
    return mul(step(y), inverse(step(y - h)))
def forward(f):
    ys = set(f) | {h + 2 for h in f}
    return clean({y: conjugate(step(y), (get(f, y)[1], get(f, y - 2)[0]))
                  for y in ys})
def backward(w):
    hs = set(w) | {y - 2 for y in w}
    untwist = lambda y: conjugate(inverse(step(y)), get(w, y))
    return clean({h: (untwist(h + 2)[1], untwist(h)[0]) for h in hs})
def translate(f, h):
    return {y + h: a for y, a in f.items()}
rng = random.Random(253199)
for _ in range(1200):
    f = clean({y: (rng.randrange(6), rng.randrange(6))
               for y in rng.sample(range(-20, 21), rng.randrange(10))})
    w = forward(f)
    check('sparse_inverse', backward(w) == f)
    check('sparse_forward_support', set(w) <= set(f) | {h + 2 for h in f})
    check('sparse_inverse_support', set(f) <= set(w) | {y - 2 for y in w})
    h = rng.randrange(-12, 13)
    lhs = forward(translate(f, h))
    rhs = clean({y: conjugate(cocycle(h, y), get(w, y - h))
                 for y in {x + h for x in w}})
    check('sparse_covariance', lhs == rhs)
for h, k in itertools.product(range(-12, 13), repeat=2):
    for y in range(-30, 31):
        check('step_cocycle', cocycle(h + k, y) ==
              mul(cocycle(h, y), cocycle(k, y - h)))
check('nontrivial_step_jump', cocycle(1, 0) != one)
check('step_jump_support', all(cocycle(1, y) == one
                               for y in range(-30, 31) if y != 0))

# Central presentation with TWO torsion generators and a free generator.
# C=(Z/16)^2, A=Z/2 + Z/4 + Z, rho=5 id. rho is identity mod 4C,
# but not identity on C. This separately tests nonfree, noncyclic C.
n = (2, 4)
c = ((1, 3), (2, 1))
b = ((2, 6), (2, 1))
def addv(x, y):
    return tuple((a + d) % 16 for a, d in zip(x, y))
def scale(k, x):
    return tuple(k * a % 16 for a in x)
def add(x, y):
    v = addv(x[0], y[0])
    residues = []
    for i in range(2):
        carry, residue = divmod(x[1][i] + y[1][i], n[i])
        v = addv(v, scale(carry, c[i]))
        residues.append(residue)
    return (v, tuple(residues), x[2] + y[2])
def theta(x):
    v = scale(5, x[0])
    for i in range(2):
        v = addv(v, scale(x[1][i], b[i]))
    return (v, x[1], x[2])
zero = ((0, 0), (0, 0), 0)
gens = [((1, 0), (0, 0), 0), ((0, 1), (0, 0), 0),
        ((0, 0), (1, 0), 0), ((0, 0), (0, 1), 0),
        ((0, 0), (0, 0), 1)]
finite_part = [((u, v), (s, t), 0) for u, v, s, t in
               itertools.product(range(16), range(16), range(2), range(4))]
check('central_rho_nonidentity', scale(5, (1, 0)) != (1, 0))
for x in finite_part:
    check('central_quotient_identity', theta(x)[1:] == x[1:])
    for g in gens:
        check('central_presentation_generator_homomorphism',
              theta(add(x, g)) == add(theta(x), theta(g)))
check('central_finite_fiber_bijection', len({theta(x) for x in finite_part}) == len(finite_part))
check('central_free_generator_fixed', theta(gens[-1]) == gens[-1])
for i in range(2):
    check('central_relation', addv(c[i], scale(n[i], b[i])) == scale(5, c[i]))

print(json.dumps({'status': 'PASS', 'assertions': sum(counts.values()),
                  'categories': counts,
                  'scope': 'Independent finite identity controls for written proofs; no proof of the original question.'},
                 indent=2, sort_keys=True))
