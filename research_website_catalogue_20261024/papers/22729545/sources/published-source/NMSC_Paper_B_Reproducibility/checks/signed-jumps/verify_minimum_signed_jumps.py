#!/usr/bin/env python3
"""Exact supporting enumeration of minimum-core signed pair-jump signatures.

Nodes: NMSB-006, NMSB-007, NMSB-008. Scope is the twelve minimum repairs,
one sampled lineage at each repair/sink leaf, all relative leaf labels and
all retained biological event orders. This does not prove universal reduction.
Primitive arc lists are reproduced from Paper B, supplementary core table.
No Paper B generator/verifier helper is imported. Standard library only.
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
D=defaultdict(list); total=0
for core,(arcs,retics,repairs) in CORES.items():
 for repair in repairs:
  edges=[]
  for i,(v,w) in enumerate(arcs):
   if i in repair: edges += [(v,'A'+str(i)),('A'+str(i),w),('A'+str(i),'z'+str(i))]
   else: edges.append((v,w))
  sinks=[v for v in retics if all(a!=v for a,b in arcs)]
  edges +=[(v,'x'+v) for v in sinks]
  verts=set(sum(([a,b] for a,b in edges),[])); children={v:[b for a,b in edges if a==v] for v in verts}
  leaves=sorted(v for v in verts if not children[v]); internal=sorted(verts-set(leaves)); n=len(leaves)
  def desc(v):
   if not children[v]:return {v}
   return set.union(*(desc(w) for w in children[v]))
  Ds={v:desc(v) for v in verts}
  affected={}
  for v in internal:
   if v in retics: pairs=set(combinations(sorted(Ds[v]),2)); typ='R'
   else:
    aa,bb=children[v]; pairs={tuple(sorted((x,y))) for x in Ds[aa] for y in Ds[bb] if x!=y}; typ='T'
   if pairs:affected[v]=(typ,pairs)
  retained=sorted(affected)
  # A retained order extends some full topological order iff it respects ancestral reachability.
  def reaches(a,b):return b in children[a] or any(reaches(w,b) for w in children[a])
  constraints=[(a,b) for a in retained for b in retained if a!=b and reaches(a,b)]
  orders=[]
  for order in permutations(retained):
   rank={v:i for i,v in enumerate(order)} # backward youngest first
   if all(rank[a]>rank[b] for a,b in constraints):orders.append(order)
  for perm in permutations(range(n)):
   lab=dict(zip(leaves,perm))
   for order in orders:
    sig=tuple((affected[v][0],tuple(sorted(tuple(sorted((lab[x],lab[y]))) for x,y in affected[v][1]))) for v in order)
    rec={'core':core,'repair':repair,'order':order,'labels':lab,'edges':edges,'retics':retics}
    D[(n,sig)].append(rec);total+=1
cross=[v for v in D.values() if len({r['core'] for r in v})>1]
summary={'rows':total,'signature_classes':len(D),'cross_core_collision_classes':len(cross),'cross_core_types':dict(Counter(tuple(sorted(set(r['core'] for r in v))) for v in cross)),'max_class':max(map(len,D.values()))}
print(summary)
# Do not serialize tuple dictionary keys
with open(OUTPUT_DIR / 'minimum_signed_jump_summary.json','w') as f:json.dump({'summary':{**summary,'cross_core_types':str(summary['cross_core_types'])},'cross_core_collisions':cross[:20]},f,indent=2)
def iso(r,s):
 mapping=dict(zip(r['order'],s['order']))
 rev={v:k for k,v in s['labels'].items()}
 mapping.update({v:rev[i] for v,i in r['labels'].items()})
 rr=set(r['retics'])-mapping.keys(); ss=set(s['retics'])-set(mapping.values())
 if len(rr)!=len(ss):return False
 target=Counter(map(tuple,s['edges']))
 for dst in permutations(ss):
  mm={**mapping,**dict(zip(rr,dst))}
  if set(mm)!=set(sum(([a,b] for a,b in r['edges']),[])):raise ValueError('incomplete map')
  if Counter((mm[a],mm[b]) for a,b in r['edges'])==target:return True
 return False
noniso=[]
for (n,sig),rows in D.items():
 for r in rows[1:]:
  if not iso(rows[0],r):noniso.append((rows[0],r,sig))
print('nonisomorphic same-signature comparisons:',len(noniso),Counter(r['core'] for r,s,sig in noniso))
with open(OUTPUT_DIR / 'minimum_signed_jump_nonisomorphic_pairs.json','w') as f:json.dump(noniso,f,indent=2)

assert not cross, "minimum signed-jump cross-core collision"
assert all(r["core"] == "cycle" and len(r["labels"]) == 2 for r,_,_ in noniso), "non-cycle structural ambiguity"
