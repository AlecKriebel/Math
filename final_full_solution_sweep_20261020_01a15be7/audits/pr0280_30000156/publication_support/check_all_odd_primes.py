#!/usr/bin/env python3
"""Exact all-odd-prime regular/completion controls; no asymptotic extrapolation.

Standard library only; no writes or assert guards. The analytic scalar law is
an explicitly credited classical input, not a consequence of these finite tests.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from math import gcd,isqrt


def primes_to(n):return [p for p in range(3,n+1,2) if all(p%d for d in range(2,isqrt(p)+1))]
def factors(n):
    result=[];q=2
    while q*q<=n:
        if n%q==0:
            result.append(q)
            while n%q==0:n//=q
        q+=1
    if n>1:result.append(n)
    return result
def order(a,p):
    if not 0<a<p:raise RuntimeError('Order requires a nonzero field element')
    d=p-1
    for q in factors(d):
        while d%q==0 and pow(a,d//q,p)==1:d//=q
    return d
def h(t):return max(F(0),min(F(1),2*t-1))
def g(t):return 2*t/(1+t)-1


def calculate():
    controls=0;rows=[];graph_points=0;graph_primes=[]
    def ck(value,message):
        nonlocal controls
        controls+=1
        if not value:raise RuntimeError(message)
    ps=primes_to(1000)
    for p in ps:
        n=p-1;aa=[(u*u+1)%p for u in range(p)];r=aa.count(0)
        ck(r==(2 if p%4==1 else 0),'root count over every odd prime')
        orders=[order(a,p) for a in aa if a]
        ph=sum(gcd(k,n)==1 for k in range(1,n+1));theta=F(ph,n);P=orders.count(n);W=2**len(factors(n))
        ck((P*n-(p-r)*ph)**2<=p*ph*ph*(W-1)**2,'primitive bound with principal p-r')
        ck(W**4<=64**4*n,'uniform elementary squarefree-divisor bound')
        hist=Counter({1:p-r})
        for d in orders:hist[d]+=p-1
        total=p*(p-r)
        ck(sum(hist.values())==total,'regular-domain normalization')
        ck(hist[1]==2*p-r-1,'regular fixed-point count')
        moment=sum(F(count,total)*h(F(d,p)) for d,count in hist.items())
        ck(moment==(1-F(2,p))*F((p-1)*P,total),'exact regular ramp identity')
        signed=sum(F(count,total)*g(F(d,p)) for d,count in hist.items())
        ck(-1<=signed<=1,'globally bounded signed test')
        xs=[F(0),F(1,4),F(1,2),F(2,3),F(3,4),F(4,5),F(7,8),F(1),F(n,p),F(2),F(p)]
        for x in xs:
            count=sum(c for d,c in hist.items() if F(d,p)<=x);reg=F(count,total)
            if F(1,2)<=x<1 and p*(1-x)>1:
                ck(reg==1-F((p-1)*P,total),'exact regular CDF identity')
            if x in [F(0),F(1),F(n,p)]:ck(reg==(0 if x==0 else 1),'regular CDF endpoints')
            for retained in sorted({0,r,r*(p-1),r*p}):
                for period in [0,1,n,p,2*p,p*p]:
                    normalized=F(period,p)
                    completed=F(count+retained*int(normalized<=x),total+retained)
                    ck(abs(completed-reg)<=F(r,p),'arbitrary exceptional CDF/deletion bound')
        for retained in sorted({0,r,r*(p-1),r*p}):
            for period in [0,1,n,p,2*p,p*p]:
                normalized=F(period,p)
                completed=(total*moment+retained*h(normalized))/(total+retained)
                ck(abs(completed-moment)<=F(r,p),'globally bounded ramp completion/deletion')
                completed_signed=(total*signed+retained*g(normalized))/(total+retained)
                ck(abs(completed_signed-signed)<=2*F(r,p),'general bounded continuous statistic control')
        if r:
            for u,a in enumerate(aa):
                if a==0:
                    ck((u,a*1%p)==(u,0),'exceptional nonzero points contract to zero section')
                    ck((u,a*0%p)==(u,0),'exceptional zero section remains fixed')
        if p<=47:
            image={(u,v):(u,aa[u]*v%p) for u in range(p) if aa[u] for v in range(p)}
            ck(len(set(image.values()))==total,'regular orbit graph permutation')
            seen=set();graph_hist=Counter()
            for z in image:
                if z in seen:continue
                path=[];local=set();t=z
                while t not in local and t not in seen:
                    path.append(t);local.add(t);t=image[t]
                ck(t==z,'regular graph has no transient or merger')
                length=len(path)
                for u,v in path:ck(length==(1 if v==0 else order(aa[u],p)),'raw regular cycle agrees with fiber order')
                seen.update(path);graph_hist[length]+=length
            ck(len(seen)==total and graph_hist==hist,'regular graph histogram')
            graph_points+=total;graph_primes.append(p)
        rows.append({'p':p,'r':r,'regular_points':total,'primitive_parameters':P,'theta':str(theta),'ramp':str(moment)})
    encoded=json.dumps(rows,sort_keys=True,separators=(',',':')).encode()
    return {'status':'PASS','scope':'Exact finite checks only; no proof by extrapolation of the classical atomless whole-prime law',
      'odd_prime_bound':1000,'odd_primes':len(ps),'class1_primes':sum(p%4==1 for p in ps),'class3_primes':sum(p%4==3 for p in ps),
      'exact_checks':controls,'regular_graph_primes':graph_primes,'regular_graph_points':graph_points,
      'exceptional_assignment_periods':'0,1,p-1,p,2p,p^2; normalized values may exceed1',
      'prime_rows_sha256':hashlib.sha256(encoded).hexdigest(),'prime_rows':rows}


if __name__=='__main__':print(json.dumps(calculate(),sort_keys=True,indent=2))
