#!/usr/bin/env python3
"""Independent diagnostics for the complementary reviewer's two-point padding."""
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
rows=[]
for n in range(1,8):
 raw=single=0;rawstates=set();singlestates=set();images=set()
 for p in permutations(range(1,n+1)):
  if not av1324(p):continue
  for m in range(n):
   A=tuple(v-m for v in p if v>m);B=tuple(v for v in p if v<=m)
   if not(av213(A) and av132(B)):continue
   C=S(B)
   q=(m+2,m+1)+tuple(v+2 if v>m else v for v in p)
   if not av1324(q):raise RuntimeError(('new forbidden occurrence',p,m,q))
   AA=tuple(v-m-1 for v in q if v>m+1)
   BB=tuple(v for v in q if v<=m+1);CC=S(BB)
   if AA!=(1,)+tuple(v+1 for v in A) or CC!=(m+1,)+C:raise RuntimeError('state mismatch')
   if not av213(AA) or not av132(BB):raise RuntimeError('cell class mismatch')
   if not (q[1]<q[0] and any(v>q[0] for v in q[2:])):raise RuntimeError('missing greedy witness')
   if tuple(v-2 if v>m+1 else v for v in q[2:])!=p:raise RuntimeError('inverse mismatch')
   key=(AA,CC,q)
   if key in images:raise RuntimeError('image collision')
   images.add(key)
   if m:raw+=1;rawstates.add((AA,CC))
   else:single+=1;singlestates.add((AA,CC))
 if rawstates & singlestates:raise RuntimeError('single-cell overlap')
 rows.append({'n':n,'raw_nonempty_pairs_checked':raw,'single_cell_images_checked':single,'images_distinct':len(images)})
result={'scope':'Finite diagnostics only; all-size proof independently reviewed','all_checks_passed':True,'checks':rows}
(P/'TWO_POINT_PADDING_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
