#!/usr/bin/env python3
"""Independent finite diagnostics for the two-collapse and three-point guard maps."""
from itertools import permutations,combinations
from collections import Counter
from pathlib import Path
import json
P=Path(__file__).resolve().parent

def std(p):
 p=tuple(p);rank={v:i+1 for i,v in enumerate(sorted(p))};return tuple(rank[v] for v in p)
def S(p):
 n=len(p);inv=[0]*n
 for i,v in enumerate(p,1):inv[v-1]=i
 return tuple(n+1-v for v in inv[::-1])
def av1324(p):return not any(p[a]<p[c]<p[b]<p[d] for a,b,c,d in combinations(range(len(p)),4))
def av213(p):return not any(p[b]<p[a]<p[c] for a,b,c in combinations(range(len(p)),3))
def av132(p):return not any(p[a]<p[c]<p[b] for a,b,c in combinations(range(len(p)),3))
def peel(p):
 rem=list(enumerate(p));cells=[]
 while rem:
  if len(cells)%2==0:
   cut=max((b[1] for a,b,c in combinations(rem,3) if b[1]<a[1]<c[1]),default=0)
   cell=[z for z in rem if z[1]>cut]
  else:
   cut=min((c[0] for a,b,c in combinations(rem,3) if a[1]<c[1]<b[1]),default=len(p))
   cell=[z for z in rem if z[0]<cut]
  cs=set(cell);assert cell;rem=[z for z in rem if z not in cs];cells.append(cell)
 return cells

def collapses(p):
 n=len(p);cells=peel(p);oddpos={i for j,c in enumerate(cells) if j%2==0 for i,v in c}
 O=[p[i] for i in range(n) if i in oddpos];E=[p[i] for i in range(n) if i not in oddpos]
 A=std(O);B=std(E);C=S(B);a=len(A);b=len(B)
 assert av213(A) and av213(C) and av132(B)
 rO={v:i+1 for i,v in enumerate(sorted(O))};rE={v:i+1 for i,v in enumerate(sorted(E))}
 V=tuple(b+rO[v] if i in oddpos else rE[v] for i,v in enumerate(p))
 H=tuple(E+O);W=S(H)
 assert av1324(V) and av1324(W),(p,cells,V,W)
 assert std(v for v in V if v>b)==A and std(v for v in V if v<=b)==S(C)
 assert std(v for v in W if v>a)==C and std(v for v in W if v<=a)==S(A)
 # W's position color word records original values in decreasing order.
 odd_values=[v for v,entry in enumerate(W[::-1],1) if entry<=a]
 even_values=[v for v,entry in enumerate(W[::-1],1) if entry>a]
 out=[];io=ie=0
 for value in V:
  if value>b:out.append(odd_values[A[io]-1]);io+=1
  else:out.append(even_values[B[ie]-1]);ie+=1
 assert tuple(out)==p,(p,V,W,out)
 return A,C,V,W

collapse_counts=[]
for n in range(9):
 seen=set();count=0
 for p in permutations(range(1,n+1)):
  if not av1324(p):continue
  key=collapses(p);assert key not in seen;seen.add(key);count+=1
 collapse_counts.append({'n':n,'avoiders_checked':count})

# All unrestricted dominoes of total size at most 7, including empty colors.
guard_counts=[]
for n in range(8):
 D=Counter();images=set();symmetric_images=set();count=0
 for p in permutations(range(1,n+1)):
  if not av1324(p):continue
  for b in range(n+1):
   A=tuple(v-b for v in p if v>b);B=tuple(v for v in p if v<=b)
   if not(av213(A) and av132(B)):continue
   C=S(B);D[A,C]+=1;count+=1
   gp=(n+2,b+1,n+3)+tuple(v if v<=b else v+1 for v in p)
   assert av1324(gp),(p,b,gp)
   AA=tuple(v-(b+1) for v in gp if v>b+1)
   BB=tuple(v for v in gp if v<=b+1)
   CC=S(BB)
   expectA=(len(A)+1,len(A)+2)+A
   expectC=(len(C)+1,)+C
   assert AA==expectA and CC==expectC
   assert av213(AA) and av132(BB)
   maxlow=gp.index(b+1)
   assert any(gp[i]<gp[j] for i in range(maxlow) for j in range(maxlow+1,len(gp)) if gp[i]>b+1 and gp[j]>b+1)
   key=(AA,CC,gp);assert key not in images;images.add(key)
   recovered=tuple(v if v<=b else v-1 for v in gp[3:]);assert recovered==p
   sp=(n+3,b+1,b+2,n+4)+tuple(v if v<=b else v+2 for v in p)
   assert av1324(sp),(p,b,sp)
   SA=tuple(v-(b+2) for v in sp if v>b+2)
   SB=tuple(v for v in sp if v<=b+2);SC=S(SB)
   assert SA==(len(A)+1,len(A)+2)+A
   assert SC==(len(C)+1,len(C)+2)+C
   assert av213(SA) and av132(SB)
   assert sp[0]<sp[3] and sp[0]>b+2 and sp[2]==b+2
   skey=(SA,SC,sp);assert skey not in symmetric_images;symmetric_images.add(skey)
   assert tuple(v if v<=b else v-2 for v in sp[4:])==p
 cross=sum(v*D[C,A] for (A,C),v in D.items())
 square=sum(v*v for v in D.values())
 assert cross<=square
 assert collapse_counts[n]['avoiders_checked']<=cross
 guard_counts.append({'n':n,'unrestricted_dominoes_checked':count,'sum_D_AC_D_CA':cross,'sum_D_squared':square,'three_point_guard_images_distinct':len(images),'symmetric_guard_images_distinct':len(symmetric_images)})
result={'scope':'Finite diagnostics, not an exponential-growth proof','all_checks_passed':True,'collapse_and_reconstruction':collapse_counts,'guard_and_Cauchy_Schwarz':guard_counts}
(P/'DOMINO_OBSTRUCTION_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
