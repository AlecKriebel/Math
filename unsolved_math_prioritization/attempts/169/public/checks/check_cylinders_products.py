#!/usr/bin/env python3
"""Independent exact cylinder relaxation and logarithmic product checks."""
from fractions import Fraction as F
from itertools import combinations
from math import comb,prod,isqrt
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise ValueError(msg)
def rat(x):
    x=F(x);return [x.numerator,x.denominator]
def convolution(A,T,p):
    f=[0]*p
    for a in A:
        for t in T:f[(a+t)%p]+=1
    return f

def cylinder_checks():
    direct=algebra=extrema=lightness=feasible_checks=0
    # Permutation symmetry lets every cylinder be represented by (a,b,u,v).
    # Each representative is also independently conditioned by enumerating S.
    for n in range(2,10):
        for k in range(1,n+1):
            N=set(range(k))
            for m in range(k,n+1):
                samples=[set(S) for S in combinations(range(n),m)]
                for r in range(min(k,m,n-m)+1):
                    vals=[]
                    for a in range(r+1):
                        for b in range(r-a+1):
                            for u in range(min(a,k)+1):
                                for v in range(min(b,k-u)+1):
                                    if a-u+b-v>n-k:continue
                                    P=set(range(u))|set(range(k,k+a-u))
                                    Q=set(range(u,u+v))|set(range(k+a-u,k+a-u+b-v))
                                    require(len(P)==a and len(Q)==b and not P&Q,'cylinder construction')
                                    selected=[S for S in samples if P<=S and not Q&S]
                                    if not selected:continue
                                    value=F(sum(len(S&N) for S in selected),len(selected))
                                    formula=u+F((m-a)*(k-u-v),n-a-b)
                                    require(value==formula,'direct conditional subset expectation')
                                    expected_probability=F(comb(n-a-b,m-a),comb(n,m))
                                    require(F(len(selected),len(samples))==expected_probability,'cylinder probability')
                                    vals.append(value);direct+=1
                                    if (m-1)*r<=m*k-n:require(value>=1,'lifted cover inequality');feasible_checks+=1
                    minimum=F(m*(k-r),n-r)
                    require(min(vals)==minimum,'conditioned minimum');extrema+=1
                    require((minimum>=1)==((m-1)*r<=m*k-n),'exact degree threshold');algebra+=1
                    if n>=m+k:
                        maximum=r+F((m-r)*(k-r),n-r)
                        require(max(vals)==maximum,'conditioned maximum at full k-neighbourhood');lightness+=1
    return {'universe_sizes':list(range(2,10)),'direct_conditioned_expectations':direct,
            'exact_minima':extrema,'degree_threshold_equivalences':algebra,
            'full_k_neighbourhood_maxima':lightness,'feasible_lifted_cover_checks':feasible_checks}

def relaxation_gap():
    p=19;A=(0,1,2,4);k=4;m=6;r=1
    count=0;best=p;first=None;optima=0;mean_sum=0
    for T in combinations(range(p),m):
        u=convolution(A,T,p).count(0);count+=1
        if u<best:best=u;first=T;optima=1
        elif u==best:optima+=1
        mean_sum+=u
    require(count==comb(p,m) and best==1,'actual cylinder/integral separation')
    N=set((-a)%p for a in A)
    conditional=[];samples=list(combinations(range(p),m))
    for P,Q in [((),())]+[((i,),()) for i in range(p)]+[((),(i,)) for i in range(p)]:
        sets=[S for S in samples if all(i in S for i in P) and all(i not in S for i in Q)]
        v=F(sum(len(set(S)&N) for S in sets),len(sets))
        require(v>=1,'degree-one cylinder cover inequality')
        conditional.append({'P':list(P),'Q':list(Q),'conditional_occupancy':rat(v),'cylinder_probability':rat(F(len(sets),len(samples)))})
    require(min(F(*x['conditional_occupancy']) for x in conditional)==1,'sharp cylinder minimum')
    return {'p':p,'A':list(A),'B':[],'m':m,'r':r,'center_sets_enumerated':count,'optimum_residual':best,
            'optimal_center_count':optima,'optimum_witness':list(first),'mean_residual':rat(F(mean_sum,count)),
            'conditional_checks_at_y_zero':conditional,
            'all_y_justification':'Every target neighbourhood y-A is a translate of -A; the same uniform-subset cylinder counts apply.',
            'invalid_implication_refuted':'Cylinder-lifted LP feasibility does not imply integral completion.',
            'scope':'Synthetic prime example at budget six; not the original coefficient-100 asymptotic cap.'}

def rational_power_ge(R,base,exponent):
    base=F(base);exponent=F(exponent)
    return R**exponent.denominator*base.denominator**exponent.numerator >= base.numerator**exponent.numerator

def product_checks():
    profiles=[]
    for p in (5,7,11):
        k=isqrt(p)
        for A in combinations(range(p),k):
            orbit={tuple(sorted((u*a+v)%p for a in A)) for u in range(1,p) for v in range(p)}
            if A==min(orbit):profiles.append({'p':p,'k':k,'A':list(A)})
    count=minimal_count=0;shape_checks={};minimal_examples=[]
    for row in profiles:
        p,k,A=row['p'],row['k'],row['A']
        if p not in (5,7,11) or k!=isqrt(p):continue
        Aset=set(A);L=max(sum((a+d)%p in Aset for a in A) for d in range(1,p))
        for mask in range(1<<p):
            T=[t for t in range(p) if mask>>t&1];t=len(T)
            f=convolution(A,T,p)
            if not all(f) or k*t<=p:continue
            total=k*t-p;Y2=sum((n-1)**2 for n in f);R=prod(f)
            require(Y2>0,'positive variance denominator')
            exponent=F(total*total,Y2);base=1+F(Y2,total)
            require(rational_power_ge(R,base,exponent),'exact Jensen representation-product bound')
            V=F(L*t*(t-1)-k*t+p,p)
            require(F(Y2,p)<=V and V>0,'codegree upper bound on second centered moment')
            e2=F(total*total,p*p)*p/V;b2=1+V/F(total,p)
            require(rational_power_ge(R,b2,e2),'codegree-substituted logarithmic product bound')
            count+=1
            minimal=all(any(f[(a+s)%p]==1 for a in A) for s in T)
            if minimal and t<p:
                private=f.count(1)
                require(private>=t,'minimal cover private target count')
                # R <= ((kt-t)/(p-t))^(p-t), checked without logs.
                require(R*(p-t)**(p-t)<=(k*t-t)**(p-t),'minimal-cover AMGM bound')
                minimal_count+=1
                if len(minimal_examples)<3:minimal_examples.append({'p':p,'A':A,'T':T,'occupancies':f,'R':R,'private_targets':private})
            key=(p,k,t,tuple(sorted(f)),L)
            shape_checks[key]={'p':p,'k':k,'t':t,'occupancy_histogram':[[i,f.count(i)] for i in sorted(set(f))],
                              'L':L,'R':R,'jensen_base':rat(base),'jensen_exponent':rat(exponent),
                              'codegree_base':rat(b2),'codegree_exponent':rat(e2)}
    require(count and minimal_count,'empty product checks')
    return {'cover_pairs_checked':count,'minimal_cover_pairs_checked':minimal_count,
            'distinct_histogram_parameter_cases':len(shape_checks),'cases':list(shape_checks.values()),'minimal_examples':minimal_examples}

def run():
    return {'scope':'Synthetic finite identity and separation checks only; no original asymptotic resolution.',
            'resolution_claimed':False,'cylinders':cylinder_checks(),'relaxation_gap':relaxation_gap(),'representation_products':product_checks()}
if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
