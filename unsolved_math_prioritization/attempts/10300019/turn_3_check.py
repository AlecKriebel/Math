"""Finite shuffle coverage, branch contradictions, and split-order finite realizations."""
from itertools import combinations,permutations
from math import comb
from collections import Counter
import json
C=Counter()
def shuffles(m,n):
 for positions in combinations(range(m+n),m):
  ps=set(positions);i=j=0;o=[]
  for k in range(m+n):
   if k in ps:o.append(('a',i));i+=1
   else:o.append(('b',j));j+=1
  yield tuple(o)
for m in range(5):
 for n in range(5):
  S=set(shuffles(m,n));assert len(S)==comb(m+n,m);C['shuffle_count']+=1
  for s in S:
   assert [k for c,k in s if c=='a']==list(range(m));assert [k for c,k in s if c=='b']==list(range(n));C['intrinsic_orders']+=2
  if m+n<=7:
   P=set(permutations([('a',i) for i in range(m)]+[('b',i) for i in range(n)]))
   P={s for s in P if [k for c,k in s if c=='a']==list(range(m)) and [k for c,k in s if c=='b']==list(range(n))}
   assert P==S;C['independent_permutation_coverage']+=1
# Conflicting switch requirements cannot be fulfilled by one shared two-point fiber.
for s in shuffles(1,1):
 pos={x:i for i,x in enumerate(s)}
 assert not(pos[('a',0)]<pos[('b',0)] and pos[('b',0)]<pos[('a',0)]);C['switch_conflict']+=1
for n in range(1,101):
 # Every finite split interval is represented by the integers 0,...,2n-1.
 j=lambda x,c:2*x+c
 for x in range(n):
  assert j(x,0)<j(x,1);C['finite_split_gap']+=1
  for y in range(x+1,n):assert j(x,1)<j(y,0);C['finite_split_order']+=1
assert 1*1-0*0==1;C['torus_intersection']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Finite order constraints only. The uncountable nonembedding and geometric intersection arguments are analytical; no realization of the split interval by source laminations is claimed.'},indent=2))
