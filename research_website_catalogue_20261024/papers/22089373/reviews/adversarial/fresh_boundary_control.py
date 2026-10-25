#!/usr/bin/env python3
"""Fresh exact boundary controls on one literal minimal theta0 STC support."""
from fresh_graph_library import tensor_terms,value_grad,F,sp,product
from pathlib import Path
import json
from datetime import datetime,timezone
edges=[('R','S'),('R','IN'),('S','U'),('S','V'),('U','P2'),('P2','X'),('P2','L2'),('V','P3'),('P3','X'),('P3','L3'),('U','V'),('X','L4')]
labels={'IN':0,'L2':1,'L3':2,'L4':3}
rets,terms=tensor_terms(edges,labels)
def flatten(params,lam,pair):
 other=[i for i in range(4) if i not in pair];rows=[]
 for a in product(range(4),repeat=2):
  row=[]
  for b in product(range(4),repeat=2):
   g=[0]*4
   for i,x in zip(pair,a):g[i]=x
   for i,x in zip(other,b):g[i]=x
   row.append(0 if g[0]^g[1]^g[2]^g[3] else value_grad(terms,g,params,lam)[0])
  rows.append(row)
 return sp.Matrix(rows)
strict=[flatten([F(1,2)]*len(edges),[F(1,2)]*2,p).rank() for p in [(0,1),(0,2),(0,3)]]
boundary=[flatten([F(1)]*len(edges),[F(1,2)]*2,p).rank() for p in [(0,1),(0,2),(0,3)]]
assert all(r>4 for r in strict) and boundary==[4,4,4]
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','graph_edges':edges,'leaf_positions':labels,'splits':[[0,1],[0,2],[0,3]],'strict_half_point_ranks':strict,'excluded_x_equals_one_boundary_ranks':boundary,'scope':'One explicit nontrivial strong blob has no two-versus-two bridge cut. All three strict-point ranks exceed four, but all collapse to four at excluded x=1. This demonstrates why strict-domain hypotheses cannot be silently dropped; it is not a universal pointwise-cut proof.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','strict':strict,'excluded_boundary':boundary}))
