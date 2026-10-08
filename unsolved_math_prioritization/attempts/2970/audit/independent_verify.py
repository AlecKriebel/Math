#!/usr/bin/env python3
"""Independent exact audit; no imports from the frozen candidate.

The quotient is represented by its faithful permutation action on P^1(F_3).
The program is deterministic, standard-library-only, and writes only stdout.
It verifies arithmetic and a finite group example, not any surface equivalence.
"""
from collections import Counter, deque
from fractions import Fraction
from itertools import permutations, product
from math import gcd
import hashlib
import json


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


def times(x, y):
    return tuple(sum(x[2*i+k]*y[2*k+j] for k in range(2)) % 3
                 for i in range(2) for j in range(2))


ONE = (1, 0, 0, 1)
MINUS = (2, 0, 0, 2)
A = (1, 1, 0, 1)
B = (1, 0, 1, 1)
P = (0, 1, 2, 0)


def mpow(x, n):
    result = ONE
    for _ in range(n):
        result = times(result, x)
    return result


def minverse(x):
    a, b, c, d = x
    check((a*d-b*c) % 3 == 1, 'matrix determinant must be one')
    return (d, -b % 3, -c % 3, a)


LINES = ((1, 0), (0, 1), (1, 1), (1, 2))


def action(matrix):
    result = []
    a, b, c, d = matrix
    for x, y in LINES:
        u, v = (a*x+b*y) % 3, (c*x+d*y) % 3
        scale = pow(u or v, -1, 3)
        result.append(LINES.index((u*scale % 3, v*scale % 3)))
    return tuple(result)


PID = tuple(range(4))


def compose(x, y):
    return tuple(x[y[i]] for i in range(4))


def inverse(x):
    return tuple(x.index(i) for i in range(4))


def conjugate(x, y):
    return compose(compose(x, y), inverse(x))


def tuple_product(seq):
    result = PID
    for x in seq:
        result = compose(result, x)
    return result


def subgroup(gens):
    reached = {PID}
    frontier = [PID]
    for q in frontier:
        for g in gens:
            z = compose(g, q)
            if z not in reached:
                reached.add(z)
                frontier.append(z)
    return reached


def braid_neighbors(seq):
    for j in range(3):
        x, y = seq[j:j+2]
        yield seq[:j] + (conjugate(x, y), x) + seq[j+2:]
        yield seq[:j] + (y, conjugate(inverse(y), x)) + seq[j+2:]


def orbit(seed, global_generators):
    reached = {seed}
    frontier = deque([seed])
    while frontier:
        seq = frontier.popleft()
        neighbors = list(braid_neighbors(seq))
        neighbors.extend(tuple(conjugate(g, x) for x in seq)
                         for g in global_generators)
        for candidate in neighbors:
            if candidate not in reached:
                reached.add(candidate)
                frontier.append(candidate)
    return reached


