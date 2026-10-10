#!/usr/bin/env python3
"""Independent exact controls; the infinite theorem is established in AUDIT.md.

No author verifier is imported. Subset enumeration computes elementary
coefficients; sparse multivariate arithmetic tests restrictions to finite RREF
families. These bounded families do not enumerate all real subspaces.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import factorial, prod
import json

counts = Counter()


def require(condition, label):
    counts[label] += 1
    if not condition:
        raise RuntimeError(label)


def es(x):
    return [sum((prod(x[i] for i in I) for I in combinations(range(len(x)), k)), 0)
            for k in range(len(x) + 1)]


def variations(a):
    a = [1 if x > 0 else -1 for x in a if x]
    return sum(x != y for x, y in zip(a, a[1:]))


vectors = 0
adjacent_zeros = 0
alphabet = tuple(map(Fraction, (-3, 0, 2, 5))) + (Fraction(-1, 2),)
for n in range(1, 7):
    for x in product(alphabet, repeat=n):
        vectors += 1
        e = es(x)
        support = sum(t != 0 for t in x)
        for r in range(2, n + 4):
            a = e[r-1] if r-1 <= n else 0
            b = e[r] if r <= n else 0
            adjacent_zeros += int(a == b == 0)
            require(a != 0 or b != 0 or support <= r-2,
                    'rational_adjacent_coefficient_support')
        # For a product of real linear factors with nonzero constant term,
        # Descartes' upper bounds are jointly sharp.
        require(variations(e) + variations([(-1)**j*a for j,a in enumerate(e)]) == support,
                'descartes_joint_sharpness')
        for r in range(2, n+1):
            # Independent coefficient differentiation from the descending
            # elementary list. The zero multiplicity is computed explicitly.
            q = [e[n-j] * (factorial(j) // factorial(j-(n-r)))
                 for j in range(n-r, n+1)]
            require(q[0] == factorial(n-r)*e[r], 'derivative_constant')
            require(q[1] == factorial(n-r+1)*e[r-1], 'derivative_linear')


def rref_matrices(n, d):
    """All RREF d by n matrices with free entries in {-1,0,1}."""
    for pivots in combinations(range(n), d):
        free = [(i,j) for i in range(d) for j in range(pivots[i]+1,n) if j not in pivots]
        for values in product((-1,0,1), repeat=len(free)):
            a = [[0]*n for _ in range(d)]
            for i,j in enumerate(pivots): a[i][j] = 1
            for (i,j),v in zip(free,values): a[i][j] = v
            yield a


def restricted_es(a, r):
    """Return coefficients of e_r evaluated at the row-span parameters."""
    d,n = len(a),len(a[0])
    zero = (0,)*d
    answer = Counter()
    for I in combinations(range(n),r):
        monomials = {zero:1}
        for j in I:
            out = Counter()
            for exp,c in monomials.items():
                for i in range(d):
                    if a[i][j]:
                        e=list(exp); e[i]+=1
                        out[tuple(e)] += c*a[i][j]
            monomials = {e:c for e,c in out.items() if c}
        for e,c in monomials.items(): answer[e] += c
    return {e:c for e,c in answer.items() if c}


rref_results = []
for n,d,r in [(3,2,2),(4,2,2),(4,3,4),(5,3,4),(5,4,4),(6,3,4)]:
    examined=vanishing=0
    for a in rref_matrices(n,d):
        examined+=1
        zero = not restricted_es(a,r)
        vanishing+=int(zero)
        if d >= r:
            require(not zero,'rref_upper_bound')
        else:
            coordinate = sum(any(a[i][j] for i in range(d)) for j in range(n)) == d
            require(not zero or coordinate,'rref_extremal_coordinate')
    rref_results.append(dict(n=n,d=d,r=r,examined=examined,vanishing=vanishing))

# Independent exact polynomial restrictions for hypothesis and terminology
# controls. The full-support plane in R^5 is inclusion-maximal but does not
# have the maximum dimension 3, so those two meanings must be distinguished.
plane = [[2,-2,0,0,0],[0,0,2,2,-1]]
require(not restricted_es(plane,4),'full_support_plane_e4')
require(all(sum(row[j] for row in plane) for j in range(5)), 'plane_has_full_support_point')
require(not restricted_es([[2,2,-1]],2),'quadratic_noncoordinate_line')
for r in (1,3,5,7):
    a=[[0]*(2*r) for _ in range(r)]
    for i in range(r): a[i][2*i]=1; a[i][2*i+1]=-1
    require(not restricted_es(a,r),'odd_degree_negative_control')

print(json.dumps({
    'status':'PASS', 'independent_of_author_verifier':True,
    'universal_claim_from_finite_tests':False,
    'rational_vectors':vectors,
    'rational_alphabet':[str(x) for x in alphabet],
    'adjacent_zero_instances':adjacent_zeros,
    'rref_families':rref_results,
    'checks':dict(sorted(counts.items())),
    'total_checks':sum(counts.values()),
    'optimization_safe':'Explicit exceptions; no assert statements.'
},indent=2,sort_keys=True))
