from itertools import combinations
from pathlib import Path
import importlib.util,json
p=Path(__file__).parent
spec=importlib.util.spec_from_file_location('submitted',p/'author_replay/construct_graph.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
checks=cases=moves=0
def ck(v):
 global checks
 assert v;checks+=1
def pairing(order):
 comps=[];pairs=set();cycles=set();birth={c:i for i,c in enumerate(order) if len(c)==1}
 for c in order:
  if len(c)==1:comps.append({c[0]})
  else:
   A=next(S for S in comps if c[0] in S);B=next(S for S in comps if c[1] in S)
   if A is B:cycles.add(c);continue
   x=min(A,key=lambda v:birth[v,]);y=min(B,key=lambda v:birth[v,]);k=max((x,y),key=lambda v:birth[v,]);pairs.add(((k,),c));comps.remove(A);comps.remove(B);comps.append(A|B)
 return pairs,cycles,frozenset((min(S,key=lambda v:birth[v,]),) for S in comps)
def orders(vertices,edges):
 def rec(seq,V,E):
  if not V and not E:yield seq;return
  for v in V:yield from rec(seq+[(v,)],V-{v},E)
  present={c[0] for c in seq if len(c)==1}
  for e in E:
   if set(e)<=present:yield from rec(seq+[e],V,E-{e})
 yield from rec([],set(vertices),set(edges))
def test(order):
 global cases,moves
 cases+=1;P,H,U=pairing(order);match={(v,e) for v,e in P if v[0] in e}
 # Independently perform every possible single postponement, preserving
 # all already-consecutive pairs, not just the constructor's chosen order.
 for v,e in match:
  i=order.index(e);prefix=order[:i];C={v[0]}
  while True:
   nxt=C|{x for d in prefix if len(d)==2 and set(d)&C for x in d}
   if nxt==C:break
   C=nxt
  inside=[c for c in prefix if set(c)<=C];outside=[c for c in prefix if not set(c)<=C]
  new=outside+[v,e]+[c for c in inside if c!=v]+order[i+1:]
  ck(pairing(new)==(P,H,U));ck(new.index(e)==new.index(v)+1)
  for w,d in P:
   if order.index(d)==order.index(w)+1:ck(new.index(d)==new.index(w)+1)
  moves+=1
 r=a.realize_graph(order);ck(pairing(r['order'])==(P,H,U))
 f=r['function'];events={}
 # Actually build closures for every integer level, without min-coface
 # formula or the author's stored entry times.
 for t in sorted(set(f.values())):
  complex_at={s for c in order if f[c]<=t for k in range(1,len(c)+1) for s in combinations(c,k)}
  for c in complex_at:events.setdefault(c,t)
 ck(events==r['entry'])
 refined=sorted(order,key=lambda c:(events[c],len(c),c))
 ck(refined==r['order']);ck(pairing(refined)==(P,H,U))
 for e in order:
  if len(e)==2:
   for v in e:ck(f[(v,)]>f[e] if ((v,),e) in match else f[e]>f[(v,)])
for n in range(5):
 E=list(combinations(range(n),2))
 for mask in range(1<<len(E)):
  edges=[e for i,e in enumerate(E) if mask>>i&1]
  for order in orders(range(n),edges):test(order)
r={'status':'PASS','exact_assertions':checks,'graph_filtrations':cases,'single_pair_postponements':moves,'coverage':'All simplex-wise orders of all labeled simple graphs on zero through four vertices. Every incident-pair postponement independently tested, including all already consecutive pairs. Generated subcomplexes explicitly closed at each integer event; labeled pairs, cycle births and unpaired H0 roots checked.'}
(p/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
