#!/usr/bin/env python3
"""Exact local tables, finite-state obstruction, and credited PPP seam surgery."""
import itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'turn1'))
from surface_gluing import surface
from search_switches import local_options,finite,analyze
checks=0
def ck(x):
 global checks
 assert x;checks+=1

def gentle(r,p,q):
 return all(sum((a,b) in r for b in range(q))<=1 and sum((a,b) not in r for b in range(q))<=1 for a in range(p)) and all(sum((a,b) in r for a in range(p))<=1 and sum((a,b) not in r for a in range(p))<=1 for b in range(q))
tables=[]
for p,q in itertools.product(range(3),repeat=2):
 pairs=list(itertools.product(range(p),range(q)))
 for bits in itertools.product((0,1),repeat=len(pairs)):
  I={x for x,b in zip(pairs,bits) if b}
  if any(sum((a,b) not in I for b in range(q))>1 for a in range(p)) or any(sum((a,b) not in I for a in range(p))>1 for b in range(q)):continue
  opts=[]
  for sub in itertools.product((0,1),repeat=len(I)):
   J={x for x,b in zip(sorted(I),sub) if b}
   if gentle(J,p,q):opts.append(J)
  sat=[J for J in opts if not any(J<K for K in opts)]
  expected=2 if ((p,q) in [(1,2),(2,1),(2,2)] and len(I)==p*q) else 1
  ck(len(sat)==expected)
  ck(all(len(J)==len(sat[0]) for J in sat))
  tables.append({'in':p,'out':q,'I':sorted(I),'saturated':list(map(sorted,sat))})
# The smallest explicit finite-locus obstruction (not a minimality assertion).
a=[(0,1),(0,1),(1,0)];r=analyze(2,a)
ck(r['finite_count']==2);ck(len(r['components'])==2)
finite_paths=[]
for st in [(0,1),(1,0)]:
 tr=set().union(*(set(map(tuple,r['options'][v][i])) for v,i in enumerate(st)))
 ck(finite(tr));ck(len(tr)==2)
 nxt=dict(tr);starts=set(range(3))-set(nxt.values()); paths=[]
 for s in starts:
  path=[s]
  while path[-1] in nxt:path.append(nxt[path[-1]])
  paths.append(path)
 ck(len(paths)==1 and len(paths[0])==3)
 finite_paths.append(paths[0])
ck({tuple(p) for p in finite_paths}=={(0,2,1),(1,2,0)})
for st in [(0,0),(1,1)]:
 tr=set().union(*(set(map(tuple,r['options'][v][i])) for v,i in enumerate(st)))
 ck(not finite(tr))
# Independent bounded-walk cycle criterion over all simple directed quivers <=3 vertices.
quivers=states=0
for n in range(1,4):
 pairs=list(itertools.product(range(n),repeat=2))
 for mask in range(1<<len(pairs)):
  arr=[x for i,x in enumerate(pairs) if mask>>i&1]
  opts=local_options(n,arr)
  if opts is None:continue
  quivers+=1;m=len(arr)
  for st in itertools.product(*[range(len(o)) for o in opts]):
   tr=set().union(*(opts[v][i] for v,i in enumerate(st))); states+=1
   live=set(range(m))
   for _ in range(m):live={b for a,b in tr if a in live}
   ck(finite(tr)==(not live))
# Full turn1 four-vertex witness and four-seam regluing.
arr=[(0,1),(0,2),(1,2),(1,3),(2,3)]
r0={(0,2),(1,4)};r1={(0,2),(2,4)}
s0=surface(4,arr,r0);s1=surface(4,arr,r1)
ck((s0['genus'],s0['boundaries'])==(0,3));ck((s1['genus'],s1['boundaries'])==(1,1));ck(s0['Euler_characteristic']==s1['Euler_characteristic']==-1)
# In the deterministic blossoming order, outgoing blossom at vertex2 is arrow8.
def seams(rel):
 return [{'incoming':a,'outgoing':b,'color':'red' if (a,b) in rel else 'green','incoming_side':2 if (a,b) in rel else 1,'outgoing_side':3 if (a,b) in rel else 0} for a,b in itertools.product([1,2],[4,8])]
x0={(1,4),(2,8)};x1={(2,4),(1,8)}
old=seams(x0);new=seams(x1)
ck(all(a['color']!=b['color'] for a,b in zip(old,new)))
ck(len({(x['incoming'],x['incoming_side']) for x in old})==4)
ck(len({(x['outgoing'],x['outgoing_side']) for x in old})==4)
ck({(x['incoming'],x['incoming_side']) for x in old}=={(x['incoming'],x['incoming_side']) for x in new})
ck({(x['outgoing'],x['outgoing_side']) for x in old}=={(x['outgoing'],x['outgoing_side']) for x in new})
print(json.dumps({'assertions':checks,'local_tables':tables,'cycle_checks':{'quivers':quivers,'states':states},'disconnected_finite_locus':r,'finite_maximal_arrow_paths':finite_paths,'four_seam_surgery':{'old':old,'new':new,'old_surface':s0,'new_surface':s1},'scope':'Combinatorial surgery is explicit; equivalence to the OWR tile rotations is not established.'},indent=2))
