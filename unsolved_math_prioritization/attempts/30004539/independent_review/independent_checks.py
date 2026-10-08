#!/usr/bin/env python3
"""Independent finite controls from the normalized Gaussian eigenfunction.

No nested-simplex coefficients or negative-eigenvalue-power recurrence is used.
All arithmetic is rational, with z=(2*pi)^(-1/2) formal until z^2=q/2.
These checks certify finite algebra, not a persistence-series radius.
"""
from fractions import Fraction as F
from math import factorial, comb, prod
from pathlib import Path
from hashlib import sha256
import json

ROOT=Path(__file__).resolve().parent
checks=0
def ck(v):
    global checks
    assert v
    checks+=1

# Polynomials in (x,z), stored by exponent pairs.
def add(a,b):
    r=a.copy()
    for k,v in b.items(): r[k]=r.get(k,F(0))+v
    return {k:v for k,v in r.items() if v}
def scale(a,s): return {k:v*s for k,v in a.items() if v*s}
def mul(a,b):
    r={}
    for (x,z),v in a.items():
        for (y,w),u in b.items():
            k=(x+y,z+w);r[k]=r.get(k,F(0))+v*u
    return {k:v for k,v in r.items() if v}
def V(j,p):
    # Coefficient rho^j of integral_{-rho*x}^0 p(s) z exp(-s^2/2) ds.
    out={}
    for (d,e),v in p.items():
        if j-1-d>=0 and (j-1-d)%2==0:
            a=(j-1-d)//2
            k=(j,e+1)
            out[k]=out.get(k,F(0))+v*F((-1)**(j+1+a),j*2**a*factorial(a))
    return {k:v for k,v in out.items() if v}
def half_moment(p):
    out={}
    for (d,e),v in p.items():
        if d%2:
            a=(d-1)//2; k=(0,e+1); c=F(2**a*factorial(a))
        else:
            a=d//2;k=(0,e); c=F(prod(range(1,2*a,2)),2)
        out[k]=out.get(k,F(0))+v*c
    return {k:v for k,v in out.items() if v}

N=30
G=[{(0,0):F(1)}]
L=[{(0,0):F(1,2)}]
for n in range(1,N+1):
    rhs={}
    for j in range(1,n+1): rhs=add(rhs,V(j,G[n-j]))
    for i in range(1,n): rhs=add(rhs,scale(mul(L[i],G[n-i]),-1))
    G.append(scale(rhs,2)); L.append(half_moment(G[n]))
    ck(all(d>0 for d,e in G[n]))
    # Verify the un-divided eigenfunction identity at this Taylor order.
    lhs={};rhs={}
    for i in range(n): lhs=add(lhs,mul(L[i],G[n-i]))
    for j in range(1,n+1):rhs=add(rhs,V(j,G[n-j]))
    ck(lhs==rhs)

P=[]
for n,l in enumerate(L):
    p={}
    for (d,e),v in l.items():
        ck(d==0 and e%2==0)
        j=e//2;p[j]=v/F(2**j)
        ck(j<=n and (n-j)%2==0)
    P.append(p)

submitted=json.loads((ROOT/'author_replay/verification.json').read_text())
for n in range(25):
    ck(P[n]=={int(j):F(v) for j,v in submitted['coefficients'][str(n)].items()})
for n in range(1,N+1):
    an=F((-1)**(n-1)*2**(n-1)*comb(2*n-2,n-1),n)
    ck(P[n][n]==an)
    if n>=3:
        m=n-2;am=F((-1)**(m-1)*2**(m-1)*comb(2*m-2,m-1),m)
        ck(P[n][n-2]==-F(8*m-3,6)*am)

# Longer univariate controls using the quadratic equation, independently of G.
M=160
lam=[F(1,2)]+[F((-1)**(n-1)*2**(n-1)*comb(2*n-2,n-1),n) for n in range(1,M+1)]
b=[F(0)]+[-F(8*n-3,6)*lam[n] for n in range(1,M+1)]
for n in range(M+1):
    conv=sum(lam[i]*lam[n-i] for i in range(n+1))
    ck(2*conv-lam[n]==(1 if n==1 else 0))
    # Eq (9) multiplied by Lambda^2: B*(Lambda^2+X/2)=-X*Lambda/6-X/8.
    lhs=sum(b[i]*sum(lam[j]*lam[n-i-j] for j in range(n-i+1)) for i in range(n+1))
    if n: lhs+=b[n-1]/2
    rhs=-lam[n-1]/6 if n else F(0)
    if n==1: rhs-=F(1,8)
    ck(lhs==rhs)

# Orientation and Gaussian half-moments, checked independently by recurrences.
for k in range(1,81):
    ck(prod((-1)**(i+1) for i in range(1,k+1))==(-1)**(k*(k-1)//2))
    delta=k*(k+1)//2-(k+1)//2
    ck(delta>=0 and delta%2==0)
    ck(delta==0 if k==1 else delta==2 if k==2 else delta>=4)
for a in range(0,60):
    # Integration by parts: E_+[x^(m+2)]=(m+1)E_+[x^m].
    ck(half_moment({(2*a+2,0):F(1)})==scale(half_moment({(2*a,0):F(1)}),2*a+1))
    ck(half_moment({(2*a+3,0):F(1)})==scale(half_moment({(2*a+1,0):F(1)}),2*a+2))

receipt={
 'verdict':'PASS', 'assertions':checks,
 'independent_eigenfunction_order':N, 'author_full_coefficients_compared':25,
 'quadratic_diagonal_control_order':M,
 'artifact_sha256':sha256((ROOT/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),
 'scope':'Finite exact eigenfunction, grading, moment and diagonal controls; no radius conclusion',
 'coefficients_25_to_30':{str(n):{str(j):str(v) for j,v in sorted(P[n].items())} for n in range(25,N+1)}
}
(ROOT/'independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='coefficients_25_to_30'},indent=2))
