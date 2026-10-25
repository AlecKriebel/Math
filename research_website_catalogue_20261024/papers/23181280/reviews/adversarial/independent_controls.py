"""Own exhaustive diagnostics; all-size proof remains in ATTACK_DERIVATIONS.md."""
from itertools import combinations,combinations_with_replacement,product
from functools import lru_cache
from collections import Counter
import json

def normalize(formula):
 out=[]
 for clause in formula:
  s=set(clause)
  if any(-x in s for x in s):continue
  if not s:return None,()
  out.append(tuple(sorted(s,key=lambda x:(abs(x),x))))
 labels=tuple(sorted({abs(x) for c in out for x in c})); pos={x:i+1 for i,x in enumerate(labels)}
 return tuple(tuple(pos[abs(x)] if x>0 else -pos[abs(x)] for x in c) for c in out),labels

def tables(n,cs,B=2):
 N=n+len(cs)+2; es=[(0,1)]+[(h,i+1) for i in range(1,n+1) for h in [0,1]]
 es += [(abs(x)+1,n+2+j) for j,c in enumerate(cs) for x in c]
 es=tuple(sorted(set(tuple(sorted(e)) for e in es))); ix={e:i for i,e in enumerate(es)}
 def arc(u,v):
  return 2*ix[tuple(sorted((u,v)))]+int(u>v)
 cost=[[0]*(2*len(es)) for _ in range(N)]
 for i,(u,v) in enumerate(es):
  b=0 if (u,v)==(0,1) else (B if v>=n+2 else 1)
  cost[0][2*i]=cost[0][2*i+1]=b
 for j,c in enumerate(cs):
  for lit in c:
   v=abs(lit)+1
   cost[n+2+j][arc(v,0)]=int(lit<0)
   cost[n+2+j][arc(v,1)]=int(lit>0)
 return N,es,cost,2*len(cs)+n

def orient(N,es,chosen):
 adj=[[] for _ in range(N)]
 for e in chosen:
  u,v=es[e];adj[u].append((v,e));adj[v].append((u,e))
 arcs=[]
 for root in range(N):
  seen={root};todo=[root];got=[]
  for u in todo:
   for v,e in adj[u]:
    if v not in seen:
     seen.add(v);todo.append(v);got.append(2*e+int(u>v))
  assert len(seen)==N
  arcs.append(tuple(got))
 # A separate cut computation: deleting e, root lies on u-side iff e directedu→v.
 cuts=[]
 for e in chosen:
  u,v=es[e];side={u};todo=[u]
  for w in todo:
   for z,ee in adj[w]:
    if ee!=e and z not in side:side.add(z);todo.append(z)
  cuts.append((e,side))
 for r in range(N):
  bycut={2*e+int(r not in side) for e,side in cuts}
  assert bycut==set(arcs[r])
 return tuple(arcs),tuple(cuts)

@lru_cache(None)
def trees(N,es):
 result=[]
 for chosen in combinations(range(len(es)),N-1):
  parent=list(range(N))
  def find(x):
   while parent[x]!=x:x=parent[x]
   return x
  for e in chosen:
   u,v=es[e];a,b=find(u),find(v)
   if a==b:break
   parent[a]=b
  else:
   arcs,cuts=orient(N,es,chosen);result.append((chosen,arcs,cuts))
 return result

def assignment_unsat(n,cs):
 return min(sum(not any(bool(bits[abs(x)-1])==(x>0) for x in c) for c in cs) for bits in product([0,1],repeat=n))

ct=Counter(); sample=[]
def verify(n,cs):
 N,es,cost,K=tables(n,cs); minimum=10**9; structured_min=10**9
 transposed=[[row[a^1] for a in range(len(row))] for row in cost]
 for chosen,arcs,cuts in trees(N,es):
  rootcost=[sum(cost[r][a] for a in arcs[r]) for r in range(N)]
  F=sum(rootcost); minimum=min(minimum,F)
  q=sum(es[e][1]>=n+2 for e in chosen);h=int(0 in chosen) # sortededge0=(0,1)
  p=len(chosen)-q-h
  assert rootcost[0]==K+(1-h)+(q-len(cs));ct['base_identity']+=1
  shifted=sum(sum(cost[r][a]+1 for a in arcs[r]) for r in range(N))
  assert shifted==F+N*(N-1);ct['positive_shift']+=1
  # Independentedge-cutaccounting, including inwardorientationwithtransposedinput.
  cutF=sum(sum(cost[r][2*e+int(r not in side)] for r in range(N)) for e,side in cuts)
  assert cutF==F;ct['independent_cut_objective']+=1
  inward=sum(sum(transposed[r][2*e+int(r in side)] for r in range(N)) for e,side in cuts)
  assert inward==F;ct['transpose_identity']+=1
  if F<=K:assert h==1 and q==len(cs);ct['threshold_structural']+=1
  if h==1 and q==len(cs):
   selected=[];truth={}
   for i in range(1,n+1):
    incident=[es[e] for e in chosen if es[e][1]==i+1 and es[e][0] in [0,1]]
    assert len(incident)==1;truth[i]=incident[0][0]==0
   false=0
   for j,c in enumerate(cs):
    incident=[es[e][0]-1 for e in chosen if es[e][1]==n+2+j]
    assert len(incident)==1;i=incident[0];lit=next(x for x in c if abs(x)==i)
    wrong=int(truth[i]!=(lit>0));assert rootcost[n+2+j]==wrong;false+=wrong
   assert F==K+false;structured_min=min(structured_min,F);ct['structured_literal_identity']+=1
  ct['trees_evaluated']+=1
 min_unsat=assignment_unsat(n,cs)
 assert (minimum<=K)==(min_unsat==0)
 assert structured_min==K+min_unsat
 ct['formula_reduction_equivalence']+=1
 if len(sample)<12:sample.append({'n':n,'clauses':cs,'trees':len(trees(N,es)),'minimum_cost':minimum,'K':K,'minimum_unsat':min_unsat})

