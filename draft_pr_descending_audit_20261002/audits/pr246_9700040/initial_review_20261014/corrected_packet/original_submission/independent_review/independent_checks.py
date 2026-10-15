#!/usr/bin/env python3
"""Independent finite controls, using cell-poset linear extensions and direct LIS.
No author module or stochastic simulation is used. These are controls, not the
proof of stationarity, uniqueness, or the infinite joint-law formula.
"""
from functools import lru_cache
from itertools import permutations,product
from fractions import Fraction as Q
from math import factorial
from collections import Counter
import json
C=Counter()
def ck(x,k):
 assert x,k
 C[k]+=1
@lru_cache(None)
def parts(n,cap=None):
 if n==0:return ((),)
 return tuple((a,)+b for a in range(1,min(n,cap or n)+1) for b in parts(n-a,a))
def sub(a,b):return len(b)<=len(a) and all(b[i]<=a[i] for i in range(len(b)))
def tr(a):return tuple(sum(v>=j for v in a) for j in range(1,max(a,default=0)+1))
@lru_cache(None)
def tab(a,b=()):
 if not sub(a,b):return 0
 cells=[(i,j) for i,v in enumerate(a) for j in range(b[i] if i<len(b) else 0,v)]
 need=[]
 for i,j in cells:
  # Full row/column partial order, not a corner-removal recurrence.
  need.append(sum(1<<k for k,(r,c) in enumerate(cells) if (r==i and c<j) or (c==j and r<i)))
 @lru_cache(None)
 def f(mask):
  if mask==(1<<len(cells))-1:return 1
  return sum(f(mask|(1<<k)) for k,n in enumerate(need) if not mask>>k&1 and n&mask==n)
 return f(0)
