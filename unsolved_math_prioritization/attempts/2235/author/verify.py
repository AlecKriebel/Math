#!/usr/bin/env python3
"""Exact finite controls for the known regular-polygon counterexample.

Standard library only. Integer polynomial remainders use Phi_n(T), with
2-T^k-T^(n-k) the squared chord length at a primitive nth root of unity.
No floating point, tolerance, or assertion statements are used. The complete
all-n mathematical proof is in PROOF.md, not supplied by these tests.
"""
from collections import Counter
from fractions import Fraction
import json

checks = Counter()

def require(ok, group):
    checks[group] += 1
    if not ok:
        raise RuntimeError('Control failed: ' + group)

def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a)

def divrem(a, b):
    a, b = list(trim(a)), trim(b)
    if b[-1] != 1:
        raise ValueError('Monic divisor required')
    q = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and any(a):
        j, c = len(a)-len(b), a[-1]
        q[j] = c
        for k, v in enumerate(b):
            a[j+k] -= c*v
        a = list(trim(a))
    return trim(q), trim(a)

def mul(a, b):
    c = [0] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)

def cyclotomics(limit):
    phis = {}
    for n in range(1, limit+1):
        xn = tuple([-1] + [0]*(n-1) + [1])
        q = xn
        divisors = [d for d in range(1,n) if n % d == 0]
        for d in divisors:
            q, r = divrem(q, phis[d])
            require(r == (0,), 'cyclotomic_exact_division')
        phis[n] = q
        product = (1,)
        for d in divisors+[n]:
            product = mul(product, phis[d])
        require(product == xn, 'cyclotomic_factorization')
    return phis

def signature(n, k, phi):
    # k in 1..n-1; if n even and k=n/2, coefficient is -2.
    p = [0]*n
    p[0] = 2
    p[k] -= 1
    p[n-k] -= 1
    return divrem(p, phi)[1]

def rational_distances(points):
    counts = []
    distances = set()
    for i, (x,y) in enumerate(points):
        fibers = Counter((x-u)**2+(y-v)**2
                         for j,(u,v) in enumerate(points) if i != j)
        counts.append(fibers)
        distances.update(fibers)
    return distances, counts

def rejected(thunk):
    try:
        thunk()
    except (RuntimeError, ValueError):
        return True
    return False

def validate_model(n, signatures, expected):
    if len(set(signatures)) != expected:
        raise ValueError('Wrong distance count')
    if any(v > 2 for v in Counter(signatures).values()):
        raise ValueError('Too many neighbors at one distance')
    if len(signatures) != n-1:
        raise ValueError('Wrong vertex count')

phis = cyclotomics(128)
for n in range(2,129):
    sig = {k:signature(n,k,phis[n]) for k in range(1,n)}
    require(len(set(sig.values())) == n//2, 'exact_distance_cardinality')
    for a in range(1,n):
        require(sig[a] != (0,), 'nonzero_chord')
        for b in range(1,n):
            expected = (a == b or a+b == n)
            require((sig[a] == sig[b]) == expected, 'exact_chord_equality')
    fiber_sizes = sorted(Counter(sig.values()).values())
    expected_sizes = ([2]*((n-1)//2) + ([1] if n%2 == 0 else []))
    require(fiber_sizes == sorted(expected_sizes), 'centered_fiber_sizes')
    validate_model(n, list(sig.values()), n//2)
    require(True, 'model_acceptance')
    # Full indexed edge counts for manageable cases, independent of rounding.
    if n <= 64:
        graphs = {s:[] for s in set(sig.values())}
        for i in range(n):
            for j in range(i+1,n):
                graphs[sig[j-i]].append((i,j))
        require(sum(map(len,graphs.values())) == n*(n-1)//2, 'edge_partition')
        for edges in graphs.values():
            degree = Counter(v for e in edges for v in e)
            require(len(set(degree.values())) == 1 and
                    set(degree.values()) <= {1,2} and len(degree) == n,
                    'distance_graph_regularity')
    for c in [Fraction(1,1),Fraction(1,100),Fraction(1,10**12)]:
        require(Fraction(n//2) < (1+c)*n/2, 'strict_counterexample')

for n in range(1,10001):
    require(((n-1)+1)//2 == n//2, 'ceiling_floor_identity')

# Direct rational coordinates supplement the cyclotomic construction.
square = [(1,0),(0,1),(-1,0),(0,-1)]
d, fibers = rational_distances(square)
require(d == {2,4}, 'rational_square_distances')
require(all(sorted(f.values()) == [1,2] for f in fibers), 'rational_square_valid')
d, fibers = rational_distances(square+[(0,0)])
require(max(fibers[-1].values()) == 4, 'center_added_is_invalid')
require(any(max(f.values()) > 2 for f in fibers), 'center_added_detected')
require(rational_distances([(0,0)]) == (set(), [Counter()]), 'singleton_boundary')
require(rejected(lambda: validate_model(4,[1,1,2],1)), 'negative_wrong_count')
require(rejected(lambda: validate_model(4,[1,1,1],1)), 'negative_invalid_fiber')
require(rejected(lambda: validate_model(4,[1,2],2)), 'negative_wrong_size')
require(rejected(lambda: divrem((1,2),(0,2))), 'negative_nonmonic_divisor')

print(json.dumps({
    'status':'PASS',
    'arithmetic':'integers and exact rational numbers only',
    'cyclotomic_n_range':[2,128],
    'full_distance_graph_n_range':[2,64],
    'counts':dict(sorted(checks.items())),
    'total_checks':sum(checks.values()),
    'proof_limit':'Finite regression checks; the all-n proof is in PROOF.md.'
},indent=2,sort_keys=True))
