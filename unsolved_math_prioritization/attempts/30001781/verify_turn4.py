#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product,combinations
from math import comb
import json
nchecks=0
def ck(v):
 global nchecks
 assert v
 nchecks+=1
# Nonidentical independent Bernoulli exceedances: exact Poisson-binomial
# probability agrees with enumeration and obeys the l-subset union bound.
for n in range(1,8):
 probs=[F(i+1,n+2) for i in range(n)]
 pmf=[F(1)]
 for p in probs:
  nxt=[F(0)]*(len(pmf)+1)
  for j,c in enumerate(pmf):nxt[j]+=c*(1-p);nxt[j+1]+=c*p
  pmf=nxt
 ck(sum(pmf)==1)
 for l in range(1,n+1):
  tail=sum(pmf[l:]);union=sum(__import__('functools').reduce(lambda x,y:x*y,(probs[i] for i in I),F(1)) for I in combinations(range(n),l))
  ck(tail<=union)
  ck(union<=comb(n,l)*max(probs)**l)
# All row profiles are included in the exact top-k Euclidean square, not just flat tests.
for w in product(range(-3,4),repeat=4):
 ss=sorted((x*x for x in w),reverse=True)
 for k in range(1,5):
  brute=max(sum(w[i]*w[i] for i in I) for I in combinations(range(4),k))
  ck(brute==sum(ss[:k]))
# Harmonic-square sum used in the additive tail estimate.
acc=F(0)
for k in range(1,301):
 acc+=F(1,k*k);ck(acc<=2)
# Elementary coefficient inequality in the tail-norm summation.
for a,b in product(range(-20,21),repeat=2):ck((a+b)**2<=2*a*a+2*b*b)
# Exact net dimensions / special column-sparsity1 bookkeeping.
for N in range(1,70):
 ck(comb(N,1)==N)
 for m in range(1,N+1):ck(comb(N,m)<=N**m)
print(json.dumps({'status':'PASS','exact_assertions':nchecks,'scope':'Exact independent-exceedance and top-k geometry controls; analytic order-statistic tails, entropy estimate and original gap are proved in TURN_4.md. No simulation or full-conjecture claim.'},indent=2,sort_keys=True))
