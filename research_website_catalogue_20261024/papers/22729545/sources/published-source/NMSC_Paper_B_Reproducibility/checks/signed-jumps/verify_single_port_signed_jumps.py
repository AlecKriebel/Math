#!/usr/bin/env python3
"""Exact one-additional-port supporting check; not a universal theorem.

Nodes: NMSB-006, NMSB-011, NMSB-008. For every minimum repair, insert one
new ordinary side port on each primitive segment, including above/below an
existing repair port. Fix all base labels and enumerate every retained-event
order. Compare explicit label/time-preserving directed multigraph bijections.
No project generator/verifier helper is imported. Standard library only.
"""
if not __debug__:
    raise SystemExit("Verification requires assertions; optimized Python is unsupported.")

from pathlib import Path
OUTPUT_DIR = Path(__file__).resolve().parent
from itertools import permutations, combinations
from collections import defaultdict, Counter
import json
CORES={
'cycle':([('S','X'),('S','X')],['X'],[(0,),(1,)]),
'θ0':([('S','U'),('S','V'),('U','X'),('V','X'),('U','V')],['V','X'],[(2,3),(3,4)]),
'θ1':([('S','U'),('S','X'),('V','X'),('U','V'),('U','V')],['V','X'],[(2,3),(2,4)]),
'θ2':([('S','U'),('S','V'),('U','X0'),('V','X0'),('U','X1'),('V','X1')],['X0','X1'],[(2,3),(2,5),(3,4),(4,5)]),
'θ3':([('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V')],['X0','X1'],[(2,),(4,)])}
def sigs(edges,retics):
 vs=set(sum(([a,b] for a,b in edges),[]));ch={v:[b for a,b in edges if a==v] for v in vs}; leaves=sorted(v for v in vs if not ch[v])
 cache={}
 def desc(v):
  if v not in cache:cache[v]={v} if not ch[v] else set.union(*(desc(w) for w in ch[v]))
  return cache[v]
 af={}
 for v in vs-set(leaves):
  if v in retics:typ='R'; pairs=set(combinations(sorted(desc(v)),2))
  else:
   assert len(ch[v])==2,(v,ch[v]);a,b=ch[v];typ='T';pairs={tuple(sorted((x,y))) for x in desc(a) for y in desc(b) if x!=y}
  if pairs:af[v]=(typ,tuple(sorted(pairs)))
 def reach(a,b):return b in ch[a] or any(reach(w,b) for w in ch[a])
 prereq={a:{b for b in af if b!=a and reach(a,b)} for a in af}
 def visit(order,rem):
  if not rem:
   yield tuple(af[v] for v in order),tuple(order);return
  for v in sorted(rem):
   if not prereq[v]&rem:yield from visit(order+[v],rem-{v})
 yield from visit([],set(af))
def iso(r,s):
 mp=dict(zip(r['order'],s['order']));mp.update({x:x for x in r['leaves']});a=set(r['retics'])-mp.keys();b=set(s['retics'])-set(mp.values());target=Counter(map(tuple,s['edges']))
 if len(a)!=len(b):return False
 for perm in permutations(b):
  mm={**mp,**dict(zip(a,perm))}
  if len(mm)!=len(set(sum(([v,w] for v,w in r['edges']),[]))):raise ValueError('incomplete')
  if Counter((mm[v],mm[w]) for v,w in r['edges'])==target:return True
 return False
allsummary=[];attacks=[];total=0
for core,(arcs,retics,repairs) in CORES.items():
 for repair in repairs:
  base=[];eligible=[]
  for i,(v,w) in enumerate(arcs):
   if i in repair:
    base += [(v,'A'+str(i)),('A'+str(i),w),('A'+str(i),'z'+str(i))]
    eligible +=[(i,'above',(v,'A'+str(i))),(i,'below',('A'+str(i),w))]
   else:base.append((v,w));eligible.append((i,'whole',(v,w)))
  sinks=[v for v in retics if all(a!=v for a,b in arcs)];base +=[(v,'x'+v) for v in sinks]
  D=defaultdict(list)
  for seg,side,edge in eligible:
   es=base.copy();es.remove(edge);v,w=edge;es +=[(v,'P'),('P',w),('P','probe')]
   leaves=sorted(set(b for a,b in es)-set(a for a,b in es))
   for sig,order in sigs(es,retics):
    rec={'core':core,'repair':repair,'placement':[seg,side], 'edges':es,'retics':retics,'leaves':leaves,'order':order};D[sig].append(rec);total+=1
  bad=[]
  for sig,rs in D.items():
   for r in rs[1:]:
    if not iso(rs[0],r):bad.append((rs[0],r,sig))
  attacks+=bad
  row={'core':core,'repair':repair,'placements':len(eligible),'ranked_rows':sum(map(len,D.values())),'signature_classes':len(D),'nonisomorphic_collisions':len(bad)};allsummary.append(row);print(row,flush=True)
print('TOTAL',total,'NONISO',len(attacks))
with open(OUTPUT_DIR / 'single_port_signed_jump_results.json','w') as f:json.dump({'scope':'one additional ordinary side port on a primitive core segment, including above/below each selected repair; fixed labelled minimum base; every retained-event topological order; only strict positive sign data','rows':allsummary,'total':total,'nonisomorphic_collisions':attacks},f,indent=2)

assert not attacks, "single-port signed-jump insertion ambiguity"
