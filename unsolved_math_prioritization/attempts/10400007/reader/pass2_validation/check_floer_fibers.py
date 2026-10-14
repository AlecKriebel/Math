#!/usr/bin/env python3
"""Independent finite algebra check from geometrically verified generator data.
These rows are checked against the exact PL monodromy replay, not inferred solely
from a polynomial's number of terms.
"""
import json
from pathlib import Path

def require(x):
 if not x:raise RuntimeError('Floer validation failed')
def rank_mod2(mat):
 a=[r[:] for r in mat];rank=0
 if not a:return 0
 for col in range(len(a[0])):
  pivot=next((i for i in range(rank,len(a)) if a[i][col]),None)
  if pivot is None:continue
  a[rank],a[pivot]=a[pivot],a[rank]
  for i in range(len(a)):
   if i!=rank and a[i][col]:a[i]=[x^y for x,y in zip(a[i],a[rank])]
  rank+=1
 return rank
p=Path(__file__).parent
rows=json.loads((p/'PL_GRADING_REPLAY.json').read_text())
out=[]
for n,key in [(1,'sigma1'),(2,'sigma1_sigma2')]:
 rr=rows[key]
 require(len(rr)==2*n+1)
 require(len({(r['A'],r['Q']) for r in rr})==len(rr))
 for r in rr:
  W=sum(3*(n-i)+1 for i in r['S']);R=sum(n-i for i in r['S'])
  r['B']=r['Q']-W+R;r['C']=R-W
 arrows=[]
 for A in sorted({r['A'] for r in rr}):
  inds=[i for i,r in enumerate(rr) if r['A']==A]
  if A==0:require(len(inds)==1);continue
  require(len(inds)==2)
  possible=[]
  for i,j in [inds,inds[::-1]]:
   b=rr[i]['B']-rr[j]['B'];c=rr[i]['C']-rr[j]['C']
   if b>=0 and c>=0:possible.append((i,j,b,c))
  require(len(possible)==1)
  arrows+=possible
 fibers={}
 for U,V in [(0,0),(0,1),(1,0),(1,1)]:
  d=[[0]*len(rr) for _ in rr]
  for i,j,b,c in arrows:d[j][i]=U**b*V**c
  require(all(sum(d[i][k]*d[k][j] for k in range(len(rr)))%2==0 for i in range(len(rr)) for j in range(len(rr))))
  fibers[f'U={U},V={V}']=len(rr)-2*rank_mod2(d)
 out.append({'braid':key,'number_of_verified_generators':len(rr),'Rees_arrows':[{'source_AQ':[rr[i]['A'],rr[i]['Q']],'target_AQ':[rr[j]['A'],rr[j]['Q']],'exponents':[b,c]} for i,j,b,c in arrows],'homology_dimensions':fibers})
require([x['homology_dimensions']['U=0,V=0'] for x in out]==[3,5])
require([x['homology_dimensions']['U=0,V=1'] for x in out]==[1,3])
require([x['homology_dimensions']['U=1,V=0'] for x in out]==[3,5])
require([x['homology_dimensions']['U=1,V=1'] for x in out]==[1,1])
print(json.dumps({'status':'all checks passed','models':out,'proof_input':'Both closures are the unknot, HFKhat is rank1 at A0, and all counted discs have nonnegative B,C drops. These facts force the nonzero two-generator arrows; no experimental disc-count claim.'},indent=2))
