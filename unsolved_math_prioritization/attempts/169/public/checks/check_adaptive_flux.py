#!/usr/bin/env python3
"""Exact finite checks. No asymptotic claim is tested or inferred."""
from fractions import Fraction as Q
from itertools import combinations
import json

def require(test, message):
    if not test:
        raise RuntimeError(message)

def profile(p, A, T):
    values=[0]*p
    for a in A:
        for t in T:
            values[(a+t)%p]+=1
    return tuple(values)

def check_case(p,k,m,q):
    As=list(combinations(range(p),k))
    Ts=list(combinations(range(p),m))
    hist={}
    for A in As:
        for T in Ts:
            f=profile(p,A,T)
            hist[A,T]=tuple(f.count(n) for n in range(k+1))
    def moments(A,T):
        h=hist[A,T]
        return tuple(sum(Q(h[n])*n**j*q**n for n in range(k+1))/p for j in range(3))
    data={key:moments(*key) for key in hist}
    selectors={
        'fixed':{A:Ts[0] for A in As},
        'minimum_pgf':{A:min(Ts,key=lambda T:(data[A,T][0],T)) for A in As},
        'minimum_score':{A:min(Ts,key=lambda T:(data[A,T][0]-data[A,T][1],T)) for A in As},
    }
    K=k*(p-k)
    lam=Q(k*m,p)
    output=[]
    swaps=0
    for name,sel in selectors.items():
        F,M,M2=(sum(data[A,sel[A]][j] for A in As)/len(As) for j in range(3))
        D=Q(0)
        old=Q(0)
        full=Q(0)
        for A in As:
            SA=set(A)
            for y in A:
                for z in range(p):
                    if z in SA:
                        continue
                    Ap=tuple(sorted((SA-{y})|{z}))
                    newH=data[Ap,sel[Ap]][0]
                    frozenH=data[Ap,sel[A]][0]
                    oldH=data[A,sel[A]][0]
                    D+=newH-frozenH
                    old+=frozenH-oldH
                    full+=newH-oldH
                    if name=='minimum_pgf':
                        require(newH<=frozenH,'PGF optimizer selection sign')
                    if name=='minimum_score':
                        require(data[Ap,sel[Ap]][0]-data[Ap,sel[Ap]][1]
                                <=data[Ap,sel[A]][0]-data[Ap,sel[A]][1],
                                'score optimizer selection sign')
                    swaps+=1
        D/=len(As)*K
        old/=len(As)*K
        full/=len(As)*K
        require(full==0 and old+D==0,'exact adaptive stationarity')
        lhs=(1-q)*M2+(p-(1-q)*(k+m))*M-q*k*m*F
        rhs=-q*K*D/(1-q)
        require(lhs==rhs,'exchange moment identity')
        C=q*K/((1-q)*p)
        correction=(1-q)*((k+m)*M-M2)/p
        require(F-M==(1-lam*q)*F-correction+C*D,'score identity')
        require(M<=lam*F,'decreasing covariance bound')
        require(0<=correction<=lam*(1-q)*(k+m)*F/p,'finite correction bound')
        alpha=1-lam*q-lam*(1-q)*(k+m)/p
        require(F**p>=q**(k*m),'Jensen bound with rational-power elimination')
        require(F-M>=alpha*F+C*D,'one-sided flux bound retaining F')
        if alpha>0:
            remainder=(F-M-C*D)/alpha
            require(remainder>=0 and remainder**p>=q**(k*m),
                    'one-sided flux bound with Jensen')
        elif alpha==0:
            require(F-M>=C*D,'zero-alpha flux bound')
        require(-(1-q)/k<=D<=(1-q)*m/(p-k),'unconditional flux interval')
        if name=='fixed':
            require(D==0,'fixed selector has zero reoptimization flux')
        if name=='minimum_pgf':
            require(D<=0,'PGF minimizer flux nonpositive')
        output.append({'p':p,'k':k,'m':m,'q':str(q),'selector':name,
                       'F':str(F),'M':str(M),'M2':str(M2),'D':str(D),
                       'score_per_site':str(F-M),'alpha':str(alpha),
                       'identity_passed':True,'bounds_passed':True})
    return output,swaps

def check_birth_death():
    checks=0
    p,k,m=7,3,3
    q=Q(1,3)
    K=k*(p-k)
    for A in combinations(range(p),k):
        SA=set(A)
        for T in combinations(range(p),m):
            f=profile(p,A,T)
            for x,n in enumerate(f):
                delta=Q(0)
                up=down=0
                for y in A:
                    for z in range(p):
                        if z in SA:
                            continue
                        Ap=(SA-{y})|{z}
                        np=sum(1 for t in T if (x-t)%p in Ap)
                        up+=np==n+1
                        down+=np==n-1
                        delta+=q**np-q**n
                b=Q((k-n)*(m-n),K)
                d=Q(n*(p-k-m+n),K)
                require(Q(up,K)==b and Q(down,K)==d,'birth/death counts')
                formula=(1-q)/(q*K)*q**n*((1-q)*n*n+(p-(1-q)*(k+m))*n-q*k*m)
                require(delta/K==formula,'pointwise generator formula')
                checks+=1
    return checks

rows=[]
swaps=0
for case in [(5,2,2),(5,2,3),(7,2,3),(7,3,3),(11,3,4)]:
    for q in [Q(1,2),Q(1,3),Q(1,200)]:
        new,n=check_case(*case,q)
        rows+=new
        swaps+=n
witness=next(r for r in rows if r['p']==5 and r['m']==3 and r['q']=='1/2' and r['selector']=='minimum_score')
require(witness['F']=='9/20' and witness['M']=='1/2' and witness['M2']=='3/5'
        and witness['D']=='-1/30' and witness['score_per_site']=='-1/20',
        'published exact negative-flux example')
# Explicit mutation guard: neither deleting nor reversing the flux term passes.
p,k,m=5,2,3
q=Q(1,2)
F,M,M2,D=(Q(witness[key]) for key in ['F','M','M2','D'])
lhs=(1-q)*M2+(p-(1-q)*(k+m))*M-q*k*m*F
require(lhs!=0,'omitted-flux mutation must fail')
require(lhs!=q*k*(p-k)*D/(1-q),'sign-reversed-flux mutation must fail')
print(json.dumps({'status':'passed','selector_cases':len(rows),'direct_swap_checks':swaps,
                  'pointwise_birth_death_checks':check_birth_death(),
                  'negative_flux_guard':witness,'mutation_guards':2,
                  'scope':'Exact finite identities only; no asymptotic flux or residual bound established.',
                  'results':rows},indent=2))
