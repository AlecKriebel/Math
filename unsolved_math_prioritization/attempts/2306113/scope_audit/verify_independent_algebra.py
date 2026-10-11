#!/usr/bin/env python3
"""Independent exact degree-10 algebra audit, without importing candidate code.

Slit coefficients are recovered by a formal fixed-point equation rather than
Catalan numbers or composition with the candidate's inverse-series expansion.
This small audit does not replay the all-circle or adaptive disk certificates.
"""
from fractions import Fraction as R
from pathlib import Path
import hashlib
import json
import sys

D=10
ZERO=(R(0),R(0))
ONE=(R(1),R(0))

def plus(x,y): return (x[0]+y[0],x[1]+y[1])
def times(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def by(x,t): return (x[0]*t,x[1]*t)
def minus(x): return by(x,-1)
def pplus(x,y): return [plus(a,b) for a,b in zip(x,y)]
def pby(x,t): return [by(a,t) for a in x]
def pmul(x,y):
    return [sumc(times(x[k],y[n-k]) for k in range(n+1)) for n in range(D+1)]
def sumc(items):
    out=ZERO
    for item in items: out=plus(out,item)
    return out

def reciprocal(x):
    if x[0]!=ONE: raise ValueError('reciprocal requires constant 1')
    out=[ONE]+[ZERO]*D
    for n in range(1,D+1):
        out[n]=minus(sumc(times(x[k],out[n-k]) for k in range(1,n+1)))
    return out

def square_one_plus(x,u):
    y=[times(a,u) for a in x]; y[0]=plus(y[0],ONE)
    return pmul(y,y)

def K_of(x,u):
    return pmul(x,reciprocal(square_one_plus(x,u)))

def inverse_fixedpoint(W,u):
    # Y = W(1+uY)^2. Since W(0)=0, each update gains one coefficient.
    Y=[ZERO]*(D+1)
    for _ in range(D):
        Y=pmul(W,square_one_plus(Y,u))
    if Y != pmul(W,square_one_plus(Y,u)):
        raise ValueError('formal fixed point did not stabilize')
    if K_of(Y,u)!=W:
        raise ValueError('defining map equation mismatch')
    return Y

def need(b,m):
    if not b: raise ValueError(m)

def main():
    raw=Path(sys.argv[1]).read_bytes(); data=json.loads(raw)
    need(hashlib.sha256(raw).hexdigest()=='65ddace3d1b7718fee4195027432b440c6f7ba0f12e33d899c0d9839df6eafd7','unexpected authored witness bytes')
    q1=R(63,80); q2=R(2,25)
    u1=(-R(1),R(0)); u2=(-R(39951,40049),-R(2800,40049)); u3=(-R(621,629),R(100,629))
    need(all(x*x+y*y==1 for x,y in (u1,u2,u3)),'unit parameter error')
    z=[ZERO,ONE]+[ZERO]*(D-1)
    phi1=inverse_fixedpoint(pby(K_of(z,u1),q1),u1)
    psi=inverse_fixedpoint(pby(K_of(phi1,u2),q2),u2)
    a=pby(K_of(psi,u3),1/(q1*q2))
    need(a[0]==ZERO and a[1]==ONE,'normalization error')
    c=[ZERO,ZERO]+[(R(x),R(y)) for x,y in data['coefficients']]
    r=R(999,1000)
    L=sumc(by(times(c[n],a[n]),r**(n-1)) for n in range(2,D+1))
    expected=R(405060549603285758485667422940782591483247763782798484017289213787330309559159416000967760687419806896501225537,402323453301734918728627923217998774858332677743835558400000000000000000000000000000000000000000000000000000000)
    need(L[0]==expected,'real L differs from theorem')
    need(L[0]>R(2517,2500),'real L too small')
    abs2=L[0]*L[0]+L[1]*L[1]
    invL=(L[0]/abs2,-L[1]/abs2)
    H=[minus(times(x,invL)) for x in c]
    convolution=plus((r,R(0)),sumc(by(times(H[n],a[n]),r**n) for n in range(2,D+1)))
    need(convolution==ZERO,'convolution not exactly zero')
    lip=sum(n*(n-1)*(abs(x)+abs(y)) for n,(x,y) in enumerate(c))
    need(lip==R(6004273,500000),'angular Lipschitz constant mismatch')
    certified=R(500679451,500000000)+lip/8192
    need(certified==R(513446291949,512000000000),'circle-cover arithmetic mismatch')
    need(certified<R(251,250),'circle-cover upper bound too large')
    gamma=R(1000000,1002001)
    need(R(2510,2517)<gamma,'separation comparison failed')
    out={
        'status':'PASS',
        'method':'Independent Gaussian-rational fixed-point and rational-function series; no candidate-code imports and no Catalan formula',
        'degree':D,
        'witness_sha256':hashlib.sha256(raw).hexdigest(),
        'coefficient_sha256':hashlib.sha256(json.dumps([[str(x),str(y)] for x,y in a],separators=(',',':')).encode()).hexdigest(),
        'real_L':str(L[0]),
        'imag_L':str(L[1]),
        'complex_scaling_zero_exact':convolution==ZERO,
        'angular_Lipschitz_upper':str(lip),
        'conditional_circle_upper':str(certified),
        'strict_neighborhood_ratio_upper':'2510/2517',
        'gamma':str(gamma),
        'ratio_separation_margin':str(gamma-R(2510,2517)),
        'limitation':'Circle sample extrema and adaptive disk traversal are independently addressed in the separate reproducibility review, not recomputed by this algebra audit.'
    }
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
