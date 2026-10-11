#!/usr/bin/env python3
"""Exact finite checks for the bulk modular squeeze; no asymptotic numerics."""
from character_tools import parts,character,centralizer
from fractions import Fraction as F
from collections import Counter
import math,json
C=Counter()
def ck(x,key):assert x,key;C[key]+=1
for n in range(1,12):
 ps=parts(n);p=len(ps);zs={mu:centralizer(mu) for mu in ps}
 for mu in ps:ck(zs[mu]<=n**len(mu),'centralizer_length_bound')
 tab=[[character(lam,mu) for mu in ps] for lam in ps]
 for j,mu in enumerate(ps):ck(sum(row[j]**2 for row in tab)==zs[mu],'column_second_moment')
 nonzero=F(sum(x!=0 for row in tab for x in row),p*p)
 for D in (1,2,3,4,6,12,60):
  delta=F(sum(x%D!=0 for row in tab for x in row),p*p)
  for L in sorted({1,n//2,n}):
   good=[j for j,mu in enumerate(ps) if len(mu)<=L];eps=1-F(len(good),p)
   exact_moment=sum((F(zs[ps[j]],p*p*D*D) for j in good),F(0))
   ck(nonzero<=delta+eps+exact_moment,'precise_modular_squeeze')
   ck(nonzero<=delta+eps+F(n**L,p*D*D),'threshold_modular_squeeze')
  for L in range(1,n+1):
   actual=F(sum(len(mu)>=L for mu in ps),p)
   union=sum((F(len(parts(n-t)),p) for t in range(L,n+1)),F(0))
   ck(actual<=union,'exact_uniform_partition_length_tail')
for B in range(1,35):
 D=math.lcm(*range(1,B+1));pps=[]
 for p in range(2,B+1):
  if any(p%d==0 for d in range(2,math.isqrt(p)+1)):continue
  q=p
  while q<=B:pps.append(q);q*=p
 ck(D<=math.factorial(B),'lcm_factorial_bound')
 for x in range(-101,102):ck((x%D==0)==all(x%q==0 for q in pps),'simultaneous_prime_power_equivalence')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Exact finite algebra and counting controls only; asymptotic statements use the written proof and credited primary estimates.'},indent=2))
