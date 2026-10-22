#!/usr/bin/env python3
"""Exact finite supplements to the uniform inequalities proved in TURN_2."""
from fractions import Fraction as F
from itertools import combinations,product
import json,random
checks=0;configs=0;dimensions=0

def ok(x):
 global checks
 assert x
 checks+=1

def dot(x,y):return sum(a*b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def norm(x):return dot(x,x)
def sites(d,k):
 V=[tuple(F(i==j) for j in range(d)) for i in range(k)]
 V=[(F(0),)*d]+V
 b=tuple(F(j<k,k+1) for j in range(d))
 G=[tuple(F(s*2*(j==r)) for j in range(d)) for r in range(k,d) for s in (-1,1)]
 return V+[b]+G

def center(d,k,i,j):
 if i==0:return tuple(F(1,2) if r==j-1 else F(-1) if r<k else F(0) for r in range(d))
 return tuple(F(2) if r in (i-1,j-1) else F(-2) if r<k else F(0) for r in range(d))

def project(c,u,v):
 w=sub(v,u);t=(norm(v)-norm(u)-2*dot(c,w))/(2*norm(w))
 return tuple(a+t*b for a,b in zip(c,w))

for d in range(2,19):
 for k in range(2,d+1):
  dimensions+=1;P=sites(d,k);h=F(1,1000*d*d)
  ok(len(P)==2*d-k+2);ok(2*h<F(1,k+1));ok(2*k*h<1)
  ok(4*h*h*d<=F(1,16));ok(5*h+8*d*h<=12*d*h)
  ok(7*h+144*d*h+12*d*h<=160*d*h<=F(2,25))
  ok(3*h+18*d*h<=20*d*h<=F(1,100))
  ok((1+2*h)/(1-2*d*h)<=2);ok(F(3,2)*h+4*d*h<=5*d*h)
  ok((2*k*k-3)*9-5*(k+1)**2==(k-2)*(13*k+16))
  ok((7*k*k-5*k-13)*9-5*(k+1)**2==(k-2)*(58*k+61))
  # A generating subset covers every index class in high dimensions.
  pairs=list(combinations(range(k+1),2)) if d<=8 else [(0,1),(1,2)]
  for i,j in pairs:
   c=center(d,k,i,j);r2=norm(sub(P[i],c))
   ok(norm(sub(P[j],c))==r2);ok(r2==(F(k)-F(3,4) if i==0 else 4*k-3))
   for z in range(len(P)):
    if z in (i,j):continue
    gap=norm(sub(P[z],c))-r2
    if z==k+1:expected=F(2*k*k-3,(k+1)**2) if i==0 else F(7*k*k-5*k-13,(k+1)**2)
    elif z>k+1:expected=4 if i==0 else 7
    elif i==0:expected=3
    else:expected=3 if z==0 else 8
    ok(gap==expected);ok(gap>=F(5,9))
  y=tuple(F(1,2) if r<k else F(0) for r in range(d))
  ok(norm(sub(P[k+1],y))-norm(sub(P[0],y))==-F(k*k,(k+1)**2))

# Exhaust all 2D cube corners and independently seeded rational perturbations.
rng=random.Random(30002957)
for d,k in [(2,2),(3,2),(3,3),(4,2),(4,3),(4,4),(5,2),(5,5)]:
 P=sites(d,k);h=F(1,1000*d*d)
 cases=product((-1,1),repeat=len(P)*d) if d==2 else [tuple(F(rng.randrange(-100,101),100) for _ in range(len(P)*d)) for __ in range(31)]
 for eps in cases:
  configs+=1;Q=[tuple(P[n][r]+h*eps[n*d+r] for r in range(d)) for n in range(len(P))]
  for i,j in combinations(range(k+1),2):
   c=center(d,k,i,j);cc=project(c,Q[i],Q[j]);r2=norm(sub(Q[i],cc))
   ok(norm(sub(Q[j],cc))==r2);ok(max(abs(a-b) for a,b in zip(c,cc))<=24*d*h)
   ok(max(map(abs,cc))<=3);ok(r2<=25*d)
   for z in range(len(P)):
    if z in (i,j):continue
    gap=norm(sub(Q[z],cc))-r2;old=norm(sub(P[z],c))-norm(sub(P[i],c))
    ok(abs(gap-old)<=160*d*h);ok(gap>0)
  # Solve the first k center coordinates with normal coordinates fixed at zero.
  A=[[2*(Q[i][r]-Q[0][r]) for r in range(k)]+[norm(Q[i])-norm(Q[0])] for i in range(1,k+1)]
  for j in range(k):
   p=next(r for r in range(j,k) if A[r][j]);A[j],A[p]=A[p],A[j]
   t=A[j][j];A[j]=[x/t for x in A[j]]
   for r in range(k):
    if r!=j:
     t=A[r][j];A[r]=[x-t*y for x,y in zip(A[r],A[j])]
  yy=tuple([A[j][-1] for j in range(k)]+[F(0)]*(d-k))
  ok(max(map(abs,yy))<=2)
  ok(norm(sub(Q[k+1],yy))<norm(sub(Q[0],yy)))
print(json.dumps(dict(status='PASS',assertions=checks,dimension_pairs=dimensions,perturbed_configurations=configs,scope='finite rational supplements; uniform all-perturbation and all-dimension statements are proved analytically'),indent=2,sort_keys=True))
