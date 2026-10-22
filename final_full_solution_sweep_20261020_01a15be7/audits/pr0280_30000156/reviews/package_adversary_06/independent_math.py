#!/usr/bin/env python3
"""Fresh finite falsification; no submitted checker imports. Exact vs numeric separated."""
from collections import Counter
from fractions import Fraction as F
from math import gcd,isqrt,cos,sin,pi
from pathlib import Path
import json,sys

def require(v,m):
    if not v:raise RuntimeError(m)
def primes(n):return [p for p in range(3,n+1,2) if all(p%d for d in range(2,isqrt(p)+1))]
def factors(n):return [q for q in range(2,n+1) if n%q==0 and all(q%d for d in range(2,isqrt(q)+1))]
def phi(n):return sum(gcd(k,n)==1 for k in range(1,n+1))
def order(a,p):
    require(a%p!=0,'zero has no multiplicative order')
    t=a%p;d=1
    while t!=1:t=t*a%p;d+=1;require(d<p,'Fermat bound')
    return d
def mu(n):
    qs=factors(n)
    return 0 if any(n%(q*q)==0 for q in qs) else (-1)**len(qs)
def ramanujan(d,k):return sum(e*mu(d//e) for e in range(1,d+1) if d%e==0 and k%e==0)
def h(t):return max(F(0),min(F(1),2*t-1))

def main():
    count=0;numeric=0;graphs=0;rows=[];largest=0
    def ck(v,m):
        nonlocal count
        count+=1;require(v,m)
    for p in primes(1000):
        n=p-1;aa=[(u*u+1)%p for u in range(p)];r=aa.count(0);qs=factors(n);theta=F(phi(n),n)
        ck(r==(0 if p%4==3 else 2),'roots')
        oo=[order(a,p) for a in aa if a];P=oo.count(n);hist=Counter({1:p-r})
        for d in oo:hist[d]+=n
        total=p*(p-r);ck(sum(hist.values())==total,'regular count');ck(hist[1]==2*p-r-1,'fixed count')
        ck((P*n-(p-r)*phi(n))**2<=p*phi(n)**2*(2**len(qs)-1)**2,'principal p-r primitive bound')
        ck(2**(4*len(qs))<=64**4*n,'omega bound')
        moment=sum(F(c,total)*h(F(d,p)) for d,c in hist.items())
        ck(moment==(1-F(2,p))*F(n*P,total),'ramp')
        for k in range(1,n+1):
            indicator=theta*sum(F(mu(d),phi(d))*ramanujan(d,k) for d in range(1,n+1) if n%d==0)
            ck(indicator==int(gcd(k,n)==1),'primitive indicator exact integer Ramanujan')
        for d in range(1,n+1):
            if n%d==0:
                direct=(p-r)+n*sum(pow(a,d,p)==1 for a in aa if a)
                ck(sum(c for o,c in hist.items() if d%o==0)==direct,'divisor fixed point count')
        cuts={F(i,j) for j in range(2,18) for i in range(j+1)}|{F(n,p),F(2*n-1,2*p),F(2*n+1,2*p),F(2)}
        for x in cuts:
            d=F(sum(c for o,c in hist.items() if F(o,p)<=x),total)
            if F(1,2)<=x<1 and p*(1-x)>1:ck(d==1-F(n*P,total),'eventual exact CDF')
            if x in [0,1,F(n,p)]:ck(d==(0 if x==0 else 1),'CDF endpoint')
            # Distinct assignments across exceptional points, not a common assigned period.
            if r:
                for e in [r,r*(p-1),r*p]:
                    assigned=[0,1,p-1,p,2*p,p*p]
                    mass=sum(F(assigned[j%6],p)<=x for j in range(e))
                    new=(total*d+mass)/(total+e)
                    ck(abs(new-d)<=F(r,p),'heterogeneous exceptional completion CDF')
        if r:
            for e in [r,r*(p-1),r*p]:
                value=sum(h(F([0,1,p-1,p,2*p,p*p][j%6],p)) for j in range(e))
                ck(abs((total*moment+value)/(total+e)-moment)<=F(r,p),'heterogeneous ramp')
            ck(len({(u,aa[u]*v%p) for u in range(p) for v in [0,1]})<2*p,'class1 full-affine collision')
        if p<=43:
            image={(u,v):(u,aa[u]*v%p) for u in range(p) if aa[u] for v in range(p)}
            ck(len(set(image.values()))==total,'actual graph permutation');visited=set();raw=Counter()
            for z in image:
                if z in visited:continue
                cycle=[];w=z
                while w not in cycle and w not in visited:cycle.append(w);w=image[w]
                ck(w==z,'no transient')
                for u,v in cycle:ck(len(cycle)==(1 if v==0 else order(aa[u],p)),'raw period')
                visited.update(cycle);raw[len(cycle)]+=len(cycle)
            ck(raw==hist,'raw histogram');graphs+=total
        if p<=101:
            generator=next(a for a in range(2,p) if order(a,p)==n);logs={pow(generator,k,p):k for k in range(n)}
            def chi(k,a):
                if not a%p:return 0j
                t=2*pi*k*logs[a%p]/n;return complex(cos(t),sin(t))
            eta=lambda a:0 if a%p==0 else (1 if pow(a%p,n//2,p)==1 else -1)
            for k in range(1,n):
                s=sum(chi(k,a) for a in aa);j=sum(eta(t)*chi(k,1-t) for t in range(p))
                require(abs(s-eta(-1)*j)<1e-8,'numeric Jacobi identity');numeric+=1
                require(abs(abs(s)**2-(1 if k==n//2 else p))<1e-7,'numeric quadratic exception');numeric+=1
            ck(sum(eta(a) for a in aa)==-1,'quadratic character exact')
            ck(sum(a!=0 for a in aa)==p-r,'principal zero extension exact')
        rows.append({'p':p,'r':r,'P':P,'points':total,'ramp':str(moment)})
    for n in range(1,3001):ck(2*phi(n)**2>=n,'totient lower bound')
    value={'status':'PASS','exact_checks':count,'numeric_diagnostics':numeric,'odd_primes':len(rows),'bound':1000,'regular_graph_points':graphs,'class3_primes':sum(z['r']==0 for z in rows),'scope':'Finite falsification only; no analytic-law proof','rows':rows}
    (Path(__file__).parent/('INDEPENDENT_MATH_OPTIMIZED.json' if sys.flags.optimize else 'INDEPENDENT_MATH.json')).write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items() if k!='rows'}))

if __name__=='__main__':main()
