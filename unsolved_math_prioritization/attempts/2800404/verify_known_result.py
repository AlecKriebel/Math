#!/usr/bin/env python3
"""Exact finite controls of the published-moment specialization, not a substitute proof."""
from fractions import Fraction as F
from itertools import product
from math import comb,ceil
import json
checks=0
def ok(x):
 global checks
 assert x
 checks+=1
def gm(k):
 if k%2:return 0
 z=1
 for a in range(1,k,2):z*=a
 return z
def mixed(a,b):return sum(comb(b,j)*(-1)**(b-j)*gm(a+2*j) for j in range(b+1))
ps=[F(1,8),F(1,3),F(1,2),F(2,3),F(7,8),F(1)]
for p in ps:
 for a,b in product(range(9),range(7)):
  if a%2:v=F(0)
  elif a>0:v=p*(1-p)**b
  elif b==0:v=F(1)
  else:v=p*(1-p)**b+(1-p)*(-p)**b
  g=mixed(a,b)
  if a%2 or (a,b)==(0,1):ok(v==0 and g==0)
  elif (a,b)==(0,0):ok(v==1 and g==1)
  else:ok(g>=1);ok(abs(v)<=p*g)
def pairings(xs):
 if not xs:yield [];return
 x=xs[0]
 for j in range(1,len(xs)):
  y=xs[j]
  for tail in pairings(xs[1:j]+xs[j+1:]):yield [(x,y)]+tail
def wishart(r,c,k):
 if not k:return r
 total=0
 for pairs in pairings(list(range(2*k))):
  row=list(range(k));col=list(range(k))
  def find(A,x):
   while A[x]!=x:x=A[x]
   return x
  for x,y in pairs:
   rx=(x//2+(x%2))%k;ry=(y//2+(y%2))%k
   row[find(row,rx)]=find(row,ry)
   col[find(col,x//2)]=find(col,y//2)
  nr=len({find(row,i) for i in range(k)});nc=len({find(col,i) for i in range(k)})
  total+=r**nr*c**nc
 return total
def centered_wishart(r,c,q):return sum(comb(q,j)*(-c)**(q-j)*wishart(r,c,j) for j in range(q+1))
def mul(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def sparse_trace(d,m,p,q):
 total=F(0)
 for xs in product((-1,0,1),repeat=d*m):
  nz=sum(x!=0 for x in xs);prob=(p/2)**nz*(1-p)**(d*m-nz)
  if not prob:continue
  X=[xs[i*m:(i+1)*m] for i in range(d)]
  G=[[F(sum(a*b for a,b in zip(X[i],X[j])))-(m*p if i==j else 0) for j in range(d)] for i in range(d)]
  A=[[F(i==j) for j in range(d)] for i in range(d)]
  for _ in range(q):A=mul(A,G)
  total+=prob*sum(A[i][i] for i in range(d))
 return total
comparisons=0
for d,m in [(1,2),(2,2),(2,3)]:
 for p in ps:
  for q in [2,4]:
   r=ceil(d*p)+q-1;t=ceil(m*p)+q-1
   lhs=sparse_trace(d,m,p,q);rhs=min(F(d,r),F(m,t))*centered_wishart(r,t,q)
   ok(0<=lhs<=rhs);ok(r<=d*p+q and t<=m*p+q);comparisons+=1
# Conservative constant bound is entirely rational after sqrt(2)<3/2.
ok(F(10)*(F(1,100)+F(1,10000))==F(101,1000));ok(F(101,1000)<F(1,3))
ok(F(7,70000)==F(1,10000));ok(F(1)-F(1,70000)>F(2,3))
# Exact scalar good-probability control for d=s=1.
for m in range(2,1001):ok(F(m-1,m)**(m-1)>F(1,3))
# Range ambiguity witness: normalized scalar Gram 4N never lies within1/2 of1.
for n in range(1001):ok(abs(4*n-1)>=1)
print(json.dumps(dict(status='PASS_KNOWN_LEMMA_SPECIALIZATION_CONTROLS',assertions=checks,exact_trace_comparisons=comparisons,moment_orders=[2,4],scalar_binomial_parameters=999,source_author_turns=0,scope='exact finite controls; universal proof uses credited published lemmas'),indent=2,sort_keys=True))