def det(a):
 n=len(a);s=Q(0)
 for p in permutations(range(n)):
  v=Q((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
  for i in range(n):v*=a[i][p[i]]
  s+=v
 return s
def D(a,b,t=Q(1),dim=None):
 if not sub(a,b):return Q(0)
 n=max(len(a),len(b)) if dim is None else dim
 aa=a+(0,)*(n-len(a));bb=b+(0,)*(n-len(b))
 return det([[Q(0) if (r:=aa[i]-bb[j]-i+j)<0 else t**r/factorial(r) for j in range(n)] for i in range(n)])
shapes=[p for n in range(7) for p in parts(n)]
for a in shapes:
 for b in shapes:
  if not sub(a,b):continue
  d=sum(a)-sum(b)
  for t in (Q(0),Q(2,5),Q(3,2)):
   expected=Q(tab(a,b),factorial(d))*t**d
   ck(D(a,b,t)==expected,'factorial_determinant_cell_poset')
   ck(D(tr(a),tr(b),t)==expected,'transpose_cell_poset')
  if len(a)<4:ck(D(a,b,dim=4)==D(a,b),'zero_padding_leibniz')
for n in range(8):ck(sum(tab(p)**2 for p in parts(n))==factorial(n),'tableau_bijection_normalization')
def lis(p):
 # Quadratic dynamic programming, independent of patience piles / RSK.
 d=[]
 for j,v in enumerate(p):d.append(1+max((d[i] for i in range(j) if p[i]<v),default=0))
 return max(d,default=0)
# Exhaust all permutations and direct time-sweep pile mechanics, including
# finite-k truncation and unequal rational event time/space coordinates.
for n in range(7):
 for p in permutations(range(1,n+1)):
  tops=[]
  for u in sorted(range(1,n+1),key=lambda z:p[z-1]):
   j=next((j for j,z in enumerate(tops) if z>u),len(tops))
   if j==len(tops):tops.append(u)
   else:tops[j]=u
  for cut in range(n+1):ck(sum(z<=cut for z in tops)==lis(p[:cut]),'time_sweep_vs_direct_prefix_LIS')
  # Conjugate event histories at v=1,...,n using Y(v)=v*Z(v).
  z=[];y=[];old=Q(1)
  for v in range(1,n+1):
   u=Q(p.index(v)+1);y=[q*v/old for q in y]
   j=next((j for j,q in enumerate(y) if q>u*v),len(y))
   if j==len(y):y.append(u*v)
   else:y[j]=u*v
   j=next((j for j,q in enumerate(z) if q>u),len(z))
   if j==len(z):z.append(u)
   else:z[j]=u
   ck(y==[v*q for q in z],'exact_log_time_geometry')
   old=Q(v)
# All three-block shape-chain weights vs directly counted LIS constraints.
queries=((1,2,3),(3,1,2),(4,2,3),(2,3,2),(1,1,1),(3,3,3))
deltas=(Q(1,3),Q(1,2),Q(2,3))
raw={r:[Q(0)]*7 for r in queries}
for n in range(7):
 for a in range(n+1):
  for b in range(a,n+1):
   ds=(a,b-a,n-b);h=Counter()
   for p in permutations(range(1,n+1)):
    h[(lis(p[:a]),lis(p[:b]),lis(p))]+=1
   for rs in queries:
    direct=sum(v for ls,v in h.items() if all(l<r for l,r in zip(ls,rs)))
    count=0
    for l1 in parts(a):
     if max(l1,default=0)>=rs[0]:continue
     for l2 in parts(b):
      if not sub(l2,l1) or max(l2,default=0)>=rs[1]:continue
      for l3 in parts(n):
       if sub(l3,l2) and max(l3,default=0)<rs[2]:count+=tab(l3)*tab(l1)*tab(l2,l1)*tab(l3,l2)
    ck(direct==count,'joint_three_prefix_count_arbitrary_indices')
    factor=Q(1,factorial(n))
    for d,t in zip(ds,deltas):factor*=t**d/factorial(d)
    raw[rs][n]+=direct*factor
for n in range(7):
 # Unconstrained total weight recovered independently by multinomial expansion.
 total=Q(0)
 for a in range(n+1):
  for b in range(n-a+1):
   ds=(a,b,n-a-b);v=Q(1)
   for d,t in zip(ds,deltas):v*=t**d/factorial(d)
   total+=v
 ck(total==sum(deltas)**n/factorial(n),'independent_Poisson_normalizer')
 for rs in queries:ck(0<=raw[rs][n]<=total,'raw_probability_coefficients_bounded')
# Exact certificate inequalities for every possible omitted constrained fraction
# in a rational grid. This checks both the unknown exponential normalizer and
# omitted constrained mass together, including W=0,T and E=0,R.
for T in (Q(1),Q(7,3),Q(5)):
 for R in (Q(1,100),Q(2,3),Q(9)):
  for wi,ei,qi in product(range(6),repeat=3):
   W=T*wi/5;E=R*ei/5;H=E*qi/5;P=(W+H)/(T+E)
   ck(W/(T+R)<=P<=(W+R)/(T+R),'rational_enclosure_all_tail_fractions')
for x in (Q(1,10),Q(7,3),Q(12)):
 for N in range(13):
  if N+2<=x:continue
  first=x**(N+1)/factorial(N+1);q=x/(N+2);R=first/(1-q)
  partial=sum((x**n/factorial(n) for n in range(N+1,N+60)),Q(0))
  ck(partial<R,'exponential_tail_geometric_control')
  for j in range(20):ck(x/(N+2+j)<=q,'all_following_tail_ratios_bounded')
# Exact Jacobian identity on positive rational points: du/dx=1/v,
# du/ds=-u; dv/dx=0, dv/ds=v for u=x exp(-s),v=exp(s).
for x,v in product((Q(1,4),Q(1),Q(7)),repeat=2):
 ck(Q(1,v)*v-(-x/v)*0==1,'unit_area_jacobian')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'three_thresholds':['1/3','5/6','3/2'],'raw_coefficients':{str(r):[str(v) for v in vs] for r,vs in raw.items()},'scope':'Finite independent algebra and enumeration only; analytic and source conclusions are in INDEPENDENT_REVIEW.md.'},indent=2))
