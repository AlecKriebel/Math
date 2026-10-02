#!/usr/bin/env python3
"""Finite name-conversion controls. Infinite jump-degree facts are proved analytically."""
from itertools import combinations,product
import random,json
checks=0;cases=0

def ok(x):
 global checks
 assert x
 checks+=1

def compatible(a,b):return a[:len(b)]==b or b[:len(a)]==a
def prefix(a,b):return b[:len(a)]==a
rng=random.Random(300046795)
U=range(9);words=[()]+[t for n in range(1,4) for t in combinations(U,n)]
for trial in range(151):
 B=rng.sample(words[1:],rng.randrange(0,13));complement_basis=[s for s in words if not any(compatible(s,t) for t in B)]
 for h in combinations(U,4):
  pos=any(prefix(t,h) for t in B);neg=any(prefix(s,h) for s in complement_basis)
  ok(pos!=neg);ok(neg==(not pos));cases+=1
# Arbitrarily delayed enumerations still decide each partition bit by dovetailing both sides.
for bits in product((0,1),repeat=8):
 plus=[(rng.randrange(1,50),e) for e,b in enumerate(bits) if b]
 minus=[(rng.randrange(1,50),e) for e,b in enumerate(bits) if not b]
 result=[None]*8
 for stage in range(50):
  for t,e in plus:
   if t==stage:result[e]=1
  for t,e in minus:
   if t==stage:result[e]=0
 ok(tuple(result)==bits)
 for e in range(8):ok(sum(x==e for _,x in plus)+sum(x==e for _,x in minus)==1)
# Every tested prefix of h0 has a compatible cylinder lying outside its singleton.
for n in range(101):
 sigma=tuple(range(n));tau=sigma+(n+1,)
 ok(compatible(sigma,tau));ok(tau!=tuple(range(n+1)));ok(all(a<b for a,b in zip(tau,tau[1:])))
print(json.dumps(dict(status='PASS',assertions=checks,finite_clopen_membership_cases=cases,delayed_partition_patterns=256,scope='finite prefix and name-conversion controls; not an empirical test of Weihrauch degrees'),sort_keys=True,indent=2))
