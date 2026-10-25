"""Independent exact finite controls from the printed kernel definitions.
No submitted support code is imported. These are not a proof for general G.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from datetime import datetime,timezone
import json
P=Path(__file__).resolve().parent
checks=0

def ck(x):
 global checks
 checks+=1
 assert x,checks

def shift(mu,u):return tuple(mu[(i+u)%len(mu)] for i in range(len(mu)))
def periods(mu):return {u for u in range(len(mu)) if shift(mu,u)==mu}
def matrix(mu,C,gate):
 n=len(mu);out=[]
 for s in range(n):
  row=[]
  for t in range(n):
   a=F(int((t-s)%n in C),(1+sum(mu[(s+c)%n] for c in C))*(1+sum(mu[(t+c)%n] for c in C)))
   row.append(a*mu[t]*gate(shift(mu,s),(t-s)%n))
  row[s]+=1-sum(row);out.append(row)
 return out

def period_matrix(mu,B):
 n=len(mu);out=[];H=periods(mu)
 for s in range(n):
  w=sum(mu[(h+s)%n] for h in H&B)
  out.append([F(int((t-s)%n in H&B)*mu[t],w) if w else F(t==s) for t in range(n)])
 return out

def preserved(mu,K):return all(sum(mu[s]*K[s][t] for s in range(len(mu)))==mu[t] for t in range(len(mu)))
def rank(A):
 A=[list(map(F,r)) for r in A];rr=0
 if not A:return 0
 for c in range(len(A[0])):
  pi=next((i for i in range(rr,len(A)) if A[i][c]),None)
  if pi is None:continue
  A[rr],A[pi]=A[pi],A[rr];v=A[rr][c];A[rr]=[x/v for x in A[rr]]
  for i in range(rr+1,len(A)):
   v=A[i][c]
   if v:A[i]=[x-v*y for x,y in zip(A[i],A[rr])]
  rr+=1
 return rr

rows=[]
for mu in [(1,2,3,4,5),(0,1,0,1,0,1),(1,3,1,3,1,3),(2,2,2,2),(0,0,0,0),(0,0,3,0,0),(1,2,0,4,0)]:
 n=len(mu);C={0,1,n-1};H=periods(mu);K=matrix(mu,C,lambda m,t:1)
 ck(all(sum(r)==1 and min(r)>=0 for r in K));ck(preserved(mu,K))
 for u in range(n):
  Ku=matrix(shift(mu,u),C,lambda m,t:1)
  ck(all(Ku[(s-u)%n][(t-u)%n]==K[s][t] for s,t in product(range(n),repeat=2)))
 # Each atom set of the measure orbit is a separating gate; selected t has
 # the reversed orientation added to enforce R0 invariance.
 states=set(shift(mu,u) for u in range(n));gates=[]
 for A,t0 in product(states,range(n)):
  def gate(m,t,A=A,t0=t0):
   first=(m==A and shift(m,t)!=A and t==t0)
   reverse=(shift(m,t)==A and m!=A and (-t)%n==t0)
   return int(first or reverse)
  gates.append(gate);Kg=matrix(mu,C,gate)
  ck(preserved(mu,Kg));ck(all(sum(r)==1 and min(r)>=0 for r in Kg))
 for B in [set(),{0},{1},{0,2%n},set(range(n))]:
  KP=period_matrix(mu,B);ck(preserved(mu,KP));ck(all(sum(r)==1 and min(r)>=0 for r in KP))
 # Ambient state is phase u in G; measure depends only on its coset modulo H.
 # Form all gate and period stationarity equations for its unnormalised law q.
 equations=[]
 for radius_set in [C,set(range(n))]:
  for gate in gates:
   transition=[matrix(shift(mu,u),radius_set,gate)[0] for u in range(n)]
   for v in range(n):equations.append([transition[u][(v-u)%n]-int(u==v) for u in range(n)])
 offrank=rank(equations)
 for B in [{t} for t in range(n)]+[set(range(n))]:
  transition=[period_matrix(shift(mu,u),B)[0] for u in range(n)]
  for v in range(n):equations.append([transition[u][(v-u)%n]-int(u==v) for u in range(n)])
 fullrank=rank(equations)
 if sum(mu):
  ck(all(sum(c*m for c,m in zip(row,mu))==0 for row in equations));ck(fullrank==n-1)
 rows.append({'mu':mu,'periods':sorted(H),'off_period_constraint_rank':offrank,'all_constraint_rank':fullrank,'expected_nonzero_Palm_nullspace_dimension':1 if sum(mu) else None})
# Constant measure: measure-only off-period gates do nothing, but period shifts
# still move the ambient phase. A nonuniform q must fail the periodic test.
mu=(1,1,1,1);q=(F(1),F(0),F(0),F(0));KP=period_matrix(mu,{1});ck(not preserved(q,KP));ck(rows[3]['off_period_constraint_rank']==0)
# Unsymmetrized choices are falsifiable negative controls.
mu=(1,2,3,4,5);ck(not preserved(mu,matrix(mu,{0,1},lambda m,t:1)))
A=mu;ck(not preserved(mu,matrix(mu,{0,1,4},lambda m,t:int(m==A and t==1))))
# Mixed zero/positive period-normalizer branches on a nontrivial coset.
mu=(0,1,0,1,0,1);KP=period_matrix(mu,{0,2});ck(KP[0][0]==1);ck(KP[1][1]==F(1,2) and KP[1][3]==F(1,2));ck(preserved(mu,KP))
out={'utc':datetime.now(timezone.utc).isoformat(),'scope':'Exact finite cyclic controls; universal measure-theoretic claims require proof. No submitted code imported.','assertions':checks,'cases':rows,'hidden_ambient_period_noninvariance_detected':True,'asymmetric_C_and_gate_negative_controls_detected':True,'mixed_zero_denominator_branch_checked':True,'passed':True}
(P/'fresh_controls.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',checks,'exact assertions')
