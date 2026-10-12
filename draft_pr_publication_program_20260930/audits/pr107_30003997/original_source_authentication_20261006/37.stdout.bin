#!/usr/bin/env python3
"""Bounded exact graph construction and exhaustive parent-choice controls."""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
import hashlib,json
counts=Counter();formulas_checked=0;trees_checked=0
def ck(k,b):
 assert b,k
 counts[k]+=1
def make(n,clauses):
 nodes=['r'];levels={'r':0};arcs=[];cost={}
 for i in range(1,n+1):
  for tag in ['t','f']:
   u=(tag,i);nodes.append(u);levels[u]=1;arcs.append(('r',u))
 for i in range(1,n+1):
  u=('v',i);nodes.append(u);levels[u]=2
  arcs.extend([(('t',i),u),(('f',i),u)])
 for j,C in enumerate(clauses):
  z=('z',j);nodes.append(z);levels[z]=3
  for lit in C:
   i=abs(lit);arcs.append((('v',i),z))
   bad=('f',i) if lit>0 else ('t',i)
   cost[z,('r',bad)]=1
 return nodes,arcs,levels,cost
def paths_of_parent(nodes,parent):
 paths={}
 for v in nodes[1:]:
  route=[];seen=set();u=v
  while u!='r':
   assert u not in seen
   seen.add(u);p=parent[u];route.append((p,u));u=p
  paths[v]=tuple(reversed(route))
 return paths
def instance(n,clauses):
 global formulas_checked,trees_checked
 nodes,arcs,levels,cost=make(n,clauses)
 ck('simple_graph',len(arcs)==len(set(arcs)))
 ck('four_layer_arcs',all(levels[v]==levels[u]+1 for u,v in arcs))
 incoming={v:[] for v in nodes[1:]}
 for u,v in arcs:incoming[v].append(u)
 ck('indegree_bound',all(1<=len(x)<=3 for x in incoming.values()))
 ck('size_bound',len(nodes)==1+3*n+len(clauses) and len(arcs)<=4*n+3*len(clauses))
 ck('binary_vectors',all(c==1 for c in cost.values()))
 opt=None;best_by_assignment={};base=4*n+3*len(clauses)
 for parents in product(*(incoming[v] for v in nodes[1:])):
  parent=dict(zip(nodes[1:],parents));paths=paths_of_parent(nodes,parent)
  ck('spanning_arborescence',len(parent)==len(nodes)-1 and all(e in arcs for P in paths.values() for e in P))
  value=sum(cost.get((v,e),0) for v,P in paths.items() for e in P)
  shifted=sum(1+cost.get((v,e),0) for v,P in paths.items() for e in P)
  ck('strict_positive_offset',shifted==value+base)
  ck('fixed_path_lengths',all(len(P)==levels[v] for v,P in paths.items()))
  assignment=tuple(parent[('v',i)]==('t',i) for i in range(1,n+1))
  witness_cost=0
  for j,C in enumerate(clauses):
   chosen=parent[('z',j)][1]
   lit=next(l for l in C if abs(l)==chosen)
   witness_cost+=int(assignment[chosen-1]!=(lit>0))
  ck('path_cost_is_false_witnesses',value==witness_cost)
  best_by_assignment[assignment]=min(best_by_assignment.get(assignment,10**9),value)
  opt=value if opt is None else min(opt,value)
  trees_checked+=1
 truth_opt=len(clauses)
 for assignment in product([False,True],repeat=n):
  unsat=sum(not any(assignment[abs(l)-1]==(l>0) for l in C) for C in clauses)
  ck('per_assignment_optimum',best_by_assignment[assignment]==unsat)
  truth_opt=min(truth_opt,unsat)
 ck('optimum_identity',opt==truth_opt)
 ck('zero_threshold_equivalence',(opt==0)==(truth_opt==0))
 formulas_checked+=1
 return opt
# Every formula with <=3 distinct clauses over two variables.
def universe(n):
 out=[]
 for k in range(1,min(n,3)+1):
  for variables in combinations(range(1,n+1),k):
   out.extend(tuple(i*sg for i,sg in zip(variables,signs)) for signs in product([-1,1],repeat=k))
 return out
U=universe(2)
for k in range(4):
 for C in combinations(U,k):instance(2,C)
# Every zero-, one- and two-clause instance over three variables.
U=universe(3)
for k in range(3):
 for C in combinations(U,k):instance(3,C)
# Unsatisfiable positive-optimum controls and repeated clauses.
ck('unit_conflict_optimum',instance(1,[(1,),(-1,)])==1)
ck('binary_unsatisfiable_optimum',instance(2,[(1,2),(1,-2),(-1,2),(-1,-2)])==1)
ck('repeated_clause_weight',instance(1,[(1,),(1,),(-1,)])==1)
ck('multiple_conflicts',instance(3,[(1,),(-1,),(2,),(-2,),(3,),(-3,)])==3)
p=Path(__file__).resolve().parent
out={'status':'PASS','formulas_checked':formulas_checked,'arborescences_checked':trees_checked,'exact_assertions':sum(counts.values()),'checks':dict(counts),'artifact_sha256':hashlib.sha256((p/'PROOF.md').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Bounded exhaustive graph controls only. The arbitrary-size NP-completeness reduction is proved in PROOF.md.'}
print(json.dumps(out,indent=2,sort_keys=True))
