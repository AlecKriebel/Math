"""Finite-group exact controls of the canonical Markov-transport argument."""
from itertools import product
from fractions import Fraction as F
from collections import Counter
import sympy as S
import json
C=Counter()
def ck(b,k):assert b,k;C[k]+=1
def shift(v,t):return v[t:]+v[:t]
patterns=0
for n in range(1,6):
 for seed in product(range(3),repeat=n):
  if not any(seed):continue
  states=sorted(set(shift(seed,t) for t in range(n)))
  if seed!=states[0]:continue
  patterns+=1; idx={v:i for i,v in enumerate(states)};m=len(states);mass=sum(seed)
  h={v:F(1,i+2) for i,v in enumerate(states)}
  edges={(v,t) for v in states for t in range(n)};gates=[]
  while edges:
   e=min(edges);v,t=e;r=(shift(v,t),(-t)%n);gate={e,r};edges-=gate;gates.append(gate)
  q=[F(v[0],sum(w[0] for w in states)) for v in states]
  ck(sum(q)==1,'Palm_root_weights')
  constraints=[]
  for gate in gates:
   K=[[F(0) for _ in states] for _ in states]
   for v in states:
    i=idx[v];row=F(0)
    for t in range(n):
     a=h[v]*h[shift(v,t)]/((1+mass)**2)*int((v,t) in gate)
     w=a*v[t];K[i][idx[shift(v,t)]]+=w;row+=w
    ck(row<=h[v]<=1,'finite_test_mass_and_row_bound')
    K[i][i]+=1-row
   for row in K:ck(sum(row)==1 and min(row)>=0,'Markov_rows')
   for j in range(m):ck(sum(q[i]*K[i][j] for i in range(m))==q[j],'Palm_stationary_each_gate')
   constraints.extend([[K[i][j]-int(i==j) for i in range(m)] for j in range(m)])
   # Spatial mass preservation is checked independently at every translated row.
   v=seed;spatial=[[F(0) for t in range(n)] for s in range(n)]
   for s in range(n):
    rsum=F(0)
    for t in range(n):
     a=h[shift(v,s)]*h[shift(v,t)]/((1+mass)**2)*int((shift(v,s),(t-s)%n) in gate)
     spatial[s][t]+=a*v[t];rsum+=a*v[t]
    spatial[s][s]+=1-rsum
   for t in range(n):ck(sum(v[s]*spatial[s][t] for s in range(n))==v[t],'spatial_mass_preservation')
  mat=S.Matrix([[S.Rational(x.numerator,x.denominator) for x in row] for row in constraints])
  ck(mat.rank()==m-1,'all_gates_force_unique_Palm_law')
  for v in states:
   H=[t for t in range(n) if shift(v,t)==v]
   for t in H:ck(v[t]==v[(-t)%n],'stabilizer_mass_inversion')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'canonical_orbit_patterns':patterns,'scope':'Finite exact controls only; no substitute for the general measure-theoretic proof or source-scope closure.'},sort_keys=True,indent=2))
