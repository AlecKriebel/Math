#!/usr/bin/env python3
"""Exact rational checks for the normalized hexagonal-bipyramid calculation.

No numerical convex-hull library or downloaded data is used. This finite checker
corroborates the identities and incidence claims; it does not prove universal
quantifiers or audit the quoted shadow-system theorem.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from functools import cmp_to_key
import json
from pathlib import Path

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def det(a,b,c): return dot(a,cross(b,c))
def solve_one(a,b,c):
    d=det(a,b,c)
    if not d:return None
    return tuple((x+y+z)/d for x,y,z in zip(cross(b,c),cross(c,a),cross(a,b)))
def normals(vertices):
    out=set()
    for a,b,c in combinations(vertices,3):
        n=solve_one(a,b,c)
        if n is not None and all(dot(n,v)<=1 for v in vertices):out.add(n)
    return sorted(out)
def cyclic(vertices,n):
    omit=next(i for i,t in enumerate(n) if t)
    ix=[i for i in range(3) if i!=omit]
    c=tuple(sum(v[i] for v in vertices)/len(vertices) for i in range(3))
    def cmp(v,w):
        a,b=([u[i]-c[i] for i in ix] for u in [v,w])
        ha=(a[1]>0 or (a[1]==0 and a[0]>=0));hb=(b[1]>0 or (b[1]==0 and b[0]>=0))
        if ha!=hb:return -1 if ha else 1
        z=a[0]*b[1]-a[1]*b[0]
        return -1 if z>0 else 1 if z<0 else 0
    return sorted(vertices,key=cmp_to_key(cmp))
def hull_data(vertices):
    ns=normals(vertices);sizes=[];volume=Q(0)
    for n in ns:
        face=cyclic([v for v in vertices if dot(n,v)==1],n)
        sizes.append(len(face))
        for i in range(1,len(face)-1):volume+=abs(det(face[0],face[i],face[i+1]))/6
    return ns,sorted(sizes),volume

def formula(p,q,r):return Q(4,3)*(p+q+1)*(4-((p+q-1)**2+r*r/3)/(p*q))
def vertices(p,q,r):
    half=[(Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),(Q(0),Q(0),Q(1)),(p,q,r)]
    return half+[tuple(-x for x in v) for v in half]

samples=[]
for p,q in product([Q(1,2),Q(3,4),Q(1),Q(5,4),Q(3,2),Q(2)],repeat=2):
    m=min(p+q-1,1-abs(p-q))
    if m<=0:continue
    for r in [Q(0),m/3,-m/2]:samples.append((p,q,r))
for p,q,r in samples:
    vs=vertices(p,q,r)
    ns,fs,v=hull_data(vs)
    ds,dfs,pv=hull_data(ns)
    assert fs==[3]*12,(p,q,r,fs)
    assert dfs==[4]*6+[6]*2,(p,q,r,dfs)
    assert set(ds)==set(vs)
    assert v==Q(2,3)*(p+q+1)
    assert pv==8-2*((p+q-1)**2+r*r/3)/(p*q)
    assert v*pv==formula(p,q,r)
    assert Q(32,3)<v*pv<=12
    assert (v*pv==12)==(p==q==1 and r==0)
    # A small, strictly admissible increase of |r| lowers the product at every point.
    m=min(p+q-1,1-abs(p-q));rr=(abs(r)+m)/2
    assert formula(p,q,rr)<formula(p,q,r)

# Exact order-two Taylor algebra around (s,d,r)=(2,0,0).
zero=(0,0,0)
def add(a,b):
    c=a.copy()
    for k,v in b.items():c[k]=c.get(k,Q(0))+v
    return {k:v for k,v in c.items() if v}
def scale(a,v):return {k:x*v for k,x in a.items() if x*v}
def mul(a,b):
    c={}
    for x,v in a.items():
        for y,w in b.items():
            k=tuple(i+j for i,j in zip(x,y))
            if sum(k)<=2:c[k]=c.get(k,Q(0))+v*w
    return {k:v for k,v in c.items() if v}
def inv(a):
    z=a[zero];h=scale(add(a,{zero:-z}),1/z)
    return scale(add(add({zero:Q(1)},scale(h,-1)),mul(h,h)),1/z)
s={zero:Q(2),(1,0,0):Q(1)};d={(0,1,0):Q(1)};r={(0,0,1):Q(1)}
sm=add(s,{zero:-Q(1)});sp=add(s,{zero:Q(1)})
den=add(mul(s,s),scale(mul(d,d),-1))
num=add(mul(sm,sm),scale(mul(r,r),Q(1,3)))
f=scale(mul(sp,add({zero:Q(4)},scale(mul(num,inv(den)),-4))),Q(4,3))
expected={zero:Q(12),(2,0,0):Q(-1,3),(0,2,0):Q(-1),(0,0,2):Q(-4,3)}
assert f==expected,(f,expected)
# Boundary cube and a nonsingular transverse path.
ns,fs,v=hull_data(vertices(Q(1),Q(1),Q(1)))
_,dfs,pv=hull_data(ns)
assert fs==[4]*6 and dfs==[3]*8 and v*pv==Q(32,3)
for eps in [Q(1,2),Q(1,3),Q(1,10)]:
    assert formula(Q(1),Q(1),eps)==12-Q(4,3)*eps*eps
# Exact dimension-count f-vector eliminations relevant to the shadow route.
assert [(V,F) for V in range(6,101,2) for F in range(4,101,2)
        if V==F+2 and 3*V==2*(V+F-2)]==[(8,6)]
assert [(p,q) for p in range(0,101,2) for q in range(0,101,2)
        if p==4 and 4*q<=3*p and p+q>=6]==[(4,2)]
result={"status":"pass","rational_interior_realizations":len(samples),
"incidences":"12 primal triangular facets; 6 quadrilateral and 2 hexagonal polar facets",
"volume_formula":"4/3*(p+q+1)*(4-((p+q-1)^2+r^2/3)/(p*q))",
"critical_point":{"p":"1","q":"1","r":"0","product":"12"},
"hessian_s_d_r":[["-2/3","0","0"],["0","-2","0"],["0","0","-8/3"]],
"boundary_cube_product":"32/3","scope":"Finite exact checks; universal proofs are in PROOF.md."}
Path(__file__).with_name('exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
