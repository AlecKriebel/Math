#!/usr/bin/env python3
"""Independent exact diagnostics, not a proof of Polish-group dynamics."""
import itertools
import json
from fractions import Fraction as Q

counts = {}
def require(ok, section):
    counts[section] = counts.get(section, 0) + 1
    if not ok:
        raise RuntimeError('independent check failed: ' + section)

G = tuple(itertools.permutations(range(3)))
e = (0, 1, 2)
def mul(a, b):
    return tuple(a[b[i]] for i in range(3))
def inverse(a):
    return tuple(a.index(i) for i in range(3))
def product(A, B):
    return {mul(a, b) for a in A for b in B}
subsets = [set(G[i] for i in range(6) if mask & (1 << i)) for mask in range(64)]
subgroups = [S for S in subsets if e in S and product(S,S) == S]
require(len(subgroups) == 6, 'factor_order')
witnesses = 0
normal_subgroups = 0
for U in subgroups:
    normal = all({mul(mul(g,u),inverse(g)) for u in U} == U for g in G)
    normal_subgroups += normal
    for F in subsets:
        FU, UF = product(F,U), product(U,F)
        require({inverse(x) for x in FU} == product(U,{inverse(f) for f in F}), 'factor_order')
        if normal:
            require(FU == UF, 'normal_factor_order')
        witnesses += FU == set(G) and UF != set(G)
require(witnesses > 0, 'factor_order')
require(normal_subgroups == 3, 'normal_factor_order')

# Exhaust all 3^5 functions with q(e)=0 and remaining values in {-1,0,1}.
# These are finite quasimorphisms, not homogeneous examples.
nonidentity = tuple(x for x in G if x != e)
for values in itertools.product((-1,0,1), repeat=5):
    q = dict(zip(nonidentity,values)); q[e] = 0
    defect = max(abs(q[mul(x,y)]-q[x]-q[y]) for x in G for y in G)
    for a,b,c in itertools.product(G,repeat=3):
        require(abs(q[mul(mul(a,b),c)]) <= abs(q[a])+abs(q[b])+abs(q[c])+2*defect,
                'two_defect_estimate')

for delta in (Q(1,13),Q(2,7),Q(3,2),Q(7)):
    for j,k in itertools.product(range(-12,13),repeat=2):
        dx,dy = delta*j/50,delta*k/50
        require(abs(delta+dy-dx) > delta/2, 'separation')

# Distinctness survives a fixed finite collection of injective maps.
points = [Q(i,20) for i in range(21)]
for power in range(1,6):
    separated = [(x,y) for x,y in itertools.combinations(points,2) if y-x >= Q(1,4)]
    eta = min(y**power-x**power for x,y in separated)
    require(eta > 0, 'finite_uniform_inverse')
    require(all(y**power-x**power >= eta for x,y in separated), 'finite_uniform_inverse')

for a,b,c,d in itertools.product(range(1,8),repeat=4):
    value,bound = Q(a,b),Q(c,d)
    n = bound//value+1
    require(n*value > bound, 'homogeneity_squeeze')
for n in range(2,12):
    for value in range(-30,31):
        require((n*value == 0) == (value == 0), 'torsion_to_Z')

print(json.dumps({'schema':1,'problem_id':30006162,'status':'PASS',
    'checks':sum(counts.values()),'sections':counts,
    'scope':'Finite exact controls only; no proof of GPP, compact-flow continuity, or infinite Baire-category claims.'},sort_keys=True))
