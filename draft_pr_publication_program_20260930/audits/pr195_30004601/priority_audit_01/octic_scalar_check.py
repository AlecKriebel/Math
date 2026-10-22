#!/usr/bin/env python3
"""Exact modular nonvanishing certificates for Janasz--Pokora's 14 rigid octics.
Nonzero minors modulo a splitting prime imply characteristic-zero nonvanishing.
The generic-cutoff deduction and limits are stated in REPORT.md. No writes.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path

PRIME = 1009
BASE = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
FACTORS = {
 '1': [[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]],
 '3': [[1,1,0,0],[0,1,1,0],[0,1,0,-1],[1,-1,-1,1]],
 '19': [[1,1,0,0],[0,1,1,0],[1,0,-1,-1],[1,1,1,-1]],
 '32': [[1,1,0,0],[0,1,1,0],[1,-1,-1,-1],[1,1,-1,1]],
 '69': [[1,1,0,0],[1,-1,1,0],[1,-1,0,-1],[1,1,-1,-1]],
 '93': [[1,1,0,0],[1,-1,1,0],[0,1,-1,-1],[1,0,1,-1]],
 '238': [[1,1,1,-1],[1,1,-1,1],[1,-1,1,1],[-1,1,1,1]],
 '239': [[1,1,1,0],[1,1,0,1],[1,0,1,1],[0,1,1,1]],
 '240': [[1,1,1,0],[1,1,-1,1],[1,-1,1,1],[1,-1,-1,-1]],
 '241': [[1,1,1,1],[1,1,-1,-1],[0,1,-1,1],[1,0,1,-1]],
 '245': [[1,1,1,0],[0,1,1,1],[1,-1,0,-1],[1,-1,1,1]],
 'A': [[1,1,0,0],[1,1,1,-1],[(-1,1),-2,(-1,1),0],[0,2,(1,-1),-2]],
 'B': [[1,1,1,0],[1,0,1,-1],[(-1,1),(1,1),-2,2],[(-1,1),(-1,1),-2,(1,1)]],
 'C': [[1,1,1,0],[0,(-1,1),-2,2],[2,2,0,(-1,1)],[(3,-1),2,(1,-1),(-1,1)]]
}
# Coherent flag: w=5s+11t+23u, followed by u=13s+29t.
SECTIONS = {'3':[[1,0,0],[0,1,0],[0,0,1],[5,11,23]],
            '2':[[1,0],[0,1],[13,29],[304,678]]}

def determinant(m):
    a=[[v % PRIME for v in row] for row in m]; out=1
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None: return 0
        if pivot != j: a[j],a[pivot]=a[pivot],a[j];out=-out
        out=out*a[j][j] % PRIME
        for i in range(j+1,len(a)):
            q=a[i][j]*pow(a[j][j],-1,PRIME) % PRIME
            a[i]=[(x-q*y) % PRIME for x,y in zip(a[i],a[j])]
    return out % PRIME

def rank_certificate(m):
    a=[[v % PRIME for v in row] for row in m];ids=list(range(len(a)))
    r=0; rows=[]; cols=[]
    for c in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][c]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r];ids[r],ids[pivot]=ids[pivot],ids[r]
        rows.append(ids[r]);cols.append(c)
        for i in range(r+1,len(a)):
            q=a[i][c]*pow(a[r][c],-1,PRIME) % PRIME
            a[i]=[(x-q*y) % PRIME for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    d=determinant([[m[i][j] for j in cols] for i in rows]);assert d
    return dict(rows=len(m),columns=len(m[0]),rank=r,minor_rows=rows,minor_columns=cols,minor_determinant_mod_prime=d)

def analyze(name,factors):
    radicand=-3 if name in ('A','B') else 5 if name=='C' else None
    root=next(x for x in range(PRIME) if x*x % PRIME==radicand % PRIME) if radicand else 0
    ns=[[((v[0]+v[1]*root) if isinstance(v,tuple) else v) % PRIME for v in row] for row in BASE+factors]
    out=dict(name=name,source='Janasz--Pokora arXiv:2502.17031v4, Section 5',
             coefficient_convention='An integer pair [a,b] denotes a+b*alpha; other integers are rational.',
             radicand=radicand,alpha_mod_prime=root,factor_normals=BASE+factors,sections={})
    for dim,s in SECTIONS.items():
        r=len(s[0]);ls=[[sum(f[j]*s[j][k] for j in range(4)) % PRIME for k in range(r)] for f in ns]
        pairs=[]
        for i,j in combinations(range(8),2):
            columns=next((c for c in combinations(range(r),2) if determinant([[ls[i][k] for k in c],[ls[j][k] for k in c]])),None)
            assert columns is not None,(name,dim,i,j)
            pairs.append(dict(factors=[i,j],columns=columns,determinant_mod_prime=determinant([[ls[i][k] for k in columns],[ls[j][k] for k in columns]])))
        m=[]
        for i,f in enumerate(ns):
            for k in range(r):
                row=[0]*(4*r+8)
                for j in range(4):row[j*r+k]=f[j]
                row[4*r+i]=-ls[i][k];m.append(row)
        m.append([0]*(4*r)+[1]*8)
        c=rank_certificate(m);assert c['rank']==4*r+8,(name,dim,c)
        out['sections'][dim]=dict(section_matrix=s,restricted_normals_mod_prime=ls,pairwise_nonproportional_minors=pairs,scalar_syzygy_system=c,linear_syzygy_dimension=0)
    return out

output=dict(prime=PRIME,arithmetic='Exact finite-field arithmetic, no floating point. Nonzero rank minors certify nonzero algebraic-integer minors in characteristic zero.',examples=[analyze(name,factors) for name,factors in FACTORS.items()])
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--verify',type=Path)
args=parser.parse_args()
if args.verify:
    assert json.loads(args.verify.read_text())==json.loads(json.dumps(output)),'frozen certificate differs'
    print(json.dumps(dict(verified=True,examples=len(FACTORS),writes=False)))
else:
    print(json.dumps(output,indent=2))
