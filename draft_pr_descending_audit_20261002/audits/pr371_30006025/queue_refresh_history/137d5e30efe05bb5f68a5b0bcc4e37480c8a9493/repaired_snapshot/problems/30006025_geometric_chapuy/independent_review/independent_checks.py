#!/usr/bin/env python3
"""Supplementary exact checks independent of the author implementations."""
from fractions import Fraction as Q
from itertools import product,combinations
from math import comb
import json
counts={}
def ck(v,k):
 assert v,k
 counts[k]=counts.get(k,0)+1
def add(a,b):
 c=dict(a)
 for e,x in b.items():c[e]=c.get(e,Q(0))+x
 return {e:x for e,x in c.items() if x}
def mul(a,b):
 c={}
 for e,x in a.items():
  for f,y in b.items():c[e+f]=c.get(e+f,Q(0))+x*y
 return {e:x for e,x in c.items() if x}
def mm(a,b):return [[add(mul(a[i][0],b[0][j]),mul(a[i][1],b[1][j])) for j in range(2)] for i in range(2)]
# Nonuniform positive integer side weights and signed rational turns.
for n in range(2,10):
 for seed in range(17):
  weights=[1+(seed+2*j)%4 for j in range(n)]
  rots=[];A=[[{0:Q(1)},{}],[{},{0:Q(1)}]]
  for j,w in enumerate(weights):
   t=Q(((seed+j)%7)-3,5);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
   ck(c>0 and c*c+s*s==1,'rotation')
   B=[[{w:c},{w:s}],[{-w:-s},{-w:c}]];A=mm(A,B);rots.append([[c,s],[-s,c]])
  trace=add(A[0][0],A[1][1]);direct={}
  for bits in product(range(2),repeat=n):
   exponent=sum((1 if b==0 else -1)*w for b,w in zip(bits,weights))
   coef=Q(1)
   for j in range(n):coef*=rots[j][bits[j]][bits[(j+1)%n]]
   direct[exponent]=direct.get(exponent,Q(0))+coef
  direct={e:c for e,c in direct.items() if c}
  ck(trace==direct,'weighted_trace_expansion')
  leading=Q(1)
  for b in rots:leading*=b[0][0]
  ck(trace[sum(weights)]==leading>0,'unique_largest_exponent')
  ck(max(trace)>0 and max(trace)==sum(weights),'nonconstant_trace')
# Dirichlet rank means via integrated inclusion-exclusion, plus full top-k telescoping.
for E in range(1,46):
 H=[Q(0)]
 for j in range(1,E+1):H.append(H[-1]+Q(1,j))
 rank=[]
 for j in range(1,E+1):
  v=sum((Q((-1)**(r-j)*comb(E,r)*comb(r-1,j-1),r*E) for r in range(j,E+1)),Q(0))
  ck(v==(H[E]-H[j-1])/E,'integrated_simplex_rank')
  rank.append(v)
 for k in range(E+1):
  v=sum(rank[:k],Q(0));ck(v==Q(k,E)*(1+H[E]-H[k]),'top_k_mean')
  ck(0<=v<=1,'mean_bounds')
# Exhaust every positive composition of a small total, every changed-edge set,
# and both decreases and increases, to test adaptation-independent domination.
def compositions(total,E):
 if E==1:
  yield(total,);return
 for a in range(1,total-E+2):
  for tail in compositions(total-a,E-1):yield(a,)+tail
cases=0
for E in range(1,5):
 for total in range(E,11):
  for raw in compositions(total,E):
   x=[Q(v,total) for v in raw]
   for mask in range(1<<E):
    selected=[i for i in range(E) if mask>>i&1];k=len(selected);top=sum(sorted(x,reverse=True)[:k],Q(0))
    for C in [Q(1),Q(3,2),Q(3)]:
     y=[v*(C if (i+total)%2 else Q(1,2)) if i in selected else v for i,v in enumerate(x)]
     net=sum(y)-1
     ck(net<=(C-1)*top,'adaptive_budget')
     if net>0:ck(max(b/a for a,b in zip(x,y))>=1+net/top,'random_stretch')
     cases+=1
# Exact all-genus threshold certificates and Poisson count-law bound.
ck(Q(157,50)**2*11>108,'genus_12_exclusion')
ck(Q(22,7)**2*10<99,'genus_11_not_excluded')
ck(Q(157,50)**2>9,'threshold_monotonicity')
ck(Q(157,150)**2*Q(99,100)>Q(26,25)**2,'uniform_delta')
for g in range(2,1001):
 N=12*g-6;area=4*(g-1);orb=Q(1,3)-Q(2,N)
 ck(area/orb==N,'triangle_cover_index')
 ck(N-2-Q(2*N,3)==area,'smooth_polygon_area')
ck((1-Q(1,2)**2)/4==Q(3,16),'poisson_first_term')
ck(Q(3,16)/(1+Q(3,16))==Q(3,19),'poisson_strict_gap')
ck(1+Q(1,8)/(1-Q(1,48))<Q(4,3),'systole_cosh_bound')
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'by_family':counts,'adaptive_controls':cases,'scope':'Exact finite algebra controls only; the source/proof audit supplies the universal geometric and probabilistic reasoning.'},indent=2,sort_keys=True))
