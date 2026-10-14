#!/usr/bin/env python3
"""Independent exact checks of final-pass identities. No asymptotic inference."""
from fractions import Fraction as F
from itertools import combinations, product, permutations
from math import comb, factorial, isqrt, prod
from collections import Counter
import json

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def subs(n,m):return list(combinations(range(n),m))
def conv(A,T,p):return tuple(sum((x-a)%p in T for a in A) for x in range(p))
def rat(q):return [q.numerator,q.denominator]

def residuals():
    swaps=thresholds=0;cases=[]
    for p in (3,5,7,11):
        k=isqrt(p);data={}
        for A in subs(p,k):
            R=[p]*(p+1)
            for m in range(p+1):
                R[m]=min(sum(n==0 for n in conv(A,T,p)) for T in subs(p,m))
            data[A]=R
            for m in range(1,p+1):
                need(R[m]<=R[m-1],'residual padding')
                for r in range(1,5):
                    for c in range(r*m,p+1):
                        if R[c]>0:need(R[m]**r>=(c-r*m+1)*p**(r-1),'integer failure threshold')
                        thresholds+=1
        for A,R in data.items():
            for a in A:
                for b in set(range(p))-set(A):
                    B=tuple(sorted((set(A)-{a})|{b}))
                    if A>=B:continue
                    for m in range(p+1):
                        need(abs(R[m]-data[B][m])<=m,'optimum m-Lipschitz');swaps+=1
        cases.append({'p':p,'k':k,'sets':len(data)})
    return {'cases':cases,'swap_comparisons':swaps,'integer_thresholds':thresholds}

def cylinders():
    identities=lower=upper=lift=0;extremizers=0
    for n in range(2,9):
        U=set(range(n))
        for k in range(1,n):
            N=set(range(k))
            for m in range(k,n+1):
                ss=[set(s) for s in subs(n,m)]
                rmax=min(k,m,n-m,n-1)
                for r in range(rmax+1):
                    observed=[]
                    for s in range(r+1):
                        for pinned in combinations(range(n),s):
                            for bits in product((0,1),repeat=s):
                                P={v for v,b in zip(pinned,bits) if b};Q=set(pinned)-P
                                accepted=[S for S in ss if P<=S and not Q&S]
                                need(bool(accepted),'positive cylinder')
                                a,b,u,v=len(P),len(Q),len(P&N),len(Q&N)
                                actual=F(sum(len(S&N) for S in accepted),len(accepted))
                                formula=u+F((m-a)*(k-u-v),n-s)
                                need(actual==formula,'conditional finite-population mean');identities+=1
                                lo=F(m*(k-r),n-r)
                                need(actual>=lo,'conditional lower envelope');lower+=1
                                if n>=m+k:
                                    hi=r+F((m-r)*(k-r),n-r)
                                    need(actual<=hi,'conditional upper envelope');upper+=1
                                if (m-1)*r<=m*k-n:
                                    need(actual>=1,'lifted cover feasibility');lift+=1
                                observed.append(actual)
                    need(min(observed)==F(m*(k-r),n-r),'sharp lower extremizer');extremizers+=1
                    if n>=m+k:
                        need(max(observed)==r+F((m-r)*(k-r),n-r),'sharp upper extremizer');extremizers+=1
    return {'conditional_mean_identities':identities,'lower_bounds':lower,'upper_bounds':upper,'lifted_cover_checks':lift,'sharp_extremizers':extremizers}

