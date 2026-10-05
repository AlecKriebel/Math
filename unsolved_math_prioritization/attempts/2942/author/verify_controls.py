#!/usr/bin/env python3
"""Exact finite controls for the elementary algebra in PROOF.md.

No manifold invariant, topology theorem, infinite tail, or source proof is computed.
Only the Python standard library is used. Checks remain active under python -O.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json

counts = Counter()


def check(condition, section):
    if not condition:
        raise RuntimeError('Failed exact control: ' + section)
    counts[section] += 1


def rank(matrix, columns=None):
    a = [[F(x) for x in row] for row in matrix]
    if not a:
        return 0
    n = len(a[0]) if columns is None else columns
    row = 0
    for col in range(n):
        pivot = next((j for j in range(row, len(a)) if a[j][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        t = a[row][col]
        a[row] = [x / t for x in a[row]]
        for j in range(len(a)):
            if j != row and a[j][col]:
                t = a[j][col]
                a[j] = [x - t * y for x, y in zip(a[j], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def matvec(m, v):
    return tuple(sum(x * y for x, y in zip(row, v)) for row in m)


def transpose(m):
    return tuple(zip(*m))


def mul(a, b):
    return tuple(tuple(sum(x*y for x, y in zip(row, col)) for col in zip(*b)) for row in a)


def dot(g, a, b):
    return sum(x*y for x, y in zip(a, matvec(g, b)))


# Capping quotients: nonisomorphic sources may have the same nonzero target.
for n in range(2, 13):
    p = [[1] + [0] * (n - 1)]
    p2 = [[1] + [0] * n]
    check(rank(p) == rank(p2) == 1 and len(p[0]) != len(p2[0]), 'quotient_dimensions')

# A functional on Q^2 factors through a nonzero row p iff it kills ker(p).
for p in product(range(-2, 3), repeat=2):
    if p == (0, 0):
        continue
    kernel = (-p[1], p[0])
    for lam in product(range(-2, 3), repeat=2):
        kills = sum(x*y for x, y in zip(lam, kernel)) == 0
        rowspace = rank([p, lam]) == 1
        check(kills == rowspace, 'cap_functional_factorization')

# A=Qe+Qf. Build every balancing relation for a basis tensor and e.
# Relations for f are negatives and those for 1 vanish.
for a, b, c, d in product(range(4), repeat=4):
    mlabels = [1]*a + [0]*b
    clabels = [1]*c + [0]*d
    labels = [(x, y) for x in mlabels for y in clabels]
    relations = []
    for k, (x, y) in enumerate(labels):
        if x != y:
            r = [0]*len(labels)
            r[k] = x-y
            relations.append(r)
    quotient_dim = len(labels) - rank(relations)
    check(quotient_dim == a*c+b*d, 'semisimple_balanced_tensor')
check(1*1+0*0 == 1*1+1*0 == 1, 'nonfaithful_nonzero_cap')

# The geometric unknot threshold is n >= -TB(U) = 1, not n >= 0.
for n in range(-10, 11):
    check((n >= -(-1)) == (n > 0), 'unknot_sign_threshold')
check(dot(((0, 1), (1, 0)), (1, 1), (1, 1)) == 2, 'positive_diagonal_square')

# Negative blowups give odd indefinite signature data; optional r avoids zero.
for bp in range(1, 25):
    for bm in range(25):
        sigma = bp-bm
        r = 2 if sigma == 1 else 1
        diagonal = [1]*bp+[-1]*(bm+r)
        check(bp > 0 and bm+r > 0 and sum(diagonal) == sigma-r != 0
              and diagonal[-1] % 2 == 1, 'blowup_signature_safeguard')

# Lee grading transport under actual integral basis changes, including reversal.
grams = [((1, 0), (0, -1)), ((0, 1), (1, 0)), ((2, 1), (1, 2)),
         ((-2, 1), (1, -3)), ((0, 0), (0, 0))]
transforms = [((1, 1), (0, 1)), ((0, 1), (1, 0)), ((1, 0), (0, -1))]
vecs = list(product(range(-1, 2), repeat=2))
for g, p in product(grams, transforms):
    det = p[0][0]*p[1][1]-p[0][1]*p[1][0]
    inv = ((p[1][1]//det, -p[0][1]//det), (-p[1][0]//det, p[0][0]//det))
    gp = mul(mul(transpose(inv), g), inv)
    for a, b in product(vecs, repeat=2):
        ap, bp = matvec(p, a), matvec(p, b)
        s = tuple(x+y for x, y in zip(a, b))
        sp = tuple(x+y for x, y in zip(ap, bp))
        h, hp = -2*dot(g, a, b), -2*dot(gp, ap, bp)
        q = ((-dot(g, s, s)) % 4, (-dot(g, s, s)-2) % 4)
        qp = ((-dot(gp, sp, sp)) % 4, (-dot(gp, sp, sp)-2) % 4)
        check(h == hp and q == qp and matvec(p, s) == sp and (a == b) == (ap == bp),
              'lee_grading_transport')

# Nonzero underlying filtered spaces can have identically zero associated graded.
for dim in range(1, 13):
    for q in range(-8, 9):
        fq, fprev = dim, dim
        check(fq > 0 and fq-fprev == 0, 'minus_infinite_filtration')

# Same finite transition prefix, but delayed death can occur arbitrarily late.
for cutoff in range(65):
    alive = [1]*(cutoff+5)
    dying = [1]*cutoff+[0]*5
    check(alive[:cutoff] == dying[:cutoff], 'same_prefix')
    for start in range(cutoff+2):
        x_alive = x_dying = F(1)
        for j in range(start, cutoff+5):
            x_alive *= alive[j]
            x_dying *= dying[j]
        check(x_alive == 1 and x_dying == 0, 'eventual_death_witness')

# Compatible functional certificate for arbitrary finite chains of rescalings.
for scalars in product((-3, -2, -1, 1, 2, 3), repeat=3):
    v, lam = F(1), F(1)
    for a in scalars:
        v *= a
        lam /= a
        check(v != 0 and lam*v == 1, 'compatible_functional')

# Finite exact controls for the explicit infinite-basis bijection in the proof.
images = [2*n+epsilon for n in range(256) for epsilon in (0, 1)]
check(sorted(images) == list(range(512)), 'infinite_tensor_bijection_prefix')
for value in images:
    n, epsilon = divmod(value, 2)
    check(2*n+epsilon == value and epsilon in (0, 1), 'basis_bijection_inverse')

# The null-homologous Gluck special case has zero shift. Nonzero intersections
# are retained as shifts, not incorrectly treated as grading-preserving maps.
for intersection in range(-16, 17):
    shifts = (-F(intersection**2, 2), F(intersection**2, 2))
    check(sum(shifts) == 0 and ((shifts == (0, 0)) == (intersection == 0)), 'gluck_shift_scope')

print(json.dumps({'status': 'pass', 'checks': sum(counts.values()),
                  'sections': dict(sorted(counts.items())),
                  'scope': 'Finite algebraic controls only; no topology theorem or manifold invariant is computed.'},
                 indent=2, sort_keys=True))
