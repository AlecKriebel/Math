#!/usr/bin/env python3
"""Exact cut, cross-ratio and planar measure controls, independently written."""
from fractions import Fraction as Q
from itertools import product,combinations
from pathlib import Path
from collections import Counter
import hashlib,json
C=Counter()
def check(name,x):
    assert x,name
    C[name]+=1
pairs=list(combinations(range(5),2))
weights=[(-1,1,1,1,-1),(3,-2,0,0,0),(-2,-1,1,1,2),(2,2,-1,-1,-1),(0,0,0,0,1)]
for b in weights:
    check('integer_weight_sum',sum(b)==1)
    for bits in product((0,1),repeat=5):
        cut=sum(b[i]*b[j] for i,j in pairs if bits[i]!=bits[j])
        k=sum(v for v,side in zip(b,bits) if side)
        check('cut_identity',cut==k*(1-k))
        check('cut_sign',cut<=0)
raw=[(0,0,0),(0,0,1),(0,1,0),(1,0,0),(1,1,1)]
expected=[[0,1,1,1,1],[1,0,2,2,1],[1,2,0,2,1],[1,2,2,0,1],[1,1,1,1,0]]
for n in [3,4,7,20,101]:
    for base in [Q(3,2),Q(2),Q(3)]:
        vec=[v+(0,)*(n-2) for v in raw]
        ps=[]
        for v in vec:
            xs=[base**a for a in v];total=sum(xs)
            ps.append(tuple(x/total for x in xs))
        check('distinct_interior_points',len(set(ps))==5 and all(sum(p)==1 and min(p)>0 for p in ps))
        for i,j in pairs:
            p,q=ps[i],ps[j]
            # Find the actual coordinate-zero times along the affine chord.
            roots=[-a/(bb-a) for a,bb in zip(p,q) if a!=bb]
            left=max(t for t in roots if t<0)
            right=min(t for t in roots if t>1)
            check('boundary_parameters',left<0 and right>1)
            lp=[a+left*(bb-a) for a,bb in zip(p,q)]
            rp=[a+right*(bb-a) for a,bb in zip(p,q)]
            check('boundary_locations',min(lp)==0 and min(rp)==0 and sum(lp)==sum(rp)==1)
            cr=right*(1-left)/((right-1)*(-left))
            check('exact_cross_ratios',cr==base**expected[i][j])
        b=weights[0]
        check('positive_margin_exponent',sum(b[i]*b[j]*expected[i][j] for i,j in pairs)==1)
        # The product formulation certifies exp(weighted metric sum)=base.
        ratio=Q(1)
        for i,j in pairs:ratio*=base**(b[i]*b[j]*expected[i][j])
        check('positive_margin_product',ratio==base and ratio>1)

# The planar logarithmic identity is checked without evaluating any logarithm:
# square of the extremal ratio equals the product of three pairwise ratios.
planar=[(Q(a,6),Q(b,6),Q(6-a-b,6)) for a in range(1,5) for b in range(1,6-a)]
for p,q in combinations(planar,2):
    r=[p[i]/q[i] for i in range(3)]
    prod=Q(1)
    for i,j in combinations(range(3),2):prod*=max(r[i]/r[j],r[j]/r[i])
    check('planar_metric_identity',prod==(max(r)/min(r))**2)
    for i,j in combinations(range(3),2):
        a,b=p[i]/p[j],q[i]/q[j]
        if a==b:continue
        level=(a+b)/2
        f0=p[i]-level*p[j];f1=q[i]-level*q[j]
        t=f0/(f0-f1)
        point=[(1-t)*p[k]+t*q[k] for k in range(3)]
        check('actual_line_intersection',0<t<1 and point[i]==level*point[j])
for u in product(range(-3,4),repeat=3):
    check('tangent_identity',2*(max(u)-min(u))==sum(abs(u[i]-u[j]) for i,j in combinations(range(3),2)))
check('four_coordinate_nonextension',2*(max([0,0,0,1])-min([0,0,0,1]))!=sum(abs(a-b) for a,b in combinations([0,0,0,1],2)))

# Boundary escape of line coefficients and unbounded interval Hilbert lengths.
for m in range(1,31):
    coefficient=Q(1,2**m)
    check('boundary_line_escape',0<coefficient<=Q(1,2) and coefficient<Q(1,m))
    N=m+1;q=1-Q(1,N)
    check('bounded_chord_unbounded_crossratio',(1+q)/(1-q)==2*N-1)

root=Path(__file__).resolve().parent
out={'status':'PASS','assertions':sum(C.values()),'checks':dict(C),
     'artifact_sha256':hashlib.sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),
     'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'scope':'Exact cut inequalities, actual chord-boundary intersections, rational metric-product certificates, planar incidence and tangent checks. Coarea and measure local finiteness are proved analytically in the review.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
