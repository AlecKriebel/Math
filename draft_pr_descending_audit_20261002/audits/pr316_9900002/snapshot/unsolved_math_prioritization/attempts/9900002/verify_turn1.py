#!/usr/bin/env python3
"""Exact finite controls for the written renewal counterexample, not a limit proof."""
from fractions import Fraction as F
import json
checks=0

def ck(v):
 global checks
 assert v
 checks+=1

def eq(a,b):ck(a==b)

# Explicit law parameters and the geometric tail majorant.
for n in range(1,9):
 p=F(1,2**(2**n));a=2**(4**n)
 eq(F(1,2**(2**(n+1))),p*p)
 eq(p*a,2**(4**n-2**n))
 partial=F(0)
 for j in range(12):
  ck(2**j>=j+1)
  # Exponent comparison proves p**(2**j)<=p**(j+1) without huge integers.
  partial+=p**(2**j) if n+j<=11 else F(0)
 ck(partial<=p/(1-p))
 if n>=2:
  aprev=2**(4**(n-1));t=F(a,2)
  ck(2<=aprev<t<a)
  exp=1+4**(n-1)+2**n-4**n
  eq(F(2*aprev,1)/(p*a),F(2)**exp)
  eq(exp,1+2**n-3*4**(n-1))
  eps=p/(1-p)+F(2)**exp
  bound=F(aprev,a)+p/(2*(1-p))
  ck(0<eps<1);ck(0<bound<1)
  if n>2:ck(eps<last_eps);ck(bound<last_bound)
  last_eps,last_bound=eps,bound
p=F(1,4)
eq(p/(1-p),F(1,3))
# Entire n>=2 exponent monotonicity: E(n+1)-E(n)=2**n-9*4**(n-1)<0.
for n in range(2,100):
 d=2**n-9*4**(n-1);ck(d<0)
 eq((1+2**(n+1)-3*4**n)-(1+2**n-3*4**(n-1)),d)

# Exact finite renewal controls. These discrete toy laws test the first-large
# interval identity only; the written counterexample's non-lattice property
# comes from its explicitly continuous base component, not these toy laws.
cases=0
for a in range(3,11):
 for pnum in range(1,5):
  for rnum in range(1,5):
   p=F(pnum,20);r=F(rnum,20);small=1-p-r
   law={1:small/3,2:2*small/3,a:p,2*a:r};q=p+r
   M=law[1]+2*law[2]
   eq(sum(law.values()),1);ck(q>0)
   for t in range(1,a):
    # u[s] is renewal mass at s; intervals are [s,s+x).
    u=[F(0)]*(t+1);u[0]=1
    for s in range(1,t+1):u[s]=sum(v*u[s-x] for x,v in law.items() if x<=s)
    total=sum(u[s]*v for s in range(t+1) for x,v in law.items() if s+x>t)
    exact=sum(u[s]*p for s in range(t+1))
    eq(total,1)
    # Independently count paths ending just before their first >=a jump.
    small_u=[F(0)]*(t+1);small_u[0]=1
    for s in range(1,t+1):small_u[s]=sum(law[x]*small_u[s-x] for x in (1,2) if x<=s)
    eq(exact,p*sum(small_u));ck(0<=exact<=1)
    ck(1-exact<=(q-p)/q+M/(q*t))
    # General threshold m(t), with t<a, has exact small plus t*tail form
    # once t>=2; this is the finite analogue of equation (12).
    if t>=2:eq(sum(v*min(x,t) for x,v in law.items()),M+t*q)
    cases+=1
   # Finite geometric sums, with exact tail remainder, check stopping identities.
   for k in range(1,16):
    eq(sum((1-q)**(j-1)*p for j in range(1,k+1)),p/q*(1-(1-q)**k))
    eq(sum((1-q)**(j-1)*M for j in range(1,k+1)),M/q*(1-(1-q)**k))

print(json.dumps({'status':'PASS','exact_assertions':checks,'finite_renewal_cases':cases,'parameter_n_values':list(range(1,9)),'arithmetic':'exact integers and fractions','scope':'Finite controls of identities and bounds only. The all-normalizers impossibility and infinite-mean non-lattice construction are proved in TURN_1.md.'},indent=2))