def flux():
    rows=[];swaps=0
    for p in (5,7):
        k=isqrt(p);As=subs(p,k);K=k*(p-k)
        for m in range(1,p):
            Ts=subs(p,m);f={(A,T):conv(A,T,p) for A in As for T in Ts}
            for q in (F(1,2),F(1,200)):
                H={(A,T):sum(q**n for n in f[A,T])/p for A in As for T in Ts}
                G={(A,T):sum((1-n)*q**n for n in f[A,T])/p for A in As for T in Ts}
                for kind in ('fixed','pgf_min','score_min'):
                    sel={A:(Ts[0] if kind=='fixed' else min(Ts,key=lambda T:((H if kind=='pgf_min' else G)[A,T],T))) for A in As}
                    FF=sum(H[A,sel[A]] for A in As)/len(As)
                    MM=sum(sum(n*q**n for n in f[A,sel[A]]) for A in As)/(p*len(As))
                    MM2=sum(sum(n*n*q**n for n in f[A,sel[A]]) for A in As)/(p*len(As))
                    D=F(0)
                    for A in As:
                        for a in A:
                            for b in set(range(p))-set(A):
                                B=tuple(sorted(set(A)-{a}|{b}))
                                D+=H[B,sel[B]]-H[B,sel[A]];swaps+=1
                    D/=len(As)*K;lam=F(k*m,p)
                    need((1-q)*MM2+(p-(1-q)*(k+m))*MM-q*k*m*FF == -q*K*D/(1-q),'flux identity')
                    need(FF-MM==(1-lam*q)*FF-(1-q)*((k+m)*MM-MM2)/p+q*K*D/((1-q)*p),'score flux identity')
                    need(MM<=lam*FF,'covariance')
                    need(-(1-q)/k<=D<=(1-q)*m/(p-k),'coarse flux bounds')
                    alpha=1-lam*q-lam*(1-q)*(k+m)/p
                    if alpha>=0:
                        # Avoid irrational q^lambda: exact preceding inequality uses F.
                        need(FF-MM>=alpha*FF+q*K*D/((1-q)*p),'pre-Jensen score bound')
                    if kind=='fixed':need(D==0,'fixed flux zero')
                    if kind=='pgf_min':need(D<=0,'PGF minimizer flux')
                    rows.append({'p':p,'k':k,'m':m,'q':rat(q),'selector':kind,'D':rat(D)})
    example=next(r for r in rows if r['p']==5 and r['m']==3 and r['q']==[1,2] and r['selector']=='score_min')
    need(example['D']==[-1,30],'strict negative example')
    return {'selector_cases':len(rows),'direct_swaps':swaps,'negative_score_example':example}

def rank(rows,p):
    a=[list(r) for r in rows];h=0
    for j in range(len(a[0]) if a else 0):
        ix=next((i for i in range(h,len(a)) if a[i][j]%p),None)
        if ix is None:continue
        a[h],a[ix]=a[ix],a[h];z=pow(a[h][j]%p,-1,p);a[h]=[(v*z)%p for v in a[h]]
        for i in range(len(a)):
            if i!=h:
                z=a[i][j];a[i]=[(x-z*y)%p for x,y in zip(a[i],a[h])]
        h+=1
    return h

def graphs():
    result=[];assignments=labels=0
    for p,k,t in ((3,2,2),(5,2,3)):
        edges=list(product(range(k),range(t)));v=k+t
        for J in combinations(edges,p):
            B=[[int(u==i or u==k+j) for u in range(v)] for i,j in J];r=rank(B,p)
            N=0
            for ell in permutations(range(p)):
                # Augmented matrix elimination rather than a forest traversal.
                N+=rank([row+[e] for row,e in zip(B,ell)],p)==r;labels+=1
            unrestricted=distinct=0
            for z in product(range(p),repeat=v):
                assignments+=1
                if len({(z[i]+z[k+j])%p for i,j in J})==p:
                    unrestricted+=1
                    distinct+=len(set(z[:k]))==k and len(set(z[k:]))==t
            need(unrestricted==p**(v-r)*N,'cycle-consistent labeling count')
            need(N==0 or N%(p*(p-1))==0,'affine label divisibility')
            need(distinct==0 or distinct%(p*p*(p-1))==0,'coordinate affine divisibility')
            result.append({'p':p,'k':k,'t':t,'rank':r,'N':N,'all_assignments':unrestricted,'distinct_assignments':distinct})
    return {'graphs':len(result),'vertex_assignments':assignments,'permutation_labelings':labels,'cases':result}

def run():return {'status':'PASS','scope':'Exact finite identity checks only; no proof of the asymptotic target.','residuals':residuals(),'cylinders':cylinders(),'flux':flux(),'graphs':graphs()}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
