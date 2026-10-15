#!/usr/bin/env python3
"""Independent exact Gram-locus controls. Universal nonexistence is a proof."""
from fractions import Fraction as Q
from itertools import product
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import sympy as s
C=Counter()
def ck(cat,cond):
    assert bool(cond),cat
    C[cat]+=1
def prod(vals):
    x=1
    for v in vals:x*=v
    return x
def grams(a,n):
    out=[]
    for i in range(n):
        rows=[[],[]]
        for other in product((0,1),repeat=n-1):
            for bit in (0,1):
                idx=other[:i]+(bit,)+other[i:]
                rows[bit].append(a.get(idx,Q(0)))
        x,y=rows
        xx=sum(t*t for t in x);yy=sum(t*t for t in y);xy=sum(t*u for t,u in zip(x,y))
        out.append((xx,yy,xy,xx*yy-xy*xy))
    return out
def hull(ds):return all(0<d<Q(1,4) and d<sum(ds)-d for d in ds)
u,v,w=s.symbols('u v w')
ts=[u,v,w];ds=[t*(1-t) for t in ts];a,b,c=ds
heron=2*(a*b+a*c+b*c)-a*a-b*b-c*c
q=(b+c-a)*(a+c-b)*(a+b-c)-heron**2/2
factors=[u-v-w,u-v+w,u+v-w,u-v-w+1,u-v+w-1,u+v-w-1,u+v+w-2,u+v+w-1]
ck('full_source_polynomial_factorization',s.expand(q+prod(factors)/2)==0)
for i,t in enumerate(ts):
    ck('pullback_involution',s.expand(q.subs(t,1-t)-q)==0)
ck('boundary_to_internal_plane',s.expand((u-v-w).subs(u,1-u)+(u+v+w-1))==0)
ck('coordinate_map_jacobian',s.expand(s.det(s.Matrix(ds).jacobian(ts))-(1-2*u)*(1-2*v)*(1-2*w))==0)
# Normalization derivative, proved symbolically before sign comparison.
r,d=s.symbols('r d',positive=True)
ar=2*d/(r+s.sqrt(r*r-4*d))
ck('ball_ratio_log_derivative',s.simplify(s.diff(ar,r)/ar+1/s.sqrt(r*r-4*d))==0)
# Norm-one rational even-parity tensors via rational parametrization of S^3.
tensor_controls=[]
for x,y,z in product((Q(-1),Q(-1,2),Q(0),Q(1,2),Q(1)),repeat=3):
    R=x*x+y*y+z*z;amps=((1-R)/(1+R),2*x/(1+R),2*y/(1+R),2*z/(1+R))
    coords=((0,0,0),(0,1,1),(1,0,1),(1,1,0))
    tensor=dict(zip(coords,amps));gg=grams(tensor,3)
    ck('rational_real_unit_tensor',sum(t*t for t in tensor.values())==1)
    lam=[]
    for aa,bb,ab,dd in gg:
        ck('rational_real_diagonal_Gram',ab==0 and aa+bb==1)
        ll=min(aa,bb);lam.append(ll)
        ck('rational_real_determinant',dd==ll*(1-ll))
    ck('polygon_necessity_controls',all(ll<=sum(lam)-ll for ll in lam))
    tensor_controls.append(tensor)
# Every rational triangle of this grid has the explicitly correct nonnegative weights.
for vals in product((Q(0),Q(1,12),Q(1,6),Q(1,4),Q(1,3),Q(5,12),Q(1,2)),repeat=3):
    if any(t>sum(vals)-t for t in vals):continue
    a,b,c=vals;ws=[1-(a+b+c)/2,(b+c-a)/2,(a+c-b)/2,(a+b-c)/2]
    ck('prescribed_real_realization',min(ws)>=0 and sum(ws)==1 and ws[0]>=Q(1,4))
    ck('prescribed_real_realization',(ws[2]+ws[3],ws[1]+ws[3],ws[1]+ws[2])==vals)
