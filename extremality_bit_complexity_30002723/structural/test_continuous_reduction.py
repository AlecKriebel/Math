"""Finite-size validation of the new reduction, NOT an AHT implementation.
Dense union-find substitutes for AHT at small q. Geometry and ranks are exact.
The finite reference is the 4q-grid extremality test for continuous input.
"""
from fractions import Fraction as F
import random, json
import numpy as np
from scipy.optimize import linprog
import sympy as sp


def lp_vertex(q, f, rng):
    rows=[]
    for i in range(q):
        for j in range(q):
            r=np.zeros(q); r[i]-=1; r[j]-=1; r[(i+j)%q]+=1; rows.append(r)
    eq=[]; rhs=[]
    r=np.zeros(q);r[0]=1;eq.append(r);rhs.append(0)
    for i in range(q):
        r=np.zeros(q);r[i]+=1;r[(f-i)%q]+=1;eq.append(r);rhs.append(1)
    res=linprog([rng.uniform(-1,1) for _ in range(q)], A_ub=rows,b_ub=np.zeros(q*q),A_eq=eq,b_eq=rhs,bounds=(0,1),method='highs')
    assert res.success
    p=[F(float(x)).limit_denominator(10**6) for x in res.x]
    assert p[0]==0 and all(p[i]+p[(f-i)%q]==1 for i in range(q))
    assert all(p[i]+p[j]>=p[(i+j)%q] for i in range(q) for j in range(q))
    return p


def interp(p,x):
    q=len(p);x=F(x)%q;i=x.numerator//x.denominator;t=x-i
    return p[i]*(1-t)+p[(i+1)%q]*t


def clipping(poly,t,sign):
    # sign=1 retains x+y>=t, sign=-1 retains x+y<=t
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        va=sign*(sum(a)-t);vb=sign*(sum(b)-t)
        if va>=0:out.append(a)
        if (va<0<vb) or (vb<0<va):
            alpha=F(va,va-vb);out.append((a[0]+alpha*(b[0]-a[0]),a[1]+alpha*(b[1]-a[1])))
    return list(dict.fromkeys(out))


def polygons(B,q):
    B2=sorted(set(B+[b+q for b in B])); ints=list(zip(B,B[1:]));ints2=list(zip(B2,B2[1:]))
    for a,b in ints:
      for c,d in ints:
       for e,g in ints2:
        poly=clipping(clipping([(F(a),F(c)),(F(b),F(c)),(F(b),F(d)),(F(a),F(d))],e,1),g,-1)
        if len(poly)<3:continue
        area=sum(x*y2-y*x2 for (x,y),(x2,y2) in zip(poly,poly[1:]+poly[:1]))
        if area:yield poly


def coarse_reduce(p,f):
    q=len(p);B=[0]+[i for i in range(1,q) if p[(i+1)%q]-p[i]!=p[i]-p[i-1] or i==f]+[q]
    B2=sorted(set(B+[b+q for b in B]));par=list(range(q))
    def find(a):
        while par[a]!=a:par[a]=par[par[a]];a=par[a]
        return a
    def union(a,b):par[find(a%q)]=find(b%q)
    delta=lambda x,y:interp(p,x)+interp(p,y)-interp(p,x+y)
    seeds=[];vertices=set()
    for poly in polygons(B,q):
        vertices.update(poly)
        if all(delta(x,y)==0 for x,y in poly):
            projections=[[v[i] for v in poly] for i in range(2)]+[[sum(v) for v in poly]]
            reps=[]
            for proj in projections:
                a,b=int(min(proj)),int(max(proj));reps.append(a%q)
                for k in range(a,b-1):union(k,k+1)
            for r in reps[1:]:union(reps[0],r)
            seeds.append(reps[0])
    # y=t edge. x=t repeats exactly the same pairings by symmetry.
    for t in B:
        cuts=sorted(set([0,q]+B+[z-t for z in B2 if 0<=z-t<=q]))
        for a,b in zip(cuts,cuts[1:]):
            if delta(a,t)==delta(b,t)==0:
                for k in range(a,b):union(k,k+t)
    # x+y=t edge
    for t in B2:
        a0=max(0,t-q);b0=min(q,t)
        if a0>=b0:continue
        cuts=sorted(set([a0,b0]+[b for b in B if a0<=b<=b0]+[t-b for b in B if a0<=t-b<=b0]))
        for a,b in zip(cuts,cuts[1:]):
            if delta(a,t-a)==delta(b,t-b)==0:
                for k in range(a,b):union(k,t-k-1)
    roots=sorted(set(find(k) for k in range(q)));covered=set(find(k) for k in seeds)
    if any(r not in covered for r in roots):return {'extreme':False,'covered':False,'n':len(B),'components':len(roots)}
    rootcol={r:j for j,r in enumerate(roots)};m=len(roots)
    def prefix(x):
        x=int(x);assert 0<=x<=2*q
        counts=[0]*m
        for k in range(x):counts[rootcol[find(k%q)]]+=1
        return counts
    rows=[prefix(q),prefix(f)]
    for x,y in vertices:
        if delta(x,y)==0:
            u,v,w=prefix(x),prefix(y),prefix(x+y)
            rows.append([a+b-c for a,b,c in zip(u,v,w)])
    rank=sp.Matrix(rows).rank()
    return {'extreme':rank==m,'covered':True,'n':len(B),'components':m,'rank':rank,'nullity':m-rank}


def dense_ref(p,f):
    q=len(p);N=4*q;rows=[]
    r=[0]*N;r[0]=1;rows.append(r)
    r=[0]*N;r[4*f]=1;rows.append(r)
    vals=[interp(p,F(i,4)) for i in range(N)]
    for i in range(N):
      for j in range(N):
        if vals[i]+vals[j]==vals[(i+j)%N]:
            r=[0]*N;r[i]+=1;r[j]+=1;r[(i+j)%N]-=1;rows.append(r)
    # Exact DomainMatrix rank is substantially faster for the integer reference.
    from sympy.polys.matrices import DomainMatrix
    rank=DomainMatrix.from_Matrix(sp.Matrix(rows)).rank()
    return {'extreme':rank==N,'nullity':N-rank}


def main():
    rng=random.Random(302720);out=[]
    for q in range(3,17):
      for trial in range(5):
        f=rng.randrange(1,q);p=lp_vertex(q,f,rng)
        if trial%2:
            other=lp_vertex(q,f,rng);p=[(x+y)/2 for x,y in zip(p,other)]
        got=coarse_reduce(p,f);ref=dense_ref(p,f)
        row={'q':q,'f':f,'trial':trial,**got,'reference':ref}
        assert got['extreme']==ref['extreme'],(row,p)
        if got['covered']:assert got['nullity']==ref['nullity'],(row,p)
        out.append(row)
    print(json.dumps({'status':'PASS','cases':len(out),'covered_cases':sum(r['covered'] for r in out),'extreme_cases':sum(r['extreme'] for r in out),'cases_detail':out},indent=2))
if __name__=='__main__':main()
