"""Own symbolic identities and finite first-contact controls for turn 3."""
from collections import deque,Counter
from itertools import combinations,permutations
import sympy as s
import json
C=Counter()
def check(ok,k):
 assert ok,k
 C[k]+=1
J,p,q,A,B,eta,etap,sg,du,delta,old=s.symbols('J p q A B eta etap sigma du delta old',real=True)
F=s.sqrt(J**2+p**2)
P=p/F
# Total derivative uses J'=B+A*p, while F_t=J*A/F.
E=s.simplify(J*A/F-s.diff(P,J)*(B+A*p)-s.diff(P,p)*q)
K=A*J**2+2*A*p**2+B*p-J*q
check(s.simplify(E-J*K/F**3)==0,'nonradial_Euler_curvature')
check(s.simplify((sg*du+delta+old)-old-(delta+sg*du))==0,'suffix_budget_identity')
check(s.simplify((s.diff(P,J)*(B+A*p)+s.diff(P,p)*q)*eta+P*etap+E*eta-(J*A/F*eta+P*etap))==0,'prefix_variation_integration_by_parts')
# z'=p e+J e_perp; z''=(q-AJ)e+(B+2Ap)e_perp.
check(s.expand(p*(B+2*A*p)-J*(q-A*J)-K)==0,'frame_determinant')
for vals in [(1,2,3,0,0),(2,1,5,-1,0),(3,2,7,1,-2),(1,1,4,0,1)]:
 v=dict(zip((J,p,q,A,B),vals));check(s.simplify(E.subs(v)-J.subs(v)*K.subs(v)/F.subs(v)**3)==0,'nonconvex_wavefront_cases')
# Five-vertex undirected unit networks. A barrier vertex may be an endpoint
# of an arrival path, but cannot be passed through. Missing arrivals use INF.
V=5;edges=list(combinations(range(V),2));barriers=(2,3,4);INF=100

def distance(adj,target,blocked):
 d={0:0};Q=deque([0])
 while Q:
  x=Q.popleft()
  if x==target:return d[x]
  for y in adj[x]:
   if y not in d and (y not in blocked or y==target):d[y]=d[x]+1;Q.append(y)
 return INF
valid=0
for mask in range(1<<len(edges)):
 adj=[[] for _ in range(V)]
 for i,(x,y) in enumerate(edges):
  if mask>>i&1:adj[x].append(y);adj[y].append(x)
 full={v:distance(adj,v,set(barriers)) for v in barriers}
 for order in permutations(barriers):
  if any(full[order[i]]>full[order[i+1]] for i in range(2)):continue
  valid+=1
  for i,v in enumerate(order):
   check(distance(adj,v,set(order[:i+1]))==full[v],'first_contact_prefix_graph_analogue')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'graphs':1<<len(edges),'monotone_orders_checked':valid,'scope':'Conditional geometric identities and discrete causal-order diagnostic only. No full winding-suffix comparison or optimizer counterexample.'},indent=2,sort_keys=True))
