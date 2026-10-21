from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from math import gcd,isqrt
import json,cmath
OUT=Path(__file__).resolve().parent
checks=0; numeric=0; graphs=0; rows=[]
def require(v,msg):
 global checks
 checks+=1
 if not v:raise RuntimeError(msg)
def primes(n):return [v for v in range(2,n+1) if all(v%d for d in range(2,isqrt(v)+1))]
def divisors(n):return [d for d in range(1,n+1) if n%d==0]
def phi(n):return sum(gcd(n,k)==1 for k in range(1,n+1))
def mu(n):
 qs=[q for q in primes(n) if n%q==0]
 return 0 if any(n%(q*q)==0 for q in qs) else (-1)**len(qs)
def order(a,p):
 b=1
 for d in range(1,p):
  b=b*a%p
  if b==1:return d
 raise RuntimeError('nonunit order')
for p in primes(1500):
 if p%4!=3:continue
 n=p-1; ds=divisors(n); w=2**len([q for q in primes(n) if n%q==0]); th=F(phi(n),n)
 aa=[(u*u+1)%p for u in range(p)]; oo=[order(a,p) for a in aa]; P=oo.count(n)
 require(0 not in aa,'zero multiplier'); require((F(P,p)-th)**2*p<=th**2*(w-1)**2,'primitive estimate')
 mass=Counter({1:p})
 for d in oo:mass[d]+=p-1
 require(sum(mass.values())==p*p,'point normalization');require(mass[1]==2*p-1,'fixed fiber exception')
 for den in range(1,14):
  for num in range(den+1):
   x=F(num,den); c=F(sum(m for d,m in mass.items() if d*den<=num*p),p*p)
   if F(1,2)<=x<1 and p*(1-x)>1:require(c==1-F(n*P,p*p),'exact threshold formula')
 for k in [-1,0,1]:
  x=F(n,p)+F(k,p*p)
  c=F(sum(m for d,m in mass.items() if F(d,p)<=x),p*p)
  require(c==(1-F(n*P,p*p) if k<0 else 1),'moving cutoff boundary')
 ramp=sum(F(m,p*p)*max(F(0),min(F(1),2*F(d,p)-1)) for d,m in mass.items())
 require(ramp==F((p-2)*n*P,p**3),'ramp')
 if p<=59:
  succ={(u,v):(u,(u*u+1)*v%p) for u in range(p) for v in range(p)}
  require(len(set(succ.values()))==p*p,'raw permutation'); unseen=set(succ); raw=Counter()
  while unseen:
   z=next(iter(unseen));t=succ[z];cycle=[z]
   while t!=z:cycle.append(t);t=succ[t]
   for q in cycle:require(q in unseen,'raw cycle overlap');unseen.remove(q)
   raw[len(cycle)]+=len(cycle)
  require(raw==mass,'raw independent histogram');graphs+=p*p
  g=next(a for a in range(1,p) if order(a,p)==n); log={pow(g,k,p):k for k in range(n)}
  for k in range(n):
   val=th*sum(F(mu(d),phi(d))*sum(e*mu(d//e) for e in divisors(gcd(d,k))) for d in ds)
   require(val==int(gcd(k,n)==1),'Ramanujan primitive indicator')
  for j in range(1,n):
   chi=lambda a:0 if not a%p else cmath.exp(2j*cmath.pi*j*log[a%p]/n)
   eta=lambda a:0 if not a%p else (1 if pow(a%p,n//2,p)==1 else -1)
   S=sum(chi(a) for a in aa); J=sum(eta(s)*chi(1-s) for s in range(p));numeric+=1
   if abs(S-eta(-1)*J)>1e-8:raise RuntimeError('Jacobi diagnostic')
   numeric+=1
   if abs(S)>p**.5+1e-8:raise RuntimeError('Jacobi bound diagnostic')
   if j==n//2:
    numeric+=1
    if abs(S+1)>1e-8:raise RuntimeError('quadratic exceptional diagnostic')
 rows.append({'p':p,'P':P,'theta':str(th),'moment':str(ramp)})
for p in [2,5,13,17,29,37,41,53]:
 zeros=[u for u in range(p) if (u*u+1)%p==0];require(len(zeros)==(1 if p==2 else 2),'bad reduction')
 for u in zeros:require((u,(u*u+1)*0%p)==(u,(u*u+1)*1%p),'bad reduction collision')
result={'status':'PASS','assertions_exact':checks,'diagnostics_complex_approximate':numeric,'admissible_primes':len(rows),'prime_bound':1500,'raw_graph_points':graphs,'rows':rows,'scope':'Independent finite falsification only; no imported checker or asymptotic inference'}
(OUT/'INDEPENDENT_MATH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
