#!/usr/bin/env python3
"""Independent graph checker: enumerate edge subsets, not parent choices."""
from itertools import combinations,product
from collections import Counter,deque
import json,math
checks=Counter();examined=0;trees=0;instances=0

def ck(p,k):
 assert p,k
 checks[k]+=1

def build(n,clauses):
 V=1+3*n+len(clauses);arcs=[]
 def t(i):return 1+2*i
 def f(i):return 2+2*i
 def v(i):return 1+2*n+i
 def z(j):return 1+3*n+j
 for i in range(n):arcs.extend([(0,t(i)),(0,f(i)),(t(i),v(i)),(f(i),v(i))])
 for j,clause in enumerate(clauses):
  arcs.extend((v(abs(l)-1),z(j)) for l in clause)
 cost=[[0]*len(arcs) for _ in range(V)]
 for j,clause in enumerate(clauses):
  for lit in clause:
   bad=f(lit-1) if lit>0 else t(-lit-1)
   cost[z(j)][arcs.index((0,bad))]=1
 return V,arcs,cost

def check_instance(n,clauses):
 global examined,trees,instances
 V,arcs,cost=build(n,clauses);M=len(arcs)
 ck(len(set(arcs))==M,'simple_graph')
 ck(V==1+3*n+len(clauses) and M<=4*n+3*len(clauses),'polynomial_size')
 ck(all(c in (0,1) for row in cost for c in row),'dense_cost_table_binary')
 # The candidates are all size-(V-1) subsets of the arc set. No canonical tree
 # parametrization is used to select them.
 best=10**9;byassignment={};valid=0
 for chosen in combinations(range(M),V-1):
  examined+=1
  indeg=[0]*V;children=[[] for _ in range(V)]
  for e in chosen:
   a,b=arcs[e];indeg[b]+=1;children[a].append((b,e))
  if indeg[0]!=0 or any(x!=1 for x in indeg[1:]):continue
  paths={0:()};parent={};queue=deque([0])
  while queue:
   a=queue.popleft()
   for b,e in children[a]:
    if b in paths:break
    paths[b]=paths[a]+(e,);parent[b]=a;queue.append(b)
  if len(paths)!=V:continue
  valid+=1;trees+=1
  assignment=tuple(parent[1+2*n+i]==1+2*i for i in range(n))
  value=sum(cost[d][e] for d in range(1,V) for e in paths[d])
  shifted=sum(cost[d][e]+1 for d in range(1,V) for e in paths[d])
  ck(shifted-value==4*n+3*len(clauses),'positive_cost_offset')
  ck(all(parent[1+2*i]==parent[2+2*i]==0 for i in range(n)),'all_tree_forced_arcs')
  false_witnesses=0
  for j,clause in enumerate(clauses):
   d=1+3*n+j
   ck(len(paths[d])==3,'clause_path_depth')
   i=parent[d]-(1+2*n)
   signs=[lit for lit in clause if abs(lit)==i+1]
   ck(len(signs)==1,'selected_parent_is_eligible_literal')
   false_witnesses+=int(assignment[i]!=(signs[0]>0))
  ck(value==false_witnesses,'actual_path_cost_false_witness_identity')
  byassignment[assignment]=min(byassignment.get(assignment,10**9),value)
  best=min(best,value)
 ck(valid==2**n*math.prod(len(c) for c in clauses),'no_noncanonical_arborescences')
 truth=[]
 for assignment in product((False,True),repeat=n):
  unsat=sum(all(assignment[abs(l)-1]!=(l>0) for l in c) for c in clauses)
  truth.append(unsat)
  ck(byassignment[assignment]==unsat,'each_global_assignment_optimum')
 ck(best==min(truth),'complete_optimum_identity')
 ck((best==0)==(0 in truth),'NP_reduction_zero_equivalence')
 instances+=1
 return best

U=[]
for k in (1,2):
 for variables in combinations((1,2),k):
  for signs in product((-1,1),repeat=k):U.append(tuple(i*s for i,s in zip(variables,signs)))
for m in range(4):
 for clauses in combinations(U,m):check_instance(2,clauses)
for signs in product((-1,1),repeat=3):check_instance(3,[tuple((i+1)*signs[i] for i in range(3))])
for signs in product((-1,1),repeat=2):
 c=(signs[0],2*signs[1],3)
 check_instance(3,[c,tuple(-x for x in c)])
 check_instance(3,[c,(-c[0],),(-c[1],)])
ck(check_instance(1,[(1,),(-1,)])==1,'fixed_no_instance')
ck(check_instance(1,[(1,)])==0,'fixed_yes_instance')
ck(check_instance(1,[(1,),(1,),(-1,)])==1,'repeated_clause_control')
ck(check_instance(2,[(1,2),(1,-2),(-1,2),(-1,-2)])==1,'unsatisfiable_binary_control')
ck(check_instance(3,[(1,),(-1,),(2,),(-2,),(3,),(-3,)])==3,'multiple_unsatisfied_clauses')
# Independently confirm harmless preprocessing, including clauses with both signs.
for raw in [[(1,1,2),(-1,2,2)],[(1,-1,2),(-2,)],[(1,1,1),(-1,-1,-1)],[]]:
 cleaned=[]
 for clause in raw:
  c=set(clause)
  if not any(-x in c for x in c):cleaned.append(tuple(sorted(c)))
 for assignment in product((False,True),repeat=2):
  lhs=sum(not any(assignment[abs(l)-1]==(l>0) for l in c) for c in raw)
  rhs=sum(not any(assignment[abs(l)-1]==(l>0) for l in c) for c in cleaned)
  ck(lhs==rhs,'preprocessing_preserves_unsatisfied_count')
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
 'formulas_checked':instances,'all_edge_subsets_examined':examined,'actual_arborescences_checked':trees,
 'method':'Independent dense destination-cost construction; unfiltered size-(|V|-1) edge-subset enumeration, indegree and reachability validation, then explicit path summation.',
 'scope':'Bounded exact verification supplements the arbitrary-size reduction proof; it is not used as a substitute for NP-hardness or a novelty claim.'},indent=2,sort_keys=True))
