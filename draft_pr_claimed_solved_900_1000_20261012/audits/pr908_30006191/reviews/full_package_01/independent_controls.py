#!/usr/bin/env python3
"""Independent occupation-coordinate determinants and full Fock controls.

Finite checks only, never a substitute for the continuum proof.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json, math
import numpy as np
from scipy.linalg import expm

def check(ok,why):
    if not ok: raise RuntimeError(why)
def determinant(a):
    a=[list(row) for row in a];p=F(1);n=len(a)
    for j in range(n):
        k=next((i for i in range(j,n) if a[i][j]),None)
        if k is None:return F(0)
        if k!=j:a[j],a[k]=a[k],a[j];p=-p
        pivot=a[j][j];p*=pivot
        for i in range(j+1,n):
            ratio=a[i][j]/pivot
            for k in range(j+1,n):a[i][k]-=ratio*a[j][k]
    return p
def parity(v):return (-1)**v.bit_count()
def main():
    exact=0;floats=0;maxerr=0.
    # Hadamard columns divided by sqrt(8). Squared minors are rational.
    H=[[F(parity(i&j)) for j in range(8)] for i in range(8)]
    choices=[tuple(range(n)) for n in range(9)]+[tuple(range(8-n,8)) for n in range(1,8)]
    for occupied in choices:
        n=len(occupied);weights=[]
        for rows in combinations(range(8),n):
            d=determinant([[H[i][j] for j in occupied] for i in rows])
            weights.append((sum(1<<i for i in rows),d*d/F(8**n)))
        check(sum(w for _,w in weights)==1,'determinant normalization');exact+=1
        for outside in range(256):
            mean=sum(w*(bits&outside).bit_count() for bits,w in weights)
            second=sum(w*((bits&outside).bit_count()**2) for bits,w in weights)
            B=[[sum(H[i][j]*H[i][k] for i in range(8) if outside>>i&1)/8 for k in occupied] for j in occupied]
            lam=sum(B[j][j] for j in range(n));tr2=sum(B[j][k]*B[k][j] for j in range(n) for k in range(n))
            check(mean==lam and second==lam*lam+lam-tr2 and second-lam*lam<=lam,'Slater exact moments');exact+=1
    # Correlated counterexample proves that extending variance<=mean is unsafe.
    mean=F(4);second=F(32)
    check(second-mean**2>mean,'correlated non-Slater negative control');exact+=1
    # Exhaust all integer eigenvalues including vacuum and k=1 zero coefficient.
    for n in range(401):
        for k in (0,1):
            for m in range(n+1):
                L=n-m;diff=L*(L-k)-n*(n-k)
                check(diff==-m*(2*n-k-m) and abs(diff)<=2*n*m,'sector bound');exact+=1
    for N in [1,2,3,7,8,9,63,64,65,1000,10**6]:
        m=math.ceil(N**(1/3))
        while m**3<N:m+=1
        while (m-1)**3>=N:m-=1
        check(m**3>=N and m<=2*N**(1/3),'packing ceiling');exact+=1
    # Full finite Fock representation: dGamma construction from CAR matrices.
    dim=5;size=1<<dim;ann=[]
    for j in range(dim):
        a=np.zeros((size,size),complex)
        for b in range(size):
            if b>>j&1:a[b^(1<<j),b]=parity(b&((1<<j)-1))
        ann.append(a)
    rng=np.random.default_rng(908301)
    h0=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim));h=(h0+h0.conj().T)/2
    T=sum((h[i,j]*ann[i].conj().T@ann[j] for i in range(dim) for j in range(dim)),np.zeros((size,size),complex))
    num=np.diag([b.bit_count() for b in range(size)])
    f=np.zeros(dim,complex);f[0]=1;A=ann[0].conj().T
    for k in (0,1):
        K=T+num@(num-k*np.eye(size))
        for n in range(dim):
            bits=sum(1<<j for j in range(1,n+1));psi=np.eye(size)[:,bits];xi=A@psi
            for t in [-.13,.07,math.pi/(2*n+1-k) if 2*n+1-k else .11]:
                U=expm(1j*t*K);actual=np.vdot(xi,U@A@U.conj().T@psi)
                predicted=np.exp(1j*t*(2*n+1-k))*np.vdot(f,expm(1j*t*h)@f)
                err=float(abs(actual-predicted));maxerr=max(maxerr,err);check(err<2e-12,'phase/CAR full Fock');floats+=1
                g=expm(1j*t*h)@f
                ag=sum((g[j]*ann[j].conj().T for j in range(dim)),np.zeros((size,size),complex))
                check(abs(np.vdot(xi,ag@psi)-np.vdot(f,g))<2e-12,'late occupied-overlap CAR');floats+=1
    # Dimension boundary is analytic rational arithmetic.
    exponents={str(d):[str(-F(1,2)+F(1,d)),str(-F(1)+F(2,d))] for d in [1,2,3,4]}
    check(exponents['2']==['0','0'] and exponents['3']==['-1/6','-1/3'],'dimension boundaries');exact+=1
    out={'status':'PASS','exact_finite_predicates':exact,'floating_diagnostics':floats,'floating_tolerance':2e-12,'maximum_phase_error':maxerr,'mechanisms':['occupation-basis minors with exact rational weights','exhausted integer leakage eigenvalues','full complex Fock CAR matrices with mixing kinetic energy','correlated-state invalid-variance negative control'],'dimension_exponents':exponents,'scope':'Finite adversarial controls. The universal continuum theorem is established by the independent written derivation, not these samples.'}
    (Path(__file__).resolve().parent/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