def finite_check():
    matrices = {x for x in product(range(3), repeat=4)
                if (x[0]*x[3]-x[1]*x[2]) % 3 == 1}
    check(len(matrices) == 24, 'SL(2,F3) order')
    alternating = {q for q in permutations(range(4))
                   if sum(q[i] > q[j] for i in range(4)
                          for j in range(i+1, 4)) % 2 == 0}
    lifts = {}
    for x in sorted(matrices):
        lifts.setdefault(action(x), []).append(x)
    check(set(lifts) == alternating and len(alternating) == 12,
          'projective quotient is the complete A4')
    check(all(len(xs) == 2 and xs[1] == tuple(-z % 3 for z in xs[0])
              for xs in lifts.values()), 'all quotient fibers equal plus/minus pairs')
    check(all(action(times(x, y)) == compose(action(x), action(y))
              for x in matrices for y in matrices), 'projective action homomorphism')
    a, b, p = map(action, (A, B, P))
    check(subgroup((a, b)) == alternating, 'a and b generate the same full quotient')
    upstairs = {ONE}
    stack = [ONE]
    for x in stack:
        for g in (A, B):
            z = times(g, x)
            if z not in upstairs:
                upstairs.add(z)
                stack.append(z)
    check(upstairs == matrices and P in upstairs, 'A,B generate SL2 and contain P')
    c = times(A, B)
    check(mpow(A, 3) == mpow(B, 3) == ONE, 'A and B cube to identity')
    check(mpow(c, 2) == mpow(P, 2) == MINUS, 'squares C and P equal minus identity')
    check(times(times(P, c), minverse(P)) == tuple(-z % 3 for z in c),
          'P conjugates C to minus C')
    t = (a, b, inverse(b), inverse(a))
    tp = (conjugate(p, a), conjugate(p, b), inverse(b), inverse(a))
    check(tuple_product(t) == tuple_product(tp) == PID, 'both factorizations multiply to identity')
    three_cycles = {q for q in alternating if q != PID and tuple_product((q, q, q)) == PID}
    canonical = {}
    for q in sorted(three_cycles):
        choices = [x for x in lifts[q] if mpow(x, 3) == ONE]
        check(len(choices) == 1, 'every order-three quotient element has one order-three lift')
        canonical[q] = choices[0]

    def lift_product(seq):
        out = ONE
        for q in seq:
            check(q in canonical, 'each factor has order three')
            out = times(out, canonical[q])
        return out

    check(lift_product(t) == ONE and lift_product(tp) == MINUS, 'distinct central lift products')
    orbits = [orbit(t, (a, b)), orbit(tp, (a, b))]
    check([len(s) for s in orbits] == [216, 144], 'exact full orbit cardinalities 216 and 144')
    check(orbits[0].isdisjoint(orbits[1]), 'orbits disjoint')
    for found, lift in zip(orbits, (ONE, MINUS)):
        for seq in found:
            check(tuple_product(seq) == PID, 'orbit tuple product')
            check(subgroup(seq) == alternating, 'every orbit tuple generates A4')
            check(lift_product(seq) == lift, 'central lift invariant throughout orbit')
            check(set(braid_neighbors(seq)) <= found, 'closed under both Hurwitz directions')
            check(all(tuple(conjugate(g, q) for q in seq) in found for g in alternating),
                  'closed under every simultaneous inner conjugation')
    class_a = {conjugate(g, a) for g in alternating}
    wanted_type = sum(q in class_a for q in t)
    universe = {seq for seq in product(sorted(three_cycles), repeat=4)
                if tuple_product(seq) == PID and subgroup(seq) == alternating
                and sum(q in class_a for q in seq) == wanted_type}
    check(orbits[0] | orbits[1] == universe,
          'two computed orbits exhaust the specified conjugacy-multiset universe')
    return {'SL2_order': len(matrices), 'A4_order': len(alternating),
            'orbit_sizes': [len(s) for s in orbits],
            'order_three_generating_identity_tuple_universe_with_two_factors_per_class': len(universe),
            'lift_products': ['I', '-I'], 'disjoint': True,
            'orbit_sha256': [hashlib.sha256(json.dumps(sorted(s)).encode()).hexdigest()
                             for s in orbits]}


