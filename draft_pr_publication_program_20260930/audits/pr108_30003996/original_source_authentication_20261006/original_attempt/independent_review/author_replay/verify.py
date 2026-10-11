from itertools import product,combinations,combinations_with_replacement
from functools import lru_cache
from pathlib import Path
import json,hashlib
checks=0;tree_cases=0;formula_count=0
@lru_cache(None)
def alltrees(N,E):
 out=[]
 for es in combinations(E,N-1):
  par=list(range(N))
  def find(a):
   while par[a]!=a:a=par[a]
   return a
  ok=True
  for u,v in es:
   a,b=find(u),find(v)
   if a==b:ok=False;break
   par[a]=b
  if not ok:continue
  adj=[[] for _ in range(N)]
  for u,v in es:adj[u].append(v);adj[v].append(u)
  oriented=[]
  for r in range(N):
   seen={r};queue=[r];arcs=[]
   for u in queue:
    for v in adj[u]:
     if v not in seen:seen.add(v);queue.append(v);arcs.append((u,v))
   oriented.append(tuple(arcs))
  out.append((es,tuple(oriented)))
 return tuple(out)
def run(n,clauses):
 global checks,tree_cases,formula_count
 m=len(clauses);N=n+m+2;B=n+1;K=B*m+n
 E={(0,1)}|{(h,i+2) for h in [0,1] for i in range(n)}
 for j,C in enumerate(clauses):
  for lit in C:E.add((abs(lit)+1,n+2+j))
 E=tuple(sorted(E));cost=[{} for _ in range(N)]
 for u,v in E:
  val=0 if (u,v)==(0,1) else (B if v>=n+2 else 1)
  cost[0][u,v]=cost[0][v,u]=val
 for j,C in enumerate(clauses):
  for lit in C:cost[n+2+j][abs(lit)+1, int(lit>0)]=1
 sats=[a for a in product([False,True],repeat=n) if all(any(a[abs(l)-1]==(l>0) for l in C) for C in clauses)]
 feasible=False
 for es,arcs in alltrees(N,E):
  tree_cases+=1
  value=sum(sum(cost[r].get(e,0) for e in arcs[r]) for r in range(N))
  q=sum(v>=n+2 for u,v in es);h=int((0,1) in es);p=len(es)-q-h
  base=sum(cost[0].get(e,0) for e in arcs[0])
  assert base==p+B*q==K+(1-h)+n*(q-m) and q>=m;checks+=1
  assert value>=base;checks+=1
  if value<=K:
   feasible=True;assert h==1 and q==m;checks+=1
   assignment=[(0,i+2) in es for i in range(n)]
   assert all(any(assignment[abs(l)-1]==(l>0) for l in C) for C in clauses);checks+=1
 assert feasible==bool(sats);checks+=1
 for assignment in sats:
  es={(0,1)}|{(0 if val else 1,i+2) for i,val in enumerate(assignment)}
  for j,C in enumerate(clauses):
   lit=next(l for l in C if assignment[abs(l)-1]==(l>0));es.add((abs(lit)+1,n+2+j))
  es=tuple(sorted(es));entry=next(arcs for ee,arcs in alltrees(N,E) if ee==es)
  value=sum(sum(cost[r].get(e,0) for e in entry[r]) for r in range(N))
  assert value==K;checks+=1
 formula_count+=1
for n in [1,2]:
 C=[]
 for size in range(1,n+1):
  for vs in combinations(range(1,n+1),size):
   C += [tuple(v*s for v,s in zip(vs,signs)) for signs in product([-1,1],repeat=size)]
 for m in [1,2,3]:
  for cs in combinations_with_replacement(C,m):run(n,cs)
C=[tuple((i+1)*s for i,s in enumerate(signs)) for signs in product([-1,1],repeat=3)]
for cs in combinations_with_replacement(C,2):run(3,cs)
for cs in [((1,),(-1,),(1,2,3)),((1,2,3),(-1,-2,-3),(1,-2,3)),((1,),(-2,),(2,3))]:run(3,cs)
r={'assertions':checks,'formulas_checked':formula_count,'spanning_tree_formula_cases':tree_cases,'distinct_graphs':alltrees.cache_info().currsize,'all_pass':True,'artifact_sha256':hashlib.sha256(Path('PROOF.md').read_bytes()).hexdigest(),'scope':'Exact controls for the stated 3-CNF reduction; the written proof establishes all-size NP-completeness.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
