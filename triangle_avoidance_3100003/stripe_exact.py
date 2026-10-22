#!/usr/bin/env python3
"""Exact rational fixed-width tests for three cyclic half-open equal stripes.
No sampled angles, no numerical tolerances. Coordinates and width use Fractions.
"""
from fractions import Fraction as F
from itertools import product
import json
H = [(1,1),(0,1),(-1,0),(-1,-1),(0,-1),(1,0)]

def inverse_gram(B,C):
    bb=sum(v*v for v in B); cc=sum(v*v for v in C)
    bc=sum(a*b for a,b in zip(B,C)); det=bb*cc-bc*bc
    assert det>0
    return ((cc/det,-bc/det),(-bc/det,bb/det))

def dotQ(x,y,M):
    return sum(x[i]*M[i][j]*y[j] for i in range(2) for j in range(2))

def extrema(M,m,n):
    vs=[(F(3*m+a),F(3*n+b)) for a,b in H]
    beta=max(dotQ(v,v,M) for v in vs)
    candidates=[]
    if m==n==0: candidates.append(F(0))
    for p,q in zip(vs,vs[1:]+vs[:1]):
        d=tuple(b-a for a,b in zip(p,q))
        t=max(F(0),min(F(1),-dotQ(p,d,M)/dotQ(d,d,M)))
        x=tuple(a+t*b for a,b in zip(p,d))
        candidates.append(dotQ(x,x,M))
    return min(candidates),beta

def ceilq(q): return -((-q.numerator)//q.denominator)

def test(B,C,w):
    B=tuple(map(F,B)); C=tuple(map(F,C)); w=F(w)
    assert w>0
    M=inverse_gram(B,C)
    # L1 bounds dominate Euclidean lengths, so these integer boxes are safe.
    mb=ceilq((sum(map(abs,B))/w+1)/3)
    nb=ceilq((sum(map(abs,C))/w+1)/3)
    hits=[]
    for m,n in product(range(-mb,mb+1),range(-nb,nb+1)):
        a,b=extrema(M,m,n)
        if w*w*a<1<w*w*b:
            hits.append({'m':m,'n':n,'alpha':str(a),'beta':str(b)})
    return {'width':str(w),'avoids':not hits,'tested_hexagons':(2*mb+1)*(2*nb+1),'intersections':hits}

if __name__=='__main__':
    cases=[
      ('boundary_h_equals_L_over_2',('1','0'),('1/2','1/2'),'1/2',True),
      ('improvement_h_below_L_over_2',('1','0'),('1/2','2/5'),'2/5',True),
      ('flat_counterexample',('1','0'),('1/2','1/10'),'1/10',False),
      ('right_3_4_5',('3','0'),('0','4'),'12/5',True),
      ('too_wide_one_strip',('1','0'),('1/2','1/2'),'51/100',False),
    ]
    results=[]
    for name,B,C,w,expected in cases:
        r=test(B,C,w);r['case']=name
        assert r['avoids']==expected, r
        results.append(r)
    print(json.dumps(results,indent=2))
