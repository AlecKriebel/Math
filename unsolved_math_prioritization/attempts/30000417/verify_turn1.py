#!/usr/bin/env python3
from itertools import product,combinations
from random import Random
from pathlib import Path
import json
count=0

def check(v,s):
 global count
 count+=1
 if not v:raise AssertionError(s)

def valid(x,d):
 return all(abs(x[i]-x[j])>=d for i in range(len(x)) for j in range(i+1,min(i+3,len(x))))

def reachable(L,d):
 if len(L)==1:return bool(L[0])
 R={(a,b) for a in L[0] for b in L[1] if abs(a-b)>=d}
 for C in L[2:]:R={(b,c) for a,b in R for c in C if abs(a-c)>=d and abs(b-c)>=d}
 return bool(R)

def compress(L,d):
 a=sorted(set().union(*map(set,L)));mapping={a[0]:1}
 for x,y in zip(a,a[1:]):mapping[y]=mapping[x]+min(d,y-x)
 return [tuple(mapping[x] for x in ls) for ls in L],mapping

rng=Random(30000417)
instances=0
for n in range(2,7):
 for d in range(1,5):
  for k in range(1,4):
   for z in range(40):
    L=[tuple(sorted(rng.sample(range(1,20),k))) for _ in range(n)]
    feasible=any(valid(x,d) for x in product(*L))
    check(reachable(L,d)==feasible,('DP brute comparison',n,d,k,z))
    C,mp=compress(L,d)
    check(reachable(C,d)==feasible,('compression feasibility',n,d,k,z))
    check(max(mp.values())<=1+d*(n*k-1),'finite palette bound')
    for a,b in combinations(mp,2):check((abs(a-b)>=d)==(abs(mp[a]-mp[b])>=d),'pair threshold equivalence')
    instances+=1
# Exhaustive tiny domains, including infeasible assignments.
small=0
for d in range(1,4):
 choices=list(combinations(range(1,6),2))
 for L in product(choices,repeat=3):
  check(reachable(L,d)==any(valid(x,d) for x in product(*L)),'all tiny triangle lists')
  small+=1
# Global-minimum constructive argument for a clique (2 or 3 vertices).
def clique_greedy(L,d):
 L=[set(a) for a in L];out=[None]*len(L)
 remaining=set(range(len(L)))
 while remaining:
  label,v=min((a,i) for i in remaining for a in L[i])
  out[v]=label;remaining.remove(v)
  for u in remaining:L[u]={a for a in L[u] if abs(a-label)>=d}
 return out
for d in range(1,16):
 for n in [2,3]:
  k=(n-1)*d+1
  for t in range(60):
   L=[rng.sample(range(1,8*d+5),k) for i in range(n)]
   x=clique_greedy(L,d)
   check(all(a in L[i] for i,a in enumerate(x)),'clique list membership')
   check(valid(x,d),'clique greedy validity')
  check(not reachable([tuple(range(1,(n-1)*d+1))]*n,d),'clique lower obstruction')
for n in range(3,45):
 for trial in range(25):
  L=[rng.sample(range(1,20),3) for i in range(n)];x=[]
  for ls in L:x.append(next(a for a in ls if a not in x[-2:]))
  check(valid(x,1),'d1 path greedy')
  check((3*(n-1))//n+1==3,'d1 floor target')
check((3*(4-1)+4-1)//4+1==4,'catalog ceiling differs at n4d1')
check((abs(1-10)>=3)!=(abs(1-2)>=3),'rank compression is unsafe control')
print(json.dumps(dict(problem_id=30000417,turn=1,status='all controls passed',assertions=count,random_dp_compression_instances=instances,exhaustive_small_triangle_assignments=small,scope='Finite controls for the exact compression/DP proofs and known boundary families; original floor conjecture remains unresolved.',dependencies='Python 3 standard library'),indent=2))
