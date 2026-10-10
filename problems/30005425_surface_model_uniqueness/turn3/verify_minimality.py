#!/usr/bin/env python3
import sys,itertools,json,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'turn1'))
from surface_gluing import surface
checks=0
def ck(x):
 global checks
 assert x; checks+=1
quivers=cover_count=0;varying=[];by_beta=collections.Counter();small=[]
for n in range(1,5):
 pairs=list(itertools.combinations(range(n),2))
 for counts in itertools.product(range(3),repeat=len(pairs)):
  a=[e for e,c in zip(pairs,counts) for _ in range(c)];m=len(a)
  if any(sum(s==v for s,t in a)>2 or sum(t==v for s,t in a)>2 for v in range(n)):continue
  seen={0}
  while True:
   more=seen|{t for s,t in a if s in seen}|{s for s,t in a if t in seen}
   if more==seen:break
   seen=more
  if len(seen)!=n:continue
  opts=[]
  for v in range(n):
   inc=[i for i,(s,t) in enumerate(a) if t==v];out=[i for i,(s,t) in enumerate(a) if s==v];ps=list(itertools.product(inc,out));oo=[]
   for bits in itertools.product((0,1),repeat=len(ps)):
    r={p for p,b in zip(ps,bits) if b}
    if all(sum((x,y) in r for y in out)<=1 and sum((x,y) not in r for y in out)<=1 for x in inc) and all(sum((x,y) in r for x in inc)<=1 and sum((x,y) not in r for x in inc)<=1 for y in out):oo.append(r)
   opts.append(oo)
  quivers+=1;types=set();beta=m-n+1
  for choice in itertools.product(*opts):
   r=set().union(*choice);s=surface(n,a,r);cover_count+=1
   g,b=s['genus'],s['boundaries'];types.add((g,b));by_beta[str(beta)]+=1
   ck(s['white_punctures']==s['black_punctures']==0)
   ck(2*g+b==beta+1);ck(b>=1)
   if beta<=1:ck((g,b)==(0,beta+1))
  if n<=3:ck(len(types)==1)
  if len(types)>1:varying.append({'vertices':n,'arrows':a,'types':sorted(types)})
  if n==3 and m==4:small.append({'arrows':a,'types':sorted(types)})
ck(bool(varying));ck(min(x['vertices'] for x in varying)==4);ck(min(len(x['arrows']) for x in varying)==5)
ck(small==[{'arrows':[(0,1),(0,1),(1,2),(1,2)],'types':[(1,1)]}])
print(json.dumps({'assertions':checks,'connected_acyclic_multiquivers':quivers,'all_gentle_relation_tables':cover_count,'cover_counts_by_cycle_rank':dict(by_beta),'three_vertex_cycle_rank_two':small,'varying_topology_quivers':varying,'scope':'All topologically ordered quivers on at most four vertices with multiplicities zero, one or two; degree bounds enforced. This finite enumeration supplements the general cycle-rank and minimality proofs.'},indent=2))