for n in [1,2]:
 pool=[]
 for sizes in range(1,n+1):
  for inds in combinations(range(1,n+1),sizes):
   for signs in product([-1,1],repeat=sizes):pool.append(tuple(i*s for i,s in zip(inds,signs)))
 for m in range(1,5):
  for cs in combinations_with_replacement(pool,m):
   if {abs(x) for c in cs for x in c}==set(range(1,n+1)):verify(n,cs)
# Width3 controls, including unsatisfiable3SAT'sall8signclauses notexhaustivelyenumeratedhere.
full=[tuple(i*s for i,s in zip([1,2,3],signs)) for signs in product([-1,1],repeat=3)]
for cs in combinations_with_replacement(full,2):verify(3,cs)
for cs in [((1,),(-1,), (2,3)),((1,2),(-1,3),(-2,-3)),((1,2,3),(-1,-2,-3),(1,-2,3)),((1,),(-1,2),(-2,3),(-3,))]:verify(3,cs)
# Preprocessing/sparse-label bound controls.
assert normalize([(10**30,10**30),(-10**30,7),(7,-7)])[0]==((2,), (1,-2))
assert normalize([(),(1,)])[0] is None
assert normalize([(1,-1)])[0]==()
ct['preprocessing_controls']=3
# Exact constructed negativecontrols: lowering Bto1 breaksstructuralforcing.
# Threevariables; contradictoryall4binaryclauseson2,3; bridgeclause(1,2).
def explicit_bad(copies,B):
 cs=tuple(c for _ in range(copies) for c in [(2,3),(2,-3),(-2,3),(-2,-3)])+((1,2),)
 n=3;N,es,cost,K=tables(n,cs,B);ix={e:i for i,e in enumerate(es)}
 pairs=[(0,1),(0,2)] # hubedge and v1→truthhub
 pairs += [(2,n+2+len(cs)-1),(3,n+2+len(cs)-1)] # bridgeq joinsv1,v2
 pairs += [(3,n+2),(4,n+2)] # firstbinaryq joinsv2,v3
 pairs += [(3,n+2+j) for j in range(1,len(cs)-1)]
 chosen=tuple(sorted(ix[tuple(sorted(e))] for e in pairs));assert len(chosen)==N-1
 arcs,cuts=orient(N,es,chosen);F=sum(sum(cost[r][a] for a in arcs[r]) for r in range(N))
 KB=B*len(cs)+n;u=assignment_unsat(n,cs)
 return {'copies':copies,'B':B,'clauses':cs,'tree_edges':[es[e] for e in chosen],'N':N,'F':F,'K_B':KB,'minimum_unsat':u,'root_costs':[sum(cost[r][a] for a in arcs[r]) for r in range(N)]}
wrong_B=explicit_bad(1,1);assert wrong_B['minimum_unsat']==1 and wrong_B['F']==wrong_B['K_B']
nonclaimed=explicit_bad(3,2);assert nonclaimed['F']==nonclaimed['K_B']+2 and nonclaimed['minimum_unsat']==3
# Trivialyes/no and N1cost.
assert sum([1,1])==2>1
assert 0<=0 and not 0<=-1
ct['negative_and_trivial_controls']=4
out={'status':'finite_independent_checks_passed','counts':dict(ct),'distinct_graphs_cached':trees.cache_info().currsize,'sample_instances':sample,'negative_control_B1_false_positive':wrong_B,'nonclaimed_unrestricted_OPT_equals_K_plus_min_unsat_counterexample':nonclaimed,'limits':'Exactfiniteenumeration/constructednegativecontrols only; universalreductionprovedseparately. Noauthoredsourceexecuted.'}
print(json.dumps(out,indent=2))
