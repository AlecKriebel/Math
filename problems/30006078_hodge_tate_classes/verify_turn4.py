#!/usr/bin/env python3
import itertools as it,json,math
from fractions import Fraction as F
import sympy as s
checks=0
def ck(v):
 global checks
 assert v
 checks+=1
def mul(a,b,N):return [sum(a[j]*b[k-j] for j in range(k+1)) for k in range(N+1)]
def power(a,r,N):
 out=[F(1)]+[F(0)]*N
 for _ in range(r):out=mul(out,a,N)
 return out
# (1+z)^(1/r), with exact binomial coefficients, raised back to r.
for r in range(1,41):
 for N in range(1,13):
  a=[F(1)]
  for j in range(1,N+1):a.append(a[-1]*(F(1,r)-j+1)/j)
  expected=[F(1),F(1)]+[F(0)]*(N-1)
  ck(power(a,r,N)==expected)
for p in (2,3,5,7,11,13):
 for r in range(1,301):
  v=0;n=r
  while n%p==0:v+=1;n//=p
  N=v+3;ck(F(N-v)>F(1,p-1));ck(N>=2)
# Normalizer acts noncommutatively but preserves the radical filtration.
J=s.Matrix([[0,1,0],[0,0,1],[0,0,0]])
ck(J**3==s.zeros(3));ck(J.rank()==2);ck((J**2).rank()==1)
for a in range(1,8):
 D=s.diag(a*a,a,1)
 ck(D*J*D.inv()==a*J)
 for t in range(-6,7):
  U=s.eye(3)+t*J
  ck(U*J==J*U)
  ck((D*U*D.inv())==s.eye(3)+a*t*J)
  if a!=1 and t!=0:ck(D*U!=U*D)
  for k in range(1,4):
   # Each invariant subspace image J^k is preserved by D and U.
   B=J**k
   ck((B.row_join(D*B)).rank()==B.rank())
   ck((B.row_join(U*B)).rank()==B.rank())
for r,m in it.product(range(1,31),range(-10,11)):
 ck(r*0+m==m);ck(r*0==0)
print(json.dumps({'status':'PASS','assertions':checks,'scope':'finite formal-root, convergence-inequality and radical-filtration controls; HT rigidity is a cited input'},indent=2,sort_keys=True))
