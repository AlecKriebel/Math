#!/usr/bin/env python3
"""Independent exact diagnostics, not a proof of the infinite group theorem.
No author code is imported. Run with Python 3 standard library.
"""
from fractions import Fraction as Q
from itertools import combinations
from collections import Counter, deque
import json

counts = Counter()
negative_controls = []

def check(label, truth):
    if not truth:
        raise AssertionError(label)
    counts[label] += 1

def reject(label, truth):
    check('negative_control_rejected', not truth)
    negative_controls.append(label)

def power_two_integer(n):
    return n > 0 and n & (n - 1) == 0

def dyadic(x):
    return power_two_integer(Q(x).denominator)

def legal_slope(x):
    x = Q(x)
    return power_two_integer(x.numerator) and power_two_integer(x.denominator)

class PL:
    """Degree-one increasing lift represented by knots over a length-one interval."""
    def __init__(self, knots):
        self.knots = tuple((Q(x), Q(y)) for x,y in knots)
    def valid(self):
        p = self.knots
        return (len(p) >= 2 and p[-1][0] - p[0][0] == 1
                and p[-1][1] - p[0][1] == 1
                and all(dyadic(x) and dyadic(y) for x,y in p)
                and all(x < u and y < v and legal_slope((v-y)/(u-x))
                        for (x,y),(u,v) in zip(p,p[1:])))
    def lift(self,x):
        x = Q(x)
        n = (x-self.knots[0][0]) // 1
        z = x-n
        for (a,b),(c,d) in zip(self.knots,self.knots[1:]):
            if a <= z <= c:
                return b+(z-a)*(d-b)/(c-a)+n
        raise AssertionError('lift interval missing')
    def __call__(self,x):
        return self.lift(x) % 1
    def inv(self):
        return PL([(y,x) for x,y in self.knots])
    def then(self, outer):
        # Exact composition: include every breakpoint and every preimage breakpoint.
        xs = {Q(0), Q(1)} | {x % 1 for x,y in self.knots}
        inverse = self.inv()
        xs |= {inverse(x) for x,y in outer.knots}
        return PL([(x, outer.lift(self.lift(x))) for x in sorted(xs)])
    def equals(self, other):
        xs = {Q(0), Q(1)} | {x % 1 for x,y in self.knots+other.knots}
        difference = self.lift(0)-other.lift(0)
        return difference.denominator == 1 and all(
            self.lift(x)-other.lift(x) == difference for x in xs)

identity = PL([(0,0),(1,1)])

def binary_partition(a,b):
    # Decompose a dyadic length by its numerator's set bits, unlike a uniform grid.
    length = b-a
    assert length > 0 and dyadic(length)
    d = length.denominator
    steps = [Q(1 << bit,d) for bit in range(length.numerator.bit_length()-1,-1,-1)
             if length.numerator & (1 << bit)]
    out = [a]
    for step in steps:
        out.append(out[-1]+step)
    assert out[-1] == b
    return out

def refine(knots):
    i = max(range(len(knots)-1), key=lambda i: knots[i+1]-knots[i])
    return knots[:i+1]+[(knots[i]+knots[i+1])/2]+knots[i+1:]

def circular_ordered(mapping):
    xs = sorted(mapping)
    if not xs or len(set(mapping.values())) != len(xs):
        return False
    ys = []
    for x in xs:
        y = mapping[x]
        if ys:
            while y <= ys[-1]:
                y += 1
        ys.append(y)
    return ys[-1] < ys[0]+1

def extension(mapping):
    assert circular_ordered(mapping)
    xs = sorted(mapping)
    ys = []
    for x in xs:
        y = mapping[x]
        if ys:
            while y <= ys[-1]:
                y += 1
        ys.append(y)
    xs.append(xs[0]+1)
    ys.append(ys[0]+1)
    out = []
    for a,b,c,d in zip(xs,xs[1:],ys,ys[1:]):
        u,v = binary_partition(a,b),binary_partition(c,d)
        while len(u) < len(v): u = refine(u)
        while len(v) < len(u): v = refine(v)
        out.extend(zip(u[:-1],v[:-1]))
    return PL(out+[(xs[-1],ys[-1])])

def slide(A,B):
    common = A & B
    if len(A-B) != 1 or len(B-A) != 1:
        return False
    if not common:
        return True
    # Component IDs are the most recent common point in positive circular order.
    def component(x):
        return min(common, key=lambda c:(x-c) % 1)
    return component(next(iter(A-B))) == component(next(iter(B-A)))

def orbital_signature(A,B):
    word = tuple(2 if x in A & B else 0 if x in A else 1 for x in sorted(A | B))
    variants = []
    for w in (word,tuple(1-x if x < 2 else 2 for x in word)):
        variants.extend(w[i:]+w[:i] for i in range(len(w)))
    return min(variants)

