#!/usr/bin/env python3
"""Own figure4 transcription, fixed-order search using BFS constraints."""
from itertools import combinations
from pathlib import Path
import json
from independent_review import distance,valid,require
V=('x','u0','l0','u3','l3','y','u1','l1','u2','l2')
E=(('x','u0'),('x','l0'),('u0','l0'),('u0','u1'),('u1','u2'),('u2','u3'),('l0','l1'),('l1','l2'),('l2','l3'),('u3','l3'),('u3','y'),('l3','y'))
A=tuple(range(1,6));C=(1,2,4,5,6);L={v:C if v=='x' else A for v in V}
F={'x':3,'u0':1,'u1':4,'u2':2,'u3':5,'l0':5,'l1':2,'l2':4,'l3':1,'y':3}
def search(edges,lists):
 _,d=distance(V,edges);f={}
 def rec(i):
  if i==len(V):return dict(f)
  v=V[i]
  for x in lists[v]:
   if all(d[v][w]>2 or abs(x-y)>=(2 if d[v][w]==1 else 1) for w,y in f.items()):
    f[v]=x;r=rec(i+1)
    if r is not None:return r
    del f[v]
  return None
 return rec(0)
require(valid(V,E,{v:A for v in V},F),'figure ordinary witness')
require(search(E,L) is None,'figure bad5')
require(search(E,{v:(1,2,3,4) for v in V}) is None,'figure ordinary lower4')
spans=[]
for es in combinations(E,9):
 if len(distance(V,es)[1]['x'])<10:continue
 f=search(es,L);require(f is not None and valid(V,es,L,f),'inherited tree unexpectedly bad');spans.append({'edges':es,'witness':f})
require(len(spans)==66,'spanning tree count')
Path('FIALA_CHECKS.json').write_text(json.dumps({'input':'own visual transcription of primary2001 Fig4, printed14','vertices':V,'edges':E,'lists':L,'witness':F,'ordinary_exact_palette':5,'bad_five_lists_infeasible':True,'cycle_rank':3,'spanning_trees':spans,'scope':'Only inherited-list deletion transfer excluded; no general priority clearance.'},indent=2)+'\n')
print('PASS: figure ordinary5, bad5, 66 inherited-list spanning trees feasible.')
