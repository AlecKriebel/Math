#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import json
c=0
def ck(v):
 global c
 assert v
 c+=1
def matmul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def transpose(a):return list(map(list,zip(*a)))
T=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
Q=[[F(3,5),F(4,5),F(0)],[-F(12,25),F(9,25),F(4,5)]]
for t in [T,Q]:
 ck(matmul(t,transpose(t))==[[F(1),F(0)],[F(0),F(1)]])
 D=len(t[0])
 for x in product(range(-3,4),repeat=2):
  v=[sum(t[i][j]*x[i] for i in range(2)) for j in range(D)]
  ck(sum(z*z for z in v)==sum(z*z for z in x))
 for seed in range(1,20):
  G=[[F((seed+2*i+3*j)%7-3) for j in range(D)] for i in range(4)]
  A=matmul(G,transpose(t))
  for x in [(F(1),F(0)),(F(3,5),F(4,5)),(F(-4,5),F(3,5))]:
   v=[sum(t[i][j]*x[i] for i in range(2)) for j in range(D)]
   for u in [(F(1),F(0),F(0),F(0)),(F(0),F(3,5),F(4,5),F(0))]:
    lhs=sum(u[i]*A[i][j]*x[j] for i in range(4) for j in range(2))
    rhs=sum(u[i]*G[i][j]*v[j] for i in range(4) for j in range(D))
    ck(lhs==rhs)
# Actual failure of coordinate unconditionality of the rotated Laplace density.
def l1_transpose(x):return sum(abs(sum(T[i][j]*x[i] for i in range(2))) for j in range(2))
ck(l1_transpose((1,2))==F(13,5));ck(l1_transpose((-1,2))==3)
ck(l1_transpose((1,2))!=l1_transpose((-1,2)))
# The deterministic tail-count bound needs no independence.
for w in product(range(-2,3),repeat=4):
 ss=sorted((x*x for x in w),reverse=True)
 for m in range(1,5):
  for a in (F(0),F(1,2),F(1),F(3,2),F(2)):
   ck(sum(ss[:m])<=m*a*a+sum(max(F(0),F(x*x)-a*a) for x in w))
# Elementary denominator bound for the Laplace MGF proof.
for j in range(1,41):
 v=F(j,100)
 ck(v<=F(1,2));ck(2-F(1,1-v)>=0)
print(json.dumps({'status':'PASS','exact_assertions':c,'scope':'Finite algebra and deterministic tail-count controls for the common-quotient theorem; no Monte Carlo or original-conjecture claim.'},sort_keys=True,indent=2))
