#!/usr/bin/env python3
"""Exact finite orbit-surgery controls; no assertion of source-wide stability."""
from itertools import permutations,combinations,product
from fractions import Fraction
from collections import Counter
import json
C=Counter()
def ck(v,k):
 C[k]+=1
 if not v:raise AssertionError(k)
def compression(p,X):
 X=tuple(X);ix={x:i for i,x in enumerate(X)};c=[]
 for x in X:
  y=p[x]
  while y not in ix:y=p[y]
  c.append(ix[y])
 return tuple(c)
def orbits(gens):
 left=set(range(len(gens[0])));ans=[]
 while left:
  O={min(left)};front=list(O)
  while front:
   x=front.pop()
   for p in gens:
    y=p[x]
    if y not in O:O.add(y);front.append(y)
  ans.append(O);left-=O
 return ans
def mismatch(p,q):return sum(a!=b for a,b in zip(p,q))
models=0
for m in range(1,5):
 ps=list(permutations(range(m)))
 for gens in product(ps,repeat=2):
  os=orbits(gens)
  for n in range(1,m+1):
   for X in combinations(range(m),n):
    Xset=set(X);B=set(range(m))-Xset;k=m-n;ix={x:i for i,x in enumerate(X)}
    for mask in range(1<<len(os)):
     U=set().union(*(O for i,O in enumerate(os) if mask>>i&1)) if mask else set()
     D=len(U)
     if D<k:continue
     models+=1;T=set(range(m,m+D-k));V=(set(range(m))-U)|T;I=Xset-U
     th={x:x for x in I};th.update(zip(sorted(Xset-I),sorted(V-I)))
     back={y:x for x,y in th.items()}
     ck(len(V)==n and set(th)==Xset and set(th.values())==V,'transport_bijection')
     for p in gens:
      tau=tuple(ix[back[p[th[x]] if th[x]<m else th[x]]] for x in X)
      ck(sorted(tau)==list(range(n)),'transport_permutation')
      err=mismatch(tau,compression(p,X));bound=D+k-2*len(B&U)
      ck(err<=bound,'overlap_sensitive_surgery_bound')
      ck(err<=D+k,'packing_surgery_bound')
# All finite integer orbit multisets up to total size 12.
def parts(n,lo=1):
 if not n:yield ()
 for x in range(lo,n+1):
  for rest in parts(n-x,x):yield (x,)+rest
for M in range(1,13):
 for sizes in parts(M):
  sums={0}
  for s in sizes:sums|={v+s for v in tuple(sums)}
  for k in range(M):
   P=min(v for v in sums if v>=k)
   ck(k<=P<=M,'packing_minimum')
   for L in range(1,M+1):
    mass=sum(s for s in sizes if s<=L)
    if mass>=k:ck(P<=k+L-1 if k else P==0,'small_orbit_greedy_bound')
# Weighted good/bad decomposition, with exact rational eta, no optimization inference.
for blocks in range(1,5):
 for ns in product(range(1,4),repeat=blocks):
  for ks in product(range(3),repeat=blocks):
   n=sum(ns);k=sum(ks)
   for eta in [Fraction(1,4),Fraction(1,2),Fraction(1),Fraction(2)]:
    bad=sum(a for a,b in zip(ns,ks) if Fraction(b,a)>eta)
    ck(Fraction(bad,1)<=Fraction(k,1)/eta,'bad_orbit_mass')
    for t in [Fraction(0),Fraction(1,3),Fraction(1)]:
     weighted=(n-bad)*t+bad
     ck(weighted/n<=t+Fraction(k,n)/eta,'transitive_modulus_arithmetic')
# An actual large-orbit/small-reservoir example: delete from the giant orbit,
# remove a disjoint two-point orbit, and transplant labels.
p=(1,2,3,4,5,0,7,6);X=(0,1,2,3,4,6,7);B={5};U={6,7};m=8;D=2;k=1
T={8};V=(set(range(m))-U)|T;I=set(X)-U
th={x:x for x in I};th.update(zip(sorted(set(X)-I),sorted(V-I)));back={y:x for x,y in th.items()};ix={x:i for i,x in enumerate(X)}
tau=tuple(ix[back[p[th[x]] if th[x]<m else th[x]]] for x in X)
err=mismatch(tau,compression(p,X))
ck(not (B&U),'reservoir_disjoint_from_deletion')
ck(err<=D+k,'disjoint_reservoir_construction')
print(json.dumps({'scope':'Finite controls only; original KOU-21.85 unresolved','checks_by_kind':dict(sorted(C.items())),'total_assertions':sum(C.values()),'orbit_surgery_models':models,'disjoint_reservoir_example_mismatches':err},indent=2,sort_keys=True))
