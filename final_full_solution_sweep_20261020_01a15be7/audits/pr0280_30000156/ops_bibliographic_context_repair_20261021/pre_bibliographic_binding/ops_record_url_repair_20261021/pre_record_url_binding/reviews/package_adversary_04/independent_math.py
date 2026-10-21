#!/usr/bin/env python3
"""Independent exact finite falsification. No submitted checker imports."""
import json, math, cmath, sys
from fractions import Fraction as F
from collections import Counter
checks=0; numerical=0

def require(v):
 global checks
 checks+=1
 if not v:raise RuntimeError('Independent finite failure '+str(checks))
def primes(n):return [p for p in range(2,n+1) if all(p%d for d in range(2,math.isqrt(p)+1))]
def phi(n):return sum(math.gcd(k,n)==1 for k in range(1,n+1))
def order(a,p):
 r=1
 for d in range(1,p):
  r=r*a%p
  if r==1:return d
 raise RuntimeError('Not a unit')
def mu(n):
 out=1
 for q in primes(n):
  if n%(q*q)==0:return 0
  if n%q==0:out=-out
 return out
rows=[];graphs=0
for p in primes(701):
 if p%4!=3:continue
 n=p-1;ds=[d for d in range(1,n+1) if n%d==0]
 orders=[order((u*u+1)%p,p) for u in range(p)];P=orders.count(n);theta=F(phi(n),n)
 hist=Counter({1:p})
 for d in orders:hist[d]+=p-1
 require(sum(hist.values())==p*p);require(hist[1]==2*p-1)
 omega=sum(n%q==0 for q in primes(n))
 require((F(P,p)-theta)**2*p<=theta**2*(2**omega-1)**2)
 require(2**(4*omega)<=64**4*n)
 for den in range(2,12):
  for num in range(den+1):
   x=F(num,den);D=F(sum(c for d,c in hist.items() if F(d,p)<=x),p*p)
   if F(1,2)<=x<1 and p*(1-x)>1:require(D==1-F(n*P,p*p))
   if x==0:require(D==0)
   if x==1:require(D==1)
 moving=F(n,p);require(sum(c for d,c in hist.items() if F(d,p)<=moving)==p*p)
 require(F(sum(c*max(F(0),min(F(1),2*F(d,p)-1)) for d,c in hist.items()),p*p)==F((p-2)*(p-1)*P,p**3))
 for d in ds:
  fixed=p+(p-1)*sum(pow((u*u+1)%p,d,p)==1 for u in range(p))
  require(fixed==sum(c for e,c in hist.items() if d%e==0))
 # Integer Ramanujan-sum indicator, independently of floating characters.
 for k in range(n):
  total=F(0)
  for d in ds:
   c=sum(e*mu(d//e) for e in range(1,d+1) if d%e==0 and k%e==0)
   total+=F(mu(d)*c,phi(d))
  require(theta*total==(1 if math.gcd(k,n)==1 else 0))
 if p<=59:
  images={(u,v):(u,(u*u+1)*v%p) for u in range(p) for v in range(p)}
  require(len(set(images.values()))==p*p);seen=set();raw=Counter()
  for z in images:
   if z in seen:continue
   path=[];w=z
   while w not in path:
    require(w not in seen);path.append(w);w=images[w]
   require(w==z)
   for u,v in path:require(len(path)==(1 if v==0 else orders[u]))
   seen.update(path);raw[len(path)]+=len(path)
  require(raw==hist);graphs+=p*p
  g=next(a for a in range(1,p) if order(a,p)==n)
  log={pow(g,k,p):k for k in range(n)}
  def chi(k,a):return 0 if a%p==0 else cmath.exp(2j*math.pi*k*log[a%p]/n)
  for k in range(1,n):
   S=sum(chi(k,u*u+1) for u in range(p));J=sum(chi(n//2,s)*chi(k,1-s) for s in range(p))
   if abs(S+J)>1e-8 or abs(abs(S)-(1 if k==n//2 else math.sqrt(p)))>1e-8:raise RuntimeError('Numerical character diagnostic')
   numerical+=2
 rows.append({'p':p,'P':P,'theta':str(theta)})
for p in [2,5,13,17,29,37,41,53]:
 images={(u,(u*u+1)*v%p) for u in range(p) for v in range(p)}
 require(len(images)<p*p)
for n in range(1,1201):require(2*phi(n)**2>=n)
print(json.dumps({'status':'PASS','exact_checks':checks,'approximate_complex_character_diagnostics':numerical,'prime_bound':701,'admissible_primes':len(rows),'full_graph_points':graphs,'optimization':sys.flags.optimize,'finite_only':True,'rows':rows},indent=2))
