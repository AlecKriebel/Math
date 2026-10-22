#!/usr/bin/env python3
"""Independent permitted-thread ribbon calculation for the fixed finite witness."""
import json
arrows=[(0,1),(0,2),(1,2),(1,3),(2,3)]
def compute(rel):
 nxt={a:b for a,(u,v) in enumerate(arrows) for b,(w,z) in enumerate(arrows) if v==w and (a,b) not in rel}
 prev={b:a for a,b in nxt.items()};threads=[]
 for a in range(len(arrows)):
  if a in prev:continue
  verts=[arrows[a][0]];path=[]
  while True:
   path.append(a);verts.append(arrows[a][1])
   if a not in nxt:break
   a=nxt[a]
  threads.append({'arrows':path,'vertices':verts})
 occurrences={v:[] for v in range(4)};sigma={};cursor=0
 for thread in threads:
  ds=list(range(cursor,cursor+len(thread['vertices'])));cursor+=len(ds);thread['darts']=ds
  for j,v in enumerate(thread['vertices']):occurrences[v].append(ds[j]);sigma[ds[j]]=ds[(j+1)%len(ds)]
 assert all(len(x)==2 for x in occurrences.values())
 alpha={}
 for a,b in occurrences.values():alpha[a]=b;alpha[b]=a
 phi={i:sigma[alpha[i]] for i in sigma};todo=set(phi);cycles=[]
 while todo:
  start=min(todo);q=start;cy=[]
  while q in todo:cy.append(q);todo.remove(q);q=phi[q]
  assert q==start;cycles.append(cy)
 chi=len(threads)-4;b=len(cycles);g=(2-b-chi)//2
 assert 2-2*g-b==chi
 return {'relations':sorted(rel),'threads':threads,'sigma':[sigma[i] for i in range(cursor)],'alpha':[alpha[i] for i in range(cursor)],'boundary_permutation':[phi[i] for i in range(cursor)],'boundary_cycles':cycles,'ribbon_vertices':len(threads),'ribbon_edges':4,'Euler_characteristic':chi,'boundary_components':b,'genus':g}
out={'arrows':arrows,'string_relations':[(0,2),(0,3),(1,4),(2,4)],'covers':[compute({(0,2),(1,4)}),compute({(0,2),(2,4)})]}
print(json.dumps(out,indent=2))
