#!/usr/bin/env python3
"""Exact finite controls for the polynomial push-forward; no analytic surrogate."""
from itertools import product
from math import comb
from fractions import Fraction
import json,random
rng=random.Random(2302055)
checks=0
def ck(x):
 global checks
 assert x
 checks+=1
def mul(A,B):
 n=len(A);return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def eye(n):return [[int(i==j) for j in range(n)]for i in range(n)]
def add(A,B):return [[a+b for a,b in zip(r,s)]for r,s in zip(A,B)]
def scale(a,A):return [[a*x for x in r]for r in A]
def pmul(p,q):
 r=[0]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q):r[i+j]+=x*y
 return r
def polyroots(rs):
 p=[1]
 for r in rs:p=pmul(p,[-r,1])
 return p
def companion(rs):
 p=polyroots(rs);n=len(rs);A=[[0]*n for _ in range(n)]
 for i in range(1,n):A[i][i-1]=1
 for i in range(n):A[i][-1]=-p[i]
 return A
def kron(A,B):return [[a*b for a in r for b in s] for r in A for s in B]
def trace(A):return sum(A[i][i]for i in range(len(A)))
cases=0;repeated=0
for ds in [(1,1,1),(2,1,1),(2,2,1),(3,2,1),(2,2,2),(3,3,1),(3,2,2)]:
 for sample in range(12):
  roots=[[rng.randrange(-2,3) for _ in range(d)]for d in ds]
  repeated+=any(len(set(r))<len(r)for r in roots)
  C=[companion(r)for r in roots];d=ds[0]*ds[1]*ds[2];I=eye(d)
  A=[kron(kron(C[0],eye(ds[1])),eye(ds[2])),kron(kron(eye(ds[0]),C[1]),eye(ds[2])),kron(kron(eye(ds[0]),eye(ds[1])),C[2])]
  for i in range(3):
   for j in range(i):ck(mul(A[i],A[j])==mul(A[j],A[i]))
  terms=[(rng.randrange(-3,4),tuple(rng.randrange(3)for _ in range(3)))for _ in range(5)]
  M=scale(0,I)
  for c,alpha in terms:
   T=I
   for i,e in enumerate(alpha):
    for _ in range(e):T=mul(T,A[i])
   M=add(M,scale(c,T))
  vals=[sum(c*rs[0]**a[0]*rs[1]**a[1]*rs[2]**a[2]for c,a in terms)for rs in product(*roots)]
  Q=polyroots(vals);powers=I;sums=[0]
  for k in range(1,d+1):
   powers=mul(powers,M);sums.append(trace(powers));ck(sums[-1]==sum(v**k for v in vals))
  # Newton recurrence for characteristic coefficients, with multiplicity.
  cs=[Fraction(1)]
  for k in range(1,d+1):
   cs.append(-sum(cs[k-j]*sums[j]for j in range(1,k+1))/k)
   ck(cs[k]==Q[d-k]);ck(abs(cs[k])<=comb(d,k)*max(map(abs,vals))**k)
  cases+=1
print(json.dumps({'cases':cases,'cases_with_repeated_roots':repeated,'exact_assertions':checks,'degree_patterns':7,'analytic_claims_tested':False},indent=2))
