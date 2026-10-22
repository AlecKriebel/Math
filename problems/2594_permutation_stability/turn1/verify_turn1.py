#!/usr/bin/env python3
"""Exact finite controls for Turn 1; no claim about the unrestricted group problem."""
from itertools import permutations, combinations
from math import gcd, lcm
from collections import Counter
import json
checks=Counter()
def check(ok,kind):
    checks[kind]+=1
    if not ok: raise AssertionError(kind)
def mul(p,q): return tuple(p[q[x]] for x in range(len(p)))
def inv(p):
    q=[0]*len(p)
    for x,y in enumerate(p):q[y]=x
    return tuple(q)
def compression(p,X):
    X=tuple(X); idx={x:i for i,x in enumerate(X)};ans=[]
    for x in X:
        y=p[x]
        while y not in idx:y=p[y]
        ans.append(idx[y])
    return tuple(ans)
def mismatch(p,q):return sum(a!=b for a,b in zip(p,q))
def power(p,k):
    if k<0:return power(inv(p),-k)
    ans=tuple(range(len(p)))
    while k:
        if k&1:ans=mul(ans,p)
        p=mul(p,p);k//=2
    return ans
def cycle_lengths(p):
    seen=set();ans=[]
    for x in range(len(p)):
        if x in seen:continue
        y=x;length=0
        while y not in seen:seen.add(y);length+=1;y=p[y]
        ans.append(length)
    return ans
# Complete universe through five points, including every nonempty subset.
for m in range(1,6):
    ps=list(permutations(range(m))); indices={p:i for i,p in enumerate(ps)}
    products=[[indices[mul(p,q)] for q in ps] for p in ps]
    for n in range(1,m+1):
        for X in combinations(range(m),n):
            k=m-n; cs=[compression(p,X) for p in ps]
            for i,p in enumerate(ps):
                c=cs[i]
                check(sorted(c)==list(range(n)),'compression_bijection')
                check(compression(inv(p),X)==inv(c),'inverse_preservation')
                check(sum(X[c[j]]!=p[x] for j,x in enumerate(X))<=k,'restriction_error')
                for a in permutations(range(n)):
                    check(mismatch(a,c)<=sum(X[a[j]]!=p[x] for j,x in enumerate(X)),'no_loss_comparison')
                for j,q in enumerate(ps):
                    check(mismatch(mul(c,cs[j]),cs[products[i][j]])<=2*k,'defect_bound_complete')
# Sharp universal factor two.
p=(2,1,0);q=(0,2,1);X=(0,1)
check(mismatch(mul(compression(p,X),compression(q,X)),compression(mul(p,q),X))==2,'sharp_factor_two')
# All integer cycle partitions and every deleted subset, m through eight.
def partitions(n,lo=1):
    if not n:yield ()
    for a in range(lo,n+1):
        for tail in partitions(n-a,a):yield (a,)+tail
for m in range(1,9):
    for sizes in partitions(m):
        p=[];start=0;orbits=[]
        for size in sizes:
            O=set(range(start,start+size));orbits.append(O)
            p.extend(list(range(start+1,start+size))+[start]);start+=size
        p=tuple(p)
        for n in range(1,m+1):
            for X in combinations(range(m),n):
                B=set(range(m))-set(X);U=set().union(*(O for O in orbits if O&B)) if B else set()
                Z=set(X)-U; idx={x:i for i,x in enumerate(X)}
                tau=tuple(idx[p[x]] if x in Z else idx[x] for x in X)
                check(sorted(tau)==list(range(n)),'core_repair_bijection')
                check(mismatch(compression(p,X),tau)<=len(U&set(X)),'core_repair_bound')
                for K in range(1,m+1):
                    large=sum(len(O) for O in orbits if len(O)>K)
                    check(len(U&set(X))<=(K-1)*len(B)+large,'orbit_tail_integer_bound')
# Uniform versus pointwise Z diagnostic, all strict actions through p=7.
prime_results=[]
for p in [3,5,7]:
    n=p-1;cyc=tuple(list(range(1,p))+[0]);X=tuple(range(n));cgen=compression(cyc,X)
    for a in range(-12,13):
        check(mismatch(compression(power(cyc,a),X),power(cgen,a))<=abs(a),'pointwise_cycle_bound')
    minimum=n
    for beta in permutations(range(n)):
        order=lcm(*cycle_lengths(beta));r=sum(beta[x]==x for x in X)
        check(mismatch(cgen,beta)>=r,'uniform_generator_fixedpoint_bound')
        vals=[mismatch(tuple(range(n)),power(beta,p*j)) for j in range(order)]
        check(2*sum(vals)>=order*(n-r),'uniform_average_bound')
        mx=max(mismatch(compression(power(cyc,a),X),power(beta,a)) for a in range(lcm(p,order)))
        check(3*mx>=n,'uniform_one_third_bound')
        minimum=min(minimum,mx)
    prime_results.append({'prime':p,'remaining':n,'minimum_uniform_mismatches':minimum})
print(json.dumps({'scope':'Finite controls only; original KOU-21.85 unresolved','checks_by_kind':dict(sorted(checks.items())),'total_assertions':sum(checks.values()),'prime_cycle_diagnostics':prime_results},indent=2,sort_keys=True))
