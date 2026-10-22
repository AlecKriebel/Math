#!/usr/bin/env python3
"""Exact finite controls for shielding and Poisson moment/truncation algebra."""
from fractions import Fraction as F
from itertools import combinations
from math import comb,factorial
import json,random
checks=0

def ok(x):
 global checks
 assert x
 checks+=1

def dot(x,y):return sum(a*b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def norm(x):return dot(x,x)
def edge(P,i,j):
 # The perpendicular bisector is c+t*w; all empty-circle tests are linear in t.
 u=P[i];v=P[j];c=tuple((a+b)/2 for a,b in zip(u,v));w=(-(v[1]-u[1]),v[0]-u[0]);lo=None;hi=None
 for z in P:
  dz=sub(z,u);a=2*dot(w,dz);b=norm(z)-norm(u)-2*dot(c,dz)
  if not a:
   if b<0:return False
  elif a>0:hi=b/a if hi is None else min(hi,b/a)
  else:lo=b/a if lo is None else max(lo,b/a)
 return lo is None or hi is None or lo<=hi

def score(P):
 N=[i for i in range(1,len(P)) if edge(P,0,i)]
 return (len(N),sum(edge(P,i,j) for i,j in combinations(N,2))),N

# Algebraic geometry constants and cell-redundancy distances.
for d in range(1,101):
 ok((F(9,8)/F(1,8))**d==9**d)
 ok(1-F(1,4)**2/2>F(7,8)) # the covering chord implies angle < pi/6
 ok(F(1,8)/F(1,2)==F(1,4));ok(F(1,2)+F(1,8)<1)
 ok(F(3,4)-F(1,8)>F(1,8));ok(F(1,4)+F(1,8)<1)
# Stirling recurrence and exact exponential-tilt coefficients through degree 12.
S=[[0]*15 for _ in range(15)];S[0][0]=1
for r in range(1,15):
 for j in range(1,r+1):S[r][j]=j*S[r-1][j]+S[r-1][j-1]
for r in range(1,13):
 for n in range(31):
  ok(sum(S[r][j]*factorial(n)//factorial(n-j) for j in range(1,min(n,r)+1))==n**r)
 for q in range(41):
  t=F(q,7);ok(sum(S[r][j]*t**j for j in range(1,r+1))<=sum(S[r])*(1+t)**r)
 for n in range(25):
  # [mu^n] e^mu T_r(2mu), compared with the Poisson sum e^-mu Σ n^r (2mu)^n/n!.
  left=sum(F(S[r][j]*2**j,factorial(n-j)) for j in range(1,min(n,r)+1))
  right=sum(F((-1)**(n-a)*a**r*2**a,factorial(n-a)*factorial(a)) for a in range(n+1))
  ok(left==right)
for m in range(31):
 for n in range(61):ok(F(n>m)<=F(2)**(n-m))
# Exact graph scores are stable under exterior insertions on these shielded examples.
rng=random.Random(571003)
for sample in range(13):
 P=[(F(0),F(0))]+[(F(i)+F(rng.randrange(-100,101),10000),F(j)+F(rng.randrange(-100,101),10000)) for i in range(-3,4) for j in range(-3,4) if (i,j)!=(0,0)]
 before,N=score(P)
 Q=P+[(F(20*i)+F(sample,1000),F(20*j)-F(sample,900)) for i,j in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1)]]
 after,NN=score(Q)
 ok(before==after);ok(N==NN)
 for i,j in combinations([0]+N,2):ok(edge(P,i,j)==edge(Q,i,j))
 ok(before[1]<=comb(before[0],2))
print(json.dumps(dict(status='PASS',assertions=checks,shielded_planar_examples=13,scope='finite exact controls; analytic proof supplies uniform stabilization probability and integration bias'),sort_keys=True,indent=2))
