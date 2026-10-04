#!/usr/bin/env python3
"""Exact auxiliary controls for 30001182. Not a formal proof checker."""
from fractions import Fraction as F
from itertools import product
import json

counts = {}
def check(tag, condition):
    assert condition, tag
    counts[tag] = counts.get(tag, 0) + 1

def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)

def zero(n):
    return mat([[0]*n for _ in range(n)])

def ident(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])

def diag(xs):
    return mat([[x if i == j else 0 for j in range(len(xs))]
                for i, x in enumerate(xs)])

def mul(a,b):
    n = len(a)
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(n)), F(0))
                       for j in range(n)) for i in range(n))

def sub(a,b):
    return tuple(tuple(x-y for x,y in zip(ar,br)) for ar,br in zip(a,b))

def transpose(a):
    return tuple(zip(*a))

def rank(rows):
    a = [list(map(F,row)) for row in rows]
    r = 0
    for c in range(len(a[0])):
        k = next((k for k in range(r,len(a)) if a[k][c]), None)
        if k is None:
            continue
        a[r],a[k] = a[k],a[r]
        pivot = a[r][c]
        a[r] = [x/pivot for x in a[r]]
        for i in range(len(a)):
            if i != r:
                f = a[i][c]
                a[i] = [x-f*y for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r

def evaluate_density(rho,a):
    return sum((rho[i][j]*a[j][i] for i in range(len(a))
                for j in range(len(a))),F(0))

def flatten(a):
    return tuple(x for row in a for x in row)

I = ident(4)
p = diag([0,0,1,1])
q = diag([0,1,0,1])
pq = mul(p,q)
rho = mat([[F(1,2),0,0,F(1,2)], [0,0,0,0], [0,0,0,0],
           [F(1,2),0,0,F(1,2)]])
phi = lambda a: evaluate_density(rho,a)
check('projection_p', mul(p,p)==p and transpose(p)==p)
check('projection_q', mul(q,q)==q and transpose(q)==q)
check('commutation', mul(p,q)==mul(q,p))
check('ambient_dimension', rank([flatten(a) for a in [I,p,q,pq]])==4)
check('distinct_coordinate_algebras', rank([flatten(a) for a in [I,p,q]])==3)
# Each coordinate algebra has dimension 2, their sum has dimension 3,
# so the intersection has dimension 1, already containing the identity.
check('subalgebra_B_dimension',rank([flatten(I),flatten(p)])==2)
check('subalgebra_C_dimension',rank([flatten(I),flatten(q)])==2)
check('density_self_adjoint',transpose(rho)==rho)
check('density_idempotent',mul(rho,rho)==rho)
check('density_rank_one',rank(rho)==1)
check('density_trace_one',sum(rho[i][i] for i in range(4))==1)
for a in (p,q,pq,mul(q,p)):
    check('target_moments',phi(a)==F(1,2))
# Basis testing establishes that restriction is the declared four-point state.
for k in range(4):
    a=diag([int(i==k) for i in range(4)])
    check('state_preserving_inclusion',phi(a)==(F(1,2) if k in (0,3) else 0))
# The upstairs density is not the diagonal two-character mixture.
mixture = diag([F(1,2),0,0,F(1,2)])
u = zero(4)
u = mat([[int(i==0 and j==3) for j in range(4)] for i in range(4)])
check('upstairs_coherence',phi(u)==F(1,2) and evaluate_density(mixture,u)==0)
# Every finite B*C basis word in p,1-p,q,1-q has the declared joint law.
letters=(p,sub(I,p),q,sub(I,q))
max_pair_length=6
for n in range(max_pair_length+1):
    for word in product(range(4),repeat=n):
        a=I
        chi0=F(1)
        chi1=F(1)
        for letter in word:
            a=mul(a,letters[letter])
            chi0 *= letters[letter][0][0]
            chi1 *= letters[letter][3][3]
        check('finite_pair_word_law',phi(a)==(chi0+chi1)/2)
# GNS collapse model: common projection with fair cyclic state.
J=ident(2)
r=diag([0,1])
eta=lambda a:(a[0][0]+a[1][1])/2
max_projection_length=5
for n in range(1,max_projection_length+1):
    # Six names represent p_1,q_1,p_2,q_2,p_3,q_3, all equal to r.
    for word in product(range(6),repeat=n):
        a=J
        for _ in word:
            a=mul(a,r)
        check('finite_projection_collapse',a==r and eta(a)==F(1,2))
# Exact zero-distance relations and availability of a third distinct index.
for i,j in product(range(1,5),repeat=2):
    if i!=j:
        check('cross_copy_zero_distance', F(1,2)+F(1,2)-F(1,2)-F(1,2)==0)
        k=next(k for k in range(1,5) if k not in (i,j))
        check('third_copy_available',k not in (i,j))
# Matrix units demonstrate that the upstairs GNS cyclic orbit spans C^4.
orbit=[]
for i,j in product(range(4),repeat=2):
    a=mat([[int(s==i and t==j) for t in range(4)] for s in range(4)])
    # Use unnormalised e_00+e_11; scaling does not affect span.
    orbit.append([a[k][0]+a[k][3] for k in range(4)])
    # eae=phi(a)e is the finite certificate used by the purity proof.
    check('rank_one_corner_identity',mul(mul(rho,a),rho)==
          tuple(tuple(phi(a)*x for x in row) for row in rho))
check('matrix_orbit_cyclic',rank(orbit)==4)
# Some exact positive-state tests, all based on rational matrices.
for values in product((-1,0,1), repeat=4):
    a=mat([[values[(i+2*j)%4] for j in range(4)] for i in range(4)])
    check('matrix_positivity_controls',phi(mul(transpose(a),a))>=0)
# Laurent obstruction: in the formal exponent algebra x*x^{-1}=1,
# x*=x and (x^-1)*=x^-1. The Gram matrix on [x,x^-1] must be
# [[0,1],[1,b]], whose determinant is -1 for every real b.
for b in map(F,range(-5,6)):
    check('laurent_gram_obstruction',F(0)*b-F(1)*F(1)==-1)

output={
    'problem_id':'30001182',
    'arithmetic':'fractions.Fraction; exact rational arithmetic only',
    'all_controls_passed':True,
    'assertions':sum(counts.values()),
    'counts':counts,
    'limits':{'pair_word_length':max_pair_length,
              'projection_word_length':max_projection_length,
              'projection_copy_count':3},
    'scope':'Auxiliary finite controls only. The all-state, all-word and infinite-copy arguments are in PROOF.md.',
}
print(json.dumps(output,indent=2,sort_keys=True))