# Every pair of configurations in a finite grid: local witness and finite slide graph.
grid = tuple(Q(i,8) for i in range(8))
for k in range(1,8):
    configs = [frozenset(c) for c in combinations(grid,k)]
    adjacency = {A:set() for A in configs}
    signatures = set()
    for A,B in combinations(configs,2):
        if slide(A,B):
            adjacency[A].add(B); adjacency[B].add(A)
            signatures.add(orbital_signature(A,B))
            check('finite_slide_edge',True)
        a = min(A-B)
        union = A | B
        delta = min((x-a) % 1 for x in union if x != a)
        aprime = (a+delta/2) % 1
        mapping = {x:(aprime if x == a else x) for x in union}
        check('local_witness_circular_order', circular_ordered(mapping))
        g = extension(mapping)
        check('local_witness_legal_PL', g.valid())
        check('local_witness_prescribed_map', all(g(x)==y for x,y in mapping.items()))
        check('local_witness_fixes_other_configuration', all(g(x)==x for x in B))
        check('local_witness_slide', slide(A,frozenset(g(x) for x in A)))
        check('local_witness_inverse_exact', g.then(g.inv()).equals(identity))
    check('single_unordered_edge_pattern',len(signatures)==1)
    seen = {configs[0]}; todo = deque(seen)
    while todo:
        A = todo.popleft()
        for B in adjacency[A]-seen:
            seen.add(B); todo.append(B)
    check('finite_slide_graph_connected',len(seen)==len(configs))

# Arbitrary cyclic shifts and wrapping, with denominator 32 and nonuniform arcs.
for k in range(1,13):
    A = tuple(Q(i,32) for i in range(k))
    B = tuple(Q(31-i,32) for i in reversed(range(k)))
    for shift in range(k):
        mapping = {a:B[(i+shift)%k] for i,a in enumerate(A)}
        g = extension(mapping)
        check('extension_shift_legal',g.valid())
        check('extension_shift_values',all(g(x)==y for x,y in mapping.items()))
        check('extension_shift_inverse_exact',g.then(g.inv()).equals(identity))

# Exact whole-piece composition proves these sample complements have exact order k.
# This supplements the written proof for arbitrary k; it does not establish it.
f = PL([(0,0),(Q(1,2),Q(1,4)),(Q(3,4),Q(1,2)),(1,1)])
for k in range(1,33):
    endpoints = [Q(0),Q(1)]
    while len(endpoints) < k+1:
        endpoints = refine(endpoints)
    knots = [(endpoints[i], endpoints[i+1] if i < k-1 else Q(1)) for i in range(k)]
    knots.append((Q(1), endpoints[1]+1))
    r = PL(knots)
    check('complement_legal',r.valid())
    power = identity
    for j in range(1,k+1):
        power = power.then(r)
        check('complement_exact_whole_map_order',power.equals(identity)==(j==k))
    def factor(i):
        a,b = endpoints[i:i+2]
        d = b-a
        return PL([(x,x) for x in endpoints[:i]]+
                  [(a+d*x,a+d*y) for x,y in f.knots]+
                  [(x,x) for x in endpoints[i+2:]])
    for i in range(k):
        f_i = factor(i)
        check('normalized_factor_legal',f_i.valid())
        conjugated = r.inv().then(f_i).then(r)
        check('cyclic_action_exact_whole_map',conjugated.equals(factor((i+1)%k)))
        check('factor_fixes_endpoints',all(f_i(x)==x % 1 for x in endpoints))
    if k > 1:
        check('different_factors_commute_exact',factor(0).then(factor(1)).equals(factor(1).then(factor(0))))
        check('pointwise_setwise_distinct',r(0)!=0 and all(r(x) in endpoints[:-1] for x in endpoints[:-1]))

# Explicit faulty alternatives must be detected.
reject('naive affine slope 3/4 is not allowed',legal_slope(Q(3,4)))
reject('rotation by 1/3 fails dyadic preservation',PL([(0,Q(1,3)),(1,Q(4,3))]).valid())
reject('equally spaced triple is not dyadic',all(dyadic(x) for x in [Q(0),Q(1,3),Q(2,3)]))
reject('triple transposition reverses circular order',circular_ordered({Q(0):Q(0),Q(1,4):Q(1,2),Q(1,2):Q(1,4)}))
reject('shared k-1 points alone is not a local slide',slide(frozenset([Q(0),Q(1,4),Q(1,2)]),frozenset([Q(1,4),Q(1,2),Q(3,8)])))
reject('moving a common point need not fix B',{Q(0):Q(1,16),Q(1,2):Q(1,2)}[Q(0)]==Q(0))

print(json.dumps({
    'status':'PASS',
    'arithmetic':'Exact Python Fraction; no author code imported',
    'counts':dict(sorted(counts.items())),
    'total_assertions':sum(counts.values()),
    'negative_controls':negative_controls,
    'coverage':{
        'finite_grid':'8 dyadic points; all unordered distinct configuration pairs for each 1<=k<=7',
        'cyclic_shift_extensions':'Every shift for 1<=k<=12; denominator 32',
        'cyclic_complements':'1<=k<=32; exact PL composition, factor conjugation and endpoint actions',
        'universal_theorem':'Established by written argument, not by these bounded checks'
    }
},indent=2,sort_keys=True))
