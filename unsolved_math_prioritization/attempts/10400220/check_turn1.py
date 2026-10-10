"""Exact logical countercontrol for the localized graph reduction; this is not a knot example."""
from collections import deque
import json
V=['U','A','Ap','B','Bp','T','Tp'];rho={'U':'U','A':'Ap','Ap':'A','B':'Bp','Bp':'B','T':'Tp','Tp':'T'}
local={frozenset(e) for e in [('A','B'),('B','T'),('T','U'),('Ap','Bp'),('Bp','Tp'),('Tp','U')]};full=local|{frozenset(('A','T'))};C=0
def ck(x):
 global C
 assert x;C+=1
def dist(edges,targets):
 d={x:0 for x in targets};q=deque(targets)
 while q:
  v=q.popleft()
  for e in edges:
   if v in e:
    w=next(x for x in e if x!=v)
    if w not in d:d[w]=d[v]+1;q.append(w)
 return d
for e in local:ck(frozenset(rho[x] for x in e) in local)
u=dist(full,{'U'});T={v for v in V if u[v]==1};delta=dist(local,T)
ck(T=={'T','Tp'});ck({rho[v] for v in T}==T)
for v in V:
 ck(rho[rho[v]]==v)
 if v=='U':continue
 ck(delta[v]==delta[rho[v]]);ck(delta[v]>=u[v]-1)
 D=delta[v]-(u[v]-1);Dp=delta[rho[v]]-(u[rho[v]]-1)
 ck(u[rho[v]]-u[v]==D-Dp)
ck(u['A']==2 and u['Ap']==3);ck(delta['A']==delta['Ap']==2)
print(json.dumps({'status':'PASS','exact_assertions':C,'full_distance_to_U':u,'local_distance_to_number_one_set':delta,'limitation':'An abstract graph countercontrol only, not an actual mutant knot pair or an asymptotic/computational search.'},indent=2))
