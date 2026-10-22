#!/usr/bin/env python3
"""Independent exact finite falsification; imports no submitted mathematical checker."""
from collections import Counter
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json
C=0
def ck(v,m):
 global C
 if not v:raise RuntimeError(m)
 C+=1
def prime(p):return p>=2 and all(p%d for d in range(2,int(p**.5)+1))
def divs(n):return [d for d in range(1,n+1) if n%d==0]
def factors(n):return [d for d in divs(n) if prime(d)]
def phi(n):return sum(gcd(k,n)==1 for k in range(1,n+1))
def mu(n):
 ps=factors(n)
 return 0 if any(n%(p*p)==0 for p in ps) else (-1)**len(ps)
def order(a,p):
 t=1
 for d in range(1,p):
  t=t*a%p
  if t==1:return d
 raise RuntimeError('order absent')
def ramp(t):return max(F(0),min(F(1),2*t-1))
ps=[p for p in range(3,908) if p%4==3 and prime(p)]; graphs=0;gpoints=0
for p in ps:
 N=p-1; ph=phi(N); ds=divs(N); W=2**len(factors(N)); aa=[(u*u+1)%p for u in range(p)]
 ck(all(aa),'good reduction');oo=[order(a,p) for a in aa];P=oo.count(N)
 ck(oo.count(1)==1,'only multiplier1 at u0');ck(p+(p-1)*oo.count(1)==2*p-1,'fixed points')
 for u,a in enumerate(aa):
  ck((a*pow(a,-1,p))%p==1,'inverse');ck(N%oo[u]==0,'orders divide N')
 for d in ds:
  ck(p+(p-1)*sum(o and d%o==0 for o in oo)==p+(p-1)*sum(pow(a,d,p)==1 for a in aa),'divisor fixed counts')
 for b in range(2,14):
  for a in range(0,b+1):
   x=F(a,b);D=F(p*(F(1,p)<=x)+(p-1)*sum(F(o,p)<=x for o in oo),p*p)
   if F(1,2)<=x<1 and p*(1-x)>1:ck(D==1-F((p-1)*P,p*p),'fixed cutoff')
   if x==0:ck(D==0,'zero');
   if x==1:ck(D==1,'one')
 ck(F(p+(p-1)*sum(F(o,p)<=F(N,p) for o in oo),p*p)==1,'moving endpoint')
 ck(sum((p-1)*ramp(F(o,p)) for o in oo)/p**2==(1-F(2,p))*F((p-1)*P,p*p),'exact continuous moment')
 ck((P*N-p*ph)**2<=p*ph*ph*(W-1)**2,'primitive bound squared');ck(W**4<=64**4*N,'omega fourth power')
 for k in range(N):
  indicator=F(ph,N)*sum(F(mu(d),phi(d))*sum(e*mu(d//e) for e in divs(gcd(d,k))) for d in ds)
  ck(indicator==int(gcd(k,N)==1),'exact Ramanujan indicator')
 if p<=43:
  points={(u,v) for u in range(p) for v in range(p)};hist=Counter()
  while points:
   z=next(iter(points));chain=[];cur=z
   while cur not in chain:
    ck(cur in points,'raw graph no transient');chain.append(cur);cur=(cur[0],((cur[0]**2+1)*cur[1])%p)
   ck(cur==z,'raw graph returns to start')
   for point in chain:points.remove(point)
   hist[len(chain)]+=len(chain)
  want=Counter({1:p})
  for o in oo:want[o]+=p-1
  ck(hist==want,'raw graph vs independent fiber formula');graphs+=1;gpoints+=p*p
bad=[]
for p in [2,5,13,17,29,37,41]:
 zeros=[u for u in range(p) if (u*u+1)%p==0];ck(bool(zeros),'bad prime has zero multiplier')
 u=zeros[0];ck((u,0)==(u,((u*u+1)*1)%p),'collision');bad.append(p)
for n in range(1,2501):ck(2*phi(n)**2>=n,'totient lower bound')
out={'exact_controls':C,'admissible_primes':len(ps),'max_prime':max(ps),'complete_graphs':graphs,'complete_graph_points':gpoints,'bad_controls_primes':bad,'all_pass':True,'scope':'Finite falsification only. Proof and classical infinite-prime inputs remain essential.'}
Path(__file__).with_name('INDEPENDENT_MATH.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
