#!/usr/bin/env python3
"""Independent finite tests of canonical deletion and merge geometry."""
from itertools import permutations, combinations
from fractions import Fraction
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent

def std(p):
 d={v:i+1 for i,v in enumerate(sorted(p))}
 return tuple(d[v] for v in p)
def contains(p,q):
 return any(std(tuple(p[i] for i in inds))==q for inds in combinations(range(len(p)),len(q)))
def remaining(p):
 curr=len(p)+1;inds=[]
 for i,v in enumerate(p,1):
  if v<curr:curr=v
  else:inds.append(i)
 vals=sorted(p[i-1] for i in inds)
 return tuple(inds),tuple(vals),std(tuple(p[i-1] for i in inds))
def merge(n,S,V,q):
 p=[None]*n
 for r,i in enumerate(S):p[i-1]=V[q[r]-1]
 restpos=sorted(set(range(1,n+1))-set(S))
 restvals=sorted(set(range(1,n+1))-set(V),reverse=True)
 for i,v in zip(restpos,restvals):p[i-1]=v
 return tuple(p)
def score(p):
 n=len(p);return sum(abs(i+v-n-1) for i,v in enumerate(p,1))
def discrepancy_n(S,n):
 # n times the count discrepancy.
 S=set(S);m=len(S);h=0;ans=0
 for j in range(n+1):
  if j in S:h+=1
  ans=max(ans,abs(n*h-m*j))
 return ans

canonical=[]
for n in range(1,8):
 rows=[]
 for q in ((1,3,4,2),(1,2,4,5,3)):
  qplus=(1,)+tuple(v+1 for v in q)
  count=0
  for p in permutations(range(1,n+1)):
   S,V,r=remaining(p)
   if merge(n,S,V,r)!=p:raise RuntimeError(('canonical reconstruction',p))
   if contains(p,qplus)!=contains(r,q):raise RuntimeError(('deletion equivalence',q,p,r))
   if not contains(p,qplus):count+=1
  rows.append({'q':q,'qplus_avoider_count':count})
 canonical.append({'n':n,'classes':rows})

geometry=[]
for n in range(1,7):
 count=0
 for k in range(n+1):
  for S in combinations(range(1,n+1),k):
   for V in combinations(range(1,n+1),k):
    E=max(discrepancy_n(S,n),discrepancy_n(V,n))
    for q in permutations(range(1,k+1)):
     p=merge(n,S,V,q);count+=1
     if k==0:
      if score(p)!=0:raise RuntimeError('zero-core merge is not decreasing')
     elif k==n:
      if p!=q:raise RuntimeError('all-core merge differs from core')
     elif k*(score(p)-4*E-n)>n*score(q):
      raise RuntimeError(('merge cost inequality',n,S,V,q,p,E))
 geometry.append({'n':n,'all_merge_tuples_checked':count})

q=(2,3,1);p=(3,4,1,5,2);r=remaining(p)[2]
if contains(p,(1,3,4,2)) or not contains(r,q):raise RuntimeError('bad-hypothesis witness failed')
result={'purpose':'Finite regression checks only, not an asymptotic proof','canonical_deletion_checks':canonical,'merge_geometry_checks':geometry,'missing_starts_with_one_counterexample':{'p':p,'q':q,'remaining_standardization':r},'all_checks_passed':True}
(OUT/'MERGE_FINITE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
