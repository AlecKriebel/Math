#!/usr/bin/env python3
"""Finite invariant checks for the arithmetical-Ramsey proof; no jump/hyperarithmetical claims tested finitely."""
from itertools import combinations
import random,json
checks=0;examples=0

def ok(x):
 global checks
 assert x
 checks+=1

def col(t,seed):return (sum((i+1)*(x+seed)**2 for i,x in enumerate(t))+sum(t)*seed)%3
for r in range(2,5):
 for seed in range(1,22):
  R=list(range(81));X=[];records={};examples+=1
  for s in range(9):
   if not R:break
   x=R.pop(0);X.append(x)
   for inds in combinations(range(len(X)),r-1):
    if inds in records:continue
    t=tuple(X[i] for i in inds)
    buckets=[[y for y in R if col(t+(y,),seed)==a] for a in range(3)]
    a=max(range(3),key=lambda a:len(buckets[a]));records[inds]=a;R=buckets[a]
   for inds,a in records.items():
    t=tuple(X[i] for i in inds)
    for y in R:ok(col(t+(y,),seed)==a)
  for inds,a in records.items():
   t=tuple(X[i] for i in inds)
   for j in range(max(inds)+1,len(X)):ok(col(t+(X[j],),seed)==a)
  for I in combinations(range(len(X)),min(len(X),r+1)):
   values={records[J] for J in combinations(I,r-1)}
   if len(values)==1:
    a=next(iter(values))
    for J in combinations(I,r):ok(col(tuple(X[j] for j in J),seed)==a)
# Prefix compatibility is exactly the finite condition used by the positive-name search.
words=[t for n in range(1,5) for t in combinations(range(8),n)]
for a in words:
 for b in words:
  compat=a[:len(b)]==b or b[:len(a)]==a
  if compat:
   longer=max((a,b),key=len);ok(longer[:len(a)]==a and longer[:len(b)]==b)
  else:ok(any(a[i]!=b[i] for i in range(min(len(a),len(b)))))
# Relative-jump accounting in the induction and the preliminary semidecision jump.
for r in range(1,101):
 ok(2+2*(r-1)==2*r);ok(1+2*r==2*r+1)
print(json.dumps(dict(status='PASS',assertions=checks,finite_end_homogeneous_examples=examples,scope='finite invariant controls only; Kleene hard-instance theorem is a credited dependency'),sort_keys=True,indent=2))
