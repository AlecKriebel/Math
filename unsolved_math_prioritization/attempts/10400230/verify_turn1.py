#!/usr/bin/env python3
"""Exact finite controls for the proved wheel family; not universal coverage."""
from fractions import Fraction
from itertools import combinations
from collections import Counter
import json,math
checks=0
def ok(x):
 global checks
 assert x
 checks+=1
def det(M):
 A=[list(map(Fraction,r)) for r in M];v=Fraction(1)
 for k in range(len(A)):
  j=next((j for j in range(k,len(A)) if A[j][k]),None)
  if j is None:return 0
  if j!=k:A[k],A[j]=A[j],A[k];v=-v
  p=A[k][k];v*=p
  for j in range(k+1,len(A)):
   q=A[j][k]/p
   for l in range(k+1,len(A)):A[j][l]-=q*A[k][l]
 return v
def graph(a):
 E=[(0,1)]*a+[(0,2),(0,3),(0,4),(2,3),(3,4),(4,1)]
 path=[1]+list(range(5,a+4))+[2]
 E+=list(zip(path,path[1:]));return a+4,E
def connected(n,E,removed=None):
 vertices=set(range(n))-{removed};seen={next(iter(vertices))}
 while True:
  new=seen|{v for u,v in E if u in seen and v!=removed}|{u for u,v in E if v in seen and u!=removed}
  if new==seen:return seen==vertices
  seen=new
def trees(n,E):
 L=[[0]*n for _ in range(n)]
 for u,v in E:L[u][u]+=1;L[v][v]+=1;L[u][v]-=1;L[v][u]-=1
 return det([r[1:] for r in L[1:]])
E=[(0,i+1) for i in range(4)]+[(i+1,(i+1)%4+1) for i in range(4)]
c=Counter()
for subset in combinations(range(8),4):
 if connected(5,[E[i] for i in subset]):c[1+(0 in subset)-(4 in subset)]+=1
ok(c=={0:16,1:16,2:13});ok(sum(c.values())==45)
for a in range(1,42):
 n,E=graph(a);P=13*a*a+16*a+16
 ok(len(E)==2*a+6);ok(trees(n,E)==P);ok(P==(3*a)**2+(2*a+4)**2)
 for v in range(n):ok(connected(n,E,v))
 for j in range(len(E)):ok(connected(n,E[:j]+E[j+1:]))
 # Dual vertex IDs: U=0, F_i=1+i, D_j=4+j.
 dual=[(0,1)]*a+[(0,2),(0,3),(0,4),(1,2),(2,3),(3,4)]
 chain=[4]+list(range(5,a+4))+[1];dual+=list(zip(chain,chain[1:]))
 phi={0:0,1:1,2:4,3:3,4:2}
 for j in range(1,a):phi[4+j]=4+a-j
 normalize=lambda es:Counter(tuple(sorted(e)) for e in es)
 ok(normalize([(phi[u],phi[v]) for u,v in E])==normalize(dual))
for k in range(10001):
 a=6*k+1;D=52*k*k+28*k+5;N=9*D
 ok(N==13*a*a+16*a+16);ok(N==468*k*k+252*k+45)
 ok(D%8==5);ok(D%3 in (1,2));ok(math.isqrt(N)**2!=N)
 ok(math.gcd(3*a,2*a+4)==3);ok(N not in (1,9,49))
print(json.dumps(dict(status='PASS',assertions=checks,expanded_graphs=41,arithmetic_parameters=10001,base_tree_coefficients=dict(sorted(c.items())),scope='finite exact controls for a proved infinite family; not full target'),indent=2,sort_keys=True))
