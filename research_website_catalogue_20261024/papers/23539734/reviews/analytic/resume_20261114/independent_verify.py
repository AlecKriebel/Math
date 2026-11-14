#!/usr/bin/env python3
"""Read-only exact diagnostics. No finite check proves a prime-limit theorem.

Independent implementations use repeated multiplication for orders, exact
cyclotomic polynomial reduction for character norms, and integer Ramanujan
sums for the primitive indicator. Python -O cannot disable any check.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from math import gcd,isqrt
import hashlib,json,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
BINDS={
 'sources/SOURCE_READY.json':'1e18c3ce5d1b7556f97ee9c90f4d8ed21fa6a4d19e54cee8b730210a15795eaa',
 'sources/fixed-birational-cycle-nonlimit.pdf':'e555c20722ca9edb2bc8d164103e748b87c37b56e5eb8bed18c80b33031f737c',
 'sources/published-source/birational-cycle-verification/paper/main.tex':'8d93d964cf09e2d895048456aca91d075edb2d2002b85de0dd061f6e2aa9e25f',
 'reviews/analytic/EARLY_SEAL.json':'b31fc6fe1b5cce1d2fb38c195c7471fbde27716f45559027bef7524fd81948a9',
}
counts=Counter()
def check(t,label):
 counts[label]+=1
 if not t:raise RuntimeError(label)
def primes(n):return [p for p in range(2,n+1) if all(p%d for d in range(2,isqrt(p)+1))]
def divs(n):return [d for d in range(1,n+1) if n%d==0]
def phi(n):return sum(gcd(k,n)==1 for k in range(1,n+1))
def mu(n):
 out=1
 for p in primes(isqrt(n)):
  if n%(p*p)==0:return 0
  if n%p==0:n//=p;out=-out
 return -out if n>1 else out
def order(a,p):
 if not 0<a<p:raise ValueError('nonzero field element required')
 b=a;d=1
 while b!=1:b=b*a%p;d+=1
 return d
def ramp(t):return max(F(0),min(F(1),2*t-1))
def trim(a):
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def divide(a,b):
 a=a[:];q=[0]*max(1,len(a)-len(b)+1)
 while len(a)>=len(b) and a!=[0]:
  k=len(a)-len(b);c=a[-1];q[k]=c
  for j,v in enumerate(b):a[k+j]-=c*v
  trim(a)
 return trim(q),a
cyclo={1:[-1,1]}
def cyclotomic(n):
 if n not in cyclo:
  a=[-1]+[0]*(n-1)+[1]
  for d in divs(n)[:-1]:
   a,r=divide(a,cyclotomic(d));check(r==[0],'cyclotomic exact division')
  cyclo[n]=a
 return cyclo[n]
def generator_logs(p):
 n=p-1
 for a in range(1,p):
  if order(a,p)==n:
   vals=[];v=1
   for k in range(n):vals.append(v);v=v*a%p
   check(len(set(vals))==n,'generator covers field units')
   return {v:k for k,v in enumerate(vals)}
 raise RuntimeError('no generator')
def main():
 check(len(sys.argv)==1,'no argument overrides')
 for path,digest in BINDS.items():check(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'input hash')
 ps=primes(1000);rows=[];point_cycle_weight_witness=None
 for p in ps:
  if p==2:continue
  n=p-1;aa=[(u*u+1)%p for u in range(p)];r=aa.count(0)
  oo=[order(a,p) for a in aa if a];P=oo.count(n);theta=F(phi(n),n)
  W=sum(mu(d)!=0 for d in divs(n));R=p*(p-r)
  check(r==(0 if p%4==3 else 2),'root count')
  check((F(P,p)-F(p-r,p)*theta)**2*p<=theta**2*(W-1)**2,'primitive character bound')
  hist=Counter({1:p-r})
  for d in oo:hist[d]+=p-1;check(n%d==0,'period divides p-1')
  check(sum(hist.values())==R,'regular point normalization')
  mom=sum(F(c,R)*ramp(F(d,p)) for d,c in hist.items())
  check(mom==F((p-2)*(p-1)*P,p*R),'ramp exact identity')
  for x in [F(0),F(1,2),F(3,4),F(7,8),F(n,p),F(1),F(2)]:
   D=F(sum(c for d,c in hist.items() if F(d,p)<=x),R)
   if F(1,2)<=x<1 and p*(1-x)>1:check(D==1-F((p-1)*P,R),'eventual CDF identity')
   if x==F(n,p):check(D==1,'moving endpoint equals one')
   if x==0:check(D==0,'zero endpoint')
   if r and p<=47:
    for e in range(r*p+1):
     for included in [0,e]:
      DD=F(D*R+included,R+e)
      check(abs(DD-D)<=F(e,R+e)<=F(r,p),'exceptional mixture extremal CDF')
  if p%4==3:
   cyc={d:c//d for d,c in hist.items()}
   Dpoint=F(sum(c for d,c in hist.items() if 4*d<=3*p),R)
   Dcycle=F(sum(c for d,c in cyc.items() if 4*d<=3*p),sum(cyc.values()))
   if Dpoint!=Dcycle and point_cycle_weight_witness is None:point_cycle_weight_witness={'p':p,'point_CDF':str(Dpoint),'cycle_CDF':str(Dcycle)}
  rows.append({'p':p,'roots':r,'P':P,'theta':str(theta),'moment':str(mom)})
 # Integer Ramanujan sums verify the primitive character indicator exactly.
 for n in range(2,201):
  ds=divs(n);ph={d:phi(d) for d in ds};mm={d:mu(d) for d in ds}
  for k in range(n):
   c=lambda d:sum(e*mm[d//e] for e in ds if d%e==0 and k%e==0)
   indicator=F(ph[n],n)*sum(F(mm[d],ph[d])*c(d) for d in ds)
   check(indicator==int(gcd(k,n)==1),'primitive indicator exact Ramanujan')
 # Character sums are exact elements of Z[zeta_(p-1)], never floats.
 for p in primes(101)[1:]:
  n=p-1;logs=generator_logs(p);pol=cyclotomic(n)
  for k in range(1,n):
   C=Counter((k*logs[(u*u+1)%p])%n for u in range(p) if (u*u+1)%p)
   corr=[0]*n
   for a,c in C.items():
    for b,d in C.items():corr[(a-b)%n]+=c*d
   rem=divide(trim(corr),pol)[1]
   check(rem==[1 if k==n//2 else p],'character norm exact cyclotomic')
   if k==n//2:check(divide([C[j] for j in range(n)],pol)[1]==[-1],'quadratic character sum minus one')
 # Finite Mobius rearrangement and an absolute tail bound, not a mean proof.
 for X in [3,10,25,100,250,1000]:
  qp=[p for p in ps if p<=X]
  lhs=sum(F(phi(p-1),p-1) for p in qp)
  coeff=[F(mu(d),d)*sum((p-1)%d==0 for p in qp) for d in range(1,X)]
  check(lhs==sum(coeff),'finite prime mean Mobius rearrangement')
  for K in [1,2,5,10]:
   tail=sum(abs(coeff[d-1]) for d in range(K+1,X))
   check(tail<=F(X,K),'finite absolute tail X/K')
 check(point_cycle_weight_witness is not None,'weighting countercontrol witness')
 data={'status':'PASS','scope':'Finite identities and exact character algebra only; analytic conclusions require the recorded proofs and primary theorem interfaces.','odd_primes_through_1000':len(rows),'character_primes_through_101':len(primes(101))-1,'controls_by_family':dict(sorted(counts.items())),'total_controls':sum(counts.values()),'point_cycle_weight_witness':point_cycle_weight_witness,'finite_prime_rows_sha256':hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'input_sha256':BINDS}
 print(json.dumps(data,indent=2,sort_keys=True))
if __name__=='__main__':main()
