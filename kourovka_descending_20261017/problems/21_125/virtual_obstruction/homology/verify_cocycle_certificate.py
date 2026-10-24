#!/usr/bin/env python3
"""Standalone exact check; no Gaussian elimination or author homology routines."""
import argparse,collections,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);p.add_argument('--output',type=Path);args=p.parse_args()
d=json.loads(args.certificate.read_text());m=d['m'];q=d['fiber_cover_degree'];r=d['stable_letter_power'];A=d['permutations']
assert len(A)==m and all(sorted(a)==list(range(q)) for a in A)
reached={0};queue=collections.deque([0])
while queue:
 v=queue.popleft()
 for a in A:
  w=a[v]
  if w not in reached:reached.add(w);queue.append(w)
assert len(reached)==q
assert d['index']==q*r
# Apply the positive Nielsen substitution directly, independently of author modules.
images=[[i] for i in range(m)]
for t in range(r):
 new=[]
 for word in images:
  expanded=[]
  for x in word:
   expanded.append(x)
   if x:expanded.append(x-1)
  new.append(expanded)
 images=new
back=[]
for a in A:
 b=[0]*q
 for v,w in enumerate(a):b[w]=v
 back.append(b)
checks=0; character_by_id={}
for character in d['characters']:
 k=character['index'];alpha={tuple(map(int,key.split(','))):value for key,value in character['positive_edge_weights'].items()}; beta=character['vertex_potentials']
 assert len(beta)==q and all(isinstance(x,int) for x in beta)
 assert all(0<=v<q and 0<=i<m and isinstance(x,int) for (v,i),x in alpha.items())
 def positive_walk(word,start):
  v=start;value=0
  for i in word:value+=alpha.get((v,i),0);v=A[i][v]
  return v,value
 for v in range(q):
  for i in range(m):
   w=A[i][v];end,value=positive_walk(images[i],v)
   assert end==w
   assert value-alpha.get((v,i),0)==beta[w]-beta[v],('cell',k,v,i)
   checks+=1
 character_by_id[k]=alpha
results=[]
for target in d['targets']:
 assert target['visible']
 alpha=character_by_id[target['character_index']];v=0;value=0
 for _ in range(target['power_closing_in_fiber_cover']):
  for x in target['word']:
   if x>0:
    i=x-1;value+=alpha.get((v,i),0);v=A[i][v]
   else:
    i=-x-1;v=back[i][v];value-=alpha.get((v,i),0)
 assert v==0
 assert value==int(target['character_value']) and value!=0
 results.append({'word':target['label'],'power':target['power_closing_in_fiber_cover'],'value':value})
result={'result':'PASS','rank':m,'subgroup_index':q*r,'fiber_cover_vertices':q,'stable_letter_power':r,'integral_characters':len(d['characters']),'lifted_edge_cell_checks':checks,'targets':results,'scope':'Certifies explicit detecting homomorphisms, not virtual specialness or RFRS'}
if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
