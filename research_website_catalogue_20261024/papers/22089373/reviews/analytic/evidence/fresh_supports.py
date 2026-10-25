"""Independent finite topology controls from the five printed directed cores."""
from fresh_graph_fourier import *
from itertools import combinations
from math import comb
cores=[('cycle',[('S','X'),('S','X')],[(0,),(1,)]),('theta0',[('S','U'),('S','V'),('U','X'),('V','X'),('U','V')],[(2,3),(3,4)]),('theta1',[('S','U'),('S','X'),('V','X'),('U','V'),('U','V')],[(2,3),(2,4)]),('theta2',[('S','U'),('S','V'),('U','X0'),('V','X0'),('U','X1'),('V','X1')],[(2,3),(2,5),(3,4),(4,5)]),('theta3',[('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V')],[(2,),(4,)])]
results=[];counts={n:0 for n in range(3,7)}
for name,arcs,repairs in cores:
 verts=set(sum(([u,v] for u,v in arcs),[]));out={v:sum(u==v for u,w in arcs) for v in verts};sinks=sorted(v for v in verts if not out[v]);accepted=[]
 for mask in range(1<<len(arcs)):
  subset={i for i in range(len(arcs)) if mask>>i&1};a=[('R','S'),('R','L_in')];leaf=0
  for i,(u,v) in enumerate(arcs):
   if i in subset:a.extend([(u,f'P{i}'),(f'P{i}',v),(f'P{i}',f'L{leaf}')]);leaf+=1
   else:a.append((u,v))
  for v in sinks:a.append((v,f'L{leaf}'));leaf+=1
  # An already-simple mixed graph is necessary, so reject repeated underlying arcs.
  und=[tuple(sorted((u,v))) for u,v in a if u!='R']+[tuple(sorted(('S','L_in')))]
  if len(set(und))<len(und):continue
  # Direct mixed no-omnian test on root-suppressed arcs, independently recomputed.
  V,ins,outs,root,Rt=topology(a);unddegree={v:0 for v in V if v!='R'};tails={v:0 for v in unddegree}
  for u,v in a:
   if u=='R':continue
   if v in Rt:tails[u]+=1
   else:unddegree[u]+=1;unddegree[v]+=1
  unddegree['S']+=1;unddegree['L_in']+=1
  strong=all(unddegree[v]>=2 or tails[v]==0 for v in unddegree)
  if strong:
   accepted.append(subset)
   assert any(set(r)<=subset for r in repairs)
   # For minimal supports, directly brute-force every root and check all TC.
   if tuple(sorted(subset)) in repairs:
    c=census(a);assert c['admissible'] and c['tree_child']==c['admissible']
    results.append({'core':name,'repair':sorted(subset),'admissible_rootings':c['admissible'],'all_tree_child':True})
  else:assert not any(set(r)<=subset for r in repairs)
 # Enumerate omitted-sink choices and ordinary-port occupancies by a separate stars-and-bars expression.
 for n in counts:
  count=sum(comb(len(sinks),k)*comb(n-k+len(arcs)-1,len(arcs)-1) for k in range(len(sinks)+1) if n>=k)
  counts[n]+=count*(1 if name=='cycle' else len(repairs))
assert counts=={3:831,4:1983,5:4155,6:7909}
assert len(results)==12 and sum(r['admissible_rootings'] for r in results)==100
Path(__file__).with_name('fresh-supports.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','all_196_subsets_checked':sum(1<<len(a) for _,a,_ in cores),'minimal_supports':results,'total_admissible_rootings':sum(r['admissible_rootings'] for r in results),'completion_counts':counts,'scope':'Repairs for the printed exhaustive core list and bounded completion count; human degree proof supplies exhaustiveness of that list.'},indent=2)+'\n')
print('PASS supports, all rootings, completion counts',flush=True)
