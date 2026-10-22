#!/usr/bin/env python3
"""Independent local checks for the rerooting bridge and incoming-edge lift."""
from pathlib import Path
from itertools import permutations,combinations
import json
P=Path(__file__).resolve().parent

def av1324(p):return not any(p[a]<p[c]<p[b]<p[d] for a,b,c,d in combinations(range(len(p)),4))
def av213(p):return not any(p[b]<p[a]<p[c] for a,b,c in combinations(range(len(p)),3))
def av132(p):return not any(p[a]<p[c]<p[b] for a,b,c in combinations(range(len(p)),3))
def S(p):
 n=len(p);inv=[0]*n
 for i,v in enumerate(p,1):inv[v-1]=i
 return tuple(n+1-v for v in inv[::-1])
def I(p):
 v=p[0];return (v,v+1)+tuple(x+(x>v) for x in p[1:])
def greedy(p,b):
 j=p.index(b)
 return any(p[i]<p[k] for i in range(j) for k in range(j+1,len(p)) if p[i]>b and p[k]>b)
states={n:[p for p in permutations(range(1,n+1)) if av213(p)] for n in range(1,8)}
bridge=inflate=lift=0
for n in states:
 for A in states[n]:
  AA=I(A)
  if not av213(AA):raise RuntimeError(('inflation class',A))
  B=S(A);m=len(B);idx=B.index(m)
  BB=B[:idx]+(m,m+1)+B[idx+1:]
  if S(AA)!=BB:raise RuntimeError(('reflection inflation',A))
  inflate+=1
for a in range(2,7):
 for b in range(1,8-a):
  for A in states[a]:
   asc=next(((i,j) for i,j in combinations(range(a),2) if A[i]<A[j]),None)
   if asc is None:continue
   for C in states[b]:
    B=S(C);k=B.index(b);L=B[:k];R=B[k+1:]
    if any(x<y for x in L for y in R):raise RuntimeError('132 max split')
    i,j=asc;upper=tuple(x+b for x in A)
    p=upper[:i+1]+L+(b,)+upper[i+1:]+R
    if not av1324(p) or not greedy(p,b):raise RuntimeError(('bridge',A,C,p))
    bridge+=1
for n in range(2,8):
 for p in permutations(range(1,n+1)):
  if not av1324(p):continue
  for b in range(1,n):
   A=tuple(v-b for v in p if v>b);B=tuple(v for v in p if v<=b)
   if not av213(A) or not av132(B) or not greedy(p,b):continue
   C=S(B);j=p.index(b);q=tuple(v+(v>b) for v in p[:j])+(b,b+1)+tuple(v+(v>b) for v in p[j+1:])
   if not av1324(q) or not greedy(q,b+1):raise RuntimeError(('incoming lift',p,b,q))
   AA=tuple(v-b-1 for v in q if v>b+1);CC=S(tuple(v for v in q if v<=b+1))
   if AA!=A or CC!=I(C):raise RuntimeError('incoming state mismatch')
   recovered=tuple(v-(v>b+1) for t,v in enumerate(q) if t!=j+1)
   if recovered!=p:raise RuntimeError('incoming inverse')
   lift+=1
result={'scope':'Local finite diagnostics only; global rerooting proof separately reviewed','all_checks_passed':True,'first_entry_inflations_through_size_7':inflate,'deterministic_bridges_through_total_size_7':bridge,'all_greedy_incoming_shuffles_through_total_size_7':lift}
(P/'ROTATION_LOCAL_MAP_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
