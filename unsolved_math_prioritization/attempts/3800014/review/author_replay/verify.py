#!/usr/bin/env python3
"""Small exact correctness tests; analytic proof, not timings, supplies the bound."""
from algorithm import shortest_exact_intervals,minplus_prefix,dominance_pairs
from fractions import Fraction as Q
from itertools import combinations_with_replacement,product
from pathlib import Path
import random,json,hashlib
checks=0;interval_cases=0;convolution_cases=0;dominance_cases=0

def ck(t):
 global checks
 assert t
 checks+=1

def exhaustive_intervals(a):
 out=[None]*len(a)
 for l in sorted(set(a)):
  for u in sorted(set(a)):
   if u<l:continue
   ids=[i for i,v in enumerate(a) if l<=v<=u]
   k=len(ids);value=(u-l,ids[-1],ids[0])
   if out[k-1] is None or value<out[k-1]:out[k-1]=value
 return [None if x is None else (x[0],x[2],x[1]) for x in out]

for n in range(1,7):
 for a in combinations_with_replacement([-2,0,1,3],n):
  expected=exhaustive_intervals(a)
  for d in [None,1,2,3]:
   interval_cases+=1;got=shortest_exact_intervals(a,d);ck(got==expected)
   for k,value in enumerate(got,1):
    if value is not None:
     width,j,i=value;ck(sum(a[j]<=x<=a[i] for x in a)==k);ck(width==a[i]-a[j])
for a in [[Q(-5,7),Q(-5,7),Q(1,3),Q(5,2)], [10**100,10**100+1,10**100+1,10**100+8],[-10**100,-5,0,7,10**100]]:
 for d in [1,2,4]:
  interval_cases+=1;ck(shortest_exact_intervals(a,d)==exhaustive_intervals(a))
ck(shortest_exact_intervals([0,0])==[None,(0,0,1)])
ck(shortest_exact_intervals([4])==[(0,0,0)])
for bad in [[],[2,1]]:
 try:shortest_exact_intervals(bad)
 except ValueError:ck(True)
 else:ck(False)

rng=random.Random(3800014)
for n in range(1,17):
 for mode in range(3):
  A=[Q(rng.randrange(-9,10),rng.choice([1,2,3])) if mode else Q(0) for _ in range(n)]
  B=[Q(rng.randrange(-9,10),rng.choice([1,2,3])) if mode else Q(0) for _ in range(n)]
  expected=[min((A[i]+B[k-i],i) for i in range(k+1)) for k in range(n)]
  M=max([abs(x) for x in A+B])+1
  for d in [1,2,3,5]:
   convolution_cases+=1;got=minplus_prefix(A,B,M,d);ck(got==expected)
   for k,(value,i) in enumerate(got):ck(value==A[i]+B[k-i]);ck(0<=i<=k)

for d in range(5):
 for size in [1,7,17,31]:
  for fixture in range(2):
   pts=[]
   for j in range(size):
    coords=tuple((Q(rng.randrange(-3,4)),rng.randrange(-1,2)) for _ in range(d))
    pts.append((coords,j%2,j))
   expected={(r[2],b[2]) for r in pts for b in pts if r[1]==0 and b[1]==1 and all(r[0][j]<=b[0][j] for j in range(d))}
   got=list(dominance_pairs(pts,d));dominance_cases+=1
   ck(set(got)==expected);ck(len(got)==len(set(got)))
# Inclusive equal-coordinate dominance: all red-blue pairs must appear once.
pts=[(((Q(0),0),)*3,j%2,j) for j in range(26)]
got=list(dominance_pairs(pts,3));ck(len(got)==169);ck(len(set(got))==169)
# Exact sufficient inequality used in the recurrence bound.
ck(17**5<32*15**4)
for m in range(17,201):ck(Q((m+1)//2,m)<=Q(17,32))

root=Path(__file__).parent
r={'problem_id':3800014,'status':'PASS_EXACT_CORRECTNESS_CONTROLS','assertions':checks,
 'interval_implementation_runs':interval_cases,'generic_minplus_runs':convolution_cases,'dominance_instances':dominance_cases+1,
 'proof_sha256':hashlib.sha256((root/'KNOWN_ALGORITHM.md').read_bytes()).hexdigest(),
 'algorithm_sha256':hashlib.sha256((root/'algorithm.py').read_bytes()).hexdigest(),
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Exact small-instance correctness and tie/duplicate/witness tests. The real-RAM o(n^2) bound is proved analytically, not benchmarked; no bit-time or truly subquadratic claim.'}
print(json.dumps(r,indent=2,sort_keys=True))
