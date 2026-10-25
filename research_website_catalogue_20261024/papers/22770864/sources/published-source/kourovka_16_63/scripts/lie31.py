#!/usr/bin/env python3
"""Exact reconstruction of a 31-dimensional perfect Lie algebra.
All coefficients are integers. No external symbolic-algebra service is used.
The starting pattern is Omirov--Ruan, arXiv:2605.04602v1, Theorem 4.8;
raw (unnormalized) transvectants specify our own complete normalization.
"""
from __future__ import annotations
from itertools import combinations
from math import comb, prod
from pathlib import Path
import json, sys, time
import numpy as np

D=31
MODS={'U':(6,3),'V':(4,10),'W':(6,15),'T':(2,22),'R':(4,25),'Z':(0,30)}
NAMES=['h','e','f']+[f'{m}{i}' for m,(d,start) in MODS.items() for i in range(d+1)]
assert len(NAMES)==D

def falling(a:int,b:int)->int:
    return 0 if a<b else prod(range(a-b+1,a+1))

def transvectant(m:int,n:int,r:int,i:int,j:int)->tuple[int,int]:
    k_out=i+j-r
    if not 0<=k_out<=m+n-2*r: return k_out,0
    coefficient=sum((-1)**k*comb(r,k)*falling(m-i,r-k)*falling(i,k)
                    *falling(n-j,k)*falling(j,r-k) for k in range(r+1))
    return k_out,coefficient

def bracket_table()->np.ndarray:
    C=np.zeros((D,D,D),dtype=np.int64)
    def put(i,j,k,v):
        assert i!=j or v==0
        assert C[i,j,k] in (0,v)
        C[i,j,k]=v; C[j,i,k]=-v
    put(0,1,1,2); put(0,2,2,-2); put(1,2,0,1)
    for m,(degree,start) in MODS.items():
        for i in range(degree+1):
            put(0,start+i,start+i,degree-2*i)
            if i: put(1,start+i,start+i-1,i)
            if i<degree: put(2,start+i,start+i+1,degree-i)
    products=[('U','U','W',3),('U','V','T',4),('U','W','T',5),
              ('U','R','T',4),('V','V','T',3),('V','R','Z',4),('R','R','T',3)]
    for aa,bb,cc,r in products:
        m,a=MODS[aa]; n,b=MODS[bb]; degree,c=MODS[cc]
        assert degree==m+n-2*r
        for i in range(m+1):
            for j in range(n+1):
                if aa==bb and i>=j: continue
                k,v=transvectant(m,n,r,i,j)
                if v: put(a+i,b+j,c+k,v)
    return C

def bracket(C,x,y):
    ans=np.zeros(D,dtype=np.int64)
    for i in np.flatnonzero(x):
        for j in np.flatnonzero(y): ans += int(x[i])*int(y[j])*C[i,j]
    return ans

def test_jacobi(C):
    checks=0
    for i,j,k in combinations(range(D),3):
        ans=np.zeros(D,dtype=np.int64)
        for a in np.flatnonzero(C[j,k]): ans += int(C[j,k,a])*C[i,a]
        for a in np.flatnonzero(C[k,i]): ans += int(C[k,i,a])*C[j,a]
        for a in np.flatnonzero(C[i,j]): ans += int(C[i,j,a])*C[k,a]
        if np.any(ans):
            raise AssertionError(f'Jacobi failure {NAMES[i],NAMES[j],NAMES[k]}: {ans.tolist()}')
        checks+=1
    assert np.array_equal(C,-C.swapaxes(0,1))
    return checks

def adapted_basis():
    E=np.eye(D,dtype=np.int64)
    x=E[0].copy()
    y=E[1]+E[2]+E[MODS['U'][1]+1]+E[MODS['V'][1]]+E[MODS['R'][1]+2]
    t=E[MODS['U'][1]].copy()
    others=[i for i in range(D) if i not in (0,1,MODS['U'][1])]
    P=np.column_stack([x,y,t]+[E[i] for i in others])
    # Integral inverse, by the fact that y replaces e with coefficient one.
    import sympy as sp
    Pinv=np.array(sp.Matrix(P.tolist()).inv().tolist(),dtype=np.int64)
    assert np.array_equal(P@Pinv,E)
    weights=np.array([0,0,1]+[2]*(D-3),dtype=np.int64)
    return P,Pinv,weights,['x=h','y=e+f+U1+V0+R2','t=U0']+[NAMES[i] for i in others]

def change_basis(C,P,Pinv):
    out=np.zeros_like(C)
    for i in range(D):
        for j in range(i+1,D):
            out[i,j]=Pinv@bracket(C,P[:,i],P[:,j]); out[j,i]=-out[i,j]
    return out

def derivation_matrix(C):
    """Rows (i<j,k), columns (output,input) of D. Delta=D[,]-[D,]-[,D]."""
    pairs=list(combinations(range(D),2))
    M=np.zeros((len(pairs)*D,D*D),dtype=np.int64)
    for pairidx,(i,j) in enumerate(pairs):
        base=pairidx*D
        for k in range(D):
            for a in np.flatnonzero(C[i,j]): M[base+k,k*D+a]+=C[i,j,a]
            for a in np.flatnonzero(C[:,j,k]): M[base+k,a*D+i]-=C[a,j,k]
            for a in np.flatnonzero(C[i,:,k]): M[base+k,a*D+j]-=C[i,a,k]
    return M

def main():
    root=Path(__file__).resolve().parents[1]
    t0=time.perf_counter(); C=bracket_table(); checks=test_jacobi(C)
    P,Pinv,weights,names=adapted_basis(); Ca=change_basis(C,P,Pinv)
    assert test_jacobi(Ca)==checks
    np.savez_compressed(root/'data/lie31_tables.npz',C=C,P=P,Pinv=Pinv,weights=weights,Ca=Ca)
    terms=[[i,j,k,int(C[i,j,k])] for i in range(D) for j in range(i+1,D) for k in np.flatnonzero(C[i,j])]
    terms=[[int(x) for x in row] for row in terms]
    (root/'data/lie31_brackets.json').write_text(json.dumps({'dimension':D,'basis':NAMES,'terms':terms},indent=2)+'\n')
    out={'dimension':D,'nonzero_bracket_terms':len(terms),'jacobi_basis_triples':checks,
         'adapted_jacobi_basis_triples':checks,'adapted_basis':names,'weights':weights.tolist(),
         'max_abs_coefficient':int(abs(C).max()),'max_abs_adapted_coefficient':int(abs(Ca).max()),
         'elapsed_seconds':time.perf_counter()-t0,'status':'Jacobi and skew symmetry passed over the integers'}
    (root/'logs/lie31_intake.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
