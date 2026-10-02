#!/usr/bin/env python3
from fractions import Fraction as Q
from itertools import product
import json,random
checks=0
def ck(x):
 global checks
 assert x;checks+=1

def dot(a,b):return sum(x*y for x,y in zip(a,b))
models=0
for e in range(1,6):
 for z in product((-1,0,1),repeat=e):
  if not any(z):continue
  a=list(z)+[0];b=[0]+list(z);aa=dot(a,a);bb=dot(b,b);ab=dot(a,b);D=aa*bb-ab*ab;ck(D>0);models+=1
  for p,q in [(0,0),(1,0),(0,1),(2,-1)]:
   alpha=Q(bb*p-ab*q,D);beta=Q(aa*q-ab*p,D);w=[alpha*x+beta*y for x,y in zip(a,b)];ck(dot(a,w)==p);ck(dot(b,w)==q)
  # Explicit zero-stratum attachment with long variable zero.
  for t in (Q(0),Q(1,3),Q(1)):
   zz=[t*x for x in z];w=[Q(0)]*(e+1);ck(dot(zz,w[:-1])==dot(zz,w[1:])==0)
# Strict equivalence corresponds to separate invertible changes of the variable blocks.
rng=random.Random(34504)
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def mv(A,x):return [dot(row,x) for row in A]
def transpose(A):return list(map(list,zip(*A)))
for m in range(1,6):
 for n in range(1,6):
  for _ in range(5):
   A=[[rng.randrange(-2,3) for _ in range(n)] for _ in range(m)]
   U=[[int(i==j) for j in range(m)] for i in range(m)];V=[[int(i==j) for j in range(n)] for i in range(n)]
   if m>1:U[0][1]=2
   if n>1:V[0][1]=-1
   u=[rng.randrange(-2,3) for _ in range(m)];v=[rng.randrange(-2,3) for _ in range(n)]
   x=mv(transpose(U),u);y=mv(V,v);ck(dot(x,mv(A,y))==dot(u,mv(mm(mm(U,A),V),v)))
print(json.dumps({'assertions':checks,'nonzero_short_block_vectors':models,'scope':'Exact singular-block full-row-rank, solution-section, attachment and strict-equivalence identities. Existence of real Kronecker decomposition is a credited theorem, not a numerical assertion.'},indent=2))
