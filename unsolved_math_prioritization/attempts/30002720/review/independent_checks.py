#!/usr/bin/env python3
"""Independent exact interval recursion, affine reward and scale diagnostics."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations,product
from math import comb,isqrt
from pathlib import Path
import hashlib,json
C=Counter();q=F(3,4)
def ck(condition,group):
    assert condition,group
    C[group]+=1

def split(lo,hi,last):
    p=F(1,2) if last is None else (q if last==0 else 1-q)
    return lo+(hi-lo)*p

def cylinder(word):
    lo,hi,last=F(0),F(1),None
    for digit in word:
        mid=split(lo,hi,last)
        if digit==0:hi=mid
        else:lo=mid
        last=digit
    return lo,hi

def reward_eventually_constant(word,tail):
    # Solve the constant-state affine recursion, then compose backwards.
    if not word:return 1+F(1,2)/(1-q)
    value=1+(q if word[-1]==tail else 1-q)/(1-q)
    for i in range(len(word)-2,-1,-1):value=1+(q if word[i]==word[i+1] else 1-q)*value
    return 1+F(1,2)*value

# Build cylinder intervals breadth-first rather than using a probability product.
level=[((),F(0),F(1),None)]
for depth in range(1,10):
    nxt=[]
    for word,lo,hi,last in level:
        mid=split(lo,hi,last)
        nxt.extend([(word+(0,),lo,mid,0),(word+(1,),mid,hi,1)])
    ck(sum((hi-lo for _,lo,hi,_ in nxt),F(0))==1,'partition_mass')
    for a,b in zip(nxt,nxt[1:]):ck(a[2]==b[1],'adjacent_intervals')
    for word,lo,hi,last in nxt:
        ck(hi-lo<=F(1,2)*q**(depth-1),'maximum_cylinder_mass')
        if word[-1]==0:
            left=reward_eventually_constant(word+(0,),1)
            right=reward_eventually_constant(word+(1,),0)
            ck(left-right==hi-lo,'affine_reward_jump')
    level=nxt

# The sparse word and all scale identities use independently built intervals.
rank_lower=F(0);previous_n=0
for j in range(2,29):
    word=tuple(int(r>=4 and isqrt(r)**2==r) for r in range(1,j*j))
    lo,hi=cylinder(word);mass=hi-lo
    formula=F(1,2)*F(1,4)**(2*j-4)*q**(j*j-2*j+2)
    ck(mass==formula,'square_transition_count')
    rank_lower+=q*mass
    rightlo,righthi=cylinder(word+(1,))
    ck(rightlo==rank_lower,'rank_series_partial_sum')
    lo2,hi2=cylinder(word+(1,)+(0,)*(2*j))
    ck(lo2==rank_lower and hi2-lo2==mass*q**(2*j)/12,'next_square_cylinder')
    width=mass*q**j; inv=width**-2;n=(inv.numerator+inv.denominator-1)//inv.denominator
    ck(1<=n*width**2<1+width**2,'subsequence_ceiling')
    ck(n*mass**2>=q**(-2*j),'scaled_jump_diverges')
    ck(n>previous_n,'subsequence_increasing');previous_n=n
    ck(n<=2*16**(j*j+j-1),'polynomial_log_scale')
    K=j//2;L=cylinder(word+(0,)+(1,)*K);R=cylinder(word+(1,)+(0,)*K)
    ck(L[1]==R[0]==rank_lower,'two_sided_window_boundary')
    ck(L[1]-L[0]==mass*q**K/4,'left_window_mass')
    ck(R[1]-R[0]==mass*q**K/12,'right_window_mass')
    if j>=18:ck(width<R[1]-R[0]<=L[1]-L[0],'quantile_window_containment')
    next_mass=F(1,2)*F(1,4)**(2*j-2)*q**(j*j+1)
    # Following-series ratios are bounded by the first following ratio.
    tail_bound=q*next_mass/(1-F(1,16)*q**(2*j+1))
    ck(0<tail_bound<hi2-lo2,'strict_rank_remainder')
    ck(tail_bound/width<q**j/12,'boundary_offset_vs_CLT_scale')

# Exact adaptive source partition of deterministic rational sample positions.
# The selection recursion stops when its chosen bucket is a singleton.
def direct_cost(sample,k):
    lo,hi,last=F(0),F(1),None;current=list(sample);total=0
    while len(current)>1:
        total+=len(current);mid=split(lo,hi,last)
        left=[u for u in current if u<mid]
        if k<len(left):current=left;hi=mid;last=0
        else:k-=len(left);current=[u for u in current if u>=mid];lo=mid;last=1
    return total

def count_cost(sample,target):
    lo,hi,last=F(0),F(1),None;total=0;mean_prefix=F(0);depth=0
    D=max(max(abs(F(i,len(sample))-u),abs(F(i+1,len(sample))-u)) for i,u in enumerate(sample))
    while True:
        count=sum(lo<=u<hi for u in sample)
        ck(abs(count-len(sample)*(hi-lo))<=2*len(sample)*D,'uniform_interval_count')
        if count<=1:break
        total+=count;mean_prefix+=hi-lo;depth+=1
        mid=split(lo,hi,last)
        if target<mid:hi=mid;last=0
        else:lo=mid;last=1
    ck(abs(total-len(sample)*mean_prefix)<=2*len(sample)*depth*D+depth,'truncated_mean_bound')
    return total

# Odd denominator ensures no cylinder endpoint, which always has dyadic denominator.
grid=[F(i,13) for i in range(1,13)]
cases=0
for n in range(2,6):
    for sample in combinations(grid,n):
        for k,target in enumerate(sample):
            cases+=1
            ck(direct_cost(sample,k)==count_cost(sample,target),'singleton_recursion_equals_counts')

# Exact binomial generating-function coefficients: all-success counts determine
# the order-statistic CDF. The triangular CLT itself is analytic, not tested here.
for n in range(1,25):
    for p in (F(1,5),F(1,3),F(1,2),F(4,5)):
        coeff=[F(1)]
        for _ in range(n):
            nxt=[F(0)]*(len(coeff)+1)
            for i,a in enumerate(coeff):nxt[i]+=a*(1-p);nxt[i+1]+=a*p
            coeff=nxt
        ck(sum(coeff,F(0))==1,'binomial_mass')
        ck(sum(i*a for i,a in enumerate(coeff))==n*p,'binomial_mean')
        ck(sum((i-n*p)**2*a for i,a in enumerate(coeff))==n*p*(1-p),'binomial_variance')
        for i,a in enumerate(coeff):ck(a==comb(n,i)*p**i*(1-p)**(n-i),'binomial_coefficients')

result={'status':'PASS','assertions':sum(C.values()),'categories':dict(C),'adaptive_selection_cases':cases,'artifact_sha256':hashlib.sha256(Path(__file__).with_name('author_replay').joinpath('COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'limits':'Exact finite controls only. Non-tightness follows from the written uniform estimate, quantile CLT and two separated cost bands, not from a finite numerical experiment.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
