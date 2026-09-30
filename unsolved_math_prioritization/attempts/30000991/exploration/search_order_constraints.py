from itertools import combinations,permutations
import random,json,time
from pathlib import Path
rng=random.Random(30000991)
def closure(maxs):return sorted({t for s in maxs for k in range(1,len(s)+1) for t in combinations(s,k)},key=lambda s:(len(s),s))
def pairing(V,order):
 pos={v:i for i,v in enumerate(order)};piv={};pairs=[]
 for cell in order:
  c={face for face in combinations(cell,len(cell)-1)} if len(cell)>1 else set()
  while c:
   p=max(c,key=pos.get)
   if p not in piv:break
   c^=piv[p]
  if c:piv[p]=c;pairs.append((p,cell))
 return tuple(pairs)
def solve(V,P,cap=12000):
 n=len(V);idx={v:i for i,v in enumerate(V)};target={t:s for s,t in P};pairs={frozenset((s,t)) for s,t in P};pre={v:set() for v in V}
 for t in V:
  if len(t)>1:pre[t].update(combinations(t,len(t)-1))
 for s,t in P:
  if set(s)<set(t):
   for face in combinations(t,len(t)-1):
    if face!=s:pre[s].add(face)
   for co in V:
    if len(co)==len(s)+1 and set(s)<set(co) and co!=t:pre[co].add(t)
 nodes=0;cut=False
 def rec(order,remaining,piv):
  nonlocal nodes,cut
  nodes+=1
  if nodes>cap:cut=True;return None
  if not remaining:return order
  pos={v:i for i,v in enumerate(order)}
  for cell in sorted(remaining,key=lambda x:(len(x),x)):
   if pre[cell]&remaining:continue
   c={face for face in combinations(cell,len(cell)-1)} if len(cell)>1 else set()
   while c:
    p=max(c,key=pos.get)
    if p not in piv:break
    c^=piv[p]
   if c:
    if target.get(cell)!=p:continue
    nxt=dict(piv);nxt[p]=c
   else:
    if cell in target:continue
    nxt=piv
   result=rec(order+[cell],remaining-{cell},nxt)
   if result is not None:return result
   if cut:return None
  return None
 result=rec([],set(V),{})
 return result,nodes,cut
out=[];seen=set();total=0
for maxs in [[(0,1,2),(1,2,3)],[(0,1,2),(0,2,3)],[(0,1,2),(0,1,3),(0,2,3)],[(0,1,2),(1,2,3),(2,3,4)]]:
 V=closure(maxs)
 for it in range(60):
  order=[];rem=set(V)
  while rem:
   avail=[v for v in rem if len(v)==1 or all(f in order for f in combinations(v,len(v)-1))]
   v=rng.choice(sorted(avail));order.append(v);rem.remove(v)
  P=pairing(V,order);key=(tuple(V),tuple(sorted(P)))
  if key in seen:continue
  seen.add(key);sol,nodes,cut=solve(V,P);total+=nodes
  row={'maximal_simplices':maxs,'original_order':order,'P':P,'solution':sol,'nodes':nodes,'cutoff':cut};out.append(row)
  if sol is None and not cut:
   print('COUNTER',json.dumps(row),flush=True);Path(__file__).with_name('search_result.json').write_text(json.dumps({'counter':row,'total_nodes':total,'tested_distinct':len(out)},indent=2));raise SystemExit
  if total>180000:break
 if total>180000:break
print('NO_COUNTER',len(out),total,'cutoffs',sum(r['cutoff'] for r in out))
Path(__file__).with_name('search_result.json').write_text(json.dumps({'results':out,'total_nodes':total,'tested_distinct':len(out)},indent=2))
