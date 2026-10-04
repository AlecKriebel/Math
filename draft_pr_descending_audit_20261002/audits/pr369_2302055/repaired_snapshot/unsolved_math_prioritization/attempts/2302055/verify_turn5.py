#!/usr/bin/env python3
from fractions import Fraction as F
from math import comb
from itertools import product
import json,random
rng=random.Random(230205505);checks=0
def ck(v):
 global checks
 assert v
 checks+=1
param_cases=0
for p in range(-20,21):
 for q in range(1,10):
  a=F(p,q)
  if a in (0,1):continue
  b=1-a
  for t in [F(1),F(-2),F(3,5)]:ck(-a*t-b*t+t==0);param_cases+=1
# Exact subunit exponents, including irrational-case-independent inequalities.
exponents=[F(p,q)for q in range(1,20)for p in range(q)]
for alpha in exponents:
 for m in range(1,20):ck(m-alpha>0)
for _ in range(2000):
 a=[rng.choice(exponents)for _ in range(3)];ck((sum(a)>0)==any(x>0 for x in a))
# I+N Jordan powers, as coefficient identities in a nilpotent variable.
jordan_cases=0
for d in range(2,13):
 p=[1]+[0]*(d-1)
 for n in range(1,41):
  p=[p[0]]+[p[k]+p[k-1]for k in range(1,d)]
  ck(p==[comb(n,k)if k<=n else 0 for k in range(d)]);ck(p[1]==n);jordan_cases+=1
# Lower bound |t+c|>=|t|/2 under |t|>=2|c|, Gaussian integers.
norm_cases=0
for _ in range(5000):
 x,y,a,b=[rng.randrange(-40,41)for _ in range(4)];T=x*x+y*y;C=a*a+b*b
 if T and T>=4*C:ck(4*((x+a)**2+(y+b)**2)>=T);norm_cases+=1
# Polynomial translations preserve the declared finite monomial span.
poly_cases=0
for degree in range(15):
 for shift in range(-5,6):
  coeff=[comb(degree,k)*shift**(degree-k)for k in range(degree+1)]
  for x in range(-3,4):ck(sum(c*x**k for k,c in enumerate(coeff))==(x+shift)**degree);poly_cases+=1
print(json.dumps({'exact_assertions':checks,'translation_parameter_cases':param_cases,'jordan_power_cases':jordan_cases,'gaussian_norm_cases':norm_cases,'polynomial_translation_cases':poly_cases,'analytic_resolution_claimed':False},indent=2))