def arithmetic_check():
    def pairing(e, v, w):
        return -e*v[0]*w[0] + v[0]*w[1] + v[1]*w[0]

    def determinant(q):
        return q[0][0]*q[1][1]-q[0][1]*q[1][0]

    def square(q, x):
        return sum(q[i][j]*x[i]*x[j] for i in range(2) for j in range(2))

    summaries = []
    for r in range(2, 102):
        bx, by = (6, 4*r), (6, 10*r)
        lx, ly = (3, 2*r), (3, 5*r)
        kbase_x, kbase_y = (-2, -2), (-2, -2*r-2)
        kx = tuple(lx[i]+kbase_x[i] for i in range(2))
        ky_pullback = tuple(ly[i]+kbase_y[i] for i in range(2))
        d = 2*pairing(0, kx, kx)
        check(d == 2*pairing(2*r, ky_pullback, ky_pullback) == 8*r-8,
              'canonical square from both double-cover formulas')
        chi_x = 2 + Fraction(pairing(0, lx, kx), 2)
        chi_y = 2 + Fraction(pairing(2*r, ly, ky_pullback), 2)
        check(chi_x == chi_y == 4*r-1, 'holomorphic Euler from both double covers')
        genus_x = 1 + Fraction(pairing(0, bx, tuple(bx[i]+kbase_x[i] for i in range(2))), 2)
        cy = (5, 10*r)
        genus_cy = 1 + Fraction(pairing(2*r, cy, tuple(cy[i]+kbase_y[i] for i in range(2))), 2)
        check(genus_x == 20*r-5 and genus_cy == 20*r-4, 'branch-component genera by adjunction')
        euler = 8-(2-2*genus_x)
        check(euler == 8-(4-2*genus_cy) == 40*r-4 == 12*chi_x-d,
              'topological Euler from branched covers and Noether')
        signature = Fraction(d-2*euler, 3)
        check(signature == -24*r, 'signature formula')
        positive, negative = 8*r-3, 32*r-3
        check(positive+negative == euler-2 and positive-negative == signature,
              'Betti ranks')
        qx = ((0, 2), (2, 0))
        qy = ((-4*r, 2), (2, 0))
        saturation = ((-r, 1), (1, 0))
        ky = (2, 3*r-2)
        check(determinant(qx) == determinant(qy) == -4 and determinant(saturation) == -1,
              'primitive versus saturated determinant')
        check(square(qx, kx) == square(saturation, ky) == d,
              'canonical square in integral cover lattices')
        check(gcd(*kx) == 1 and gcd(*ky) == (2 if r % 2 == 0 else 1),
              'canonical divisibility and spin parity')
        check(-r*ky[0]+ky[1] == r-2, 'ramification sphere canonical pairing')
        check(Fraction(-6, 2) == -3 and pairing(0, kx, (0, 1)) == 1,
              'nodal-grid smooth sphere square and canonical pairing')
        signs = [1]*positive + [-1]*negative
        canonical = [3]*(4*r-1)+[1]*(4*r-2)+[1]*negative
        candidate = [0]*positive+[-1]*(r-1)+[1]+[0]*(negative-r)
        check(all(x % 2 == 1 for x in canonical), 'formal canonical vector characteristic')
        check(sum(s*x*x for s, x in zip(signs, canonical)) == d, 'formal canonical square')
        check(sum(s*x*x for s, x in zip(signs, candidate)) == -r, 'formal sphere square')
        check(sum(s*x*y for s, x, y in zip(signs, candidate, canonical)) == r-2,
              'formal canonical-sphere pairing')
        pencils = []
        for k in (1, 2, 4, 8, 16):
            genus = 1+Fraction(k*(k+1)*d, 2)
            base = k*k*d
            nodes = euler+base-4+4*genus
            check(nodes == euler+d*(3*k*k+2*k), 'pencil node formula from Euler identity')
            pencils.append([k, int(genus), base, int(nodes)])
        summaries.append({'r': r, 'K2': d, 'pg': int(chi_x-1), 'euler': int(euler),
                          'signature': int(signature), 'pencils': pencils})
    check(summaries[1]['pencils'][0] == [1, 17, 16, 196], 'smallest canonical-pencil data')
    check(8*4-8 == 24 and gcd(2, 3*4-2) == 2, 'r=4 counterexample range and spin case')
    check([r for r in range(3, 102, 2)
           if (4*r-2 in (6, 10) or (4*r-4) % 4 != 0)] == [3],
          'normal-moduli connectedness parameter conversion')
    return {'r_range': [2, 101], 'pencil_degrees': [1, 2, 4, 8, 16],
            'canonical_r3': summaries[1],
            'arithmetic_sha256': hashlib.sha256(json.dumps(summaries, sort_keys=True).encode()).hexdigest()}


def main():
    result = {'status': 'passed', 'finite_group': finite_check(), 'arithmetic': arithmetic_check(),
              'scope': 'Exact algebra only; no geometric realization or KP-4.94 equivalence established.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
