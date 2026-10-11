#!/usr/bin/env python3
"""Exact finite covariance controls; no knot-recognition claim."""
import itertools,json
nchecks=0
for n in range(1,7):
 states=list(range(1<<n))
 # Several independently chosen Boolean target sets; nonempty by construction.
 targets=[{0},{(1<<n)-1},{m for m in states if m.bit_count()%2==0},
          {m for m in states if (m*m+3*m+1)%5<3}]
 for p in itertools.permutations(range(n)):
  if n>4 and p not in [tuple(range(n)),tuple(reversed(range(n))),tuple(range(1,n))+(0,)]:continue
  def f(m):return sum(((m>>i)&1)<<p[i] for i in range(n))
  w=tuple(i+1 for i in range(n)); wp=[0]*n
  for i in range(n):wp[p[i]]=w[i]
  cost=lambda m,weights:sum(weights[i] for i in range(n) if m>>i&1)
  assert len({f(m) for m in states})==1<<n;nchecks+=1
  for T in targets:
   if not T:continue
   U={f(m) for m in T}
   assert sorted(m.bit_count() for m in T)==sorted(m.bit_count() for m in U);nchecks+=1
   assert min(cost(m,w) for m in T)==min(cost(m,wp) for m in U);nchecks+=1
   for m in states:
    assert (m in T)==(f(m) in U);nchecks+=1
print(json.dumps({'status':'PASS','exact_assertions':nchecks,'scope':'Formal resolution-cube covariance, cardinality and arbitrary relabeled positive integer costs. No actual unknot detection, source classification, or original-target solution.'},indent=2))
