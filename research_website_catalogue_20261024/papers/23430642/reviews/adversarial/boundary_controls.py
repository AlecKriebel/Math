from fractions import Fraction as F
from itertools import product
from pathlib import Path
from datetime import datetime,timezone
import json
from fresh_controls import net,shortest,advance,dot,build_game,verify_aux
R=Path(__file__).resolve().parent
checks=0
def check(v,name):
 global checks;checks+=1
 if not v:raise AssertionError(name)
def simplex(d,total):
 return [tuple(F(x,total) for x in z) for z in product(range(total+1),repeat=d) if sum(z)==total]
def br(v):return {i for i,x in enumerate(v) if x==max(v)}
A=[[F((i+1)*(j+2)%7-3) for j in range(4)] for i in range(3)];a=[F(-1),F(0),F(2)];b=[F(0),F(1),F(-2),F(3)]
B=[[-A[i][j]+a[i]*b[j] for j in range(4)] for i in range(3)]
wrong=0
for x in simplex(3,4):
 lam=dot(a,x);aux=[[A[i][j]-lam*b[j] for j in range(4)] for i in range(3)]
 for y in simplex(4,3):
  check(br([dot(row,y) for row in A])==br([dot(row,y) for row in aux]),'row best response sets')
  col=[dot(x,[B[i][j] for i in range(3)]) for j in range(4)];acol=[-dot(x,[aux[i][j] for i in range(3)]) for j in range(4)]
  check(col==acol,'column payoffs agree exactly')
  wrongcol=[-dot(x,[A[i][j]-(lam+1)*b[j] for i in range(3)]) for j in range(4)]
  if br(wrongcol)!=br(col):wrong+=1
check(wrong>0,'wrong scalar parameter negative control')
# A zero matrix with a constant-one opponent payoff has exact sum rank one,
# and the full product of strategy simplexes is an equilibrium continuum.
for m,N in [(1,2),(2,1),(2,2),(3,4)]:
 AA=[[F(0)]*N for _ in range(m)];BB=[[F(1)]*N for _ in range(m)]
 for x in simplex(m,2):
  for y in simplex(N,2):
   ay=[dot(row,y) for row in AA];bx=[dot(x,[BB[i][j] for i in range(m)]) for j in range(N)]
   check(max(ay)==dot(x,ay) and max(bx)==dot(y,bx),'degenerate continuum exact NE')
# M=0 drops every feasibility constraint: origin is strictly cheaper than a
# value-one feasible flow in the potential-shifted positive-cost network.
E,nodes,Fmax=net([1]);rank={v:i for i,v in enumerate(nodes)};cost=[c+2*(rank[v]-rank[u]) for u,v,cap,c in E]
f=advance(tuple(F(0) for _ in E),shortest(E,nodes,tuple(F(0) for _ in E),cost)[0])
check(dot(cost,f)>0 and sum(f)>0,'positive feasible value-one cost')
zero_penalty={'lambda':1,'infeasible_origin_cost':0,'feasible_flow_cost':str(dot(cost,f)),'origin_q':0,'strictly_better_infeasible':True}
res={'completed_utc':datetime.now(timezone.utc).isoformat(),'completion_percent':80,'status':'ALL_BOUNDARY_CONTROLS_PASSED','assertions':checks,'scalar_correspondence_pairs':len(simplex(3,4))*len(simplex(4,3)),'wrong_parameter_negative_control_detections':wrong,'degenerate_cases':[[1,2],[2,1],[2,2],[3,4]],'zero_penalty_negative_control':zero_penalty,'limits':'Exact rational finite boundary controls; universal support-cell and equilibrium-exhaustion proofs are documented separately.'}
(R/'boundary_results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