# Rational crossings of the true boundary remain inside the granted convex hull.
for b,c in product((Q(1,20),Q(1,10),Q(1,8),Q(1,6)),repeat=2):
    a=b+c;d0=[t*(1-t) for t in (a,b,c)]
    ck('true_boundary_inside_hull',hull(d0))
    ck('true_boundary_inside_hull',d0[1]+d0[2]-d0[0]==2*b*c)
    for eps in (Q(1,10000),Q(1,20000)):
        for sign in (-1,1):
            tt=(a+sign*eps,b,c);dd=[t*(1-t) for t in tt]
            ck('two_sided_boundary_crossing',hull(dd) and (all(t<sum(tt)-t for t in tt)==(sign<0)))
# The symmetry-conjugate plane has an open interior triangle patch.
for b,c in product((Q(3,10),Q(1,3),Q(7,20)),repeat=2):
    a=1-b-c
    for eps in (Q(-1,10000),Q(0),Q(1,10000)):
        tt=(a+eps,b,c);dd=[t*(1-t) for t in tt]
        ck('internal_conjugate_plane',all(0<t<Q(1,2) and t<sum(tt)-t for t in tt) and hull(dd))
# Exact zero slices, including non-coordinate unit factors.
units=[(Q(3,5),Q(4,5)),(Q(5,13),Q(12,13)),(Q(-1),Q(0))]
for a in tensor_controls[::8]:
    base=[g[3] for g in grams(a,3)]
    current=a
    for n,unit in zip((4,5,6),units):
        current={idx+(bit,):val*unit[bit] for idx,val in current.items() for bit in (0,1)}
        gg=grams(current,n)
        ck('rank_one_slice_norm',sum(t*t for t in current.values())==1)
        ck('rank_one_slice_determinants',[g[3] for g in gg]==base+[0]*(n-3))
# Four-factor source expression recomputed by pairing opposite sign choices.
roots=tuple(Q(x,100) for x in (49,36,36,1));dd=tuple(x*x for x in roots)
q1=prod(sum(dd)-2*x for x in dd)
positive_half=[sum(e*x for e,x in zip((1,)+tail,roots)) for tail in product((-1,1),repeat=3)]
q2=prod(positive_half)**2/2
ck('rational_counterexample',q1==Q(168760917,305175781250))
ck('rational_counterexample',q2==Q(23632249608,2384185791015625))
ck('rational_counterexample',q1-q2==Q(2589624828909,4768371582031250)>0)
ck('rational_counterexample',hull(dd))
ck('rational_spectral_separation',dd[0]>Q(2,5)*(1-Q(2,5)))
ck('rational_spectral_separation',dd[1]==dd[2]<Q(1,6)*(1-Q(1,6)))
ck('rational_spectral_separation',dd[3]<Q(1,100)*(1-Q(1,100)))
ck('rational_spectral_separation',Q(1,3)+Q(1,100)<Q(2,5))
# GHZ is an independent source-display control, not an input to the main proof.
ghz=s.MutableDenseNDimArray.zeros(2,2,2);ghz[0,0,0]=1/s.sqrt(2);ghz[1,1,1]=1/s.sqrt(2)
for i in range(3):
    rows=[]
    for bit in (0,1):
        rows.append([ghz[other[:i]+(bit,)+other[i:]] for other in product((0,1),repeat=2)])
    M=s.Matrix(rows)
    ck('GHZ_Gram_source_control',M*M.T==s.eye(2)/2 and (M*M.T).det()==s.Rational(1,4))
dghz=[Q(1,4)]*3
hghz=2*sum(dghz[i]*dghz[j] for i in range(3) for j in range(i+1,3))-sum(t*t for t in dghz)
ck('GHZ_printed_source_regions',prod(sum(dghz)-2*t for t in dghz)==Q(1,64)<hghz*hghz/2==Q(9,512))
ck('GHZ_printed_source_regions',Q(1,2)*(dghz[0]+dghz[1])==Q(1,4)>Q(3,16))
root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),
 'rational_unit_tensors':len(tensor_controls),
 'source_polynomial_pullback':'-1/2 times the eight affine factors listed in independent_checks.py',
 'positive_n4_Q1_minus_Q2':str(q1-q2),
 'artifact_sha256':sha256((root/'author_replay/COUNTEREXAMPLE.md').read_bytes()).hexdigest(),
 'sympy_version':s.__version__,
 'scope':'Exact finite/algebraic controls; all-polynomial nonexistence is the independently audited multiplicity proof.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
