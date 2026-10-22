#!/usr/bin/env python3
from itertools import permutations,product,combinations
from fractions import Fraction as F
from math import factorial,comb
from collections import Counter
import json
C=Counter()
def ck(v,k):
 C[k]+=1
 if not v:raise AssertionError(k)
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def orbits(gs):
 left=set(range(len(gs[0])));out=[]
 while left:
  O={min(left)};todo=list(O)
  while todo:
   x=todo.pop()
   for p in gs:
    y=p[x]
    if y not in O:O.add(y);todo.append(y)
  out.append(O);left-=O
 return out
def comp(p,n):
 ans=[]
 for x in range(n):
  y=p[x]
  while y>=n:y=p[y]
  ans.append(y)
 return tuple(ans)
models=0
for M in range(2,5):
 ps=list(permutations(range(M)))
 for pos in product(ps,repeat=2):
  if len(orbits(pos))!=1:continue
  rho=list(pos)+[inv(p) for p in pos]
  for n in range(1,M):
   ts=list(permutations(range(n)))
   for pos_t in product(ts,repeat=2):
    models+=1;tau=list(pos_t)+[inv(p) for p in pos_t]
    diag=[tuple(p[y]*n+q[x] for y in range(M) for x in range(n)) for p,q in zip(rho,tau)]
    A={x*n+x for x in range(n)};os=orbits(diag);var=F(0);proj=[F(0)]*(M*n)
    for O in os:
     a=len(A&O);d=len({v%n for v in O})
     ck(len(O)%d==0 and len(O)//d>=2,'product_orbit_fiber')
     ck(2*a<=len(O),'graph_occupancy_half')
     var+=F(a)-F(a*a,len(O))
     for v in O:proj[v]=F(a,len(O))
    ck(2*var>=n,'projection_variance_bound')
    centered=[F(v in A)-proj[v] for v in range(M*n)]
    ck(sum(v*v for v in centered)==var,'projection_exact_variance')
    for s,(p,q,r) in enumerate(zip(rho,tau,diag)):
     e=sum(p[x]!=q[x] for x in range(n));boundary=len({r[x] for x in A}^A)
     ck(boundary==2*e,'graph_energy_identity')
     energy=sum((centered[r[v]]-centered[v])**2 for v in range(M*n))
     ck(energy==boundary,'projection_preserves_energy')
# Rational certificates for numerical constants in the unbounded existence proof.
ck(sum(F(5)**j/factorial(j) for j in range(7))>100,'exp5_lower')
x=F(5,4);N=12
upper=sum(x**j/factorial(j) for j in range(N+1))+x**(N+1)/factorial(N+1)/(1-x/F(N+2))
ck(upper<F(7,2),'exp_five_quarters_upper')
ck(1+4*F(3,50)<F(5,4),'entropy_exponent_margin')
ck(F(74,25)>F(17,6),'power_exponent_margin')
ck(2**17>7**6,'power_integer_certificate')
# Exact finite union probabilities: each independent permutation maps B uniformly.
for M in list(range(2,41))+[64,100,128,200]:
 total=F(0)
 for a in range(1,M//2+1):
  # j<a/100, exactly, including the zero-boundary case.
  jmax=(a-1)//100
  prob=F(sum(comb(a,j)*comb(M-a,j) for j in range(jmax+1)),comb(M,a))
  total+=comb(M,a)*prob**4
 ck(total<1,'finite_exact_union_bound')
# Explicit small witnesses and their puncture graph Rayleigh bounds.
witnesses=[]
for M in [8,11]:
 pos=[tuple((x+1)%M for x in range(M)),tuple((-x)%M for x in range(M)),tuple((x^1) if M==8 else (2*x)%M for x in range(M)),tuple((x+3)%M for x in range(M))]
 for p in pos:ck(sorted(p)==list(range(M)),'explicit_permutation')
 for a in range(1,M//2+1):
  for B0 in combinations(range(M),a):
   B=set(B0);out=max(len({p[x] for x in B}-B) for p in pos)
   ck(100*out>=a,'explicit_boundary_condition')
 rho=pos+[inv(p) for p in pos];n=M-1;tp=[comp(p,n) for p in pos];tau=tp+[inv(p) for p in tp]
 diag=[tuple(p[y]*n+q[x] for y in range(M) for x in range(n)) for p,q in zip(rho,tau)]
 A={x*n+x for x in range(n)};var=sum(F(len(A&O))-F(len(A&O)**2,len(O)) for O in orbits(diag))
 energy=F(sum(2*sum(p[x]!=q[x] for x in range(n)) for p,q in zip(rho,tau)),8)
 ck(var>=F(n,2),'explicit_projection_variance')
 ck(energy/var<=F(4,n),'explicit_joint_rayleigh_upper')
 ck(all(comp(p,n)==q for p,q in zip(rho,tau)),'zero_generator_repair_error')
 witnesses.append({'M':M,'n':n,'centered_graph_variance':str(var),'joint_rayleigh_quotient':str(energy/var)})
print(json.dumps({'scope':'Exact finite controls; unbounded existence is proved in prose; original problem unresolved','checks_by_kind':dict(sorted(C.items())),'total_assertions':sum(C.values()),'diagonal_action_models':models,'explicit_witnesses':witnesses},indent=2,sort_keys=True))
