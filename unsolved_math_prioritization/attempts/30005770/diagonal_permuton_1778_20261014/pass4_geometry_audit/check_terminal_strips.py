#!/usr/bin/env python3
"""Independent finite check of terminal-strip containment under exact symmetries."""
from itertools import permutations,combinations
from collections import Counter
from pathlib import Path
import json
P=Path(__file__).resolve().parent

def av1324(p):return not any(p[a]<p[c]<p[b]<p[d] for a,b,c,d in combinations(range(len(p)),4))
def inv(p):
 q=[0]*len(p)
 for i,v in enumerate(p,1):q[v-1]=i
 return tuple(q)
def rc(p):return tuple(len(p)+1-v for v in p[::-1])
def std(p):
 p=tuple(p);r={v:i+1 for i,v in enumerate(sorted(p))};return tuple(r[v] for v in p)
def peel(p):
 n=len(p);rem=list(enumerate(p,1));cells=[]
 while rem:
  if len(cells)%2==0:
   cut=max((b[1] for a,b,c in combinations(rem,3) if b[1]<a[1]<c[1]),default=0)
   cell=[z for z in rem if z[1]>cut]
  else:
   cut=min((c[0] for a,b,c in combinations(rem,3) if a[1]<c[1]<b[1]),default=n+1)
   cell=[z for z in rem if z[0]<cut]
  if not cell:raise RuntimeError('empty peel')
  chosen=set(cell);rem=[z for z in rem if z not in chosen];cells.append(cell)
 return cells
rows=[]
for n in range(1,9):
 odd=even=0;images=Counter()
 for p in permutations(range(1,n+1)):
  if not av1324(p):continue
  cells=peel(p);r=len(cells);m=len(cells[-1])
  if r%2:
   odd+=1
   if sorted(i for i,v in cells[-1])!=list(range(n-m+1,n+1)):raise RuntimeError(('odd strip',p,cells))
   q=inv(p)
  else:
   even+=1
   if sorted(v for i,v in cells[-1])!=list(range(1,m+1)):raise RuntimeError(('even strip',p,cells))
   q=rc(p)
  if not av1324(q):raise RuntimeError('symmetry class mismatch')
  if len(peel(q)[0])<m:raise RuntimeError(('frontier containment',p,cells,q))
  raw=std(v for i,v in cells[-1]);A=raw if r%2 else rc(inv(raw))
  b=n-m;guard=(n+2,b+1,n+3)+tuple(v+(v>b) for v in q)
  if not av1324(guard):raise RuntimeError(('terminal guard avoidance',p,guard))
  first=peel(guard)[0];pattern=std(v for i,v in first)
  if pattern!=(m+1,m+2)+inv(A):raise RuntimeError(('terminal guard state',p,A,pattern))
  old=tuple(v-(v>b+1) for v in guard[3:])
  recover=inv(old) if r%2 else rc(old)
  if recover!=p:raise RuntimeError('terminal guard inverse')
  images[guard]+=1
 if max(images.values())>2:raise RuntimeError('terminal guard fiber')
 rows.append({'n':n,'odd_final_index':odd,'even_final_index':even,'all_avoiders_checked':odd+even,'terminal_guard_images':len(images),'maximum_guard_fiber':max(images.values())})
r={'scope':'Finite diagnostics only; strip and symmetry argument is all-size','all_checks_passed':True,'checks':rows}
(P/'TERMINAL_STRIP_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
