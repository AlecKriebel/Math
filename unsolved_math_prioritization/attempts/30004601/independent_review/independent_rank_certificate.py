#!/usr/bin/env python3
"""Independent exact integer-polynomial and Fraction-matrix review; standard library only."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,hashlib

def add(a,b):
    c=a.copy()
    for e,v in b.items():
        c[e]=c.get(e,0)+v
        if not c[e]:del c[e]
    return c

def scale(a,c):return {e:c*v for e,v in a.items() if c*v}
def mul(a,b):
    c={}
    for e,u in a.items():
        for f,v in b.items():
            k=tuple(x+y for x,y in zip(e,f));c[k]=c.get(k,0)+u*v
    return {e:v for e,v in c.items() if v}
def lin(row):
    n=len(row);out={}
    for i,v in enumerate(row):
        e=[0]*n;e[i]=1
        if v:out[tuple(e)]=v
    return out

def diff(p,i):
    out={}
    for e,v in p.items():
        if e[i]:
            f=list(e);f[i]-=1;out[tuple(f)]=v*e[i]
    return out

def restrict(p,coords):
    n=len(next(iter(coords[0])));out={}
    for e,c in p.items():
        term={(0,)*n:c}
        for L,k in zip(coords,e):
            for _ in range(k):term=mul(term,L)
        out=add(out,term)
    return out

def mons(n,d):
    if n==1:return [(d,)]
    return [(i,)+j for i in range(d+1) for j in mons(n-1,d-i)]

def rref_certificate(M):
    R=[[F(x) for x in row] for row in M];m=len(R);n=len(R[0])
    E=[[F(i==j) for j in range(m)] for i in range(m)]
    original_ids=list(range(m));pivot_rows=[];pivot_columns=[];k=0
    for col in range(n):
        p=next((i for i in range(k,m) if R[i][col]),None)
        if p is None:continue
        R[k],R[p]=R[p],R[k];E[k],E[p]=E[p],E[k]
        original_ids[k],original_ids[p]=original_ids[p],original_ids[k]
        pivot_rows.append(original_ids[k]);pivot_columns.append(col)
        a=R[k][col];R[k]=[x/a for x in R[k]];E[k]=[x/a for x in E[k]]
        for j in range(m):
            if j!=k and R[j][col]:
                a=R[j][col];R[j]=[x-a*y for x,y in zip(R[j],R[k])];E[j]=[x-a*y for x,y in zip(E[j],E[k])]
        k+=1
        if k==m:break
    # Direct identity confirms both lower and upper rank certificates.
    for i in range(m):
        for j in range(n):assert sum(E[i][t]*M[t][j] for t in range(m))==R[i][j]
    assert determinant(E)!=0
    assert all(not any(row) for row in R[k:])
    for i,c in enumerate(pivot_columns):assert all(R[j][c]==(i==j) for j in range(m))
    minor=[[M[i][j] for j in pivot_columns] for i in pivot_rows]
    det=determinant(minor);assert det
    return {'rank':k,'pivot_columns':pivot_columns,'independent_original_rows':pivot_rows,
            'nonzero_minor_determinant':str(det),'row_transform':[[str(x) for x in row] for row in E],
            'rref':[[str(x) for x in row] for row in R]}

def determinant(M):
    a=[[F(x) for x in row] for row in M];n=len(a);d=F(1)
    for i in range(n):
        j=next((j for j in range(i,n) if a[j][i]),None)
        if j is None:return F(0)
        if j!=i:a[i],a[j]=a[j],a[i];d=-d
        pivot=a[i][i];d*=pivot
        for j in range(i+1,n):
            q=a[j][i]/pivot
            for k in range(i+1,n):a[j][k]-=q*a[i][k]
            a[j][i]=0
    return d

def macaulay(polars,n,d):
    columns=mons(n,d);multipliers=mons(n,d-6);rows=[]
    for p in polars:
        for e in multipliers:
            rows.append([mul(p,{e:1}).get(f,0) for f in columns])
    c=rref_certificate(rows)
    return {'number_variables':n,'degree':d,'monomial_columns':columns,'row_order':'polar index first, then multiplier exponent list','multiplier_exponents':multipliers,'matrix':rows,**c}

factor_rows=[(1,0,0,0),(0,1,0,0),(1,-1,0,0),(1,-2,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,1)]
Q={(0,0,0,0):1}
for row in factor_rows:Q=mul(Q,lin(row))
assert set(map(sum,Q))=={7}
polars=[diff(Q,i) for i in range(4)]
assert all(set(map(sum,p))=={6} for p in polars)
euler={}
for i,p in enumerate(polars):
 e=[0]*4;e[i]=1;euler=add(euler,mul(p,{tuple(e):1}))
assert euler==scale(Q,7)

C3=[(1,0,0),(0,1,0),(0,0,1),(1,2,3)]
C2=[(1,0),(0,1),(2,3),(7,11)]
certs=[];summary=[];allpolars={}
for n,C in [(3,C3),(2,C2)]:
    coords=list(map(lin,C));ps=[restrict(p,coords) for p in polars];allpolars[n]=ps
    L=[restrict(lin(a),coords) for a in factor_rows]
    # Check the flag has no coincident/nonzero hyperplane restrictions.
    vectors=[[p.get(tuple(int(i==j) for i in range(n)),0) for j in range(n)] for p in L]
    assert all(any(v) for v in vectors)
    for a,b in combinations(vectors,2):assert any(a[i]*b[j]!=a[j]*b[i] for i,j in combinations(range(n),2))
    for d in (6,7,8):
        c=macaulay(ps,n,d);certs.append(c)
        summary.append({'variables':n,'degree':d,'matrix_shape':[len(c['matrix']),len(c['monomial_columns'])],'rank':c['rank'],
                        'quotient_dimension':len(c['monomial_columns'])-c['rank'],
                        'nonzero_minor_determinant':c['nonzero_minor_determinant']})

# Explicit degree-one binary syzygy, tested as polynomial identity.
coeffs=[lin((11,0)),lin((0,11)),lin((-146,-219)),lin((175,275))]
syzygy={}
for a,p in zip(coeffs,allpolars[2]):syzygy=add(syzygy,mul(a,p))
assert not syzygy
assert [s['rank'] for s in summary]==[4,12,21,4,7,9]

# Independent scalar degree accounting underlying Hilbert--Burch, not a genericity sample.
degrees=[(a,b,c) for a in range(1,7) for b in range(a,7) for c in range(b,7)
         if a+b+c==6 and [a,b,c].count(1)==1]
assert degrees==[(1,2,3)]
def H2(d):return d+1-4*max(0,d-5)+sum(max(0,d-k+1) for k in (7,8,9))
assert [H2(d) for d in (6,7,8)]==[3,1,0]
assert 21-24+H2(6)==0 and 24-24+H2(7)==1

root=Path(__file__).resolve().parent
certificate={'arithmetic':'exact rational Fraction; integer polynomial dictionaries','flag_3':C3,'flag_2':C2,
             'ambient_factors':factor_rows,'matrices':certs}
(root/'RANK_CERTIFICATES.json').write_text(json.dumps(certificate,indent=2)+'\n')
out={'status':'PASS','matrices_checked':6,'results':summary,'binary_linear_syzygy_checked':True,
     'hilbert_burch_coefficient_degrees':degrees[0],'binary_H6_H7_H8':[H2(d) for d in (6,7,8)],
     'genericity_scope':'Genericity is proved algebraically in the reviewed proof; these are exact compatible-flag checks.',
     'rank_certificate_sha256':hashlib.sha256((root/'RANK_CERTIFICATES.json').read_bytes()).hexdigest(),
     'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,indent=2))
