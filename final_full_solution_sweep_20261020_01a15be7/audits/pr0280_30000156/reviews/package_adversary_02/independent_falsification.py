#!/usr/bin/env python3
"""Fresh direct graph/iteration checks, independent of packaged order reduction."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from math import gcd, isqrt
import cmath, json, time

def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p)+1))

def order_by_iteration(a,p):
    t=a%p
    for k in range(1,p):
        if t==1: return k
        t=t*a%p
    raise ValueError((a,p))

def trim(v):
    while len(v)>1 and v[-1]==0:v.pop()
    return v

def division(a,b):
    a=trim(list(a));b=trim(list(b));q=[0]*max(1,(len(a)-len(b)+1))
    while len(a)>=len(b) and a!=[0]:
        k=len(a)-len(b)
        if a[-1]%b[-1]:raise ValueError('Nonintegral polynomial division')
        c=a[-1]//b[-1];q[k]=c
        for j in range(len(b)):a[k+j]-=c*b[j]
        trim(a)
    return trim(q),trim(a)

_cyclotomic={}
def cyclotomic(n):
    if n not in _cyclotomic:
        p=[-1]+[0]*(n-1)+[1]
        for d in range(1,n):
            if n%d==0:
                p,r=division(p,cyclotomic(d))
                if r!=[0]:raise ValueError('Inexact cyclotomic recursion')
        _cyclotomic[n]=p
    return _cyclotomic[n]

def main():
    start=time.time(); counts=Counter(); rows=[]; character_max_error=0.0
    def need(v,label):
        counts[label]+=1
        if not v: raise RuntimeError(label)
    for p in (v for v in range(3,2001) if v%4==3 and prime(v)):
        n=p-1; orders=[order_by_iteration((u*u+1)%p,p) for u in range(p)]
        phi=sum(gcd(k,n)==1 for k in range(1,n+1)); theta=F(phi,n)
        q=n; factors=[]
        for d in range(2,n+1):
            if q%d==0:
                factors.append(d)
                while q%d==0:q//=d
        primitive=orders.count(n)
        need((F(primitive,p)-theta)**2*p<=theta**2*(2**len(factors)-1)**2,'primitive_bound_exact_squared')
        need((2**len(factors))**4<=64**4*n,'crude_omega_bound')
        # Compare direct graph cycle decomposition, including every affine point.
        if p<=59:
            successor={u*p+v:u*p+((u*u+1)*v%p) for u in range(p) for v in range(p)}
            need(len(set(successor.values()))==p*p,'full_graph_permutation')
            unseen=set(successor); periods={}
            while unseen:
                z=min(unseen); path=[]; w=z
                while w not in path:
                    path.append(w); w=successor[w]
                need(w==z,'full_graph_no_transient')
                for w in path: periods[w]=len(path)
                unseen.difference_update(path)
            need(len(periods)==p*p,'full_graph_point_count')
            for z,d in periods.items():
                u,v=divmod(z,p)
                need(d==(orders[u] if v else 1),'graph_vs_iterative_multiplier_order')
            for denominator in range(1,18):
                for numerator in range(0,denominator+1):
                    x=F(numerator,denominator)
                    observed=sum(F(d,p)<=x for d in periods.values())
                    if F(1,2)<=x<1 and p*(1-x)>1:
                        need(observed==p*p-n*primitive,'all_rational_cutoff_inclusions')
                    if x>=F(n,p):need(observed==p*p,'maximal_cutoff_endpoint')
                    if x==0:need(observed==0,'zero_cutoff')
            moment=sum(max(F(0),min(F(1),2*F(d,p)-1)) for d in periods.values())/p**2
            need(moment==F((p-2)*n*primitive,p**3),'continuous_ramp_graph_identity')
        # Character arithmetic diagnostic, never promoted to exact proof.
        if p<=103:
            g=next(a for a in range(1,p) if order_by_iteration(a,p)==n)
            logs={pow(g,k,p):k for k in range(n)}
            eta=lambda a:0 if a%p==0 else (1 if pow(a%p,n//2,p)==1 else -1)
            for k in range(1,n):
                chi=lambda a:0j if a%p==0 else cmath.exp(2j*cmath.pi*k*logs[a%p]/n)
                s=sum(chi(u*u+1) for u in range(p))
                j=sum(eta(t)*chi(1-t) for t in range(p))
                character_max_error=max(character_max_error,abs(s-eta(-1)*j))
                need(abs(s-eta(-1)*j)<1e-9,'jacobi_identity_numerical_diagnostic')
                target=1 if k==n//2 else p
                need(abs(abs(s)**2-target)<1e-8,'jacobi_exception_numerical_diagnostic')
                # Independent standard-library cyclotomic-ring verification.
                sv=[0]*n;jv=[0]*n
                for u in range(p):sv[k*logs[(u*u+1)%p]%n]+=1
                for t in range(p):
                    if (1-t)%p:jv[k*logs[(1-t)%p]%n]+=eta(t)
                need(division([a-eta(-1)*b for a,b in zip(sv,jv)],cyclotomic(n))[1]==[0],
                     'jacobi_identity_exact_cyclotomic_remainder')
                norm=[0]*n
                for a,v in enumerate(sv):
                    for b,w in enumerate(sv):norm[(a-b)%n]+=v*w
                norm[0]-=target
                need(division(norm,cyclotomic(n))[1]==[0],'jacobi_exception_exact_cyclotomic_remainder')
            for k in range(n):
                val=F(1)
                for ell in factors:
                    val*=F(0) if k%ell==0 else F(ell,ell-1)
                need(theta*val==int(gcd(k,n)==1),'primitive_indicator_exact_factorization')
        rows.append({'p':p,'primitive':primitive,'theta':str(theta)})
    for p in [2,5,13,17,29,37,41,53]:
        images={(u,(u*u+1)*v%p) for u in range(p) for v in range(p)}
        need(len(images)<p*p,'nonadmissible_collision_control')
    return {'status':'PASS','exact_and_numeric_diagnostics_separated':True,'prime_bound':2000,
            'admissible_primes':len(rows),'counts':dict(counts),'checks_total':sum(counts.values()),
            'exact_checks':sum(v for k,v in counts.items() if 'numerical' not in k),
            'numerical_diagnostics':sum(v for k,v in counts.items() if 'numerical' in k),
            'character_max_error':character_max_error,'elapsed_seconds':time.time()-start,
            'scope':'Finite falsification only; infinite conclusions require proofs and cited classical inputs.',
            'rows':rows}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
