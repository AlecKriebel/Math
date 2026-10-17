#!/usr/bin/env python3
"""Independent exact PASS4 identities; no asymptotic conclusion."""
from fractions import Fraction
from itertools import combinations
from math import isqrt, comb
import json

def require(cond,msg):
    if not cond: raise RuntimeError(msg)

def convolution(A,T,p):
    f=[0]*p
    for a in A:
        for t in T: f[(a+t)%p]+=1
    return f

def covered_mask(A,T,p):
    out=0
    for a in A:
        for t in T: out|=1<<((a+t)%p)
    return out

def all_profiles(p,A):
    best=[p]*(p+1)
    scores=[]
    for m in range(p+1):
        for T in combinations(range(p),m):
            holes=p-covered_mask(A,T,p).bit_count()
            best[m]=min(best[m],holes)
            scores.append((T,holes))
    for m in range(1,p+1): best[m]=min(best[m],best[m-1])
    return best,scores

profile_count=pair_checks=iterated_checks=markov_checks=0
unique_difference_counts=0
score_sign_checks=0
by_prime={}; profile_records={}
for p in (5,7,11):
    k=isqrt(p); profiles=[]
    for A in combinations(range(p),k):
        R,_=all_profiles(p,A); profiles.append(R); profile_count+=1
        for m in range(p+1):
            for n in range(p-m+1):
                require(R[m+n] <= (R[m]*R[n])//p, ('two_budget',p,A,m,n))
                pair_checks+=1
            for r in range(1,5):
                if r*m<=p:
                    require(R[r*m] <= R[m]**r//p**(r-1), ('iterated',p,A,m,r))
                    tau=next(j for j,x in enumerate(R) if x==0)
                    require(tau<=r*m+R[m]**r//p**(r-1), ('repair',p,A,m,r))
                    iterated_checks+=1
        profile_records[(p,A)]=R
    for c in range(p+1):
        fail=sum(R[c]>0 for R in profiles)
        for m in range(c+1):
            mu_num=sum(R[m] for R in profiles)
            for r in range(1,5):
                if r*m<=c:
                    b=c-r*m
                    require(fail**r*(b+1)*p**(r-1)<=mu_num**r, ('Markov_bridge',p,c,m,r))
                    markov_checks+=1
    for d in range(1,p):
        observed=0
        for A in combinations(range(p),k):
            observed += sum((a+d)%p in A for a in A)==1
        expected=p*comb(p-k-1,k-2)
        require(observed==expected,('single_edge_count',p,d))
        unique_difference_counts+=1
    by_prime[p]={'k':k,'A_count':len(profiles)}

# Explicit collective construction, independently computing all holes and shifts.
p=19; A=(0,1,2,5); T=(0,6,12)
H=set(range(p))-set(x for x in range(p) if covered_mask(A,T,p)>>x&1)
require(H=={3,4,9,10,15,16,18},'explicit_initial_holes')
require(min(p-covered_mask(A,V,p).bit_count() for V in combinations(range(p),3))==7,'explicit_R3')
overlap=[len(H&{(x+d)%p for x in H}) for d in range(p)]
require(sum(overlap)==len(H)**2 and min(overlap)==1 and overlap[2]==1,'translation_average')
TT=set(T)|{(t+2)%p for t in T}
HH=set(range(p))-set(x for x in range(p) if covered_mask(A,TT,p)>>x&1)
require(HH=={18},'explicit_amplified_holes')
repaired=TT|{18}
require(len(repaired)==7 and covered_mask(A,repaired,p).bit_count()==p,'explicit_repair')

# Finite optimized-coverage submodularity counterexample.
p=7; AA=(0,1)
def maxcover(A): return max(covered_mask(A,T,p).bit_count() for T in combinations(range(p),2))
vals=[maxcover(V) for V in (AA,(0,1,3),(0,1,5),(0,1,3,5))]
require(vals==[4,5,5,7] and vals[1]+vals[2]<vals[0]+vals[3], 'submodularity_counterexample')

# Bounded one-sided score and exact minimum comparisons on all small A,T.
pointwise=score_min_checks=score_swap_checks=0
qs=(Fraction(1,2),Fraction(1,10),Fraction(1,100))
for q in qs:
    def g(n):return (1-n)*q**n
    for n in range(51):
        require((1 if n==0 else 0)-q*q <=g(n)<= (1 if n==0 else 0),'score_minorant')
        require(-1<=g(n+1)-g(n)<=q*q,'increment_range')
        pointwise+=1
for p in (5,7):
    k=isqrt(p); As=list(combinations(range(p),k)); allmin={}
    for q in qs:
        for A in As:
            R=profile_records[(p,A)]; minima=[Fraction(p)]*(p+1)
            for m in range(p+1):
                for T in combinations(range(p),m):
                    f=convolution(A,T,p)
                    value=sum((1-v)*q**v for v in f)
                    U=sum(v==0 for v in f)
                    require(U-q*q*p<=value<=U, ('fixed_score',p,A,T,q))
                    minima[m]=min(minima[m],value)
                if m: minima[m]=min(minima[m],minima[m-1])
                require(R[m]-q*q*p<=minima[m]<=R[m],('minimum_score',p,A,m,q))
                score_min_checks+=1
                if q*q*p<1:
                    require((R[m]==0)==(minima[m]<=0),('exact_score_sign',p,A,m,q))
                    score_sign_checks+=1
            allmin[(q,A)]=minima
        for i,A in enumerate(As):
            for B in As[i+1:]:
                if len(set(A)&set(B))!=k-1:continue
                for m in range(p+1):
                    require(abs(allmin[(q,A)][m]-allmin[(q,B)][m])<=m*(1+q*q),('score_swap',p,A,B,m,q))
                    score_swap_checks+=1
result={'status':'PASS','probability_model':'Uniform floor(sqrt(p))-sets at each listed small prime; deterministic tests on all candidates.',
 'profile_sets':profile_count,'two_budget_amplification_checks':pair_checks,
 'iterated_amplification_and_repair_checks':iterated_checks,'exact_Markov_bridge_checks':markov_checks,
 'prime_counts':by_prime,'explicit_p19_amplification':{'A':[0,1,2,5],'T':[0,6,12],'holes_before':7,'shift':2,'holes_after':1,'repaired_budget':7},
 'non_submodular_coverage_values':vals,'score_pointwise_cases':pointwise,
 'unique_difference_cycle_counts':unique_difference_counts,'exact_small_q_sign_checks':score_sign_checks,
 'optimized_score_comparisons':score_min_checks,'optimized_score_swap_checks':score_swap_checks,
 'scope':'Exact finite identities and counterexample only; no unproved mean estimate or asymptotic covering conclusion.'}
print(json.dumps(result,indent=2,sort_keys=True))
