#!/usr/bin/env python3
"""Exact finite controls for the uniform-counting proof; not a probability proof."""
from fractions import Fraction as F
from itertools import product
import random,json
rng=random.Random(300042934)
checks=0; telescopes=0; quotients=0; residuals=0
# Rational interval and summation-by-parts identities, including ties.
for t in range(1,81):
 for trial in range(40):
  cs=sorted([F(rng.randrange(1,100),100) for _ in range(t)],reverse=True)
  c=F(rng.randrange(0,int(cs[-1]*100)+1),100)
  hs=[F(0)]+[F(j*j+2*j,17) for j in range(1,t+1)]
  n=[rng.randrange(12) for _ in range(t)]
  Q=[sum(n[j:]) for j in range(t)]
  assert sum(hs[j+1]*n[j] for j in range(t))==sum((hs[j+1]-hs[j])*Q[j] for j in range(t));checks+=1
  ds=cs+[c]
  lhs=-sum(cs)+sum((ds[j]-ds[j+1])*hs[j+1] for j in range(t))
  rhs=(hs[1]-1)*cs[0]+sum((hs[j+1]-hs[j]-1)*cs[j] for j in range(1,t))-c*hs[t]
  assert lhs==rhs;checks+=1;telescopes+=1
# Exact coset cardinality for binary partition subspaces: quotient by constants.
for d in range(1,13):
 vals=list(product((0,1),repeat=d))
 images={tuple(x-x0 for x in v) for v in vals for x0 in [v[0]]}
 assert len(images)==2**d-1;checks+=1;quotients+=1
# Finitely many quotient-sum assignments cannot exceed product of cell counts.
for d in range(2,6):
 classes={tuple(x-v[0] for x in v) for v in product((0,1),repeat=d)}
 for n in range(0,5):
  sums={tuple(sum((j+2)*v[i] for j,v in enumerate(vs)) for i in range(d)) for vs in product(classes,repeat=n)}
  assert len(sums)<=len(classes)**n;checks+=1;residuals+=1
# Geometric coefficients decrease below 7/3, using rational comparisons.
for j in range(2,300):
 q=F(2**(j+1)-1,2**j-1)
 assert 2<q<=F(7,3)<F(5,2);checks+=1
# Probability deletion ratio, exact and valid only on distinct entries.
for n in range(2,14):
 I=list(range(2,n+1))
 for _ in range(50):
  B={i for i in I if rng.randrange(2)}
  K={i for i in B if rng.randrange(2)};Bp=B-K
  def prob(X):
   ans=F(1)
   for i in I:ans*=F(1,i) if i in X else F(i-1,i)
   return ans
  ratio=F(1)
  for i in K:ratio*=F(1,i-1)
  assert prob(B)==prob(Bp)*ratio;checks+=1
# Exact logarithmic rational enclosures from the atanh series.
def logbounds(x,N=80):
 z=(x-1)/(x+1)
 lo=2*sum((z**(2*j+1)/F(2*j+1) for j in range(N)),F(0))
 hi=lo+2*z**(2*N+1)/(F(2*N+1)*(1-z*z))
 return lo,hi
l2,u2=logbounds(F(2));l3,u3=logbounds(F(3))
assert F(0)<l3-1<u3-1<F(1,10);checks+=1
assert F(47,1000)<(l3-1)*l2*l2< (u3-1)*u2*u2<F(48,1000);checks+=1
# Negative-gap maximization with certified log enclosures, random rational bins.
for t in range(1,30):
 h=[F(0)]+[logbounds(F(2**(j+1)-1),N=160)[0] for j in range(1,t+1)] if t<5 else None
 # Check the exact linear-program coefficient algebra with synthetic increments
 # satisfying the same h_1>1 and subsequent increments in (0,1).
 for _ in range(30):
  a=F(1,10);hs=[F(0),1+a]
  for j in range(2,t+1):hs.append(hs[-1]+F(rng.randrange(1,99),100))
  cs=sorted([F(rng.randrange(1,100),100) for _ in range(t)],reverse=True);c=cs[-1]*F(1,2)
  ds=cs+[c]
  lhs=-sum(cs)+sum((ds[j]-ds[j+1])*hs[j+1] for j in range(t))
  assert lhs<=a-c*(t+a);checks+=1
print(json.dumps({'exact_assertions':checks,'summation_by_parts_cases':telescopes,'diagonal_cube_quotient_cases':quotients,'residual_sum_cases':residuals,'infinite_probabilistic_claims_tested':False},indent=2))
