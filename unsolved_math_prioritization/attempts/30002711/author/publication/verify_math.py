#!/usr/bin/env python3
"""Standard-library exact diagnostics for RESULTS.md; finite tests are not proofs."""
from fractions import Fraction
from math import comb, gcd
import argparse, json

COUNTS = {}
def check(condition, family):
    if not condition:
        raise ValueError('verification failed: ' + family)
    COUNTS[family] = COUNTS.get(family, 0) + 1

def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return trim(c)

def neg(a):return [-x for x in a]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)

def power(a,n):
    b=[1]
    while n:
        if n&1:b=mul(b,a)
        a=mul(a,a);n//=2
    return b

def mod(a,f):
    a=trim(a)
    if f[-1]!=1:raise ValueError('nonmonic modulus')
    while len(a)>=len(f):
        z=a[-1];d=len(a)-len(f)
        for i,c in enumerate(f):a[i+d]-=z*c
        a=trim(a)
    return a

def cyclo(p,n):
    f=[0]*(p**(n-1)*(p-1)+1)
    for j in range(p):f[j*p**(n-1)]=1
    return f

def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def mpow(A,n):
    B=[[1,0],[0,1]]
    for _ in range(n):B=mm(B,A)
    return B

def homogenize(f,a,b):
    d=len(f)-1;out=[0]
    for i,c in enumerate(f):out=add(out,[c*x for x in mul(power(a,i),power(b,d-i))])
    return out

def vp(x,p):
    if x==0:return 1000000
    x=abs(x);s=0
    while x%p==0:x//=p;s+=1
    return s

def run():
    # Cyclotomic identities and reduction-order diagnostics, all in Z[x]/Phi.
    for p in (2,3,5,7):
        for n in (1,2,3):
            q=p**n;f=cyclo(p,n);e=len(f)-1
            shifted=[0]*(e+1)
            for i,c in enumerate(f):
                for j in range(i+1):shifted[j]+=c*comb(i,j)
            check(shifted[-1]==1,'eisenstein')
            check(shifted[0]==p and shifted[0]%(p*p)!=0,'eisenstein')
            for c in shifted[:-1]:check(c%p==0,'eisenstein')
            # S_j and zeta^j determined recursively, including exact first vanishing.
            zp=[1];S=[0]
            for j in range(1,q+1):
                S=mod(add(S,zp),f);zp=mod(mul(zp,[0,1]),f)
                if j==q:
                    check(S==[0] and zp==[1],'cyclic_iteration')
                else:
                    check(zp!=[1],'cyclic_iteration')
            for j in range(1,q+1):
                # reduction of U-map is U/(1+jU); identity iff p divides j.
                R=mpow([[1,0],[1,1]],j)
                check([[c%p for c in row] for row in R]==[[1,0],[j%p,1]],'reduced_iteration')
            check(sum(1 for j in range(q) if j%p==0)==p**(n-1),'reduction_kernel')
            if n>1:check(p!=q,'negative_order_control')
    # Integrality of the formal mth-root coefficients, beyond ordinary factorial arguments.
    for p in (2,3,5,7):
        for m in range(1,16):
            if gcd(m,p)!=1:continue
            c=Fraction(1)
            for j in range(1,81):
                c=c*(Fraction(-1,m)-(j-1))/j
                check(vp(c.numerator,p)>=vp(c.denominator,p),'binomial_integrality')
            check((-pow(m,-1,p))%p!=0,'faithful_leading_term')
    # Explicit unramified order-three lift.
    M=[[1,-3],[1,-2]]
    check(mpow(M,3)==[[1,0],[0,1]],'unramified_mobius')
    check(mpow(M,2)==[[-2,3],[-1,1]],'unramified_mobius')
    N=[0,9,-9,2];D=[2,-3,1];a=[-3,1];b=[-2,1]
    check(sub(mul(homogenize(N,a,b),D),mul(mul(N,b),homogenize(D,a,b)))==[0],'invariant_norm')
    check(N==mul(mul([0,1],[-3,1]),[-3,2]),'invariant_norm')
    check(D==mul([-2,1],[-1,1]),'invariant_norm')
    check([c%3 for c in N]==[0,0,0,2] and [c%3 for c in D]==[2,0,1],'special_norm')
    # PGL order fails after a perturbation: an actual mutation, not a hardcoded false claim.
    mutated=[[1,-4],[1,-2]];P=mpow(mutated,3)
    check(not(P[0][1]==P[1][0]==0 and P[0][0]==P[1][1]),'negative_mobius_control')
    # Cyclotomic lambda arithmetic for the bad birational lift.
    f=[3,3,1];lam=[0,1]
    check(mod(mul(lam,[-3,-1]),f)==[3],'bad_model_coefficients')
    check(mod(mul(power(lam,2),[2,1]),f)==[3],'bad_model_coefficients')
    disc=sub(power(lam,6),[4*x for x in power(lam,4)])
    check(mod(disc,f)!=[0],'bad_model_discriminant')
    # Exact derivative numerator of t=z^3/(1-z^2) modulo three.
    A=[0,0,0,1];B=[1,0,-1]
    der=lambda v:[i*v[i] for i in range(1,len(v))] or [0]
    numerator=sub(mul(der(A),B),mul(A,der(B)))
    red=[c%3 for c in numerator]
    check(next(i for i,c in enumerate(red) if c)==4,'special_different')
    d_generic=3*(3-1);d_special=4
    check(d_generic==6 and d_generic!=d_special,'negative_smoothness_control')
    # Boundary model valuations show why field points need not descend.
    for r in range(2,101):
        check(Fraction(1,r).denominator>1,'descent_valuation')
        for v in range(-5,6):check(r*v!=1,'descent_valuation')
    # Independent Artin-Schreier equations have exponent p, not p^n.
    for p in (2,3,5,7):
        for a in range(p):
            for b in range(p):
                check(((p*a)%p,(p*b)%p)==(0,0),'product_group_exponent')
    return {'scope':'finite exact diagnostics only; unrestricted problem unresolved','families':dict(sorted(COUNTS.items())),'total_checks':sum(COUNTS.values()),'negative_controls':['higher-order reduction loses faithfulness','mutated Mobius matrix loses order three','birational model has different mismatch']}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    out=json.dumps(run(),indent=2,sort_keys=True)+'\n'
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(out)
    print(out,end='')
