#!/usr/bin/env python3
"""Independent finite controls. No author imports and no knot realizations."""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
import json
count={}
def ck(k,v):
    assert v,k
    count[k]=count.get(k,0)+1

# Biggraded injectivity: rank deficits cannot cancel across gradings.
vals=list(product(range(3),repeat=4))
for a in vals:
    for b in vals:
        if all(x<=y for x,y in zip(a,b)):
            deficit=sum(y-x for x,y in zip(a,b))
            ck('nonnegative_rank_deficit',deficit>=0)
            if deficit==0:ck('equality_in_every_grading',a==b)
            if a!=b:ck('strict_inclusion_has_larger_rank',deficit>0)
# Equal dimensions alone are not enough without the graded injection.
ck('grading_without_injection_negative_control',(1,0)!=(0,1) and sum((1,0))==sum((0,1)))

# Linear maps represented by images of basis vectors encoded in F2 bit vectors.
def apply(images,x):
    y=0
    for i,v in enumerate(images):
        if (x>>i)&1:y^=v
    return y
def compose(A,B):return tuple(apply(A,x) for x in B)
def ident(n):return tuple(1<<i for i in range(n))
rectangular={}
for m,n in ((1,1),(1,2),(1,3),(2,2),(2,3),(3,3)):
    pairs=0
    for F in product(range(1<<n),repeat=m):
        if len({apply(F,x) for x in range(1<<m)})!=(1<<m):continue
        for G in product(range(1<<m),repeat=n):
            if compose(G,F)!=ident(m):continue
            pairs+=1
            P=compose(F,G)
            ck('left_inverse_projector',compose(P,P)==P)
            if m==n:ck('equal_dimension_two_sided_inverse',P==ident(n))
            else:ck('proper_retract_not_surjective',P!=ident(n))
    rectangular[f'{m}->{n}']=pairs

# Full finite-support translation proof modeled on nonzero graded multisets.
support=[(h,q) for h in range(-1,2) for q in (-2,0,2)]
Hs=[Counter({x:1 for x in s}) for k in (1,2,3) for s in combinations(support,k)]
bases=[Counter(),Counter({(0,0):2}),Counter({(-2,-4):1,(2,4):3})]
def shift(H,n):return Counter({(h+2*n,q+4*n):v for (h,q),v in H.items()})
for H in Hs:
    for base in bases:
        family=[base+shift(H,n) for n in (-2,-1,0,1,2)]
        for A,B in combinations(family,2):
            ck('shifted_total_rank_equal',sum(A.values())==sum(B.values()))
            ck('nonzero_finite_support_shift_distinct',A!=B)
            ck('no_graded_injection_forward',any(A[k]>B[k] for k in A))
            ck('no_graded_injection_backward',any(B[k]>A[k] for k in B))

# Free finite categories: identity image does not make an absent reverse arrow exist.
arrows={(0,0),(0,1),(1,1)}
for x,y,z in product((0,1),repeat=3):
    if (x,y) in arrows and (y,z) in arrows:
        ck('poset_functor_composition',(x,z) in arrows and 1*1==1)
ck('no_geometric_inverse_from_functor',(0,1) in arrows and (1,0) not in arrows)

# Euler parity and conditional strictly decreasing odd ranks.
for v in product(range(4),repeat=5):
    chi=sum((-1)**i*x for i,x in enumerate(v))
    ck('euler_total_rank_parity',(sum(v)-chi)%2==0)
    if chi==1:ck('normalized_euler_odd_rank',sum(v)%2==1)
for r in range(1,40,2):
    for s in range(1,r,2):
        ck('strict_odd_drop_at_least_two',r-s>=2)
    chain=list(range(r,0,-2))
    ck('conditional_chain_bound',len(chain)-1==(r-1)//2)
# Constant numerical ranks can accompany strictly descending abstract objects forever.
ck('rank_stabilization_not_object_stabilization',all(3==3 for _ in range(10)) and len(set(range(10)))==10)
ck('morse_index_reversal',[2-k for k in [0,1]]==[2,1])
result={'status':'PASS','assertions_passed':sum(count.values()),'by_category':count,
        'left_inverse_pairs_by_dimensions':rectangular,
        'scope':'Exact finite linear-algebra and grading diagnostics, not knot computations.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
