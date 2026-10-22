#!/usr/bin/env python3
"""Exact finite controls for the reflection lemma; no proposal code imported.
This does not establish the asymptotic analytic inputs of the derivation.
"""
import json
import math
from fractions import Fraction as F

checks=0
cases=0
nonidentical=0
incompatible=0

def require(value,label):
    global checks
    checks+=1
    if not value:raise RuntimeError(label)

def ok(n,W,conds,sign):
    return n%W==0 and all((n+sign*r)%d==0 for d,r in conds)

for W in [1,4,6]:
 for d in range(1,7):
  for e in range(1,7):
   for r in range(1,4):
    for s in range(1,4):
     for q in range(1,8):
      for k in range(1,4):
       conds=[(d,r),(e,s),(q,k)]
       Q=math.lcm(W,d,e,q)
       plus={n for n in range(Q) if ok(n,W,conds,1)}
       minus={n for n in range(Q) if ok(n,W,conds,-1)}
       require(len(plus)<=1 and len(minus)<=1,'unique CRT class')
       require(minus=={(-n)%Q for n in plus},'exact negated class')
       incompatible+=not bool(plus)
       for a,h in [(1,0),(2,1),(7,9),(3,23)]:
        cp=sum(ok(n,W,conds,1) for n in range(a,a+h))
        cm=sum(ok(n,W,conds,-1) for n in range(a,a+h))
        require(abs(cp-cm)<=1,'one-class interval error')
        nonidentical+=(cp!=cm)
       cases+=1

# Signed expansion: absolute coefficients, not signed inequalities.
configs=[(F(3,2),1,[(2,1),(3,2)]),
         (F(-7,3),4,[(3,1),(5,2)]),
         (F(1,5),6,[(4,1),(6,2)]),
         (F(-2),1,[(2,2),(7,1)])]
budget=sum(abs(c) for c,W,cs in configs)
for a in range(1,14):
 for h in range(31):
  totals=[]
  for sign in [1,-1]:
   totals.append(sum(c*sum(ok(n,W,cs,sign) for n in range(a,a+h))
                     for c,W,cs in configs))
  require(abs(totals[0]-totals[1])<=budget,'signed coefficient budget')

# Negating only the queried condition does not preserve compatibility.
wrong_plus=sum(n%3==2 and n%3==2 for n in range(1,31))
wrong_minus=sum(n%3==1 and n%3==2 for n in range(1,31))
require(abs(wrong_plus-wrong_minus)>1,'partial-reflection failure control')
require(nonidentical>0,'no false equality-of-distributions assertion')
require(incompatible>0,'incompatible configurations exercised')
require(F(1)-F(2,99)==F(97,99),'normalization exponent')
require(F(97,99)>F(95,100),'uniform exponent margin')
require(F(95,100)-F(4,100)>F(1,10),'relative-moment error margin')
print(json.dumps({'status':'PASS','checks':checks,'CRT_configurations':cases,
                 'incompatible_configurations':incompatible,
                 'nonidentical_interval_counts':nonidentical,
                 'signed_expansion_budget':str(budget),
                 'partial_reflection_control_difference':wrong_plus-wrong_minus,
                 'limit':'Finite controls supplement the all-modulus argument; published asymptotic sieve inputs are not computationally certified.'},sort_keys=True,indent=2))
