#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
checks=0
def ck(v):
 global checks
 assert v
 checks+=1
def reps(A):
 R=Counter({0:1})
 for a in A:
  S=R.copy()
  for t,n in R.items():S[t+a]+=n
  R=S
 return R
sets=0
for mask in range(1<<11):
 A=[i+1 for i in range(11)if mask>>i&1];R=reps(A);m=max(R.values());ck(sum(R.values())==2**len(A));ck(m>=1)
 for a in range(1,12):
  if a not in A:
   T=reps(A+[a]);ck(m<=max(T.values())<=2*m)
   ck(all(T[x]==R[x]+R[x-a]for x in T))
 for X in range(1,12):
  B=[a for a in A if a<=X];M=max(reps(B).values());L=max([R[x]for x in range(X+1)]);ck(L<=M)
 sets+=1
windows=0
for L in range(1,9):
 for size in range(1,9):
  I=list(range(L+1,L+size+1));prob=F(0)
  for mask in range(1<<size):
   A=[];p=F(1)
   for j,a in enumerate(I):
    if mask>>j&1:A.append(a);p*=F(1,a)
    else:p*=F(a-1,a)
   if max(reps(A).values())>=2:prob+=p
  bound=F(1,L)
  for a in I:bound*=1+F(2,a)
  ck(prob<=bound);windows+=1
tensors=0
for n in range(1,13):
 target=sum(3*7**j for j in range(n));seen=set()
 for choices in product(range(2),repeat=n):
  B=tuple(a for j,b in enumerate(choices)for a in ([3*7**j]if b==0 else[7**j,2*7**j]))
  ck(sum(B)==target);seen.add(B)
 ck(len(seen)==2**n);tensors+=1
print(json.dumps({'exact_assertions':checks,'finite_sets':sets,'exact_probability_windows':windows,'tensor_cases':tensors,'infinite_probabilistic_claims_tested':False},indent=2))
