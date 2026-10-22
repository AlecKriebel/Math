#!/usr/bin/env python3
"""Earlier arrangement overlap checks; exact standard-library arithmetic.
Ambient differentiation precedes restriction. Nonzero minors certify ranks.
Generic conclusions also use the bounds/Hilbert--Burch argument in REPORT.md.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

def mons(n,d):
    return [(d,)] if n==1 else [(i,)+t for i in range(d+1) for t in mons(n-1,d-i)]
def mul(a,b):
    o={}
    for e,c in a.items():
        for f,d in b.items():
            g=tuple(x+y for x,y in zip(e,f)); o[g]=o.get(g,0)+c*d
    return {e:c for e,c in o.items() if c}
def lin(row):
    return {tuple(int(j==i) for j in range(len(row))):c for i,c in enumerate(row) if c}
def prod(ps,n):
    o={(0,)*n:1}
    for p in ps:o=mul(o,p)
    return o
def diff(p,j):
    o={}
    for e,c in p.items():
        if e[j]:
            f=list(e);f[j]-=1;o[tuple(f)]=c*e[j]
    return o
def sub(p,s):
    r=len(s[0]);o={}
    for e,c in p.items():
        q=prod([lin(s[j]) for j,d in enumerate(e) for _ in range(d)],r)
        for f,d in q.items():o[f]=o.get(f,0)+c*d
    return {e:c for e,c in o.items() if c}
def pivots(m):
    a=[[F(v) for v in row] for row in m];ids=list(range(len(a)));r=0;rows=[];cols=[]
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];ids[r],ids[p]=ids[p],ids[r];rows.append(ids[r]);cols.append(c)
        for i in range(r+1,len(a)):
            q=a[i][c]/a[r][c]
            if q:
                for j in range(c,len(a[0])):a[i][j]-=q*a[r][j]
        r+=1
        if r==len(a):break
    return rows,cols
def det(m):
    a=[[F(v) for v in row] for row in m];o=F(1)
    for j in range(len(a)):
        p=next((i for i in range(j,len(a)) if a[i][j]),None)
        if p is None:return F(0)
        if p!=j:a[j],a[p]=a[p],a[j];o=-o
        o*=a[j][j]
        for i in range(j+1,len(a)):
            q=a[i][j]/a[j][j]
            for k in range(j+1,len(a)):a[i][k]-=q*a[j][k]
            a[i][j]=0
    return o
def cert(m):
    rows,cols=pivots(m);d=det([[m[i][j] for j in cols] for i in rows]);assert d
    return dict(rows=len(m),columns=len(m[0]),rank=len(cols),minor_rows=rows,minor_columns=cols,minor_determinant=str(d))
def analyze(name,ns,s3,s2,degrees):
    a=len(ns[0]);n=len(ns);q=prod([lin(f) for f in ns],a);ps=[diff(q,j) for j in range(a)]
    out=dict(name=name,factor_normal_rows=ns,factors=n,ambient_dimension=a,normal_rank=len(pivots(ns)[1]),generator_degree=n-1,sections={})
    for s in [s3,s2]:
        r=len(s[0]);ls=[[sum(f[j]*s[j][k] for j in range(a)) for k in range(r)] for f in ns]
        assert all(any(f) for f in ls)
        assert all(len(pivots([ls[i],ls[j]])[1])==2 for i,j in combinations(range(n),2))
        mat=[]
        for i in range(n):
            for k in range(r):
                eq=[0]*(a*r+n)
                for j in range(a):eq[j*r+k]=ns[i][j]
                eq[a*r+i]=-ls[i][k];mat.append(eq)
        mat.append([0]*(a*r)+[1]*n);c=cert(mat);c['kernel_dimension']=a*r+n-c['rank']
        data=dict(section_matrix_ambient_rows=s,restricted_factor_rows=ls,pairwise_nonproportional=True,scalar_syzygy_system=c,macaulay={})
        fs=[sub(f,s) for f in ps]
        for d in degrees:
            ms=mons(r,d);cols=[]
            for f in fs:
                for e in mons(r,d-(n-1)):
                    p={tuple(x+y for x,y in zip(e,g)):v for g,v in f.items()};cols.append([p.get(g,0) for g in ms])
            c=cert([list(v) for v in zip(*cols)]);c['quotient_hilbert_function']=len(ms)-c['rank'];data['macaulay'][str(d)]=c
        out['sections'][str(r)]=data
    return out
examples=[
 analyze('PT2020 Example 8.2 = PT2022 Example 8.4',[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,-1,1,0],[0,1,1,-3],[1,0,1,1],[1,0,0,-5]],[[1,0,0],[0,1,0],[0,0,1],[1,2,3]],[[1,0],[0,1],[2,3],[7,11]],[7,8,9]),
 analyze('PT2020 Example 8.11',[[1,0,0,0,0],[0,1,0,0,0],[0,0,0,1,0],[1,-1,1,1,0],[1,0,0,0,1],[1,1,0,1,1],[0,0,1,-1,-1]],[[1,0,0],[0,1,0],[0,0,1],[1,2,3],[2,-3,5]],[[1,0],[0,1],[2,3],[7,11],[12,12]],[6,7,8]),
 analyze('PT2020 Example 8.6',[[1,0,0,0],[0,0,0,1],[1,1,0,1],[1,-1,0,0],[1,0,1,0]],[[1,0,0],[0,1,0],[0,0,1],[1,2,3]],[[1,0],[0,1],[2,3],[7,11]],[4,5,6])]
o=dict(arithmetic='Python standard library, integer polynomials and Fraction elimination; no floating point',examples=examples)
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--verify',type=Path,help='compare against a frozen certificate without writing any file')
args=parser.parse_args()
if args.verify:
    assert json.loads(args.verify.read_text())==o, 'frozen certificate differs'
    print(json.dumps({'verified':True,'examples':len(examples),'writes':False}))
else:
    print(json.dumps(o,indent=2))
