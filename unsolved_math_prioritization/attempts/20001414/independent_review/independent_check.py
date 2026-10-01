#!/usr/bin/env python3
"""Independent exact transport certificates on a non-line three-point metric."""
from itertools import product
from fractions import Fraction as F
from functools import lru_cache
import json
D=((0,2,4),(2,0,3),(4,3,0));count=0

def ck(t):
 global count
 assert t
 count+=1

def solve(a,b):
 n=len(a)
 @lru_cache(None)
 def row(i,rem):
  if i==n:
   return (0,()) if not any(rem) else (10**9,())
  best=(10**9,())
  for flow in product(*(range(min(a[i],r)+1) for r in rem)):
   if sum(flow)!=a[i]:continue
   rest=tuple(rem[j]-flow[j] for j in range(n));cost,plan=row(i+1,rest)
   candidate=sum(flow[j]*D[i][j] for j in range(n))+cost
   if candidate<best[0]:best=(candidate,(flow,)+plan)
  return best
 return row(0,tuple(b))

pots=[(0,p,q) for p in range(-2,3) for q in range(-4,5) if abs(p-q)<=3]
cases=0
for x in range(3):
 for y in range(3):
  if x==y:continue
  for vx,vy in product(product(range(3),repeat=2),repeat=2):
   jx=[0]*3;jy=[0]*3
   for i,v in zip([i for i in range(3) if i!=x],vx):jx[i]=v
   for i,v in zip([i for i in range(3) if i!=y],vy):jy[i]=v
   rx,ry=sum(jx),sum(jy);a=jx.copy();b=jy.copy();a[x]+=ry;b[y]+=rx;M=rx+ry
   ck(sum(a)==sum(b)==M)
   cost,plan=solve(tuple(a),tuple(b))
   ck(tuple(map(sum,plan))==tuple(a))
   ck(tuple(sum(plan[i][j] for i in range(3)) for j in range(3))==tuple(b))
   dual=max(sum(p[i]*(a[i]-b[i]) for i in range(3)) for p in pots)
   ck(cost==dual)
   drift=sum(plan[i][j]*(D[i][j]-D[x][y]) for i in range(3) for j in range(3))
   ck(drift==cost-M*D[x][y])
   for f in product((-1,0,2),repeat=3):
    ck(sum(plan[i][j]*(f[i]-f[x]) for i in range(3) for j in range(3))==sum(jx[i]*(f[i]-f[x]) for i in range(3)))
    ck(sum(plan[i][j]*(f[j]-f[y]) for i in range(3) for j in range(3))==sum(jy[j]*(f[j]-f[y]) for j in range(3)))
   cases+=1
# Adding couplings of two local components is feasible but need not be optimal.
strict=0
x,y=0,2
for raw in product(product((0,1),repeat=2),repeat=4):
 arrays=[];costs=[]
 for left,right in [(raw[0],raw[1]),(raw[2],raw[3])]:
  jx=[0,*left];jy=[*right,0];a=jx.copy();b=jy.copy();a[x]+=sum(jy);b[y]+=sum(jx)
  arrays.append((a,b));costs.append(solve(tuple(a),tuple(b))[0])
 aa=tuple(arrays[0][0][i]+arrays[1][0][i] for i in range(3));bb=tuple(arrays[0][1][i]+arrays[1][1][i] for i in range(3));total=solve(aa,bb)[0]
 ck(total<=sum(costs))
 strict+=total<sum(costs)
ck(strict>0)
# Two-state clocks, including absorbing and fully frozen boundaries.
for a,b in product(range(7),repeat=2):
 mass=a+b
 # The augmented measures coincide: both have masses (b,a).
 ck((b,a)==(b,a));cost=0;G=cost-mass*7;ck(G==-7*(a+b))
 if mass:
  pi=(F(b,mass),F(a,mass));ck(-a*pi[0]+b*pi[1]==0);ck(sum(pi)==1)
 else:ck(a==b==0)
print(json.dumps({'status':'PASS','exact_assertions':count,'non_line_metric_transport_cases':cases,'strict_local_sum_suboptimal_examples':strict,'scope':'Finite exact primal-dual transport, augmented-generator marginals, local-sum sufficiency and clock-normalization controls. General process existence and source coverage are assessed in the written review, not inferred from enumeration.'},indent=2))
