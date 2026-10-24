#!/usr/bin/env python3
"""Extract stored rank6 standard-generator witnesses into direct integer cells."""
from fractions import Fraction as Q
from pathlib import Path
import collections,json,math
root=Path(__file__).parent
f=json.loads((root/'character_search_rank6.json').read_text())['found']['result']
A=f['permutations'];m=f['m'];q=f['fiber_cover_degree'];r=f['stable_letter_power'];assert (m,q,r)==(6,128,16)
paths={0:[]};queue=collections.deque([0])
while queue:
 v=queue.popleft()
 for i,a in enumerate(A):
  w=a[v]
  if w not in paths:paths[w]=paths[v]+[i];queue.append(w)
tw=[[i] for i in range(m)]
for _ in range(r):tw=[[j for k in word for j in ([k] if k==0 else [k,k-1])] for word in tw]
chars=[];targets=[]
for witness in f['witnesses']:
 assert witness['visible'];index=witness['generator'];ell={int(k):Q(v) for k,v in witness['functional'].items()};scale=math.lcm(*(v.denominator for v in ell.values()));integral={k:int(scale*v) for k,v in ell.items()};divisor=math.gcd(*integral.values());integral={k:v//divisor for k,v in integral.items()};assert scale%divisor==0
 alpha={str(v)+','+str(i):integral.get(k,0) for k,(v,i) in enumerate(f['basis_edges']) if integral.get(k,0)}
 def walk(word,start=0):
  v=start;value=0
  for i in word:value+=alpha.get(str(v)+','+str(i),0);v=A[i][v]
  return v,value
 beta=[]
 for v in range(q):
  end,x=walk([j for i in paths[v] for j in tw[i]]);assert end==v
  end,y=walk(paths[v]);assert end==v
  beta.append(x-y)
 chars.append({'index':index,'positive_edge_weights':alpha,'vertex_potentials':beta})
 targets.append({'label':'a'+str(index),'word':[index],'power_closing_in_fiber_cover':witness['power'],'visible':True,'character_index':index,'character_value':str(scale//divisor)})
cert={'claim':'Rank6 explicit index2048 subgroup admits integer characters nonzero on powers of all standard generators; no RFRS or virtual specialness conclusion','m':m,'fiber_cover_degree':q,'stable_letter_power':r,'index':q*r,'permutations':A,'characters':chars,'targets':targets}
(root/'rank6_cocycle_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
