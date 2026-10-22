#!/usr/bin/env python3
"""Finite falsification of the supplementary source-quantifier robustness argument."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,isqrt
import json
C=0
def ck(v,m):
 global C
 if not v:raise RuntimeError(m)
 C+=1
def prime(n):return n>1 and all(n%d for d in range(2,isqrt(n)+1))
def factors(n):return [q for q in range(2,n+1) if prime(q) and n%q==0]
def order(a,p):
 r=1
 for d in range(1,p):
  r=r*a%p
  if r==1:return d
 raise RuntimeError('no order')
def h(t):return max(F(0),min(F(1),2*t-1))
ps=[p for p in range(3,908) if prime(p)];badclass=[]
for p in ps:
 N=p-1;aa=[(u*u+1)%p for u in range(p)];r=aa.count(0);ck(r==(2 if p%4==1 else 0),'quadratic root count');orders=[order(a,p) for a in aa if a];P=orders.count(N);ph=sum(gcd(k,N)==1 for k in range(1,N+1));W=2**len(factors(N))
 ck((P*N-(p-r)*ph)**2<=p*ph*ph*(W-1)**2,'primitive estimate around principal p-r')
 total=p*(p-r);ck((p-r)+(p-1)*len(orders)==total,'regular point normalization')
 for x in [F(1,2),F(2,3),F(3,4),F(4,5),F(7,8)]:
  count=(p-r)*int(F(1,p)<=x)+(p-1)*sum(F(d,p)<=x for d in orders)
  if p*(1-x)>1:ck(F(count,total)==1-F((p-1)*P,total),'regular CDF identity')
  reg=F(count,total)
  for accepted in [0,r*p]:ck(abs(F(count+accepted,p*p)-reg)<=F(r,p),'arbitrary exceptional CDF completion bounded')
 moment=(p-1)*sum(h(F(d,p)) for d in orders)/total;ck(moment==(1-F(2,p))*F((p-1)*P,total),'regular continuous ramp')
 for hm in [F(0),F(r,p)]:ck(abs((1-F(r,p))*moment+hm-moment)<=F(r,p),'arbitrary exceptional moment bounded')
 if r:badclass.append(p)
(O:=Path(__file__).with_name('QUANTIFIER_EXTENSION_CHECKS.json')).write_text(json.dumps({'exact_finite_controls':C,'all_odd_primes_tested':len(ps),'class1_primes_tested':len(badclass),'maximum':max(ps),'all_pass':True,'scope':'Supplementary source-quantifier robustness, outside the frozen theorem stated only on class3. Finite checks do not prove the analytic whole-prime atomless law.'},indent=2)+'\n');print(C)
