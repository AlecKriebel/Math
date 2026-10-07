from pathlib import Path
import sys,json,hashlib,random
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations,product
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'clean_package/code'))
import gadget as g
import sampling as s

# Independent recurrence over concrete edge sets. No package counter is called.
def matchings(n,edges):
 adj=[set() for _ in range(n)]
 for u,v in edges: adj[u].add(v);adj[v].add(u)
 @lru_cache(None)
 def visit(V):
  if not V:return ((),)
  S=set(V);u=min(V,key=lambda x:len(adj[x]&S));out=[]
  for v in sorted(adj[u]&S):
   for tail in visit(tuple(x for x in V if x not in (u,v))):out.append(tuple(sorted(((min(u,v),max(u,v)),*tail))))
  return tuple(out)
 return visit(tuple(range(n)))

def count(n,edges,removed=()):
 adj=[set() for _ in range(n)]
 for u,v in edges: adj[u].add(v);adj[v].add(u)
 @lru_cache(None)
 def visit(V):
  if not V:return 1
  if len(V)%2:return 0
  S=set(V);u=min(V,key=lambda x:len(adj[x]&S))
  return sum(visit(tuple(x for x in V if x not in (u,v))) for v in adj[u]&S)
 return visit(tuple(x for x in range(n) if x not in removed))

sig=0
for W in list(range(1,257))+[511,512,513,1023,1024,1025]:
 G=g.integer_gadget(W).graph
 actual=tuple(count(G.order,G.edges,R) for R in [(),(0,1),(0,),(1,)])
 assert actual==(W,1,0,0);sig+=1
# Every gadget orientation for K4. Gluing is reconstructed independently.
E=list(combinations(range(4),2)); global_cases=0;fiber_cases=0
for mask in range(64):
 weights=[1,2,3,1,2,1];edges=[];owners={};n=4
 for i,((u,v),W) in enumerate(zip(E,weights)):
  H=g.integer_gadget(W).graph
  if mask&(1<<i):u,v=v,u
  names={0:u,1:v,**{j:n+j-2 for j in range(2,H.order)}};n+=H.order-2
  for x,y in H.edges:
   edge=tuple(sorted((names[x],names[y])));edges.append(edge);owners[edge]=E[i]
 assert len(set(edges))==len(edges)
 fibers={}
 for M in matchings(n,tuple(edges)):
  used={}
  for edge in M:
   owner=owners[edge]
   used.setdefault(owner,set()).update(x for x in edge if x<4)
  assert all(not U or U==set(e) for e,U in used.items())
  image=tuple(sorted(e for e,U in used.items() if U));fibers[image]=fibers.get(image,0)+1
 for M in matchings(4,tuple(E)):
  expected=1
  for edge in M:expected*=weights[E.index(edge)]
  assert fibers[M]==expected;fiber_cases+=1
 global_cases+=1

# Fully integrate the ACTUAL imperative wrapper on all K4 graphs, all finite
# draw tapes, and synthetic nonzero gross-overestimate failure tapes. This
# independently exercises failed outputs beyond the release's zero-only laws.
executions=0;law_cases=0;maxratio=F(0)
for mask in range(64):
 edges=tuple(e for i,e in enumerate(E) if mask&(1<<i)); G=s.Graph.make(range(4),edges)
 true=matchings(4,edges)
 if not true:continue
 witness=lambda H:(matchings(4,H.edges)[0] if len(H.vertices)==4 and matchings(4,H.edges) else (tuple(H.edges) if len(H.vertices)==2 and H.edges else (() if not H.vertices else None)))
 eta=F(1,7);par=s.parameters(4,eta);R=1<<par.bits_per_draw
 children=[v for v in G.neighbors(0) if witness(G.without(0,v)) is not None]
 law={}
 patterns=list(product((0,1),repeat=len(children))) if len(children)>1 else [()]
 for pattern in patterns:
  mass=par.call_failure**sum(pattern)*(1-par.call_failure)**(len(pattern)-sum(pattern))
  for tape in range(R):
   index=[0]
   def oracle(H,a,d):
    i=index[0];index[0]+=1
    return F(2**128+1,3**37) if pattern[i] else 1+(a if i%2 else -a)
   stats=s.Stats();M=s.sample_perfect_matching(G,eta,oracle,witness,lambda b:tape,stats)
   assert M in true
   assert stats.count_calls<=par.call_cap and stats.witness_calls<=par.call_cap+1
   assert stats.random_bits<=par.pairs*par.bits_per_draw
   law[M]=law.get(M,F(0))+mass/R;executions+=1
 assert sum(law.values())==1
 tv=sum(abs(law.get(M,0)-F(1,len(true))) for M in true)/2
 bound=par.pairs*par.relative_error/(1-par.relative_error)+par.call_cap*par.call_failure+F(par.call_cap,R)
 assert tv<=bound<eta
 maxratio=max(maxratio,tv/eta);law_cases+=1

report={'status':'passed','independent_signatures':sig,'all_terminal_orientation_global_cases':global_cases,'individual_fibers':fiber_cases,'actual_wrapper_gross_overestimate_laws':law_cases,'actual_wrapper_executions':executions,'max_tv_over_eta':str(maxratio),'scope':'finite falsification support; no upstream FPRAS execution or kernel verification'}
(ROOT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
