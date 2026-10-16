#!/usr/bin/env python3
"""Exact checks of the current-algebra exterior coefficient action maps.

Free-Lie bases are built as independent spans of generator commutators in the
tensor algebra, rather than by the author's Lyndon-word construction. These
bounded models verify sign twists and degree conventions, not a general solution.
Run: python independent_checks.py
"""
from itertools import product,combinations
from functools import lru_cache
from math import comb
from pathlib import Path
import hashlib,json
import sympy as s

def comm(a,b):
    out={}
    for x,c in a.items():
        for y,d in b.items():
            out[x+y]=out.get(x+y,0)+c*d
            out[y+x]=out.get(y+x,0)-c*d
    return {w:c for w,c in out.items() if c}
@lru_cache(None)
def lie(m,d):
    if d==1:return tuple({(j,):1} for j in range(m))
    candidates=[comm({(j,):1},b) for j in range(m) for b in lie(m,d-1)]
    words=list(product(range(m),repeat=d))
    A=s.Matrix([[b.get(w,0) for b in candidates] for w in words])
    chosen=A.rref()[1]
    return tuple(candidates[j] for j in chosen)
@lru_cache(None)
def action(m,d,j,k):
    basis=lie(m,d+1)
    words=list(product(range(m),repeat=d+1))
    B=s.Matrix([[b.get(w,0) for b in basis] for w in words])
    rows=B.T.rref()[1]
    c=comm({(j,):1},lie(m,d)[k])
    col=s.Matrix([c.get(words[z],0) for z in rows])
    coeff=B.extract(rows,list(range(B.cols))).inv()*col
    assert B*coeff==s.Matrix([c.get(w,0) for w in words])
    return tuple(coeff)

def schur_dim(shape,m):
    value=s.S.One
    for i,length in enumerate(shape):
        for j in range(length):
            hook=length-j+sum(row>j for row in shape[i+1:])
            value*=s.Rational(m+j-i,hook)
    return int(value)

def model(m,e,r,d):
    entries=[(a,k,j) for a in range(e) for k in range(1,d+1) for j in range(len(lie(m,k)))]
    # Only degrees <=d-r+1 can contribute to an r-fold wedge of total degree d.
    entries=[x for x in entries if x[1]<=d-r+1]
    index={x:j for j,x in enumerate(entries)}
    wedges=list(combinations(range(len(entries)),r))
    source=[w for w in wedges if sum(entries[j][1] for j in w)==d-1]
    target=[w for w in wedges if sum(entries[j][1] for j in w)==d]
    rowindex={w:j for j,w in enumerate(target)}
    A=s.zeros(len(target),m*len(source))
    for gen in range(m):
        for n,w in enumerate(source):
            for position,ind in enumerate(w):
                a,k,j=entries[ind]
                for q,c in enumerate(action(m,k,gen,j)):
                    if not c:continue
                    replaced=list(w);replaced[position]=index[(a,k+1,q)]
                    if len(set(replaced))<r:continue
                    inversions=sum(replaced[u]>replaced[v] for u in range(r) for v in range(u+1,r))
                    A[rowindex[tuple(sorted(replaced))],gen*len(source)+n]+=(-1)**inversions*c
    rank=A.to_DM().rank()
    actual=A.cols-rank
    if d==r+1:
        expected=(comb(e,r) if e>=r else 0)*comb(m+r,r+1)
    elif d==r+2:
        expected=comb(e+r-1,r)*(comb(m,r+2) if m>=r+2 else 0)
        if r>1: expected+=(comb(e,r) if e>=r else 0)*schur_dim((r,1,1),m)
    else:
        assert r==1 and d==4
        expected=e*schur_dim((2,2),m)
    assert actual==expected,(m,e,r,d,actual,expected)
    return {'dim_V':m,'dim_E':e,'ideal_degree':r,'V_degree':d,'action_domain':A.cols,'action_codomain':A.rows,'rank':rank,'kernel':actual,'predicted':expected}

cases=[(3,1,1,2),(3,1,1,3),(3,1,1,4),
       (4,1,2,3),(4,1,2,4),(3,2,2,3),(3,2,2,4),
       (3,3,3,4),(3,2,3,5)]
rows=[model(*case) for case in cases]
p1,p2,p3,p4=s.symbols('p1 p2 p3 p4')
ell={1:p1,2:(p1**2-p2)/2,3:(p1**3-p3)/3,4:(p1**4-p2**2)/4}
expected={2:(p1**2+p2)/2,3:(p1**3-3*p1*p2+2*p3)/6,4:(p1**4+3*p2**2-4*p1*p3)/12}
for d in (2,3,4):
    assert s.expand(p1*ell[d-1]-ell[d]-expected[d])==0
receipt={'status':'PASS','sympy_version':s.__version__,'arithmetic':'exact rational ranks','models':rows,'cyclic_character_checks':3,'scope':'Nine finite models and three character identities; no all-degree decomposition claim.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
