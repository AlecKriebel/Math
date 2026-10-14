#!/usr/bin/env python3
"""Independent finite regression for canonical staircase geometry."""
from itertools import permutations, combinations
from pathlib import Path
import json
P=Path(__file__).resolve().parent

def avoids1324(p):
 return not any(p[a]<p[c]<p[b]<p[d] for a,b,c,d in combinations(range(len(p)),4))

def peel(p):
 n=len(p);full=list(enumerate(p,1));rem=full[:];cells=[];column=1;row=n
 while rem:
  odd=len(cells)%2==0
  source_slice=[z for z in full if (z[0]>=column if odd else z[1]<=row)]
  if source_slice!=rem:raise RuntimeError(('global-source/remainder mismatch',p,cells,source_slice,rem))
  if odd:
   witnesses=[b[1] for a,b,c in combinations(rem,3) if b[1]<a[1]<c[1]]
   cut=max(witnesses,default=0)
   cell=[z for z in rem if z[1]>cut];row=cut
  else:
   witnesses=[c[0] for a,b,c in combinations(rem,3) if a[1]<c[1]<b[1]]
   cut=min(witnesses,default=n+1)
   cell=[z for z in rem if z[0]<cut];column=cut
  if not cell:raise RuntimeError('empty nonfinal peel')
  cs=set(cell);rem=[z for z in rem if z not in cs];cells.append(cell)
 return cells

def skew(*ps):
 total=sum(map(len,ps));out=[]
 for p in ps:
  total-=len(p);out.extend(v+total for v in p)
 return tuple(out)

checks=[]
for n in range(1,8):
 count=0
 for p in permutations(range(1,n+1)):
  if not avoids1324(p):continue
  count+=1;cells=peel(p);sizes=list(map(len,cells));M=max(sizes)
  for j,cell in enumerate(cells):
   q=sum(sizes[max(0,j-1):j+2])
   for i,v in cell:
    if abs(i+v-n-1)>q-1:raise RuntimeError(('point geometry',p,sizes,j,i,v))
   for later in cells[j+2:]:
    if any(not(a[0]<b[0] and a[1]>b[1]) for a in cell for b in later):
     raise RuntimeError(('nonadjacent order',p,cells))
 checks.append({'n':n,'all_1324_avoiders_checked':count})

examples=[];G=(2,4,1,3)
for r in range(1,6):
 for N in range(1,21):
  p=skew(*([G]*r+[tuple(range(1,N+1))]+[G]*r))
  sizes=list(map(len,peel(p)))
  expected=[3]+[4]*(r-1)+[N+4]+[4]*(r-1)+[1]
  if sizes!=expected:raise RuntimeError(('escape cell sizes',r,N,sizes,expected))
  if any(p[i-1]!=i for i in range(4*r+1,4*r+N+1)):
   raise RuntimeError('central identity is not fixed pointwise')
  examples.append({'r':r,'N':N,'cell_sizes':sizes})
result={'scope':'Finite regression only; asymptotic conclusions use written proof','canonical_geometry_checks':checks,'escape_examples_checked':len(examples),'example_parameters':{'r':[1,5],'N':[1,20]},'all_checks_passed':True}
(P/'STAIRCASE_FINITE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
