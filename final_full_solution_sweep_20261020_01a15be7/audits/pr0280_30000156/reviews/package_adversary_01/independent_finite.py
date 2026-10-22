#!/usr/bin/env python3
"""Independent direct orbit diagnostics, using no code from the submitted checker."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from math import gcd,isqrt
import datetime,json,sys

OUT=Path(__file__).resolve().parent
checks=0
def check(ok,why):
    global checks
    checks+=1
    if not ok:raise RuntimeError(why)
def primes(n):
    return [p for p in range(2,n+1) if not any(p%d==0 for d in range(2,isqrt(p)+1))]
def brute_order(a,p):
    y=1
    for k in range(1,p):
        y=y*a%p
        if y==1:return k
    raise RuntimeError('order not found')
def totient(n):return sum(gcd(k,n)==1 for k in range(1,n+1))
def distinct_factors(n):return [q for q in primes(n) if n%q==0]

rows=[];graph_points=0;graph_primes=[]
for p in [p for p in primes(311) if p%4==3]:
    n=p-1
    orders=[brute_order((u*u+1)%p,p) for u in range(p)]
    primitive=sum(d==n for d in orders)
    theta=Fraction(totient(n),n)
    histogram=Counter({1:p})
    for d in orders:histogram[d]+=p-1
    check(sum(histogram.values())==p*p,'mass')
    check(histogram[1]==2*p-1,'fixed points')
    check((Fraction(primitive,p)-theta)**2*p <= theta**2*(2**len(distinct_factors(n))-1)**2,'character estimate')
    below=Fraction(n,p)-Fraction(1,p*p)
    for x in [Fraction(1,2),Fraction(3,4),Fraction(15,16),below,Fraction(n,p),Fraction(1)]:
        cdf=Fraction(sum(v for d,v in histogram.items() if d<=p*x),p*p)
        if x>=Fraction(1,2) and x<Fraction(n,p):
            check(cdf==1-Fraction(n*primitive,p*p),'CDF')
        if x>=Fraction(n,p):check(cdf==1,'primitive boundary')
    h=lambda t:max(Fraction(0),min(Fraction(1),2*t-1))
    moment=sum(Fraction(v,p*p)*h(Fraction(d,p)) for d,v in histogram.items())
    check(moment==Fraction((p-2)*n*primitive,p**3),'moment')
    if p<=71:
        remaining={(u,v) for u in range(p) for v in range(p)}
        graph_hist=Counter()
        while remaining:
            z=min(remaining);t=z;cycle=[]
            while True:
                cycle.append(t);remaining.remove(t)
                u,v=t;t=(u,(u*u+1)*v%p)
                if t==z:break
                check(t in remaining,'raw graph transient or cycle merge')
            graph_hist[len(cycle)]+=len(cycle)
            for u,v in cycle:check(len(cycle)==(1 if v==0 else orders[u]),'raw period')
        check(graph_hist==histogram,'raw graph point histogram')
        graph_points+=p*p;graph_primes.append(p)
    rows.append({'p':p,'primitive':primitive,'theta':str(theta),'moment':str(moment)})
bad=[]
for p in [2,5,13,17,29,37,41]:
    roots=[u for u in range(p) if (u*u+1)%p==0]
    check(len(roots)==(1 if p==2 else 2),'bad prime root count')
    for u in roots:check((u,(u*u+1)*0%p)==(u,(u*u+1)*1%p),'bad prime collision')
    bad.append(p)
for n in range(1,1501):check(2*totient(n)**2>=n,'totient lower bound')
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,
        'status':'PASS','exact_checks':checks,'admissible_primes':len(rows),'prime_bound':311,
        'raw_graph_primes':graph_primes,'raw_graph_points':graph_points,'bad_prime_controls':bad,
        'totient_gcd_count_bound':1500,'rows':rows,
        'scope':'Independent finite identities and boundary controls only; no infinitude or atomlessness claim'}
(OUT/'INDEPENDENT_FINITE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
